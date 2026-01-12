from __future__ import annotations

import uuid
from typing import Self


class Payload:
    def __init__(
        self,
        user_uuid: str,
        emergency_id: int,
        severity: int,
        position: tuple[float, float],
    ) -> None:
        emergency_id_limit: int = 64
        severity_limit: int = 256
        lat_limits: tuple[int, int] = (-90, 90)
        lon_limits: tuple[int, int] = (-180, 180)

        try:
            uuid.UUID(user_uuid)
        except ValueError:
            raise ValueError("user_uuid must be a valid UUID string")

        if not (0 <= emergency_id < emergency_id_limit):
            raise ValueError("emergency_id must be in the range 0 <= emergency_id < 64")

        if not (0 <= severity < severity_limit):
            raise ValueError("severity must be in the range 0 <= severity < 256")

        if (
            not isinstance(position, tuple)
            or len(position) != 2
            or not all(isinstance(v, (int, float)) for v in position)
        ):
            raise ValueError("position must be a tuple (lat, lon)")

        lat, lon = position

        if not (lat_limits[0] <= lat <= lat_limits[1]):
            raise ValueError("Latitude must be in the range -90 <= lat <= 90")

        if not (lon_limits[0] <= lon <= lon_limits[1]):
            raise ValueError("Longitude must be in the range -180 <= lon <= 180")

        self.user_uuid = user_uuid
        self.emergency_id = emergency_id
        self.severity = severity
        self.position = (float(lat), float(lon))

    def pack_data(self):
        uuid_bytes = uuid.UUID(self.user_uuid).bytes

        lat_pos = int((self.position[0] + 90) * 511 / 180)
        lon_pos = int((self.position[1] + 180) * 511 / 360)

        packed = (
            (self.emergency_id << 26)  # 6 bit
            | (self.severity << 18)  # 8 bit
            | (lat_pos << 9)  # 9 bit
            | lon_pos  # 9 bit
        ).to_bytes(4, byteorder="big")

        return uuid_bytes + packed

    @classmethod
    def unpack_data(cls: type[Self], data: bytes) -> Self:
        if len(data) != 20:
            raise ValueError("Data must be exactly 20 bytes")

        uuid_bytes = data[:16]
        uuid_str = str(uuid.UUID(bytes=uuid_bytes))

        packed_data = int.from_bytes(data[16:20], byteorder="big")

        emergency_id = (packed_data >> 26) & 0b111111
        severity = (packed_data >> 18) & 0b11111111
        lat_pos = (packed_data >> 9) & 0b111111111
        lon_pos = packed_data & 0b111111111

        # TODO: find a way to increment the precision
        lat = lat_pos * 180 / 511 - 90
        lon = lon_pos * 360 / 511 - 180

        return cls(
            user_uuid=uuid_str,
            emergency_id=emergency_id,
            severity=severity,
            position=(lat, lon),
        )
