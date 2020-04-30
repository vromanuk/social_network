from src import db
from src.models import User


class AuthService:
    @classmethod
    def register(cls, user: User):
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()

    @classmethod
    def login(cls, user: User):
        pass

    @classmethod
    def logout(cls):
        pass
