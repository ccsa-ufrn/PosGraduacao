"""
Implements a generic DAO design pattern.

Acts as a middleware. All data must be manipulated
using this class, so if a problem happens, I can directly make
some change without depending only of PyMongo Client.
"""



from mongo_client import DB



class DAO(object):
    """
    It's just an own abstraction for DB persistence.

    Must be used by another class from domain, that implements business rules
    for acessing data.
    """



    def __init__(self, collection: str):
        """
        Initialize a data access object for a given collection from
        a mongo data base.
        """
        self.collection = collection



    def find_all(self):
        """
        Gets a list of all the documents from the collection.
        """
        return DB[self.collection].find_all()



    def find_by_id(self, document_id):
        """
        Gets a single dict corresponding to a found document with the id field provided.
        """
        return DB[self.collection].find_one({'id': document_id})



    def find(self, conditions: dict):
        """
        Filters the documents with provided conditions as a dictionary representing the
        filter json and returns a list of dicts corresponding to found documents
        from the collection.
        """
        return DB[self.collection].find(conditions)



    def insert(self, document: dict):
        """
        Insert a document into the collection and returns its new id if it worked.
        """
        return DB[self.collection].insert_one(document).inserted_id



    def insert_many(self, document: list):
        """
        Insert a list of documents into the collection and returns their
        new ids if it worked.
        """
        return DB[self.collection].insert_one(document).inserted_ids



    def update(self):
        """
        Update this document by its id in the collection and returns True if it worked,
        otherwise False.
        """
        raise NotImplementedError("Tried to call an update function without implementing it.")



    def delete(self):
        """
        Logical delete this document from the collection by its id, and returns True if
        it could be done, False otherwise. So, the document still recorded at persistence,
        but can no longer be retrieved using regular CRUD methods.
        """
        raise NotImplementedError("Need to implement update function for logical deleting it.")
