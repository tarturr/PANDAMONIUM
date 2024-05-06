import flask as fk

from datetime import datetime

from pandamonium.database import get_db
from pandamonium.security import date_from_string, date_to_string, uuid_split

from uuid import uuid4

class Branch:
    """Classe représentant une branche d'un bambou.
    Une branche est un endroit où les utilisateurs, les pandas, peuvent envoyer des messages au sein d'un bambou.
    Un bambou peut contenir une ou plusieurs branches.
    Les attributs d'une branche sont :
    """

    def __init__(
            self,
            branch_uuid: str = None,
            name: str = None,
            parent_bamboo: str = None
    ):
        if branch_uuid is not None:
            self.uuid = branch_uuid
            db = get_db()
            with db.cursor() as curs:
                curs.execute(
                    'SELECT name, parent_bamboo FROM branches WHERE uuid = %s',
                    [self.uuid]
                )
                branch = curs.fetchone()
                self.name = branch[0]
                self.parent_bamboo = branch[1]

        elif name is not None and parent_bamboo is not None:
            self.uuid = str(uuid4())
            self.name = name
            self.parent_bamboo = fk.g.user

            db = get_db()
            db.cursor().execute(
                'INSERT INTO branches(uuid, name, bamboo_parent) VALUES (%s, %s, %s)',
                (self.uuid, self.name, self.parent_bamboo)
            )

