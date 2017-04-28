from ntm.utils.logger import CustomLogger
from ntm.utils.object import ObjectUtil
from django.utils import timezone

log = CustomLogger.__call__().get_logger()


class Consumer(object):
    key = None
    name = None
    created_at = None

    def __init__(self, key, name):
        self.key = key
        self.name = name
        self.created_at = timezone.now()


class _WebSocketManager:
    _groups = None

    def __init__(self):
        self._groups = []

    def _get_group(self, group_id):
        for group in self._groups:
            if group['id'] == group_id:
                return group
        return self._append_group(group_id)

    def _get_consumer(self, group, key):
        if ObjectUtil.is_null_or_empty(group, key):
            return None
        for consumer in group['consumers']:
            log.debug('key1:%s, key2:%s', key, consumer.key)
            if consumer.key == key:
                return consumer
        return None

    def _append_group(self, group_id):
        log.debug('append_group:%s', group_id)
        group = {'id': group_id, 'consumers': []}
        self._groups.append(group)
        return group

    def get_manager(self):
        return self

    def append_user(self, group_id, key, name):
        group = self._get_group(group_id)
        append_consumer = Consumer(key, name)
        group['consumers'].append(append_consumer)
        log.debug('append_user {key:%s, name:%s}',
                  append_consumer.key, append_consumer.name)
        return append_consumer

    def discard_user(self, group_id, key):
        group = self._get_group(group_id)
        remove_consumer = self._get_consumer(group, key)
        if group is None or remove_consumer is None:
            return None
        group['consumers'].remove(remove_consumer)
        log.debug('discard_user {key:%s, name:%s}',
                  remove_consumer.key, remove_consumer.name)
        return remove_consumer


_manager = _WebSocketManager()


class WebSocketUtil(object):

    @staticmethod
    def append(group_id, key, name):
        if ObjectUtil.is_null_or_empty(group_id, key, name):
            return -1
        return _manager.append_user(group_id, key, name)

    def discard(group_id, key):
        if ObjectUtil.is_null_or_empty(group_id, key):
            return -1
        return _manager.discard_user(group_id, key)
