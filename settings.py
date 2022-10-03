from datetime import timedelta
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
    JSON_SORT_KEYS = False
    PREFERRED_URL_SCHEME = 'https'
    
    # JSON
    JWT_SECRET_KEY = str(os.getenv('JWT_SECRET_KEY'))
    ACCESS_EXPIRE = timedelta(hours=1)
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRE
    
    