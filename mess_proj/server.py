"""Программа-сервер"""
import argparse
import socket
import select
import sys
import json
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, DEFAULT_IP_ADDRESS
from common.utils import get_message, send_message
import logging
import log.server_log_config
from decos import log

SERVER_LOG = logging.getLogger('server_mess')


def get_address_and_port():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', required=False, default=DEFAULT_IP_ADDRESS,
                        help='После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
    parser.add_argument('-p', type=int, required=False, default=DEFAULT_PORT,
                        help='В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
    args = parser.parse_args()

    try:
        if args.p < 1024 or args.p > 65535:
            raise ValueError
    except ValueError:
        SERVER_LOG.error('В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        print(
            'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    return args.a, args.p


@log
def process_client_message(message):
    '''
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента

    :param message:
    :return:
    '''
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        SERVER_LOG.info('Сообщение корректно')
        return {RESPONSE: 200}
    SERVER_LOG.warning('Сообщение не корректно!')
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


@log
def read_requests(read_list, clients):

    responses = []
    for sock in read_list:
        try:
            message = sock.recv(1024).decode('utf-8')
            responses.append(message)
        except:
            print(f'Клиент {sock.fileno()} {sock.getpeername()}отключился')
            clients.remove(sock)
    return responses


@log
def write_response(requests, write_list, clients):
    for sock in write_list:
            try:
                for data in requests:
                    sock.send(data.encode('utf-8'))
            except:
                print(f'Клиент {sock.fileno()} {sock.getpeername()}отключился')
                sock.cloce()
                clients.remove(sock)


def main():
    '''
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 8079 -a 192.168.0.100
    :return:
    '''
    clients = []

    # Готовим сокет

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(get_address_and_port())
    print('Сервер запущен!')

    # Слушаем порт

    server_socket.listen(MAX_CONNECTIONS)
    server_socket.settimeout(0.2)

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            SERVER_LOG.info(f'Соединение с клиентом {client_address} установлено')
        except OSError:
            pass
        else:
            if client_socket not in clients:
                try:
                    message_from_cient = get_message(client_socket)
                    print(message_from_cient)
                    response = process_client_message(message_from_cient)
                    send_message(client_socket, response)
                except (ValueError, json.JSONDecodeError):
                    SERVER_LOG.error('Принято некорретное сообщение от клиента.')
                    print('Принято некорретное сообщение от клиента.')
                    client_socket.close()
                    SERVER_LOG.info('Соединение с клиентом закрыто')
            clients.append(client_socket)
        finally:
            wait = 0
            read_list = []
            write_list = []
            try:
                read_list, write_list, err = select.select(clients, clients, [], wait)
            except:
                pass

            requests = read_requests(read_list, clients)

            if requests:
                write_response(requests, write_list, clients)


if __name__ == '__main__':
    main()
