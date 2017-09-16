"""
Has everything you need to start acessing data from Mongo.
"""

import os
from pymongo import MongoClient

# database info
try:
    __DB_HOST = os.environ['MINERVAENV_DB_1_PORT_27017_TCP_ADDR']
except KeyError:
    __DB_HOST = 'localhost'

__DB_PORT = 27017
__DB_NAME = 'minerva'

if __DB_HOST is None:
    __DB_HOST = 'localhost'

# try to create a public object to access content from this mongo database
__DB_CLIENT = MongoClient(__DB_HOST, __DB_PORT)
DB = __DB_CLIENT[__DB_NAME]
