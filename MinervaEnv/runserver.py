"""
This script runs the Minerva application using a development server.
"""
import locale

from os import environ
from Minerva import app

if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') # caution, this may crash in some OS

    app.jinja_env.cache = {}
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    HOST = environ.get('SERVER_HOST', 'localhost')

    try:
        PORT = int(environ.get('SERVER_PORT', '4444'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)
