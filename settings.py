import os
from dotenv import load_dotenv

load_dotenv()
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

class Config(object):
    # SECRET KEY
    SECRET_KEY = str(os.getenv('SECRET_KEY'))
    
    # DATABASE ENGINE WITH SQLALCHEMY
    ENGINE = str(os.getenv('ENGINE'))
    USER = str(os.getenv('USER'))
    PASSWORD = str(os.getenv('PASSWORD'))
    HOST = str(os.getenv('HOST'))
    NAME = str(os.getenv('NAME'))
    
    SQLALCHEMY_DATABASE_URI = ENGINE+'://'+USER+':'+PASSWORD+'@'+HOST+'/'+NAME
    # SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/db_monitoring'
    SQLALCHEMY_TRACK_MODIFICATIONS = str(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'))
    SQLALCHEMY_QUERIES_RECORD= str(os.getenv('SQLALCHEMY_QUERIES_RECORD'))
    
    # MODIFY DEFAULT CONFIG
    JSON_SORT_KEY = False
    PREFERRED_URL_SCHEME = 'https'
    
    # FLASK JWT EXTENDED
    JWT_SECRET_KEY = str(os.getenv('JWT_SECRET_KEY'))
    JWT_ACCESS_TOKEN_EXPIRES = str(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    