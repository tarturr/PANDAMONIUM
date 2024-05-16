import abc
import typing as tp
from uuid import uuid4

from pandamonium.database import get_db
from pandamonium.security import set_security_error, is_valid_uuid


class Column:
    """Classe représentant un 'filtre' spécifique face à une valeur donnée d'une colonne d'une table quelconque."""

    def __init__(self,
                 name: str,
                 value: tp.Any,
                 index: int,
                 constraint: tp.Callable[[tp.Any], str | None] = lambda val: None):
        """Constructeur de la classe.

        :param name: Colonne visée par le filtre.
        :param value: Valeur de la colonne.
        :param index: Index de la colonne par rapport à sa table (débute à 0).
        :param constraint: Filtre (lambda avec single param) qui sera utilisé sur les données à tester."""
        self.name = name
        self.valid = True
        self.index = index
        self.__constraint = constraint

        if self.__value_fits(value):
            self.__value = value
        else:
            self.__value = None
            self.valid = False

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: tp.Any):
        if self.__value_fits(value):
            self.__value = value
        else:
            self.valid = False

    def __value_fits(self, value) -> bool:
        """Méthode vérifiant si la valeur donnée est valide pour la colonne actuelle.
        Si ce n'est pas le cas, l'erreur obtenue est insérée dans le gestionnaire d'erreur de l'application.

        :param value: Valeur à essayer."""
        message = self.__constraint(value)

        if message is not None:
            set_security_error(message)
            return False

        return True


class Entity(abc.ABC):
    """Classe représentant une table de la base de données dont les instances ont besoin d'être différenciée des autres
    par un UUID."""

    def __init__(self, entity_name: str, uuid: str | None, **columns):
        """Constructeur de la classe.

        :param entity_name: Nom de la table.
        :param uuid: UUID (clé primaire) de la première colonne.
        :param columns: Noms des colonnes de la table, associés à leur valeur ou à une paire valeur-contrainte (sous
            forme de tuple)."""
        self.name = entity_name
        self.valid = True
        self.__columns = {'uuid': Column('uuid', uuid if uuid is not None else str(uuid4()), 0)}

        for index, (entity_name, column) in enumerate(columns.items(), 1):
            if isinstance(column, tuple):
                self.__columns[entity_name] = Column(entity_name, column[0], index, column[1])
            else:
                self.__columns[entity_name] = Column(entity_name, column, index)

            if not self.__columns[entity_name].valid:
                self.valid = False
                break

    @property
    def columns(self):
        return self.__columns

    def get_column(self, name: str) -> Column | None:
        """Obtenir une colonne à partir de son nom.

        :param name: Nom de la colonne.

        :return La valeur de la colonne portant le nom donné en argument, ou None si elle n'existe pas."""
        column = self.get_column_instance(name)
        return column.value if column is not None else None

    def get_column_instance(self, name: str) -> Column | None:
        """Obtenir une colonne à partir de son nom.

        :param name: Nom de la colonne.

        :return L'instance de Column portant le nom donné en argument, ou None si elle n'existe pas."""
        return self.__columns[name] if name in self.__columns else None

    def set_column(self, name: str, value):
        """Écrase la valeur de la colonne portant le nom donné en argument.

        :param name: Nom de la colonne.
        :param value: Valeur de la colonne."""
        if name in self.__columns:
            self.__columns[name].value = value

            if not self.__columns[name].valid:
                self.valid = False

    @classmethod
    @abc.abstractmethod
    def instant(cls, *args):
        """Constructeur créant à la fois une nouvelle instance de la classe actuelle tout en la créant en base de
        données."""
        pass

    @classmethod
    @abc.abstractmethod
    def fetch_by(cls, *args):
        """Constructeur créant une instance de la classe actuelle à partir d'informations qui seront récupérées en base
        de données via une requête SQL de type SELECT."""
        pass

    def update(self):
        """Méthode permettant de mettre à jour certaines valeurs de l'instance de la table actuelle."""
        fetched_column = self.fetch_by(self.get_column('uuid'))
        values = {}

        for name, column in fetched_column.columns.items():
            if self.get_column(name) != column.value:
                values[name] = self.get_column(name)

        self._update(values)

    @abc.abstractmethod
    def _update(self, new_values: dict[str, tp.Any]):
        """Méthode permettant de mettre à jour certaines valeurs de l'instance de la table actuelle.
        Cette méthode ne doit être utilisée que par les classes filles, qui doivent la redéfinir.

        :param new_values: Nouvelles valeurs à attribuer aux colonnes de la table."""
        pass


