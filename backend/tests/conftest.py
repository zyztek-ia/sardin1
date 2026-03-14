import pytest
from backend.main import create_app, db as _db

@pytest.fixture(scope='session')
def app():
    """
    Creates a new Flask application for a test session.
    Uses an in-memory SQLite database for testing.
    """
    app = create_app(config_name='testing')

    # Establish an application context before running the tests
    with app.app_context():
        yield app

@pytest.fixture(scope='function')
def client(app):
    """
    Creates a test client for the Flask application.
    """
    return app.test_client()

@pytest.fixture(scope='function')
def session(app):
    """
    Creates a new database session for each test, ensuring a clean slate.
    This fixture handles the application context, table creation, and teardown.
    """
    with app.app_context():
        # The db object is imported from backend.main
        # We need to make sure it's the same one used by the app
        from backend.main import db

        db.create_all()

        yield db.session

        db.session.remove()
        db.drop_all()
