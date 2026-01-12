import os
import sys
import uuid
import logging
import base64
import requests
import random
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Any

from flask import Flask, render_template, request, redirect, url_for, abort, jsonify, Response
from dotenv import load_dotenv

# Crypto Imports
from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV

# 1. PATH & ENV CONFIGURATION
base_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(base_dir)
sys.path.append(project_root)

# Load environment variables (similar to __init__.py)
load_dotenv(Path(__file__).parent / '.env')

template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')

# 2. BACKEND IMPORTS
try:
    from db import DatabaseManager
    from common.models.user import User, BloodType
    from common.models.emergency import Emergency
    from common.services import crypto
except ImportError as e:
    print(f"CRITICAL: Failed to import backend modules from {project_root}. Error: {e}")
    raise e

# 3. GLOBAL STATE (from __init__.py)
UUID: Optional[str] = None
IS_RESCUER: Optional[bool] = None
DEC_CIPHER: Optional[AESGCMSIV] = None
ENC_CIPHER: Optional[AESGCMSIV] = None
NONCE: Optional[bytes] = None
CLOUD_NONCE: Optional[bytes] = None

# Configuration Paths
DATA_PATH = Path(os.getenv("DATA_FILE", "data.txt"))
# Default to project_root/certs if env vars are missing
cert_dir = os.getenv("CERTIFICATE_DIR", os.path.join(project_root, "certs"))
SKEY_PATH = Path(cert_dir) / Path(os.getenv("SIGNING_KEY_NAME", "client.key"))
CERTIFICATE_PATH = Path(cert_dir) / Path(os.getenv("CERTIFICATE_NAME", "client.crt"))

CLOUD_URL = "http://127.0.0.1:8000"  # Updated to match network.py port

# 4. APP SETUP
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Initialize Database
db_path = os.path.join(project_root, 'rescue.db')
db = DatabaseManager.get_instance(db_path)


# --- INITIALIZATION LOGIC (from __init__.py) ---

def init_info():
    """Initialize UUID and IS_RESCUER from local file if it exists."""
    global UUID, IS_RESCUER

    if not DATA_PATH.exists():
        # If no data file, we wait for registration to set this
        pass
    else:
        try:
            with DATA_PATH.open() as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    UUID = lines[0].strip()
                    IS_RESCUER = lines[1].strip() != '0'
        except Exception as e:
            logger.error(f"Failed to load init info: {e}")


def init_certificate_and_skey():
    """Ensure certificates and keys exist."""
    global SKEY_PATH, CERTIFICATE_PATH

    if not SKEY_PATH.parent.exists():
        SKEY_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not SKEY_PATH.exists() or not CERTIFICATE_PATH.exists():
        logger.info("Generating new certificate and key...")
        skey, certificate = crypto.gen_certificate("IT", "Salerno", "Fisciano", "Luigi Turco")
        crypto.save_certificate(CERTIFICATE_PATH, certificate)
        crypto.save_edkey(SKEY_PATH, skey)
    else:
        # Check validity
        try:
            certificate = crypto.load_certificate(CERTIFICATE_PATH)
            # FIX: Use timezone.utc instead of datetime.UTC
            if certificate.not_valid_after_utc <= datetime.now(timezone.utc):
                logger.info("Certificate expired. Regenerating...")
                skey, certificate = crypto.gen_certificate("IT", "Salerno", "Fisciano", "Luigi Turco")
                crypto.save_certificate(CERTIFICATE_PATH, certificate)
                crypto.save_edkey(SKEY_PATH, skey)
        except Exception as e:
            logger.error(f"Certificate check failed: {e}")

# Run initialization immediately
init_info()
init_certificate_and_skey()


# --- NETWORK & CRYPTO HELPERS (Merged from network.py and app.py) ---

