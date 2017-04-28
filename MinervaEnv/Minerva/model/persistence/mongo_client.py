"""
Has everything you need to start acessing data from Mongo.
"""

from pymongo import MongoClient

# database info
__DB_HOST = 'localhost'
__DB_PORT = 27017
__DB_NAME = 'minerva'

# try to create a public object to access content from this mongo database
# TODO: search for its exceptions
__DB_CLIENT = MongoClient(__DB_HOST, __DB_PORT)
DB = __DB_CLIENT[__DB_NAME]
