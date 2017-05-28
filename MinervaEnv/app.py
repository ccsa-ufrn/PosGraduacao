"""
This script runs the Minerva application using a development server.
"""
#import locale

from Minerva import app

PUBLIC_HOST = '0.0.0.0'
PUBLIC_PORT = 80
DEV_HOST = 'localhost'
DEV_PORT = 4444

if __name__ == '__main__':
#    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    #app.jinja_env.cache = {}
    #app.jinja_env.auto_reload = True
    #app.config['TEMPLATES_AUTO_RELOAD'] = True

    try:
        app.run(PUBLIC_HOST, PUBLIC_PORT)
    except PermissionError:
        print('DEVELOPMENT MODE: running at localhost only!!!')
        app.run(DEV_HOST, DEV_PORT, debug=True)
