"""
This script runs the Minerva application using a development server.
"""
#import locale

from Minerva import app

if __name__ == '__main__':
#    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    #app.jinja_env.cache = {}
    #app.jinja_env.auto_reload = True
    #app.config['TEMPLATES_AUTO_RELOAD'] = True

    HOST = '0.0.0.0'
    PORT = 80

    try:
        app.run(HOST, PORT, debug=True)
    except PermissionError:
        app.run('DEVELOPMENT MODE: running at localhost only!!!')
        app.run('localhost', 4444, debug=True)
