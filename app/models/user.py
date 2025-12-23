import datetime
from enum import Enum


class BloodType(Enum):
    ANEG = 0
    APOS = 1
    BPOS = 2
    BNEG = 3
    OPOS = 4
    ONEG = 5
    ABPOS = 6
    ABNEG = 7


class User:
    uuid: str
    is_rescuer: bool
    name: str
    surname: str
    birthday: datetime.date
    blood_type: BloodType
    # TODO: could be a new table
    health_info_str: str

    def __init__(
        self,
        uuid: str,
        is_rescuer: bool,
        name: str,
        surname: str,
        birthday: datetime.date,
        blood_type: BloodType,
        health_info_json: str,
    ) -> None:
        self.uuid = uuid
        self.is_rescuer = is_rescuer
        self.name = name
        self.surname = surname
        self.birthday = birthday
        self.blood_type = blood_type
        self.health_info_str = health_info_json

    def to_db_tuple(self) -> tuple:
        return (
            self.uuid,
            self.is_rescuer,
            self.name,
            self.surname,
            self.birthday,
            self.blood_type.name,  # The enum name (e.g: ONEG -> "ONEG")
            self.health_info_str,
        )
