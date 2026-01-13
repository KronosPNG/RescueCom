import traceback
import base64
import datetime
import os
import requests

from pathlib import Path

from typing import Optional, Any
from flask import request, jsonify, Response

import cloud
from cloud.clientDTO import ClientDTO
from common.models import enc_emergency, user
from common.models.emergency import Emergency
from common.services import crypto
from cloud import persistence, app


def get_validated_json() -> tuple[Optional[dict[str, Any]], Optional[tuple[Any, int]]]:
    """Extract and validate JSON data from request"""
    data: Optional[dict[str, Any]] = request.get_json()
    if not data:
        return None, (jsonify({"error": "No JSON data provided"}), 400)
    return data, None


def extract_emergency_fields(
    data: dict[str, Any],
) -> tuple[Optional[enc_emergency.EncryptedEmergency], Optional[tuple[Any, int]]]:
    """Extract and validate emergency fields from request data"""
    emergency_id: Optional[int] = data.get("emergency_id")
    user_uuid: Optional[str] = data.get("user_uuid")
    routing_info_json: Optional[str] = data.get("routing_info_json")
    blob_b64: Optional[str] = data.get("blob")
    severity: Optional[int] = data.get("severity")

    if not emergency_id or not user_uuid:
        return None, (
            jsonify({"error": "Missing required fields: emergency_id and user_uuid"}),
            400,
        )

    # Create EncryptedEmergency instance
    encrypted_emergency: enc_emergency.EncryptedEmergency = (
        enc_emergency.EncryptedEmergency(
            emergency_id=emergency_id,
            user_uuid=user_uuid,
            severity=severity,
            created_at=datetime.datetime.now(datetime.UTC),
            routing_info_json=routing_info_json,
            blob=base64.b64decode(blob_b64.encode()),
        )
    )

    return encrypted_emergency, None


def create_user_from_data(
    data: dict[str, Any],
) -> tuple[Optional[user.User], Optional[tuple[Any, int]]]:
    """Extract and validate user fields from request data"""
    # Validate required fields
    required_fields: list[str] = [
        "uuid",
        "is_rescuer",
        "name",
        "surname",
        "birthday",
        "blood_type",
    ]
    missing_fields: list[str] = [
        field
        for field in required_fields
        if field not in data or data.get(field) is None
    ]
    if missing_fields:
        app.logger.error(traceback.format_exc())
        return None, (
            jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}),
            400,
        )

    try:
        new_user: user.User = user.User(
            uuid=data.get("uuid"),
            is_rescuer=data.get("is_rescuer"),
            name=data.get("name"),
            surname=data.get("surname"),
            birthday=data.get("birthday"),
            blood_type=user.BloodType[data.get("blood_type")],
            health_info_json=data.get("health_info_json"),
        )
        return new_user, None
    except (ValueError, TypeError) as e:
        return None, (jsonify({"error": f"Invalid data format: {traceback.format_exc()}"}), 400)


@app.route("/emergency/submit/", methods=["POST"])
def emergency_submit() -> tuple[Any, int]:
    """Submit an emergency"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            app.logger.error(error_response)
            return error_response

        encrypted_emergency, error_response = extract_emergency_fields(data)
        if error_response:
            app.logger.error(error_response)
            return error_response

        client = cloud.CLIENTS[encrypted_emergency.user_uuid]

        if not client:
            app.logger.debug("Client not found")
            raise Exception("Client not found")

        decrypted_blob: bytes = crypto.decrypt(
            client.dec_cipher, client.nonce, encrypted_emergency.blob, b""
        )  # TODO: align with client about aad
        emergency: Emergency = Emergency.unpack(
            encrypted_emergency.emergency_id,
            encrypted_emergency.user_uuid,
            decrypted_blob,
        )

        app.logger.debug(data)
        return jsonify(
            {"message": "Emergency submitted successfully", "data": data}
        ), 200
    except Exception:
        app.logger.error(traceback.format_exc())
        return jsonify({"error": f"Internal server error: {traceback.format_exc()}"}), 500


@app.route("/emergency/accept/", methods=["POST"])
def emergency_accept() -> tuple[Any, int]:
    """Accept an emergency"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            app.logger.error(error_response)
            return error_response

        encrypted_emergency, error_response = extract_emergency_fields(data)
        if error_response:
            app.logger.error(error_response)
            return error_response

        rescuer = None
        if data.get("uuid") in cloud.RESCUERS:
            rescuer = cloud.RESCUERS[data.get("uuid")]

        if not rescuer:
            raise Exception("Rescuer uuid not found")

        user_uuid: str = encrypted_emergency.user_uuid

        if user_uuid in cloud.CLIENTS:
            client: ClientDTO = cloud.CLIENTS[user_uuid]
        else:
            raise Exception("Client couldn't be found")

        decrypted_blob: bytes = crypto.decrypt(
            rescuer.dec_cipher, rescuer.nonce, encrypted_emergency.blob, b""
        )  # TODO: align with client about aad

        message: dict[str, str] = {
            "type": "emergency_accepted",
            "emergency_id": encrypted_emergency.emergency_id,
            "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
        }

        encrypted_message: bytes = crypto.encrypt(
            client.enc_cipher, client.cloud_nonce, str(message).encode(), b""
        )

        try:
            requests.post(
                client.ip + "/notification/receive",
                json={
                    "message": base64.b64encode(encrypted_message).decode(),
                },
                timeout=3,
            )
        except Exception as msg_err:
            app.logger.error(str(msg_err))

        app.logger.debug(data)
        return jsonify(
            {"message": "Emergency accepted successfully", "data": data}
        ), 200

    except Exception as e:
        app.logger.error(traceback.format_exc())
        return jsonify({"error": f"Internal server error: {traceback.format_exc()}"}), 500


