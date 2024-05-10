import abc

from datetime import date, datetime

from pandamonium.database import get_db
from pandamonium.entities.data_structures import Entity, UUIDList
from pandamonium.entities.user import User
from pandamonium.security import max_size_filter


class Bamboo(Entity, abc.ABC):
    """Classe représentant un serveur unique du réseau social.
    Par "bambou", nous parlons d'un endroit virtuel créé sur notre réseau social pour discuter de façon communautaire.
    Différentes "branches" de discussion peuvent être créése, des rôles et permissions peuvent être
    attribués aux différents membres par le créateur ou les administrateurs du bambou."""

    def __init__(self,
                 uuid: str | None,
                 name: str | None,
                 owner_uuid: str | None,
                 members: str | None = None,
                 creation_date: date | None = datetime.now().date()):
        """Constructeur de la classe.

        :param uuid: UUID du bamboo.
        :param name: Nom du bamboo.
        :param owner_uuid: UUID du User étant propriétaire du bamboo.
        :param members: Chaîne d'UUIDs des membres du bamboo.
        :param creation_date: Date de création du bamboo."""
        super().__init__(
            'bamboo',
            uuid,
            name=(
                name,
                max_size_filter(50, "Le nom de votre bambou est trop long.")
            ),
            creation_date=creation_date,
            members=UUIDList(members),
            owner_uuid=User.fetch_by(uuid=owner_uuid)
        )

    @classmethod
    def fetch_by(cls, uuid: str):
        """Crée une instance de Bamboo à partir de son UUID. Ne renvoie rien si le bamboo n'est pas trouvé en base de
        données avec l'UUID fourni.

        :param uuid: UUID du bamboo.

        :rtype Bamboo | None
        :return: Instance de la classe Bamboo si le bamboo existe en base de données avec l'UUID fourni, sinon None."""
        db = get_db()

        with db.cursor() as curs:
            curs.execute(
                'SELECT name, creation_date, members, owner_uuid FROM bamboos WHERE uuid = %s',
                [uuid]
            )

            bamboo = curs.fetchone()

            if bamboo is None:
                return None

            return cls(
                uuid,
                bamboo[0],
                bamboo[1],
                bamboo[2],
                bamboo[3]
            )

    @classmethod
    def instant(cls, name: str, owner_uuid: str):
        """Constructeur créant à la fois une nouvelle instance de la classe actuelle tout en la créant en base de
        données.

        :param name: Nom du bamboo.
        :param owner_uuid: UUID du User étant propriétaire du bamboo.

        :rtype Bamboo | None
        :return Instance de la classe Bamboo si les données entrées sont valides, sinon None."""
        bamboo = Bamboo(None, name, owner_uuid, owner_uuid)

        if bamboo.valid:
            db = get_db()

            with db.cursor() as curs:
                curs.execute(
                    'INSERT INTO bamboos(uuid, name, creation_date, owner_uuid, members) VALUES (%s, %s, %s, %s, %s)',
                    (
                        bamboo.get_column('uuid').value,
                        name,
                        bamboo.get_column('creation_date').value,
                        owner_uuid,
                        owner_uuid
                    )
                )

                return bamboo

        return None

    def _update(self, name: str):
        """Met à jour le nom du bamboo actuel.

        :param name: Nouveau nom du bamboo."""
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
        """Renvoie une liste contenant les UUIDs de toutes les branches faisant partie de l'instance.

        :return Instance de UUIDList contenant l'UUID de chaque branche du bamboo actuel."""
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
