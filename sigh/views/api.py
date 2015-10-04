import json
from functools import wraps

from flask import Blueprint
from flask import Response

from ..models import Tag
from ..models import User


api_views = Blueprint('api', __name__, url_prefix='/api/')


def jsonify(func):
    @wraps(func)
    def _(*args, **kwargs):
        result = func(*args, **kwargs)
        return Response(json.dumps(result),  mimetype='application/json')
    return _


@api_views.route('tag/autocompletion/<q>')
@jsonify
def autocomplete_tag(q):
    tags = Tag.query.filter(Tag.searchable_name.ilike(u'%{}%'.format(q.lower()))).all()
    tags = [tag.to_dict('id_', 'display_name') for tag in tags]
    return tags


@api_views.route('user/autocompletion/<q>')
@jsonify
def autocomplete_user(q):
    users = User.query.filter(User.username.ilike(u'%{}%'.format(q.lower()))).all()
    users = [user.to_dict('id_', 'name', 'username', 'avatar') for user in users]
    return users
