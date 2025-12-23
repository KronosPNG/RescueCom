from __future__ import annotations
from typing import Self

import sqlite3
from models import emergency, user


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
        self.__init_db()

    @classmethod
    def get_instance(cls: type[Self], db_path: str | None = None) -> Self:
        if cls.__instance is None:
            if db_path is None:
                raise ValueError("'db_path' required on first initialization")

            cls.__allow_init = True
            cls.__instance = cls(db_path)
            cls.__allow_init = False

        return cls.__instance

    def __init_db(self) -> None:
        schema: str = """
        CREATE TABLE IF NOT EXISTS user (
            uuid TEXT PRIMARY KEY,
            is_rescuer INTEGER NOT NULL,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            birthday DATE NOT NULL,
            blood_type INTEGER NOT NULL,
            health_info_str TEXT DEFAULT '',

            CHECK (blood_type IN ('ANEG', 'APOS', 'BPOS', 'BNEG', 'OPOS', 'ONEG', 'ABPOS', 'ABNEG'))
        );

        CREATE TABLE IF NOT EXISTS emergency (
            id INTEGER PRIMARY KEY,
            user_uuid TEXT NOT NULL,
            position TEXT NULL DEFAULT '0,0,0',
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            street_number INTEGER NOT NULL,
            place_description TEXT,
            photo_b64 TEXT,
            resolved INTEGER NOT NULL,
            details_json TEXT
        );
        """

        for sub_query in schema.split(";"):
            self.conn.execute(sub_query)

        self.conn.commit()

    def insert_user(self, user: user.User) -> None:
        insert_query: str = "INSERT INTO user(uuid, is_rescuer, name, surname, birthday, blood_type, health_info_str) VALUES(?, ?, ?, ?, ?, ?, ?)"

        # Begin transaction
        self.conn.execute("BEGIN")
        try:
            self.conn.execute(insert_query, user.to_db_tuple())
            self.conn.commit()
        except self.conn.Error as e:
            self.conn.rollback()
            raise e

    def insert_emergency(self, emergency: emergency.Emergency) -> None:
        insert_query: str = """
            INSERT INTO emergency (user_uuid, position, address, city, street_number, place_description, photo_b64, resolved, details_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        # Begin transaction
        self.conn.execute("BEGIN")
        try:
            # Skip the field `id`
            vales = emergency.to_db_tuple()[1:]
            self.conn.execute(insert_query, vales)
            self.conn.commit()
        except self.conn.Error as e:
            self.conn.rollback()
            raise e
