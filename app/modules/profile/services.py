from app.modules.profile.repositories import UserProfileRepository
from app.modules.auth.repositories import UserRepository
from core.services.BaseService import BaseService
import re
from flask_login import current_user


class UserProfileService(BaseService):
    def __init__(self):
        super().__init__(UserProfileRepository())
        self.user_repo = UserRepository()

    def update_profile(self, user_profile_id, form, **kwargs):

        try:
            name = form.name.data
            surname = form.surname.data
            affiliation = form.affiliation.data
            orcid = form.orcid.data
            developer = form.developer.data
            github_user = form.github_user.data

            if not name:
                raise ValueError("Name is required.")
            if len(name) > 100:
                raise ValueError("Name is too long.")
            if not surname:
                raise ValueError("Surname is required.")
            if len(surname) > 100:
                raise ValueError("Surname is too long.")
            if len(orcid) != 19 and len(orcid) != 0:
                raise ValueError("ORCID must have 16 numbers separated by dashes.")
            if orcid and not re.match(r'^\d{4}-\d{4}-\d{4}-\d{4}$', orcid):
                raise ValueError("Invalid ORCID format.")
            if affiliation and (len(affiliation) > 100 or len(affiliation) < 5):
                raise ValueError("Invalid affiliation length.")
            if not isinstance(developer, bool):
                raise ValueError("Developer field must be a boolean value.")
            if developer and not github_user:
                raise ValueError("Developer must have a GitHub username.")

            user_data = {
                "developer": developer,
                "github_user": github_user
            }
            profile_data = {
                "name": name,
                "surname": surname,
                "affiliation": affiliation,
                "orcid": orcid
            }

            self.user_repo.update(current_user.profile.user.id, **user_data)
            updated_instance = self.update(user_profile_id, **profile_data)

            self.user_repo.session.commit()
            self.repository.session.commit()

        except Exception as exc:
            self.repository.session.rollback()
            self.user_repo.session.rollback()
            raise exc

        return updated_instance
