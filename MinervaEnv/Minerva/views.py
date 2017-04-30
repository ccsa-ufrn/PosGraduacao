"""
Routes and views (actually, they're controllers!) for this flask application.
"""

from flask import render_template, redirect
from Minerva import app

import Minerva.util.keyring as keyring
import Minerva.util.apisistemas_oauth2client as api_sistemas
import Minerva.persistence.factory as factory



DEFAULT_POST_GRADUATION_INITIALS = 'PPGP'



@app.route('/')
@app.route('/home')
@app.route('/inicio')
def home():
    """Render the default post graduation program page."""
    return program(DEFAULT_POST_GRADUATION_INITIALS)



@app.route('/<string:initials>')
def program(initials=DEFAULT_POST_GRADUATION_INITIALS):
    """
    Render a post graduation program page.

    Try to find which program has been requested.

    If it's here: signed in Minerva, show its main page,
    otherwise the user is redirected to that programs external web site.

    If couldn't find which program has been requested, show a 404 page error.
    """

    # search some documents for post graduation data
    post_graduation_dao = factory.post_graduation_dao()
    initials = initials.upper()
    post_graduation = post_graduation_dao.find_one({'initials': initials})
    post_graduations_registered = post_graduation_dao.find({'isSignedIn': True})
    post_graduations_unregistered = post_graduation_dao.find({'isSignedIn': False})

    # renders an own page or redirect to another (external/404)?
    if post_graduation is None:
        return page_not_found()

    if not post_graduation['isSignedIn']:
        return redirect(post_graduation['oldUrl'])

    # query google maps api
    google_maps_api_dict = keyring.get(keyring.GOOGLE_MAPS)

    google_maps_api_key = 'none'
    if google_maps_api_dict is not None:
        google_maps_api_key = google_maps_api_dict['key']

    # ready... fire!
    return render_template(
        'index.html',
        post_graduation=post_graduation,
        post_graduations_registered=post_graduations_registered,
        post_graduations_unregistered=post_graduations_unregistered,
        google_maps_api_key=google_maps_api_key
    )



@app.route('/login')
def login():
    return redirect(api_sistemas.user_authorization_url())



@app.route('/dashboard')
def dashboard(code=None):
    return program('PPGP')



@app.route('/404')
@app.errorhandler(404)
def page_not_found(error=None):
    """Render page not found error."""

    print(str(error)) # TODO: this exception swallowing should be avoided!
    return render_template('404.html'), 404
