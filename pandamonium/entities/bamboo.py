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
            bamboo_uuid: str = None,
            name: str = None
    ):
        """Ctor d'un bambou. Instancie le bambou à partir de la base de données si son uuid est donné en argument.
        Sinon, crée le bambou dans la base de données si le nom est indiqué en argument.
        Paramètres :
            bamboo_uuid STR
                L'UUID du bambou existant à aller chercher dans la base de données et à instancier.
            name STR
                Le nom du bambou à créer et à instancier
        Les différents attributs donnés à l'instance sont : nom, date de création, uuid du créateur et membres (sous la
        forme d'une liste)."""

        if bamboo_uuid is not None:
            self.uuid = bamboo_uuid
            db = get_db()
            with db.cursor() as curs:
                curs.execute(
                    'SELECT name, creation_date, owner_uuid, members FROM bamboos WHERE uuid = %s',
                    [self.uuid]
                )
                bamboo = curs.fetchone()
                self.name = bamboo[0]
                self.creation_time = bamboo[1]
                self.creator = bamboo[2]
                self.members = uuid_split(bamboo[3])

        elif name is not None:
            self.uuid = str(uuid4())
            self.name = name
            self.creator = fk.g.user
            self.creation_time = date_to_string(datetime.now())

            db = get_db()
            db.cursor().execute(
                'INSERT INTO bamboos(uuid, name, creation_date, owner_uuid, members) VALUES (%s, %s, %s, %s, %s)',
                (self.uuid, self.name, self.creation_time, self.creator.get_column('uuid'),
                 self.creator.get_column('uuid'))
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
