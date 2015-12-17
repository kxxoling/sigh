from __future__ import print_function
import os
import yaml

from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.script import Manager
from flask.ext.shellplus import Shell

from sigh.apps import create_app
from sigh.models import db
from sigh.models import User, Sigh, Tag, tag_identifier, Comment


base_dir = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(base_dir, 'config.py')
application = create_app(config_file)
manager = Manager(application)


def debug_app(app):
    toolbar = DebugToolbarExtension()
    toolbar.init_app(app)


def manage_app(app, app_manager):
    app_manager.init_app(app)


@manager.command
def runserver(port=5000, host='0.0.0.0', init=False):
    port = int(port)
    debug_app(application)
    if init is True:
        application.db.create_all()
    try:
        from livereload import Server
        server = Server(application)
        server.serve(port=port)
    except ImportError:
        application.run(host=host, port=port)


@manager.command
def load(fxtdir='fixtures/', app_name='sigh'):
    application.db.create_all()

    fixture_dir = os.path.join(base_dir, app_name, fxtdir)
    fixture_file = os.path.join(fixture_dir, 'testdata.yaml')
    with open(fixture_file) as f:
        fixture_data = yaml.load(f.read())

    data_pairs = ((User, fixture_data['users']),
        (Sigh, fixture_data['sighs']),
        (Tag, fixture_data['tags']),
        (Comment, fixture_data['comments']))

    with application.app_context():
        for model, datas in data_pairs:
            for data in datas:
                model(**data).save()

        for data in fixture_data['tag_identifiers']:
            db.engine.execute(tag_identifier.insert().values(**data))


manager.add_command('shell', Shell(context=dict(app=application, db=db)))


if __name__ == '__main__':
    manager.run()

