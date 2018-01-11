"""
This script runs the application using a development server.
"""
# import locale

from flask import Flask

from views.public import app as public_app
from views.admin import APP as admin_app
from views.crud_books import crud_books
from views.crud_articles import crud_articles
from views.crud_subjects import crud_subjects
from views.crud_attendances import crud_attendances
from views.crud_projects import crud_projects
from settings.extensions import ExtensionsManager

APP = Flask(__name__)
ExtensionsManager.auto_configure(APP)

APP.register_blueprint(public_app)
APP.register_blueprint(admin_app)
APP.register_blueprint(crud_books)
APP.register_blueprint(crud_articles)
APP.register_blueprint(crud_subjects)
APP.register_blueprint(crud_attendances)
APP.register_blueprint(crud_projects)

PUBLIC_HOST = '0.0.0.0'
PUBLIC_PORT = 3001
DEV_HOST = 'localhost'
DEV_PORT = 4444

if __name__ == '__main__':

    try:
        APP.run(PUBLIC_HOST, PUBLIC_PORT)
    except PermissionError:
        print('DEVELOPMENT MODE: running at localhost only!!!')
        APP.jinja_env.auto_reload = True
        APP.config['TEMPLATES_AUTO_RELOAD'] = True
        APP.run(DEV_HOST, DEV_PORT, debug=True)
