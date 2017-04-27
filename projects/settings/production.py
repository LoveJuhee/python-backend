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


# Channel layer
# https://www.slideshare.net/deview/django-websocket/16?src=clipshare
redis_host = os.environ.get('REDIS_HOST', '')
redis_port_str = os.environ.get('REDIS_HOST', '0')
redis_port = int(redis_port_str)

if len(redis_host) == 0 or redis_port <= 0:
    sys.exit('redis_host or redis_port is empty.')

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(redis_host, redis_port)],
        },
        "ROUTING": "backend.routing.channel_routing",
    },
}
