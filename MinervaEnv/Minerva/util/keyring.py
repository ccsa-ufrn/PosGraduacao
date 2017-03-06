"""
A simple 'key ring' script. Read data from json files and return the target api credentials.
"""

import json
import logging


# note: id-keys (for each element of a dict or a json) != api-keys (mostly a hash granted by an api)


# json file where the api keys should be organized
ENV_FILE_PATH = 'Minerva/env/api_keys.json'

# json will be converted to dict, and as py dicts (like json, btw) need
# identification keys for each element, the available ones will be listed here,
GOOGLE_MAPS = 'google_maps_js_api'



def get(id_key):
    """Try to open the env file, load its json and search for the wanted data dict.

    Args:
        key_id (str): an identificator for the wanted API inside the found json
                      (as should be described at '?/fake/api_keys.json')
                      (PS: avoid using literal strings, use the local constants)

    Returns:
        dict: found specific json (as described at '?/fake/api_keys.json') of the
              wanted API.
        None: (and log something) if it couldn't be done, didn't find
              the env file or its content is invalid (non-json or has a js comment).
    """

    # reading data from file
    try:
        with open(ENV_FILE_PATH, 'r') as keys_file:
            keys_file_content = keys_file.read()
    except FileNotFoundError:
        logging.error('Failed to find ' + ENV_FILE_PATH)
        return None
    except IOError:
        logging.error('IO Error when trying to read ' + ENV_FILE_PATH)
        return None

    # decoding content into a py dict
    try:
        full_json = json.loads(keys_file_content)
    except json.decoder.JSONDecodeError:
        logging.error('Failed to decode json from ' + ENV_FILE_PATH)
        return None

    # finding the wanted api object
    try:
        return full_json[id_key]
    except KeyError:
        logging.error('Didn\'t find key \'' + id_key + '\' in dict from ' + ENV_FILE_PATH)
        return None
