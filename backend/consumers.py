import json

from channels import Group
from channels.sessions import channel_session

from ntm.utils.logger import CustomLogger

from .models import Center

log = CustomLogger.__call__().get_logger()

accounts = []


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
        account = {'id': id, 'key': str(message.reply_channel)}
        accounts.append(account)
    except ValueError as e:
        log.debug('invalid ws path=%s', message['path'])
        return

    log.debug('chat connect center=%s client=%s:%s path=%s reply_channel=%s',
              center.label, message['client'][0], message['client'][1],
              message['path'], message.reply_channel)

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
        center = Center.objects.get(label=label)
        group = __get_group(label, message.channel_layer)
        group.discard(message.reply_channel)

        log.debug('label:%s, channel_layer:%s, center.name:%s',
                  label,
                  message.channel_layer,
                  center.name)

        key = str(message.reply_channel)
        for tmp in accounts:
            if tmp['key'] == key:
                account = tmp
                break
        accounts.remove(account)
        log.debug('account size: %d', len(accounts))

        data = {
            'message': account['id'] + ' is disconnected.'
        }

        group.send({'text': json.dumps(data)})
    except (KeyError, Center.DoesNotExist):
        pass
