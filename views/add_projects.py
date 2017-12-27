"""
Script that will add all in execution projects in a certain area and add to db
"""

from models.clients.util import keyring

from models.factory import PosGraduationFactory
from models.clients.api_sistemas import SigaaError, FailedToGetTokenForSigaaError, UnreachableSigaaError, NoAppCredentialsForSigaaError

initials = ['PPGD']

from initial in initials
    pfactory = PosGraduationFactory(initial)
    projects = pfactory.projects_dao().find()
