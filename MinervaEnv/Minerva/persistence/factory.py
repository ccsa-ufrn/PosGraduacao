"""
All DAOs should be called using this module, instead
of directly call their own constructor.

A factory of Data Access Objects.
"""

from .dao import DAO

# constants for collection names in mongodb

COLLECTION_OF_USERS = 'users'
COLLECTION_OF_POST_GRADUATIONS = 'postGraduations'
COLLECTION_OF_FINAL_REPORTS = 'finalReports'
COLLECTION_OF_WEEKLY_SCHEDULES = 'weeklySchedules'
COLLECTION_OF_GRADES_OF_SUBJECTS = 'gradesOfSubjects'

# factory methods

#def get_user_dao():
#    """ Get a user DAO instance. (TODO: implement some kind of singleton) """
#    return DAO(COLLECTION_OF_USERS)

def post_graduations_dao():
    """ Gets an instance of a data access object for a certain collection
    (TODO: implement some kind of singleton) """
    return DAO(COLLECTION_OF_POST_GRADUATIONS)

def final_reports_dao():
    """ Gets an instance of a data access object for a certain collection
    (TODO: implement some kind of singleton) """
    return DAO(COLLECTION_OF_FINAL_REPORTS)

def weekly_schedules_dao():
    """ Gets an instance of a data access object for a certain collection
    (TODO: implement some kind of singleton) """
    return DAO(COLLECTION_OF_WEEKLY_SCHEDULES)

def grades_of_subjects_dao():
    """ Gets an instance of a data access object for a certain collection
    (TODO: implement some kind of singleton) """
    return DAO(COLLECTION_OF_GRADES_OF_SUBJECTS)
