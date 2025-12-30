from typing import Self
import datetime, struct


class Emergency:
    def __init__(
        self,
        emergency_id: int,
        user_uuid: str,
        address: str,
        city: str,
        street_number: int,
        severity: int,
        created_at: datetime.datetime,
        resolved: bool = False,
        position: tuple[float, float] = (0.0, 0.0),
        place_description: str = "",
        photo_b64: str = "",
        details_json: str = "",
    ) -> None:
        self.emergency_id = emergency_id
        self.user_uuid = user_uuid
        self.position = position
        self.address = address
        self.city = city
        self.street_number = street_number
        self.place_description = place_description
        self.photo_b64 = photo_b64
        self.severity = severity
        self.resolved = resolved
        self.details_json = details_json
        self.created_at = created_at

    def to_db_tuple(self) -> tuple:
        """
        Converts the emergency instance into a tuple suitable for SQLite insertion.

        The returned tuple contains the emergency attributes in a fixed order,
        matching the expected parameter order of the insert query.
        The `position` tuple is serialized as a comma-separated string.

        Returns:
            tuple: A tuple containing the following values, in order:
                - emergency_id (int): Unique identifier of the emergency.
                - user_uuid (str): UUID of the user who created the emergency.
                - position (str): Serialized position as "x,y".
                - address (str): Street address of the emergency.
                - city (str): City where the emergency occurred.
                - street_number (int): Street number of the address.
                - place_description (str): Additional place description.
                - photo_b64 (str): Base64-encoded photo associated with the emergency.
                - severity (int): The severity score of the emergency.
                - resolved (bool): Whether the emergency has been resolved.
                - details_json (str): Serialized emergency details.
                - created_at (datetime.datetime): Timestamp indicating when the
                    emergency was created.
        """

        return (
            self.emergency_id,
            self.user_uuid,
            # NOTE: Saved in the db as: "x,y"
            f"{self.position[0]},{self.position[1]}",
            self.address,
            self.city,
            self.street_number,
            self.place_description,
            self.photo_b64,
            self.severity,
            self.resolved,
            self.details_json,
            self.created_at,
        )

    def pack(self) -> bytes:
        """
        Pack an Emergency using the struct module (not all fields)
        """

        def pack_str(s: str):
            return struct.pack(f"<I{}s".format(len(s)), len(s), s.encode())

        return pack_str(self.position) +
            pack_str(self.address) +
            pack_str(self.city) +
            struct.pack("<I", self.street_number) +
            pack_str(self.place_description) +
            pack_str(self.photo_b64) +
            struct.pack("<I", self.severity) +
            struct.pack("?", self.resolved) +
            pack_str(self.details_json) +
            pack_str(str(self.created_at))

    @classmethod
    def unpack(cls: type[Self], emergency_id: int, user_uuid: str, data: bytes) -> Self:
        """
        Unpack a bytes object to an instance of Emergency

        Args:
            emergency_id (int): emergency id
            user_uuid (str): uuid of the user who's owner of the Emergency
            data (bytes): bytes blob (usually result of decryption)

        Returns:
            The instantiated Emergency

        Raises:
            TypeError: if any argument is of the wrong type
            ValueError: if instantiation fails
        """

        def unpack_str(blob: bytes):
            length = struct.unpack("<I", blob[:4])[0]
            unpacked = struct.unpack("{}s".format(length), blob[4:])
            return blob[4+length:], unpacked[0].decode()

        if not isinstance(emergency_id, int) or not isinstance(user_uuid, str) or not isinstance(data, bytes):
            raise TypeError("Wrong types for arguments")

        try:
            blob, position_str = unpack_str(blob)
            blob, address = unpack_str(blob)
            blob, city = unpack_str(blob)
            blob, street_number = blob[4:], struct.unpack("<I", blob)[0]
            blob, place_description = unpack_str(blob)
            blob, photo_b64 = unpack_str(blob)
            blob, severity = blob[4:], struct.unpack("<I", blob)[0]
            blob, resolved = blob[1:], struct.unpack("?", blob)[0]
            blob, details_json = unpack_str(blob)
            blob, created_at_str = unpack_str(blob)

            position = tuple(map(float, position_str.split(',')))
            created_at = datetime.fromisoformat(created_at_str)

            return Emergency(emergency_id,
                             user_uuid,
                             address,
                             city,
                             street_number,
                             severity,
                             created_at,
                             resolved,
                             position,
                             place_description,
                             photo_b64,
                             details_json)
        except Exception as e:
            raise ValueError("Something went wrong:" + str(e))
