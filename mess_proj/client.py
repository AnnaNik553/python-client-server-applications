"""Программа-клиент"""

import sys
import json
import socket
import time
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message
import logging
import log.client_log_config

CLIENT_LOG = logging.getLogger('client_mess')


def create_presence(account_name='Guest'):
    '''
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    '''
    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOG.info('A message from the client has been prepared')
    return out


def process_ans(message):
    '''
    Функция разбирает ответ сервера
    :param message:
    :return:
    '''
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            CLIENT_LOG.info('Response from the server 200 : OK')
            return '200 : OK'
        CLIENT_LOG.warning('Response from the server 400')
        return f'400 : {message[ERROR]}'
    CLIENT_LOG.error('The message from the server does not contain the code')
    raise ValueError


def main():
    '''Загружаем параметы коммандной строки'''
    # client.py 192.168.0.100 8079
    try:
        server_address = sys.argv[2]
        server_port = int(sys.argv[3])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        CLIENT_LOG.error('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Инициализация сокета и обмен

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    message_to_server = create_presence()
    send_message(transport, message_to_server)
    try:
        answer = process_ans(get_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        CLIENT_LOG.error('Не удалось декодировать сообщение сервера.')
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
