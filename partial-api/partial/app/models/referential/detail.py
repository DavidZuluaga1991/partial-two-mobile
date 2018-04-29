from ... import Base, session
from sqlalchemy import String, Integer, Column, DateTime, VARBINARY, or_, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.dialects.mysql import TINYINT
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from ...exceptions import ValidationError, InternalServerError
from jose import jwt, JWSError, ExpiredSignatureError
import os
from flask import g, abort


class Detail(Base):
    """
    Detail as a public class
    """
    __tablename__ = 'details'
    detailId = Column(Integer, primary_key=True, nullable=False)
    value = Column(DECIMAL(18, 4), default=0.0)
    itemId = Column(ForeignKey('items.itemId'), index=True)


    def export_data(self):
        return {
            'detailId': self.detailId,
            'value': self.value,
            'itemId': self.itemId
        }

    def import_data(self, data):
        try:
            if 'detailId' in data:
                self.detailId = data['detailId']
            if 'value' in data:
                self.value = data['value']
            if 'itemId' in data:
                self.itemId = data['itemId']
            return self
        except KeyError as e:
            raise ValidationError("Invalid detail: missing " + e.args[0])

    @staticmethod
    def get_detail_by_id(id):
        try:
            # Consulta en la tabla details por el id
            detail = session.query(Detail).get(id)
            #retorna el objeto
            return detail
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def get_details():
        try:
            # Consulta todos los details
            details = session.query(Detail).all()
            # Retorna una lista con todos los details
            return details
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def save_detail(data):
        try:
            detail = Detail()
            # Importa los datos que vienen en el data
            detail.import_data(data)
            # Adiciona el objeto a la session
            session.add(detail)
            # Simula el guardado en la base de datos (para obtener los ids que genera la db)
            session.flush()
            # Realiza el commit en la base de datos
            session.commit()
            return detail.detailId
        except Exception as e:
            session.rollback()
            print(e)
            # Genera un error 500
            raise InternalServerError(e)

    @staticmethod
    def update_detail(id, data):
        try:
            detail = session.query(Detail).get(id)
            if detail is None:
                abort(404)
            # Importa los datos que vienen en el data
            detail.import_data(data)
            # Aadiciona el objeto a la session
            session.add(detail)
            # Simula el guardado en la base de datos (para obtener los ids que genera la db)
            session.flush()
            # Realiza el commit en la base de datos
            session.rollback()
        except Exception as e:
            session.rollback()
            print(e)
            # Genera un error 500
            raise InternalServerError(e)

    @staticmethod
    def delete_detail(id):
        try:
            detail = session.query(Detail).get(id)
            if detail is None:
                # Genera un error de 404 de no encontrado
                abort(404)
            session.delete(detail)
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)