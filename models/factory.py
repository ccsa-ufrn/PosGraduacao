"""
All DAOs should be called using this module, instead
of directly call their own constructor.

A factory of Data Access Objects.
"""

from models.clients import api_sistemas
from models.dao import GenericMongoDAO, StudentSigaaDAO, ProjectSigaaDAO, ClassesSigaaDAO, PublicationsSigaaDAO, ArticlesSigaaDAO

# constants for collection names in mongodb

_COLLECTION_OF_POST_GRADUATIONS = 'postGraduations'
_COLLECTION_OF_FINAL_REPORTS = 'finalReports'
_COLLECTION_OF_WEEKLY_SCHEDULES = 'weeklySchedules'
_COLLECTION_OF_GRADES_OF_SUBJECTS = 'gradesOfSubjects'
_COLLECTION_OF_BOARD_OF_PROFESSORS = 'boardsOfProfessors'
_COLLECTION_OF_INTEGRATIONS_INFOS = 'integrationsInfos'
_COLLECTION_OF_BOARDS_OF_STAFFS = 'boardsOfStaffs'
_COLLECTION_OF_OFFICIAL_DOCUMENTS = 'officialDocuments'
_COLLECTION_OF_ATTENDANCES = 'attendances'
_COLLECTION_OF_CALENDAR = 'calendar'
_COLLECTION_OF_PUBLICATIONS = 'publications'
_COLLECTION_OF_PROJECTS = 'projects'
_COLLECTION_OF_NEWS = 'news'
_COLLECTION_OF_COORDINATORS = 'studentsCoordinators'
_COLLECTION_OF_FIRST_CLASSES = 'firstClasses'

# factory methods

class PosGraduationFactory(object):
    """
    Provide factory methods for data access objects to postgraduation programs.
    """

    def __init__(self, initials='noInitialsProvided'):
        """
        If a parameter is given (program's initials), all data access objects
        created will be implictly searching for the found program.
        """
        self.post_graduation = self.post_graduations_dao().find_one({
            'initials': initials.upper()
        })
        if self.post_graduation is not None:
            self.mongo_id = self.post_graduation['_id']
            self.sigaa_code = self.post_graduation['sigaaCode']
            self.id_courses = self.post_graduation['coursesId']
            self.id_unit = self.post_graduation['idUnit']
        else:
            self.mongo_id = None
            self.sigaa_code = None


    def post_graduations_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return GenericMongoDAO(_COLLECTION_OF_POST_GRADUATIONS)

    def final_reports_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return GenericMongoDAO(_COLLECTION_OF_FINAL_REPORTS, self.mongo_id)

    def weekly_schedules_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return GenericMongoDAO(_COLLECTION_OF_WEEKLY_SCHEDULES, self.mongo_id)

    def grades_of_subjects_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return GenericMongoDAO(_COLLECTION_OF_GRADES_OF_SUBJECTS, self.mongo_id)

    def publications_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return GenericMongoDAO(_COLLECTION_OF_PUBLICATIONS, self.mongo_id)

    def board_of_professors_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return GenericMongoDAO(_COLLECTION_OF_BOARD_OF_PROFESSORS, self.mongo_id)

    def integrations_infos_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return GenericMongoDAO(_COLLECTION_OF_INTEGRATIONS_INFOS, self.mongo_id)

    def calendar_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return GenericMongoDAO(_COLLECTION_OF_CALENDAR, self.mongo_id)

    def news_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return GenericMongoDAO(_COLLECTION_OF_NEWS, self.mongo_id)

    def boards_of_staffs_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return GenericMongoDAO(_COLLECTION_OF_BOARDS_OF_STAFFS, self.mongo_id)

    def official_documents_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return GenericMongoDAO(_COLLECTION_OF_OFFICIAL_DOCUMENTS, self.mongo_id)

    def attendances_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return GenericMongoDAO(_COLLECTION_OF_ATTENDANCES, self.mongo_id)

    def projects_database_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return GenericMongoDAO(_COLLECTION_OF_PROJECTS, self.mongo_id)

    def classes_database_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return GenericMongoDAO(_COLLECTION_OF_FIRST_CLASSES, self.mongo_id)

    def projects_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return ProjectSigaaDAO(int(self.sigaa_code))

    def coordinators_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return GenericMongoDAO('studentsCoordinators', self.mongo_id)

    def students_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        courses_dict = {}
        for course in self.id_courses:
            courses_dict[course['nameCourse']] = StudentSigaaDAO(int(course['idCourse'])).find()
        return courses_dict

    def classes_dao(self, year, period, limit):
        """Gets an instance of a data access object for a certain collection """
        return ClassesSigaaDAO(int(self.id_unit), int(year), int(period), int(limit))

    def publications_sigaa_dao(self, list_of_professors, type_of_publication):
        """Gets an instance of a data access object for a certain collection """
        return PublicationsSigaaDAO(list_of_professors, type_of_publication)

    def articles_sigaa_dao(self, list_of_professors, type_of_publication):
        """Gets an instance of a data access object for a certain collection """
        return ArticlesSigaaDAO(list_of_professors, type_of_publication)
