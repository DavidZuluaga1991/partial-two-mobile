from ... import Base, session
from sqlalchemy import String, Integer, Column, DateTime, VARBINARY, ForeignKey
from ...exceptions import ValidationError, InternalServerError
from flask import g, abort


class Item(Base):
    """
    Item as a public class
    """
    __tablename__ = 'items'
    itemId = Column(Integer, primary_key=True, nullable=False)
    code = Column(String(50), nullable=False)
    name = Column(String(200), nullable=False)

    def export_data(self):
        return {
            'itemId': self.itemId,
            'code': self.code,
            'name': self.name
        }

    def import_data(self, data):
        try:
            if 'itemId' in data:
                self.itemId = data['itemId']
            if 'code' in data:
                self.code = data['code']
            if 'name' in data:
                self.name = data['name']
            return self
        except KeyError as e:
            raise ValidationError("Invalid item: missing " + e.args[0])

    @staticmethod
    def get_item_by_id(id):
        try:
            # Consulta en la tabla items por el id
            item = session.query(Item).get(id)
            #retorna el objeto
            return item
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def get_items():
        try:
            # Consulta todos los items
            items = session.query(Item).all()
            # Retorna una lista con todos los items
            return items
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def save_item(data):
        try:
            item = Item()
            # Importa los datos que vienen en el data
            item.import_data(data)
            # Adiciona el objeto a la session
            session.add(item)
            # Simula el guardado en la base de datos (para obtener los ids que genera la db)
            session.flush()
            # Realiza el commit en la base de datos
            session.commit()
            return item.itemId
        except Exception as e:
            session.rollback()
            print(e)
            # Genera un error 500
            raise InternalServerError(e)

    @staticmethod
    def update_item(id, data):
        try:
            item = session.query(Item).get(id)
            if item is None:
                abort(404)
            # Importa los datos que vienen en el data
            item.import_data(data)
            # Aadiciona el objeto a la session
            session.add(item)
            # Simula el guardado en la base de datos (para obtener los ids que genera la db)
            session.flush()
            # Realiza el commit en la base de datos
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
            # Genera un error 500
            raise InternalServerError(e)

    @staticmethod
    def delete_item(id):
        try:
            item = session.query(Item).get(id)
            if item is None:
                # Genera un error de 404 de no encontrado
                abort(404)
            session.delete(item)
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)