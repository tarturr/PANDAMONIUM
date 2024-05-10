import flask as fk

from datetime import datetime, date
import re
import abc
from mysql.connector import IntegrityError

from pandamonium.database import get_db, column_filter
from pandamonium.entities.bamboo import Bamboo
from pandamonium.entities.data_structures import Entity, UUIDList
from pandamonium.security import check_password, date_to_string, set_security_error, hash_password, \
    max_size_filter


@column_filter
def username_filter(username: str) -> str | None:
    """Filtre pour une donnée de type nom d'utilisateur.

    :param username: Nom d'utilisateur entré par l'utilisateur.

    :return: None si le nom d'utilisateur a un schéma correct, sinon un message d'erreur."""
    if re.match('^[\\w.-]{3,16}$', username) is None:
        return ("Votre nom d'utilisateur doit faire entre 3 et 16 caractères alphanumériques pouvant contenir des "
                "tirets (-), des points (.) ou des underscores (_).")


@column_filter
def email_filter(email: str) -> str | None:
    """Filtre pour une donnée de type email.

    :param email: Email entré par l'utilisateur.

    :return: None si l'email a un schéma correct, sinon un message d'erreur."""
    if re.fullmatch('^[\\w.-]+@([\\w-]+\\.)+[\\w-]{2,4}$', email) is None:
        return "Le format de votre adresse email est invalide."


@column_filter
def password_filter(password: str) -> str | None:
    """Filtre pour une donnée de type mot de passe.

    :param password: Mot de passe entré par l'utilisateur.

    :return: None si le mot de passe a un schéma correct, sinon un message d'erreur."""
    pw_len = len(password)

    if pw_len < 6 or pw_len > 64:
        return "Votre mot de passe doit faire entre 6 et 64 caractères."


@column_filter
def date_of_birth_filter(date_of_birth: date) -> str | None:
    """Filtre pour une donnée de type date de naissance.

    :param date_of_birth: Date de naissance entrée par l'utilisateur.

    :return: None si la date de naissance a au moins 15 ans d'écart avec la date actuelle, sinon un message d'erreur."""
    if (datetime.now().date() - date_of_birth).days < 15 * 365.25:
        return "Vous êtes trop jeune pour inscrire sur PANDAMONIUM."


