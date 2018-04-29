from ... import Base, session
from sqlalchemy import String, Integer, Column, DateTime, VARBINARY, ForeignKey
from ...exceptions import ValidationError, InternalServerError
from flask import g, abort


class Propietary(Base):
    """
    propietary as a public class
    """
    __tablename__ = 'propietary'
    idpropietary = Column(Integer, primary_key=True, nullable=False)
    ididentification = Column(Integer, nullable=False)
    lastname = Column(String(45), nullable=False)
    frishname = Column(String(45), nullable=False)

    def export_data(self):
        return {
            'idpropietary': self.idpropietary,
            'ididentification': self.ididentification,
            'lastname': self.lastname,
            'frishname': self.frishname
        }

    def import_data(self, data):
        try:
            if 'idpropietary' in data:
                self.idpropietary = data['idpropietary']
            if 'ididentification' in data:
                self.ididentification = data['ididentification']
            if 'lastname' in data:
                self.lastname = data['lastname']
            if 'frishname' in data:
                self.frishname = data['frishname']
            return self
        except KeyError as e:
            raise ValidationError("Invalid propietary: missing " + e.args[0])

    @staticmethod
    def get_propietary_by_id(id):
        try:
            # Consulta en la tabla propietarys por el id
            propietary = session.query(Propietary).get(id)
            #retorna el objeto
            return propietary
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def get_propietarys():
        try:
            # Consulta todos los propietarys
            propietarys = session.query(Propietary).all()
            # Retorna una lista con todos los propietarys
            return propietarys
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def save_propietary(data):
        try:
            propietary = Propietary()
            # Importa los datos que vienen en el data
            propietary.import_data(data)
            # Adiciona el objeto a la session
            session.add(propietary)
            # Simula el guardado en la base de datos (para obtener los ids que genera la db)
            session.flush()
            # Realiza el commit en la base de datos
            session.commit()
            return propietary.propietaryId
        except Exception as e:
            session.rollback()
            print(e)
            # Genera un error 500
            raise InternalServerError(e)

    @staticmethod
    def update_propietary(id, data):
        try:
            propietary = session.query(Propietary).get(id)
            if propietary is None:
                abort(404)
            # Importa los datos que vienen en el data
            propietary.import_data(data)
            # Aadiciona el objeto a la session
            session.add(propietary)
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
    def delete_propietary(id):
        try:
            propietary = session.query(Propietary).get(id)
            if propietary is None:
                # Genera un error de 404 de no encontrado
                abort(404)
            session.delete(propietary)
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)