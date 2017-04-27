import os
import sys

from .base import *

DEBUG = False


db_name = os.getenv('PRODUCT_DB_NAME', '')
db_user = os.getenv('PRODUCT_DB_USER', '')
db_pass = os.getenv('PRODUCT_DB_PASS', '')
db_host = os.getenv('PRODUCT_DB_HOST', '')
db_port = os.getenv('PRODUCT_DB_PORT', '')

ALLOWED_HOSTS = PRODUCT_ALLOWED_HOSTS

if len(db_name) == 0 or len(db_user) == 0 or len(db_pass) == 0 \
        or len(db_host):
    sys.exit('db_name or db_user or db_pass or db_host is empty.')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': db_name,
        'USER': db_user,
        'PASSWORD': db_pass,
        'HOST': db_host,
        'PORT': db_port,
    }
}
