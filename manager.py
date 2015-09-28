from __future__ import print_function
import os
from sigh.apps import create_app
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.script import Manager


config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.py')
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
    application.run(debug=True, host='0.0.0.0', port=port)


if __name__ == '__main__':
    manager.run()

