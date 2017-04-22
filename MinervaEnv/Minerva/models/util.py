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
    """

    def __init__(self):
        """
        This constructor must be implemented in RepositoryBase subclasses only.
        """
        raise NotImplementedError("Tried to create an instance of an abstract class.")



    def get_all(self):
        """
        Gets all the documents from the collection.
        """
        raise NotImplementedError("Tried to call an abstract function without implement.")



    def get_by_id(self):
        """
        Gets the document with the id field provided.
        """
        raise NotImplementedError("Tried to call an abstract function without implement.")



    def filter(self):
        """
        Filter the documents with provided conditions.
        """
        raise NotImplementedError("Tried to call an abstract function without implement.")



    def save(self):
        """
        Insert a document to the table.
        """
        raise NotImplementedError("Tried to call an abstract function without implement.")



    def update_by_id(self):
        """
        Update an existing document.
        """
        raise NotImplementedError("Tried to call an abstract function without implement.")



    def delete_by_id(self):
        """
        Logical delete a document by its id.
        """
        raise NotImplementedError("Tried to call an abstract function without implement.")
