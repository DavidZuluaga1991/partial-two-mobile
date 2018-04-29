import os
from flask import g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import Dotenv
from .utils import validator
from .utils import email

dotenv_path = Dotenv(os.path.join(os.getcwd(), ".env.example"))
os.environ.update(dotenv_path)

db_setup = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(
    os.environ.get("USERNAME"),
    os.environ.get("PASSWORD"),
    os.environ.get("HOST"),
    os.environ.get("PORT"),
    os.environ.get("DATABASE")
)

engine = create_engine(db_setup, echo=True)
Session = sessionmaker(bind=engine, expire_on_commit=True, autoflush=False)
session = Session()

Base = declarative_base()


def create_app(app):
    """This function create an application instance.
       :param app: flask instance over create blueprint instance
       :type app: Flask instance. 
    """
    Base.metadata.create_all(engine)

    # register blueprints
    from .api_v1 import api as api_blueprint
    from .api_v1.security import api_security
    from .api_v1.auth import api_auth

    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    app.register_blueprint(api_auth, url_prefix="/oauth")
    app.register_blueprint(api_security, url_prefix="/api_security/v1")

    validator(Base)
    #email(Base)
    # register an after request handler
    # @app.after_request
    # def after_request(rv):
    #     headers = getattr(g, 'headers', {})
    #     rv.headers.extend(headers)
    #     return rv
    return app
