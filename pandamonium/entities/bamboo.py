import flask as fk

from datetime import datetime

from pandamonium.database import get_db
from pandamonium.security import date_from_string, date_to_string, uuid_split

from uuid import uuid4


class Bamboo:
    """Classe représentant un serveur unique du réseau social.
    Par "bambou", nous parlons d'un endroit virtuel créé sur notre réseau social pour discuter de façon communautaire.
    Différentes "branches" de discussion peuvent être créése, des rôles et permissions peuvent être
    attribués aux différents membres par le créateur ou les administrateurs du bambou."""

    def __init__(
            self,
            bamboo_uuid: str
    ):
        """Ctor d'un bambou. Prend en paramètre l'uuid du bamboo et récupère dans la base de données
        les différents attributs de l'instance : nom, date de création, uuid du créateur et membres (sous la forme d'une
        liste)."""

        self.uuid = bamboo_uuid

        db = get_db()
        with db.cursor() as curs:
            curs.execute(
                'SELECT name, creation_time, uuid_1, members FROM bamboos WHERE uuid = %s',
                self.uuid
            )
            bamboo = curs.fetchone()
            self.name = bamboo[0]
            self.creation_time = date_from_string(bamboo[1])
            self.creator = bamboo[2]
            self.members = uuid_split(bamboo[3])

    def create(self, name):
        """Méthode qui ajoute un bambou à la base de données et instancie le bambou dans Python."""
        self.uuid = uuid4()
        self.name = name
        self.creator = fk.session['username']
        self.creation_time = date_to_string(datetime.now())

        db = get_db()
        db.cursor().execute(
            'INSERT INTO bamboos(uuid, name, creation_time, creator, members) VALUES (%s, %s, %s, %s, %s)',
            (self.uuid, self.name, self.creation_time, self.creator, self.creator)
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
                'UPDATE servers SET name = %s WHERE id = %s',
                (self.name, self.uuid)
            )
