import base64
import datetime
import os
import requests

from pathlib import Path

from typing import Optional, Any
from flask import request, jsonify

import cloud
from cloud.clientDTO import ClientDTO
from common.models import enc_emergency, user
from common.models.emergency import Emergency
from common.services import crypto
from cloud import persistence, app


CERTIFICATE_PATH = Path(os.getenv("CERTIFICATE_DIR", None)) / Path(os.getenv("CERTIFICATE_NAME", None))
SIGNING_KEY_PATH = Path(os.getenv("CERTIFICATE_DIR", None)) / Path(os.getenv("SIGNING_KEY_NAME", None))



def get_validated_json() -> tuple[Optional[dict[str, Any]], Optional[tuple[Any, int]]]:
    """Extract and validate JSON data from request"""
    data: Optional[dict[str, Any]] = request.get_json()
    if not data:
        return None, (jsonify({'error': 'No JSON data provided'}), 400)
    return data, None


def extract_emergency_fields(data: dict[str, Any]) -> tuple[
    Optional[enc_emergency.EncryptedEmergency], Optional[tuple[Any, int]]]:
    """Extract and validate emergency fields from request data"""
    emergency_id: Optional[int] = data.get('emergency_id')
    user_uuid: Optional[str] = data.get('user_uuid')
    routing_info_json: Optional[str] = data.get('routing_info_json')
    blob: Optional[bytes] = data.get('blob')
    severity: Optional[int] = data.get('severity')

    # Validate required fields
    if not emergency_id or not user_uuid:
        return None, (jsonify({'error': 'Missing required fields: emergency_id and user_uuid'}), 400)

    # Create EncryptedEmergency instance
    encrypted_emergency: enc_emergency.EncryptedEmergency = enc_emergency.EncryptedEmergency(
        emergency_id=emergency_id,
        user_uuid=user_uuid,
        severity=severity,
        created_at=datetime.datetime.now(),
        routing_info_json=routing_info_json,
        blob=blob
    )

    return encrypted_emergency, None


def create_user_from_data(data: dict[str, Any]) -> tuple[Optional[user.User], Optional[tuple[Any, int]]]:
    """Extract and validate user fields from request data"""
    # Validate required fields
    required_fields: list[str] = ['uuid', 'is_rescuer', 'name', 'surname', 'birthday', 'blood_type']
    missing_fields: list[str] = [field for field in required_fields if field not in data or data.get(field) is None]
    if missing_fields:
        return None, (jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400)

    try:
        new_user: user.User = user.User(
            uuid=data.get('uuid'),
            is_rescuer=data.get('is_rescuer'),
            name=data.get('name'),
            surname=data.get('surname'),
            birthday=data.get('birthday'),
            blood_type=data.get('blood_type'),
            health_info_json=data.get('health_info_json')
        )
        return new_user, None
    except (ValueError, TypeError) as e:
        return None, (jsonify({'error': f'Invalid data format: {str(e)}'}), 400)


