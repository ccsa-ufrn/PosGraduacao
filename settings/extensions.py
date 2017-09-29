"""Flask extensions configuration."""

from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from views.public import app as public_app
from views.admin import APP as admin_app


class ExtensionsManager:
    """An app's Flask extensions manager."""
    csrf = CSRFProtect()
    login_manager = LoginManager()

    @staticmethod
    def auto_configure(app):
        """Initialize extensions needed for this Flask app."""
        app.config['SECRET_KEY'] = 'english,motherfucker!doyouspeak?'

        app.register_blueprint(public_app)
        app.register_blueprint(admin_app)

        ExtensionsManager.csrf.init_app(app)
        ExtensionsManager.login_manager.init_app(app)
