from uuid import uuid4

import flask as fk

import mysql.connector as connector
import mysql.connector.abstracts as abstracts

import abc
import typing as tp
import functools

from pandamonium.security import set_security_error


def column_filter(func):
    """Décorateur des fonctions servant de filtres aux colonnes visées.

    :param func: Fonction filtre visée.

    :return Une nouvelle fonction adaptée aux filtres, "enveloppant" celle de base."""
    @functools.wraps(func)
    def wrapper(arg):
        if arg is not None:
            return func(arg)

    return wrapper


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

    def __init__(self, name: str, uuid: str | None, **columns):
        """Constructeur de la classe.

        :param name: Nom de la table.
        :param uuid: UUID (clé primaire) de la première colonne.
        :param columns: Noms des colonnes de la table, associés à leur valeur ou à une paire valeur-contrainte (sous
            forme de tuple)."""
        self.name = name
        self.valid = True
        self.__columns = {'uuid': Column('uuid', uuid if uuid is not None else str(uuid4()), 0)}

        for index, (name, column) in enumerate(columns.items(), 1):
            if isinstance(column, tuple):
                self.__columns[name] = Column(name, column[0], index, column[1])
            else:
                self.__columns[name] = Column(name, column, index)

            if not self.__columns[name].valid:
                self.valid = False
                break

    @property
    def columns(self):
        return self.__columns

    def get_column(self, name: str) -> Column | None:
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

    def update(self, **values):
        """Méthode permettant de mettre à jour certaines valeurs de l'instance de la table actuelle.

        :param values: Paires de clés-valeurs à assigner aux colonnes, où la clé est le nom de la colonne attachée à
            sa valeur."""
        for key, value in values.items():
            if key not in self.__columns:
                raise ValueError(f"La colonne '{key}' n'existe pas dans la table {self.name}.")

        self._update(**values)

    @abc.abstractmethod
    def _update(self, **values):
        """Méthode permettant de mettre à jour certaines valeurs de l'instance de la table actuelle.
        Cette méthode ne doit être utilisée que par les classes filles, qui doivent la redéfinir.

        :param values: Nouvelles valeurs à attribuer aux colonnes de la table."""
        pass


def get_db() -> abstracts.MySQLConnectionAbstract:
    """Crée une instance de Connection représentant la connexion à la base de données. Si la connexion n'a pas encore
    été établie, elle le devient. Sinon, elle est renvoyée telle quelle.

    :rtype: MySQLCursorAbstract
    :return: Instance de la connexion à la base de données."""
    if 'db' not in fk.g:
        fk.g.db = connector.connect(**fk.current_app.config['DATABASE_CREDENTIALS'])
        fk.g.db.autocommit = True

        if fk.g.db.is_connected():
            print('[PANDAMONIUM] Successfully connected to database!')
        else:
            raise RuntimeError('Unable to connect to the database.')

    return fk.g.db


def init_db(set_default_values: bool):
    """Initialise la base de données en se servant du schema.sql fourni. Charge les valeurs par défaut si le paramètre
    set_default_values est défini sur True.

    :param bool set_default_values: Activer/désactiver la création de valeurs par défaut dans la base de données."""
    with fk.current_app.open_resource('schema_dev.sql' if set_default_values else 'schema.sql') as resource:
        sql_statements = filter(
            lambda line: not (line.startswith('--') or line.startswith('/*') or not line.strip()),
            resource.read().decode().split('\n')
        )

    db = get_db()

    with db.cursor() as cursor:
        for sql_statement in sql_statements:
            cursor.execute(sql_statement)


def close_db(e=None):
    """Ferme la connexion à la base de données."""
    db = fk.g.pop('db', None)

    if db is not None:
        db.close()
