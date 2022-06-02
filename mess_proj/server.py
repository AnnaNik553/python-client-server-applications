"""Программа-сервер"""

import socket
import sys
import json
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from common.utils import get_message, send_message
import logging
import log.server_log_config

SERVER_LOG = logging.getLogger('server_mess')

def process_client_message(message):
    '''
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента

    :param message:
    :return:
    '''
    SERVER_LOG.info('Entered the function "process_client_message()"')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        SERVER_LOG.info('Message is valid')
        return {RESPONSE: 200}
    SERVER_LOG.warning('Message is not valid!')
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    '''
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 8079 -a 192.168.0.100
    :return:
    '''

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        SERVER_LOG.error('После параметра -\'p\' необходимо указать номер порта.')
        print('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        SERVER_LOG.error('В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        print(
            'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Затем загружаем какой адрес слушать

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''

    except IndexError:
        SERVER_LOG.error('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        print(
            'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    # Готовим сокет

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((listen_address, listen_port))

    # Слушаем порт

    server_socket.listen(MAX_CONNECTIONS)

    while True:
        client_socket, client_address = server_socket.accept()
        SERVER_LOG.info('The connection with the client is open')
        try:
            message_from_cient = get_message(client_socket)
            print(message_from_cient)
            # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
            response = process_client_message(message_from_cient)
            send_message(client_socket, response)
            client_socket.close()
            SERVER_LOG.info('The connection with the client is closed')
        except (ValueError, json.JSONDecodeError):
            SERVER_LOG.error('Принято некорретное сообщение от клиента.')
            print('Принято некорретное сообщение от клиента.')
            client_socket.close()
            SERVER_LOG.info('The connection with the client is closed')


if __name__ == '__main__':
    main()
