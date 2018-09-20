"""
Routes and views for articles CRUD.
"""

from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request

from models.factory import PosGraduationFactory

from settings.extensions import ExtensionsManager

from views.forms.content import NewsForm

from bson.json_util import dumps
import json
import string
import time 
import random

crud_news = Blueprint('crud_news', __name__, url_prefix='/admin')

@crud_news.route('/add_noticia/', methods=['GET', 'POST'])
@login_required
def add_news():
    """
    Render a news adding form
    """

    form = NewsForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.news_dao()

    if form.validate_on_submit() and form.create.data:
        id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        new_news = {
            'title': form.title.data,
            'headLine': form.headLine.data,
            'body': form.body.data,
            'id' : id,
            'date': time.strftime("%d/%m/%Y")
        }

        dao.find_one_and_update(None, {
            '$push': {'news': new_news}
        })

        return redirect(
            url_for(
                'crud_news.add_news',
                success_msg='Nova notícia adicionada com sucesso.'
            )
        )

    return render_template(
        'admin/add_news.html',
        form=form,
        success_msg=request.args.get('success_msg')
    )

@crud_news.route('/editar_noticia/', methods=['GET', 'POST'])
@login_required
def edit_news():

    form = NewsForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.news_dao()
    news = pfactory.news_dao().find_one()
    news = dict(news)
    news = dumps(news)

    if form.validate_on_submit() and form.create.data:
        index = str(form.index.data)

        dao.find_one_and_update(None, {
            '$set': {'news.' + index + '.title' : form.title.data}
        })

        dao.find_one_and_update(None, {
            '$set': {'news.' + index + '.headLine' : form.headLine.data}
        })

        dao.find_one_and_update(None, {
            '$set': {'news.' + index + '.body' : form.body.data}
        })

        return redirect(
            url_for(
                'crud_news.edit_news',
                success_msg='Notícia editada com sucesso.'))

    return render_template(
        'admin/edit_news.html',
        news=news,
        form=form,
        success_msg=request.args.get('success_msg')
    )

@crud_news.route('/deletar_noticia/', methods=['GET', 'POST'])
@login_required
def delete_news():

    form = NewsForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.news_dao()
    news = pfactory.news_dao().find_one()
    news = dict(news)
    news = dumps(news)

    if form.validate_on_submit() and form.create.data:
        index = str(form.index.data)
        dao.find_one_and_update(None, {
            '$set': {'news.' + index + '.deleted' : ''}
        })

        return redirect(
            url_for(
                'crud_news.delete_news',
                success_msg='Notícia deletada com sucesso.'))

    return render_template(
        'admin/delete_news.html',
        news=news,
        form=form,
        success_msg=request.args.get('success_msg')
    )
