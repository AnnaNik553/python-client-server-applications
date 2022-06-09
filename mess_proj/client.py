"""Программа-клиент"""

import sys
import json
import socket
import argparse
import time
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message
import logging
import log.client_log_config
from decos import log

CLIENT_LOG = logging.getLogger('client_mess')


@log
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
    CLIENT_LOG.info(f'Сообщение от клиента было подготовлено: {out}')
    return out


@log
def process_ans(message):
    '''
    Функция разбирает ответ сервера
    :param message:
    :return:
    '''
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            CLIENT_LOG.info('Ответ от сервера 200 : OK')
            return '200 : OK'
        CLIENT_LOG.warning('Ответ от сервера 400')
        return f'400 : {message[ERROR]}'
    CLIENT_LOG.error('Сообщение от сервера не содержит кода состояния')
    raise ValueError


def main():
    '''Загружаем параметы коммандной строки'''
    # client.py -a 192.168.0.100 -p 8079 -m read

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', required=False, default=DEFAULT_IP_ADDRESS,
                        help='После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
    parser.add_argument('-p', type=int, required=False, default=DEFAULT_PORT,
                        help='В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
    parser.add_argument('-m', '-mode', help='mode может иметь значение read  или write')
    args = parser.parse_args()

    try:
        if args.p < 1024 or args.p > 65535:
            raise ValueError
    except ValueError:
        CLIENT_LOG.error('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Инициализация сокета и обмен

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((args.a, args.p))
    message_to_server = create_presence()
    send_message(transport, message_to_server)
    try:
        answer = process_ans(get_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        CLIENT_LOG.error('Не удалось декодировать сообщение сервера.')
        print('Не удалось декодировать сообщение сервера.')

    while True:
        if args.m == 'write':
            message = input('Введите сообщение: ')
            if message == 'exit':
                break
            transport.send(message.encode('utf-8'))
        if args.m == 'read':
            data = transport.recv(1024).decode('utf-8')
            print(data)


if __name__ == '__main__':
    main()
