from flask.ext.whooshalchemy import whoosh_index

from .base import db
from .user import User                                      # noqa
from .main import Sigh, Tag, Comment, tag_identifier        # noqa


def index(app):
    for model in [Sigh]:
        whoosh_index(app, model)

