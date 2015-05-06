from flask import Flask
from flask import send_file

from .views import frontend_views
from .views import oauth_views
from .views import oauth
from .models import db as main_db
from .admin import register_admin


def create_app(config=None):
    app = Flask(
        __name__,
        template_folder='templates'
    )

    if isinstance(config, dict):
        app.config.update(config)
    elif config:
        app.config.from_pyfile(config)

    #: prepare for database
    main_db.init_app(app)
    main_db.app = app
    main_db.create_all()

    register_jinja(app)
    register_static(app)
    register_oauth(app, oauth)
    register_routes(app)
    register_admin(app, main_db)

    return app


def register_routes(app):
    app.register_blueprint(frontend_views)
    app.register_blueprint(oauth_views)
    return app


def register_oauth(app, oauth):
    oauth.init_app(app)


def register_static(app):
    @app.route('/<file_name>.txt')
    def plain_file(file_name):
        return send_file(file_name)
    return app


def register_jinja(app):
    app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
    return app
