from __future__ import print_function
import os
from sigh.apps import create_app


config_file = os.path.join(os.path.dirname(os.path.realpath(__file__))
                           , 'config.py')
app = create_app(config_file)


if __name__ == '__main__':
    print('URL map:')
    print(app.url_map)
    app.run(debug=True, host='0.0.0.0')
