"""
All data must be only manipulated through this middleware,
and not directly using Pymongo nor other API wrapper.
"""


from .mongo import DB
from . import api_sistemas


class AbstractDAO(object):

    def __init__(self, collection: str):
        raise NotImplementedError("Tried to create instance from abstract class.")

    def find_all(self):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def find_one(self, conditions: dict):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def find(self, conditions: dict):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def insert_one(self, document: dict):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def insert_many(self, document: list):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def update(self, document: dict):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def delete(self, document: dict):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")



class GenericMongoDAO(AbstractDAO):
    """
    Implements a generic middleware for accessing MongoDB.

    Note that this instance itself don't represent anything at domain,
    it's just useful for accessing dictionaries that stands for documents
    from a certain database collection.
    """


    def __init__(self, collection: str, owner_post_graduation_id: str = None):
        """
        Don't use this constructor directly as you're probably doing now.
        Use its factory instead!

        Create an instance for starting using data access methods.

        All data access will assume as context the given collection and will
        add a 'ownerProgram' search parameter to all data operations if it was
        provided. Collection name must never be None.
        """
        self.collection = collection
        self.owner_post_graduation_id = owner_post_graduation_id



    def find_all(self):
        """
        Gets a list of all the documents from the collection.
        TODO: retrieve only logical alive documents (maybe a 'alive_only=True' param?)
        """
        return DB[self.collection].find_all()



    def find_one(self, conditions: dict = {}):
        """
        Gets a single found document with the given conditions, returns it as dict.
        TODO: retrieve only logical alive documents (maybe a 'alive_only=True' param?)
        """
        if self.owner_post_graduation_id is not None:
            conditions['ownerProgram'] = self.owner_post_graduation_id
        return DB[self.collection].find_one(conditions)



    def find(self, conditions: dict = {}):
        """
        Filters documents from database collection. The given dictionary param
        represents the filter json. Returns a list of dicts, where each of them
        is a found document.
        TODO: retrieve only logical alive documents (maybe a 'alive_only=True' param?)
        """
        if self.owner_post_graduation_id is not None:
            conditions['ownerProgram'] = self.owner_post_graduation_id
        return DB[self.collection].find(conditions)



    def insert_one(self, document: dict):
        """
        Insert a document as dict into the collection and returns its new id if it worked.
        TODO: insert an alive document
        """
        if self.owner_post_graduation_id is not None:
            conditions['ownerProgram'] = self.owner_post_graduation_id
        return DB[self.collection].insert_one(document).inserted_id



    def insert_many(self, document: list):
        """
        TODO: Insert a list of documents into the collection and returns a list of their
        new ids if it worked.
        """
        raise NotImplementedError("Tried to call an update function without implementing it.")



    def update(self, document: dict):
        """
        TODO: implement an update for a single document.
        """
        raise NotImplementedError("Tried to call an update function without implementing it.")



    def delete(self, document: dict):
        """
        TODO: Logical delete. So the document still recorded at persistence,
        but can no longer be retrieved using regular CRUD methods.
        """
        raise NotImplementedError("Need to implement update function for logical deleting it.")




class StudentSigaaDAO(AbstractDAO):

    def __init__(self, program_sigaa_code: int):
        self.ENDPOINT = api_sistemas.API_URL_ROOT
        self.ENDPOINT += 'stricto-sensu-services/services/consulta/discente/'
        self.ENDPOINT += str(program_sigaa_code)

    def find_all(self):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def find_one(self, conditions):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def find(self, conditions: dict = {}):
        return api_sistemas.get_public_data(self.ENDPOINT)

    def insert_one(self, document: dict):
        raise NotImplementedError("Data from SIGAA are read-only.")

    def insert_many(self, document: list):
        raise NotImplementedError("Data from SIGAA are read-only.")

    def update(self, document: dict):
        raise NotImplementedError("Data from SIGAA are read-only.")

    def delete(self, document: dict):
        raise NotImplementedError("Data from SIGAA are read-only.")



class ProjectSigaaDAO(AbstractDAO):

    def __init__(self, program_sigaa_code: int):
        self.ENDPOINT = api_sistemas.API_URL_ROOT
        self.ENDPOINT += 'stricto-sensu-services/services/consulta/projeto/' 
        self.ENDPOINT += str(program_sigaa_code)

    def find_all(self):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def find_one(self, conditions: dict):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def find(self, conditions: dict = {}):
        return api_sistemas.get_public_data(self.ENDPOINT)

    def insert_one(self, document: dict):
        raise NotImplementedError("Data from SIGAA are read-only.")

    def insert_many(self, document: list):
        raise NotImplementedError("Data from SIGAA are read-only.")

    def update(self, document: dict):
        raise NotImplementedError("Data from SIGAA are read-only.")

    def delete(self, document: dict):
        raise NotImplementedError("Data from SIGAA are read-only.")
