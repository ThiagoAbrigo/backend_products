from os import environ, path
from dotenv import load_dotenv

base_dir = path.abspath(path.dirname('__file__'))
load_dotenv(path.join(base_dir, '.env'))

class config:
    #genaral configuration
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    
    #bd configuration
    user= environ.get("MYSQL_USER")
    password = environ.get("MYSQL_PASSWORD")
    host = environ.get("MYSQL_HOST")
    db = environ.get("MYSQL_DATABASE")
    
    SECRET_KEY = environ.get("SECRET_KEY")
    
    #SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = f'mysql://{user}:{password}@{host}/{db}'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_RECORS_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = 'enable'
    
    IMAGE_SERVER_BASE_URL = environ.get('IMAGE_SERVER_BASE_URL')