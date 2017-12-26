"""
Routes and views for system administration pages.
"""
import os
import glob
import sys

from flask_login import LoginManager, \
    login_user, login_required, logout_user, current_user
from flask import Blueprint, render_template, redirect, url_for, request

from bson.objectid import ObjectId

from werkzeug.utils import secure_filename

from models.factory import PosGraduationFactory
from models.users import User

from settings.extensions import ExtensionsManager

from views.forms.auth import LoginForm
from views.forms.content import ParticipationsInEventsForm, \
    ScheduledReportForm, InstitutionsWithCovenantsForm, \
    DocumentForm, SubjectsForm, ProfessorForm, StaffForm, CalendarForm, \
    EditInstitutionsWithCovenantsForm, EditDocumentForm

from models.clients.api_sistemas import SigaaError, \
    FailedToGetTokenForSigaaError, UnreachableSigaaError, \
    NoAppCredentialsForSigaaError

from bson.json_util import dumps
import json
import requests

import datetime

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

###############################################################################
#Adicionar deletar e editar defesas de teses e dissertações
###############################################################################

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

    if form.validate_on_submit() and form.create.data:
        index = str(form.index.data)
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

    if form.validate_on_submit():
        index = str(form.index.data)
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


###############################################################################
#Adicionar deletar e editar membros da equipe de servidores
###############################################################################



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

###############################################################################
#Adicionar deletar e editar intercâmbios
###############################################################################

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

    if form.validate_on_submit() and form.create.data:
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

###############################################################################
#Adicionar deletar e editar eventos
###############################################################################

@APP.route('/add_evento/', methods=['GET', 'POST'])
@login_required
def add_events():
    """Render a view for adding events."""

    form = CalendarForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.calendar_dao()
    
    if form.validate_on_submit():
        initial_date = datetime.datetime.combine(form.initial_date.data, datetime.datetime.min.time())
        if form.final_date.data != "":
            final_date = datetime.datetime.strptime(form.final_date.data, '%d/%m/%Y')
            final_date = datetime.datetime.combine(final_date, datetime.datetime.min.time())
        else:
            final_date = form.final_date.data
        new_event = {
            'title': form.title.data,
            'initialDate': initial_date,
            'finalDate': final_date,
            'hour': form.hour.data,
            'link': form.link.data
        }

        dao.find_one_and_update(None, {
            '$push': {'events': new_event}
        })

        return redirect(
            url_for(
                'admin.add_events',
                success_msg='Evento adicionado adicionado com sucesso.'
            )
        )

    return render_template(
        'admin/add_events.html',
        form=form,
        success_msg=request.args.get('success_msg')
    )

@APP.route('/editar_evento/', methods=['GET', 'POST'])
@login_required
def edit_events():
    """Render a view for editing events."""

    form = CalendarForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.calendar_dao()
    json = pfactory.calendar_dao().find_one()
    json = dict(json)
    json = dumps(json)
    index = str(form.index.data)

    if form.validate_on_submit() and form.create.data:
        initial_date = datetime.datetime.combine(form.initial_date.data, datetime.datetime.min.time())
        if form.final_date.data != "":
            final_date = datetime.datetime.strptime(form.final_date.data, '%d/%m/%Y')
            final_date = datetime.datetime.combine(final_date, datetime.datetime.min.time())
        else:
            final_date = form.final_date.data
        new_event = {
            'title': form.title.data,
            'initialDate': initial_date,
            'finalDate': final_date,
            'hour': form.hour.data,
            'link': form.link.data
        }

        dao.find_one_and_update(None, {
            '$set': {'events.' + index : new_event}
        })

        return redirect(
            url_for(
                'admin.edit_events',
                events=json,
                success_msg='Evento editado com sucesso.'
            )
        )

    return render_template(
        'admin/edit_events.html',
        events=json,
        form=form,
        success_msg=request.args.get('success_msg')
    )


