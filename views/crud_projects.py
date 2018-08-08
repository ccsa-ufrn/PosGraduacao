"""
Routes and views for articles CRUD.
"""

from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, jsonify

import sys

from models.factory import PosGraduationFactory

from settings.extensions import ExtensionsManager

from views.forms.content import ProjectForm, MemberOfProjectForm 

from bson.json_util import dumps
from bson.objectid import ObjectId
import json

crud_projects = Blueprint('crud_projects', __name__, url_prefix='/admin')

@crud_projects.route('/add_projeto/', methods=['GET', 'POST'])
@login_required
def add_project():
    """Render project adding form."""

    form = ProjectForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.projects_database_dao()
    ownerProgram = pfactory.mongo_id

    if form.validate_on_submit() and form.create.data:
        new_project = {
            'ownerProgram': ownerProgram,
            'title': form.title.data,
            'subtitle': form.subtitle.data,
            'description': form.description.data,
            'situation': form.situation.data,
            'year': form.year.data,
            'email': form.email.data,
            'dt_init': form.dt_init.data,
            'dt_end': form.dt_end.data,
            'members' : []
        }

        dao.insert_one(None, new_project)

        return redirect(
            url_for(
                'crud_projects.add_project',
                success_msg='Projeto adicionado adicionado com sucesso.'
            )
        )
    return render_template(
        'admin/add_project.html',
        form=form,
        success_msg=request.args.get('success_msg')
    )

@crud_projects.route('/deletar_projeto/', methods=['GET', 'POST'])
@login_required
def delete_project():
    """Render project deleting form."""

    form = ProjectForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.projects_database_dao()
    projects = pfactory.projects_database_dao().find()
    projects = list(projects)
    projects = dumps(projects)
    if form.validate_on_submit() and form.create.data:
        dao.find_one_and_update({'_id' : ObjectId(form.project_id.data)}, {
            '$set' : {'deleted' : '' }})
        return redirect(
            url_for(
                'crud_projects.delete_project',
                success_msg='Projeto deletado com sucesso.'
            )
        )
    return render_template(
        'admin/delete_project.html',
        form=form,
        projects=projects,
        success_msg=request.args.get('success_msg')
    )

@crud_projects.route('/editar_projeto/', methods=['GET', 'POST'])
@login_required
def edit_project():
    """Render project editing form."""

    form = ProjectForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.projects_database_dao()
    projects = pfactory.projects_database_dao().find()
    projects = list(projects)
    projects = dumps(projects)
    if form.validate_on_submit() and form.create.data:
        new_project = {
            'title': form.title.data,
            'subtitle': form.subtitle.data,
            'description': form.description.data,
            'situation': form.situation.data,
            'year': form.year.data,
            'email': form.email.data,
            'dt_init': form.dt_init.data,
            'dt_end': form.dt_end.data
        }
        dao.find_one_and_update({'_id' : ObjectId(form.project_id.data)}, {
            '$set' : new_project})
        return redirect(
            url_for(
                'crud_projects.edit_project',
                success_msg='Projeto editado com sucesso.'
            )
        )
    return render_template(
        'admin/edit_projects.html',
        form=form,
        projects=projects,
        success_msg=request.args.get('success_msg')
    )

@crud_projects.route('/membros_de_projeto/', methods=['GET', 'POST'])
@login_required
def view_member():

    form = MemberOfProjectForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    projects = pfactory.projects_database_dao().find()
    projects = list(projects)
    projects = dumps(projects)
    if request.args.get('crud_type') == 'Adicionar':
        return render_template(
            'admin/add_member_in_project.html',
            form=form,
            projects=projects,
            crud_type=request.args.get('crud_type'),
            success_msg=request.args.get('success_msg')
        )
    if request.args.get('crud_type') == 'Deletar':
        return render_template(
            'admin/delete_member_in_project.html',
            form=form,
            projects=projects,
            crud_type=request.args.get('crud_type'),
            success_msg=request.args.get('success_msg')
        )
    else:
        return render_template(
            'admin/edit_member_in_project.html',
            form=form,
            projects=projects,
            crud_type=request.args.get('crud_type'),
            success_msg=request.args.get('success_msg')
        )
@crud_projects.route('/add_membro/', methods=['GET', 'POST'])
@login_required
def add_member():

    form = MemberOfProjectForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.projects_database_dao()
    projects = pfactory.projects_database_dao().find()
    projects = list(projects)
    projects = dumps(projects)
    if form.validate_on_submit():
        new_member = {
            'name' : form.name.data,
            'general_role' : form.general_role.data,
            'project_role' : form.project_role.data
        }
        dao.find_one_and_update({'_id' : ObjectId(form.project_id.data)}, {
            '$push': {'members': new_member}})
        projects = pfactory.projects_database_dao().find()
        projects = list(projects)
        projects = dumps(projects)
        return jsonify(projects=projects)
    else:
        return jsonify({'error':'Houve um erro'})

@crud_projects.route('/deletar_membro/', methods=['GET', 'POST'])
@login_required
def delete_member():

    form = MemberOfProjectForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.projects_database_dao()
    projects = pfactory.projects_database_dao().find()
    projects = list(projects)
    projects = dumps(projects)
    if form.validate_on_submit():
        index = str(form.index.data)
        dao.find_one_and_update({'_id' : ObjectId(form.project_id.data)}, {
            '$set': {'members.' + index + '.deleted' : '' }})
        projects = pfactory.projects_database_dao().find()
        projects = list(projects)
        projects = dumps(projects)
        return jsonify(projects=projects)
    else:
        return jsonify({'error':'Houve um erro'})

@crud_projects.route('/editar_membro/', methods=['GET', 'POST'])
@login_required
def edit_member():

    form = MemberOfProjectForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.projects_database_dao()
    projects = pfactory.projects_database_dao().find()
    projects = list(projects)
    projects = dumps(projects)
    if form.validate_on_submit():
        index = str(form.index.data)
        new_member = {
            'name' : form.name.data,
            'general_role' : form.general_role.data,
            'project_role' : form.project_role.data
        }
        dao.find_one_and_update({'_id' : ObjectId(form.project_id.data)}, {
            '$set': {'members.' + index : new_member}})
        projects = pfactory.projects_database_dao().find()
        projects = list(projects)
        projects = dumps(projects)
        return jsonify(projects=projects)
    else:
        return jsonify({'error':'Houve um erro'})
