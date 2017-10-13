"""
Routes and views for system administration pages.
"""

import re

from flask_login import LoginManager, \
    login_user, login_required, logout_user, current_user
from flask import Blueprint, render_template

from models.factory import PosGraduationFactory
from models.users import User

from settings.extensions import ExtensionsManager

from views.forms.auth import LoginForm
from views.forms.scheduled_report import ScheduledReportForm
from models.clients.api_sistemas import SigaaError, \
    FailedToGetTokenForSigaaError, UnreachableSigaaError, \
    NoAppCredentialsForSigaaError


APP = Blueprint('admin',
                __name__,
                static_folder='static',
                url_prefix='/admin')


@APP.route('/')
def index():
    """
    If user is already authenticated, render its
    dashboard, otherwise ask for his password.
    """
    if current_user and current_user.is_authenticated:

        pfactory = PosGraduationFactory(current_user.pg_initials)
        post_graduation = pfactory.post_graduation

        return render_template(
            'admin/index.html',
            post_graduation=post_graduation
        )

    else:
        return login()


@APP.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Render an user authorization form.
    """

    form = LoginForm()

    if form.validate_on_submit():
        user_attempting = User.get(form.nick.data, 'PPGP')

        if (user_attempting is not None) and (user_attempting.authenticate(form.password.data)):
            login_user(user_attempting)
            return index()
        else:
            return render_template(
                'admin/login.html',
                form=form,
                incorrect_attempt=True
            )
    else:
        return render_template(
            'admin/login.html',
            form=form,
            incorrect_attempt=False
        )


@APP.route('/logout/')
@login_required
def logout():
    """
    Render a logged out page.
    """

    logout_user()

    return render_template(
        'admin/logout.html'
    )


@APP.route('/new_report/', methods=['GET', 'POST'])
@login_required
def create_report():
    """
    Render a report form.
    """

    form = ScheduledReportForm()

    if form.validate_on_submit():
        return index()
    else:
        return render_template(
            'admin/create_report.html',
            form=form
        )


@ExtensionsManager.login_manager.user_loader
def user_loader(user_id):
    """Load an user from database,
    using an user_id string formatted like 'user_nick@program_initials'."""
    match = re.match('(?P<nick>.*)@(?P<pg>.*)', user_id)
    if match is not None:
        return User.get(
            match.group('nick'),
            match.group('pg'),
            authenticated=True
        )
    else:
        return None


@APP.route('/401/')
@ExtensionsManager.login_manager.unauthorized_handler
def unauthorized():
    """Render page to be showed up for not logged in users."""
    return render_template('admin/401.html')


@APP.route('/404/')
@APP.errorhandler(404)
def page_not_found(error=None):
    """Render page not found error."""

    print(str(error))
    return render_template('admin/404.html',), 404


@APP.errorhandler(SigaaError)
def sigaa_exception_handler(error):
    """Render page for APISistemas errors. """
    print("ERROR for API Sistemas (" + repr(error) + "): " + str(error))

    if isinstance(error, UnreachableSigaaError):
        return render_template('admin/503.html',), 503

    if isinstance(error, FailedToGetTokenForSigaaError):
        return render_template('admin/501.html',), 501

    if isinstance(error, NoAppCredentialsForSigaaError):
        return render_template('admin/500.html',), 500
