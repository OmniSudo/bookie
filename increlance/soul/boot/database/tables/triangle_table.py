import uuid

from increlance.triangle import Triangle
from increlance.soul.boot.database.database import Database
from typing import cast


class TriangleTable(Triangle):
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
                primary key (this_uuid)
        );
        '""")
        self.db.connection.commit()

    def get_id(self, value: Triangle) -> uuid:
        if value.uuid is not None:
            return value.uuid

        root = value.root()
        self_hex = root.uuid.hex if root.uuid is not None else ''
        res = self.db.get(
            f"query?sql='SELECT triangle.uuid as uuid FROM self JOIN triangle ON ((:self_uuid IS NULL OR :self_uuid == '') or self.self_uuid = :self_uuid) AND self.this_uuid = triangle.uuid AND type = :type AND name = :name;'&self_uuid='{self_hex}'&type='{type(value).__name__}'&name='{value.name}'"
        )

        if res is None or len(res) == 0:
            return uuid.uuid4()
        return uuid.UUID(res[0]['uuid'])

    def change(self, old: uuid.UUID, new: uuid.UUID) -> None:
        self.db.get(
            f"query?sql='UPDATE self SET this_uuid = :new_uuid WHERE this_uuid = :old_uuid;'&new_uuid='{new.hex}'&old_uuid='{old.hex}'"
        )
        self.db.get(
            f"query?sql='UPDATE triangle SET uuid = :new_uuid WHERE uuid = :old_uuid;'&new_uuid='{new.hex}'&old_uuid='{old.hex}'"
        )


    def save(self, value: Triangle):
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

        center_uuid = ''
        up_uuid = ''
        right_uuid = ''
        left_uuid = ''

        if value.center_child is not None:
            if value.center_child.uuid is not None:
                center_uuid = value.center_child.uuid.hex
                self.save(value.center_child)
        if value.top_child is not None:
            if value.top_child.uuid is not None:
                top_uuid = value.top_child.uuid.hex
                self.save(value.top_child)
        if value.right_child is not None:
            if value.right_child.uuid is not None:
                right_uuid = value.right_child.uuid.hex
                self.save(value.right_child)
        if value.left_child is not None:
            if value.left_child.uuid is not None:
                left_uuid = value.left_child.uuid.hex
                self.save(value.left_child)

        self.db.get(
            f"query?sql='UPDATE triangle SET center = :center, up = :up, right = :right, left = :left WHERE uuid = :uuid;'&uuid='{value.uuid.hex}'&center='{center_uuid}'&up='{up_uuid}'&right='{right_uuid}'&left='{left_uuid}'"
        )

        self.db.connection.commit()
