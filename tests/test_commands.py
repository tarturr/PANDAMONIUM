from flask.testing import FlaskCliRunner


def test_reset_db(runner: FlaskCliRunner):
    """Fonction de test de la commande 'reset-db [--blank]'.

    :param FlaskCliRunner runner: L'instance d'une classe FlaskCliRunner permettant de tester la commande."""
    result = runner.invoke(args=['reset-db', '--dev'])
    assert 'avec' in result.output

    result = runner.invoke(args=['reset-db'])
    assert 'sans' in result.output
