import socket
import time
import json
import sys


sock = socket.socket()
if len(sys.argv) == 2:
    if len(sys.argv[1]) > 4:
        sock.connect((sys.argv[1], 7777))
    elif len(sys.argv[1]) == 4:
        sock.connect(('localhost', int(sys.argv[1])))
elif len(sys.argv) == 3:
    sock.connect((sys.argv[1], int(sys.argv[2])))
else:
    sock.connect(('localhost', 7777))


# сформировать presence-сообщение
def get_presence_message(username='Guest'):
    msg = {
        "action": "presence",
        "time": time.time(),
        "type": "status",
        "user": {
            "account_name": username,
            "status": "Yep, I am here!"
        }
    }
    msg_json = json.dumps(msg)
    return msg_json


# отправить сообщение серверу
def send_msg(username):
    sock.send(get_presence_message(username).encode('utf-8'))


# получить ответ сервера
def get_answer():
    data_json = sock.recv(1024).decode('utf-8')
    data = json.loads(data_json)
    if data['response'] == 200:
        return 'OK, 200'


def main():
    send_msg(username='Guest')
    message = get_answer()
    print(message)

    sock.close()


if __name__ == '__main__':
    main()
