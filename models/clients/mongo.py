"""
Has everything you need to start acessing data from Mongo.
"""

import os
from models.clients.util import keyring
from pymongo import MongoClient

mongo_uri_dict = keyring.get(keyring.MONGO_URI)
MONGO_URI = mongo_uri_dict['mongo_uri']

# database info
try:
    __DB_NAME = os.environ['DATABASE_NAME']
except KeyError:
    __DB_NAME = 'posgrad'
__DB_PORT = 27017

if MONGO_URI is None:
    MONGO_URI = 'localhost'

# try to create a public object to access content from this mongo database
__DB_CLIENT = MongoClient(MONGO_URI)
DB = __DB_CLIENT[__DB_NAME]
