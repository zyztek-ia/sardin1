from backend.app import db
from backend.app.models.user import User
from werkzeug.security import generate_password_hash

class UserService:
    @staticmethod
    def get_all_users():
        """Returns all users."""
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        """Returns a single user by their ID."""
        return User.query.get(user_id)

    @staticmethod
    def create_user(data):
        """
        Creates a new user.
        'data' is a dictionary containing user information.
        """
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')

        if not all([username, email, password]):
            return None, "Username, email, and password are required."

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return None, "A user with this username or email already exists."

        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        return new_user, "User created successfully."

    @staticmethod
    def update_user(user_id, data):
        """Updates an existing user."""
        user = UserService.get_user_by_id(user_id)
        if not user:
            return None, "User not found."

        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.role = data.get('role', user.role)

        if 'password' in data and data['password']:
            user.password_hash = generate_password_hash(data['password'])

        db.session.commit()
        return user, "User updated successfully."

    @staticmethod
    def delete_user(user_id):
        """Deletes a user."""
        user = UserService.get_user_by_id(user_id)
        if not user:
            return False, "User not found."

        db.session.delete(user)
        db.session.commit()
        return True, "User deleted successfully."
