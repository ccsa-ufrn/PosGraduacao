"""
Routes and views for system administration pages.
"""

from flask_login import LoginManager, \
    login_user, login_required, logout_user
from flask import Blueprint, render_template
# from pymongo.errors import ServerSelectionTimeoutError

# from models.scraping import final_reports
# from models.clients.util import keyring

# from models.factory import PosGraduationFactory
from views.forms.auth import LoginForm
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
    return login()


@APP.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Render an user authorization form.
    """

    form = LoginForm()

    if form.validate_on_submit():
        pass
        # TODO login user from db (see: https://medium.com/@perwagnernielsen/getting-started-with-flask-login-can-be-a-bit-daunting-in-this-tutorial-i-will-use-d68791e9b5b5)
        # login_user(user.findone)
        # if found, go index, else invalidate form
    else:
        return render_template(
            'admin/login.html',
            form=form,
        )


@APP.route('/logout/')
def logout():
    """
    Render a logged out page.
    """

    form = LoginForm()

    logout_user()

    return render_template(
        'admin/login.html',
        form=form,
        goodbye=True
    )


@APP.route('/401')
@login_required
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
