import base64
import os
import uuid
from pathlib import Path

import cloud
import requests

from cloud import clientDTO
# from clientDTO import ClientDTO

from common.models import db, emergency, enc_emergency
from common.services import crypto, emergency_queue

# TODO: do better
CERTIFICATE_PATH = os.getenv("CERTIFICATE_PATH", "./certificates/cert.pem")


def broadcast_emergency_to_rescuers(emergency: emergency.Emergency):
    """
    Multicast an emergency to available Rescuers

    Args:
        emergency (Emergency): emergency to send to Rescuers
    """

    for rescuer in cloud.RESCUERS.values():
        if rescuer.busy:
            continue

        encrypted_emergency = enc_emergency.EncryptedEmergency(
            emergency_id=emergency.emergency_id,
            user_uuid=emergency.user_uuid,
            severity=emergency.severity,
            routing_info_json="",  # unnecessary in this case
            blob=crypto.encrypt(
                rescuer.enc_cipher, rescuer.nonce, emergency.pack(), b""
            ),
            created_at=emergency.created_at,
        )

        resp = requests.post(
            rescuer.ip + "/ask/vittorio",
            json={
                "encrypted_emergency": base64.b64encode(
                    str(encrypted_emergency.to_db_tuple()).encode()
                )
            },
        )
        if not resp.ok:
            continue

        if resp.json()["accepted"]:
            rescuer.busy = True
            break


def sync_new_emergency(
    queue: emergency_queue.EmergencyQueue,
    emergency: emergency.Emergency | enc_emergency.EncryptedEmergency,
) -> None:
    """
    Synchronizes a new emergency with the priority queue.

    This function adds a newly received emergency to the given
    `EmergencyQueue` in order to evaluate its priority and urgency relative
    to other unresolved emergencies already in the queue.

    Args:
        queue (EmergencyQueue): The emergency priority queue used to manage
            unresolved emergencies.
        emergency (Emergency | EncryptedEmergency): The emergency instance to
            be synchronized and queued.
    """

    queue.push_emergency(emergency)


def establish_connection(client_uuid: uuid.UUID, client_ip: str, client_nonce: bytes):
    """
    Establish a connection with a client by performing key exchange

    Args:
        client_uuid (UUID): client's uuid
        client_ip (str): client's ip address
        client_nonce (bytes): client's nonce for the session
    Raises:
        TypeError: if any argument is of the wrong type
    """

    if not isinstance(client_ip, str) or not isinstance(client_nonce, bytes):
        raise TypeError("Wrong types for arguments")

    certificate = crypto.load_certificate(Path(CERTIFICATE_PATH))

    nonce = os.urandom(12)

    skey, pkey = crypto.gen_ecdh_keys()

    signature = crypto.sign(skey, nonce)

    resp = requests.post(
        client_ip + "/certificate/verify",
        json={"certificate": certificate, "nonce": nonce, "signature": signature},
    )
    if not resp.ok:
        raise requests.RequestException("Request failed")

    # raises KeyError
    client_pkey_bytes = resp.json()["pkey"]

    # raises ValueError
    client_pkey = crypto.decode_ecdh_pkey(client_pkey_bytes)

    encoded_pkey = crypto.encode_ecdh_pkey(pkey)
    resp = requests.post(
        client_ip + "/publickey/register", json={"public_key": encoded_pkey}
    )

    key = crypto.derive_shared_key(skey, client_pkey)

    enc_cipher, dec_cipher = crypto.get_ciphers(key)

    cloud.CLIENTS[client_uuid] = clientDTO.ClientDTO(client_ip, enc_cipher, dec_cipher, nonce, client_nonce, False)

    user = db.DatabaseManager.get_instance().get_user_by_uuid(str(client_uuid))

    if user is not None and user.is_rescuer:
        cloud.RESCUERS[client_uuid] = clientDTO.ClientDTO(client_ip, enc_cipher, dec_cipher, nonce, client_nonce, True)
