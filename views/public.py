"""
Routes and views for public pages about Post Graduation Programs.
"""
import sys
import datetime

from flask import Blueprint, render_template, redirect, \
current_app, request, jsonify, url_for
from pymongo.errors import ServerSelectionTimeoutError

from scraping.institutional_repository import RIScraper
from scraping.professors_sigaa import SigaaScraper
from models.clients.util import keyring

from views.forms.content import FindClass 

from models.factory import PosGraduationFactory
from models.clients.api_sistemas import SigaaError, FailedToGetTokenForSigaaError, UnreachableSigaaError, NoAppCredentialsForSigaaError

from bson.json_util import dumps
from bson.objectid import ObjectId


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
    final_reports = pfactory.final_reports_dao().find_one()
    calendar = pfactory.calendar_dao().find_one()['events']
    selections = []
    events = []
    for event in range(len(calendar)):
        if "deleted" not in calendar[event]:
            if "Seleção" in calendar[event]['title']:
                selections.append(calendar[event])
            else:
                events.append(calendar[event])
    final_reports = final_reports['scheduledReports']
    news = pfactory.news_dao().find_one()['news']
    classes = pfactory.classes_database_dao().find_one()['firstClasses']
    integrations_infos = pfactory.integrations_infos_dao().find_one()
    if integrations_infos is None:
        integrations_infos = {
            'name': "",
            'initials': "",
            'logoFile': "",
        }
        institutions_with_covenant = integrations_infos
    else:
        institutions_with_covenant = integrations_infos['institutionsWithCovenant']
    attendance = pfactory.attendances_dao().find_one()
    if attendance is None:
        attendance = {
            'location' : {
                'building' : '',
                'floor' : '',
                'room' : '',
                'opening' : ''
                },
            'email' : '',
            'phones' : {
                'type' : '',
                'number' : ''
                }
        }

    # ready... fire!
    return render_template(
        'public/home.html',
        std=get_std_for_template(post_graduation),
        google_maps_api_key=google_maps_api_key,
        final_reports=final_reports,
        events=events,
        selections=selections,
        classes=classes,
        news=news,
        institutions_with_covenant=institutions_with_covenant,
        attendance=attendance,
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

    grades_of_subjects = pfactory.grades_of_subjects_dao().find({ '$or': [ { 'title': 'Eletivas' }, { 'title':'Obrigatórias' } ] })

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/subjects.html',
        std=get_std_for_template(post_graduation),
        grades_of_subjects=grades_of_subjects
    )



@app.route('/<string:initials>/docentes/')
def view_professors(initials):
    """Render a view for professors list."""

    try:
        post_graduation = PosGraduationFactory(initials).post_graduation
        board_of_professors = SigaaScraper.professors_list(initials)

        return render_template(
            'public/professors.html',
            std=get_std_for_template(post_graduation),
            board_of_professors=board_of_professors,
        )
    except Exception:
        return page_not_found()



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

    calendar_info = pfactory.calendar_dao().find_one()

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/calendar.html',
        std=get_std_for_template(post_graduation),
        calendar_info=calendar_info
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

    students = pfactory.students_dao()
    course_list = {}
    coordinators = pfactory.coordinators_dao()
    coordinators = list(coordinators.find())
    for course in students.keys():
        for student in students[course]:
            for coordinator in coordinators:
                if student['class'] == str(coordinator['registration']):
                    student['coordinator'] = coordinator['coordinator']
                if 'coordinator' not in student.keys():
                    student['coordinator'] = 'Sem coordenador(a)'

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/students.html',
        std=get_std_for_template(post_graduation),
        students=students
    )

@app.route('/<string:initials>/turmas/', methods=['POST','GET'])
def view_classes(initials):
    """Render a view for classes list."""

    form = FindClass()
    
    pfactory = PosGraduationFactory(initials)
    post_graduation = pfactory.post_graduation
    now = datetime.datetime.now()
    if now.month <= 7:
        semester = 1
    else:
        semester = 2
    classes=pfactory.classes_dao(now.year,semester,100).find()
    if form.validate_on_submit():
        return redirect(
            url_for(
                'public.find_classes',
                initials=initials,
                year=form.year.data,
                period=form.period.data
            )
        )

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/subjectsinclasses.html',
        std=get_std_for_template(post_graduation),
        form=form,
        classes=classes
    )

@app.route('/achar_classes', methods=['POST', 'GET'])
def find_classes():
    form = FindClass()
    pfactory = PosGraduationFactory(request.args['initials'])
    post_graduation = pfactory.post_graduation
    classes_2 =pfactory.classes_dao(request.args['year'], request.args['period'], 100).find()
    return render_template(
        'public/subjectsinclasses.html',
        std=get_std_for_template(post_graduation),
        form=form,
        classes=classes_2
    )


