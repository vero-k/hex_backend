import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    UPLOAD_DIR_BASE = 'hex_be/static/images/baseimg/'
    UPLOAD_DIR_RASTER = 'hex_be/static/images/rastered/'
    UPLOAD_DIR_LEVEL = ['hex_be/static/images/levelone/', 'hex_be/static/images/leveltwo/', 'hex_be/static/images/levelthree/']
    UPLOAD_DIR_RASTER_DONE = '/static/images/rastered/'
    UPLOAD_DIR_LEVEL_DONE = ['levelone', 'leveltwo', 'levelthree']
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    database_path = os.path.join(os.pardir, 'database.db')
    # database_path_env = os.environ.get('DATABASE_URL')
    DATABASE = 'sqlite:///{}'.format(database_path)
    SECRET_KEY = os.environ.get('SECRET_KEY')

class DevConfig(Config):
    
    DEBUG = True
    #TESTING = False
    FLASK_ENV = "development"
    ENV = 'development'
    

class ProdConfig(Config):
    DEBUG = False
    #TESTING = False
    FLASK_ENV="production"
    ENV = 'production'

class TestConfig(Config):
    TESTING = True
