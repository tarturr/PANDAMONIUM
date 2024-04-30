import flask as fk

from datetime import datetime, date

from mysql.connector import IntegrityError

from pandamonium.database import get_db
from pandamonium.security import check_password, date_to_string, fill_requirements, set_security_error, hash_password

column_indexes = {
    'username': 0,
    'email': 1,
    'password': 2,
    'date_of_birth': 3,
    'registration_date': 4,
    'last_connection_date': 5,
    'friends': 6
}


class User:
    """
    Classe représentant un utilisateur unique du site web.

    Invariant: l'utilisateur existe toujours en base de données.
    """

    def __init__(self,
                 username: str,
                 email: str,
                 password: str,
                 date_of_birth: date,
                 friends: list[str] = None,
                 registration_date: date = datetime.now().date()):
        """Constructeur de la classe User. Crée automatiquement le nouvel utilisateur en base de données.

        Si une erreur survient, elle doit être gérée en utilisant les fonctions du module security.

        :param username: Nom de l'utilisateur.
        :param email: Adresse mail de l'utilisateur.
        :param password: Mot de passe de l'utilisateur.
        :param date_of_birth: Date de naissance de l'utilisateur, sous forme d'objet datetime.
        :param friends: Liste d'amis de l'utilisateur.
        :param registration_date: Date d'inscription de l'utilisateur, sous forme d'objet datetime."""
        self.username = username
        self.email = email
        self.password = hash_password(password)
        self.date_of_birth = date_of_birth
        self.friends = friends if friends else []
        self.last_connection_date = datetime.now().date()
        self.registration_date = registration_date

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
