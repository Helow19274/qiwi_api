import os
import unittest

from qiwi_api import Qiwi, Providers
from qiwi_api.exceptions import WrongToken


class TestApi(unittest.TestCase):
    def setUp(self):
        self.api = Qiwi(os.environ['TOKEN'])

    def test_bad_token(self):
        with self.assertRaises(WrongToken):
            Qiwi('1234')

    def test_get_profile(self):
        res = self.api.get_profile()

        self.assertIsInstance(res, dict)

        number = res['authInfo']['personId']
        self.assertEqual(number, int(os.environ['NUMBER']))
        self.assertEqual(number, self.api.number)

    def test_history(self):
        res = self.api.history(rows=1)
        self.assertIsInstance(res, dict)

        with self.assertRaises(ValueError):
            self.api.history(operation='wrong')

        with self.assertRaises(ValueError):
            self.api.history(sources='wrong')

    def test_balance(self):
        res = self.api.balance()
        self.assertIsInstance(res, list)

        res2 = self.api.balance(only_balance=True)
        self.assertIsInstance(res2, list)

        self.assertLess(len(res2), len(res))

    def test_statistics(self):
        res = self.api.statistics('2018-07-26-+0300', '2018-07-28-+0300')
        self.assertIsInstance(res, dict)

        with self.assertRaises(ValueError):
            self.api.statistics(
                '2018-07-26-+0300',
                '2018-07-28-+0300',
                operation='wrong'
            )

        with self.assertRaises(ValueError):
            self.api.statistics(
                '2018-07-26-+0300',
                '2018-07-28-+0300',
                sources='wrong'
            )

    def test_method(self):
        res = self.api.method('person-profile/v1/profile/current')
        self.assertIsInstance(res, dict)

        self.assertEqual(res['authInfo']['personId'], int(os.environ['NUMBER']))

    def test_detect_operator(self):
        res = self.api._detect_operator(os.environ['NUMBER'])
        self.assertIsInstance(res, str)

        self.assertEqual(res, '42')

    def test_comission(self):
        res = self.api.comission(Providers.QIWI)
        self.assertIsInstance(res, dict)

        self.assertEqual(
            res['content']['terms']['commission']['ranges'][0]['rate'],
            0
        )


if __name__ == '__main__':
    unittest.main()
