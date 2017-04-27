import logging
import os

from django.utils import timezone


class SingletonType(type):
    def __call__(cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(
                SingletonType, cls).__call__(*args, **kwargs)
            return cls.__instance


class CustomLogger(object):
    __metaclass__ = SingletonType
    _logger = None

    def __init__(self):
        self._logger = logging.getLogger("crumbs")
        self._logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s'
        )

        now = timezone.now()

        dirname = './logs'
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        fileHandler = logging.FileHandler(
            dirname + "/" + now.strftime("%Y%m%d_%H%M%S_%Z") + ".log")
        streamHandler = logging.StreamHandler()

        fileHandler.setFormatter(formatter)
        streamHandler.setFormatter(formatter)

        self._logger.addHandler(fileHandler)
        self._logger.addHandler(streamHandler)

    def get_logger(self):
        return self._logger
