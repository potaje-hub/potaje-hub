import os
from flask_login import login_user
from flask_login import current_user
from flask import current_app

from app.modules.auth.models import User
from app.modules.auth.repositories import UserRepository
from app.modules.profile.models import UserProfile
from app.modules.profile.repositories import UserProfileRepository
from core.configuration.configuration import uploads_folder_name
from core.services.BaseService import BaseService
from itsdangerous import URLSafeTimedSerializer


class AuthenticationService(BaseService):
    def __init__(self):
        super().__init__(UserRepository())
        self.user_profile_repository = UserProfileRepository()
        self.user_repository = UserRepository()

    def login(self, email, password, remember=True):
        user = self.repository.get_by_email(email)
        # Correct credentials
        if user is not None and user.check_password(password):
            # Email verified
            if user.is_confirmed:
                login_user(user, remember=remember)
                return "success"
            # Email not verified
            else:
                return "email_not_confirmed"
        return "invalid_credentials"

    def is_email_available(self, email: str) -> bool:
        return self.repository.get_by_email(email) is None

    def create_with_profile(self, **kwargs):
        try:
            email = kwargs.pop("email", None)
            password = kwargs.pop("password", None)
            name = kwargs.pop("name", None)
            surname = kwargs.pop("surname", None)
            is_confirmed = kwargs.pop("is_confirmed", None)
            developer = kwargs.pop("developer", False)
            github_user = kwargs.pop("github_user", None)

            if not email:
                raise ValueError("Email is required.")
            if not password:
                raise ValueError("Password is required.")
            if not name:
                raise ValueError("Name is required.")
            if not surname:
                raise ValueError("Surname is required.")
            if developer and not github_user:
                raise ValueError("For a developer a Github User is required.")

            user_data = {
                "email": email,
                "password": password,
                "is_confirmed": is_confirmed
                "developer": developer,
                "github_user": github_user
            }
            profile_data = {
                "name": name,
                "surname": surname,
            }

            user = self.create(commit=False, **user_data)
            profile_data["user_id"] = user.id
            self.user_profile_repository.create(**profile_data)
            self.repository.session.commit()
        except Exception as exc:
            self.repository.session.rollback()
            raise exc
        return user

    def update_profile(self, user_profile_id, form):
        if form.validate():
            updated_instance = self.update(user_profile_id, **form.data)
            return updated_instance, None

        return None, form.errors

    def get_authenticated_user(self) -> User | None:
        if current_user.is_authenticated:
            return current_user
        return None

    def get_authenticated_user_profile(self) -> UserProfile | None:
        if current_user.is_authenticated:
            return current_user.profile
        return None

    def temp_folder_by_user(self, user: User) -> str:
        return os.path.join(uploads_folder_name(), "temp", str(user.id))

    def generate_confirmation_token(self, user_id):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(user_id, salt='email-confirm-salt')

    def confirm_token(self, token, expiration=3600):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            user_id = serializer.loads(token, salt='email-confirm-salt', max_age=expiration)
        except Exception:
            return None
        return user_id

    def update_email_confirmed(self, user_id):
        updated_instance = self.user_repository.update(user_id, is_confirmed=True)
        return updated_instance
