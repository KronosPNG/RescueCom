from __future__ import annotations
from typing import List, Self

import sqlite3
from datetime import datetime
from common.models import emergency, user, enc_emergency


class DatabaseManager:
    __instance = None
    __allow_init = False

    def __init__(self, db_path: str) -> None:
        if not DatabaseManager.__allow_init:
            raise TypeError(
                "DatabaseManager singleton must be created using DatabaseManager.get_instance"
            )

        # NOTE: For multithreading
        # self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        # Enable Foreign Key constraints. It's disabled by default
        # See: https://sqlite.org/foreignkeys.html "Overview" and "2. Enabling Foreign Key Support"
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.__init_db()

    @classmethod
    def get_instance(cls: type[Self], db_path: str | None = None) -> Self:
        """
        Returns the singleton instance of DatabaseManager.

        This class method implements the Singleton pattern. On the first call,
        a database path must be provided to initialize the underlying SQLite
        connection. Subsequent calls will return the already-created instance
        and will ignore the `db_path` parameter.

        Args:
            db_path (str | None): Path to the SQLite database file. This parameter
                is required only on the first invocation.

        Returns:
            DatabaseManager: The singleton instance of the database manager.

        Raises:
            ValueError: If `db_path` is not provided on the first invocation.
        """

        if cls.__instance is None:
            if db_path is None:
                raise ValueError("'db_path' required on first initialization")

            cls.__allow_init = True
            cls.__instance = cls(db_path)
            cls.__allow_init = False

        return cls.__instance

    def __init_db(self) -> None:
        """
        Initialize the database by creating the schema.
        """

        schema: str = """
        CREATE TABLE IF NOT EXISTS user (
            uuid TEXT PRIMARY KEY,
            is_rescuer INTEGER NOT NULL,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            birthday DATE NOT NULL,
            blood_type INTEGER NOT NULL,
            health_info_json TEXT DEFAULT '',

            CHECK (blood_type IN ('ANEG', 'APOS', 'BPOS', 'BNEG', 'OPOS', 'ONEG', 'ABPOS', 'ABNEG'))
        );

        CREATE TABLE IF NOT EXISTS emergency (
            emergency_id INTEGER NOT NULL,
            user_uuid TEXT NOT NULL,
            position TEXT DEFAULT '0,0',
            address TEXT,
            city TEXT,
            street_number INTEGER,
            place_description TEXT,
            photo_b64 TEXT,
            severity INTEGER NOT NULL,
            resolved INTEGER NOT NULL,
            emergency_type TEXT NOT NULL,
            description TEXT NOT NULL,
            details_json TEXT,
            created_at DATE DEFAULT CURRENT_TIMESTAMP,

            PRIMARY KEY (emergency_id, user_uuid)
        );

        CREATE TABLE IF NOT EXISTS encrypted_emergency (
            emergency_id INTEGER NOT NULL,
            user_uuid TEXT NOT NULL,
            severity INTEGER NOT NULL,
            routing_info_json TEXT NOT NULL,
            blob BLOB NOT NULL,
            created_at DATE DEFAULT CURRENT_TIMESTAMP,

            /*
                In order to prevent the violation of
                the foreign key constraint, when the user
                receives an emergency from another user,
                the sender must also send their user_uuid,
                and the receiver must insert it into the
                `user` table before inserting the newly
                received emergency.
            */
            PRIMARY KEY (emergency_id, user_uuid)
        );
        """

        for sub_query in schema.split(";"):
            self.conn.execute(sub_query)

        self.conn.commit()

    def insert_user(self, user: user.User) -> None:
        """
        Inserts a User into the database.

        The operation is wrapped in an explicit transaction:
        the transaction is committed on success and rolled back if an error
        occurs.

        Args:
            user (user.User): The User instance to be inserted into the database.

        Raises:
            sqlite3.Error: If the insertion fails, the transaction is rolled back
                and the original database error is re-raised.
        """

        insert_query: str = "INSERT INTO user(uuid, is_rescuer, name, surname, birthday, blood_type, health_info_json) VALUES(?, ?, ?, ?, ?, ?, ?)"

        # Begin transaction
        self.conn.execute("BEGIN")
        try:
            self.conn.execute(insert_query, user.to_db_tuple())
            self.conn.commit()
        except self.conn.Error as e:
            self.conn.rollback()
            raise e

    def insert_emergency(self, emergency: emergency.Emergency) -> int | None:
        """
        Inserts an Emergency into the database.

        The operation is wrapped in an explicit transaction:
        the transaction is committed on success and rolled back if an error
        occurs.

        Args:
            emergency (emergency.Emergency): The Emergency instance to be
                inserted into the database.

        Returns:
        int | None: The ID of the newly inserted emergency record, or `None`
            if the database does not provide a last inserted row ID.

        Raises:
            sqlite3.Error: If the insertion fails, the transaction is rolled back
                and the original database error is re-raised.
        """

        insert_query: str = """
            INSERT INTO emergency (emergency_id, user_uuid, position, address, city, street_number, place_description,
            photo_b64, severity, resolved, emergency_type, description, details_json, created_at)
            VALUES (SQ, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        # Begin transaction
        self.conn.execute("BEGIN")
        try:
            # Skip the field `id`
            values = emergency.to_db_tuple()[1:]
            self.conn.execute(insert_query, values)
            self.conn.commit()
        except self.conn.Error as e:
            self.conn.rollback()
            raise e

        return self.cursor.lastrowid

    def insert_emergency_from_rescuee(self, emergency: emergency.Emergency) -> None:
        """
        Inserts an Emergency from the Rescuee into the database.

        The operation is wrapped in an explicit transaction:
        the transaction is committed on success and rolled back if an error
        occurs.

        Args:
            emergency (emergency.Emergency): The Emergency instance to be
                inserted into the database.

        Returns:
        int | None: The ID of the newly inserted emergency record, or `None`
            if the database does not provide a last inserted row ID.

        Raises:
            sqlite3.Error: If the insertion fails, the transaction is rolled back
                and the original database error is re-raised.
        """

        insert_query: str = """
            INSERT INTO emergency (emergency_id, user_uuid, position, address, city, street_number, place_description, photo_b64,
            severity, resolved, emergency_type, description, details_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        # Begin transaction
        self.conn.execute("BEGIN")
        try:
            self.conn.execute(insert_query, emergency.to_db_tuple())
            self.conn.commit()
        except self.conn.Error as e:
            self.conn.rollback()
            raise e

    def insert_encrypted_emergency(
        self, enc_emergency: enc_emergency.EncryptedEmergency
    ) -> None:
        """
        Inserts an EncryptedEmergency into the database.

        The operation is wrapped in an explicit transaction:
        the transaction is committed on success and rolled back if an error
        occurs.

        Args:
            enc_emergency (emergency.Emergency): The EncryptedEmergency instance to be
                inserted into the database.

        Raises:
            sqlite3.Error: If the insertion fails, the transaction is rolled back
                and the original database error is re-raised.
        """

        insert_query = """
            INSERT INTO encrypted_emergency(emergency_id, user_uuid, severity, routing_info_json, blob, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """

        # Begin transaction
        self.conn.execute("BEGIN")
        try:
            values = enc_emergency.to_db_tuple()
            self.conn.execute(insert_query, values)
            self.conn.commit()
        except self.conn.Error as e:
            self.conn.rollback()
            raise e

    def get_users(self) -> List[user.User]:
        """
        Retrieves all users stored in the database.

        This method queries the `user` table and converts each database row
        into a `User` object. Database-specific representations are
        translated into application-level types.

        Returns:
            List[user.User]: A list of User instances representing all users
            currently stored in the database.

        Raises:
            sqlite3.Error: If an error occurs while executing the SELECT query
                or fetching the results.
            ValueError: If the stored date or enum values cannot be parsed into
                the expected Python types.
        """

        select_query = """
            SELECT uuid, is_rescuer, name, surname, birthday, blood_type, health_info_json
            FROM user
        """

        self.cursor.execute(select_query)
        result = self.cursor.fetchall()

        users = []

        for row in result:
            users.append(
                user.User(
                    uuid=row[0],
                    is_rescuer=row[1] == 1,
                    name=row[2],
                    surname=row[3],
                    birthday=datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S.%f").date(),
                    blood_type=user.BloodType[row[5]],
                    health_info_json=row[6],
                )
            )

        return users

    def get_user_by_uuid(self, uuid: str) -> user.User | None:
        """
        Retrieves a user by uuid.

        This method queries the `user` table for the user with the UUID
        passed as an argument and converts each database row into a `User`
        object. Database-specific representations are translated into
        application-level types.

        Args:
            uuid (str): The UUID of the user to retrieve.

        Returns:
            user.User | None: The `User` instance corresponding to the given UUID,
            or `None` if no matching user is found.

        Returns:
            user.User: The user with the corresponding UUID.

        Raises:
            sqlite3.Error: If an error occurs while executing the SELECT query
                or fetching the results.
            ValueError: If the stored date or enum values cannot be parsed into
                the expected Python types.
        """

        select_query = """
            SELECT uuid, is_rescuer, name, surname, birthday, blood_type, health_info_json
            FROM user
            WHERE uuid = ?
        """

        self.cursor.execute(select_query, (uuid,))
        result = self.cursor.fetchone()

        if result is None:
            return None

        return user.User(
            uuid=result[0],
            is_rescuer=result[1] == 1,
            name=result[2],
            surname=result[3],
            birthday=datetime.strptime(result[4], "%Y-%m-%d %H:%M:%S.%f").date(),
            blood_type=user.BloodType[result[5]],
            health_info_json=result[6],
        )

    def get_rescuers(self) -> List[user.User]:
        """
        Retrieves all Rescuers stored in the database.

        This method queries the `user` table for the role of Rescuer (is_rescuer = 1)
        and converts each database row into a `User` object. Database-specific
        representations are translated into application-level types.

        This method queries the `user` table for users whose `is_rescuer` flag
        is set to true (value `1` in the database) and converts each database
        row into a `User` object. Database-specific representations are
        translated into application-level types.

        Returns:
            List[user.User]: A list of User instances representing all Rescuers
            currently stored in the database.

        Raises:
            sqlite3.Error: If an error occurs while executing the SELECT query
                or fetching the results.
            ValueError: If the stored date or enum values cannot be parsed into
                the expected Python types.
        """

        select_query = """
            SELECT uuid, is_rescuer, name, surname, birthday, blood_type, health_info_json
            FROM user
            WHERE is_rescuer = 1
        """

        self.cursor.execute(select_query)
        result = self.cursor.fetchall()

        rescuers = []

        for row in result:
            rescuers.append(
                user.User(
                    uuid=row[0],
                    is_rescuer=row[1] == 1,
                    name=row[2],
                    surname=row[3],
                    birthday=datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S.%f").date(),
                    blood_type=user.BloodType[row[5]],
                    health_info_json=row[6],
                )
            )

        return rescuers

    def get_rescuees(self) -> List[user.User]:
        """
        Retrieves all Rescuees stored in the database.

        This method queries the `user` table for the role of Rescuee (is_rescuer = 0)
        and converts each database row into a `User` object. Database-specific
        representations are translated into application-level types.

        This method queries the `user` table for users whose `is_rescuer` flag
        is set to false (value `0` in the database) and converts each database
        row into a `User` object. Database-specific representations are
        translated into application-level types.

        Returns:
            List[user.User]: A list of User instances representing all Rescuees
            currently stored in the database.

        Raises:
            sqlite3.Error: If an error occurs while executing the SELECT query
                or fetching the results.
            ValueError: If the stored date or enum values cannot be parsed into
                the expected Python types.
        """

        select_query = """
            SELECT uuid, is_rescuer, name, surname, birthday, blood_type, health_info_json
            FROM user
            WHERE is_rescuer = 0
        """

        self.cursor.execute(select_query)
        result = self.cursor.fetchall()

        rescuees = []

        for row in result:
            rescuees.append(
                user.User(
                    uuid=row[0],
                    is_rescuer=row[1] == 1,
                    name=row[2],
                    surname=row[3],
                    birthday=datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S.%f").date(),
                    blood_type=user.BloodType[row[5]],
                    health_info_json=row[6],
                )
            )

        return rescuees

    def get_emergencies(self) -> List[emergency.Emergency]:
        """
        Retrieves all emergencies stored in the database.

        This method queries the `emergency` table and converts each database row
        into a `Emergency` object. Database-specific representations are
        translated into application-level types.

        Returns:
            List[emergency.Emergency]: A list of Emergency instances representing all
            emergencies currently stored in the database.

        Raises:
            sqlite3.Error: If an error occurs while executing the SELECT query
                or fetching the results.
            ValueError: If the stored position or other fields cannot be parsed
                into the expected Python types.
        """

        select_query = """
            SELECT emergency_id, user_uuid, position, address, city, street_number,
            place_description, photo_b64, severity, resolved, emergency_type, description,
            details_json, created_at
            FROM emergency
        """

        self.cursor.execute(select_query)
        result = self.cursor.fetchall()

        emergencies = []

        for row in result:
            emergencies.append(
                emergency.Emergency(
                    emergency_id=row[0],
                    user_uuid=row[1],
                    position=tuple(row[2].split(",")),
                    address=row[3],
                    city=row[4],
                    street_number=row[5],
                    place_description=row[6],
                    photo_b64=row[7],
                    severity=row[8],
                    resolved=row[9] == 1,  # If True the emergency is resolved
                    emergency_type=row[10],
                    description=row[11],
                    details_json=row[12],
                    created_at=datetime.strptime(row[13], "%Y-%m-%d %H:%M:%S.%f"),
                )
            )

        return emergencies

    def get_emergency_by_id(
        self, user_uuid: str, id: int
    ) -> emergency.Emergency | None:
        """
        Retrieves a specific emergency by user UUID and emergency ID.

        This method queries the `emergency` table for the emergency with the
        user UUID and ID passed as argument and converts the resulting database
        row into an `Emergency` object. Database-specific representations
        are translated into application-level types.

        Args:
            user_uuid (str): The UUID of the user associated with the emergency.
            id (int): The ID of the emergency to retrieve.

        Returns:
            emergency.Emergency | None: The `Emergency` instance corresponding to
            the given user UUID and ID, or `None` if no matching record is found.

        Raises:
            sqlite3.Error: If an error occurs while executing the SELECT query
                or fetching the result.
            ValueError: If the stored position or other fields cannot be parsed
                into the expected Python types.
        """

        select_query = """
            SELECT emergency_id, user_uuid, position, address, city, street_number,
            place_description, photo_b64, severity, resolved, emergency_type, description,
            details_json, created_at
            FROM emergency
            WHERE user_uuid = ? AND emergency_id = ?
        """

        self.cursor.execute(select_query, (user_uuid, id))
        result = self.cursor.fetchone()

        if result is None:
            return None

        return emergency.Emergency(
            emergency_id=result[0],
            user_uuid=result[1],
            position=tuple(result[2].split(",")),
            address=result[3],
            city=result[4],
            street_number=result[5],
            place_description=result[6],
            photo_b64=result[7],
            severity=result[8],
            resolved=result[9] == 1,  # If True the emergency is resolved
            emergency_type=result[10],
            description=result[11],
            details_json=result[12],
            created_at=datetime.strptime(result[13], "%Y-%m-%d %H:%M:%S.%f"),
        )

    def get_emergencies_by_user_uuid(self, user_uuid: str) -> List[emergency.Emergency]:
        """
        Retrieves all emergencies associated with a specific user UUID.

        This method queries the `emergency` table for all the emergencies matching
        the user UUID passed as an argument and converts each resulting
        database row into an `Emergency` object. Database-specific representations
        are translated into application-level types.

        Args:
            user_uuid (str): The UUID of the user whose emergencies are to be
                retrieved.

        Returns:
            List[emergency.Emergency]: A list of Emergency instances associated
            with the specified user.

        Raises:
            sqlite3.Error: If an error occurs while executing the SELECT query
                or fetching the results.
            ValueError: If the stored position or other fields cannot be parsed
                into the expected Python types.
        """

        select_query = """
            SELECT emergency_id, user_uuid, position, address, city, street_number,
            place_description, photo_b64, severity, resolved, emergency_type, description,
            details_json, created_at
            FROM emergency
            WHERE user_uuid = ?
        """

        self.cursor.execute(select_query, (user_uuid,))
        result = self.cursor.fetchall()

        emergencies = []

        for row in result:
            emergencies.append(
                emergency.Emergency(
                    emergency_id=row[0],
                    user_uuid=row[1],
                    position=tuple(row[2].split(",")),
                    address=row[3],
                    city=row[4],
                    street_number=row[5],
                    place_description=row[6],
                    photo_b64=row[7],
                    severity=row[8],
                    resolved=row[9] == 1,  # If True the emergency is resolved
                    emergency_type=row[10],
                    description=row[11],
                    details_json=row[12],
                    created_at=datetime.strptime(row[13], "%Y-%m-%d %H:%M:%S.%f"),
                )
            )

        return emergencies

    def get_encrypted_emergencies(self) -> List[enc_emergency.EncryptedEmergency]:
        """
        Retrieves all encrypted emergencies stored in the database.

        This method queries the `encrypted_emergency` table and converts each
        database row into an `EncryptedEmergency` object.

        Returns:
            List[enc_emergency.EncryptedEmergency]: A list of EncryptedEmergency
            instances representing all encrypted emergencies currently stored
            in the database.

        Raises:
            sqlite3.Error: If an error occurs while executing the SELECT query
                or fetching the results.
        """

        select_query = """
            SELECT emergency_id, user_uuid, severity, routing_info_json, blob, created_at
            FROM encrypted_emergency
        """

        self.cursor.execute(select_query)
        result = self.cursor.fetchall()

        enc_emergencies = []

        for row in result:
            enc_emergencies.append(
                enc_emergency.EncryptedEmergency(
                    emergency_id=row[0],
                    user_uuid=row[1],
                    severity=row[2],
                    routing_info_json=row[3],
                    blob=row[4],
                    created_at=datetime.strptime(result[5], "%Y-%m-%d %H:%M:%S.%f"),
                )
            )

        return enc_emergencies

    def update_user(self, uuid: str, user: user.User) -> None:
        """
        Updates an existing user record in the database.

        This method updates the fields of a user identified by the given UUID
        using the values provided by the `User` instance. The update operation
        is executed within an explicit transaction: changes are committed on
        success and rolled back if an error occurs.

        Args:
            uuid (str): The UUID of the user record to update.
            user (user.User): A User instance containing the updated values.
                The UUID field of the object is not used for identification.

        Raises:
            sqlite3.Error: If the update operation fails, the transaction is
                rolled back and the original database error is re-raised.
        """

        update_query = """
            UPDATE user
            SET is_rescuer = ?, name = ?, surname = ?, birthday = ?,
            blood_type = ?, health_info_json = ?
            WHERE uuid = ?
        """

        # Beging transaction
        self.conn.execute("BEGIN")
        try:
            self.cursor.execute(update_query, (*user.to_db_tuple()[1:], uuid))
            self.conn.commit()
        except self.conn.Error as e:
            self.conn.rollback()
            raise e

    def update_emergency(
        self, uuid: str, id: int, emergency: emergency.Emergency
    ) -> None:
        """
        Updates an existing emergency record in the database.

        This method updates the fields of an emergency identified by the given
        emergency ID and user UUID using the values provided by the
        `Emergency` instance. The update operation is executed within an
        explicit transaction: changes are committed on success and rolled back
        if an error occurs.

        Args:
            uuid (str): The UUID of the user associated with the emergency.
            id (int): The unique identifier of the emergency to update.
            emergency (emergency.Emergency): An Emergency instance containing
                the updated values. The `id` and `user_uuid` fields of the
                object are not used for record identification.

        Raises:
            sqlite3.Error: If the update operation fails, the transaction is
                rolled back and the original database error is re-raised.
        """

        update_query = """
            UPDATE emergency
            SET position = ?, address = ?, city = ?, street_number = ?,
            place_description = ?, photo_b64 = ?, severity = ?, resolved = ?,
            emergency_type = ?, description = ?, details_json = ?, created_at = ?
            WHERE emergency_id = ? AND user_uuid = ?
        """

        # Beging transaction
        self.conn.execute("BEGIN")
        try:
            self.cursor.execute(
                update_query,
                (*emergency.to_db_tuple()[2:], id, uuid),
            )
            self.conn.commit()
        except self.conn.Error as e:
            self.conn.rollback()
            raise e

    def update_encrypted_emergency(
        self,
        user_uuid: str,
        emergency_id: int,
        enc_emergency: enc_emergency.EncryptedEmergency,
    ) -> None:
        """
        Updates an existing encrypted emergency record in the database.

        This method updates the encrypted data associated with an emergency
        identified by the given user UUID and emergency ID. The update
        operation is executed within an explicit transaction: changes are
        committed on success and rolled back if an error occurs.

        Args:
            user_uuid (str): The UUID of the user associated with the encrypted
                emergency.
            emergency_id (int): The unique identifier of the encrypted emergency
                to update.
            enc_emergency (enc_emergency.EncryptedEmergency): An
                EncryptedEmergency instance containing the updated encrypted
                data. The identifying fields of the object are not used for
                record selection.

        Raises:
            sqlite3.Error: If the update operation fails, the transaction is
                rolled back and the original database error is re-raised.
        """

        update_query = """
            UPDATE encrypted_emergency
            SET severity = ?, routing_info_json = ?, blob = ?, created_at = ?
            WHERE user_uuid = ?, emergency_id = ?
        """

        # Beging transaction
        self.conn.execute("BEGIN")
        try:
            self.cursor.execute(
                update_query,
                (*enc_emergency.to_db_tuple()[2:], user_uuid, emergency_id),
            )
            self.conn.commit()
        except self.conn.Error as e:
            self.conn.rollback()
            raise e

    def delete_user(self, uuid: str) -> None:
        """
        Deletes a user record from the database.

        This method removes the user identified by the given UUID from the
        `user` table. The deletion is executed within an explicit transaction:
        the transaction is committed on success and rolled back if an error
        occurs.

        Args:
            uuid (str): The UUID of the user to delete.

        Raises:
            sqlite3.Error: If the deletion operation fails, the transaction is
                rolled back and the original database error is re-raised.
        """

        delete_query = """
            DELETE FROM user
            WHERE uuid = ?
        """

        # Beging transaction
        self.conn.execute("BEGIN")
        try:
            self.cursor.execute(delete_query, (uuid,))
            self.conn.commit()
        except self.conn.Error as e:
            self.conn.rollback()
            raise e

    def delete_emergency(self, user_uuid: str, id: int) -> None:
        """
        Deletes an emergency record from the database.

        This method removes the emergency identified by the given emergency ID
        and associated user UUID from the `emergency` table. The deletion is
        executed within an explicit transaction: the transaction is committed
        on success and rolled back if an error occurs.

        Args:
            user_uuid (str): The UUID of the user associated with the emergency.
            id (int): The unique identifier of the emergency to delete.

        Raises:
            sqlite3.Error: If the deletion operation fails, the transaction is
                rolled back and the original database error is re-raised.
        """

        delete_query = """
            DELETE FROM emergency
            WHERE emergency_id = ? AND user_uuid = ?
        """

        # Beging transaction
        self.conn.execute("BEGIN")
        try:
            self.cursor.execute(delete_query, (id, user_uuid))
            self.conn.commit()
        except self.conn.Error as e:
            self.conn.rollback()
            raise e

    def delete_encrypted_emergency(self, user_uuid: str, emergency_id: int) -> None:
        """
        Deletes a specific encrypted emergency from the database.

        This method removes the encrypted emergency record identified by the
        given user UUID and emergency ID from the `encrypted_emergency` table.
        The deletion is executed within an explicit transaction: the
        transaction is committed on success and rolled back if an error
        occurs.

        Args:
            user_uuid (str): The UUID of the user associated with the encrypted
                emergency.
            emergency_id (int): The unique identifier of the encrypted emergency
                to delete.

        Raises:
            sqlite3.Error: If the deletion operation fails, the transaction is
                rolled back and the original database error is re-raised.
        """

        delete_query = """
            DELETE FROM encrypted_emergency
            WHERE user_uuid = ? AND emergency_id = ?
        """

        # Beging transaction
        self.conn.execute("BEGIN")
        try:
            self.cursor.execute(delete_query, (user_uuid, emergency_id))
            self.conn.commit()
        except self.conn.Error as e:
            self.conn.rollback()
            raise e
