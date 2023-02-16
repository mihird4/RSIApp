"""Flask config class."""
import os


class Config:
    """Base config vars."""
    SECRET_KEY = '\xe0\\t~\xd0m\x9c3;\x81\xcbq\xbc\xce\xe3Hd\xfc\x8a\x0e\x15\x94^6-CHANGETHIS'


class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    DOWNLOAD = '/var/tmp/RSIAPP'
    ENV = 'production'



class DevConfig(Config):
    DEBUG = True
    TESTING = True
    DEVELOPMENT = True
    DOWNLOAD = './RSIAPP'
    ENV= 'development'
