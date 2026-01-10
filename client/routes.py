import base64
import json
import os

from pathlib import Path
from typing import Optional, Any

from flask import request, jsonify, Response

import client
from client import app
from common.models.emergency import Emergency
from common.services import crypto
from . import network

CERTIFICATE_PATH = Path(os.getenv("CERTIFICATE_DIR", None)) / Path(os.getenv("CERTIFICATE_NAME", None))
SKEY_PATH = Path(os.getenv("CERTIFICATE_DIR", None)) / Path(os.getenv("SIGNING_KEY_NAME", None))

def get_validated_json() -> tuple[Optional[dict[str, Any]], Optional[tuple[Response, int]]]:
    data: Optional[dict[str, Any]] = request.get_json()

    if not data:
        return None, (jsonify({'error': 'No JSON data provided'}), 400)

    return data, None

def decrypt_message(encrypted_b64: str) -> tuple[Optional[dict[str, Any]], Optional[tuple[Response, int]]]:
    if client.DEC_CIPHER is None or client.NONCE is None or client.CLOUD_NONCE is None:
        return None, (jsonify({'error': 'Client crypto not initialized'}), 500)

    try:
        encrypted_bytes: bytes = base64.b64decode(encrypted_b64.encode())
        decrypted_bytes: bytes = crypto.decrypt(client.DEC_CIPHER, client.CLOUD_NONCE, encrypted_bytes, b"")
        return json.loads(decrypted_bytes.decode()), None

    except (ValueError, json.JSONDecodeError) as e:
        return None, (jsonify({'error': f'Failed to decrypt message: {str(e)}'}), 400)

    except Exception as e:
        return None, (jsonify({'error': f'Decryption error: {str(e)}'}), 500)


@app.route('/notification/receive', methods=['POST'])
def notification_receive() -> tuple[Response, int]:
    """Receive encrypted notifications from cloud"""
    try:
        data, error = get_validated_json()
        if error:
            return error

        message_b64: Optional[str] = data.get('message')
        if not message_b64:
            return jsonify({'error': 'Missing required field: message'}), 400

        message_data, error = decrypt_message(message_b64)
        if error:
            return error

        notification_type: Optional[str] = message_data.get('type')
        if not notification_type:
            return jsonify({'error': 'Missing notification type'}), 400

        # Simple inline handling (cloud-style)
        if notification_type == 'emergency_accepted':
            print(f"Emergency {message_data.get('emergency_id')} accepted")
        elif notification_type == 'emergency_update':
            print(f"Emergency {message_data.get('emergency_id')} updated")
        elif notification_type == 'rescuer_assigned':
            print(f"Rescuer assigned to emergency {message_data.get('emergency_id')}")
        elif notification_type == 'emergency_resolved':
            print(f"Emergency {message_data.get('emergency_id')} resolved")
        else:
            print(f"Unknown notification type: {notification_type}")

        return jsonify({'message': 'Notification received'}), 200

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/emergency/receive', methods=['POST'])
def emergency_receive() -> tuple[Response, int]:
    """Receive encrypted emergency payload (rescuer side)"""
    try:
        data, error = get_validated_json()
        if error:
            return error

        emergency_id: Optional[int] = data.get('emergency_id')
        user_uuid: Optional[str] = data.get('user_uuid')
        blob_b64: Optional[str] = data.get('blob')
        severity: Optional[int] = data.get('severity')

        if not emergency_id or not user_uuid or not blob_b64:
            return jsonify({
                'error': 'Missing required fields: emergency_id, user_uuid, blob'
            }), 400

        if client.DEC_CIPHER is None or client.NONCE is None or client.CLOUD_NONCE is None:
            return jsonify({'error': 'Client crypto not initialized'}), 500

        encrypted_blob: bytes = base64.b64decode(blob_b64.encode())
        decrypted_blob: bytes = crypto.decrypt(client.DEC_CIPHER, client.CLOUD_NONCE, encrypted_blob, b"")

        emergency: Emergency = Emergency.unpack(
            emergency_id,
            user_uuid,
            decrypted_blob
        )

        return jsonify({
            'message': 'Emergency received',
            'emergency_id': emergency.emergency_id,
            'severity': severity
        }), 200

    except ValueError as e:
        return jsonify({'error': f'Failed to unpack emergency: {str(e)}'}), 400

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/emergency/status', methods=['POST'])
def emergency_status() -> tuple[Response, int]:
    """Receive encrypted emergency status update"""
    try:
        data, error = get_validated_json()
        if error:
            return error

        message_b64: Optional[str] = data.get('message')
        if not message_b64:
            return jsonify({'error': 'Missing required field: message'}), 400

        message_data, error = decrypt_message(message_b64)
        if error:
            return error

        emergency_id: Optional[int] = message_data.get('emergency_id')
        status: Optional[str] = message_data.get('status')
        timestamp: Optional[str] = message_data.get('timestamp')

        if not emergency_id or not status:
            return jsonify({'error': 'Missing emergency_id or status'}), 400

        return jsonify({
            'message': 'Status update received',
            'emergency_id': emergency_id,
            'status': status,
            'timestamp': timestamp
        }), 200

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/rescuer/assignment', methods=['POST'])
def rescuer_assignment() -> tuple[Response, int]:
    """Receive encrypted rescuer assignment"""
    try:
        data, error = get_validated_json()
        if error:
            return error

        message_b64: Optional[str] = data.get('message')
        if not message_b64:
            return jsonify({'error': 'Missing required field: message'}), 400

        message_data, error = decrypt_message(message_b64)
        if error:
            return error

        emergency_id: Optional[int] = message_data.get('emergency_id')
        if not emergency_id:
            return jsonify({'error': 'Missing emergency_id'}), 400

        return jsonify({
            'message': 'Assignment received',
            'emergency_id': emergency_id
        }), 200

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/', methods=['GET'])
def homepage() -> tuple[Response, int]:
    """Initialize connection"""
    try:
        ec, dc, nonce, c_nonce = network.connect(client.UUID, SKEY_PATH, CERTIFICATE_PATH)

        client.ENC_CIPHER = ec
        client.DEC_CIPHER = dc
        client.NONCE = nonce
        client.CLOUD_NONCE = c_nonce

        return jsonify({
            'message': 'Cloud connection successful'
        }), 200

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