@APP.route('/deletar_evento/', methods=['GET', 'POST'])
@login_required
def delete_events():
    """Render a view for deleting events."""

    form = CalendarForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.calendar_dao()
    json = pfactory.calendar_dao().find_one()
    json = dict(json)
    json = dumps(json)

    if form.validate_on_submit() and form.create.data:
        index = str(form.index.data)
        dao.find_one_and_update(None, {
            '$set': {'events.' + index + '.deleted' : ""}
        })

        return redirect(
            url_for(
                'admin.delete_events',
                events=json,
                success_msg='Evento deletado com sucesso.'
            )
        )

    return render_template(
        'admin/delete_events.html',
        events=json,
        form=form,
        success_msg=request.args.get('success_msg')
    )



###############################################################################
#Adicionar deletar e editar professores(Não finalizado)
###############################################################################


@APP.route('/add_professors/', methods=['GET', 'POST'])
@login_required
def add_professors():
    """Render a view for professors."""

    form = ProfessorForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.boards_of_professors_dao()

    if form.validate_on_submit() and form.create.data:
        new_professor = {
            'name': form.name.data,
            'rank': form.rank.data,
            'lattes': form.lattes.data,
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

@APP.route('/editar_professors/', methods=['GET', 'POST'])
@login_required
def edit_professors():
    """Render a view for editing professors."""

    form = ProfessorForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.boards_of_professors_dao()
    json = pfactory.boards_of_professors_dao().find_one()
    json = dict(json)
    json = dumps(json)

    if form.validate_on_submit() and form.create.data:
        index = str(form.index.data)
        new_professor = {
            'name': form.name.data,
            'rank': form.rank.data,
            'lattes': form.lattes.data,
            'email': form.email.data
        }

        dao.find_one_and_update(None, {
            '$set': {'professors.' + index : new_professor}
        })

        return redirect(
            url_for(
                'admin.edit_professors',
                professors=json,
                success_msg='Professor editado com sucesso.'
            )
        )

    return render_template(
        'admin/edit_professors.html',
        form=form,
        professors=json,
        success_msg=request.args.get('success_msg')
    )

@APP.route('/deletar_professors/', methods=['GET', 'POST'])
@login_required
def delete_professors():
    """Render a view for deleting professors."""

    form = ProfessorForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.boards_of_professors_dao()
    json = pfactory.boards_of_professors_dao().find_one()
    json = dict(json)
    json = dumps(json)

    if form.validate_on_submit() and form.create.data:
        index = str(form.index.data)
        dao.find_one_and_update(None, {
            '$set': {'professors.' + index + '.deleted'  : ""}
        })

        return redirect(
            url_for(
                'admin.delete_professors',
                professors=json,
                success_msg='Professor deletado com sucesso.'
            )
        )

    return render_template(
        'admin/delete_professors.html',
        form=form,
        professors=json,
        success_msg=request.args.get('success_msg')
    )





###############################################################################
#Adicionar deletar e editar convênios(Não finalizado)
###############################################################################

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
            if filename.count('.') > 1:
                return redirect(
                    url_for(
                        'admin.covenants',
                        success_msg='Nome da logo contem mais de um . por favor corrija isso'
                    )
                )
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
        form=form,
        success_msg=request.args.get('success_msg')
    )

@APP.route('/deletar_convenios/', methods=['GET', 'POST'])
@login_required
def delete_covenants():
    """Render covenant deleting form."""

    form = EditInstitutionsWithCovenantsForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.integrations_infos_dao()
    json = pfactory.integrations_infos_dao().find_one()
    json = dict(json)
    json = dumps(json)

    if form.validate_on_submit() and form.create.data:
        index = str(form.index.data)
        dao.find_one_and_update(None, {
            '$set': {'institutionsWithCovenant.' + index + '.deleted' : ""}
        })
        return redirect(
            url_for(
                'admin.delete_covenants',
                integrations=json,
                success_msg='Convênio deletado com sucesso.'
            )
        )

    return render_template(
        'admin/delete_covenants.html',
        form=form,
        integrations=json,
        success_msg=request.args.get('success_msg')
    )

