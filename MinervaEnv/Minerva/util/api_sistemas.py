"""
A simple OAuth 2 Client for API Sistemas, a read-only API
for SIGAA (the university database).

Do not use this module directly, use factory instead.

For more details about what was needed to build this script, check out APISistemas doc:
https://api.ufrn.br/
"""

import requests # To read: http://docs.python-requests.org/en/master/user/quickstart/
import json

#from urllib3 import urlencode

import logging
from . import keyring



# try to get security keys to access APISistemas
sinfo_api_dict = keyring.get(keyring.SINFO_API)

# security data
CLIENT_ID     = sinfo_api_dict['client-id']
CLIENT_SECRET = sinfo_api_dict['client-secret']

# important URLs for APISistemas
API_URL_ROOT           = 'http://apitestes.info.ufrn.br/' # API root (it's a test security link for now)
AUTHORIZATION_ENDPOINT = API_URL_ROOT + 'authz-server/oauth/authorize' # auth
TOKEN_ENDPOINT         = API_URL_ROOT + 'authz-server/oauth/token' # token

# other URLs for some available services
URL_SERVICES = {
    'ensino'        : API_URL_ROOT + 'ensino-services/services/',
    'usuario'       : API_URL_ROOT + 'usuario-services/services/', # deprecated
    'stricto_sensu' : API_URL_ROOT + 'stricto-sensu-services/services/',
    'docente'       : API_URL_ROOT + 'docente-services/services/',
}



def has_app_credentials():
    """
    Return True if credentials retrieving went ok, 
    and False if they're None or raised an Excepton.
    """
    return (CLIENT_ID is not None) and (CLIENT_SECRET is not None)



def get_public_data(resource_url):
    """
    Use a token to access public data from API.
    TEST: get_public_data('http://apitestes.info.ufrn.br/stricto-sensu-services/services/consulta/discente/1672')
    
    Returns the expected json (check API Sistemas web site and its Swagger) as a Python Dictionary.
    """
    headers = {
        'Authorization' : 'Bearer ' + retrieve_token(),
    }
    
    returned_data = requests.get(resource_url, headers=headers)
    dict_data = json.loads(returned_data.text)
    return dict_data


def retrieve_token():
    """
    Retrieve access_token as a json and convert it to dict in a global variable.
    
    Return the data string (only the token itself) if it could be retrieved (successfully or not), 
    and None if it could not be done due to lack of credentials.
    TODO: better exception handling for situations where server could not respond
    or the application access has been somehow denied.
    TODO: better management for the retrieved token, what's the returned 'expires_in' about?
    """
    
    if not has_app_credentials():
        return None
    
    query_params = {
        'client_id'     : CLIENT_ID,
        'client_secret' : CLIENT_SECRET,
        'grant_type'    : 'client_credentials',
    }

    returned_data = requests.post(TOKEN_ENDPOINT, data=query_params)
    dict_data = json.loads(returned_data.text)
    return dict_data['access_token'] # what is the return type if json cannot be loaded?



def user_authorization_url():
    """
    Assemble (and return) URL for this application redirect (GET) to the authentication server.
    WARNING: If you're running in local host, Sinfo's servers won't be able to find "localhost".
    
    Return the URL string if it could be assembled, 
    and None if it could not be done due to lack of credentials.
    """
    
    if not has_app_credentials():
        return None
    
    query_params_str  = '?client_id='+CLIENT_ID
    query_params_str += '&response_type=code'
    query_params_str += '&redirect_uri=http://localhost:4444/dashboard'

    return AUTHORIZATION_ENDPOINT + query_params_str

