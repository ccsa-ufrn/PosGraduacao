"""
Form about the scheduled reports
"""

from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SubmitField
from wtforms.validators import DataRequired


class ScheduledReportForm(FlaskForm):
    """
    Scheduled report form.
    """
    time = DateTimeField('Data e hora', format='%d/%m/%Y %H:%M')
    title = StringField('Trabalho de conclusão', validators=[
        DataRequired('Digite o título do trabalho.')
    ])
    author = StringField('Autor(es)', validators=[
        DataRequired('Digite o nome do(s) autor(es).')
    ])
    location = StringField('Localização', validators=[
        DataRequired('Digite a localização.')
    ])
    create = SubmitField('Cadastrar')
