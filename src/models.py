from datetime import datetime

from sqlalchemy import func

from src import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    sessions = db.relationship('Session', backref='u_session', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def as_dict(self):
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.relationship('Like', backref='post', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

    def as_dict(self):
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    likes = db.Column(db.Integer, default=1)
    liked_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    @classmethod
    def filter_by_date_and_post(cls, post_id: int, date_from, date_to) -> int:
        likes = db.session.query(func.sum(cls.likes).label('likes_filtered')). \
            filter(cls.post_id == post_id). \
            filter(cls.liked_at >= date_from). \
            filter(cls.liked_at < date_to).one()[0]

        return likes

    @classmethod
    def sum_likes_by_post(cls, post_id: int):
        likes = db.session.query(func.sum(cls.likes).label('likes')). \
            filter(cls.post_id == post_id). \
            one()[0]
        return likes

    @classmethod
    def filter_by_date(cls, date_from, date_to) -> int:
        likes = db.session.query(func.sum(cls.likes).label('likes_filtered')). \
            filter(cls.liked_at >= date_from). \
            filter(cls.liked_at < date_to).one()[0]

        return likes


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(100), nullable=False, unique=True)
    login_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def as_dict(self):
        return {
            'id': self.id,
            'token': self.token,
            'user_id': self.user_id,
            'login_time': str(self.login_time),
        }

    @classmethod
    def get_last_login(cls, user_id: int) -> str:
        last_login = db.session.query(func.max(cls.login_time).label('last_login')). \
            filter(cls.user_id == user_id). \
            first()[0]

        return str(last_login)
