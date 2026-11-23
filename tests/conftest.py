import pytest
from app import app as flask_app
from models import init_db


@pytest.fixture
def client(tmp_path):
    flask_app.config['TESTING'] = True
    flask_app.config['DATABASE'] = str(tmp_path / 'test.db')

    with flask_app.app_context():
        init_db(flask_app)

    with flask_app.test_client() as client:
        yield client
