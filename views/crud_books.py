"""
Routes and views for book CRUD.
"""

from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request

from models.factory import PosGraduationFactory

from settings.extensions import ExtensionsManager

from views.forms.content import BookForm, ChapterForm

from bson.json_util import dumps
import json
import sys

crud_books = Blueprint('crud_books', __name__, url_prefix='/admin')

@crud_books.route('/add_livro/', methods=['GET', 'POST'])
@login_required
def add_book():
    """
    Render a book adding form
    """

    form = BookForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.publications_dao()

    if form.validate_on_submit() and form.create.data:
        new_book = {
            'title': form.title.data,
            'subtitle': form.subtitle.data,
            'authors': form.authors.data,
            'edition': form.edition.data,
            'location': form.location.data,
            'publisher': form.publisher.data,
            'year': form.year.data
        }

        dao.find_one_and_update(None, {
            '$push': {'books': new_book}
        })

        return redirect(
            url_for(
                'crud_books.add_book',
                success_msg='Novo livro adicionado com sucesso.'
            )
        )

    return render_template(
        'admin/add_book.html',
        form=form,
        success_msg=request.args.get('success_msg')
    )

@crud_books.route('/editar_livro/', methods=['GET', 'POST'])
@login_required
def edit_book():
    """
    Render a book editing form
    """

    form = BookForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.publications_dao()
    json = pfactory.publications_dao().find_one()
    json = dict(json)
    json = dumps(json)

    if form.validate_on_submit() and form.create.data:
        index = str(form.index.data)
        new_book = {
            'title': form.title.data,
            'subtitle': form.subtitle.data,
            'authors': form.authors.data,
            'edition': form.edition.data,
            'location': form.location.data,
            'publisher': form.publisher.data,
            'year': form.year.data
        }

        dao.find_one_and_update(None, {
            '$set': {'books.' + index : new_book}
        })

        return redirect(
            url_for(
                'crud_books.edit_book',
                success_msg='Livro editado com sucesso.'))

    return render_template(
        'admin/edit_books.html',
        publications=json,
        form=form,
        success_msg=request.args.get('success_msg')
    )

@crud_books.route('/deletar_livro/', methods=['GET', 'POST'])
@login_required
def delete_book():
    """
    Render a book deleting form
    """

    form = BookForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.publications_dao()
    json = pfactory.publications_dao().find_one()
    json = dict(json)
    json = dumps(json)

    if form.validate_on_submit() and form.create.data:
        index = str(form.index.data)
        dao.find_one_and_update(None, {
            '$set': {'books.' + index + '.deleted' : ''}
        })

        return redirect(
            url_for(
                'crud_books.delete_book',
                success_msg='Livro deletado com sucesso.'))

    return render_template(
        'admin/delete_books.html',
        publications=json,
        form=form,
        success_msg=request.args.get('success_msg')
    )

@crud_books.route('/add_capitulo/', methods=['GET', 'POST'])
@login_required
def add_chapter():
    """
    Render a chapter in book adding form
    """

    pfactory = PosGraduationFactory(current_user.pg_initials)
    form = ChapterForm()

    dao = pfactory.publications_dao()

    if form.validate_on_submit() and form.create.data:
        new_chapter = {
            'bookTitle': form.book_title.data,
            'bookAuthors': form.book_authors.data,
            'chapterTitle': form.chapter_title.data,
            'chapterAuthors': form.chapter_authors.data,
            'edition': form.edition.data,
            'location': form.location.data,
            'publisher': form.publisher.data,
            'pages': form.pages.data,
            'year': form.year.data
        }

        dao.find_one_and_update(None, {
            '$push': {'chapters': new_chapter}
        })

        return redirect(
            url_for(
                'crud_books.add_chapter',
                success_msg='Novo capitulo adicionado com sucesso.'
            )
        )

    return render_template(
        'admin/add_chapter.html',
        form=form,
        success_msg=request.args.get('success_msg')
    )

@crud_books.route('/editar_capitulo/', methods=['GET', 'POST'])
@login_required
def edit_chapter():
    """
    Render a chapter editing form
    """

    form = ChapterForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.publications_dao()
    publications = pfactory.publications_dao().find_one()
    publications = dict(publications)
    publications = dumps(publications)

    if form.validate_on_submit() and form.create.data:
        index = str(form.index.data)
        new_chapter = {
            'bookTitle': form.book_title.data,
            'bookAuthors': form.book_authors.data,
            'chapterTitle': form.chapter_title.data,
            'chapterAuthors': form.chapter_authors.data,
            'edition': form.edition.data,
            'location': form.location.data,
            'publisher': form.publisher.data,
            'pages': form.pages.data,
            'year': form.year.data
        }

        dao.find_one_and_update(None, {
            '$set': {'chapters.' + index : new_chapter}
        })

        return redirect(
            url_for(
                'crud_books.edit_chapter',
                success_msg='Capítulo editado com sucesso.'))

    return render_template(
        'admin/edit_chapters.html',
        publications=publications,
        form=form,
        success_msg=request.args.get('success_msg')
    )

@crud_books.route('/deletar_capitulo/', methods=['GET', 'POST'])
@login_required
def delete_chapter():
    """
    Render a chapter delete form
    """

    form = ChapterForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.publications_dao()
    publications = pfactory.publications_dao().find_one()
    publications = dict(publications)
    publications = dumps(publications)

    if form.validate_on_submit() and form.create.data:
        index = str(form.index.data)
        dao.find_one_and_update(None, {
            '$set': {'chapters.' + index + '.deleted' : ''}
        })

        return redirect(
            url_for(
                'crud_books.delete_chapter',
                success_msg='Capítulo deletado com sucesso.'))

    return render_template(
        'admin/delete_chapters.html',
        publications=publications,
        form=form,
        success_msg=request.args.get('success_msg')
    )
