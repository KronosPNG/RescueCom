from common.models import db, enc_emergency, user


def save_user(user: user.User) -> None:
    """
    Persists a user to the database.

    This function stores the given `User` instance in the database by
    delegating the operation to the `DatabaseManager`.

    Args:
        user (user.User): The User instance to be persisted in the database.

    Raises:
        sqlite3.Error: If an error occurs while inserting the user into the
            database.
    """
    dbm = db.DatabaseManager.get_instance()
    dbm.insert_user(user)


def update_user(uuid: str, user: user.User) -> None:
    """
    Updates an existing user in the database.

    This function updates the user identified by the given UUID using the
    values provided by the `User` instance. The update operation is delegated
    to the `DatabaseManager`.

    Args:
        uuid (str): The UUID of the user to update.
        user (user.User): A User instance containing the updated values.

    Raises:
        sqlite3.Error: If an error occurs while updating the user in the
            database.
    """

    dbm = db.DatabaseManager.get_instance()
    dbm.update_user(uuid, user)


def delete_user(uuid: str) -> None:
    """
    Deletes a user from the database.

    This function removes the user identified by the given UUID from the
    database by delegating the operation to the `DatabaseManager`.

    Args:
        uuid (str): The UUID of the user to delete.

    Raises:
        sqlite3.Error: If an error occurs while deleting the user from the
            database.
    """

    dbm = db.DatabaseManager.get_instance()
    dbm.delete_user(uuid)


def save_encrypted_emergency(enc_emergency: enc_emergency.EncryptedEmergency) -> None:
    """Persists an encrypted emergency to the database.

    This function stores the given `EncryptedEmergency` instance in the database by
    delegating the operation to the `DatabaseManager`.
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


def update_encrypted_emergency(
    user_uuid: str,
    emergency_id: int,
    enc_emergency: enc_emergency.EncryptedEmergency,
) -> None:
    """
    Updates an encrypted emergency record in the database.

    This function updates the encrypted data of an emergency associated with
    the given user UUID and emergency ID by delegating the operation to the
    `DatabaseManager`.

    Args:
        user_uuid (str): The UUID of the user associated with the encrypted
            emergency.
        emergency_id (int): The unique identifier of the encrypted emergency
            to update.
        enc_emergency (enc_emergency.EncryptedEmergency): An
            EncryptedEmergency instance containing the updated encrypted data.

    Raises:
        sqlite3.Error: If an error occurs while updating the encrypted
            emergency in the database.
    """

    dbm = db.DatabaseManager.get_instance()
    dbm.update_encyrpted_emergency(user_uuid, emergency_id, enc_emergency)


def delete_request(user_uuid: str, emergency_id: int):
    """
    Deletes an encrypted emergency from the database.

    This function removes a specific encrypted emergency associated with the
    given user UUID and emergency ID by delegating the operation to the
    `DatabaseManager`.

    Args:
        user_uuid (str): The UUID of the user associated with the request.
        emergency_id (int): The unique identifier of the encrypted emergency
            request to delete.

    Raises:
        sqlite3.Error: If an error occurs while deleting the request from the
            database.
    """

    dbm = db.DatabaseManager.get_instance()
    dbm.delete_encrypted_emergency(user_uuid, emergency_id)
