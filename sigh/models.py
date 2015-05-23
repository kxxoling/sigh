import datetime

from flask import jsonify
from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class BasicMixin(object):

    id_ = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)          # First time the column is created.

    def to_json(self, *columns):
        dct = self.to_dict(*columns)
        for key in dct:
            if isinstance(dct[key], datetime.datetime):
                dct[key] = dct[key].strftime('%Y-%m-%d %H:%M:%S')
        return jsonify(dct)

    def to_dict(self, *columns):
        dct = {}
        for col in columns:
            dct[col] = getattr(self, col)
        return dct

    def __unicode__(self):
        return "<Model %s>%d: %s" % (self.__class__.__name__, self.id_,
                                     getattr(self, 'name', None) or getattr(self, 'title', 'Untitled'))


class SessionMinin(object):
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self


class User(db.Model, BasicMixin, SessionMinin):
    __tablename__ = 'users'

    name = db.Column(db.String(100))
    email = db.Column(db.String(50))
    family_name = db.Column(db.String(100))
    role = db.Column(db.Integer)
    sighs = db.relationship('Sigh')
    tags = db.relationship('Tag')


tag_identifier = db.Table('tag_identifier',
                          db.Column('tag_id', db.Integer, db.ForeignKey('tags.id_')),
                          db.Column('sigh_id', db.Integer, db.ForeignKey('sighs.id_')))


class Sigh(db.Model, BasicMixin, SessionMinin):
    __tablename__ = 'sighs'

    creator_id = db.Column(db.Integer, db.ForeignKey('users.id_'))
    content = db.Column(db.Text, nullable=False)
    type_ = db.Column(db.Enum('sigh', 'wtf', 'fml'), nullable=False)
    is_anonymous = db.Column(db.Boolean, default=False)
    tags = db.relationship('Tag', secondary=tag_identifier)


class Tag(db.Model, BasicMixin, SessionMinin):
    __tablename__ = 'tags'

    name = db.Column(db.String(50), unique=True, nullable=False)
    display_name = db.Column(db.String(50), unique=True, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id_'))