class User(Entity, abc.ABC):
    """Classe représentant un utilisateur unique du site web."""

    def __init__(self,
                 uuid: str | None,
                 username: str | None,
                 email: str | None,
                 password: str | None,
                 date_of_birth: date | None,
                 pronouns: str | None,
                 public_display_name: str | None,
                 private_display_name: str | None,
                 public_bio: str = None,
                 private_bio: str = None,
                 friends: str = None,
                 relations: str = None,
                 bamboos: str = None,
                 registration_date: date = datetime.now().date()):
        """Constructeur de la classe User.

        :param uuid: UUID de l'utilisateur.
        :param username: Nom de l'utilisateur.
        :param email: Adresse mail de l'utilisateur.
        :param password: Mot de passe de l'utilisateur.
        :param date_of_birth: Date de naissance de l'utilisateur, sous forme d'objet date.
        :param pronouns: Pronoms de l'utilisateur.
        :param public_display_name: Nom de l'utilisateur en visibilité publique.
        :param public_bio: Bio de l'utilisateur en visibilité publique.
        :param private_display_name: Nom de l'utilisateur en visibilité privée.
        :param private_bio: Bio de l'utilisateur en visibilité privée.
        :param friends: Liste d'amis de l'utilisateur.
        :param relations: Relations professionnelles de l'utilisateur.
        :param registration_date: Date d'inscription de l'utilisateur, sous forme d'objet date."""
        super().__init__(
            'user',
            uuid,
            username=(username, username_filter),
            email=(email, email_filter),
            password=(password, password_filter),
            date_of_birth=(date_of_birth, date_of_birth_filter),
            friends=(
                UUIDList(friends) if friends is not None else [],
                max_size_filter(3600, "Vous avez trop d'amis (100 maximum).")
            ),
            relations=(
                UUIDList(relations) if relations is not None else [],
                max_size_filter(3600, "Vous avez trop de connaissances (100 maximum).")
            ),
            bamboos=(
                [Bamboo.fetch_by(bamboo_uuid) for bamboo_uuid in UUIDList(bamboos)] if bamboos is not None else [],
                max_size_filter(3600, "Vous avez trop de bambous (100 maximum).")
            ),
            registration_date=registration_date,
            last_connection_date=datetime.now().date(),
            pronouns=(
                pronouns,
                max_size_filter(50, "Vos pronoms sont trop longs.")
            ),
            public_display_name=(
                public_display_name,
                max_size_filter(50, "Votre pseudo public est trop long.")
            ),
            public_bio=(
                public_bio,
                max_size_filter(300, "Votre bio publique est trop longue.")
            ),
            private_display_name=(
                private_display_name,
                max_size_filter(50, "Votre pseudo privé est trop long.")
            ),
            private_bio=(
                private_bio,
                max_size_filter(300, "Votre bio privée est trop longue.")
            )
        )

    @classmethod
    def instant(cls,
                username: str,
                email: str,
                password: str,
                date_of_birth: date,
                pronouns: str,
                public_display_name: str,
                private_display_name: str):
        """Constructeur créant à la fois une nouvelle instance de la classe actuelle tout en la créant en base de
        données.

        :param username: Nom de l'utilisateur.
        :param email: Adresse mail de l'utilisateur.
        :param password: Mot de passe de l'utilisateur.
        :param date_of_birth: Date de naissance de l'utilisateur, sous forme d'objet date.
        :param pronouns: Pronoms de l'utilisateur.
        :param public_display_name: Nom de l'utilisateur en visibilité publique.
        :param private_display_name: Nom de l'utilisateur en visibilité privée.

        :rtype User | None
        :return Instance de la classe User si les données entrées sont valides, sinon None."""
        db = get_db()

        user = User(
            None,
            username,
            email,
            hash_password(password),
            date_of_birth,
            pronouns,
            public_display_name,
            private_display_name
        )

        if user.valid:
            with db.cursor() as cursor:
                try:
                    cursor.execute(
                        'INSERT INTO users ('
                        '    uuid, username, email, password, date_of_birth, registration_date, '
                        '    last_connection_date, pronouns, public_display_name, private_display_name'
                        ') VALUES ('
                        '    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s'
                        ')',
                        (
                            user.get_column('uuid').value,
                            username,
                            email,
                            password,
                            date_of_birth,
                            user.get_column('registration_date').value,
                            user.get_column('last_connection_date').value,
                            pronouns,
                            public_display_name,
                            private_display_name
                        )
                    )

                    user.create_session()
                    return user
                except IntegrityError:
                    set_security_error(
                        f"Une erreur est survenue lors de la création de votre compte. Veuillez utiliser un autre nom "
                        f"d'utilisateur ou un autre email."
                    )

        return None

    @classmethod
    def fetch_by(cls, uuid: str = '', username: str = '', email: str = ''):
        """Crée une instance de User à partir du username ou de l'email renseigné (ignoré si le username est fourni). Ne
        renvoie rien si l'utilisateur n'est pas trouvé en base de données avec l'identifiant fourni.

        :param uuid: UUID de l'utilisateur.
        :param username: Nom de l'utilisateur.
        :param email: Adresse mail de l'utilisateur.

        :rtype: User | None
        :return: Instance de la classe User si l'utilisateur existe en base de données avec l'identifiant fourni, sinon
            None.

        :raises ValueError: Si ni le username ni l'email ne sont fournis (ou qu'ils sont vides)."""
        request, param = None, None

        if uuid:
            request = 'SELECT * FROM users WHERE uuid = %s'
            param = uuid
        elif username:
            request = 'SELECT * FROM users WHERE username = %s'
            param = username
        elif email:
            request = 'SELECT * FROM users WHERE email = %s'
            param = email
        
        if request is None:
            raise ValueError("Tentative de récupérer un utilisateur dans la base de données sans fournir de valeur sur "
                             "laquelle s'appuyer.")

        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute(request, [param])
            fetched_user = cursor.fetchone()

        return cls(
            fetched_user['uuid'],
            fetched_user['username'],
            fetched_user['email'],
            fetched_user['password'],
            fetched_user['date_of_birth'],
            fetched_user['pronouns'],
            fetched_user['public_display_name'],
            fetched_user['private_display_name'],
            fetched_user['public_bio'],
            fetched_user['private_bio'],
            fetched_user['friends'],
            fetched_user['relations'],
            fetched_user['bamboos'],
            fetched_user['registration_date'],
        ) if fetched_user is not None else None

    @classmethod
    def login(cls, identifier: str, password: str):
        """Crée une instance de User depuis la base de données via son username ou son email s'il y existe et que son
        mot de passe correspond à celui donné en argument, sinon ne renvoie rien.

        Si une erreur survient, elle doit être gérée en utilisant les fonctions du module security.

        :param identifier: Identifiant de l'utilisateur (username ou email).
        :param password: Mot de passe de l'utilisateur.

        :rtype: User | None
        :return: Instance de User si toutes les conditions sont remplies, sinon None."""
        user = User('', None, None, password, None, None, None, None)

        if not user.valid:
            return None

        user.set_column('username', identifier)

        if user.valid:
            user = User.fetch_by(username=identifier)
        else:
            user.set_column('email', identifier)

            if user.valid:
                user = User.fetch_by(email=identifier)
            else:
                set_security_error(f"L'identifiant {identifier} est invalide.")
                return None

        if user is not None:
            if check_password(password, user.get_column('password').value):
                user.create_session()
                return user
            else:
                set_security_error(f"Mot de passe incorrect pour l'identifiant {identifier}.")
                return None

        set_security_error(f"Aucun utilisateur trouvé avec l'identifiant {identifier}.")
        return None

    def _update(self, new_data: 'User'):
        """Met à jour les données de l'utilisateur actuel en prenant en compte seulement les colonnes dont les valeurs
        sont non None.

        Si une erreur survient, elle doit être gérée en utilisant les fonctions du module security.

        :param new_data: Données à mettre à jour dans l'utilisateur actuel. Les colonnes ayant pour valeur None seront
            ignorées. Attention : toutes les autres écraseront les valeurs des anciennes colonnes.

        :raise ValueError: Si l'utilisateur n'existe pas en base de données ou si aucune donnée n'a été fournie en
            arguments."""
        request = 'UPDATE users SET last_connection_date = %s'
        values = [date_to_string(datetime.now())]

        for column in new_data.columns.values():
            if column.value is not None:
                request += f', {column.name} = %s'

                match column.value:
                    case date():
                        values.append(date_to_string(column.value))
                    case list():
                        values.append(''.join(column.value))
                    case _:
                        values.append(column.value)

        if len(values) == 1:
            raise ValueError("Une requête UPDATE ne peut pas être exécutée si aucun changement de valeur n'est "
                             "exécuté dans la base de données.")

        request += ' WHERE uuid = %s'
        values.append(self.get_column('uuid').value)

        db = get_db()

        with db.cursor() as cursor:
            try:
                cursor.execute(request, values)

                for column in new_data.columns.values():
                    if column.value is not None:
                        self.set_column(column.name, column.value)
            except IntegrityError:
                set_security_error("Une erreur est survenue lors de la mise à jour de vos données. Le nom "
                                   "d'utilisateur ou l'email est peut-être déjà pris par un autre compte.")

    def create_session(self):
        """Initialise une nouvelle session à partir de l'utilisateur actuel."""
        fk.session.clear()
        fk.session['username'] = self.get_column('username').value
