import flask as fk

import click

from pandamonium.database import close_db, init_db


def register_commands(app: fk.Flask):
    """Enregistre toutes les commandes disponibles dans le CLI Flask de l'application PANDAMONIUM.

    :param fk.Flask app: L'instance de l'application Flask."""
    app.cli.add_command(reset_db)


@click.command('reset-db')
@click.option('-d', '--dev', is_flag=True, default=False, help='Générer la base de données en mode dev.')
def reset_db(dev: bool):
    """Commande Flask qui réinitialise les données de la base de données. Insère les valeurs par défaut si le
    paramètre is_blank est True.

    :param bool dev: définit si des valeurs par défaut doivent être insérées lors de la réinitialisation de la
    base de données."""
    init_db(set_default_values=dev)

    if dev:
        click.echo('[PANDAMONIUM] Reset de la base de données effectué avec les valeurs par défaut.')
    else:
        click.echo('[PANDAMONIUM] Reset de la base de données effectué sans valeurs par défaut.')

    close_db()
