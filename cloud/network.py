from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV
from common.models import *
from common.services.crypto import *
import os, requests, uuid, app, struct, base64

# TODO: do better
CERTIFICATE_PATH = os.getenv("CERTIFICATE_PATH", "./certificates/cert.pem")
DB_PATH = os.getenv("DB_PATH", "idk")


def broadcast_emergency_to_rescuers(emergency: emergency.Emergency):
    """
    Multicast an emergency to available Rescuers

    Args:
        emergency (Emergency): emergency to send to Rescuers
    """

    # Utility function
    def pack_str(s: str):
        return struct.pack(f"<I@{}s".format(len(s)), len(s), s.encode())

    for rescuer in app.RESCUERS:
        ip, enc_cipher, dec_cipher, nonce = rescuer

        encrypted_emergency = enc_emergency.EncryptedEmergency(
                emergency.id,
                emergency.user_uuid,
                "", # unnecessary in this case
                encrypt(enc_cipher, nonce,

                        pack_str(emergency.position) +
                        pack_str(emergency.address) +
                        pack_str(emergency.city) +
                        struct.pack("<I", emergency.street_number) +
                        pack_str(emergency.place_description) +
                        pack_str(emergency.photo_b64) +
                        struct.pack("?", emergency.resolved) +
                        pack_str(emergency.details_json),

                        b""
                    )
                )

        requests.post(ip + "/ask/vittorio", json={"encrypted_emergency": base64.b64encode(str(encrypted_emergency.to_db_tuple()))})

def assign_emergency_to_rescuer():
    """
    If more than one Rescuer accepts an emergency, choose one to assign it to
    """

    pass

def sync_new_request():
    """
    Synchronise a new emergency to figure out how important and urgent it is relative to known unresolved emergency
    """

    pass

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

    certificate = load_certificate(CERTIFICATE_PATH)

    nonce = os.urandom(12)

    skey, pkey = gen_ecdh_keys()

    signature = sign(skey, nonce)

    resp = requests.post(client_ip + "/certificate/verify", json={"certificate": cert, "nonce": nonce, "signature": signature})
    if not resp.ok:
        raise requests.RequestException("Request failed")

    # raises KeyError
    client_pkey_bytes = resp.json["pkey"]

    # raises ValueError
    client_pkey = decode_ecdh_pkey(client_pkey_bytes)

    encoded_pkey = encode_ecdh_pkey(pkey)
    resp = requests.post(client_ip + "/publickey/register", json={"public_key": encoded_pkey})

    key = derive_shared_key(skey, client_pkey)

    enc_cipher, dec_cipher = get_ciphers(key)

    app.CLIENTS[client_uuid] = (client_ip, enc_cipher, dec_cipher, client_nonce)

    user = db.DatabaseManager.get_instance(DB_PATH).get_user_by_uuid(str(client_uuid))

    if user is not None and user.is_rescuer:
        app.RESCUERS[client_uuid] = (client_ip, enc_cipher, dec_cipher, client_nonce)
