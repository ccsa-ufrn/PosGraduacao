"""
Routes and views for system administration pages.
"""

from flask_login import LoginManager, \
    login_user, login_required, logout_user
from flask import Blueprint, render_template

from models.factory import PosGraduationFactory
from models.users import User

from settings.extensions import ExtensionsManager

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
        login_user(User())
        return render_template(
            'admin/login.html',
            form=form,
        )
    else:
        return render_template(
            'admin/login.html',
            form=form,
        )


@APP.route('/logout/')
@login_required
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


@ExtensionsManager.login_manager.user_loader
def user_loader(post_graduation_initials, nick='mazuh'):
    """Load an user from database."""
    print('LOADER')
    print(post_graduation_initials)
    print(nick)
    return User.get(post_graduation_initials, nick)


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
