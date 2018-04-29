from flask import Blueprint
from ..auth import auth_token

api = Blueprint('api', __name__)


@api.before_request
#@auth_token.login_required
def before_request():
    """<b>Description:</b>All routes in this blueprint require authentication"""
    pass


@api.after_request
def after_request(response):
    """
    <b>Description:</b> that allows restricted or not resources on a web page to be
     requested from another domain outside the domain from which the resource originated.
     SoftPymes Plus is (*)
    """
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

from .referential import items
from .referential import details
from .referential import menu
from .referential import user
from .referential import typeproperty
from .referential import management
from .referential import zona
from .referential import property