"""
This script runs the application using a development server.
"""
#import locale

from flask import Flask, Blueprint
from views.public import app as public_app

app = Flask(__name__)
app.register_blueprint(public_app)

PUBLIC_HOST = '0.0.0.0'
PUBLIC_PORT = 80
DEV_HOST = 'localhost'
DEV_PORT = 4444

if __name__ == '__main__':
    #locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    try:
        app.run(PUBLIC_HOST, PUBLIC_PORT)
    except PermissionError:
        print('DEVELOPMENT MODE: running at localhost only!!!')
        app.jinja_env.cache = {}
        app.jinja_env.auto_reload = True
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.run(DEV_HOST, DEV_PORT, debug=True)
