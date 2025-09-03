from flask import current_app
from backend.main import db
from backend.app.models.user import User

class UserService:
    @staticmethod
    def get_all_users():
        """Returns all users."""
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        """Returns a single user by their ID."""
        return db.session.get(User, user_id)

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
            role=role
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        current_app.logger.info(f"New user created: {new_user.username} (ID: {new_user.id})")
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
            user.set_password(data['password'])

        db.session.commit()
        current_app.logger.info(f"User updated: {user.username} (ID: {user.id})")
        return user, "User updated successfully."

    @staticmethod
    def delete_user(user_id):
        """Deletes a user."""
        user = UserService.get_user_by_id(user_id)
        if not user:
            return False, "User not found."

        username = user.username
        db.session.delete(user)
        db.session.commit()
        current_app.logger.info(f"User deleted: {username} (ID: {user_id})")
        return True, "User deleted successfully."
