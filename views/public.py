"""
Routes and views for public pages about Post Graduation Programs.
"""

from flask import Blueprint, render_template, redirect,\
                  current_app, request
from pymongo.errors import ServerSelectionTimeoutError

from scraping.institutional_repository import RIScraper
from models.clients.util import keyring

from models.factory import PosGraduationFactory
from models.clients.api_sistemas import SigaaError, FailedToGetTokenForSigaaError, UnreachableSigaaError, NoAppCredentialsForSigaaError


app = Blueprint('public', __name__, static_folder='static', url_prefix='')

@app.route('/')
def root():
    """
    Render a root page for public access.
    """
    return render_template(
        'public/index.html',
        std=get_std_for_template(None),
    )




@app.route('/<string:initials>/')
def home(initials):
    """
    Render a post-graduation program page.

    Try to find which program has been requested.

    If it's here: signed in Minerva, show its main page,
    otherwise the user is redirected to that programs external web site.

    If couldn't find which program has been requested, show a 404 page error.
    """

    pfactory = PosGraduationFactory(initials)
    post_graduation = pfactory.post_graduation

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

    # search for home data
    final_reports = pfactory.final_reports_dao().find_one()['scheduledReports']
    weekly_schedules = pfactory.weekly_schedules_dao().find()
    integrations_infos = pfactory.integrations_infos_dao().find_one()
    attendance = pfactory.attendances_dao().find_one()

    # ready... fire!
    return render_template(
        'public/home.html',
        std=get_std_for_template(post_graduation),
        google_maps_api_key=google_maps_api_key,
        final_reports=final_reports,
        weekly_schedules=weekly_schedules,
        attendance=attendance,
        institutionsWithCovenant=integrations_infos['institutionsWithCovenant']
    )



@app.route('/<string:initials>/documents/<string:filename>/')
def download_documents(initials, filename):
    """
    Open a file from static folder.
    """
    return current_app.send_static_file('upload_files/' + initials.lower() + '/' + filename)



@app.route('/<string:initials>/disciplinas/')
def view_subjects(initials):
    """Render a view for subjects."""

    pfactory = PosGraduationFactory(initials)
    post_graduation = pfactory.post_graduation

    grades_of_subjects = pfactory.grades_of_subjects_dao().find()

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/subjects.html',
        std=get_std_for_template(post_graduation),
        grades_of_subjects=grades_of_subjects
    )



@app.route('/<string:initials>/docentes/')
def view_professors(initials):
    """Render a view for professors list."""

    pfactory = PosGraduationFactory(initials)
    post_graduation = pfactory.post_graduation

    board_of_professors = pfactory.boards_of_professors_dao().find_one()

    # manually fill missing lattes
    for professor in board_of_professors['professors']:
        if 'Djalma Freire Borges'.upper() in professor['name'].upper():
            professor['lattes'] = 'http://lattes.cnpq.br/3216184364856265'
        elif 'Káio César Fernandes'.upper() in professor['name'].upper():
            professor['lattes'] = 'http://lattes.cnpq.br/9740792920379789'
        elif 'Richard Medeiros de Araújo'.upper() in professor['name'].upper():
            professor['lattes'] = 'http://lattes.cnpq.br/6158536331515084'
        elif 'Ítalo Fittipaldi'.upper() in professor['name'].upper():
            professor['lattes'] = 'http://lattes.cnpq.br/7626654802346326'
        elif 'Hironobu Sano'.upper() in professor['name'].upper():
            professor['lattes'] = 'http://lattes.cnpq.br/6037766951080411'


    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/professors.html',
        std=get_std_for_template(post_graduation),
        board_of_professors=board_of_professors
    )



@app.route('/<string:initials>/intercambios/')
def view_participations(initials):
    """Render a view for integrations lists."""

    pfactory = PosGraduationFactory(initials)
    post_graduation = pfactory.post_graduation

    integrations_infos = pfactory.integrations_infos_dao().find_one()

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/participations.html',
        std=get_std_for_template(post_graduation),
        integrations_infos=integrations_infos
    )