@app.route("/emergency/update/", methods=["POST"])
def emergency_update() -> tuple[Any, int]:
    """Update an emergency"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            app.logger.error(error_response)
            return error_response

        encrypted_emergency, error_response = extract_emergency_fields(data)
        if error_response:
            app.logger.error(error_response)
            return error_response

        persistence.update_encrypted_emergency(
            encrypted_emergency.user_uuid,
            encrypted_emergency.emergency_id,
            encrypted_emergency,
        )

        app.logger.debug(data)
        return jsonify({"message": "Emergency updated successfully", "data": data}), 200
    except Exception as e:
        app.logger.error(traceback.format_exc())
        return jsonify({"error": f"Internal server error: {traceback.format_exc()}"}), 500


@app.route("/emergency/delete/", methods=["POST"])
def emergency_delete() -> tuple[Any, int]:
    """Delete an emergency"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            app.logger.error(error_response)
            return error_response

        user_uuid: Optional[str] = data.get("user_uuid")
        emergency_id: Optional[int] = data.get("emergency_id")

        if not user_uuid or not emergency_id:
            app.logger.error("Missing required fields: user_uuid and emergency_id")
            return jsonify(
                {"error": "Missing required fields: user_uuid and emergency_id"}
            ), 400

        persistence.delete_encrypted_emergency(user_uuid, emergency_id)

        app.logger.debug(data)
        return jsonify({"message": "Emergency deleted successfully", "data": data}), 200
    except Exception as e:
        app.logger.error(traceback.format_exc())
        return jsonify({"error": f"Internal server error: {traceback.format_exc()}"}), 500


@app.route("/user/save/", methods=["POST"])
def user_save() -> tuple[Any, int]:
    """Save a user"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            app.logger.error(error_response)
            return error_response

        new_user, error_response = create_user_from_data(data)
        if error_response:
            app.logger.error(error_response)
            return error_response

        persistence.save_user(new_user)

        app.logger.debug(data)
        return jsonify({"message": "User saved successfully", "data": data}), 200
    except Exception as e:
        app.logger.error(traceback.format_exc())
        return jsonify({"error": f"Internal server error: {traceback.format_exc()}"}), 500


@app.route("/user/update/", methods=["POST"])
def user_update() -> tuple[Any, int]:
    """Update a user"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            app.logger.error(error_response)
            return error_response

        updated_user, error_response = create_user_from_data(data)
        if error_response:
            app.logger.error(error_response)
            return error_response

        persistence.update_user(updated_user.uuid, updated_user)

        app.logger.debug(data)
        return jsonify({"message": "User updated successfully", "data": data}), 200
    except Exception as e:
        app.logger.error(traceback.format_exc())
        return jsonify({"error": f"Internal server error: {traceback.format_exc()}"}), 500