@app.route('/<string:initials>/projetos/')
def view_projects(initials):
    """Render a view for projects list."""

    pfactory = PosGraduationFactory(initials)
    post_graduation = pfactory.post_graduation
    projects = pfactory.projects_database_dao().find()
    projects = list(projects)
    for project in projects:
        coordinators_names = []
        for member in project['members']:
            if 'Coordenador(a)' in member['project_role']:
                coordinators_names.append(member)
                project['members'].remove(member)
        project['coordinators_names'] = coordinators_names

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/projects.html',
        std=get_std_for_template(post_graduation),
        projects=projects
    )


@app.route('/<string:initials>/livros/')
def view_books(initials):
    """Render a view for books list."""

    pfactory = PosGraduationFactory(initials)
    post_graduation = pfactory.post_graduation

    publications = pfactory.publications_dao().find_one()

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/books.html',
        std=get_std_for_template(post_graduation),
        publications=publications
    )

@app.route('/<string:initials>/artigos/')
def view_articles(initials):
    """Render a view for artigos list."""

    pfactory = PosGraduationFactory(initials)
    post_graduation = pfactory.post_graduation

    publications = pfactory.publications_dao().find_one()

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/articles.html',
        std=get_std_for_template(post_graduation),
        publications=publications
    )

@app.route('/<string:initials>/noticias/')
def view_news(initials):
    """Render a view for news viewing."""

    pfactory = PosGraduationFactory(initials)
    post_graduation = pfactory.post_graduation

    id = request.args.get('id')
    news = pfactory.news_dao().find_one()['news']
    fullNews = next(piece for piece in news if piece['id'] == id)

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/news.html',
        std=get_std_for_template(post_graduation),
        fullNews=fullNews 
    )


@app.route('/<string:initials>/capitulos/')
def view_chapters(initials):
    """Render a view for chapters list."""

    pfactory = PosGraduationFactory(initials)
    post_graduation = pfactory.post_graduation

    publications = pfactory.publications_dao().find_one()

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/chapters.html',
        std=get_std_for_template(post_graduation),
        publications=publications
    )


@app.route('/<string:initials>/documentos/regimentos')
def view_documents_regiments(initials):
    """Render a view for documents list."""

    pfactory = PosGraduationFactory(initials)
    post_graduation = pfactory.post_graduation

    documents = pfactory.official_documents_dao().find({'category':'regimento'})

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/documents_regiments.html',
        std=get_std_for_template(post_graduation),
        documents=documents
    )

@app.route('/<string:initials>/documentos/atas')
def view_documents_atas(initials):
    """Render a view for documents list."""

    pfactory = PosGraduationFactory(initials)
    post_graduation = pfactory.post_graduation

    documents = pfactory.official_documents_dao().find({'category':'ata'})

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/documents_atas.html',
        std=get_std_for_template(post_graduation),
        documents=documents
    )

@app.route('/<string:initials>/documentos/outros')
def view_documents_others(initials):
    """Render a view for documents list."""

    pfactory = PosGraduationFactory(initials)
    post_graduation = pfactory.post_graduation

    documents = pfactory.official_documents_dao().find({'category':'outros'})

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/documents_others.html',
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
        else:
            page = int(page)
        if initials != 'PPGIC':
            final_reports, max_page = RIScraper.final_reports_list(initials, page, 'master')
        else:
            final_reports = [{'author':'', 'title':'', 'year':'', 'link':''}]
            max_page = 1

        return render_template(
            'public/final_reports.html',
            std=get_std_for_template(post_graduation),
            final_reports=final_reports,
            current_page=page,
            max_page=max_page,
        )
    except Exception:
        return page_not_found()

@app.route('/<string:initials>/conclusoes_doutorado/')
def view_final_reports_phd(initials):
    """Render a view for phd conclusion works list."""

    try:
        post_graduation = PosGraduationFactory(initials).post_graduation

        page = request.args.get('page')
        if page is None:
            page = 1
        else:
            page = int(page)
        if initials != 'PPGIC':
            final_reports, max_page = RIScraper.final_reports_list(initials, page, 'phd')
        else:
            final_reports = [{'author':'', 'title':'', 'year':'', 'link':''}]
            max_page = 1

        return render_template(
            'public/final_reports_phd.html',
            std=get_std_for_template(post_graduation),
            final_reports=final_reports,
            current_page=page,
            max_page=max_page,
        )
    except Exception:
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
