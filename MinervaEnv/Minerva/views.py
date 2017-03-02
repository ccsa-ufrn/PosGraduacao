"""
Routes and views for the flask application.
"""

from flask import render_template
from Minerva import app



PROGRAM = {'initials': 'PPGP', 'name': 'Gestão Pública'}



@app.route('/')
@app.route('/inicio')
@app.route('/index')
@app.route('/home')
def home():
    """Renders the home page."""

    return render_template(
        'index.html',
        program=PROGRAM,
    )



@app.errorhandler(404)
def page_not_found(error):
    """Renders page not found error."""
    # TODO: avoid this exception swallowing
    print(str(error))
    return render_template('404.html', program=PROGRAM), 404