class UUIDList:
    """Classe représentant une chaîne d'UUIDs."""

    def __init__(self, chain: str = ''):
        """Constructeur de la classe UUIDList.

        :param chain: Chaîne d'UUIDs, sous forme de chaîne de caractères.

        :raise ValueError: Si un UUID est mal formé."""
        chain_length = len(chain)

        if chain_length % 36 != 0:
            raise ValueError('The UUID chain is malformed.')

        self.chain = chain
        self.length = chain_length // 36

        for uuid in self:
            if not is_valid_uuid(uuid):
                raise ValueError(f"'{uuid}' is not a valid UUID.")

    def __iter__(self):
        """Transforme la classe actuelle en Iterable."""
        index = 0

        while index < self.length:
            start = self.__get_targeted_index(index)
            end = self.__get_targeted_index(index + 1)

            yield self.chain[start:end]
            index += 1

    def __getitem__(self, index: int):
        """Obtenir l'UUID d'index demandé.

        :param index: Index de l'UUID demandé.

        :raise IndexError: Si l'index est en dehors de la plage de données."""
        target_index = self.__get_targeted_index(index)
        return self.chain[target_index:target_index + 36]

    def __setitem__(self, index: int, uuid: str):
        """Remplacer la valeur de l'UUID à l'index donné avec le nouvel UUID donné.

        :param index: Index de l'UUID remplacé.
        :param uuid: Nouvel UUID.

        :raise IndexError: Si l'index est en dehors de la plage de données.
        :raise ValueError: Si l'UUID donné est mal formé."""
        target_index = self.__get_targeted_index(index)

        if not is_valid_uuid(uuid):
            raise ValueError(f"'{uuid}' is not a valid UUID.")

        self.chain[target_index:target_index + 36] = uuid

    def __len__(self):
        """Renvoie le nombre d'UUIDs se trouvant dans la liste des UUIDs."""
        return self.length

    def __repr__(self):
        """Renvoie une représentation de l'objet actuel sous forme de chaîne de caractères (str)."""
        return (f"<{self.__class__.__module__ + '.' + self.__class__.__name__}: "
                f"chain={self.chain}, length={self.length}>")

    def __str__(self):
        """Renvoie le contenu de la liste d'UUIDs en brut."""
        return self.chain

    def __add__(self, uuid: str):
        """Ajoute un nouvel UUID à la fin de la chaîne.

        :param uuid: Nouvel UUID.

        :raise ValueError: Si l'UUID donné est mal formé."""
        if not is_valid_uuid(uuid):
            raise ValueError(f"'{uuid}' is not a valid UUID.")

        return UUIDList(self.chain + uuid)

    def __radd__(self, uuid: str):
        """Ajoute un nouvel UUID à la fin de la chaîne.

        :param uuid: Nouvel UUID.

        :raise ValueError: Si l'UUID donné est mal formé."""
        return self.__add__(uuid)

    def __delitem__(self, index: int):
        """Supprime l'UUID visé par l'index donné.

        :param index: Index de l'UUID à supprimer.

        :raise IndexError: Si l'index est en dehors de la plage de données."""
        start = self.__get_targeted_index(index)
        end = self.__get_targeted_index(index + 1)
        slice_to_delete = self.chain[start:end]

        self.chain = self.chain.replace(slice_to_delete, '')
        self.length -= 1

    def __get_targeted_index(self, index: int) -> int:
        """Transforme l'index donné en index correspondant à la chaîne d'UUIDs, soit index * 36, si celui-ci existe.
        Sinon, une exception de type IndexError est lancée.

        :param index: Index de l'utilisateur.

        :raise IndexError: Si l'index est en dehors de la plage de données."""
        if not 0 <= index <= self.length:
            raise IndexError(f"The index with value {index} is out of range for length {self.length}!")

        return index * 36

    def append(self, uuid: str):
        """Ajoute un nouvel UUID à la fin de la chaîne.

        :param uuid: Nouvel UUID.

        :raise ValueError: Si l'UUID donné est mal formé."""
        if not is_valid_uuid(uuid):
            raise ValueError(f"'{uuid}' is not a valid UUID.")

        self.chain += uuid
        self.length += 1

    def pop(self, index: int = None):
        """Supprime l'UUID à l'index donné s'il existe, sinon supprime le dernier de la liste des UUIDs.

        :param index: Index de l'UUID à supprimer.

        :raise IndexError: Si l'index est en dehors de la plage de données ou si un pop est effectué sur une liste
            vide."""
        if self.length == 0:
            raise IndexError("You cannot pop an empty list.")

        target_index = index if index is not None else self.length - 1
        elem = self.__getitem__(target_index)

        self.__delitem__(target_index)
        return elem
