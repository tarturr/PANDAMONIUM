import hashlib as hl
import re
from datetime import datetime


def fill_requirements(**identifiers: str) -> None | str:
    """Fonction permettant de vérifier les exigences attendues. Elles sont fixées sur le nom de l'utilisateur, son
    email, son mot de passe ou sa date de naissance.

    :param identifiers: Les paires de valeurs avec en clé 'username', 'email', 'password' ou 'date_of_birth' et la
        valeur associée à chaque clé qui doit être celle entrée par l'utilisateur.
    :return: None si tous les exigences attendues sont remplies, sinon un message d'erreur décrivant l'exigence
        attendue.
    :raise ValueError: Exception levée si et seulement si une clé rentrée est inexistante."""
    for identifier in identifiers:
        match identifier:
            case 'username':
                if re.fullmatch('^[a-zA-Z0-9_-]{3,16}$', identifiers[identifier]) is None:
                    return ("Votre nom d'utilisateur doit faire entre 3 et 16 caractères alphanumériques pouvant "
                            "contenir des traits d'union (-) ou des underscores (_).")
            case 'email':
                if re.fullmatch('^\\w+@\\w.\\w$', identifiers[identifier]) is None:
                    return "Le format de votre adresse email est invalide."
            case 'password':
                if len(identifiers[identifier]) < 6:
                    return "Votre mot de passe doit faire au minimum 6 caractères."
            case 'date_of_birth':
                if int(identifiers[identifier].split('-')[0]) > datetime.today().year - 15:
                    return "Vous êtes trop jeune pour inscrire sur PANDAMONIUM."
            case _:
                raise ValueError(f"L'identificateur {identifier} est inconnu.")


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
