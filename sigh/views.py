import datetime

from flask import Blueprint
from flask import render_template
from flask import url_for, session, request, redirect, flash
from flask.ext.oauthlib.client import OAuth

from .models import Sigh, Tag
from .models import db


frontend_views = Blueprint('frontend', __name__, url_prefix='/')

oauth_views = Blueprint('oauth', __name__, url_prefix='/oauth/')

oauth = OAuth()
github = oauth.remote_app(
    'github',
    consumer_key='08db72ce47a207704fb4',
    consumer_secret='f5e5eff75760ea886e033a6ec87b23d33d4903a0',
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)


@frontend_views.route('/')
def index():
    sighs = Sigh.query.all()
    return render_template('index.jade', page_title='Programmer sighs!', sighs=sighs)


@frontend_views.route('sigh/<int:sigh_id>/')
def render_sigh(sigh_id):
    sigh = Sigh.query.get_or_404(sigh_id)
    return render_template('sigh.jade', page_title='Programmer sighs!', sigh=sigh)


@frontend_views.route('new/', methods=['POST'])
def post_sigh():
    """TODO: Should be login required later"""
    if request.form.get('wtf') == 'on':
        type_ = 'wtf'
    elif request.form.get('fml') == 'on':
        type_ = 'fml'
    else:
        type_ = 'sigh'
    content = request.form.get('content')
    is_anonymous = (request.form.get('is_anonymous') == 'on') or False
    tags = request.form.getlist('tags')
    tag_models = filter(lambda x: x, [Tag.query.filter_by(name=tag).first() for tag in tags])
    sigh = Sigh(type_=type_, content=content, is_anonymous=is_anonymous, creator_id=1,
                create_time=datetime.datetime.now())
    sigh.tags.extend(tag_models)
    db.session.add(sigh)
    db.session.commit()
    return redirect(url_for('frontend.render_sigh', sigh_id=sigh.id_))


@oauth_views.route('login/')
def github_login():
    return github.authorize(callback=url_for('oauth.github_authorized', _external=True))


@oauth_views.route('logout')
def github_logout():
    session.pop('github_token', None)
    return redirect(url_for('frontend.index'))


@oauth_views.route('login/authorized')
def github_authorized():
    resp = github.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error'],
            request.args['error_description'],
        )
    session['github_token'] = (resp['access_token'], '')
    user = github.get('user')
    flash('%s, Welcome!' % user.data['name'])
    return redirect('/')


@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')
