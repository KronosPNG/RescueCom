import os
import sys
import json
import uuid
import logging
import base64
import requests
import struct
import random
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, abort

# 1. PATH CONFIGURATION
base_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(base_dir)
sys.path.append(project_root)

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

# 3. APP SETUP
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Initialize Database
db_path = os.path.join(project_root, 'rescue.db')
db = DatabaseManager.get_instance(db_path)

# 4. CONFIGURATION & STATE
CLOUD_URL = "http://127.0.0.1:5000"  # Adjust this to your Cloud server address
current_user = None

# Crypto state (Expected to be set by your connection logic, e.g. routes_.py)
_ENC_CIPHER = None
_DEC_CIPHER = None
_NONCE = None


def get_current_user():
    """Retrieves the current authenticated user from local DB."""
    global current_user
    if current_user:
        return current_user

    users = db.get_users()
    if users:
        current_user = users[0]
        return current_user
    return None


@app.context_processor
def inject_user():
    return dict(user=get_current_user())


# --- HELPER: Cloud Communication ---

def send_to_cloud(endpoint, payload):
    """Helper to post JSON to the cloud."""
    try:
        response = requests.post(f"{CLOUD_URL}{endpoint}", json=payload, timeout=5)
        response.raise_for_status()
        return True
    except Exception as e:
        logger.error(f"Cloud Sync Failed ({endpoint}): {e}")
        return False


def encrypt_emergency_blob(emergency_obj):
    """Packs and encrypts an emergency object for transmission."""
    if not _ENC_CIPHER or not _NONCE:
        logger.warning("Encryption skipped: Client crypto not initialized.")
        # For prototype/testing without handshake, we might send dummy data
        # or fail depending on strictness. Returning dummy bytes here.
        return b""

    packed_data = emergency_obj.pack()
    # Encrypt: (cipher, nonce, data, associated_data)
    # Assuming empty AAD as per typical usage in your files
    return crypto.encrypt(_ENC_CIPHER, _NONCE, packed_data, b"")


# --- ROUTES ---

@app.route('/')
def index():
    user = get_current_user()
    if user:
        if user.is_rescuer:
            return redirect(url_for('rescuer_home'))
        else:
            return redirect(url_for('rescuee_home'))
    return redirect(url_for('welcome'))


@app.route('/welcome/')
def welcome():
    return render_template('welcome.html')


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            surname = request.form.get('surname')
            is_rescuer = request.form.get('is_rescuer') == 'on'
            birthday_str = request.form.get('birthday')
            bloodtype_str = request.form.get('bloodtype')

            user_uuid = str(uuid.uuid4())
            birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()

            try:
                blood_type = BloodType[bloodtype_str]
            except KeyError:
                return render_template('error.html', status_code=400), 400

            h_json = request.form.get('healthinfo') or "{}"

            new_user = User(
                uuid=user_uuid,
                is_rescuer=is_rescuer,
                name=name,
                surname=surname,
                birthday=birthday,
                blood_type=blood_type,
                health_info_json=h_json
            )

            db.insert_user(new_user)

            global current_user
            current_user = new_user

            # Note: You might want to sync the new user to cloud here via /user/save
            # But the prompt focused on "new emergency".

            if is_rescuer:
                return redirect(url_for('rescuer_home'))
            else:
                return redirect(url_for('rescuee_home'))

        except Exception as e:
            logger.error(f"Registration Error: {e}")
            return render_template('error.html', status_code=500), 500

    return render_template('registration.html')


@app.route('/rescuee/')
def rescuee_home():
    user = get_current_user()
    if not user:
        return redirect(url_for('welcome'))

    user_emergencies = db.get_emergencies_by_user_uuid(user.uuid)
    last_emergency = user_emergencies[-1] if user_emergencies else None

    return render_template('rescuee_home.html', last_emergency=last_emergency)


# TODO: implement Bluetooth
@app.route('/rescuer/', methods=['GET', 'POST'])
def rescuer_home():
    user = get_current_user()
    if not user:
        return redirect(url_for('welcome'))

    # [EXCHANGE LOGIC] Handling Rescuer Acceptance
    if request.method == 'POST':
        try:
            emergency_id = int(request.form.get('emergency_id'))

            # 1. Retrieve the emergency locally
            # Rescuer should have received it via sync, so it's in DB
            # We search all emergencies since we are the rescuer
            all_em = db.get_emergencies()
            target_em = next((e for e in all_em if e.emergency_id == emergency_id), None)

            if not target_em:
                abort(404)

            # 2. Prepare Cloud Payload for /emergency/accept
            # Cloud expects: uuid (rescuer), emergency_id, user_uuid (rescuee), blob, severity...
            encrypted_blob = encrypt_emergency_blob(target_em)

            payload = {
                "uuid": user.uuid,  # Rescuer UUID
                "emergency_id": target_em.emergency_id,
                "user_uuid": target_em.user_uuid,  # Rescuee UUID
                "severity": target_em.severity,
                "blob": base64.b64encode(encrypted_blob).decode('utf-8'),
                "routing_info_json": ""
            }

            # 3. Send to Cloud
            send_to_cloud("/emergency/accept", payload)

            # 4. Update local state (Optimistic UI update)
            # In a real app, we might wait for the callback, but here we can set resolved?
            # Or just redirect.
            return redirect(url_for('rescuer_home'))

        except Exception as e:
            logger.error(f"Accept Error: {e}")
            return render_template('error.html', status_code=500), 500

    # GET: Show list
    all_emergencies = db.get_emergencies()
    return render_template('rescuer_home.html', received_emergencies=all_emergencies)


