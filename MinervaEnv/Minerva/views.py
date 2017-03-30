"""
Routes and views for the flask application.
"""

from flask import render_template, redirect
from Minerva import app

import Minerva.util.keyring as keyring
import Minerva.util.apisistemas_oauth2client as api_sistemas


DEFAULT_PROGRAM_INITIALS = 'PPGP'

PROGRAMS = {
    'PPGP': {
        'name': 'Gestão Pública',
        'initials': 'PPGP',
        'signedIn': True,
        'oldURL': 'https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=5679'
    },
    'PPGA': {
        'name': 'Administração',
        'initials': 'PPGA',
        'signedIn': False,
        'oldURL': 'https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=74'
    },
    'PPGCC': {
        'name': 'Ciências Contábeis',
        'initials': 'PPGCC',
        'signedIn': False,
        'oldURL': 'https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=9066'
    },
    'PPGD': {
        'name': 'Direito',
        'initials': 'PPGD',
        'signedIn': False,
        'oldURL': 'https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=404'
    },
    'PPGECO': {
        'name': 'Economia',
        'initials': 'PPGECO',
        'signedIn': False,
        'oldURL': 'https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=434'
    },
    'PPGPGIC': {
        'name': 'Gestão da Informação e do Conhecimento',
        'initials': 'PPGIC',
        'signedIn': False,
        'oldURL': 'https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=9196'
    },
    'PPGSS': {
        'name': 'Serviço Social',
        'initials': 'PPGSS',
        'signedIn': False,
        'oldURL': 'https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=376'
    },
    'PPGTUR': {
        'name': 'Turismo',
        'initials': 'PPGTUR',
        'signedIn': False,
        'oldURL': 'https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=4295'
    }
}



@app.route('/')
@app.route('/home')
@app.route('/inicio')
def home():
    """Render the default post graduation program page."""
    return program(DEFAULT_PROGRAM_INITIALS)



@app.route('/<string:program_initials>')
def program(program_initials=None):
    """
    Render a post graduation program page.

    Try to find which program has been requested.

    If it's here: signed in Minerva, show its main page,
    otherwise the user is redirected to that programs external web site.

    If couldn't find which program has been requested, show a 404 page error.
    """

    program_initials = program_initials.upper()

    if program_initials is None or not program_initials in PROGRAMS:
        return page_not_found()
    elif program_initials in PROGRAMS and not PROGRAMS[program_initials]['signedIn']:
        return redirect(PROGRAMS[program_initials]['oldURL'])

    # query google maps api
    google_maps_api_dict = keyring.get(keyring.GOOGLE_MAPS)
    google_maps_api_key = google_maps_api_dict['key'] if google_maps_api_dict is not None else 'none'

    # query sinfo api
    token = api_sistemas.gen_acess_token()
    
    return render_template(
        'index.html',
        program=PROGRAMS[program_initials],
        test=token,
        programs_list=PROGRAMS,
        google_maps_api_key=google_maps_api_key
    )



@app.route('/404')
@app.errorhandler(404)
def page_not_found(error=None):
    """Render page not found error."""

    print(str(error)) # TODO: this exception swallowing should be avoided!
    return render_template('404.html'), 404
