from pandamonium.database import get_db
from pandamonium.entities.bamboo import Bamboo

from uuid import uuid4


class Branch:
    """Classe représentant une branche d'un bambou.
    Une branche est un endroit où les utilisateurs, les pandas, peuvent envoyer des messages au sein d'un bambou.
    Un bambou peut contenir une ou plusieurs branches.
    Les attributs d'une branche sont :
    """

    def __init__(
            self,
            parent_bamboo: Bamboo,
            branch_uuid: str = None,
            name: str = None
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
                self.parent_bamboo = parent_bamboo

        elif name is not None:
            self.uuid = str(uuid4())
            self.name = name
            self.parent_bamboo = parent_bamboo

            db = get_db()

            with db.cursor() as curs:
                curs.execute(
                    'INSERT INTO branches(uuid, name, bamboo_uuid) VALUES (%s, %s, %s)',
                    (self.uuid, self.name, self.parent_bamboo.uuid)
                )

    def update(
            self,
            name: str,
    ):
        """Méthode permettant de modifier les informations """

        if self.name != name:
            self.name = name

            db = get_db()
            db.cursor().execute(
                'UPDATE branches SET name = %s WHERE id = %s',
                (self.name, self.uuid)
            )
