import functools
import traceback
import base64

import requests
import random
import json
from datetime import datetime
from flask import render_template, request, redirect, url_for, abort, jsonify
from common.models.db import DatabaseManager

import client
from client import network
from common.models.user import User, BloodType
from common.models.emergency import Emergency
from common.services import crypto

CLOUD_URL = "http://127.0.0.1:8000"

# --- IN-MEMORY STORAGE (Replaces DatabaseManager) ---
# These act as a local cache for the running session.
# Data is lost when the client app restarts.
LOCAL_USER_CACHE = None
LOCAL_EMERGENCY_CACHE = {}  # Format: {emergency_id: EmergencyObject}


def rescuer_only(route):
    @functools.wraps(route)
    def wrapper(*args, **kwargs):
        if client.IS_RESCUER:
            return route(*args, **kwargs)
        return redirect(url_for("index"))

    return wrapper


def login_required(route):
    @functools.wraps(route)
    def wrapper(*args, **kwargs):
        if client.ENC_CIPHER is not None:
            return route(*args, **kwargs)
        return redirect(url_for("index"))

    return wrapper


def perform_handshake():
    """
    Initiates the connection sequence (Certificate + Key Exchange).
    """

    if client.ENC_CIPHER or client.DEC_CIPHER:
        return None

    try:
        enc, dec, nonce, c_nonce = network.connect(
            client.UUID, client.SKEY_PATH, client.CERTIFICATE_PATH, client.IS_RESCUER
        )

        client.ENC_CIPHER = enc
        client.DEC_CIPHER = dec
        client.NONCE = nonce
        client.CLOUD_NONCE = c_nonce
    except Exception as e:
        client.app.logger.error(f"Handshake failed: {traceback.format_exc()}")


def encrypt_blob(emergency_obj) -> bytes:
    """Encrypts emergency data using the global cipher."""
    if not client.ENC_CIPHER or not client.NONCE:
        client.app.logger.warning("Encryption skipped: Crypto not initialized.")
        return b""
    try:
        return crypto.encrypt(
            client.ENC_CIPHER, client.NONCE, emergency_obj.pack(), b""
        )
    except Exception as e:
        client.app.logger.error(f"Encryption error: {traceback.format_exc()}")
        return b""


def decrypt_payload(b64_data: str):
    """Decrypts incoming base64 data using the global cipher."""
    if not client.DEC_CIPHER or not client.CLOUD_NONCE:
        raise ValueError("Crypto not initialized")

    encrypted_bytes = base64.b64decode(b64_data.encode())
    return crypto.decrypt(client.DEC_CIPHER, client.CLOUD_NONCE, encrypted_bytes, b"")


@client.app.route("/legal-info/", methods=["GET"])
def legal_info():
    return render_template("legal-info.html", user=client.USER)


@client.app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        client.ACCEPTED_GDPR = True
        return redirect(url_for("index"))

    else:
        if not client.ACCEPTED_GDPR:
            return redirect(url_for("welcome"))

        if client.IS_RESCUER is None:
            return redirect(url_for("registration"))

        if client.ENC_CIPHER is None:
            perform_handshake()

        return redirect(
            url_for("rescuer_home") if client.IS_RESCUER else url_for("rescuee_home")
        )


@client.app.route("/welcome/", methods=["GET"])
def welcome():
    return render_template("welcome.html")


