from flask import request, jsonify
from common.models import enc_emergency
from cloud import persistence
from cloud.app import app


@app.route('/request/forward', methods=['POST'])
def request_forward() -> tuple:
    """Forward a request"""
    data = request.get_json()
    # TODO: get parameters from the request and forward the corresponding request
    # if rescuee_id and rescuer_id are not None, forward the request to the rescuer
    return jsonify({'message': 'Request forwarded successfully', 'data': data}), 200

@app.route('/request/accept', methods=['POST'])
def request_accept() -> tuple:
    """Accept a request"""
    data = request.get_json()

    # Extract fields from request data
    emergency_id = data.get('emergency_id')
    user_uuid = data.get('user_uuid')
    routing_info_json = data.get('routing_info_json')
    blob = data.get('blob')

    # Create EncryptedEmergency instance and save to database
    encrypted_emergency = enc_emergency.EncryptedEmergency(
        emergency_id=emergency_id,
        user_uuid=user_uuid,
        routing_info_json=routing_info_json,
        blob=blob
    )

    persistence.save_encrypted_emergency(encrypted_emergency)

    return jsonify({'message': 'Request accepted successfully', 'data': data}), 200


@app.route('/request/update', methods=['POST'])
def request_update() -> tuple:
    """Update a request"""
    data = request.get_json()

    # Extract fields from request data
    emergency_id = data.get('emergency_id')
    user_uuid = data.get('user_uuid')
    routing_info_json = data.get('routing_info_json')
    blob = data.get('blob')

    # Create EncryptedEmergency instance and update in database
    encrypted_emergency = enc_emergency.EncryptedEmergency(
        emergency_id=emergency_id,
        user_uuid=user_uuid,
        routing_info_json=routing_info_json,
        blob=blob
    )

    persistence.update_encrypted_emergency(user_uuid, emergency_id, encrypted_emergency)

    return jsonify({'message': 'Request updated successfully', 'data': data}), 200


@app.route('/request/delete', methods=['POST'])
def request_delete() -> tuple:
    """Delete a request"""
    data = request.get_json()

    # Extract fields from request data
    user_uuid = data.get('user_uuid')
    emergency_id = data.get('emergency_id')

    # Delete the request from the database
    persistence.delete_request(user_uuid, emergency_id)

    return jsonify({'message': 'Request deleted successfully', 'data': data}), 200


@app.route('/certificate/verify', methods=['POST'])
def certificate_verify() -> tuple:
    """Verify a certificate with nonce and signature"""
    data = request.get_json()

    # Extract fields from request data
    certificate = data.get('certificate')
    nonce = data.get('nonce')
    signature = data.get('signature')

    # TODO: Implement certificate verification logic
    # Verify the certificate against trusted CA
    # Verify the signature using the certificate's public key and nonce

    # For now, return a placeholder response with public key
    return jsonify({'message': 'Certificate verified successfully', 'pkey': 'placeholder_public_key'}), 200

@app.route('/publickey/register', methods=['POST'])
def publickey_register() -> tuple:
    data = request.get_json()

    # Extract fields from request data
    public_key = data.get('public_key')

    # TODO: Implement logic to save or update user with public key

    return jsonify({'message': 'Public key registered successfully', 'data': data}), 200
