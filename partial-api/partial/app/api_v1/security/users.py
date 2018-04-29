from flask import request, jsonify
from . import api_security
from ...models import User


@api_security.route("/users/", methods=['POST'])
def new_user():

    result = User.new_user(request.json)
    return jsonify(result.export_data())