from __future__ import print_function
import os
from sigh.apps import create_app
from flask.ext.debugtoolbar import DebugToolbarExtension


config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.py')


def debug_app(app):
    app.debug = True
    toolbar = DebugToolbarExtension()
    toolbar.init_app(app)


if __name__ == '__main__':
    application = create_app(config_file)
    debug_app(application)
    application.run(debug=True, host='0.0.0.0')
