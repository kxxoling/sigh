from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class BasicModel(object):

    id_ = db.Column(db.Integer, primary_key=True)

    def to_dict(self):
        raise NotImplementedError       # Exception('NotImplemented')

    def to_json(self):
        pass

    def __unicode__(self):
        return "<Model %s>%d: %s" % (self.__class__.__name__, self.id_,
                getattr(self, 'name', None) or getattr(self, 'title', 'Untitled'))


class User(BasicModel, db.Model):
    __tablename__ = 'users'

    name = db.Column(db.String(100))
    email = db.Column(db.String(50))
    family_name = db.Column(db.String(100))
    register_time = db.Column(db.DateTime)
    role = db.Column(db.Integer)
    sigh = db.relationship('Sigh')


class Sigh(BasicModel, db.Model):
    __tablename__ = 'sighs'

    creater_id = db.Column(db.Integer, db.ForeignKey('users.id_'))
    create_time = db.Column(db.DateTime)
    content = db.Column(db.Text)
