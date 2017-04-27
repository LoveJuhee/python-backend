import os

from .base import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

db_name = os.getenv('LOCAL_DB_NAME', 'backend')
db_user = os.getenv('LOCAL_DB_USER', 'backend')
db_pass = os.getenv('LOCAL_DB_PASS', 'atm@px10')
db_host = os.getenv('LOCAL_DB_HOST', 'localhost')
db_port = os.getenv('LOCAL_DB_PORT', '')

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
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port_str = os.environ.get('REDIS_HOST', '6379')
redis_port = int(redis_port_str)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(redis_host, redis_port)],
        },
        "ROUTING": "backend.routing.channel_routing",
    },
}
