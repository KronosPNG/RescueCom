class EncryptedEmergency:
    def __init__(
        self,
        emergency_id: int,
        user_uuid: str,
        severity: int,
        routing_info_json: str,
        blob: bytes,
    ) -> None:
        self.emergency_id = emergency_id
        self.user_uuid = user_uuid
        self.severity = severity
        self.routing_info_json = routing_info_json
        self.blob = blob

    def to_db_tuple(self) -> tuple:
        """
        Converts the encrypted_emergency instance into a tuple suitable for SQLite insertion.

        The returned tuple contains the emergency attributes in a fixed order,
        matching the expected parameter order of the insert query.

        Returns:
            tuple: A tuple containing the following values, in order:
                - emergency_id (int): Unique identifier of the emergency.
                - user_uuid (str): UUID of the user who created the emergency.
                - severity (int): The severity score of the emergency.
                - routing_info_json (str): Serialized routing informations.
                - blob (bytes): encrypted values
        """
        return (
            self.emergency_id,
            self.user_uuid,
            self.severity,
            self.routing_info_json,
            self.blob,
        )
