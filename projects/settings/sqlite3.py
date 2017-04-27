import os

from .base import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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
