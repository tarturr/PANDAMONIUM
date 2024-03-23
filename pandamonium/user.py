from datetime import datetime
import flask as fk

from pandamonium.db import get_db
from pandamonium.security import check_password, date_from_string, date_to_string, fill_requirements, \
    set_security_error


class User:
    def __init__(self,
                 username: str,
                 email: str,
                 password: str,
                 date_of_birth: datetime,
                 friends: list[str] = [],
                 registered_at: datetime = datetime.now()):
        self.username = username
        self.email = email
        self.password = password
        self.date_of_birth = date_of_birth
        self.friends = friends
        self.logged_at = datetime.now()
        self.registered_at = registered_at

    @classmethod
    def fetch_by(cls, username: str = '', email: str = ''):
        if not (username or email):
            raise ValueError("Aucune valeur n'a été donnée pour récupérer un utilisateur dans la base de données. "
                             "Veuillez indiquer soit le username, soit l'email.")

        db = get_db()

        with db.cursor() as cursor:
            if username:
                cursor.execute('SELECT * FROM users WHERE username = %s', username)
            else:
                cursor.execute('SELECT * FROM users WHERE email = %s', email)

            user = cursor.fetchone()

            return cls(
                user['username'],
                user['email'],
                user['password'],
                date_from_string(user['date_of_birth']),
                user['friends'].split(","),
                date_from_string(user['registered_at']),
            ) if user else None

    @classmethod
    def login(cls, password: str, username: str = '', email: str = ''):
        """Fonction permettant d'instancier un utilisateur depuis la base de données via son username ou son email.
        Si l'utilisateur existe en base de données, son mot de passe est aussi comparé à celui donné en argument.

        Si toutes les conditions sont remplies, la session est clear et la clé 'username' de la session prend la valeur
        du pseudo de l'utilisateur, et une nouvelle instance de User est renvoyée, comportant toutes les données de
        l'utilisateur recherché.

        :param username: nom de l'utilisateur.
        :param email: l'email de l'utilisateur.
        :param password: le mot de passe de l'utilisateur.
        :rtype: User | None
        :return: Une nouvelle instance de User si toutes les conditions sont remplies, sinon None."""
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
        if not self.exists():
            raise ValueError(f"Une requête UPDATE tente d'être exécutée pour l'utilisateur {self.username} qui "
                             f"n'existe pourtant pas dans la base de données. Utilisez la méthode User.exists() "
                             f"afin de vérifier si l'utilisateur existe dans la base de données.")

        if not (username or email or password or date_of_birth or add_friends or remove_friends):
            raise ValueError(f"Une requête UPDATE ne peut pas être exécutée si aucun changement de valeur n'est "
                             f"exécuté dans la base de données.")

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
        if not (User.fetch_by(username=self.username) is None and User.fetch_by(email=self.email) is None):
            return set_security_error(
                f"Un utilisateur avec l'identifiant '{self.username if self.username else self.email}'"
            )

        db = get_db()

        with db.cursor() as cursor:
            cursor.execute(
                'INSERT INTO users ('
                '    username, email, password, date_of_birth, friends, logged_at, registered_at'
                ') VALUES ('
                '    %s, %s, %s, %s, %s, %s, %s)'
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

    def create_session(self):
        fk.session.clear()
        fk.session['username'] = self.username
