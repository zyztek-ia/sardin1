from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO
from celery import Celery
from backend.config import config_by_name

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
socketio = SocketIO()

# Initialize Celery
# The broker and backend are configured in the Flask app config
celery_app = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)


def create_app(config_name='default'):
    """
    Application factory function.
    """
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}}) # Example CORS config
    socketio.init_app(app)

    # Update celery config from flask app config
    celery_app.conf.update(app.config)

    # Register blueprints
    with app.app_context():
        # Import and register blueprints here
        from .routes.auth import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/api/auth')

        from .routes.vessel import vessel_bp
        app.register_blueprint(vessel_bp, url_prefix='/api/vessels')

        from .routes.users import user_bp
        app.register_blueprint(user_bp, url_prefix='/api/users')

        # A simple health check endpoint
        @app.route('/health')
        def health_check():
            return "OK", 200

    return app
