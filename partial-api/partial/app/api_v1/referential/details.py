from .. import api
from flask import g, request, jsonify, abort
from ...models import Detail


@api.route('/details/', methods=['GET'])
def get_details():
    """
    Obtiene todos los details
    :return: json con la lista de todos los details
    """
    details = Detail.get_details()
    if details is None:
        abort(404)
    # Recorre la lista de details y ejecuta la funcion de export_data para convertir los datos a diccionario
    response = [i.export_data() for i in details]
    return jsonify(data=response)


@api.route('/details/<int:id>', methods=['GET'])
def get_detail_by_id(id):
    """
    Obtiene detail por id
    :param id: id del detail
    :return: detail en json
    """
    detail = Detail.get_detail_by_id(id)
    if detail is None:
        abort(404)
    # Retorna el objeto convertido en diccionario
    return jsonify(detail.export_data())


@api.route('/details/', methods=['POST'])
def post_detail():
    # Obtiene el json que envian desde el frontend
    data = request.json
    detail_id = Detail.save_detail(data)
    # Crea la respuesta devolviendo el id del detail
    response = jsonify({'detailId': detail_id})
    # Asigna el status code 201 que es el de creado
    response.status_code = 201
    return response


@api.route('/details/<int:id>', methods=['PUT'])
def update_detail(id):
    # Obtiene el json que envian desde el frontend
    data = request.json
    # Ejecuta la funcion de actualizar
    Detail.update_detail(id, data)
    # Crea el mensaje a devolver
    response = jsonify({'message': 'Modificado correctamente'})
    response.status_code = 201
    return response


@api.route('/details/<int:id>', methods=['DELETE'])
def delete_detail(id):
    # Ejecuta la funcion de actualizar
    Detail.delete_detail(id)
    # Crea el mensaje a devolver
    return jsonify({'message': 'Eliminado correctamente'})