# TODO: implement Bluetooth
@app.route('/new/', methods=['GET', 'POST'])
def new_emergency():
    user = get_current_user()
    if not user:
        return redirect(url_for('welcome'))

    if request.method == 'POST':
        try:
            # 1. Generate ID (Random for prototype to avoid collision in simple setups)
            # In production, this should come from a coordinated source or UUIDs.
            em_id = random.randint(1, 10000000)

            # 2. Parse Fields
            e_type = request.form.get('emergency_type')
            desc = request.form.get('description')
            try:
                severity = int(request.form.get('severity'))
            except (ValueError, TypeError):
                severity = 0

            pos_str = request.form.get('position')
            position = (0.0, 0.0)
            if pos_str and ',' in pos_str:
                try:
                    lat, lng = map(float, pos_str.split(','))
                    position = (lat, lng)
                except ValueError:
                    pass

            address = request.form.get('address') or ""
            city = request.form.get('city') or ""
            street_num = int(request.form.get('street_number') or -1)
            place_desc = request.form.get('place_description') or ""
            photo_b64 = request.form.get('photo_b64') or ""
            details_json = request.form.get('details_json') or ""

            # 3. Create Emergency Object
            new_em = Emergency(
                emergency_id=em_id,
                user_uuid=user.uuid,
                severity=severity,
                emergency_type=e_type,
                description=desc,
                created_at=datetime.now(),
                address=address,
                city=city,
                street_number=street_num,
                resolved=False,
                position=position,
                place_description=place_desc,
                photo_b64=photo_b64,
                details_json=details_json
            )

            # 4. Save Locally
            db.insert_emergency(new_em)

            # 5. [EXCHANGE LOGIC] Send to Cloud
            encrypted_blob = encrypt_emergency_blob(new_em)

            payload = {
                "emergency_id": new_em.emergency_id,
                "user_uuid": new_em.user_uuid,
                "severity": new_em.severity,
                "blob": base64.b64encode(encrypted_blob).decode('utf-8'),
                "routing_info_json": ""  # Optional routing info
            }

            send_to_cloud("/emergency/submit", payload)

            return redirect(url_for('rescuee_home'))

        except Exception as e:
            logger.error(f"New Emergency Error: {e}")
            return render_template('error.html', status_code=500), 500

    return render_template('send_emergency.html', sent_emergency=None)


@app.route('/edit/<int:emergency_id>/', methods=['GET', 'POST'])
def edit_emergency(emergency_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('welcome'))

    emergency = db.get_emergency_by_id(user.uuid, emergency_id)
    if not emergency:
        abort(404)

    if request.method == 'POST':
        try:
            # 1. Update Object
            emergency.description = request.form.get('description')
            emergency.emergency_type = request.form.get('emergency_type')
            emergency.place_description = request.form.get('place_description')
            emergency.details_json = request.form.get('details_json')
            if request.form.get('severity'):
                emergency.severity = int(request.form.get('severity'))

            # 2. Update Locally
            db.update_emergency(user.uuid, emergency_id, emergency)

            # 3. [EXCHANGE LOGIC] Update on Cloud
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
    user = get_current_user()
    if not user:
        return redirect(url_for('welcome'))

    user_emergencies = db.get_emergencies_by_user_uuid(user.uuid)
    return render_template('my_emergencies.html', sent_emergencies=user_emergencies)


@app.route('/emergency/<int:emergency_id>/')
def emergency_status(emergency_id):
    user = get_current_user()
    emergency = None
    if user:
        emergency = db.get_emergency_by_id(user.uuid, emergency_id)
        if not emergency and user.is_rescuer:
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
def bad_request(e):
    return render_template('error.html', status_code=400), 400


@app.errorhandler(401)
def unauthorized(e):
    return render_template('error.html', status_code=401), 401


@app.errorhandler(403)
def forbidden(e):
    return render_template('error.html', status_code=403), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', status_code=404), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', status_code=500), 500