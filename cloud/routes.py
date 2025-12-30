from flask import request, jsonify
from common.models import enc_emergency, user, db
from common.services.crypto import decrypt
from cloud import persistence
from cloud.app import app


def get_validated_json() -> tuple:
    """Extract and validate JSON data from request"""
    data = request.get_json()
    if not data:
        return None, (jsonify({'error': 'No JSON data provided'}), 400)
    return data, None


def extract_emergency_fields(data: dict) -> tuple:
    """Extract and validate emergency fields from request data"""
    emergency_id = data.get('emergency_id')
    user_uuid = data.get('user_uuid')
    routing_info_json = data.get('routing_info_json')
    blob = data.get('blob')

    # Validate required fields
    if not emergency_id or not user_uuid:
        return None, (jsonify({'error': 'Missing required fields: emergency_id and user_uuid'}), 400)

    # Create EncryptedEmergency instance
    encrypted_emergency = enc_emergency.EncryptedEmergency(
        emergency_id=emergency_id,
        user_uuid=user_uuid,
        routing_info_json=routing_info_json,
        blob=blob
    )

    return encrypted_emergency, None


@app.route('/emergency/submit', methods=['POST'])
def emergency_submit() -> tuple:
    """Submit an emergency"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            return error_response

        encrypted_emergency, error_response = extract_emergency_fields(data)
        if error_response:
            return error_response

        client = app.CLIENTS[encrypted_emergency.get('user_uuid')]
        decrypted_blob = decrypt(client.dec_cipher, client.nonce, blob, b"") # TODO: align with client about aad
        emergency = Emergency.unpack(encrypted_emergency.emergency_id,
                                     encrypted_emergency.user_uuid,
                                     decrypted_blob)

        return jsonify({'message': 'Emergency submitted successfully', 'data': data}), 200
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/emergency/accept', methods=['POST'])
def emergency_accept() -> tuple:
    """Accept an emergency"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            return error_response

        encrypted_emergency, error_response = extract_emergency_fields(data)
        if error_response:
            return error_response

        persistence.save_encrypted_emergency(encrypted_emergency)

        return jsonify({'message': 'Emergency accepted successfully', 'data': data}), 200
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/emergency/update', methods=['POST'])
def emergency_update() -> tuple:
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
def emergency_delete() -> tuple:
    """Delete an emergency"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            return error_response

        # Extract fields from request data
        user_uuid = data.get('user_uuid')
        emergency_id = data.get('emergency_id')

        # Validate required fields
        if not user_uuid or not emergency_id:
            return jsonify({'error': 'Missing required fields: user_uuid and emergency_id'}), 400

        # Delete the emergency from the database
        persistence.delete_request(user_uuid, emergency_id)

        return jsonify({'message': 'Emergency deleted successfully', 'data': data}), 200
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/certificate/verify', methods=['POST'])
def certificate_verify() -> tuple:
    """Verify a certificate with nonce and signature"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            return error_response

        # Extract fields from request data
        certificate = data.get('certificate')
        nonce = data.get('nonce')
        signature = data.get('signature')

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
def publickey_register() -> tuple:
    try:
        data, error_response = get_validated_json()
        if error_response:
            return error_response

        # Extract fields from request data
        public_key = data.get('public_key')

        # Validate required fields
        if not public_key:
            return jsonify({'error': 'Missing required field: public_key'}), 400

        # TODO: Implement logic to save or update user with public key

        return jsonify({'message': 'Public key registered successfully', 'data': data}), 200
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/user/save', methods=['POST'])
def user_save() -> tuple:
    """Save a user"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            return error_response

        # Validate required fields
        required_fields = ['uuid', 'is_rescuer', 'name', 'surname', 'birthday', 'blood_type']
        missing_fields = [field for field in required_fields if field not in data or data.get(field) is None]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        new_user = user.User(
            uuid=data.get('uuid'),
            is_rescuer=data.get('is_rescuer'),
            name=data.get('name'),
            surname=data.get('surname'),
            birthday=data.get('birthday'),
            blood_type=data.get('blood_type'),
            health_info_json=data.get('health_info_json')
        )

        persistence.save_user(new_user)
        return jsonify({'message': 'User saved successfully', 'data': data}), 200
    except (ValueError, TypeError) as e:
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/user/update', methods=['POST'])
def user_update() -> tuple:
    """Update a user"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            return error_response

        uuid = data.get('uuid')

        # Validate required fields
        required_fields = ['uuid', 'is_rescuer', 'name', 'surname', 'birthday', 'blood_type']
        missing_fields = [field for field in required_fields if field not in data or data.get(field) is None]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        updated_user = user.User(
            uuid=uuid,
            is_rescuer=data.get('is_rescuer'),
            name=data.get('name'),
            surname=data.get('surname'),
            birthday=data.get('birthday'),
            blood_type=data.get('blood_type'),
            health_info_json=data.get('health_info_json')
        )

        persistence.update_user(uuid, updated_user)
        return jsonify({'message': 'User updated successfully', 'data': data}), 200
    except (ValueError, TypeError) as e:
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/user/delete', methods=['POST'])
def user_delete() -> tuple:
    """Delete a user"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            return error_response

        uuid = data.get('uuid')

        # Validate required fields
        if not uuid:
            return jsonify({'error': 'Missing required field: uuid'}), 400

        persistence.delete_user(uuid)
        return jsonify({'message': 'User deleted successfully', 'uuid': uuid}), 200
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
