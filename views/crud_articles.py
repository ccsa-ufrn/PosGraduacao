"""
Routes and views for articles CRUD.
"""

from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request

from models.factory import PosGraduationFactory

from settings.extensions import ExtensionsManager

from views.forms.content import ArticleForm

from bson.json_util import dumps
import json

crud_articles = Blueprint('crud_articles', __name__, url_prefix='/admin')

@crud_articles.route('/add_artigo/', methods=['GET', 'POST'])
@login_required
def add_article():
    """
    Render a article adding form
    """

    form = ArticleForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.publications_dao()

    if form.validate_on_submit() and form.create.data:
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
            '$push': {'articles': new_article}
        })

        return redirect(
            url_for(
                'crud_articles.add_article',
                success_msg='Novo artigo adicionado com sucesso.'
            )
        )

    return render_template(
        'admin/add_article.html',
        form=form,
        success_msg=request.args.get('success_msg')
    )

@crud_articles.route('/editar_artigo/', methods=['GET', 'POST'])
@login_required
def edit_article():
    """
    Render a article editing form
    """

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
                'crud_articles.edit_article',
                success_msg='Livro editado com sucesso.'))

    return render_template(
        'admin/edit_articles.html',
        publications=json,
        form=form,
        success_msg=request.args.get('success_msg')
    )


@crud_articles.route('/deletar_artigo/', methods=['GET', 'POST'])
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
                'crud_articles.delete_article',
                success_msg='Arigo deletado com sucesso.'))

    return render_template(
        'admin/delete_articles.html',
        publications=json,
        form=form,
        success_msg=request.args.get('success_msg')
    )
