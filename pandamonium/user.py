import flask as fk

from datetime import datetime, date
import re
import abc
from mysql.connector import IntegrityError

from pandamonium.database import get_db, Entity, Column
from pandamonium.security import check_password, date_to_string, fill_requirements, set_security_error, hash_password, \
    uuid_split

column_indexes = {
    'uuid': 0,
    'username': 1,
    'email': 2,
    'password': 3,
    'date_of_birth': 4,
    'friends': 5,
    'relations': 6,
    'registration_date': 7,
    'last_connection_date': 8,
    'pronouns': 9,
    'pb_display_name': 10,
    'pb_bio': 11,
    'pv_display_name': 12,
    'pv_bio': 13,
}


def username_filter(username: str):
    if re.match('^[\\w.-]{3,16}$', username) is None:
        return ("Votre nom d'utilisateur doit faire entre 3 et 16 caractères alphanumériques pouvant contenir des "
                "tirets (-), des points (.) ou des underscores (_).")


def email_filter(email: str):
    if re.fullmatch('^[\\w.-]+@([\\w-]+\\.)+[\\w-]{2,4}$', email) is None:
        return "Le format de votre adresse email est invalide."


def password_filter(password: str):
    pw_len = len(password)

    if pw_len < 6 or pw_len > 64:
        return "Votre mot de passe doit faire entre 6 et 64 caractères."


def date_of_birth_filter(date_of_birth: date):
    if (datetime.now().date() - date_of_birth).days < 15 * 365.25:
        return "Vous êtes trop jeune pour inscrire sur PANDAMONIUM."


