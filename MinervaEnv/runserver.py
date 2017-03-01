"""
This script runs the Minerva application using a development server.
"""

from os import environ
from Minerva import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '4444'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
