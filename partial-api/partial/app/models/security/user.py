from ... import Base, session
from sqlalchemy import String, Integer, Column, DateTime, VARBINARY, or_, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.dialects.mysql import TINYINT
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from ...exceptions import ValidationError, InternalServerError
from jose import jwt, JWSError, ExpiredSignatureError
import os
from flask import g, abort


class User(Base):
    """User as a public model class.

    note::

    """
    __tablename__ = 'users'

    userId = Column(Integer, primary_key=True, nullable=False)
    userName = Column(String(512), default=None, nullable=False)
    passwordHash = Column(String(2000), default=None, nullable=True)

    def export_data(self):
        """
        Allow export user data
        :return:  user object in JSON format
        """
        return {
            "userId": self.userId,
            "userName": self.userName,
        }

    def import_data(self, data):
        """
        Allow create un ner user from user data directly
        :param data: information by new user
        :exception: ValidationError An error occurs
        :return: user object create in JOSN format
        """
        try:
            if 'userId' in data:
                self.userId = data["userId"]
            if 'userName' in data:
                self.userName = data["userName"]
            return self
        except KeyError as e:
            raise ValidationError("Invalid user: missing " + e.args[0])

    def set_password(self, password):
        """
        Allow set a new password hash according to input text seed
        :param password: seed to generate password
        :return: hash password
        """
        self.passwordHash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Allow validate a according to input seed and hash store by user
        :param password: seed to generate validate password
        :return: boolean status
        """
        if self.passwordHash is None:
            return False
        return check_password_hash(self.passwordHash, password)

    def change_password(self, old_password, new_password):
        """
        Allow change password
        :param old_password: old hash password
        :param new_password: new hash password
        :raise: An error occurs when a old an new passwords no match
        :return: none wheter is changed, raise otherwise
        """
        if check_password_hash(self.passwordHash, old_password):
            self.set_password(new_password)
        else:
            raise ValidationError("Las contraseñas no coiniciden")

    @staticmethod
    def find_user(username, password):
        """
        Allow find an user from username and password
        :param username: username by user to search
        :param password:  password hash by user to search
        :return: user object or None otherwise
        """
        try:
            user = session.query(User).filter(User.userName == username).first()
            if user is None:
                return None
            if user.verify_password(password):
                return user
            else:
                return None
        except Exception as e:
            print(e)
            session.rollback()
            raise InternalServerError(e)

    def generate_auth_token(self, user):
        """
        Allow generate a token by un new user
        :param user: full user data
        :return: string token
        """
        payload = {
            "sub": str(user.userId),
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(days=1),
            "name": str(user.userName)
        }
        token = jwt.encode(payload, os.environ.get("SECRET_KEY"), algorithm="HS256")
        return token

    @staticmethod
    def verify_auth_token(token):
        """
        Allow validate a user according a yours token
        :param token: token to validate
        :raise: ValidationError an error occurs when no auth token faile
        :return: token encode or 401 unauthorized
        """
        if token is None or token == "":
            return None
        try:
            jw = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=["HS256"])
            g.user = jw
            return jw
        except JWSError as e:
            raise ValidationError(e)
        except ExpiredSignatureError as e:
            return None
        except Exception as e:
            return None

    @staticmethod
    def get_user(id):
        """
        Allow obtain a user for to give identifier

        :param id: user indentifier
        :return: User object
        """
        return session.query(User).filter_by(userId=id).one_or_none()

    @staticmethod
    def new_user(data):
        """
        Allow creata an new user<br/> Metodo para creacion de usaurios
        :param data: information by new user
        :exception: An error occurs when server or database no allow user.
        :return:
        """
        try:
            user = User()

            # carga inicial de los campos que son requeridos
            user.import_data(data)
            user_exist = session.query(User).filter(User.userName == user.userName).all()
            if len(user_exist):
                raise InternalServerError('El usuario ya existe')
            user.set_password(data['password'])
            session.add(user)

            session.commit()

            return user
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def update_user(id, data):
        """
            Allow update a user live user
            :param id: identifier by user
            :param data: user information
            :return: status code and results
        """
        try:
            user = session.query(User).get(id)
            user.import_data(data)
            user.set_password(data['password'])
            session.add(user)
            session.commit()

            return {}, 200, {}
        except KeyError as e:
            return {"error": str(e)}, 500, {}
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def delete_user(id):
        """
        Allow delet a user according to identifier
        :param id: identifier by user to delete
        :return: status code and result
        """
        try:
            user = session.query(User).get(id)
            if user is not None:
                session.delete(user)
                session.commit()
                return {}, 200, {}
            else:
                return {}, 404, {}
        except Exception as e:
            return {"error": str(e)}, 500, {}
