from flask import Blueprint
from flask import render_template, jsonify
from flask import url_for, request
from flask import g

from ..models import Sigh
from ..forms import SighForm, CommentForm
from ..models import Comment
from ..models import User
from ..models import Tag


frontend_views = Blueprint('frontend', __name__, url_prefix='/')


@frontend_views.before_request
def get_site_info():
    g.user_count = User.query.count()
    g.comment_count = Comment.query.count()
    g.sigh_count = Sigh.query.count()
    g.tag_count = Tag.query.count()


@frontend_views.route('/')
@frontend_views.route('<int:page_num>/')
def index(page_num=1):
    sighs_pagination = Sigh.query.order_by(Sigh.create_time.desc()).paginate(page_num, per_page=20, error_out=True)
    return render_template('index.jade', page_title='Programmer sighs!', sighs_pagination=sighs_pagination)


@frontend_views.route('sigh/<int:sigh_id>/')
def render_sigh(sigh_id):
    sigh = Sigh.query.get_or_404(sigh_id)
    comments = sigh.comments
    return render_template('sigh.jade', page_title='Programmer sighs!', sigh=sigh, comments=comments)


@frontend_views.route('new/', methods=['POST'])
def post_sigh():
    """TODO: Should be login required later"""

    form = SighForm(request.form)
    if form.validate():
        sigh = form.save()
        return jsonify(dict(
            sigh_id=sigh.id_,
            redirect_url=url_for('frontend.render_sigh', sigh_id=sigh.id_),
        ))
    else:
        return jsonify(form.errors), 405


@frontend_views.route('sigh/<int:sigh_id>/comment/', methods=['POST'])
def post_comment(sigh_id):
    """TODO: Should be login required later"""
    form = CommentForm(request.form)
    if form.validate():
        comment = form.save(creator_id=1, sigh_id=sigh_id)
        return comment.to_json('creator_id', 'content', 'id_', 'create_time', 'sigh_id')
    else:
        return jsonify(form.errors), 405

