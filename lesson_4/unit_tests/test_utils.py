from lesson_4.common.utils import *
from lesson_4.common.variables import *
import unittest


# Тестовый класс для тестирования отправки и получения, при создании требует словарь, который будет прогонятся
# через тестовую функцию
class TestSocket:
    def __init__(self, test_dict):
        self.testdict = test_dict

    # тестовая функция отправки, корретно  кодирует сообщение, так-же сохраняет что должно было отправлено в сокет.
    def send(self, message_to_send):
        json_test_message = json.dumps(self.testdict)
        self.encoded_message = json_test_message.encode(ENCODING)
        self.receved_message = message_to_send

    def recv(self, max_len):
        json_test_message = json.dumps(self.testdict)
        return json_test_message.encode(ENCODING)


# Тестовый класс, собственно выполняющий тестирование.
class Tests(unittest.TestCase):
    test_dict_send_from_client = {
        ACTION: PRESENCE,
        TIME: 111111.111111,
        USER: {
            ACCOUNT_NAME: 'test_test'
        }
    }
    test_dict_send_from_server_ok = {RESPONSE: 200}
    test_dict_send_from_server_err = {RESPONSE: 400, ERROR: 'Bad Request'}

    test_dict_recv_ok = {RESPONSE: 200}
    test_dict_recv_err = {RESPONSE: 400, ERROR: 'Bad Request'}

    test_dict_recv_from_client = {
        ACTION: PRESENCE,
        TIME: 111111.111111,
        USER: {
            ACCOUNT_NAME: 'test_test'
        }
    }

    # тестируем корректность работы фукции отправки,создадим тестовый сокет и проверим корректность отправки словаря
    def test_send_message_from_client(self):
        # экземпляр тестового словаря, хранит собственно тестовый словарь
        test_socket = TestSocket(self.test_dict_send_from_client)
        # вызов тестируемой функции, результаты будут сохранены в тестовом сокете
        send_message(test_socket, self.test_dict_send_from_client)
        # проверка корретности кодирования словаря.
        self.assertEqual(test_socket.encoded_message, test_socket.receved_message)

    def test_send_message_from_server_ok(self):
        test_socket = TestSocket(self.test_dict_send_from_server_ok)
        send_message(test_socket, self.test_dict_send_from_server_ok)
        self.assertEqual(test_socket.encoded_message, test_socket.receved_message)

    def test_send_message_from_server_err(self):
        test_socket = TestSocket(self.test_dict_send_from_server_err)
        send_message(test_socket, self.test_dict_send_from_server_err)
        self.assertEqual(test_socket.encoded_message, test_socket.receved_message)

    # тест функции приёма сообщения
    def test_get_message_from_server_ok(self):
        test_sock_ok = TestSocket(self.test_dict_recv_ok)
        # тест корректной расшифровки корректного словаря
        self.assertEqual(get_message(test_sock_ok), self.test_dict_recv_ok)

    def test_get_message_from_server_err(self):
        test_sock_err = TestSocket(self.test_dict_recv_err)
        # тест корректной расшифровки ошибочного словаря
        self.assertEqual(get_message(test_sock_err), self.test_dict_recv_err)

    def test_get_message_from_client(self):
        test_socket = TestSocket(self.test_dict_recv_from_client)
        self.assertEqual(get_message(test_socket), self.test_dict_recv_from_client)

    def test_get_message_value_error(self):
        test_socket = TestSocket('')
        self.assertRaises(ValueError, get_message, test_socket)


if __name__ == '__main__':
    unittest.main()
