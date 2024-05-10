import abc

from pandamonium.database import get_db

from pandamonium.entities.data_structures import Entity
from pandamonium.security import max_size_filter


class Branch(Entity, abc.ABC):
    """Classe représentant une branche d'un bambou.
    Une branche est un endroit où les utilisateurs, les pandas, peuvent envoyer des messages au sein d'un bambou.
    Un bambou peut contenir une ou plusieurs branches."""

    def __init__(self,
                 uuid: str | None,
                 name: str | None,
                 bamboo_uuid: str | None):
        """Constructeur de la classe Branch.

        :param uuid: UUID de la branche.
        :param bamboo_uuid: UUID du bamboo dans lequel se trouve la branche.
        :param name: Nom de la branche."""
        super().__init__(
            'branches',
            uuid,
            name=(
                name,
                max_size_filter(50, "Le nom de la branche est trop long (50 caractères max).")
            ),
            bamboo_uuid=bamboo_uuid
        )

    @classmethod
    def instant(cls, name: str, bamboo_uuid: str):
        """Constructeur créant à la fois une nouvelle instance de la classe actuelle tout en la créant en base de
        données.

        :param name: Nom du bamboo.
        :param bamboo_uuid: UUID du bamboo dans lequel se trouve la branche.

        :rtype Branch | None
        :return Instance de la classe Branch si les données entrées sont valides, sinon None."""
        branch = Branch(None, name, bamboo_uuid)

        if branch.valid:
            db = get_db()

            with db.cursor() as curs:
                curs.execute(
                    'INSERT INTO branches(uuid, name, bamboo_uuid) VALUES (%s, %s, %s)',
                    (
                        branch.get_column('uuid').value,
                        name,
                        bamboo_uuid
                    )
                )

                return branch

        return None

    @classmethod
    def fetch_by(cls, uuid: str):
        """Crée une instance de Branch à partir de son UUID. Ne renvoie rien si le bamboo n'est pas trouvé en base de
        données avec l'UUID fourni.

        :param uuid: UUID du bamboo.

        :rtype Bamboo | None
        :return: Instance de la classe Bamboo si le bamboo existe en base de données avec l'UUID fourni, sinon None."""
        db = get_db()

        with db.cursor() as curs:
            curs.execute(
                'SELECT name, bamboo_uuid FROM branches WHERE uuid = %s',
                (uuid,)
            )

            branch = curs.fetchone()

            if branch is None:
                return None

            return cls(
                uuid,
                branch[0],
                branch[1]
            )

    def _update(self, name: str):
        """Met à jour le nom de la branche actuelle.

        :param name: Nouveau nom de la branche."""
        if self.get_column('name') != name:
            bamboo = Branch('', name, None)

            if bamboo.valid:
                self.set_column('name', name)
                db = get_db()

                with db.cursor() as curs:
                    curs.execute(
                        'UPDATE branches SET name = %s WHERE uuid = %s',
                        (name, self.get_column('uuid').value)
                    )
