from .. import api
from flask import g, request, jsonify, abort
from ...models import Item


@api.route('/items/', methods=['GET'])
def get_items():
    """
    Obtiene todos los items
    :return: json con la lista de todos los items
    """
    items = Item.get_items()
    if items is None:
        abort(404)
    # Recorre la lista de items y ejecuta la funcion de export_data para convertir los datos a diccionario
    response = [i.export_data() for i in items]

    return jsonify(data=response)


@api.route('/items/<int:id>', methods=['GET'])
def get_item_by_id(id):
    """
    Obtiene item por id
    :param id: id del item
    :return: item en json
    """
    item = Item.get_item_by_id(id)
    if item is None:
        abort(404)
    # Retorna el objeto convertido en diccionario
    return jsonify(item.export_data())


@api.route('/items/', methods=['POST'])
def post_item():
    # Obtiene el json que envian desde el frontend
    data = request.json
    item_id = Item.save_item(data)
    # Crea la respuesta devolviendo el id del item
    response = jsonify({'itemId': item_id})
    # Asigna el status code 201 que es el de creado
    response.status_code = 201
    return response


@api.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    # Obtiene el json que envian desde el frontend
    data = request.json
    # Ejecuta la funcion de actualizar
    Item.update_item(id, data)
    # Crea el mensaje a devolver
    response = jsonify({'message': 'Modificado correctamente'})
    response.status_code = 201
    return response


@api.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    # Ejecuta la funcion de actualizar
    Item.delete_item(id)
    # Crea el mensaje a devolver
    return jsonify({'message': 'Eliminado correctamente'})