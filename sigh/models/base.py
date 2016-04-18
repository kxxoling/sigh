import datetime

from flask import jsonify
from flask import abort
from flask.ext.sqlalchemy import SQLAlchemy


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

