"""
Routes and views for articles CRUD.
"""

from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request

from models.factory import PosGraduationFactory

from settings.extensions import ExtensionsManager

from views.forms.content import SubjectsForm

from bson.json_util import dumps
import json

crud_subjects = Blueprint('crud_subjects', __name__, url_prefix='/admin')

###############################################################################
#Adicionar deletar e editar disciplinas
###############################################################################


@crud_subjects.route('/add_disciplinas/', methods=['GET', 'POST'])
@login_required
def subjects():
    """
    Render a subject form.
    """

    form = SubjectsForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.grades_of_subjects_dao()

    if form.validate_on_submit():
        new_subject = {
            'name': form.name.data,
            'description': form.description.data,
            'workloadInHours': form.workload_in_hours.data,
            'credits': form.credits.data
        }

        condition = {'title': form.requirement.data, 'courseType' : request.args.get('course_type') }

        dao.find_one_and_update(condition, {
            '$push': {'subjects': new_subject}
        })

        return redirect(
            url_for(
                'crud_subjects.subjects',
                success_msg='Disciplina adicionada com sucesso.',
                course_type=request.args.get('course_type')
            )
        )

    return render_template(
        'admin/subjects.html',
        form=form,
        course_type=request.args.get('course_type')
    )

@crud_subjects.route('/deletar_disciplinas/', methods=['GET', 'POST'])
@login_required
def delete_subjects():
    """
    Render a delete subject form.
    """

    form = SubjectsForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.grades_of_subjects_dao()
    json = pfactory.grades_of_subjects_dao().find({'courseType' : request.args.get('course_type')})
    json = list(json)
    json = dumps(json)

    if form.validate_on_submit():
        index = str(form.index.data)
        dao.find_one_and_update({'title': form.requirement.data, 'courseType' : request.args.get('course_type')}, {
            '$set': {'subjects.' + index + '.deleted' : ""}
        })

        return redirect(
            url_for(
                'crud_subjects.delete_subjects',
                subjects=json,
                success_msg='Disciplina deletada com sucesso',
                course_type=request.args.get('course_type')
            )
        )
    return render_template(
        'admin/delete_subjects.html',
        form=form,
        subjects=json,
        success_msg=request.args.get('success_msg'),
        course_type=request.args.get('course_type')
    )

@crud_subjects.route('/editar_disciplinas/', methods=['GET', 'POST'])
@login_required
def edit_subjects():
    """
    Render an edit subject form.
    """

    form = SubjectsForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.grades_of_subjects_dao()
    json = pfactory.grades_of_subjects_dao().find({'courseType': request.args.get('course_type')})
    json = list(json)
    json = dumps(json)
    index = str(form.index.data)

    if form.validate_on_submit():
        new_subject = {
            'name': form.name.data,
            'description': form.description.data,
            'workloadInHours': form.workload_in_hours.data,
            'credits': form.credits.data
        }

        condition = {'title': form.requirement.data, 'courseType' : request.args.get('course_type')}

        dao.find_one_and_update(condition, {
            '$set': {'subjects.' + index : new_subject}
        })

        return redirect(
            url_for(
                'crud_subjects.edit_subjects',
                subjects=json,
                success_msg='Disciplina editada com sucesso',
                course_type=request.args.get('course_type')
            )
        )
    return render_template(
        'admin/edit_subjects.html',
        form=form,
        subjects=json,
        success_msg=request.args.get('success_msg'),
        course_type=request.args.get('course_type')
    )


