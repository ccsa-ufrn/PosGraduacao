"""
Form about the scheduled reports
"""

import datetime

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import DateField
from wtforms.widgets.html5 import TimeInput
from wtforms.validators import DataRequired


class TimeField(StringField):
    """
    HTML5 time input.
    """
    widget = TimeInput()

    def __init__(self, label=None, validators=None, format='%H:%M:%S', **kwargs):
        super(TimeField, self).__init__(label, validators, **kwargs)
        self.format = format

    def _value(self):
        if self.raw_data:
            return ' '.join(self.raw_data)
        else:
            return self.data and self.data.strftime(self.format) or ''

    def process_formdata(self, valuelist):
        if valuelist:
            time_str = ' '.join(valuelist)
            try:
                components = time_str.split(':')
                hour = 0
                minutes = 0
                seconds = 0
                if len(components) in range(2, 4):
                    hour = int(components[0])
                    minutes = int(components[1])

                    if len(components) == 3:
                        seconds = int(components[2])
                else:
                    raise ValueError
                self.data = datetime.time(hour, minutes, seconds)
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid time string'))


class ScheduledReportForm(FlaskForm):
    """
    Scheduled report form.
    """
    date = DateField('Data', validators=[
        DataRequired('Digite a data da apresentação.')
    ])
    time = TimeField(label='Hora', validators=[
        DataRequired('Digite a hora da apresentação')
    ])
    title = StringField('Trabalho de conclusão', validators=[
        DataRequired('Digite o título do trabalho.')
    ])
    author = StringField('Autor(es)', validators=[
        DataRequired('Digite o nome do(s) autor(es).')
    ])
    location = StringField('Localização', validators=[
        StringField('Digite a localização.')
    ])
