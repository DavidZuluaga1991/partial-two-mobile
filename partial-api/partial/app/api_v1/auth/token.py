# -*- coding: utf-8 -*-
#!/usr/bin/env python
#########################################################
# All rights by SoftPymes Plus
#
# Auth module
# Allow the access to Sofpymes by token key
# Date: 19-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


from . import api_auth
from ...auth import auth
from flask import g, request, jsonify
from ...models import User
from ... import session
from ...exceptions import ValidationError
from sqlalchemy import func


@api_auth.route('/token', methods=['GET', 'POST'])
def get_auth_token():
    """Allow store a NON basic access authentication 
        is a method for an HTTP user agent to provide a 
        <b>user name</b> and <b>password </b>when 
        making a request. <br>
        <b>Description (ES):</b> Almacena en variable 
        global el usuario que se esta logeando 
        (para ser usado en toda la aplicacion) <b>g.user = user</b> 
        Validacion para verificar el usuario que 
        por primer vez se logea y ademas que viene de
        la anterior version.

    # /token <br>
    GET: Returns HTTP 200 on success; body is payload with token.
         Returns HTTP 401 bad.
    """
    try:
        username = request.json['username']
        password = request.json['password']

        user = User.find_user(username, password) ## busqueda del usuario

        if user is None:
            raise ValidationError('Tu usuario o contraseña es incorrecto')

        return jsonify({'token': user.generate_auth_token(user)})

    except KeyError as e:

        raise ValidationError('Invalid user: missing ' + e.args[0])
