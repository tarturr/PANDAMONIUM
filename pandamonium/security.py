import hashlib as hl
import re
import typing

import flask as fk
from datetime import datetime, date


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


def is_valid_uuid(uuid: str) -> bool:
    return re.match('^[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}$', uuid) is not None


def max_size_filter(size: int, message: str) -> typing.Callable[[typing.Any], str | None]:
    """Fonction qui en retourne une autre dont la responsabilité est de retourner message si l'argument qui lui sera
    passé a une longueur supérieure à size, sinon None.

    :param size: Longueur maximale de l'argument testé dans le futur.
    :param message: Message à afficher si la longueur de l'argument dépasse la longueur maximale."""
    from pandamonium.database import column_filter

    @column_filter
    def filter_func(val):
        if len(val) > size:
            return message

    return filter_func
