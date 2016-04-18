from .base import db, BasicMixin, SessionMixin


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

