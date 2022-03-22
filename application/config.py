import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = "zkjdauhi75763hs"
    SQLALCHEMY_DATABASE_URI = "sqlite:///quantifiedself.sqlite3"

class LocalDevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False