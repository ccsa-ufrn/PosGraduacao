"""
Routes and views for the flask application.
"""

from flask import render_template, redirect
from Minerva import app



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
    """Render a post graduation program page."""
    program_initials = program_initials.upper()

    if program_initials is None or not program_initials in PROGRAMS:
        return page_not_found()
    elif program_initials in PROGRAMS and not PROGRAMS[program_initials]['signedIn']:
        return redirect(PROGRAMS[program_initials]['oldURL'])

    return render_template(
        'index.html',
        program=PROGRAMS[program_initials],
        programs_list=PROGRAMS
    )



@app.route('/404')
@app.errorhandler(404)
def page_not_found(error=None):
    """Render page not found error."""

    print(str(error)) # TODO: this exception swallowing should be avoided!
    return render_template('404.html'), 404
