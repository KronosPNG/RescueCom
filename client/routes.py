import base64
import json
from typing import Any, Callable, Dict, Optional, Tuple

from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV
from flask import request, jsonify, Response

from client import app
from common.models.emergency import Emergency
from common.services import crypto

# Type aliases for clarity
JsonResponse = Tuple[Response, int]
ValidationResult = Tuple[Optional[Dict[str, Any]], Optional[JsonResponse]]

# Client state (should be initialized during app setup)
_DEC_CIPHER: Optional[AESGCMSIV] = None
_NONCE: Optional[bytes] = None

# Notification handlers registry
_NOTIFICATION_HANDLERS: Dict[str, Callable[[Dict[str, Any]], None]] = {}


def init_client_crypto(dec_cipher: AESGCMSIV, nonce: bytes) -> None:
    """Initialize the client's cryptographic state."""
    global _DEC_CIPHER, _NONCE
    _DEC_CIPHER = dec_cipher
    _NONCE = nonce


def register_notification_handler(notification_type: str, handler: Callable[[Dict[str, Any]], None]) -> None:
    """Register a handler for a specific notification type."""
    _NOTIFICATION_HANDLERS[notification_type] = handler


# --- Validation Helpers (DRY) ---

def get_validated_json() -> ValidationResult:
    """Extract and validate JSON data from request."""
    data: Optional[Dict[str, Any]] = request.get_json()
    if not data:
        return None, (jsonify({'error': 'No JSON data provided'}), 400)
    return data, None


def validate_required_fields(data: Dict[str, Any], required_fields: list[str]) -> Optional[JsonResponse]:
    """Validate that all required fields are present in the data."""
    missing_fields: list[str] = [
        field for field in required_fields
        if field not in data or data.get(field) is None
    ]
    if missing_fields:
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
    return None


def decrypt_message(encrypted_b64: str) -> Tuple[Optional[Dict[str, Any]], Optional[JsonResponse]]:
    """Decrypt a base64-encoded encrypted message."""
    if _DEC_CIPHER is None or _NONCE is None:
        return None, (jsonify({'error': 'Client crypto not initialized'}), 500)

    try:
        encrypted_bytes: bytes = base64.b64decode(encrypted_b64)
        decrypted_bytes: bytes = crypto.decrypt(_DEC_CIPHER, _NONCE, encrypted_bytes, b"")
        message_data: Dict[str, Any] = json.loads(decrypted_bytes.decode('utf-8'))
        return message_data, None
    except (ValueError, json.JSONDecodeError) as e:
        return None, (jsonify({'error': f'Failed to decrypt message: {str(e)}'}), 400)
    except Exception as e:
        return None, (jsonify({'error': f'Decryption error: {str(e)}'}), 500)


def create_success_response(message: str, data: Optional[Dict[str, Any]] = None) -> JsonResponse:
    """Create a standardized success response."""
    response: Dict[str, Any] = {'message': message}
    if data:
        response['data'] = data
    return jsonify(response), 200


def create_error_response(error: str, status_code: int = 500) -> JsonResponse:
    """Create a standardized error response."""
    return jsonify({'error': error}), status_code


def route_handler(func: Callable[..., JsonResponse]) -> Callable[..., JsonResponse]:
    """Decorator that wraps route handlers with standard error handling."""
    def wrapper(*args: Any, **kwargs: Any) -> JsonResponse:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return create_error_response(f'Internal server error: {str(e)}')
    wrapper.__name__ = func.__name__
    return wrapper


# --- Notification Handlers ---

def handle_emergency_accepted(data: Dict[str, Any]) -> None:
    """Handle emergency_accepted notification."""
    emergency_id: Optional[int] = data.get('emergency_id')
    timestamp: Optional[str] = data.get('timestamp')
    print(f"Emergency {emergency_id} accepted at {timestamp}")


def handle_emergency_update(data: Dict[str, Any]) -> None:
    """Handle emergency_update notification."""
    emergency_id: Optional[int] = data.get('emergency_id')
    print(f"Emergency {emergency_id} updated")


