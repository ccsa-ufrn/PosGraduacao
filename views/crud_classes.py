"""
Routes and views for book CRUD.
"""

from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request

from models.factory import PosGraduationFactory

from settings.extensions import ExtensionsManager


from bson.json_util import dumps
import json
import datetime
import sys

crud_classes = Blueprint('crud_classes', __name__, url_prefix='/admin')

@crud_classes.route('/add_primeira_turma/', methods=['GET', 'POST'])
@login_required
def add_first_class():

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.classes_database_dao()
    now = datetime.datetime.now()
    if now.month <= 7:
        semester = 1
    else:
        semester = 2
    classes=pfactory.classes_dao(now.year,semester,100).find()
    dao.find_one_and_update(None, {
        '$set': { 'firstClasses': classes}
    })

    return redirect(
        url_for(
            'admin.index',
            success_msg='Primeiras turmas modificadas com sucesso.'
        )
    )
    

