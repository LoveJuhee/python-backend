import os

from .base import *

DEBUG = False

db_name = os.getenv('PRODUCT_DB_NAME')
db_user = os.getenv('PRODUCT_DB_USER')
db_pass = os.getenv('PRODUCT_DB_PASS')
db_host = os.getenv('PRODUCT_DB_HOST')
db_port = os.getenv('PRODUCT_DB_PORT', '')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'LOCAL_DB_NAME',
        'USER': 'LOCAL_DB_USER',
        'PASSWORD': 'LOCAL_DB_PASSWORD',
        'HOST': 'LOCAL_DB_HOST',
        'PORT': 'LOCAL_DB_PORT',
    }
}
