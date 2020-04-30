import datetime

from flask_jwt_extended import create_access_token

from src import db
from src.models import User, Session


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
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        session = Session(token=access_token, u_session=user)

        db.session.add(session)
        db.session.commit()

        return {'token': access_token}

    @classmethod
    def logout(cls):
        pass
