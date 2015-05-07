import os
from sigh.apps import create_app


config_file = os.path.join(os.path.dirname(os.path.realpath(__file__))
                           , 'config.py')
application = create_app(config_file)

