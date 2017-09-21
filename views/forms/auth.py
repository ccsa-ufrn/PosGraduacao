"""
Forms about content editing.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """
    Sign in form.
    """
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
