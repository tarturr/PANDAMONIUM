import abc

from datetime import date, datetime

from pandamonium.database import get_db
from pandamonium.entities.data_structures import Entity, UUIDList
from pandamonium.entities.user import User
from pandamonium.security import date_to_string, max_size_filter

from uuid import uuid4


class Bamboo(Entity, abc.ABC):
    """Classe représentant un serveur unique du réseau social.
    Par "bambou", nous parlons d'un endroit virtuel créé sur notre réseau social pour discuter de façon communautaire.
    Différentes "branches" de discussion peuvent être créése, des rôles et permissions peuvent être
    attribués aux différents membres par le créateur ou les administrateurs du bambou."""

    def __init__(self,
                 uuid: str | None,
                 name: str | None,
                 owner_uuid: User | None,
                 members: UUIDList | None = None,
                 creation_date: date | None = datetime.now().date()):
        """Ctor d'un bambou. Instancie le bambou à partir de la base de données si son uuid est donné en argument.
        Sinon, crée le bambou dans la base de données si le nom est indiqué en argument.
        Paramètres :
            bamboo_uuid STR
                L'UUID du bambou existant à aller chercher dans la base de données et à instancier.
            name STR
                Le nom du bambou à créer et à instancier
        Les différents attributs donnés à l'instance sont : nom, date de création, uuid du créateur et membres (sous la
        forme d'une liste)."""
        super().__init__(
            'bamboo',
            uuid,
            name=(
                name,
                max_size_filter(50, "Le nom de votre bambou est trop long.")
            ),
            creation_date=creation_date,
            members=members,
            owner_uuid=owner_uuid
        )

    @classmethod
    def fetch_by(cls, uuid: str):
        db = get_db()

        with db.cursor() as curs:
            curs.execute(
                'SELECT name, creation_date, members, owner_uuid FROM bamboos WHERE uuid = %s',
                [uuid]
            )

            bamboo = curs.fetchone()

            return cls(
                uuid,
                bamboo[0],
                bamboo[1],
                UUIDList(bamboo[2]),
                User.fetch_by(username=bamboo[3])
            )

    @classmethod
    def instant(cls, name: str, owner: User):
        uuid = str(uuid4())
        owner_uuid = owner.get_column('uuid').value
        creation_date = date_to_string(datetime.now())

        db = get_db()

        with db.cursor() as curs:
            curs.execute(
                'INSERT INTO bamboos(uuid, name, creation_date, owner_uuid, members) VALUES (%s, %s, %s, %s, %s)',
                (uuid, name, creation_date, owner_uuid, UUIDList(owner_uuid).chain)
            )

    def _update(self, name: str):
        """Méthode permettant de modifier les informations """
        if self.get_column('name') != name:
            bamboo = Bamboo('', name, None)

            if bamboo.valid:
                self.set_column('name', name)
                db = get_db()

                with db.cursor() as curs:
                    curs.execute(
                        'UPDATE bamboos SET name = %s WHERE id = %s',
                        (name, self.get_column('uuid').value)
                    )

    def get_branches(self):
        """Méthode qui renvoie une liste contenant les uuid de toutes les branches faisant partie de l'instance."""
        from pandamonium.entities.branch import Branch

        db = get_db()

        with db.cursor() as curs:
            curs.execute(
                'SELECT uuid FROM branches WHERE bamboo_uuid = %s',
                (self.get_column('uuid').value,)
            )

            branch_uuids = UUIDList()

            for result in curs.fetchall():
                branch_uuids += result

            return branch_uuids
