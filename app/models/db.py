from __future__ import annotations
from typing import Self

import sqlite3


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

    @classmethod
    def get_instance(cls: type[Self], db_path: str | None = None) -> Self:
        if cls.__instance is None:
            if db_path is None:
                raise ValueError("'db_path' required on first initialization")

            cls.__allow_init = True
            cls.__instance = cls(db_path)
            cls.__allow_init = False

        return cls.__instance
