from common.models import db, enc_emergency


def save_encrypted_emergency(enc_emergency: enc_emergency.EncryptedEmergency):
    """Persists an encrypted emergency request to the database.

    This function stores the given `EncryptedEmergency` instance in the database.
    The encrypted emergency is persisted until it is resolved or explicitly removed.

    Args:
        enc_emergency (enc_emergency.EncryptedEmergency): The EncryptedEmergency instance
        to be persisted in the database.

    Raises:
        sqlite3.Error: If an error occurs while inserting the encrypted emergency into
            the database.
    """

    dbm = db.DatabaseManager.get_instance()
    dbm.insert_encrypted_emergency(enc_emergency)


def delete_request():
    """
    Delete a request from the DB
    """

    pass
