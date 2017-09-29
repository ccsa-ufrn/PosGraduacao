"""
Has some functionalities about user authentication and
session management.
"""

from models.factory import PosGraduationFactory


class User(object):
    """
    Implements some properties and methods according to Flask-Login
    extension:
    <https://flask-login.readthedocs.io/en/latest/#your-user-class)
    """

    def __init__(self):
        self._id = 'meuid'
        self._is_authenticated = True
        self._is_active = True
        self._is_anonymous = False

    @property
    def is_authenticated(self):
        """
        This property should return True if the user is authenticated,
        i.e. they have provided valid credentials.
        (Only authenticated users will fulfill the criteria of
        login_required.)
        """
        return self._is_authenticated

    @property
    def is_active(self):
        """
        This property should return True if this is an active
        user - in addition to being authenticated, they also have
        activated their account, not been suspended, or any condition
        your application has for rejecting an account. Inactive
        accounts may not log in (without being forced of course).
        """
        return self._is_active

    @property
    def is_anonymous(self):
        """
        This property should return True if this is an anonymous user.
        (Actual users should return False instead.)
        """
        return self._is_anonymous

    def get_id(self):
        """
        This method must return a unicode that uniquely identifies
        this user, and can be used to load the user from the
        user_loader callback. Note that this must be a
        unicode - if the ID is natively an int or some other type,
        you will need to convert it to unicode.
        """
        return self._id

    @staticmethod
    def get(pg_initials, nick):
        """Return an user dict from database. If failed, None."""
        try:
            program = PosGraduationFactory(pg_initials).post_graduation
            for user in program['users']:
                if nick == user['nick']:
                    return user
            return None
        except (TypeError, AttributeError):
            return None