@app.route('/<string:initials>/convenios/')
def view_covenants(initials):
    """Render a view for integrations lists."""

    pfactory = PosGraduationFactory(initials)
    post_graduation = pfactory.post_graduation

    integrations_infos = pfactory.integrations_infos_dao().find_one()

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/covenants.html',
        std=get_std_for_template(post_graduation),
        integrations_infos=integrations_infos
    )



@app.route('/<string:initials>/calendario/')
def view_calendar(initials):
    """Render a view for calendar."""

    pfactory = PosGraduationFactory(initials)
    post_graduation = pfactory.post_graduation

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/calendar.html',
        std=get_std_for_template(post_graduation)
    )



@app.route('/<string:initials>/equipe/')
def view_staffs(initials):
    """Render a view for staff list."""

    pfactory = PosGraduationFactory(initials)
    post_graduation = pfactory.post_graduation

    board_of_staffs = pfactory.boards_of_staffs_dao().find_one()

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/staffs.html',
        std=get_std_for_template(post_graduation),
        board_of_staffs=board_of_staffs
    )



@app.route('/<string:initials>/discentes/')
def view_students(initials):
    """Render a view for students list."""

    pfactory = PosGraduationFactory(initials)
    post_graduation = pfactory.post_graduation

    students = pfactory.students_dao().find()

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/students.html',
        std=get_std_for_template(post_graduation),
        students=students
    )



@app.route('/<string:initials>/projetos/')
def view_projects(initials):
    """Render a view for projects list."""

    pfactory = PosGraduationFactory(initials)
    post_graduation = pfactory.post_graduation

    projects = pfactory.projects_dao().find()

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/projects.html',
        std=get_std_for_template(post_graduation),
        projects=projects
    )



@app.route('/<string:initials>/documentos/')
def view_documents(initials):
    """Render a view for documents list."""

    pfactory = PosGraduationFactory(initials)
    post_graduation = pfactory.post_graduation

    documents = pfactory.official_documents_dao().find()

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/documents.html',
        std=get_std_for_template(post_graduation),
        documents=documents
    )



@app.route('/<string:initials>/conclusoes/')
def view_final_reports(initials):
    """Render a view for conclusion works list."""

    try:
        post_graduation = PosGraduationFactory(initials).post_graduation

        page = request.args.get('page')
        if page is None:
            page = 1

        final_reports, max_page = RIScraper.final_reports_list(initials, page)

        return render_template(
            'public/final_reports.html',
            std=get_std_for_template(post_graduation),
            final_reports=final_reports,
            current_page=page,
            max_page=max_page,
        )
    except AttributeError | Exception:
        return page_not_found()


# AUX
def get_std_for_template(post_graduation, give_me_empty=False):
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

    Jinja will have the following template vars, if you called it with give_me_empty=True:
        std.post_graduation == None
        std.post_graduations_registered == []
        std.post_graduations_unregistered == []
    """
    if give_me_empty:
        return {
            'post_graduation': None,
            'post_graduations_registered': [],
            'post_graduations_unregistered': [],
        }
    else:
        pfactory = PosGraduationFactory()
        post_graduations_registered = pfactory.post_graduations_dao().find({'isSignedIn': True})
        post_graduations_unregistered = pfactory.post_graduations_dao().find({'isSignedIn': False})
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
        return render_template('public/503.html', std=get_std_for_template(None)), 503
    
    if type(error) == FailedToGetTokenForSigaaError:
        return render_template('public/501.html', std=get_std_for_template(None)), 501

    if type(error) == NoAppCredentialsForSigaaError:
        return render_template('public/500.html', std=get_std_for_template(None)), 500


@app.errorhandler(ServerSelectionTimeoutError)
def pymongo_exception_handler(error):
    """Render page for PyMongo errors."""
    print("ERROR for PyMongo: MongoDB took too long to answer, is its service available, running and can be reached?")
    # never renders it... =[ why?
    return render_template('public/500.html', std=get_std_for_template(None), give_me_empty=True), 500
