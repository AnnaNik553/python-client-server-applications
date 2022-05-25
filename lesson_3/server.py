import json
import socket
import sys

sock = socket.socket()

if len(sys.argv) > 1:
    if '-p' in sys.argv and '-a' in sys.argv:
        sock.bind((sys.argv[sys.argv.index('-a') + 1], int(sys.argv[sys.argv.index('-p') + 1])))
    elif '-p' in sys.argv:
        sock.bind(('', int(sys.argv[sys.argv.index('-p') + 1])))
    elif '-a' in sys.argv:
        sock.bind((sys.argv[sys.argv.index('-a') + 1], 7777))
else:
    sock.bind(('', 7777))
sock.listen(1)


# формирует ответ клиенту
def get_message(code, alert=None, error=None, ):
    msg = {
        "response": code
    }
    if alert is not None:
        msg['alert'] = alert
    if error is not None:
        msg['error'] = error
    msg_json = json.dumps(msg)
    return msg_json


def main():
    while True:
        conn, addr = sock.accept()
        # принимает сообщение клиента
        data_json = conn.recv(1024).decode('utf-8')
        data = json.loads(data_json)
        print(data)
        # отправляет ответ клиенту
        if data['action'] == 'presence':
            conn.send(get_message(200).encode('utf-8'))

        conn.close()


if __name__ == '__main__':
    main()