@APP.route('/editar_convenios/', methods=['GET', 'POST'])
@login_required
def edit_covenants():
    """Render covenant editing form."""

    allowed_extensions = ['jpg', 'png']

    form = EditInstitutionsWithCovenantsForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.integrations_infos_dao()
    json = pfactory.integrations_infos_dao().find_one()
    json = dict(json)
    json = dumps(json)

    if form.validate_on_submit() and form.create.data:
        index = str(form.index.data)
        if form.logo.data and allowedFile(form.logo.data.filename, allowed_extensions):
            photo = form.logo.data
            path = os.path.normpath("static/assets")
            filename = secure_filename(photo.filename)
            if filename.count('.') > 1:
                return redirect(
                    url_for(
                        'admin.edit_covenants',
                        integrations=json,
                        success_msg='Nome da logo contem mais de um . por favor corrija isso'
                    )
                )
            name, extension = filename.split('.')
            logoFile = 'logo-' + form.initials.data.lower() + '.' + extension
            uploadFiles(photo, path, logoFile)
            new_covenant = {
                'name': form.name.data,
                'initials': form.initials.data.upper(),
                'logoFile': logoFile
            }

            dao.find_one_and_update(None, {
                '$set': {'institutionsWithCovenant.' + index : new_covenant}
            })
        else:
            new_covenant = {
                'name': form.name.data,
                'initials':form.initials.data.upper()
            }

            dao.find_one_and_update(None, {
                '$set' : {'institutionsWithCovenant.' + index : new_covenant}
            })

        return redirect(
            url_for(
                'admin.edit_covenants',
                integrations=json,
                success_msg='Convênio editado com sucesso.'
            )
        )


    return render_template(
        'admin/edit_covenants.html',
        form=form,
        integrations=json,
        success_msg=request.args.get('success_msg')
    )

###############################################################################
#Adicionar deletar e editar documentos
###############################################################################

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
                'category': form.category.data,
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

@APP.route('/deletar_documentos/', methods=['GET', 'POST'])
@login_required
def delete_documents():
    """Render document deleting form."""

    form = EditDocumentForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.official_documents_dao()
    json = pfactory.official_documents_dao().find()
    json = list(json)
    json = dumps(json)

    if form.validate_on_submit() and form.create.data:
        dao.find_one_and_update({'_id' : ObjectId(form.document_id.data)}, {
            '$set' : {'deleted' : ''}})
        return redirect(
            url_for(
                'admin.delete_documents',
                success_msg='Documento deletado com sucesso.'
            )
        )
        
    return render_template(
        'admin/delete_documents.html',
        documents=json,
        form=form,
        success_msg=request.args.get('success_msg')
    )


@APP.route('/editar_documentos/', methods=['GET', 'POST'])
@login_required
def edit_documents():
    """Render document editing form."""

    allowed_extensions = ['docx', 'pdf']

    form = EditDocumentForm()

    pfactory = PosGraduationFactory(current_user.pg_initials)
    dao = pfactory.official_documents_dao()
    ownerProgram = pfactory.mongo_id
    json = pfactory.official_documents_dao().find()
    json = list(json)
    json = dumps(json)

    if form.validate_on_submit() and form.create.data:
        document_id = form.document_id.data
        if form.document.data:
            if allowedFile(form.document.data.filename, allowed_extensions):
                insertedOn = datetime.datetime.now()
                insertedBy = current_user._full_name
                document = form.document.data
                path = os.path.normpath("static/upload_files/" + current_user.pg_initials.lower())
                filename = uploadFiles(document, path, document.filename)
                new_document = {
                    'title': form.title.data,
                    'cod': form.cod.data,
                    'file': filename,
                    'insertedBy': insertedBy,
                    'insertedOn': insertedOn
                }

                dao.find_one_and_update({'_id' : ObjectId(form.document_id.data)}, {
                    '$set' : new_document
                })
            else:
                return redirect(
                    url_for(
                        'admin.edit_documents',
                        success_msg='Tipo de documento inválido'
                    )
                )

        else:
            new_document = {
                'title':form.title.data,
                'cod': form.cod.data
            }
            dao.find_one_and_update({'_id' : ObjectId(form.document_id.data)}, {
                '$set' : new_document
            })

        return redirect(
            url_for(
                'admin.edit_documents',
                success_msg='Documento editado com sucesso.'
            )
        )

    return render_template(
        'admin/edit_documents.html',
        documents=json,
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
