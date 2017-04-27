import json

from channels import Group
from channels.sessions import channel_session

from ne.utils.logger import CustomLogger

from .models import Center

log = CustomLogger.__call__().get_logger()


def __get_group(label, channel_layer):
    return Group('chat-' + label, channel_layer=channel_layer)


@channel_session
def ws_connect(message):
    try:
        prefix, label = message['path'].strip('/').split('/')
        if prefix != 'chat':
            log.debug('invalid ws path=%s', message['path'])
            return
        room = Center.objects.get(label=label)
    except ValueError as e:
        log.debug('invalid ws path=%s', message['path'])
        return

    log.debug('chat connect room=%s client=%s:%s path=%s reply_channel=%s',
              room.label, message['client'][0], message['client'][1],
              message['path'], message.reply_channel)

    message.reply_channel.send({"accept": True})
    __get_group(label, message.channel_layer).add(message.reply_channel)

    message.channel_session['room'] = room.label


@channel_session
def ws_receive(message):
    try:
        label = message.channel_session['room']
        room = Center.objects.get(label=label)
        log.debug('label=%s, room=%s', label, room)
    except KeyError:
        log.debug('no room in channel_session')
        return
    except Center.DoesNotExist:
        log.debug('recieved message, but room does not exist label=%s', label)
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
        log.debug('chat message room=%s handle=%s message=%s',
                  room.label, data['handle'], data['message'])
        m = room.messages.create(**data)

        group = __get_group(label, message.channel_layer)
        group.send({'text': json.dumps(m.as_dict())})


@channel_session
def ws_disconnect(message):
    try:
        label = message.channel_session['room']
        # room = Center.objects.get(label=label)
        group = __get_group(label, message.channel_layer)
        group.discard(message.reply_channel)
    except (KeyError, Center.DoesNotExist):
        pass