def handle_rescuer_assigned(data: Dict[str, Any]) -> None:
    """Handle rescuer_assigned notification."""
    emergency_id: Optional[int] = data.get('emergency_id')
    print(f"Rescuer assigned to emergency {emergency_id}")


def handle_emergency_resolved(data: Dict[str, Any]) -> None:
    """Handle emergency_resolved notification."""
    emergency_id: Optional[int] = data.get('emergency_id')
    print(f"Emergency {emergency_id} resolved")


# Register default handlers
register_notification_handler('emergency_accepted', handle_emergency_accepted)
register_notification_handler('emergency_update', handle_emergency_update)
register_notification_handler('rescuer_assigned', handle_rescuer_assigned)
register_notification_handler('emergency_resolved', handle_emergency_resolved)


# --- Routes ---

@app.route('/notification/receive', methods=['POST'])
@route_handler
def notification_receive() -> JsonResponse:
    """Receive and process encrypted notifications from the server."""
    data, error = get_validated_json()
    if error:
        return error

    error = validate_required_fields(data, ['message'])
    if error:
        return error

    message_data, error = decrypt_message(data['message'])
    if error:
        return error

    notification_type: Optional[str] = message_data.get('type')
    if not notification_type:
        return create_error_response('Missing notification type', 400)

    handler: Optional[Callable[[Dict[str, Any]], None]] = _NOTIFICATION_HANDLERS.get(notification_type)
    if handler:
        handler(message_data)
    else:
        print(f"Unknown notification type: {notification_type}")

    return create_success_response('Notification received')


@app.route('/emergency/receive', methods=['POST'])
@route_handler
def emergency_receive() -> JsonResponse:
    """Receive emergency data from the server (for rescuers)."""
    data, error = get_validated_json()
    if error:
        return error

    error = validate_required_fields(data, ['emergency_id', 'user_uuid', 'blob'])
    if error:
        return error

    emergency_id: int = data['emergency_id']
    user_uuid: str = data['user_uuid']
    encrypted_blob_b64: str = data['blob']
    severity: Optional[int] = data.get('severity')

    if _DEC_CIPHER is None or _NONCE is None:
        return create_error_response('Client crypto not initialized')

    try:
        encrypted_blob: bytes = base64.b64decode(encrypted_blob_b64)
        decrypted_blob: bytes = crypto.decrypt(_DEC_CIPHER, _NONCE, encrypted_blob, b"")
        emergency: Emergency = Emergency.unpack(emergency_id, user_uuid, decrypted_blob)

        return create_success_response('Emergency received', {
            'emergency_id': emergency_id,
            'severity': severity
        })
    except ValueError as e:
        return create_error_response(f'Failed to unpack emergency: {str(e)}', 400)


@app.route('/emergency/status', methods=['POST'])
@route_handler
def emergency_status() -> JsonResponse:
    """Receive emergency status updates from the server."""
    data, error = get_validated_json()
    if error:
        return error

    error = validate_required_fields(data, ['message'])
    if error:
        return error

    message_data, error = decrypt_message(data['message'])
    if error:
        return error

    emergency_id: Optional[int] = message_data.get('emergency_id')
    status: Optional[str] = message_data.get('status')
    timestamp: Optional[str] = message_data.get('timestamp')

    if not emergency_id or not status:
        return create_error_response('Missing emergency_id or status in message', 400)

    return create_success_response('Status update received', {
        'emergency_id': emergency_id,
        'status': status,
        'timestamp': timestamp
    })


@app.route('/rescuer/assignment', methods=['POST'])
@route_handler
def rescuer_assignment() -> JsonResponse:
    """Receive rescuer assignment notification (for rescuers)."""
    data, error = get_validated_json()
    if error:
        return error

    error = validate_required_fields(data, ['message'])
    if error:
        return error

    message_data, error = decrypt_message(data['message'])
    if error:
        return error

    emergency_id: Optional[int] = message_data.get('emergency_id')

    if not emergency_id:
        return create_error_response('Missing emergency_id in message', 400)

    return create_success_response('Assignment received', {
        'emergency_id': emergency_id
    })


@app.route('/health', methods=['GET'])
def health_check() -> JsonResponse:
    """Health check endpoint for the client."""
    return create_success_response('Client is healthy')