from flask import url_for

from .base import db, BasicMixin, SessionMixin


class User(db.Model, BasicMixin, SessionMixin):
    __tablename__ = 'users'

    username = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(50))
    avatar = db.Column(db.String(100))
    github_id = db.Column(db.String(20), unique=True)
    github_username = db.Column(db.String(50))
    role = db.Column(db.Integer)

    sighs = db.relationship('Sigh')
    tags = db.relationship('Tag')
    comments = db.relationship('Comment')

    @property
    def profile_url(self):
        return url_for('front.render_profile', user_id=self.id_)

    def split_avatar(self, width):
        return '{}&s={}'.format(self.avatar, width)

