"""
Routes and views for articles CRUD.
"""

from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, jsonify

import sys

from models.factory import PosGraduationFactory

from settings.extensions import ExtensionsManager

from views.forms.content import StudentCoordinatorForm
from bson.json_util import dumps
from bson.objectid import ObjectId
import json

crud_students = Blueprint('crud_students', __name__, url_prefix='/admin')

@crud_students.route('/coordenadores/', methods=['GET', 'POST'])
@login_required
def view_student():

    form = StudentCoordinatorForm()
    pfactory = PosGraduationFactory(current_user.pg_initials)
    students, courses = mergeDicts(pfactory)
    return render_template(
        'admin/add_student_coordinator.html',
        form=form,
        students=students,
        courses=courses,
        crud_type=request.args.get('crud_type'),
        success_msg=request.args.get('success_msg')
    )
@crud_students.route('/editar_coordenador/', methods=['GET', 'POST'])
@login_required
def coordinator():

    form = StudentCoordinatorForm()
    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.coordinators_dao()
    ownerProgram = pfactory.mongo_id
    if form.validate_on_submit():
        new_coordinator = {
            'coordinator' : form.coordinator.data,
            'registration' : form.registration.data,
            'ownerProgram' : ownerProgram 
        }
        if dao.find_one({'registration': int(form.registration.data)}) is not None:
            dao.find_one_and_update({'registration': form.registration.data}, {'$set': new_coordinator})
        else:
            dao.insert_one(None, new_coordinator)
        return jsonify(mergeDicts(pfactory))
    else:
        return jsonify({'error':'Houve um erro'})

def mergeDicts(pfactory):
    students = pfactory.students_dao()
    coordinators = pfactory.coordinators_dao()
    coordinators = list(coordinators.find())
    students_list = []
    course_list = []
    for course in students.keys():
        for student in students[course]:
            for coordinator in coordinators:
                if student['class'] == str(coordinator['registration']):
                    student['coordinator'] = coordinator['coordinator']
            if 'coordinator' not in student.keys():
                student['coordinator'] = 'Sem coordenador(a)'
        course_list.append(course)
        students_list.append(students[course])
    students = dumps(students_list)
    course_list = dumps(course_list)
    return students, course_list
