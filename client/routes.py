import traceback
import logging
import base64

import requests
import random
import json
from datetime import datetime
from flask import render_template, request, redirect, url_for, abort, jsonify
from common.models.db import DatabaseManager
# Import existing app and network logic
import client
from client import network
from common.models.user import User, BloodType
from common.models.emergency import Emergency
from common.services import crypto

# --- CONFIGURATION ---
CLOUD_URL = "http://127.0.0.1:8000"
logger = logging.getLogger(__name__)

# --- IN-MEMORY STORAGE (Replaces DatabaseManager) ---
# These act as a local cache for the running session.
# Data is lost when the client app restarts.
# TODO: sync with the local database
LOCAL_USER_CACHE = None
LOCAL_EMERGENCY_CACHE = {}  # Format: {emergency_id: EmergencyObject}


# --- HELPERS ---

def perform_handshake():
    """
    Initiates the connection sequence (Certificate + Key Exchange).
    """

    if client.ENC_CIPHER or client.DEC_CIPHER:
        return None

    try:
        enc, dec, nonce, c_nonce = network.connect(
            client.UUID,
            client.SKEY_PATH,
            client.CERTIFICATE_PATH,
            client.IS_RESCUER
        )

        # Update globals in client module
        client.ENC_CIPHER = enc
        client.DEC_CIPHER = dec
        client.NONCE = nonce
        client.CLOUD_NONCE = c_nonce
    except Exception as e:
        logger.error(f"Handshake failed: {traceback.format_exc()}")


def encrypt_blob(emergency_obj) -> bytes:
    """Encrypts emergency data using the global cipher."""
    if not client.ENC_CIPHER or not client.NONCE:
        logger.warning("Encryption skipped: Crypto not initialized.")
        return b""
    try:
        return crypto.encrypt(client.ENC_CIPHER, client.NONCE, emergency_obj.pack(), b"")
    except Exception as e:
        logger.error(f"Encryption error: {traceback.format_exc()}")
        return b""


def decrypt_payload(b64_data: str):
    """Decrypts incoming base64 data using the global cipher."""
    if not client.DEC_CIPHER or not client.CLOUD_NONCE:
        raise ValueError("Crypto not initialized")

    encrypted_bytes = base64.b64decode(b64_data.encode())
    return crypto.decrypt(client.DEC_CIPHER, client.CLOUD_NONCE, encrypted_bytes, b"")


@client.app.context_processor
def inject_user():
    """Injects user data into templates from local memory."""
    return dict(user=LOCAL_USER_CACHE)


# --- UI ROUTES ---


@client.app.route('/legal-info/', methods=['GET'])
def legal_info():
    return render_template('legal-info.html', user=None) # TODO: make global user

@client.app.route('/', methods=['GET'])
def index():
    if client.IS_RESCUER is None:
        return redirect(url_for('registration'))

    if client.ENC_CIPHER is not None:
        return redirect(url_for('rescuer_home') if client.IS_RESCUER else url_for('rescuee_home'))

    abort(404)

@client.app.route('/welcome/', methods=['GET'])
def welcome():
    return render_template('welcome.html')

@client.app.route('/registration/', methods=['GET', 'POST'])
def registration():
    global LOCAL_USER_CACHE

    if request.method == 'POST':
        try:
            is_rescuer = request.form.get('is_rescuer') == '1'
            uuid = client.UUID

            payload = {
                "uuid": uuid,
                "is_rescuer": is_rescuer,
                "name": request.form.get('name'),
                "surname": request.form.get('surname'),
                "birthday": request.form.get('birthday'),
                "blood_type": request.form.get('bloodtype'),
                "health_info_json": request.form.get('health_info_json') or "{}"
            }

            requests.post(f"{CLOUD_URL}/user/save", json=payload, timeout=5).raise_for_status()

            client.IS_RESCUER = is_rescuer

            with client.DATA_PATH.open('w') as f:
                f.write(f"{client.UUID}\n{'1' if is_rescuer else '0'}")

            perform_handshake()

            try:
                b_type = BloodType[request.form.get('bloodtype')]
                LOCAL_USER_CACHE = User(
                    uuid=client.UUID,
                    is_rescuer=is_rescuer,
                    name=request.form.get('name'),
                    surname=request.form.get('surname'),
                    birthday=datetime.strptime(request.form.get('birthday'), '%Y-%m-%d').date(),
                    blood_type=b_type,
                    health_info_json=request.form.get('health_info_json') or "{}"
                )
            except Exception as e:
                logger.warning(f"Error caching user locally: {traceback.format_exc()}")

            return redirect(url_for('rescuer_home' if is_rescuer else 'rescuee_home'))

        except Exception as e:
            logger.error(f"Registration Error: {traceback.format_exc()}")
            return render_template('error.html', status_code=500), 500

    return render_template('registration.html')

