"""
Routes and views for scheduled reports CRUD.
"""

from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request

from models.factory import PosGraduationFactory

from settings.extensions import ExtensionsManager

from views.forms.content import ScheduledReportForm

from bson.json_util import dumps
import json

crud_scheduled_reports = Blueprint('crud_scheduled_reports', __name__, url_prefix='/admin')

###############################################################################
#Adicionar deletar e editar defesas de teses e dissertações
###############################################################################

@crud_scheduled_reports.route('/apresentacoes/', methods=['GET', 'POST'])
@login_required
def scheduled_reports():
    """
    Render a report scheduling form.
    """

    form = ScheduledReportForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.final_reports_dao()

    if form.validate_on_submit():
        new_report = {
            'time': form.time.data,
            'title': form.title.data,
            'author': form.author.data,
            'location': form.location.data
        }

        dao.find_one_and_update(None, {
            '$push': {'scheduledReports': new_report}
        })

        return redirect(
            url_for(
                'crud_scheduled_reports.scheduled_reports',
                success_msg='Defesa de tese adicionada com sucesso.'
            )
        )

    return render_template(
        'admin/scheduled_reports.html',
        form=form,
        success_msg=request.args.get('success_msg')
    )

@crud_scheduled_reports.route('/deletar_agendamento/', methods=['GET', 'POST'])
@login_required
def delete_scheduled_reports():

    form = ScheduledReportForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.final_reports_dao()
    json = pfactory.final_reports_dao().find_one()
    json = dict(json)

    json = dumps(json)

    if form.validate_on_submit() and form.create.data:
        index = str(form.index.data)
        dao.find_one_and_update(None, {
            '$set': {'scheduledReports.' + index + '.deleted' : ""}
        })
        return redirect(
            url_for(
                'crud_scheduled_reports.delete_scheduled_reports',
                final_reports=json,
                success_msg='Agendamento deletado com sucesso'
            )
        )

    return render_template(
        'admin/delete_scheduled_reports.html',
        final_reports=json,
        form=form,
        post_graduation=current_user.pg_initials,
        success_msg=request.args.get('success_msg')
    )

@crud_scheduled_reports.route('/editar_agendamento/', methods=['GET', 'POST'])
@login_required
def edit_scheduled_reports():

    form = ScheduledReportForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.final_reports_dao()
    json = pfactory.final_reports_dao().find_one()
    json = dict(json)
    json = dumps(json, ensure_ascii=False)

    if form.validate_on_submit():
        index = str(form.index.data)
        new_report = {
            'time': form.time.data,
            'title': form.title.data,
            'author': form.author.data,
            'location': form.location.data
        }
        dao.find_one_and_update(None, {
            '$set': {'scheduledReports.' + index : new_report}
        })
        return redirect(
            url_for(
                'crud_scheduled_reports.edit_scheduled_reports',
                success_msg='Defesa de tese editada com sucesso.',
                final_reports=json
            )
        )

    return render_template(
        'admin/edit_scheduled_reports.html',
        final_reports=json,
        form=form,
        post_graduation=current_user.pg_initials,
        success_msg=request.args.get('success_msg')
    )