def perform_cloud_handshake():
    """
    Connect to the cloud by performing key exchange.
    Updates global ENC_CIPHER, DEC_CIPHER, NONCE, CLOUD_NONCE.
    """
    global UUID, IS_RESCUER, ENC_CIPHER, DEC_CIPHER, NONCE, CLOUD_NONCE

    if not UUID:
        logger.warning("Cannot connect: UUID not initialized.")
        return False

    try:
        skey = crypto.load_signing_key(SKEY_PATH)
        certificate = crypto.load_certificate(CERTIFICATE_PATH)

        nonce = os.urandom(12)
        signature = crypto.sign(skey, nonce)
        certificate_bytes = crypto.encode_certificate(certificate)

        # 1. Connect
        resp = requests.post(f"{CLOUD_URL}/connect", json={
            "uuid": UUID,
            "nonce": nonce.hex(),
            "certificate": certificate_bytes.hex(),
            "signature": signature.hex(),
            "is_rescuer": IS_RESCUER
        }, timeout=5)

        if not resp.ok:
            raise Exception(f"Connect failed: {resp.status_code}")

        data = resp.json()
        cloud_cert_bytes = bytes.fromhex(data.get("certificate"))
        cloud_nonce = bytes.fromhex(data.get("nonce"))
        cloud_signature = bytes.fromhex(data.get("signature"))

        cloud_certificate = crypto.decode_certificate(cloud_cert_bytes)

        if not crypto.verify_certificate(cloud_certificate, cloud_signature, cloud_nonce):
            raise Exception("Cloud certificate verification failed")

        # 2. Key Exchange
        e_skey, e_pkey = crypto.gen_ecdh_keys()
        encoded_pkey = crypto.encode_ecdh_pkey(e_pkey)

        resp = requests.post(f"{CLOUD_URL}/pkey", json={
            "uuid": UUID,
            "public_key": encoded_pkey.hex()
        }, timeout=5)

        if not resp.ok:
            raise Exception(f"Key exchange failed: {resp.status_code}")

        data = resp.json()
        cloud_pkey = crypto.decode_ecdh_pkey(bytes.fromhex(data.get("pkey")))

        # 3. Derive Keys
        key = crypto.derive_shared_key(e_skey, cloud_pkey)
        enc_cipher, dec_cipher = crypto.get_ciphers(key)

        # Update Globals
        ENC_CIPHER = enc_cipher
        DEC_CIPHER = dec_cipher
        NONCE = nonce
        CLOUD_NONCE = cloud_nonce

        logger.info("Cloud handshake successful.")
        return True

    except Exception as e:
        logger.error(f"Handshake failed: {e}")
        return False


def encrypt_emergency_blob(emergency_obj) -> bytes:
    """Packs and encrypts an emergency object using global ciphers."""
    global ENC_CIPHER, NONCE

    if not ENC_CIPHER or not NONCE:
        logger.warning("Encryption skipped: Client crypto not initialized.")
        return b""

    try:
        packed_data = emergency_obj.pack()
        return crypto.encrypt(ENC_CIPHER, NONCE, packed_data, b"")
    except Exception as e:
        logger.error(f"Encryption error: {e}")
        return b""


def decrypt_message(encrypted_b64: str) -> tuple[Optional[dict[str, Any]], Optional[tuple[Response, int]]]:
    """Helper to decrypt incoming messages using global ciphers."""
    global DEC_CIPHER, CLOUD_NONCE

    if DEC_CIPHER is None or CLOUD_NONCE is None:
        return None, (jsonify({'error': 'Client crypto not initialized'}), 500)

    try:
        encrypted_bytes: bytes = base64.b64decode(encrypted_b64.encode())
        decrypted_bytes: bytes = crypto.decrypt(DEC_CIPHER, CLOUD_NONCE, encrypted_bytes, b"")
        return json.loads(decrypted_bytes.decode()), None
    except Exception as e:
        return None, (jsonify({'error': f'Decryption error: {str(e)}'}), 500)


def get_validated_json() -> tuple[Optional[dict[str, Any]], Optional[tuple[Response, int]]]:
    data: Optional[dict[str, Any]] = request.get_json()
    if not data:
        return None, (jsonify({'error': 'No JSON data provided'}), 400)
    return data, None


def send_to_cloud(endpoint, payload):
    """Helper to post JSON to the cloud."""
    try:
        response = requests.post(f"{CLOUD_URL}{endpoint}", json=payload, timeout=5)
        response.raise_for_status()
        return True
    except Exception as e:
        logger.error(f"Cloud Sync Failed ({endpoint}): {e}")
        return False


@app.context_processor
def inject_user():
    # Helper to inject user into templates based on global UUID
    if UUID:
        users = db.get_users()
        user = next((u for u in users if u.uuid == UUID), None)
        return dict(user=user)
    return dict(user=None)


# --- API ROUTES (from routes.py) ---

