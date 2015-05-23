import datetime

from flask import Blueprint
from flask import render_template, jsonify
from flask import url_for, session, request
from flask import redirect, flash, abort
from flask.ext.oauthlib.client import OAuth

from .models import Sigh, Tag
from .forms import SighForm


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

    form = SighForm(request.form)
    if form.validate():
        sigh = form.save()
        return redirect(url_for('frontend.render_sigh', sigh_id=sigh.id_))
    else:
        return jsonify(form.errors), 405


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
