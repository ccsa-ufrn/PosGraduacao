"""
Forms about content editing.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField,\
                    TextAreaField, DateTimeField, SubmitField
from wtforms.validators import DataRequired


class ParticipationsInEventsForm(FlaskForm):
    """
    Form for the list of participations in events.
    """
    title = StringField('Instituição visitada:', validators=[
        DataRequired('Digite uma chamada para o intercâmbio.')
    ])

    description = TextAreaField('Resumo do envolvimento:', validators=[
        DataRequired('Insira um breve resumo sobre a participação.')
    ])

    year = IntegerField('Ano:', validators=[
        DataRequired('Informe qual o ano do evento.')
    ])

    location = StringField('Cidade e país:', validators=[
        DataRequired('Falta localizar a cidade e país.')
    ])

    create = SubmitField('Adicionar')


class ScheduledReportForm(FlaskForm):
    """
    Scheduled report form.
    """
    time = DateTimeField('Data e hora:', format='%d/%m/%Y %H:%M')

    title = StringField('Título do trabalho:', validators=[
        DataRequired('Digite o título do trabalho.')
    ])

    author = StringField('Autoria:', validators=[
        DataRequired('Digite o nome do(s) autor(es).')
    ])

    location = StringField('Localização:', validators=[
        DataRequired('Digite a localização.')
    ])

    create = SubmitField('Agendar')
