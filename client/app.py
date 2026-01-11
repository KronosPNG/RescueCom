import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, abort

# 1. SETUP LOGGING
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# 2. PATH CONFIGURATION
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


# --- MOCK MODELS ---

class User:
    def __init__(self, name, surname, is_rescuer=False, birthday=None, bloodtype=None, health_info=None):
        self.name = name
        self.surname = surname
        self.is_rescuer = is_rescuer
        self.birthday = birthday
        self.bloodtype = bloodtype
        self.health_info = health_info
        self.uuid = "mock-user-uuid-123"  # Simulate a User UUID
        self.email = "test@example.com"


class Emergency:
    # UPDATED: Matches the exact structure you provided
    def __init__(self, emergency_id: int, user_uuid: str, severity: int, emergency_type: str,
                 description: str, created_at: datetime = None, address: str = "",
                 city: str = "", street_number: int = -1, resolved: bool = False,
                 position: tuple[float, float] = (0.0, 0.0), place_description: str = "",
                 photo_b64: str = "", details_json: str = ""):
        self.emergency_id = emergency_id
        self.user_uuid = user_uuid
        self.severity = severity
        self.emergency_type = emergency_type
        self.description = description
        self.created_at = created_at if created_at else datetime.now()
        self.address = address
        self.city = city
        self.street_number = street_number
        self.resolved = resolved
        self.position = position
        self.place_description = place_description
        self.photo_b64 = photo_b64
        self.details_json = details_json

        # Compatibility property if templates use .id instead of .emergency_id
        self.id = emergency_id

    # Mock Logged User


current_user = User(name="Mario", surname="Rossi", is_rescuer=False)

# Mock Database
emergencies_db = [
    Emergency(
        emergency_id=1,
        user_uuid="mock-user-uuid-123",
        severity=5,
        emergency_type="Trauma Fisico",
        description="Caduta dalla bici",
        position=(41.9028, 12.4964)
    )
]


# --- CONTEXT PROCESSOR ---
@app.context_processor
def inject_user():
    return dict(user=current_user)


# --- ROUTES ---

@app.route('/')
def index():
    return redirect(url_for('welcome'))


@app.route('/welcome/')
def welcome():
    return render_template('welcome.html')


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        is_rescuer = request.form.get('is_rescuer') == 'on'
        birthday = request.form.get('birthday')
        bloodtype = request.form.get('bloodtype')

        h_json = request.form.get('healthinfo') or request.form.get('health_info_json')
        health_data = {}
        if h_json:
            try:
                health_data = json.loads(h_json)
            except json.JSONDecodeError:
                pass

        global current_user
        current_user = User(name, surname, is_rescuer, birthday, bloodtype, health_data)

        if is_rescuer:
            return redirect(url_for('rescuer_home'))
        else:
            return redirect(url_for('rescuee_home'))

    return render_template('registration.html')


@app.route('/rescuee/')
def rescuee_home():
    last_emergency = emergencies_db[-1] if emergencies_db else None
    return render_template('rescuee_home.html', last_emergency=last_emergency)


@app.route('/rescuer/')
def rescuer_home():
    return render_template('rescuer_home.html', received_emergencies=emergencies_db)


@app.route('/new/', methods=['GET', 'POST'])
def new_emergency():
    if request.method == 'POST':
        try:
            new_id = len(emergencies_db) + 1

            # --- Type Conversion (Safe Parsing) ---
            # 1. Severity (int)
            try:
                severity = int(request.form.get('severity'))
            except (ValueError, TypeError):
                severity = 0

            # 2. Street Number (int)
            try:
                street_number = int(request.form.get('street_number'))
            except (ValueError, TypeError):
                street_number = -1

            # 3. Position (tuple[float, float])
            position = (0.0, 0.0)
            pos_str = request.form.get('position')
            if pos_str and ',' in pos_str:
                try:
                    lat, lng = map(float, pos_str.split(','))
                    position = (lat, lng)
                except ValueError:
                    pass  # Keep default (0.0, 0.0)

            # 4. Strings
            e_type = request.form.get('emergency_type') or "Altro"
            desc = request.form.get('description') or ""
            address = request.form.get('address') or ""
            city = request.form.get('city') or ""
            place_desc = request.form.get('place_description') or ""
            photo = request.form.get('photo_b64') or ""
            details = request.form.get('details_json') or ""

            # --- Create Object ---
            new_em = Emergency(
                emergency_id=new_id,
                user_uuid=current_user.uuid,
                severity=severity,
                emergency_type=e_type,
                description=desc,
                address=address,
                city=city,
                street_number=street_number,
                position=position,
                place_description=place_desc,
                photo_b64=photo,
                details_json=details
            )

            emergencies_db.append(new_em)
            return redirect(url_for('rescuee_home'))

        except Exception as e:
            logger.error(f"Error creating emergency: {e}")
            abort(500)

    return render_template('send_emergency.html', sent_emergency=None)


@app.route('/edit/<int:emergency_id>/', methods=['GET', 'POST'])
def edit_emergency(emergency_id):
    # Retrieve by emergency_id
    emergency = next((e for e in emergencies_db if e.emergency_id == emergency_id), None)
    if not emergency:
        abort(404)

    if request.method == 'POST':
        # Update allowed fields
        emergency.description = request.form.get('description')
        emergency.emergency_type = request.form.get('emergency_type')
        emergency.place_description = request.form.get('place_description')

        try:
            emergency.severity = int(request.form.get('severity'))
        except (ValueError, TypeError):
            pass

        return redirect(url_for('rescuee_home'))

    return render_template('send_emergency.html', sent_emergency=emergency)


@app.route('/myemergencies/')
def my_emergencies():
    return render_template('my_emergencies.html', sent_emergencies=emergencies_db)


@app.route('/emergency/<int:emergency_id>/')
def emergency_status(emergency_id):
    emergency = next((e for e in emergencies_db if e.emergency_id == emergency_id), None)
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
    logger.warning(f"400 Error: {e}")
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
    logger.error(f"500 Error: {e}")
    return render_template('error.html', status_code=500), 500