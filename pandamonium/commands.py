import click
from flask import Flask

import pandamonium.db as db


def register_commands(app: Flask):
    """Enregistre toutes les commandes disponibles dans le CLI Flask de l'application PANDAMONIUM.

    :param Flask app: L'instance de l'application Flask."""
    @app.cli.command('reset-db')
    @click.option('-d', '--dev', is_flag=True, default=False, help='Générer la base de données en mode dev.')
    def reset_db(dev: bool):
        """Commande Flask qui réinitialise les données de la base de données. Insère les valeurs par défaut si le
        paramètre is_blank est True.

        :param bool dev: définit si des valeurs par défaut doivent être insérées lors de la réinitialisation de la
        base de données."""
        db.init_db(set_default_values=dev)

        if dev:
            click.echo('[PANDEMONIUM] Reset de la base de données effectué avec les valeurs par défaut.')
        else:
            click.echo('[PANDEMONIUM] Reset de la base de données effectué sans valeurs par défaut.')
