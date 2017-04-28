"""
This module has everything you need to start and maintain the models.
"""

from pymongo import MongoClient


# database info
__DB_HOST = 'localhost'
__DB_PORT = 27017
__DB_NAME = 'minerva'

# try to create a public object to access content from this mongo database
__DB_CLIENT = MongoClient(__DB_HOST, __DB_PORT)
DB = __DB_CLIENT[__DB_NAME]


# abstract class that is base for other models
class RepositoryBase(object):
    """
    Describes methods for each model do its own implementation.
    The method names are based and on MongoDB functions.
    """

    def __init__(self):
        """
        This constructor must be implemented in RepositoryBase subclasses only.
        """
        raise NotImplementedError("Tried to create an instance of an abstract class.")



    def find_all(self):
        """
        Gets all the documents from the collection.
        """
        raise NotImplementedError("Tried to call an abstract function without implement.")



    def find_by_id(self, document_id):
        """
        Gets the document with the id field provided.
        """
        raise NotImplementedError("Tried to call an abstract function without implement.")



    def find_by_filter(self, conditions):
        """
        Filter the documents with provided conditions as a dictionary representing the
        filter json and returns an array of instances for this model.
        """
        raise NotImplementedError("Tried to call an abstract function without implement.")



    def insert(self):
        """
        Insert this document into the collection and returns its new id if it worked,
        otherwise False.
        """
        raise NotImplementedError("Tried to call an abstract function without implement.")



    def update(self):
        """
        Update this document by its id in the collection and returns True if it worked,
        otherwise False.
        """
        raise NotImplementedError("Tried to call an abstract function without implement.")



    def delete(self):
        """
        Logical delete this document from the collection by its id, and returns True if
        it could be done, False otherwise. So, the document still recorded at persistence,
        but can no longer be retrieved using regular CRUD methods.
        """
        raise NotImplementedError("Tried to call an abstract function without implement.")
