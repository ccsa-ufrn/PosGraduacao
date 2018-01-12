"""
Routes and views for articles CRUD.
"""

from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, jsonify

import sys

from models.factory import PosGraduationFactory

from settings.extensions import ExtensionsManager

from views.forms.content import ArticleForm

from bson.json_util import dumps
import json

crud_projects = Blueprint('crud_projects', __name__, url_prefix='/admin')

@crud_projects.route('/add_projetos/', methods=['GET', 'POST'])
@login_required
def add_article():

    initials = ['PPGTUR','PPGA','PPGCC','PPGECO','PPGIC','PPGD','PPGSS','PPGP']
    for initial in initials:
        pfactory = PosGraduationFactory(initial)
        ownerProgram = pfactory.mongo_id
        dao = pfactory.projects_database_dao()
        result = pfactory.projects_dao().find()
        if result:
            for project in result:
                print(project, file=sys.stderr)
                print('\n', file=sys.stderr)
                project['ownerProgram'] = ownerProgram
                dao.insert_one(None, project)
    final_result = dao.find()
    return jsonify(final_result)

"""
@crud_projects.route('/editar_artigo/', methods=['GET', 'POST'])
@login_required
def edit_article():

    form = ArticleForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.publications_dao()
    json = pfactory.publications_dao().find_one()
    json = dict(json)
    json = dumps(json)

    if form.validate_on_submit() and form.create.data:
        index = str(form.index.data)
        new_article = {
            'title': form.title.data,
            'subtitle': form.subtitle.data,
            'authors': form.authors.data,
            'edition': form.edition.data,
            'location': form.location.data,
            'publisher': form.publisher.data,
            'number': form.number.data,
            'pages': form.pages.data,
            'date': form.date.data
        }

        dao.find_one_and_update(None, {
            '$set': {'articles.' + index : new_article}
        })

        return redirect(
            url_for(
                'crud_projects.edit_article',
                success_msg='Livro editado com sucesso.'))

    return render_template(
        'admin/edit_articles.html',
        publications=json,
        form=form,
        success_msg=request.args.get('success_msg')
    )


@crud_projects.route('/deletar_artigo/', methods=['GET', 'POST'])
@login_required
def delete_article():

    form = ArticleForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.publications_dao()
    json = pfactory.publications_dao().find_one()
    json = dict(json)
    json = dumps(json)

    if form.validate_on_submit() and form.create.data:
        index = str(form.index.data)
        dao.find_one_and_update(None, {
            '$set': {'articles.' + index + '.deleted' : ''}
        })

        return redirect(
            url_for(
                'crud_projects.delete_article',
                success_msg='Arigo deletado com sucesso.'))

    return render_template(
        'admin/delete_articles.html',
        publications=json,
        form=form,
        success_msg=request.args.get('success_msg')
    )
"""
