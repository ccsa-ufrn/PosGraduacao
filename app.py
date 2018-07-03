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
from views.crud_students import crud_students
from views.crud_news import crud_news
from views.crud_staff import crud_staff
from views.crud_events import crud_events
from views.crud_classes import crud_classes
from views.crud_participation import crud_participation
from views.crud_scheduled_reports import crud_scheduled_reports
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
APP.register_blueprint(crud_news)
APP.register_blueprint(crud_staff)
APP.register_blueprint(crud_students)
APP.register_blueprint(crud_events)
APP.register_blueprint(crud_classes)
APP.register_blueprint(crud_participation)
APP.register_blueprint(crud_scheduled_reports)

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
