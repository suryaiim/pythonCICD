import os
import pprint
import socket
import logging
from flask import request, Flask
from flask.logging import default_handler


class BaseRepr(object):
    ''' Simple class repr '''
    def __repr__(self):
        return "<{name} @{id:x}:\n{attrs}>".format(
            name=self.__class__.__name__, id=id(self) & 0xFFFFFF,
            attrs = pprint.pformat(self.__dict__)
            )

class Config(BaseRepr):
    #BASE_HOST='localhost.localdomain'
    BASE_HOST='localhost'

    APP_NAME = "devops_test"

    #Set the cookie domain to only operate within the <mountpoint> subdomain
    MOUNTPOINT = os.getenv("MOUNTPOINT", None)
    SUBMOUNT_URL = os.getenv("SUBMOUNT_URL", "")

    APPLICATION_ROOT = MOUNTPOINT + SUBMOUNT_URL

    assert APPLICATION_ROOT != None
    assert APPLICATION_ROOT != ''

    SESSION_COOKIE_NAME = os.getenv('SESSION_COOKIE_NAME', 'session_test')
    API_VERSION = os.getenv('API_VERSION', '0.1')

    # Environment Variables below:
    APP_PORT = int(os.getenv('APP_PORT', 80))

    #TODO add logic for when we want to split back and front end instances.
    API_ENDPOINT = "http://{BASE_HOST}:{APP_PORT}{APPLICATION_ROOT}/api/{API_VERSION}".format(
            BASE_HOST=BASE_HOST,
            APP_PORT=APP_PORT,
            APPLICATION_ROOT = APPLICATION_ROOT,
            API_VERSION=API_VERSION )


    # Flask settings
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    # WTForms settings
    WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY', 'wtf_secret' )

    PROPAGATE_EXCEPTIONS = True

    #Generate key on startup, this signs the cookie the cookie is NOT ENCRYPTED
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret' )

    # (Default) Flask Restplus settings
    SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    ERROR_404_HELP = False

    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True

    DEBUG = False

    ''' jsonify responses will be output with newlines, spaces, and indentation for easier reading by humans. Always enabled in debug mode'''
    JSONIFY_PRETTYPRINT_REGULAR = True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = True

class IntegrationConfig(TestingConfig):
    ...

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SUBMOUNT_URL = ''

class DEVConfig(Config):
    DEBUG = True
    TESTING = False #Do we populate test data?
    SUBMOUNT_URL = '/dev' # needs forward slash at the front


class UATConfig(Config):
    DEBUG = True
    TESTING = False #Do we populate test data?
    SUBMOUNT_URL = '/uat' # needs forward slash at the front


class DebugConfig(ProductionConfig):
    DEBUG = True

"""
The config is applied by the app using the ENVIRONMENT environment variable
It will default to dev if not found: ENVIRONMENT=os.getenv("ENVIRONMENT", "dev")
And applies the config via: server.config.from_object(config_by_name[ENVIRONMENT])
"""
config_by_name = {
        'dev':DEVConfig,
        'uat':UATConfig,
        'testing':TestingConfig,
        'integration': IntegrationConfig,
        'prod':ProductionConfig
        }

ENVIRONMENT = os.getenv("ENVIRONMENT")
app_config = config_by_name[ENVIRONMENT]
