"""
Routes and views for participation CRUD.
"""

from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request

from models.factory import PosGraduationFactory

from settings.extensions import ExtensionsManager

from views.forms.content import CalendarForm

from bson.json_util import dumps
import json
import datetime

crud_events = Blueprint('crud_events', __name__, url_prefix='/admin')


###############################################################################
#Adicionar deletar e editar eventos
###############################################################################

@crud_events.route('/add_evento/', methods=['GET', 'POST'])
@login_required
def add_events():
    """Render a view for adding events."""

    form = CalendarForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.calendar_dao()
    
    if form.validate_on_submit():
        initial_date = datetime.datetime.combine(form.initial_date.data, datetime.datetime.min.time())
        if form.final_date.data != "":
            final_date = datetime.datetime.strptime(form.final_date.data, '%d/%m/%Y')
            final_date = datetime.datetime.combine(final_date, datetime.datetime.min.time())
        else:
            final_date = form.final_date.data
        new_event = {
            'title': form.title.data,
            'initialDate': initial_date,
            'finalDate': final_date,
            'hour': form.hour.data,
            'link': form.link.data
        }

        dao.find_one_and_update(None, {
            '$push': {'events': new_event}
        })

        return redirect(
            url_for(
                'crud_events.add_events',
                success_msg='Evento adicionado adicionado com sucesso.'
            )
        )

    return render_template(
        'admin/add_events.html',
        form=form,
        success_msg=request.args.get('success_msg')
    )

@crud_events.route('/editar_evento/', methods=['GET', 'POST'])
@login_required
def edit_events():
    """Render a view for editing events."""

    form = CalendarForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.calendar_dao()
    json = pfactory.calendar_dao().find_one()
    json = dict(json)
    json = dumps(json)
    index = str(form.index.data)

    if form.validate_on_submit() and form.create.data:
        initial_date = datetime.datetime.combine(form.initial_date.data, datetime.datetime.min.time())
        if form.final_date.data != "":
            final_date = datetime.datetime.strptime(form.final_date.data, '%d/%m/%Y')
            final_date = datetime.datetime.combine(final_date, datetime.datetime.min.time())
        else:
            final_date = form.final_date.data
        new_event = {
            'title': form.title.data,
            'initialDate': initial_date,
            'finalDate': final_date,
            'hour': form.hour.data,
            'link': form.link.data
        }

        dao.find_one_and_update(None, {
            '$set': {'events.' + index : new_event}
        })

        return redirect(
            url_for(
                'crud_events.edit_events',
                events=json,
                success_msg='Evento editado com sucesso.'
            )
        )

    return render_template(
        'admin/edit_events.html',
        events=json,
        form=form,
        success_msg=request.args.get('success_msg')
    )


@crud_events.route('/deletar_evento/', methods=['GET', 'POST'])
@login_required
def delete_events():
    """Render a view for deleting events."""

    form = CalendarForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.calendar_dao()
    json = pfactory.calendar_dao().find_one()
    json = dict(json)
    json = dumps(json)

    if form.validate_on_submit() and form.create.data:
        index = str(form.index.data)
        dao.find_one_and_update(None, {
            '$set': {'events.' + index + '.deleted' : ""}
        })

        return redirect(
            url_for(
                'crud_events.delete_events',
                events=json,
                success_msg='Evento deletado com sucesso.'
            )
        )

    return render_template(
        'admin/delete_events.html',
        events=json,
        form=form,
        success_msg=request.args.get('success_msg')
    )

