import flask as fk

from datetime import datetime

from mysql.connector import IntegrityError

from pandamonium.db import get_db
from pandamonium.security import check_password, date_from_string, date_to_string, fill_requirements, \
    set_security_error


column_indexes = {
    'username': 0,
    'email': 1,
    'password': 2,
    'date_of_birth': 3,
    'registered_at': 4,
    'logged_at': 5,
    'friends': 6
}


class User:
    """Classe représentant un utilisateur unique du site web."""

    def __init__(self,
                 username: str,
                 email: str,
                 password: str,
                 date_of_birth: datetime,
                 friends: list[str] = [],
                 registered_at: datetime = datetime.now()):
        """Constructeur de la classe User.

        :param username: Nom de l'utilisateur.
        :param email: Adresse mail de l'utilisateur.
        :param password: Mot de passe de l'utilisateur.
        :param date_of_birth: Date de naissance de l'utilisateur, sous forme d'objet datetime.
        :param friends: Liste d'amis de l'utilisateur.
        :param registered_at: Date d'inscription de l'utilisateur, sous forme d'objet datetime."""
        self.username = username
        self.email = email
        self.password = password
        self.date_of_birth = date_of_birth
        self.friends = friends
        self.logged_at = datetime.now()
        self.registered_at = registered_at

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
        if not (username or email):
            raise ValueError("Aucune valeur n'a été donnée pour récupérer un utilisateur dans la base de données. "
                             "Veuillez indiquer soit le username, soit l'email.")

        if not (fill_requirements(username=username) or fill_requirements(email=email)):
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
                user[column_indexes['registered_at']],
            ) if user else None

    @classmethod
    def login(cls, password: str, username: str = '', email: str = ''):
        """Crée une instance de User depuis la base de données via son username ou son email s'il y existe et que son
        mot de passe correspond à celui donné en argument, sinon ne renvoie rien.

        Si une erreur survient, elle doit être gérée en utilisant les fonctions du module security.

        :param username: Nom de l'utilisateur.
        :param email: Email de l'utilisateur.
        :param password: Mot de passe de l'utilisateur.
        :rtype: User | None
        :return: Instance de User si toutes les conditions sont remplies, sinon None."""
        identifier = username if not username else email

        if not (fill_requirements(username=username, password=password)
                or fill_requirements(email=email, password=password)):
            return None

        user = User.fetch_by(username=username, email=email)

        if user is not None:
            if check_password(password, user.password):
                user.create_session()
                return user
            else:
                set_security_error(f"Mot de passe incorrect pour l'identifiant {identifier}.")

        set_security_error(f"Aucun utilisateur trouvé avec l'identifiant {identifier}.")
        return None

    def exists(self) -> bool:
        """Vérifie si l'utilisateur courant existe en base de données ou non.

        :rtype: bool
        :return: True si l'utilisateur existe en base de données, sinon False."""
        db = get_db()

        with db.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM users WHERE username = %s OR email = %s',
                (self.username, self.email)
            )

            return cursor.fetchone() is not None

    def update(self,
               username: str = '',
               email: str = '',
               password: str = '',
               date_of_birth: datetime = None,
               add_friends: list[str] = [],
               remove_friends: list[str] = []):
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
        if not self.exists():
            raise ValueError(f"Une requête UPDATE tente d'être exécutée pour l'utilisateur {self.username} qui "
                             f"n'existe pourtant pas dans la base de données. Utilisez la méthode User.exists() "
                             f"afin de vérifier si l'utilisateur existe dans la base de données.")

        if not (username or email or password or date_of_birth or add_friends or remove_friends):
            raise ValueError(f"Une requête UPDATE ne peut pas être exécutée si aucun changement de valeur n'est "
                             f"exécuté dans la base de données.")

        if not fill_requirements(
                username=self.username,
                email=self.email,
                password=self.password,
                date_of_birth=self.date_of_birth):
            return

        request = 'UPDATE users SET logged_at = %s'
        values = [date_to_string(datetime.now())]
        new_username = self.username

        db = get_db()

        with db.cursor() as cursor:
            if username:
                if User.fetch_by(username=username) is not None:
                    return set_security_error(f"L'utilisateur portant le nom de {username} existe déjà.")

                request += f', username = %s'
                values.append(username)
                new_username = username

            if email:
                if User.fetch_by(email=email) is not None:
                    return set_security_error(f"Un utilisateur utilisant l'email {email} existe déjà.")

                request += f', email = %s'
                values.append(email)
                self.email = email

            if password:
                request += f', password = %s'
                values.append(password)
                self.password = password

            if date_of_birth:
                request += f', date_of_birth = %s'
                values.append(date_to_string(date_of_birth))
                self.date_of_birth = date_of_birth

            if add_friends or remove_friends:
                if add_friends:
                    self.friends.extend(add_friends)

                if remove_friends:
                    self.friends = filter(lambda friend: friend not in remove_friends, self.friends)

                request += f', friends = %s'
                values.append(','.join(self.friends))

            request += ' WHERE username = %s'
            values.append(self.username)

            cursor.execute(request, values)
            self.username = new_username

    def create(self):
        """Crée l'utilisateur actuel en base de données.

        Si une erreur survient, elle doit être gérée en utilisant les fonctions du module security."""
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
                    '    username, email, password, date_of_birth, friends, logged_at, registered_at'
                    ') VALUES ('
                    '    %s, %s, %s, %s, %s, %s, %s'
                    ')',
                    (
                        self.username,
                        self.email,
                        self.password,
                        self.date_of_birth,
                        ','.join(self.friends),
                        self.logged_at,
                        self.registered_at
                    )
                )

                self.create_session()
            except IntegrityError:
                set_security_error(
                    f"Un utilisateur avec l'identifiant '{self.username if self.username else self.email}' existe déjà "
                    f"en base de données."
                )

    def create_session(self):
        """Initialise une nouvelle session à partir de l'utilisateur actuel."""
        fk.session.clear()
        fk.session['username'] = self.username
