import hashlib as hl
import re
import flask as fk
from datetime import datetime, date


def fill_requirements(**identifiers) -> bool:
    """Fonction permettant de vérifier les exigences attendues. Elles sont fixées sur le nom de l'utilisateur, son
    email, son mot de passe ou sa date de naissance.

    :param identifiers: Les paires de valeurs avec en clé 'username', 'email', 'password' ou 'date_of_birth' et la
        valeur associée à chaque clé qui doit être celle entrée par l'utilisateur.
    :return: True si tous les exigences attendues sont remplies, sinon False.
    :raise ValueError: Exception levée si et seulement si une clé rentrée est inexistante."""
    for identifier in identifiers:
        value = identifiers[identifier]

        match identifier:
            case 'username':
                if re.match('^[\\w.-]{3,16}$', value) is None:
                    set_security_error("Votre nom d'utilisateur doit faire entre 3 et 16 caractères alphanumériques "
                                       "pouvant contenir des tirets (-), des points (.) ou des underscores (_).")
                    return False
            case 'email':
                if re.fullmatch('^[\\w.-]+@([\\w-]+\\.)+[\\w-]{2,4}$', value) is None:
                    set_security_error("Le format de votre adresse email est invalide.")
                    return False
            case 'password':
                pw_len = len(value)

                if pw_len < 6 or pw_len > 64:
                    set_security_error("Votre mot de passe doit faire entre 6 et 64 caractères.")
                    return False
            case 'date_of_birth':
                if (datetime.now().date() - value).days < 15 * 365.25:
                    set_security_error("Vous êtes trop jeune pour inscrire sur PANDAMONIUM.")
                    return False
            case _:
                raise ValueError(f"L'identificateur {identifier} est inconnu.")

    return True


def set_security_error(message: str):
    """Crée un message d'erreur inséré dans le cache d'erreur du module security.

    :param message: le message d'erreur à destination de l'utilisateur."""
    fk.g.security_error = message


def get_security_error() -> str | None:
    """Permet d'obtenir la dernière erreur dans le cache d'erreur du module security s'il n'est pas vide, puis vide ce
    cache.

    :rtype: str | None
    :return: la dernière erreur dans le cache d'erreur du module security s'il n'est pas vide, sinon None."""
    return fk.g.pop('security_error', None)


def is_security_error() -> bool:
    """Vérifie si une erreur de sécurité a été lancée pendant l'exécution de l'application.

    :rtype: bool
    :return: True si une erreur est présente, False sinon."""
    return 'security_error' in fk.g


def hash_password(password: str) -> str:
    """Fonction qui transforme un mot de passe sous le hash utilisant la méthode SHA256.

    :param password: le mot de passe à hasher.
    :rtype str
    :return: le mot de passe hashé."""
    return hl.sha256(password.encode()).hexdigest()


def check_password(password: str, hashed_password: str) -> bool:
    """Fonction qui vérifie que le mot de passe donné soit égal au mot de passe déjà hashé.

    :param password: le mot de passe à vérifier.
    :param hashed_password: le mot de passe hashé.
    :rtype bool
    :return: True si les mots de passe correspondent, False sinon."""
    return hash_password(password) == hashed_password


def date_from_string(str_date: str) -> date:
    """Fonction convertissant une date sous forme de chaîne de caractères au format YYYY-MM-DD vers un objet datetime.

    :param str_date: La date au format YYYY-MM-DD.
    :rtype datetime
    :return: Une nouvelle instance de datetime correspondant à la date donnée en argument."""
    return datetime.strptime(str_date, '%Y-%m-%d').date()


def date_to_string(date_instance: date) -> str:
    """Fonction convertissant un objet datetime vers une chaîne de caractères au format YYYY-MM-DD.

    :param date_instance: L'objet datetime.
    :rtype str
    :return: Une chaîne de caractères au format YYYY-MM-DD correspondant à la date donnée en argument."""
    return datetime.strftime(date_instance, '%Y-%m-%d')


def uuid_split(uuid_chain: str) -> list[str]:
    """Fonction permettant d'obtenir une liste d'UUIDs à partir d'une chaîne de caractères donnée.

    :param uuid_chain: Chaîne d'UUIDs à séparer.
    :return: Une liste d'UUIDs.
    :raise ValueError: Si la chaîne n'est pas un multiple de 16, signifiant que la chaîne est mal formée."""
    chain_len = len(uuid_chain)

    if chain_len % 16 != 0:
        raise ValueError('The UUID list is malformed.')

    return [uuid_chain[i:i + 16] for i in range(0, chain_len, 16)]