@app.route('/notification/receive', methods=['POST'])
def notification_receive() -> tuple[Response, int]:
    """Receive encrypted notifications from cloud"""
    try:
        data, error = get_validated_json()
        if error: return error

        message_b64 = data.get('message')
        if not message_b64: return jsonify({'error': 'Missing required field: message'}), 400

        message_data, error = decrypt_message(message_b64)
        if error: return error

        notification_type = message_data.get('type')
        logger.info(f"Received notification: {notification_type}")

        return jsonify({'message': 'Notification received'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/emergency/receive', methods=['POST'])
def emergency_receive() -> tuple[Response, int]:
    """Receive encrypted emergency payload (rescuer side)"""
    global DEC_CIPHER, CLOUD_NONCE
    try:
        data, error = get_validated_json()
        if error: return error

        emergency_id = data.get('emergency_id')
        user_uuid = data.get('user_uuid')
        blob_b64 = data.get('blob')
        severity = data.get('severity')

        if not (emergency_id and user_uuid and blob_b64):
            return jsonify({'error': 'Missing fields'}), 400

        if not DEC_CIPHER or not CLOUD_NONCE:
            return jsonify({'error': 'Crypto not initialized'}), 500

        encrypted_blob = base64.b64decode(blob_b64.encode())
        decrypted_blob = crypto.decrypt(DEC_CIPHER, CLOUD_NONCE, encrypted_blob, b"")

        emergency = Emergency.unpack(emergency_id, user_uuid, decrypted_blob)

        # Save received emergency to DB so it appears in Rescuer Home
        db.insert_emergency(emergency)

        return jsonify({'message': 'Emergency received', 'id': emergency.emergency_id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/emergency/status', methods=['POST'])
def api_emergency_status() -> tuple[Response, int]:
    """Receive encrypted emergency status update"""
    data, error = get_validated_json()
    if error: return error

    message_b64 = data.get('message')
    if not message_b64: return jsonify({'error': 'Missing message'}), 400

    message_data, error = decrypt_message(message_b64)
    if error: return error

    # Logic to update local status could go here
    return jsonify({'message': 'Status update received'}), 200


@app.route('/rescuer/assignment', methods=['POST'])
def rescuer_assignment() -> tuple[Response, int]:
    """Receive encrypted rescuer assignment"""
    data, error = get_validated_json()
    if error: return error

    message_b64 = data.get('message')
    if not message_b64: return jsonify({'error': 'Missing message'}), 400

    message_data, error = decrypt_message(message_b64)
    if error: return error

    return jsonify({'message': 'Assignment received'}), 200


# --- UI ROUTES (from app.py) ---

@app.route('/')
def index():
    if UUID:
        if IS_RESCUER:
            return redirect(url_for('rescuer_home'))
        else:
            return redirect(url_for('rescuee_home'))
    return redirect(url_for('welcome'))


@app.route('/welcome/')
def welcome():
    return render_template('welcome.html')


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    global UUID, IS_RESCUER

    if request.method == 'POST':
        try:
            name = request.form.get('name')
            surname = request.form.get('surname')
            is_rescuer_val = request.form.get('is_rescuer') == 'on'
            birthday_str = request.form.get('birthday')
            bloodtype_str = request.form.get('bloodtype')

            new_uuid = str(uuid.uuid4())
            birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()

            try:
                blood_type = BloodType[bloodtype_str]
            except KeyError:
                return render_template('error.html', status_code=400), 400

            h_json = request.form.get('healthinfo') or "{}"

            new_user = User(
                uuid=new_uuid,
                is_rescuer=is_rescuer_val,
                name=name,
                surname=surname,
                birthday=birthday,
                blood_type=blood_type,
                health_info_json=h_json
            )

            db.insert_user(new_user)

            # Update Globals and File
            UUID = new_uuid
            IS_RESCUER = is_rescuer_val

            with DATA_PATH.open('w') as f:
                f.write(f"{UUID}\n{'1' if IS_RESCUER else '0'}")

            # Trigger connection immediately after registration
            perform_cloud_handshake()

            if IS_RESCUER:
                return redirect(url_for('rescuer_home'))
            else:
                return redirect(url_for('rescuee_home'))

        except Exception as e:
            logger.error(f"Registration Error: {e}")
            return render_template('error.html', status_code=500), 500

    return render_template('registration.html')


@app.route('/rescuee/')
def rescuee_home():
    if not UUID:
        return redirect(url_for('welcome'))

    user_emergencies = db.get_emergencies_by_user_uuid(UUID)
    last_emergency = user_emergencies[-1] if user_emergencies else None
    return render_template('rescuee_home.html', last_emergency=last_emergency)


@app.route('/rescuer/', methods=['GET', 'POST'])
def rescuer_home():
    if not UUID:
        return redirect(url_for('welcome'))

    if request.method == 'POST':
        try:
            emergency_id = int(request.form.get('emergency_id'))
            all_em = db.get_emergencies()
            target_em = next((e for e in all_em if e.emergency_id == emergency_id), None)

            if not target_em: abort(404)

            encrypted_blob = encrypt_emergency_blob(target_em)

            payload = {
                "uuid": UUID,
                "emergency_id": target_em.emergency_id,
                "user_uuid": target_em.user_uuid,
                "severity": target_em.severity,
                "blob": base64.b64encode(encrypted_blob).decode('utf-8'),
                "routing_info_json": ""
            }

            send_to_cloud("/emergency/accept", payload)
            return redirect(url_for('rescuer_home'))

        except Exception as e:
            logger.error(f"Accept Error: {e}")
            return render_template('error.html', status_code=500), 500

    all_emergencies = db.get_emergencies()
    return render_template('rescuer_home.html', received_emergencies=all_emergencies)


@app.route('/new/', methods=['GET', 'POST'])
def new_emergency():
    if not UUID:
        return redirect(url_for('welcome'))

    if request.method == 'POST':
        try:
            em_id = random.randint(1, 10000000)
            e_type = request.form.get('emergency_type')
            desc = request.form.get('description')
            try:
                severity = int(request.form.get('severity'))
            except (ValueError, TypeError):
                severity = 0

            # Position parsing
            pos_str = request.form.get('position')
            position = (0.0, 0.0)
            if pos_str and ',' in pos_str:
                try:
                    lat, lng = map(float, pos_str.split(','))
                    position = (lat, lng)
                except ValueError:
                    pass

            new_em = Emergency(
                emergency_id=em_id,
                user_uuid=UUID,
                severity=severity,
                emergency_type=e_type,
                description=desc,
                created_at=datetime.now(),
                address=request.form.get('address') or "",
                city=request.form.get('city') or "",
                street_number=int(request.form.get('street_number') or -1),
                resolved=False,
                position=position,
                place_description=request.form.get('place_description') or "",
                photo_b64=request.form.get('photo_b64') or "",
                details_json=request.form.get('details_json') or ""
            )

            db.insert_emergency(new_em)

            encrypted_blob = encrypt_emergency_blob(new_em)

            payload = {
                "emergency_id": new_em.emergency_id,
                "user_uuid": new_em.user_uuid,
                "severity": new_em.severity,
                "blob": base64.b64encode(encrypted_blob).decode('utf-8'),
                "routing_info_json": ""
            }

            send_to_cloud("/emergency/submit", payload)
            return redirect(url_for('rescuee_home'))

        except Exception as e:
            logger.error(f"New Emergency Error: {e}")
            return render_template('error.html', status_code=500), 500

    return render_template('send_emergency.html', sent_emergency=None)


@app.route('/edit/<int:emergency_id>/', methods=['GET', 'POST'])
def edit_emergency(emergency_id):
    if not UUID:
        return redirect(url_for('welcome'))

    emergency = db.get_emergency_by_id(UUID, emergency_id)
    if not emergency:
        abort(404)

    if request.method == 'POST':
        try:
            emergency.description = request.form.get('description')
            emergency.emergency_type = request.form.get('emergency_type')
            emergency.place_description = request.form.get('place_description')
            emergency.details_json = request.form.get('details_json')
            if request.form.get('severity'):
                emergency.severity = int(request.form.get('severity'))

            db.update_emergency(UUID, emergency_id, emergency)

            encrypted_blob = encrypt_emergency_blob(emergency)

            payload = {
                "emergency_id": emergency.emergency_id,
                "user_uuid": emergency.user_uuid,
                "severity": emergency.severity,
                "blob": base64.b64encode(encrypted_blob).decode('utf-8'),
                "routing_info_json": ""
            }

            send_to_cloud("/emergency/update", payload)
            return redirect(url_for('rescuee_home'))
        except Exception as e:
            logger.error(f"Edit Error: {e}")
            return render_template('error.html', status_code=500), 500

    return render_template('send_emergency.html', sent_emergency=emergency)


@app.route('/myemergencies/')
def my_emergencies():
    if not UUID:
        return redirect(url_for('welcome'))
    user_emergencies = db.get_emergencies_by_user_uuid(UUID)
    return render_template('my_emergencies.html', sent_emergencies=user_emergencies)


@app.route('/emergency/<int:emergency_id>/')
def emergency_status(emergency_id):
    if not UUID:
        return redirect(url_for('welcome'))

    # Check as owner
    emergency = db.get_emergency_by_id(UUID, emergency_id)
    # Check as rescuer (if owner check failed)
    if not emergency and IS_RESCUER:
        all_em = db.get_emergencies()
        emergency = next((e for e in all_em if e.emergency_id == emergency_id), None)

    if not emergency:
        abort(404)

    return render_template('emergency_status.html', single_emergency=emergency)


@app.route('/legal-info/')
def legal_info():
    return render_template('legal-info.html')


@app.route('/legal/')
def legal_alias():
    return redirect(url_for('legal_info'))


# --- ERROR HANDLERS ---
@app.errorhandler(400)
def bad_request(e): return render_template('error.html', status_code=400), 400


@app.errorhandler(401)
def unauthorized(e): return render_template('error.html', status_code=401), 401


@app.errorhandler(403)
def forbidden(e): return render_template('error.html', status_code=403), 403


@app.errorhandler(404)
def page_not_found(e): return render_template('error.html', status_code=404), 404


@app.errorhandler(500)
def internal_server_error(e): return render_template('error.html', status_code=500), 500


# --- APP STARTUP ---
if __name__ == '__main__':
    # Try to connect on startup if we already have a UUID
    if UUID:
        perform_cloud_handshake()

    app.run(debug=True, port=5001)