@client.app.route("/registration/", methods=["GET", "POST"])
def registration():
    global LOCAL_USER_CACHE

    if client.ENC_CIPHER is not None:
        return redirect(url_for("index"))

    if request.method == "POST":
        try:
            is_rescuer = request.form.get("is_rescuer") == "on"
            uuid = client.UUID

            payload = {
                "uuid": uuid,
                "is_rescuer": is_rescuer,
                "name": request.form.get("name"),
                "surname": request.form.get("surname"),
                "birthday": request.form.get("birthday"),
                "blood_type": request.form.get("bloodtype"),
                "health_info_json": request.form.get("health_info_json") or "{}",
            }

            client.IS_RESCUER = is_rescuer

            with client.DATA_PATH.open("w") as f:
                f.write(
                    f"{client.UUID}\n{'1' if is_rescuer else '0'}\n{'1' if client.ACCEPTED_GDPR else '0'}"
                )

            requests.post(
                f"{CLOUD_URL}/user/save/", json=payload, timeout=5
            ).raise_for_status()

            perform_handshake()

            try:
                b_type = BloodType[request.form.get("bloodtype")]
                LOCAL_USER_CACHE = client.USER = User(
                    uuid=client.UUID,
                    is_rescuer=is_rescuer,
                    name=request.form.get("name"),
                    surname=request.form.get("surname"),
                    birthday=datetime.strptime(
                        request.form.get("birthday"), "%Y-%m-%d"
                    ).date(),
                    blood_type=b_type,
                    health_info_json=request.form.get("health_info_json") or "{}",
                )
            except Exception as e:
                client.app.logger.warning(
                    f"Error caching user locally: {traceback.format_exc()}"
                )

            return redirect(url_for("rescuer_home" if is_rescuer else "rescuee_home"))

        except Exception as e:
            client.app.logger.error(f"Registration Error: {traceback.format_exc()}")
            return render_template("error.html", user=client.USER, status_code=500), 500

    return render_template("registration.html", user=client.USER)


@client.app.route("/myemergencies/", methods=["GET"])
@login_required
def myemergencies():
    try:
        db = DatabaseManager.get_instance()
        ems = db.get_emergencies_by_user_uuid(client.UUID)

        return render_template(
            "my_emergencies.html", user=client.USER, sent_emergencies=ems
        )
    except Exception as e:
        client.app.logger.error(f"Get emergencies error: {traceback.format_exc()}")
        return render_template("error.html", user=client.USER, status_code=500), 500


@client.app.route("/emergency/<emergency_id>", methods=["GET"])
@login_required
def emergency_details(emergency_id):
    try:
        em = LOCAL_EMERGENCY_CACHE.get(emergency_id)
        if not em:
            db = DatabaseManager.get_instance()
            em = db.get_emergency_by_id(client.UUID, emergency_id)

            if not em:
                return render_template(
                    "error.html", user=client.USER, status_code=404
                ), 404

        return render_template(
            "emergency_status.html", user=client.USER, single_emergency=em
        )
    except Exception as e:
        client.app.logger.error(f"Get emergency detail error: {traceback.format_exc()}")
        return render_template("error.html", user=client.USER, status_code=500), 500


@client.app.route("/edit/<emergency_id>", methods=["GET", "POST"])
@login_required
def emergency_update(emergency_id):
    try:
        em = LOCAL_EMERGENCY_CACHE.get(emergency_id)
        if not em:
            db = DatabaseManager.get_instance()
            em = db.get_emergency_by_id(client.UUID, emergency_id)

            if not em:
                return render_template(
                    "error.html", user=client.USER, status_code=404
                ), 404
    except Exception as e:
        client.app.logger.error(f"Get emergency error: {traceback.format_exc()}")
        return render_template("error.html", user=client.USER, status_code=500), 500

    if request.method == "GET":
        return render_template(
            "send_emergency.html", user=client.USER, sent_emergency=em
        )
    else:
        try:
            db = DatabaseManager.get_instance()
            db.update_emergency(client.UUID, em.emergency_id, em)

            blob = encrypt_blob(em)

            payload = {
                "emergency_id": em.emergency_id,
                "user_uuid": client.UUID,
                "severity": em.severity,
                "blob": base64.b64encode(blob).decode("utf-8"),
                "routing_info_json": "",
            }

            requests.post(
                f"{CLOUD_URL}/emergency/update/", json=payload, timeout=5
            ).raise_for_status()

            LOCAL_EMERGENCY_CACHE[em.emergency_id] = em

            return redirect(url_for("index"))
        except:
            client.app.logger.error(f"Update emergency error: {traceback.format_exc()}")
            return render_template("error.html", user=client.USER, status_code=404), 404


