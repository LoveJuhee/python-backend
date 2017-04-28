import re
from pprint import pprint

from channels import Group
from channels.auth import (channel_session_user,
                           channel_session_user_from_http, http_session_user)
from channels.generic.websockets import JsonWebsocketConsumer
from channels.sessions import channel_session
from django.utils.decorators import method_decorator

from ntm.utils.logger import log


class LobbyConsumer(JsonWebsocketConsumer):

    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True
    _group = 'lobby'

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        log.debug('adding to connection group lobby. id:%s', kwargs['id'])
        # self.send({'accept': True})
        return [self._group]

    def connect(self, message, **kwargs):
        """
        Perform things on connection start
        """
        pass

    def receive(self, content, **kwargs):
        """
        Called when a message is received with either text or bytes
        filled out.
        """
        pass

    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        pass
