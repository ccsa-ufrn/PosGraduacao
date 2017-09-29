"""Flask extensions configuration."""

from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from views.public import app as public_app
from views.admin import APP as admin_app


def configure_flask(app):
    """Initialize extensions needed for this Flask app."""

    app.config['SECRET_KEY'] = 'english,motherfucker!doyouspeak?'

    app.register_blueprint(public_app)
    app.register_blueprint(admin_app)

    csrf = CSRFProtect()
    csrf.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
