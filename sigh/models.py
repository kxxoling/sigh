import datetime

from flask import jsonify
from flask import abort
from flask import url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.whooshalchemy import whoosh_index


db = SQLAlchemy()


class BasicMixin(object):

    id_ = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)          # First time the column is created.

    @classmethod
    def get_or_404(cls, id_=None, **kwargs):
        if id_ is not None:
            obj = cls.query.get(id_)
        else:
            objs = cls.query.filter_by(**kwargs)
            obj = objs and objs[0] or None
        if obj is None:
            abort(404)
        return obj

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
                                     getattr(self, 'name', None) or
                                     getattr(self, 'display_name', None) or
                                     getattr(self, 'title', ''))


class SessionMixin(object):
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self


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
        return url_for('frontend.render_profile', user_id=self.id_)

    def split_avatar(self, width):
        return '{}&s={}'.format(self.avatar, width)


tag_identifier = db.Table('tag_identifier',
                          db.Column('tag_id', db.Integer, db.ForeignKey('tags.id_')),
                          db.Column('sigh_id', db.Integer, db.ForeignKey('sighs.id_')))


class Sigh(db.Model, BasicMixin, SessionMixin):
    __tablename__ = 'sighs'
    __searchable__ = ['content']

    creator_id = db.Column(db.Integer, db.ForeignKey('users.id_'))
    creator = db.relationship('User')
    content = db.Column(db.Text, nullable=False)
    type_ = db.Column(db.Enum('sigh', 'wtf', 'fml', name='content_types'), nullable=False)
    is_anonymous = db.Column(db.Boolean, default=False)
    comments = db.relationship('Comment', order_by="desc(Comment.create_time)")
    tags = db.relationship('Tag', secondary=tag_identifier)


class Tag(db.Model, BasicMixin, SessionMixin):
    __tablename__ = 'tags'

    display_name = db.Column(db.String(50), unique=True, nullable=False)
    searchable_name = db.Column(db.String(500), unique=True, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id_'))      # This could be NULL when it's created bu system
    sighs = db.relationship('Sigh', order_by="desc(Sigh.id_)", secondary=tag_identifier)

    @property
    def sighs_count(self):
        query = db.session.query(tag_identifier).filter_by(tag_id=self.id_)
        return query.count()


class Comment(db.Model, BasicMixin, SessionMixin):
    __tablename__ = 'comments'

    content = db.Column(db.Text, nullable=False)
    sigh_id = db.Column(db.Integer, db.ForeignKey('sighs.id_'))
    sigh = db.relationship('Sigh')
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id_'))
    creator = db.relationship('User')


def index(app):
    for model in [Sigh]:
        whoosh_index(app, model)
