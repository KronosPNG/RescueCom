import base64
import cloud
import requests

from cloud import clientDTO

from common.models import emergency, enc_emergency
from common.services import crypto, emergency_queue

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
