"""
Routes and views for system administration pages.
"""
import os
import sys
import datetime
import glob

from flask_login import LoginManager, \
    login_user, login_required, logout_user, current_user
from flask import Blueprint, render_template, redirect, url_for, request

from werkzeug.utils import secure_filename

from models.factory import PosGraduationFactory
from models.users import User

from settings.extensions import ExtensionsManager

from views.forms.auth import LoginForm
from views.forms.content import ParticipationsInEventsForm, \
    ScheduledReportForm, InstitutionsWithCovenantsForm, \
    DocumentForm, SubjectsForm, ProfessorForm, StaffForm

from models.clients.api_sistemas import SigaaError, \
    FailedToGetTokenForSigaaError, UnreachableSigaaError, \
    NoAppCredentialsForSigaaError

from bson.json_util import dumps
import json
import requests

APP = Blueprint('admin',
                __name__,
                static_folder='static',
                url_prefix='/admin')


@APP.route('/')
def index():
    """
    If user is already authenticated, render its
    dashboard, otherwise ask for his password.
    """
    if current_user and current_user.is_authenticated:

        pfactory = PosGraduationFactory(current_user.pg_initials)
        post_graduation = pfactory.post_graduation

        return render_template(
            'admin/index.html',
            post_graduation=post_graduation
        )

    else:
        return login()


@APP.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Render an user authorization form.
    """
    form = LoginForm()

    if form.validate_on_submit():
        user_attempting = User.get(form.nick.data)

        if (user_attempting is not None) and (user_attempting.authenticate(form.nick.data, form.password.data)):
            login_user(user_attempting)
            return index()
        else:
            return render_template(
                'admin/login.html',
                form=form,
                incorrect_attempt=True
            )
    else:
        return render_template(
            'admin/login.html',
            form=form,
            incorrect_attempt=False
        )


@APP.route('/logout/')
@login_required
def logout():
    """
    Render a logged out page.
    """

    logout_user()

    return render_template(
        'admin/logout.html'
    )


@ExtensionsManager.login_manager.user_loader
def user_loader(user_id):
    """Load an user from database,
    using an user_id string formatted like 'user_nick@program_initials'."""
    if user_id is not None:
        return User.get(
            user_id,
            authenticated=True
        )
    else:
        return None


@APP.route('/apresentacoes/', methods=['GET', 'POST'])
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
                'admin.scheduled_reports',
                success_msg='Defesa de tese adicionada com sucesso.'
            )
        )

    return render_template(
        'admin/scheduled_reports.html',
        form=form,
        success_msg=request.args.get('success_msg')
    )

@APP.route('/deletar_agendamento/', methods=['GET', 'POST'])
@login_required
def delete_scheduled_reports():

    form = ScheduledReportForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.final_reports_dao()
    json = pfactory.final_reports_dao().find_one()
    json = dict(json)

    json = dumps(json)
    index = str(form.index.data)

    if form.validate_on_submit():
        dao.find_one_and_update(None, {
            '$set': {'scheduledReports.' + index + '.deleted' : ""}
        })
        return redirect(
            url_for(
                'admin.delete_scheduled_reports',
                final_reports=json,
                success_msg='Documento deletado com sucesso'
            )
        )

    return render_template(
        'admin/delete_scheduled_reports.html',
        final_reports=json,
        form=form,
        post_graduation=current_user.pg_initials,
        success_msg=request.args.get('success_msg')
    )

@APP.route('/editar_agendamento/', methods=['GET', 'POST'])
@login_required
def edit_scheduled_reports():

    form = ScheduledReportForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.final_reports_dao()
    json = pfactory.final_reports_dao().find_one()
    json = dict(json)
    json = dumps(json, ensure_ascii=False)
    index = str(form.index.data)

    if form.validate_on_submit():
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
                'admin.edit_scheduled_reports',
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


@APP.route('/add_disciplinas/', methods=['GET', 'POST'])
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

        condition = {'title': form.requirement.data}

        dao.find_one_and_update(condition, {
            '$push': {'subjects': new_subject}
        })

        return redirect(
            url_for(
                'admin.subjects',
                success_msg='Disciplina adicionada com sucesso.'
            )
        )

    return render_template(
        'admin/subjects.html',
        form=form,
        success_msg=request.args.get('success_msg')
    )

@APP.route('/deletar_disciplinas/', methods=['GET', 'POST'])
@login_required
def delete_subjects():
    """
    Render a delete subject form.
    """

    form = SubjectsForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.grades_of_subjects_dao()
    json = pfactory.grades_of_subjects_dao().find()
    json = list(json)
    json = dumps(json)
    index = str(form.index.data)

    if form.validate_on_submit():
        dao.find_one_and_update({'title': form.requirement.data}, {
            '$set': {'subjects.' + index + '.deleted' : ""}
        })

        return redirect(
            url_for(
                'admin.delete_subjects',
                subjects=json,
                success_msg='Disciplina deletada com sucesso'
            )
        )
    return render_template(
        'admin/delete_subjects.html',
        form=form,
        subjects=json,
        success_msg=request.args.get('success_msg')
    )

@APP.route('/editar_disciplinas/', methods=['GET', 'POST'])
@login_required
def edit_subjects():
    """
    Render an edit subject form.
    """

    form = SubjectsForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.grades_of_subjects_dao()
    json = pfactory.grades_of_subjects_dao().find()
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

        condition = {'title': form.requirement.data}

        dao.find_one_and_update(condition, {
            '$set': {'subjects.' + index : new_subject}
        })

        return redirect(
            url_for(
                'admin.edit_subjects',
                subjects=json,
                success_msg='Disciplina editada com sucesso',
            )
        )
    return render_template(
        'admin/edit_subjects.html',
        form=form,
        subjects=json,
        success_msg=request.args.get('success_msg')
    )



@APP.route('/add_servidor/', methods=['GET', 'POST'])
@login_required
def add_staff():
    """
    Render a subject form.
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
                'admin.add_staff',
                success_msg='Servidor adicionado com sucesso.'
                )
        )

    return render_template(
        'admin/add_staff.html',
        form=form,
        success_msg=request.args.get('success_msg')
    )

