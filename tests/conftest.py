import pytest

from pandamonium import create_app


@pytest.fixture()
def app():
    """Lance l'application en mode test."""
    app = create_app()
    app.config.update({"TESTING": True})

    yield app


@pytest.fixture()
def runner(app):
    yield app.test_cli_runner()
