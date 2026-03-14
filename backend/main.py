import logging
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO
from celery import Celery
from backend.config import config_by_name, Config

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

    # Configure logging
    if not app.debug and not app.testing:
        # In production mode, add a handler to send logs to stdout
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        )
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('SARDIN-AI startup')

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
        from backend.app.routes.auth import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/api/auth')

        from backend.app.routes.vessel import vessel_bp
        app.register_blueprint(vessel_bp, url_prefix='/api/vessels')

        from backend.app.routes.users import user_bp
        app.register_blueprint(user_bp, url_prefix='/api/users')

        # A simple health check endpoint
        @app.route('/health')
        def health_check():
            return "OK", 200

        @app.before_request
        def log_request_info():
            app.logger.debug('Request Headers: %s', request.headers)
            app.logger.debug('Request Body: %s', request.get_data())
            app.logger.info(f"Incoming request: {request.method} {request.path}")

        @app.errorhandler(Exception)
        def log_unhandled_exception(e):
            app.logger.error(f"Unhandled Exception: {e}", exc_info=True)
            # You can also return a generic error response to the client
            return {"message": "An unexpected error occurred."}, 500

    return app