class User(Entity, abc.ABC):
    """Classe représentant un utilisateur unique du site web.
    Le constructeur principal de la classe User ne doit jamais être appelé en dehors de la classe elle-même."""

    def __init__(self,
                 unique_id: str,
                 username: str,
                 email: str,
                 password: str,
                 date_of_birth: date,
                 pronouns: str,
                 public_display_name: str,
                 public_bio: str,
                 private_display_name: str,
                 private_bio: str,
                 friends: str,
                 relations: str,
                 registration_date: date = datetime.now().date()):
        """Constructeur de la classe User. Crée automatiquement le nouvel utilisateur en base de données.

        Si une erreur survient, elle doit être gérée en utilisant les fonctions du module security.

        :param unique_id: UUID de l'utilisateur.
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
        super().__init__('user', [
            Column('uuid', unique_id, 0),
            Column('username', username, 1, username_filter),
            Column('email', email, 2, email_filter),
            Column('password', hash_password(password), 3, password_filter),
            Column('date_of_birth', date_of_birth, 4, date_of_birth_filter),
            Column('friends', uuid_split(friends), 5, lambda val: None if len(val) <= 3600 else "Vous avez trop d'amis (100 maximum)."),
            Column('relations', uuid_split(relations), 6, lambda val: None if len(val) <= 3600 else "Vous avez trop de connaissances (100 maximum)."),
            Column('registration_date', registration_date, 7),
            Column('last_connection_date', datetime.now().date(), 8),
            Column('pronouns', pronouns, 9, lambda val: None if len(val) <= 50 else "Vos pronoms sont trop longs."),
            Column('pb_display_name', public_display_name, 10, lambda val: None if len(val) <= 50 else "Votre pseudo public est trop long."),
            Column('pb_bio', public_bio, 11, lambda val: None if len(val) <= 300 else "Votre bio publique est trop longue."),
            Column('pv_display_name', private_display_name, 12, lambda val: None if len(val) <= 50 else "Votre pseudo privé est trop long."),
            Column('pv_bio', private_bio, 13, lambda val: None if len(val) <= 300 else "Votre bio privée est trop longue."),
        ])

    @classmethod
    def instant(cls):
        if not fill_requirements(
                username=self.username,
                email=self.email,
                password=self.password,
                date_of_birth=self.date_of_birth):
            return

        db = get_db()

        with db.cursor() as cursor:
            try:
                cursor.execute(
                    'INSERT INTO users ('
                    '    username, email, password, date_of_birth, friends, last_connection_date, registration_date'
                    ') VALUES ('
                    '    %s, %s, %s, %s, %s, %s, %s'
                    ')',
                    (
                        self.username,
                        self.email,
                        self.password,
                        self.date_of_birth,
                        ','.join(self.friends),
                        self.last_connection_date,
                        self.registration_date
                    )
                )

                self.create_session()
            except IntegrityError:
                set_security_error(
                    f"Un utilisateur avec l'identifiant '{self.username if self.username else self.email}' existe déjà "
                    f"en base de données."
                )

    @classmethod
    def fetch_by(cls, username: str = '', email: str = ''):
        """Crée une instance de User à partir du username ou de l'email renseigné (ignoré si le username est fourni). Ne
        renvoie rien si l'utilisateur n'est pas trouvé en base de données avec l'identifiant fourni.

        :param username: Nom de l'utilisateur.
        :param email: Adresse mail de l'utilisateur.

        :rtype: User | None
        :return: Instance de la classe User si l'utilisateur existe en base de données avec l'identifiant fourni, sinon
            None.

        :raises ValueError: Si ni le username ni l'email ne sont fournis (ou qu'ils sont vides)."""
        is_valid = fill_requirements(username=username)

        if not (is_valid or fill_requirements(email=email)):
            set_security_error(f"L'identifiant {username if not is_valid else email} est invalide.")
            return None

        db = get_db()

        with db.cursor() as cursor:
            if username:
                cursor.execute('SELECT * FROM users WHERE username = %s', [username])
            else:
                cursor.execute('SELECT * FROM users WHERE email = %s', [email])

            user = cursor.fetchone()

            return cls(
                user[column_indexes['username']],
                user[column_indexes['email']],
                user[column_indexes['password']],
                user[column_indexes['date_of_birth']],
                user[column_indexes['friends']].split(","),
                user[column_indexes['registration_date']],
            ) if user else None

    @classmethod
    def login(cls, identifier: str, password: str):
        """Crée une instance de User depuis la base de données via son username ou son email s'il y existe et que son
        mot de passe correspond à celui donné en argument, sinon ne renvoie rien.

        Si une erreur survient, elle doit être gérée en utilisant les fonctions du module security.

        :param identifier: Identifiant de l'utilisateur (username ou email).
        :param password: Mot de passe de l'utilisateur.
        :rtype: User | None
        :return: Instance de User si toutes les conditions sont remplies, sinon None."""

        user = None

        if fill_requirements(password=password):
            if fill_requirements(username=identifier):
                user = User.fetch_by(username=identifier)
            elif fill_requirements(email=identifier):
                user = User.fetch_by(email=identifier)
            else:
                set_security_error(f"L'identifiant {identifier} est invalide.")
                return None
        else:
            set_security_error("Votre mot de passe doit faire entre 6 et 64 caractères.")
            return None

        if user is not None:
            if check_password(password, user.password):
                user.create_session()
                return user
            else:
                set_security_error(f"Mot de passe incorrect pour l'identifiant {identifier}.")
                return None

        set_security_error(f"Aucun utilisateur trouvé avec l'identifiant {identifier}.")
        return None

    def update(self,
               username: str = '',
               email: str = '',
               password: str = '',
               date_of_birth: datetime = None,
               add_friends: list[str] = None,
               remove_friends: list[str] = None):
        """Met à jour les données de l'utilisateur actuel en changeant uniquement les paramètres fournis.
        La date de connexion est automatiquement mise à celle de l'exécution de cette méthode.

        Si une erreur survient, elle doit être gérée en utilisant les fonctions du module security.

        :param username: Nom de l'utilisateur.
        :param email: Adresse mail de l'utilisateur.
        :param password: Mot de passe de l'utilisateur.
        :param date_of_birth: Date de naissance de l'utilisateur, sous forme d'objet datetime.
        :param add_friends: Amis à ajouter à la liste d'amis de l'utilisateur.
        :param remove_friends: Amis à supprimer de la liste d'amis de l'utilisateur.

        :raise ValueError: Si l'utilisateur n'existe pas en base de données ou si aucune donnée n'a été fournie en
            arguments."""
        if not fill_requirements(
                username=self.username,
                email=self.email,
                password=self.password,
                date_of_birth=self.date_of_birth):
            return

        request = 'UPDATE users SET last_connection_date = %s'
        values = [date_to_string(datetime.now())]
        new_username = self.username

        if username:
            request += ', username = %s'
            values.append(username)
            new_username = username

        if email:
            request += ', email = %s'
            values.append(email)
            self.email = email

        if password:
            request += ', password = %s'
            values.append(password)
            self.password = password

        if date_of_birth:
            request += ', date_of_birth = %s'
            values.append(date_to_string(date_of_birth))
            self.date_of_birth = date_of_birth

        if add_friends or remove_friends:
            if add_friends:
                self.friends.extend(add_friends)

            if remove_friends:
                self.friends = filter(lambda friend: friend not in remove_friends, self.friends)

            request += ', friends = %s'
            values.append(','.join(self.friends))

        if len(values) == 1:
            raise ValueError("Une requête UPDATE ne peut pas être exécutée si aucun changement de valeur n'est "
                             "exécuté dans la base de données.")

        request += ' WHERE username = %s'
        values.append(self.username)

        db = get_db()

        with db.cursor() as cursor:
            try:
                cursor.execute(request, values)
                self.username = new_username
            except IntegrityError:
                set_security_error("Un utilisateur avec le nom "
                                   f"'{new_username if self.username != new_username else self.email}' existe déjà.")

    def create_session(self):
        """Initialise une nouvelle session à partir de l'utilisateur actuel."""
        fk.session.clear()
        fk.session['username'] = self.username
