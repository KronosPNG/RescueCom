import base64
import datetime
from typing import Optional, Tuple, Dict, Any

import requests
from flask import request, jsonify

import cloud
from cloud.clientDTO import ClientDTO
from common.models import enc_emergency, user
from common.models.emergency import Emergency
from common.services import crypto
from cloud import persistence, app


def get_validated_json() -> Tuple[Optional[Dict[str, Any]], Optional[Tuple[Any, int]]]:
    """Extract and validate JSON data from request"""
    data: Optional[Dict[str, Any]] = request.get_json()
    if not data:
        return None, (jsonify({'error': 'No JSON data provided'}), 400)
    return data, None


def extract_emergency_fields(data: Dict[str, Any]) -> Tuple[
    Optional[enc_emergency.EncryptedEmergency], Optional[Tuple[Any, int]]]:
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


def create_user_from_data(data: Dict[str, Any]) -> Tuple[Optional[user.User], Optional[Tuple[Any, int]]]:
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
def emergency_submit() -> Tuple[Any, int]:
    """Submit an emergency"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            return error_response

        encrypted_emergency, error_response = extract_emergency_fields(data)
        if error_response:
            return error_response

        client: ClientDTO = cloud.CLIENTS[encrypted_emergency.user_uuid]
        decrypted_blob: bytes = crypto.decrypt(client.dec_cipher, client.nonce, encrypted_emergency.blob, b"")  # TODO: align with client about aad
        emergency: Emergency = Emergency.unpack(encrypted_emergency.emergency_id,
                                                encrypted_emergency.user_uuid,
                                     decrypted_blob)

        return jsonify({'message': 'Emergency submitted successfully', 'data': data}), 200
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/emergency/accept', methods=['POST'])
def emergency_accept() -> Tuple[Any, int]:
    """Accept an emergency"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            return error_response

        encrypted_emergency, error_response = extract_emergency_fields(data)
        if error_response:
            return error_response

        persistence.save_encrypted_emergency(encrypted_emergency)

        # Send a message to the rescuee associated with the request
        user_uuid: str = encrypted_emergency.user_uuid
        if user_uuid in cloud.CLIENTS:
            client: ClientDTO = cloud.CLIENTS[user_uuid]
            # Create notification message
            message: Dict[str, str] = {
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
def emergency_update() -> Tuple[Any, int]:
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
def emergency_delete() -> Tuple[Any, int]:
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


@app.route('/certificate/verify', methods=['POST'])
def certificate_verify() -> Tuple[Any, int]:
    """Verify a certificate with nonce and signature"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            return error_response

        # Extract fields from request data
        certificate: Optional[str] = data.get('certificate')
        nonce: Optional[str] = data.get('nonce')
        signature: Optional[str] = data.get('signature')

        # Validate required fields
        if not certificate or not nonce or not signature:
            return jsonify({'error': 'Missing required fields: certificate, nonce, and signature'}), 400

        # TODO: Implement certificate verification logic
        # Verify the certificate against trusted CA
        # Verify the signature using the certificate's public key and nonce

        # For now, return a placeholder response with public key
        return jsonify({'message': 'Certificate verified successfully', 'pkey': 'placeholder_public_key'}), 200
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/publickey/register', methods=['POST'])
def publickey_register() -> Tuple[Any, int]:
    try:
        data, error_response = get_validated_json()
        if error_response:
            return error_response

        # Extract fields from request data
        public_key: Optional[str] = data.get('public_key')

        # Validate required fields
        if not public_key:
            return jsonify({'error': 'Missing required field: public_key'}), 400

        # TODO: Implement logic to save or update user with public key

        return jsonify({'message': 'Public key registered successfully', 'data': data}), 200
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/user/save', methods=['POST'])
def user_save() -> Tuple[Any, int]:
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
def user_update() -> Tuple[Any, int]:
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
def user_delete() -> Tuple[Any, int]:
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
