from backend.main import db
from backend.app.models.user import User

class AuthService:
    @staticmethod
    def register_user(username, email, password, role='user'):
        """
        Registers a new user.
        Returns the new user object or None if user already exists.
        """
        if User.query.filter((User.username == username) | (User.email == email)).first():
            # User already exists
            return None

        new_user = User(username=username, email=email, role=role)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return new_user

    @staticmethod
    def authenticate_user(username, password):
        """
        Authenticates a user.
        Returns the user object if authentication is successful, otherwise None.
        """
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None
