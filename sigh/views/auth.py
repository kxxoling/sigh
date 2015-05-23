from flask import Blueprint
from flask import url_for, session, request
from flask import redirect, flash
from flask.ext.oauthlib.client import OAuth


oauth_views = Blueprint('oauth', __name__, url_prefix='/oauth/')

oauth = OAuth()

github = oauth.remote_app(
    'github',
    app_key='GITHUB',
)


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