@client.app.route('/myemergencies/', methods=['GET'])
def myemergencies():
    try:
        db = DatabaseManager.get_instance()
        ems = db.get_emergencies_by_user_uuid(client.UUID)

        return render_template('my_emergencies.html', sent_emergencies=ems)
    except Exception as e:
        logger.error(f"Get emergencies error: {traceback.format_exc()}")
        return render_template('error.html', status_code=500), 500

@client.app.route('/new/', methods=['GET', 'POST'])
def new_emergency():
    if request.method == 'POST':
        try:
            pos = ('0.0', '0.0')
            if request.form.get('position') and ',' in request.form.get('position'):
                try:
                    pos = tuple(request.form.get('position').split(','))
                except:
                    pass

            temp_em = Emergency(
                emergency_id=0,
                user_uuid=client.UUID,
                severity=int(request.form.get('severity') or 0),
                emergency_type=request.form.get('emergency_type'),
                description=request.form.get('description'),
                created_at=datetime.now(),
                address=request.form.get('address') or "",
                city=request.form.get('city') or "",
                street_number=int(request.form.get('street_number') or -1),
                resolved=False,
                position=pos,
                place_description=request.form.get('place_description') or "",
                photo_b64=request.form.get('photo_b64') or "",
                details_json=request.form.get('details_json') or ""
            )

            print(temp_em.to_db_tuple())
            db = DatabaseManager.get_instance()
            out = db.insert_emergency(temp_em)
            if out is None:
                return render_template('error.html', status_code=500), 500

            encrypted_blob = encrypt_blob(temp_em)

            payload = {
                "emergency_id": out,
                "user_uuid": client.UUID,
                "severity": temp_em.severity,
                "blob": base64.b64encode(encrypted_blob).decode('utf-8'),
                "routing_info_json": ""
            }


            requests.post(f"{CLOUD_URL}/emergency/submit", json=payload, timeout=5).raise_for_status()

            return redirect(url_for('rescuee_home'))

        except Exception as e:
            logger.error(f"New Emergency Error: {traceback.format_exc()}")
            return render_template('error.html', status_code=500), 500

    return render_template('send_emergency.html')


@client.app.route('/rescuer/', methods=['GET', 'POST'])
def rescuer_home():
    if not client.UUID: return redirect(url_for('welcome'))

    if request.method == 'POST':
        try:
            em_id = int(request.form.get('emergency_id'))

            # Fetch from Memory Cache
            target_em = LOCAL_EMERGENCY_CACHE.get(em_id)
            if not target_em:
                abort(404)

            # Encrypt
            encrypted_blob = encrypt_blob(target_em)

            payload = {
                "uuid": client.UUID,
                "emergency_id": target_em.emergency_id,
                "user_uuid": target_em.user_uuid,
                "severity": target_em.severity,
                "blob": base64.b64encode(encrypted_blob).decode('utf-8'),
                "routing_info_json": ""
            }

            # Send Accept to Cloud
            requests.post(f"{CLOUD_URL}/emergency/accept", json=payload, timeout=5).raise_for_status()

            return redirect(url_for('rescuer_home'))
        except Exception as e:
            logger.error(f"Accept Error: {traceback.format_exc()}")
            return render_template('error.html', status_code=500), 500

    # Render list from Memory Cache
    emergencies_list = list(LOCAL_EMERGENCY_CACHE.values())
    return render_template('rescuer_home.html', received_emergencies=emergencies_list)


@client.app.route('/rescuee/')
def rescuee_home():
    if not client.UUID: return redirect(url_for('welcome'))

    # Filter memory cache for current user's emergencies
    my_emergencies = [e for e in LOCAL_EMERGENCY_CACHE.values() if e.user_uuid == client.UUID]
    last_emergency = my_emergencies[-1] if my_emergencies else None

    return render_template('rescuee_home.html', last_emergency=last_emergency)


# --- INGRESS ROUTES (Called by Cloud) ---

@client.app.route('/emergency/receive', methods=['POST'])
def emergency_receive():
    """
    Callback from Cloud to push data to the client.
    Stores data in the global in-memory dictionary.
    """
    try:
        data = request.get_json()
        if not data: return jsonify({'error': 'No data'}), 400

        decrypted_blob = decrypt_payload(data['blob'])
        emergency = Emergency.unpack(data['emergency_id'], data['user_uuid'], decrypted_blob)

        db = DatabaseManager.get_instance()
        db.insert_emergency_from_rescuee(emergency)

        # Update Memory Cache
        LOCAL_EMERGENCY_CACHE[emergency.emergency_id] = emergency

        return jsonify({'message': 'Emergency received', 'id': emergency.emergency_id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@client.app.route('/notification/receive', methods=['POST'])
def notification_receive():
    try:
        data = request.get_json()
        decrypted_bytes = decrypt_payload(data['message'])
        notification = json.loads(decrypted_bytes.decode('utf-8'))

        logger.info(f"Notification: {notification}")
        # Logic to update UI status or alert user could go here

        return jsonify({'message': 'Received'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@client.app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', status_code=404), 404


@client.app.errorhandler(500)
def internal_error(e):
    return render_template('error.html', status_code=500), 500
