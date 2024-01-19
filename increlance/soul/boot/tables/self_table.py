import uuid

from increlance.triangle import Triangle
from increlance.soul.boot.database import Database
from typing import cast


class SelfTable(Triangle):
    db: Database

    def __init__(self, parent: Triangle):
        super().__init__(
            parent,
            self.__class__.__name__
        )
        self.db = cast(Database, self.get('../..'))
        self.create()

    def create(self):
        self.db.get("""query?sql='
        create table if not exists triangle
        (
            uuid    text
                constraint triangle_pk
                    primary key,
            type    text,
            name    text,
            center  text
                constraint triangle_triangle_uuid_fk1
                    references triangle,
            "right" text
                constraint triangle_triangle_uuid_fk2
                    references triangle,
            "left"  text
                constraint triangle_triangle_uuid_fk3
                    references triangle,
            up      text
                constraint triangle_triangle_uuid_fk4
                    references triangle,
            data    INTEGER
        );
        '""")
        self.db.get("""query?sql='
        create table if not exists self
        (
            self_uuid text
                constraint self_triangle_uuid_fk2
                    references triangle,
            this_uuid text
                constraint self_triangle_uuid_fk
                    references triangle,
            constraint self_pk
                primary key (self_uuid, this_uuid)
        );
        '""")
        self.db.connection.commit()

    def get_triangle_id(self, value: Triangle) -> uuid:
        if value.uuid is not None:
            return value.uuid

        res = self.db.get(
            f"query?sql='SELECT uuid FROM triangle WHERE type = :type AND name = :name;'&type='{type(value).__name__}'&name='{value.name}'")

        if res is None or len(res) == 0:
            return uuid.uuid4()
        return uuid.UUID(res[0]['uuid'])

    def save_triangle(self, value: Triangle):
        uid = None
        if value.uuid is None:
            res = self.db.get(
                f"query?sql='SELECT uuid FROM triangle WHERE type = :type AND name = :name;'&type='{type(value).__name__}'&name='{value.name}'"
            )

            if res is not None and len(res) != 0:
                uid = uuid.UUID(res[0]['uuid'])
        else:
            res = self.db.get(
                f"query?sql='SELECT uuid FROM triangle WHERE uuid = :uuid;'&uuid='{value.uuid.hex}'"
            )

            if res is not None and len(res) != 0:
                uid = uuid.UUID(res[0]['uuid'])

        if uid is None or uid != value.uuid:
            value.uuid = uid if uid is not None else value.uuid
            self.db.get(
                f"query?sql='INSERT INTO triangle (uuid, type, name) VALUES (:uuid, :type, :name);'&type='{type(value).__name__}'&name='{value.name}'&uuid='{value.uuid.hex}'"
            )
            self.db.get(
                f"query?sql='INSERT INTO self (self_uuid, this_uuid) VALUES (:self_uuid, :this_uuid);'&self_uuid='{value.root().uuid.hex}'&this_uuid='{value.uuid.hex}'"
            )
        else:
            self.db.get(
                f"query?sql='UPDATE triangle SET type = :type, name = :name WHERE uuid = :uuid;'&type='{type(value).__name__}'&name='{value.name}'&uuid='{value.uuid.hex}'"
            )
        self.db.connection.commit()
