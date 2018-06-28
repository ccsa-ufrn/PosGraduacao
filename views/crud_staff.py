"""
Routes and views for staff CRUD.
"""

from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request

from models.factory import PosGraduationFactory

from settings.extensions import ExtensionsManager

from views.forms.content import StaffForm

from bson.json_util import dumps
import json

crud_staff = Blueprint('crud_staff', __name__, url_prefix='/admin')

###############################################################################
#Adicionar deletar e editar membros da equipe de servidores
###############################################################################

@crud_staff.route('/add_servidor/', methods=['GET', 'POST'])
@login_required
def add_staff():
    """
    Render a staff form.
    """

    form = StaffForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.boards_of_staffs_dao()

    if form.validate_on_submit():
        if form.photo.data == '':
            photo = None
        else:
            photo = form.photo.data
        if form.function.data == 'coordination':
            new_staff = {
                'name': form.name.data,
                'rank': form.rank.data,
                'abstract': form.abstract.data,
                'photo': photo
            }

        else:
            new_staff = {
                'name': form.name.data,
                'function': {
                    'rank': form.rank.data,
                    'description': form.abstract.data
                },
                'photo': photo
            }
        dao.find_one_and_update(None, {
            '$push': {form.function.data: new_staff}
            })
        return redirect(
            url_for(
                'crud_staff.add_staff',
                success_msg='Servidor adicionado com sucesso.'
                )
        )

    return render_template(
        'admin/add_staff.html',
        form=form,
        success_msg=request.args.get('success_msg')
    )

@crud_staff.route('/editar_servidor/', methods=['GET', 'POST'])
@login_required
def edit_staff():
    """
    Render a staff form.
    """

    form = StaffForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.boards_of_staffs_dao()
    json = pfactory.boards_of_staffs_dao().find_one()
    json = dict(json)
    json = dumps(json)

    dao = pfactory.boards_of_staffs_dao()

    if form.validate_on_submit():
        index = '.' + str(form.index.data)
        if form.photo.data == '':
            photo = None
        else:
            photo = form.photo.data
        if form.function.data == 'coordination':
            new_staff = {
                'name': form.name.data,
                'rank': form.rank.data,
                'abstract': form.abstract.data,
                'photo': photo
            }

        else:
            new_staff = {
                'name': form.name.data,
                'function': {
                    'rank': form.rank.data,
                    'description': form.abstract.data
                },
                'photo': photo
            }
        dao.find_one_and_update(None, {
            '$set': {form.function.data + index: new_staff}
            })
        return redirect(
            url_for(
                'crud_staff.edit_staff',
                success_msg='Servidor editado com sucesso.',
                staff=json
                )
        )

    return render_template(
        'admin/edit_staff.html',
        form=form,
        success_msg=request.args.get('success_msg'),
        staff=json
    )


@crud_staff.route('/deletar_servidor/', methods=['GET', 'POST'])
@login_required
def delete_staff():
    """
    Render a delete staff form.
    """

    form = StaffForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.boards_of_staffs_dao()
    json = pfactory.boards_of_staffs_dao().find_one()
    json = dict(json)
    json = dumps(json)
    index = '.' + str(form.index.data)
    if form.validate_on_submit():
        dao.find_one_and_update(None, {
            '$set': {form.function.data + index + '.deleted' : ''}
            })
        return redirect(
            url_for(
                'crud_staff.delete_staff',
                success_msg='Servidor deletado com sucesso.',
                staff=json
                )
        )

    return render_template(
        'admin/delete_staff.html',
        form=form,
        success_msg=request.args.get('success_msg'),
        staff=json
    )

