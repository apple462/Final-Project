import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False

class LocalDevelopmentConfig():
    DEBUG = True

class ProductionConfig():
    DEBUG = False