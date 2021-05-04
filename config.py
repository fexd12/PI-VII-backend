import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'development.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_SERVER =  os.environ.get('DB_SERVER')
    DB_DATABASE = os.environ.get('DB_DATABASE')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWD = os.environ.get('DB_PASSWD')

    SQLALCHEMY_DATABASE_URI = 'postgresql://{}/{}?user={}&password={}' \
            .format(DB_SERVER,DB_DATABASE,DB_USER,DB_PASSWD)
    # print(SQLALCHEMY_DATABASE_URI)

class ProductionConfig(Config):
    DB_SERVER = os.environ.get('DB_SERVER_PROD')