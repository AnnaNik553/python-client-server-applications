from mess_proj.server import process_client_message
from mess_proj.common.variables import *
import unittest


class TestServer(unittest.TestCase):

    ok_answer = {RESPONSE: 200}
    err_answer = {RESPONSE: 400, ERROR: 'Bad Request'}

    def test_no_action(self):
        self.assertEqual(process_client_message({TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_answer)

    def test_action_incorrect(self):
        self.assertEqual(process_client_message({ACTION: 'incorrect', TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_answer)

    def test_no_time(self):
        self.assertEqual(process_client_message({ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_answer)

    def test_not_guest(self):
        self.assertEqual(process_client_message({ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'not a Guest'}}), self.err_answer)

    def test_ok(self):
        self.assertEqual(process_client_message({ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}), self.ok_answer)
