from flask import jsonify, g, current_app, request
from flask.ext.httpauth import HTTPBasicAuth, HTTPTokenAuth
from .models.security.user import User
from werkzeug.routing import ValidationError
from . import session

auth = HTTPBasicAuth()
auth_token = HTTPTokenAuth()


@auth_token.verify_token
def verify_auth_token(token):
    """This function validate the auth token, this allow 
    enter wheter change your password from login page

    :param token:
    :return: boolean whether test pass, or none
    """
    user = User.verify_auth_token(token)

    return user is not None


@auth_token.error_handler
def unauthorized_token():
    """
    This function validate authorized token

    :return: status code
    """
    response = jsonify({'status': 401, 'error': 'unauthorized',
                        'message': 'please send your authentication token'})
    response.status_code = 401
    return response