@app.route('/emergency/submit', methods=['POST'])
def emergency_submit() -> tuple[Any, int]:
    """Submit an emergency"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            return error_response

        encrypted_emergency, error_response = extract_emergency_fields(data)
        if error_response:
            return error_response

        client = None
        with cloud.status_lock:
            client = cloud.CLIENTS[encrypted_emergency.user_uuid]

        if not client:
            raise Exception("Client not found")

        decrypted_blob: bytes = crypto.decrypt(client.dec_cipher, client.nonce, encrypted_emergency.blob, b"")  # TODO: align with client about aad
        emergency: Emergency = Emergency.unpack(encrypted_emergency.emergency_id,
                                                encrypted_emergency.user_uuid,
                                     decrypted_blob)

        return jsonify({'message': 'Emergency submitted successfully', 'data': data}), 200
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/emergency/accept', methods=['POST'])
def emergency_accept() -> tuple[Any, int]:
    """Accept an emergency"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            return error_response

        encrypted_emergency, error_response = extract_emergency_fields(data)
        if error_response:
            return error_response

        rescuer = None
        with cloud.status_lock:
            if data["uuid"] in cloud.RESCUERS:
                rescuer = cloud.RESCUERS[data["uuid"]]

        if not rescuer:
            raise Exception("Rescuer uuid not found")

        # Send a message to the Rescuee associated with the request
        user_uuid: str = encrypted_emergency.user_uuid

        with cloud.status_lock:
            if user_uuid in cloud.CLIENTS:
                client: ClientDTO = cloud.CLIENTS[user_uuid]
            else:
                raise Exception("Client couldn't be found")

        decrypted_blob: bytes = crypto.decrypt(rescuer.dec_cipher, rescuer.nonce, encrypted_emergency.blob, b"")  # TODO: align with client about aad

        # Create notification message
        message: dict[str, str] = {
            "type": "emergency_accepted",
            "emergency_id": encrypted_emergency.emergency_id,
            "timestamp": datetime.datetime.now().isoformat()
        }

        # Encrypt the message for the client
        encrypted_message: bytes = crypto.encrypt(
            encrypted_emergency, client.cloud_nonce,
            str(message).encode(), b""  # No additional authenticated data for now
        )

        # Send message to the client
        try:
            requests.post(
                client.ip + "/notification/receive",
                json={
                    "message": base64.b64encode(encrypted_message).decode(),
                },
                timeout=3  # Short timeout to avoid blocking
            )
        except Exception as msg_err:
            # Log the error but continue with the main request
            app.logger.error(f"Failed to send notification: {str(msg_err)}")

        return jsonify({'message': 'Emergency accepted successfully', 'data': data}), 200

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/emergency/update', methods=['POST'])
def emergency_update() -> tuple[Any, int]:
    """Update an emergency"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            return error_response

        encrypted_emergency, error_response = extract_emergency_fields(data)
        if error_response:
            return error_response

        persistence.update_encrypted_emergency(encrypted_emergency.user_uuid, encrypted_emergency.emergency_id,
                                               encrypted_emergency)

        return jsonify({'message': 'Emergency updated successfully', 'data': data}), 200
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/emergency/delete', methods=['POST'])
def emergency_delete() -> tuple[Any, int]:
    """Delete an emergency"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            return error_response

        # Extract fields from request data
        user_uuid: Optional[str] = data.get('user_uuid')
        emergency_id: Optional[int] = data.get('emergency_id')

        # Validate required fields
        if not user_uuid or not emergency_id:
            return jsonify({'error': 'Missing required fields: user_uuid and emergency_id'}), 400

        # Delete the emergency from the database
        persistence.delete_encrypted_emergency(user_uuid, emergency_id)

        return jsonify({'message': 'Emergency deleted successfully', 'data': data}), 200
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/user/save', methods=['POST'])
def user_save() -> tuple[Any, int]:
    """Save a user"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            return error_response

        new_user, error_response = create_user_from_data(data)
        if error_response:
            return error_response

        persistence.save_user(new_user)
        return jsonify({'message': 'User saved successfully', 'data': data}), 200
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/user/update', methods=['POST'])
def user_update() -> tuple[Any, int]:
    """Update a user"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            return error_response

        updated_user, error_response = create_user_from_data(data)
        if error_response:
            return error_response

        persistence.update_user(updated_user.uuid, updated_user)
        return jsonify({'message': 'User updated successfully', 'data': data}), 200
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/user/delete', methods=['POST'])
def user_delete() -> tuple[Any, int]:
    """Delete a user"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            return error_response

        uuid: Optional[str] = data.get('uuid')

        # Validate required fields
        if not uuid:
            return jsonify({'error': 'Missing required field: uuid'}), 400

        persistence.delete_user(uuid)
        return jsonify({'message': 'User deleted successfully', 'uuid': uuid}), 200
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/connect', methods=['POST'])
def connect() -> tuple[Any, int]:
    """Connect with a client"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            return error_response

        uuid: Optional[str] = data.get('uuid')
        cert_bytes: Optional[bytes] = data.get('certificate')
        client_nonce: Optional[bytes] = data.get('nonce')
        signature: Optional[str] = data.get('signature')

        # Validate required fields
        if not uuid or not cert_bytes or not client_nonce or not signature:
            return jsonify({'error': 'Missing required fields'}), 400

        client_certificate = crypto.decode_certificate(cert_bytes)
        if not crypto.verify_certificate(client_certificate, signature, client_nonce):
            return jsonify({'error': 'Couldn\'t verify certificate or signature'}), 400

        certificate = crypto.load_certificate(CERTIFICATE_PATH)
        certificate_bytes = crypto.encode_certificate(certificate)
        nonce = os.urandom(12)
        skey = crypto.load_signing_key(SIGNING_KEY_PATH)
        signature = crypto.sign(skey, nonce)

        with cloud.status_lock:
            cloud.CLIENTS[uuid] = ClientDTO(
                    request.remote_addr,
                    None, None, client_nonce, nonce,
                    True, # TODO: how do we identify Rescuers?
                    )

        return jsonify({'message': 'Verification successful', 'certificate': certificate_bytes, 'nonce': nonce, 'signature': signature}), 200
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/pkey', methods=['POST'])
def pkey() -> tuple[Any, int]:
    """Connect with a client"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            return error_response

        uuid: Optional[str] = data.get('uuid')
        pkey_bytes: Optional[str] = data.get('public_key')

        # Validate required fields
        if not uuid or not pkey_bytes:
            return jsonify({'error': 'Missing required fields'}), 400

        client_pkey = crypto.decode_ecdh_pkey(pkey_bytes)

        skey, pkey = gen_ecdh_keys()

        key = derive_shared_key(skey, client_pkey)

        enc_cipher, dec_cipher = get_ciphers(key)

        with cloud.status_lock:
            if not uuid in cloud.CLIENTS:
                raise Exception("Perform certificate verification first")

            cloud.CLIENTS[uuid].enc_cipher = enc_cipher
            cloud.CLIENTS[uuid].dec_cipher = dec_cipher

        return jsonify({'message': 'Key exchange completed', 'pkey': crypto.encode_ecdh_pkey(pkey)}), 200
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
