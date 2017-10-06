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
    nick = StringField('Usuário', validators=[
        DataRequired('Digite o seu usuário.')
    ])
    password = PasswordField('Senha', validators=[
        DataRequired('Digite sua senha.')
    ])
