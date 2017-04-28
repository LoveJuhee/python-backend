import json

from channels import Group
from channels.sessions import channel_session

from ntm.utils.logger import CustomLogger
from ntm.utils.web_socket import WebSocketUtil

from .models import Center

log = CustomLogger().get_logger()


def __get_group(label, channel_layer):
    return Group('chat-' + label, channel_layer=channel_layer)


@channel_session
def ws_connect(message):
    try:
        prefix, label, id = message['path'].strip('/').split('/')
        if prefix != 'chat':
            log.debug('invalid ws path=%s', message['path'])
            return
        center = Center.objects.get(label=label)
        key = str(message.reply_channel)
        consumer = WebSocketUtil.append(label, key, id)
        log.debug('append consumer:%s', consumer)
    except ValueError as e:
        log.debug('invalid ws path=%s', message['path'])
        return

    message.reply_channel.send({"accept": True})
    __get_group(label, message.channel_layer).add(message.reply_channel)

    message.channel_session['center'] = center.label


@channel_session
def ws_receive(message):
    try:
        label = message.channel_session['center']
        center = Center.objects.get(label=label)
        log.debug('label:%s, center.name:%s', label, center.name)
    except KeyError:
        log.debug('no center in channel_session')
        return
    except Center.DoesNotExist:
        log.debug('recieved message, but center does not exist label=%s', label)
        return

    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", message['text'])
        return

    if set(data.keys()) != set(('handle', 'message')):
        log.debug('ws message unexpected format data=%s', data)
        return

    if data:
        log.debug('chat message center=%s handle=%s message=%s',
                  center.label, data['handle'], data['message'])
        m = center.messages.create(**data)

        group = __get_group(label, message.channel_layer)
        group.send({'text': json.dumps(m.as_dict())})


@channel_session
def ws_disconnect(message):
    try:
        label = message.channel_session['center']
        # center = Center.objects.get(label=label)
        group = __get_group(label, message.channel_layer)
        group.discard(message.reply_channel)

        key = str(message.reply_channel)
        consumer = WebSocketUtil.discard(label, key)
        if consumer is None:
            log.debug('discard consumer is None')
            return

        data = {
            'message': consumer.name + ' is disconnected.'
        }
        group.send({'text': json.dumps(data)})
    except (KeyError, Center.DoesNotExist):
        pass