@app.route("/user/delete/", methods=["POST"])
def user_delete() -> tuple[Any, int]:
    """Delete a user"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            app.logger.error(error_response)
            return error_response

        uuid: Optional[str] = data.get("uuid")

        if not uuid:
            app.logger.error("Missing required field: uuid")
            return jsonify({"error": "Missing required field: uuid"}), 400

        persistence.delete_user(uuid)

        app.logger.debug(data)
        return jsonify({"message": "User deleted successfully", "uuid": uuid}), 200
    except Exception as e:
        app.logger.error(traceback.format_exc())
        return jsonify({"error": f"Internal server error: {traceback.format_exc()}"}), 500


@app.route("/connect/", methods=["POST"])
def connect() -> tuple[Any, int]:
    """Connect with a client"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            app.logger.error(error_response)
            return error_response

        uuid: Optional[str] = data.get("uuid")
        cert_bytes = data.get("certificate")
        client_nonce = data.get("nonce")
        client_signature = data.get("signature")
        is_rescuer: Optional[bool] = data.get("is_rescuer")

        if (
            not uuid
            or not cert_bytes
            or not client_nonce
            or not client_signature
            or is_rescuer is None
        ):
            app.logger.error("Missing required fields")
            return jsonify({"error": "Missing required fields"}), 400

        cert_bytes = bytes.fromhex(cert_bytes)
        client_nonce = bytes.fromhex(client_nonce)
        client_signature = bytes.fromhex(client_signature)

        client_certificate = crypto.decode_certificate(cert_bytes)
        if not crypto.verify_certificate(client_certificate, client_signature, client_nonce):
            app.logger.error("Couldn't verify certificate or signature")
            return jsonify({"error": "Couldn't verify certificate or signature"}), 400

        certificate = crypto.load_certificate(cloud.CERTIFICATE_PATH)
        certificate_bytes = crypto.encode_certificate(certificate)
        nonce = os.urandom(12)
        skey = crypto.load_signing_key(cloud.SKEY_PATH)
        signature = crypto.sign(skey, nonce)

        cloud.CLIENTS[uuid] = ClientDTO(
            request.remote_addr,
            None,
            None,
            client_nonce,
            nonce,
            is_rescuer,
        )

        if is_rescuer:
            cloud.RESCUERS[uuid] = ClientDTO(
                request.remote_addr,
                None,
                None,
                client_nonce,
                nonce,
                is_rescuer,
            )

        app.logger.debug("Verification successful")
        return jsonify(
            {
                "message": "Verification successful",
                "certificate": certificate_bytes.hex(),
                "nonce": nonce.hex(),
                "signature": signature.hex(),
            }
        ), 200
    except Exception as e:
        app.logger.error(traceback.format_exc())
        return jsonify({"error": f"Internal server error: {traceback.format_exc()}"}), 500


@app.route("/pkey/", methods=["POST"])
def pkey() -> tuple[Any, int]:
    """Connect with a client"""
    try:
        data, error_response = get_validated_json()
        if error_response:
            app.logger.error(error_response)
            return error_response

        uuid: Optional[str] = data.get("uuid")
        pkey_bytes = data.get("public_key")

        if not uuid or not pkey_bytes:
            app.logger.error("Missing required fields")
            return jsonify({"error": "Missing required fields"}), 400

        pkey_bytes = bytes.fromhex(pkey_bytes)
        client_pkey = crypto.decode_ecdh_pkey(pkey_bytes)

        skey, pkey = crypto.gen_ecdh_keys()

        key = crypto.derive_shared_key(skey, client_pkey)

        enc_cipher, dec_cipher = crypto.get_ciphers(key)

        if not uuid in cloud.CLIENTS:
            raise Exception("Perform certificate verification first")

        client_dto = cloud.CLIENTS[uuid]

        cloud.CLIENTS[uuid] = ClientDTO(
                client_dto.ip,
                enc_cipher,
                dec_cipher,
                client_dto.nonce,
                client_dto.cloud_nonce,
                client_dto.is_rescuer,
                client_dto.busy
                )

        if uuid in cloud.RESCUERS:
            cloud.RESCUERS[uuid] = ClientDTO(
                client_dto.ip,
                enc_cipher,
                dec_cipher,
                client_dto.nonce,
                client_dto.cloud_nonce,
                client_dto.is_rescuer,
                client_dto.busy
                )


        app.logger.debug("Key exchange completed")
        return jsonify(
            {"message": "Key exchange completed", "pkey": crypto.encode_ecdh_pkey(pkey).hex()}
        ), 200
    except Exception as e:
        app.logger.error(traceback.format_exc())
        return jsonify({"error": f"Internal server error: {traceback.format_exc()}"}), 500


@app.route("/health/", methods=["GET"])
def health_check() -> tuple[Response, int]:
    return jsonify({"message": "Cloud is healthy"}), 200
