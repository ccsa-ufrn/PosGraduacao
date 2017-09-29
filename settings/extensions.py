"""Flask extensions configuration."""

from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect


class ExtensionsManager:
    """An app's Flask extensions manager."""
    csrf = CSRFProtect()
    login_manager = LoginManager()

    def __init__(self):
        """This will raise an exception."""
        raise NotImplementedError('Use only static members for this class.')

    @staticmethod
    def auto_configure(app):
        """Initialize extensions needed for this Flask app."""
        app.config['SECRET_KEY'] = 'english,motherfucker!doyouspeak?'

        ExtensionsManager.csrf.init_app(app)
        ExtensionsManager.login_manager.init_app(app)
