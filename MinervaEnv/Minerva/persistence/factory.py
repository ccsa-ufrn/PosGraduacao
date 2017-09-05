"""
All DAOs should be called using this module, instead
of directly call their own constructor.

A factory of Data Access Objects.
"""

from . import api_sistemas
from .dao import GenericMongoDAO, StudentSigaaDAO, ProjectSigaaDAO

# constants for collection names in mongodb

COLLECTION_OF_USERS = 'users' # TODO need more auth algorithms and plugins
COLLECTION_OF_POST_GRADUATIONS = 'postGraduations'
COLLECTION_OF_FINAL_REPORTS = 'finalReports'
COLLECTION_OF_WEEKLY_SCHEDULES = 'weeklySchedules'
COLLECTION_OF_GRADES_OF_SUBJECTS = 'gradesOfSubjects'
COLLECTION_OF_BOARDS_OF_PROFESSORS = 'boardsOfProfessors'
COLLECTION_OF_INTEGRATIONS_INFOS = 'integrationsInfos'
COLLECTION_OF_BOARDS_OF_STAFFS = 'boardsOfStaffs'
COLLECTION_OF_OFFICIAL_DOCUMENTS = 'officialDocuments'

# factory methods

#def get_user_dao():
#    """ Get a user DAO instance. (TODO: implement some kind of singleton) """
#    return DAO(COLLECTION_OF_USERS)

def post_graduations_dao():
    """ Gets an instance of a data access object for a certain collection
    (TODO: implement some kind of singleton) """
    return GenericMongoDAO(COLLECTION_OF_POST_GRADUATIONS)

def final_reports_dao():
    """ Gets an instance of a data access object for a certain collection
    (TODO: implement some kind of singleton) """
    return GenericMongoDAO(COLLECTION_OF_FINAL_REPORTS)

def weekly_schedules_dao():
    """ Gets an instance of a data access object for a certain collection
    (TODO: implement some kind of singleton) """
    return GenericMongoDAO(COLLECTION_OF_WEEKLY_SCHEDULES)

def grades_of_subjects_dao():
    """ Gets an instance of a data access object for a certain collection
    (TODO: implement some kind of singleton) """
    return GenericMongoDAO(COLLECTION_OF_GRADES_OF_SUBJECTS)

def boards_of_professors_dao():
    """ Gets an instance of a data access object for a certain collection
    (TODO: implement some kind of singleton) """
    return GenericMongoDAO(COLLECTION_OF_BOARDS_OF_PROFESSORS)

def integrations_infos_dao():
    """ Gets an instance of a data access object for a certain collection
    (TODO: implement some kind of singleton) """
    return GenericMongoDAO(COLLECTION_OF_INTEGRATIONS_INFOS)

def boards_of_staffs_dao():
    """ Gets an instance of a data access object for a certain collection
    (TODO: implement some kind of singleton) """
    return GenericMongoDAO(COLLECTION_OF_BOARDS_OF_STAFFS)

def official_documents_dao():
    """ Gets an instance of a data access object for a certain collection
    (TODO: implement some kind of singleton) """
    return GenericMongoDAO(COLLECTION_OF_OFFICIAL_DOCUMENTS)

def students_dao():
    """ Gets an instance of a data access object for a certain collection
    (TODO: implement some kind of singleton) """
    return StudentSigaaDAO(1672)

def projects_dao():
    """ Gets an instance of a data access object for a certain collection
    (TODO: implement some kind of singleton) """
    return ProjectSigaaDAO(1672)
