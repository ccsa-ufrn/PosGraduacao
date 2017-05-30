"""
Routes and views (actually, they're controllers!) for this flask application.
"""

from pymongo.errors import ServerSelectionTimeoutError
from flask import render_template, redirect
from Minerva import app

import Minerva.util.keyring as keyring
import Minerva.persistence.factory as factory
from Minerva.util.api_sistemas import SigaaError, FailedToGetTokenForSigaaError, UnreachableSigaaError, NoAppCredentialsForSigaaError


DEFAULT_POST_GRADUATION_INITIALS = 'PPGP'
DEFAULT_ACTION = 'view'



@app.route('/')
@app.route('/<string:initials>/')
def home(initials=DEFAULT_POST_GRADUATION_INITIALS):
    """
    Render a post-graduation program page.

    Try to find which program has been requested.

    If it's here: signed in Minerva, show its main page,
    otherwise the user is redirected to that programs external web site.

    If couldn't find which program has been requested, show a 404 page error.
    """

    post_graduation = find_post_graduation(initials)

    # renders an own page or redirect to another (external/404)?
    if post_graduation is None:
        return page_not_found()

    if not post_graduation['isSignedIn']:
        return redirect(post_graduation['oldURL'])

    # query google maps api
    google_maps_api_dict = keyring.get(keyring.GOOGLE_MAPS)

    google_maps_api_key = 'none'
    if google_maps_api_dict is not None:
        google_maps_api_key = google_maps_api_dict['key']

    # search for final reports schedule
    final_reports = factory.final_reports_dao().find_one({
        'ownerProgram': post_graduation['_id']
    })['scheduledReports']

    # search for weekly schedules
    weekly_schedules = factory.weekly_schedules_dao().find({
        'ownerProgram': post_graduation['_id']
    })

    # ready... fire!
    return render_template(
        'index.html',
        std=get_std_for_template(post_graduation),
        google_maps_api_key=google_maps_api_key,
        final_reports=final_reports,
        weekly_schedules=weekly_schedules
    )



@app.route('/<string:initials>/disciplinas/')
def view_subjects(initials):
    """Render a view for subjects."""

    post_graduation = find_post_graduation(initials)

    grades_of_subjects = factory.grades_of_subjects_dao().find({
        'ownerProgram': post_graduation['_id']
    })

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'subjects_view.html',
        std=get_std_for_template(post_graduation),
        grades_of_subjects=grades_of_subjects
    )



@app.route('/<string:initials>/docentes/')
def view_professors(initials):
    """Render a view for professors list."""

    post_graduation = find_post_graduation(initials)

    board_of_professors = factory.boards_of_professors_dao().find_one({
        'ownerProgram': post_graduation['_id']
    })

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'professors_view.html',
        std=get_std_for_template(post_graduation),
        board_of_professors=board_of_professors
    )



@app.route('/<string:initials>/eventoseconvenios/')
def view_integrations(initials):
    """Render a view for integrations lists."""

    post_graduation = find_post_graduation(initials)

    integrations_infos = factory.integrations_infos_dao().find_one({
        'ownerProgram': post_graduation['_id']
    })

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'integrations_view.html',
        std=get_std_for_template(post_graduation),
        integrations_infos=integrations_infos
    )



@app.route('/<string:initials>/equipe/')
def view_staffs(initials):
    """Render a view for staff list."""

    post_graduation = find_post_graduation(initials)

    board_of_staffs = factory.boards_of_staffs_dao().find_one({
        'ownerProgram': post_graduation['_id']
    })

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'staffs_view.html',
        std=get_std_for_template(post_graduation),
        board_of_staffs=board_of_staffs
    )



@app.route('/<string:initials>/discentes/')
def view_students(initials):
    """Render a view for students list."""

    post_graduation = find_post_graduation(initials)

    students_from_sigaa = factory.students_dao().find_all()
    students = []
    for student_from_sigaa in students_from_sigaa:
        students.append({
            'name': student_from_sigaa['nome'].title(),
            'class': student_from_sigaa['matricula'][0:4],
            'level': student_from_sigaa['descricaoNivel'].capitalize(),
            'orientation': student_from_sigaa['orientacoesAcademica'][0]['nome'].title()
        })

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'students_view.html',
        std=get_std_for_template(post_graduation),
        students=students
    )



@app.route('/<string:initials>/documentos/')
def view_documents(initials):
    """Render a view for documents list."""

    post_graduation = find_post_graduation(initials)

    documents = factory.official_documents_dao().find({
        'ownerProgram': post_graduation['_id']
    })

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'documents_view.html',
        std=get_std_for_template(post_graduation),
        documents=documents
    )



# AUX
def find_post_graduation(initials):
    """Search for post graduation from database using the given
    initials as a parameter. It's case insensitive.
    It wrappes _dao.find_one(conditions)"""
    return factory.post_graduations_dao().find_one({
        'initials': initials.upper(),
        #'isSignedIn': True
    })



# AUX
def get_std_for_template(post_graduation, giveMeEmpty=False):
    """
    Return default template stuff for jinja to render.

    Freely put None if theres no post_graduation dict.
    But if there's one, must be the found by DAOs
    and requested by user.

    Must be called like this in every template:
        return render_template('MYTEMPLATE.html', std=get_std_for_template(None), ...)
    That said, there will always be a std dict in jinja environments.

    Jinja will have following template vars, if you called it right:
        std.post_graduation (dict for current given post graduation)
        std.post_graduations_registered (dict for the post graduations available at minerva)
        std.post_graduations_unregistered (dict for post graduations unavailable at minerva)
    They can be None if nothing has found from database or provided by function args.

    Jinja will have the following template vars, if you called it with giveMeEmpty=True:
        std.post_graduation == None
        std.post_graduations_registered == []
        std.post_graduations_unregistered == []
    """
    if giveMeEmpty:
        return {
            'post_graduation': None,
            'post_graduations_registered': [],
            'post_graduations_unregistered': [],
        }
    else:
        post_graduations_dao = factory.post_graduations_dao()
        post_graduations_registered = post_graduations_dao.find({'isSignedIn': True})
        post_graduations_unregistered = post_graduations_dao.find({'isSignedIn': False})
        return {
            'post_graduation': post_graduation,
            'post_graduations_registered': post_graduations_registered,
            'post_graduations_unregistered': post_graduations_unregistered,
        }



@app.route('/404')
@app.errorhandler(404)
def page_not_found(error=None):
    """Render page not found error."""

    print(str(error))
    return render_template('404.html', std=get_std_for_template(None)), 404



@app.errorhandler(SigaaError)
def sigaa_exception_handler(error):
    """Render page for APISistemas errors. """
    print("ERROR for API Sistemas (" + repr(error) + "): " + str(error))

    if type(error) == UnreachableSigaaError:
        return render_template('503.html', std=get_std_for_template(None)), 503
    
    if type(error) == FailedToGetTokenForSigaaError:
        return render_template('501.html', std=get_std_for_template(None)), 501

    if type(error) == NoAppCredentialsForSigaaError:
        return render_template('500.html', std=get_std_for_template(None)), 500


@app.errorhandler(ServerSelectionTimeoutError)
def pymongo_exception_handler(error):
    """Render page for PyMongo errors."""
    print("ERROR for PyMongo: MongoDB took too long to answer, is its service available, running and can be reached?")
    # never renders it... =[ why?
    return render_template('500.html', std=get_std_for_template(None), giveMeEmpty=True), 500
