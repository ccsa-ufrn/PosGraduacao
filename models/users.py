"""
Has some functionalities about user authentication and
session management.
"""

from models.factory import PosGraduationFactory
from bcrypt import checkpw, hashpw, gensalt

class User(object):
    """
    Implements some properties and methods according to Flask-Login
    extension:
    <https://flask-login.readthedocs.io/en/latest/#your-user-class)
    """

    def __init__(self):
        self._id = None
        self._post_graduation_program_initials = None
        self._nick = None
        self._password = None
        self._full_name = None
        self._role = None
        self._email = None
        self.__is_authenticated = None
        self.__is_active = None
        self.__is_anonymous = None

    def authenticate(self, raw_password_try):
        """Try to log in using an raw password (not hashed yet), and return True
        if this user instance is now authenticated, otherwise False."""
        if User._check_password(self._password, raw_password_try):
            self.__is_authenticated = True
        else:
            self.__is_authenticated = False

        return self.__is_authenticated

    @staticmethod
    def _hash_password(raw_password):
        """Encode and convert a raw password into a hash. Return a string result."""
        return hashpw(raw_password.encode('utf-8'), gensalt())

    @staticmethod
    def _check_password(real_hashed_password, raw_password_try):
        """Hash the raw_try_pass and check if they match. Return a boolean result."""
        return checkpw(real_hashed_password, raw_password_try.encode('utf-8'))

    @property
    def id(self):
        """An unique representation of a certain user."""
        return '{}@{}'.format(self._nick, self._post_graduation_program_initials)

    @property
    def nick(self):
        """An user nickname."""
        return self._nick

    @property
    def password(self):
        """An user password, already hashed."""
        return self._password

    @property
    def is_authenticated(self):
        """
        This property should return True if the user is authenticated,
        i.e. they have provided valid credentials.
        (Only authenticated users will fulfill the criteria of
        login_required.)
        """
        return self.__is_authenticated

    @property
    def is_active(self):
        """
        This property should return True if this is an active
        user - in addition to being authenticated, they also have
        activated their account, not been suspended, or any condition
        your application has for rejecting an account. Inactive
        accounts may not log in (without being forced of course).
        """
        return self.__is_active

    @property
    def is_anonymous(self):
        """
        This property should return True if this is an anonymous user.
        (Actual users should return False instead.)
        """
        return self.__is_anonymous

    def get_id(self):
        """
        This method must return a unicode that uniquely identifies
        this user, and can be used to load the user from the
        user_loader callback. Note that this must be a
        unicode - if the ID is natively an int or some other type,
        you will need to convert it to unicode.
        """
        return self.id

    @staticmethod
    def get(nick, pg_initials):
        """Return an User from database. If failed, None."""
        try:
            program = PosGraduationFactory(pg_initials).post_graduation
            for user in program['users']:
                if nick.lower() == user['nick'].lower():
                    found_user = User()
                    found_user._nick = user['nick']
                    found_user._post_graduation_program_initials = pg_initials.lower()
#                    found_user._password = bytes(user['password'].encode('utf-8'))
                    found_user._password = User._hash_password('mazuh')
                    found_user._full_name = user['fullName']
                    found_user._role = user['role']
                    found_user._email = user['email']
                    found_user.__is_authenticated = False
                    found_user.__is_active = True
                    found_user.__is_anonymous = False
                    return found_user
            return None
        except (TypeError, AttributeError):
            return None
