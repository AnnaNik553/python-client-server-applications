from mess_proj.client import create_presence, process_ans
from mess_proj.common.variables import *
import unittest
import os

os.chdir(os.path.abspath(os.path.join(os.getcwd(), "..")))


# Класс с тестами
class TestClass(unittest.TestCase):
    # тест коректного запроса
    def test_def_presence(self):
        test = create_presence()
        test[TIME] = 1.1  # время необходимо приравнять принудительно иначе тест никогда не будет пройден
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_def_presence_action(self):
        test = create_presence()
        test_action = test[ACTION]
        self.assertEqual(test_action, 'presence')

    def test_def_presence_user(self):
        test = create_presence()
        test_user = test[USER]
        self.assertEqual(test_user, {ACCOUNT_NAME: 'Guest'})

    # тест корректтного разбора ответа 200
    def test_200_ans(self):
        self.assertEqual(process_ans({RESPONSE: 200}), '200 : OK')

    # тест корректного разбора 400
    def test_400_ans(self):
        self.assertEqual(process_ans({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')

    # тест исключения без поля RESPONSE
    def test_no_response(self):
        self.assertRaises(ValueError, process_ans, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