@APP.route('/editar_servidor/', methods=['GET', 'POST'])
@login_required
def edit_staff():
    """
    Render a subject form.
    """

    form = StaffForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.boards_of_staffs_dao()
    json = pfactory.boards_of_staffs_dao().find_one()
    json = dict(json)
    json = dumps(json)
    index = '.' + str(form.index.data)

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
            '$set': {form.function.data + index: new_staff}
            })
        return redirect(
            url_for(
                'admin.edit_staff',
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


@APP.route('/deletar_servidor/', methods=['GET', 'POST'])
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
                'admin.delete_staff',
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



@APP.route('/intercambios/', methods=['GET', 'POST'])
@login_required
def participations():
    """Render a view for integrations lists."""

    form = ParticipationsInEventsForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.integrations_infos_dao()

    if form.validate_on_submit() and form.create.data:
        new_participation = {
            'title': form.title.data,
            'description': form.description.data,
            'year': form.year.data,
            'international': form.location.data
        }

        dao.find_one_and_update(None, {
            '$push': {'participationsInEvents': new_participation}
        })

        return redirect(
            url_for(
                'admin.participations',
                success_msg='Intercâmbio adicionado adicionado com sucesso.'
            )
        )

    return render_template(
        'admin/participations.html',
        form=form,
        success_msg=request.args.get('success_msg')
    )

@APP.route('/deletar_intercâmbio/', methods=['GET', 'POST'])
@login_required
def delete_participations():
    """
    Render a delete participation form.
    """

    form = ParticipationsInEventsForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.integrations_infos_dao()
    json = pfactory.integrations_infos_dao().find_one()
    json = dict(json)
    json = dumps(json)
    index = str(form.index.data)


    if form.validate_on_submit():
        dao.find_one_and_update(None , {
            '$set': {'participationsInEvents.' + index + '.deleted' : ""}
        })

        return redirect(
            url_for(
                'admin.delete_participations',
                participations=json,
                success_msg='Participação deletada com sucesso'
            )
        )
    return render_template(
        'admin/delete_participations.html',
        form=form,
        participations=json,
        success_msg=request.args.get('success_msg')
    )

@APP.route('/editar_intercâmbio/', methods=['GET', 'POST'])
@login_required
def edit_participations():
    """
    Render a edit participation form.
    """

    form = ParticipationsInEventsForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.integrations_infos_dao()
    json = pfactory.integrations_infos_dao().find_one()
    json = dict(json)
    json = dumps(json)
    index = str(form.index.data)

    if form.validate_on_submit():
        year = int(form.year.data)
        new_participation = {
            'title': form.title.data,
            'description': form.description.data,
            'year': year,
            'international': form.location.data
        }

        dao.find_one_and_update(None, {
            '$set': {'participationsInEvents.' + index : new_participation}
        })

        return redirect(
            url_for(
                'admin.edit_participations',
                participations=json,
                success_msg='Participação editada com sucesso'
            )
        )
    return render_template(
        'admin/edit_participations.html',
        form=form,
        participations=json,
        success_msg=request.args.get('success_msg')
    )


@APP.route('/add_professors/', methods=['GET', 'POST'])
@login_required
def add_professors():
    """Render a view for professors."""

    form = ProfessorForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.boards_of_professors_dao()

    if form.validate_on_submit() and form.create.data:
        lattes = form.lattes.data
        if lattes == "":
            lattes = None
        new_professor = {
            'name': form.name.data,
            'rank': form.rank.data,
            'lattes': lattes,
            'email': form.email.data
        }

        dao.find_one_and_update(None, {
            '$push': {'professors': new_professor}
        })

        return redirect(
            url_for(
                'admin.add_professors',
                success_msg='Professor adicionado adicionado com sucesso.'
            )
        )

    return render_template(
        'admin/add_professors.html',
        form=form,
        success_msg=request.args.get('success_msg')
    )

@APP.route('/convenios/', methods=['GET', 'POST'])
@login_required
def covenants():
    """Render covenant adding form."""

    allowed_extensions = ['jpg', 'png']

    form = InstitutionsWithCovenantsForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.integrations_infos_dao()

    if form.validate_on_submit() and form.create.data:
        if form.logo.data and allowedFile(form.logo.data.filename, allowed_extensions):
            photo = form.logo.data
            path = os.path.normpath("static/assets")
            filename = secure_filename(photo.filename)
            name, extension = filename.split('.')
            logoFile = 'logo-' + form.initials.data.lower() + '.' + extension
            uploadFiles(photo, path, logoFile)
            new_covenant = {
                'name': form.name.data,
                'initials': form.initials.data.upper(),
                'logoFile': logoFile
            }

        dao.find_one_and_update(None, {
            '$push': {'institutionsWithCovenant': new_covenant}
        })

        return redirect(
            url_for(
                'admin.covenants',
                success_msg='Convênio adicionado adicionado com sucesso.'
            )
        )


    return render_template(
        'admin/covenants.html',
        participations=dao.find_one()['institutionsWithCovenant'],
        form=form,
        success_msg=request.args.get('success_msg')
    )

@APP.route('/documentos/', methods=['GET', 'POST'])
@login_required
def documents():
    """Render document adding form."""

    allowed_extensions = ['docx', 'pdf']

    form = DocumentForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.official_documents_dao()
    ownerProgram = pfactory.mongo_id

    if form.validate_on_submit() and form.create.data:
        insertedOn = datetime.datetime.now()
        insertedBy = current_user._full_name
        document = form.document.data
        path = os.path.normpath("static/upload_files/" + current_user.pg_initials.lower())
        if allowedFile(document.filename, allowed_extensions):
            filename = uploadFiles(document, path, document.filename)
            new_document = {
                'ownerProgram': ownerProgram,
                'title': form.title.data,
                'cod': form.cod.data,
                'file': filename,
                'insertedOn': insertedOn,
                'insertedBy': insertedBy
            }

            dao.insert_one(None, new_document)

            return redirect(
                url_for(
                    'admin.documents',
                    success_msg='Documento adicionado adicionado com sucesso.'
                )
            )
        else:

            return redirect(
                url_for(
                    'admin.documents',
                    success_msg='',
                    invalid_type='Tipo de documento inválido'
                )
            )

    return render_template(
        'admin/documents.html',
        documents=dao.find_one(),
        form=form,
        success_msg=request.args.get('success_msg')
    )

def uploadFiles(document, path, filename):
    """3 functions, effectively upload files to server,
    if a file with the same name already exists, change filename
    to filename_x and also prevent not secure filenames ex: with / * etc
    """
    name, extension = (secure_filename(filename)).split('.')
    checkpath = os.path.join((os.getcwd()), path, os.path.normpath(name))
    if glob.glob(checkpath + '*.' + extension):
        numberofcopies = 0
        dirs = glob.glob(checkpath + '*.' + extension)
        for i in dirs:
            numberofcopies += 1
        filename = name + '_' + str(numberofcopies) + '_.' + extension
    filename = secure_filename(filename)
    document.save(os.path.join((os.getcwd()), path, os.path.normpath(filename)))
    return filename

def allowedFile(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

@APP.route('/401/')
@ExtensionsManager.login_manager.unauthorized_handler
def unauthorized():
    """Render page to be showed up for not logged in users."""
    return render_template('admin/401.html')


@APP.route('/404/')
@APP.errorhandler(404)
def page_not_found(error=None):
    """Render page not found error."""

    print(str(error))
    return render_template('admin/404.html',), 404


@APP.errorhandler(SigaaError)
def sigaa_exception_handler(error):
    """Render page for APISistemas errors. """
    print("ERROR for API Sistemas (" + repr(error) + "): " + str(error))

    if isinstance(error, UnreachableSigaaError):
        return render_template('admin/503.html',), 503

    if isinstance(error, FailedToGetTokenForSigaaError):
        return render_template('admin/501.html',), 501

    if isinstance(error, NoAppCredentialsForSigaaError):
        return render_template('admin/500.html',), 500
