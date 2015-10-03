from __future__ import print_function
import os
import yaml

from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.script import Manager

from sigh.apps import create_app
from sigh.models import User, Sigh, Tag


base_dir = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(base_dir, 'config.py')
application = create_app(config_file)
manager = Manager(application)


def debug_app(app):
    app.debug = True
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
    application.run(debug=True, host=host, port=port)


@manager.command
def load(fxtdir='fixtures/', app_name='sigh'):
    application.db.create_all()

    fixture_dir = os.path.join(base_dir, app_name, fxtdir)
    fixture_file = os.path.join(fixture_dir, 'testdata.yaml')
    with open(fixture_file) as f:
        fixture_data = yaml.load(f.read())
    user_data = fixture_data['users']
    sigh_data = fixture_data['sighs']
    tag_data = fixture_data['tags']

    with application.app_context():
        for user in user_data:
            User(**user).save()

        for sigh in sigh_data:
            Sigh(**sigh).save()

        for tag in tag_data:
            Tag(**tag).save()


if __name__ == '__main__':
    manager.run()

