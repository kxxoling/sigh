from flask import Flask
from flask import send_file
from flask import request
from flask_babelex import Babel

from .views.front import front_views
from .views.auth import oauth_views
from .views.auth import oauth
from .views.api import api_views
from .models import db as main_db
from .models import index
from .admin import register_admin
from .utils import timeago, plain_markdown


def create_app(default_config=None, config_spec=None):
    app = Flask(
        __name__,
        template_folder='templates'
    )

    app.config.from_pyfile(default_config)
    if app.config.get('LOCAL_CONFIG'):
        app.config.from_pyfile(app.config['LOCAL_CONFIG'])
    if isinstance(config_spec, dict):
        app.config.update(config_spec)

    #: prepare for database
    main_db.init_app(app)
    app.db = main_db
    with app.app_context():
        index(app)

    register_babel(app)
    register_jinja(app)
    register_static(app)
    register_oauth(app, oauth)
    register_routes(app)
    register_admin(app, main_db)
    register_filter(app, timeago=timeago, md=plain_markdown)

    return app


def register_routes(app):
    app.register_blueprint(front_views)
    app.register_blueprint(oauth_views)
    app.register_blueprint(api_views)
    return app


def register_oauth(app, oauth):
    app.config['GITHUB'].update(dict(
        request_token_params={'scope': 'user:email'},
        base_url='https://api.github.com/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='https://github.com/login/oauth/access_token',
        authorize_url='https://github.com/login/oauth/authorize')
    )
    oauth.init_app(app)


def register_static(app):
    @app.route('/<file_name>.txt')
    def plain_file(file_name):
        return send_file(file_name)
    return app


def register_jinja(app):
    app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
    return app


def register_babel(app):
    babel = Babel(app)
    app.jinja_env.add_extension('jinja2.ext.with_')

    @babel.localeselector
    def get_locale():
        match = app.config['BABEL_SUPPORTED_LOCALES']
        default = app.config['BABEL_DEFAULT_LOCALE']
        return request.accept_languages.best_match(match, default)
    return babel


def register_filter(app, **filters):
    app.jinja_env.filters.update(filters)
