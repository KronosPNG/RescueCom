from common.models import db, enc_emergency, user, emergency


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


def save_emergency(emergency: emergency.Emergency) -> None:
    """
    Persists an emergency to the database.

    This function stores the given `Emergency` instance in the database by
    delegating the operation to the `DatabaseManager`.
    The emergency is persisted until it is resolved or explicitly removed.

    Args:
        emergency (emergency.Emergency): The Emergency instance to be
            persisted in the database.

    Raises:
        sqlite3.Error: If an error occurs while inserting the emergency into
            the database.
    """

    dbm = db.DatabaseManager.get_instance()
    dbm.insert_emergency(emergency)


def update_emergency(
    user_uuid: str,
    emergency_id: int,
    emergency: emergency.Emergency,
) -> None:
    """
    Updates an emergency record in the database.

    This function updates the data of an emergency associated with the
    given user UUID and emergency ID by delegating the operation to the
    `DatabaseManager`.

    Args:
        user_uuid (str): The UUID of the user associated with the
            emergency.
        emergency_id (int): The unique identifier of the emergency to
            update.
        emergency (emergency.Emergency): An Emergency instance containing
            the updated data.

    Raises:
        sqlite3.Error: If an error occurs while updating the emergency into
            the database.
    """

    dbm = db.DatabaseManager.get_instance()
    dbm.update_emergency(user_uuid, emergency_id, emergency)


def delete_emergency(user_uuid: str, emergency_id: int):
    """
    Deletes an emergency from the database.

    This function removes a specific emergency associated with the given
    user UUID and emergency ID by delegating the operation to the
    `DatabaseManager`.

    Args:
        user_uuid (str): The UUID of the user associated with the request.
        emergency_id (int): The unique identifier of the emergency request
        to delete.

    Raises:
        sqlite3.Error: If an error occurs while deleting the request from the
            database.
    """

    dbm = db.DatabaseManager.get_instance()
    dbm.delete_emergency(user_uuid, emergency_id)


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
    dbm.update_encrypted_emergency(user_uuid, emergency_id, enc_emergency)


def delete_encrypted_emergency(user_uuid: str, emergency_id: int):
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