@client.app.route("/new/", methods=["GET", "POST"])
@login_required
def new_emergency():
    if request.method == "POST":
        try:
            pos = (0.0, 0.0)
            if request.form.get("position") and "," in request.form.get("position"):
                try:
                    pos = tuple(map(float, request.form.get("position").split(",")))
                    pos = (pos[0], pos[1])
                except Exception:
                    pass

            temp_em = Emergency(
                emergency_id=0,
                user_uuid=client.UUID,
                severity=int(request.form.get("severity") or 0),
                emergency_type=request.form.get("emergency_type"),
                description=request.form.get("description"),
                created_at=datetime.now(),
                address=request.form.get("address") or "",
                city=request.form.get("city") or "",
                street_number=int(request.form.get("street_number") or 0),
                resolved=False,
                position=pos,
                place_description=request.form.get("place_description") or "",
                photo_b64=request.form.get("photo_b64") or "",
                details_json=request.form.get("details_json") or "",
            )

            db = DatabaseManager.get_instance()
            out = db.insert_emergency(temp_em)
            if out is None:
                return render_template(
                    "error.html", user=client.USER, status_code=500
                ), 500

            encrypted_blob = encrypt_blob(temp_em)

            payload = {
                "emergency_id": out,
                "user_uuid": client.UUID,
                "severity": temp_em.severity,
                "blob": base64.b64encode(encrypted_blob).decode("utf-8"),
                "routing_info_json": "",
            }

            requests.post(
                f"{CLOUD_URL}/emergency/submit/", json=payload, timeout=5
            ).raise_for_status()

            LOCAL_EMERGENCY_CACHE[out] = temp_em

            return redirect(url_for("rescuee_home"))

        except Exception as e:
            client.app.logger.error(f"New Emergency Error: {traceback.format_exc()}")
            return render_template("error.html", user=client.USER, status_code=500), 500

    return render_template("send_emergency.html", user=client.USER)


@client.app.route("/rescuer/", methods=["GET", "POST"])
@login_required
@rescuer_only
def rescuer_home():
    if not client.UUID:
        return redirect(url_for("welcome"))

    if request.method == "POST":
        try:
            em_id = int(request.form.get("emergency_id"))

            target_em = LOCAL_EMERGENCY_CACHE.get(em_id)
            if not target_em:
                abort(404)

            encrypted_blob = encrypt_blob(target_em)

            payload = {
                "uuid": client.UUID,
                "emergency_id": target_em.emergency_id,
                "user_uuid": target_em.user_uuid,
                "severity": target_em.severity,
                "blob": base64.b64encode(encrypted_blob).decode("utf-8"),
                "routing_info_json": "",
            }

            requests.post(
                f"{CLOUD_URL}/emergency/accept/", json=payload, timeout=5
            ).raise_for_status()

            return redirect(url_for("rescuer_home"))
        except Exception as e:
            client.app.logger.error(f"Accept Error: {traceback.format_exc()}")
            return render_template("error.html", user=client.USER, status_code=500), 500

    ems = list()
    dbm = DatabaseManager.get_instance()
    ems_from_db = dbm.get_emergencies()

    emergencies_list = list(ems_from_db)
    return render_template(
        "rescuer_home.html", user=client.USER, received_emergencies=emergencies_list
    )


@client.app.route("/rescuee/")
@login_required
def rescuee_home():
    if not client.UUID:
        return redirect(url_for("welcome"))

    my_emergencies = [
        e for e in LOCAL_EMERGENCY_CACHE.values() if e.user_uuid == client.UUID
    ]
    last_emergency = my_emergencies[-1] if my_emergencies else None

    return render_template(
        "rescuee_home.html", user=client.USER, last_emergency=last_emergency
    )


@client.app.route("/emergency/receive", methods=["POST"])
def emergency_receive():
    """
    Callback from Cloud to push data to the client.
    Stores data in the global in-memory dictionary.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data"}), 400

        decrypted_blob = decrypt_payload(data.get("blob"))
        emergency = Emergency.unpack(
            data.get("emergency_id"), data.get("user_uuid"), decrypted_blob
        )

        db = DatabaseManager.get_instance()
        db.insert_emergency_from_rescuee(emergency)

        LOCAL_EMERGENCY_CACHE[emergency.emergency_id] = emergency

        return jsonify(
            {"message": "Emergency received", "id": emergency.emergency_id}
        ), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@client.app.route("/notification/receive", methods=["POST"])
def notification_receive():
    try:
        data = request.get_json()
        decrypted_bytes = decrypt_payload(data.get("message"))
        notification = json.loads(decrypted_bytes.decode("utf-8"))

        client.app.logger.info(f"Notification: {notification}")

        return jsonify({"message": "Received"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
