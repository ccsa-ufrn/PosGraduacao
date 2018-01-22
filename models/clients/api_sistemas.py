"""
A simple OAuth 2 Client for API Sistemas, a read-only API
for SIGAA (the university database).

Do not use this module directly, use factory instead.

For more details about what was needed to build this script, check out APISistemas doc:
https://api.ufrn.br/
"""

import json
import sys
import datetime

import requests # To read: http://docs.python-requests.org/en/master/user/quickstart/
#from urllib3 import urlencode
from flask import session

from models.clients.util import keyring

# try to get security keys to access APISistemas
sinfo_api_dict = keyring.get(keyring.SINFO_API)

# security data
CLIENT_ID  =T = 'none'
CLIENT_SECRET = 'none'
X_API_KEY = 'none'

try:
    CLIENT_ID     = sinfo_api_dict['client-id']
    CLIENT_SECRET = sinfo_api_dict['client-secret']
    X_API_KEY = sinfo_api_dict['x-api-key']
except KeyError:
    raise NoAppCredentialsForSigaaError()

# important URLs for APISistemas
API_URL_ROOT           = 'https://apitestes.info.ufrn.br/' # API root (it's a test security link for now)
AUTHORIZATION_ENDPOINT = API_URL_ROOT + 'authz-server/oauth/authorize' # auth
TOKEN_ENDPOINT         = API_URL_ROOT + 'authz-server/oauth/token' # token

# other URLs for some available services WARNING: dict not working as expected
URL_SERVICES = {
    'ensino'        : API_URL_ROOT + 'ensino-services/services/',
    'usuario'       : API_URL_ROOT + 'usuario-services/services/', # deprecated
    'stricto_sensu' : API_URL_ROOT + 'stricto-sensu-services/services/',
    'docente'       : API_URL_ROOT + 'docente-services/services/',
}

def get_public_data(resource_url, bearer_token):
    """
    Try to retrieve a token and then access a resource from API Sistemas.
    
    Returns the expected json (check API Sistemas web site and its Swagger) as a Python Dictionary.
    """
    headers = {
        'Authorization' : 'Bearer ' + bearer_token,
        'x-api-key': X_API_KEY
    }
    
    try:
        returned_data = requests.get(resource_url, headers=headers)
        dict_data = json.loads(returned_data.text)
        return dict_data
    except:
        raise UnreachableSigaaError(resource_url)



def retrieve_token():
    """
    Retrieve access_token as a json and convert it to dict in a global variable.
    
    Return the data string (only the token itself) if it could be retrieved (successfully or not), 
    and None if it could not be done due to lack of credentials.
    TODO: better management for the retrieved token, what's the returned 'expires_in' about?
    """
    
    query_params = {
        'client_id'     : CLIENT_ID,
        'client_secret' : CLIENT_SECRET,
        'grant_type'    : 'client_credentials',
    }

    try:
        returned_data = requests.post(TOKEN_ENDPOINT, data=query_params)
        dict_data = json.loads(returned_data.text)
        bearer_token = dict_data['access_token']
        return bearer_token
    except KeyError:
        raise FailedToGetTokenForSigaaError()
    except:
        raise UnreachableSigaaError(TOKEN_ENDPOINT)

def user_authorization_url():
    """
    Assemble (and return) URL for this application redirect (GET) to the authentication server.
    WARNING: If you're running in local host, Sinfo's servers won't be able to find "localhost".
    
    Return the URL string if it could be assembled, 
    and None if it could not be done due to lack of credentials.
    """

    query_params_str  = '?client_id=' + CLIENT_ID
    query_params_str += '&response_type=code'
    query_params_str += '&redirect_uri=http://localhost:4444/dashboard'

    return AUTHORIZATION_ENDPOINT + query_params_str




# ERROR HANDLING


class SigaaError(Exception):
    """Base class for exceptions about API Sistemas"""
    pass


class UnreachableSigaaError(SigaaError, ConnectionError):
    """If API Sistemas couldn't be reached."""

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def __str__(self):
        return repr("Tried to access: " + self.endpoint)


class NoAppCredentialsForSigaaError():
    """App provided by API Sistemas developers couldn't be retrieved."""

    def __str__(self):
        return repr("Couldn't find security files.")


class FailedToGetTokenForSigaaError(SigaaError, ConnectionError):
    """Token couldn't be retrieved, so the app failed while trying to authenticate."""

    def __str__(self):
        return repr("Credentials are wrong.")
