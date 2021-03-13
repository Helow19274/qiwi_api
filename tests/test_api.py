import os
import unittest

from qiwi_api import Qiwi, Providers
from qiwi_api.exceptions import WrongToken


class TestApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = Qiwi(os.environ['TOKEN'])

    def test_bad_token(self):
        with self.assertRaises(WrongToken):
            Qiwi('1234')

    def test_str(self):
        self.assertEqual(
            self.api.__str__(),
            '<Wallet {}>'.format(os.environ['NUMBER'])
        )

    def test_get_profile(self):
        res = self.api.get_profile()
        self.assertIsInstance(res, dict)

        self.assertEqual(
            res['authInfo']['personId'],
            int(os.environ['NUMBER'])
        )

    def test_get_identidication(self):
        res = self.api.get_identification()
        self.assertIsInstance(res, dict)

        self.assertEqual(res['id'], int(os.environ['NUMBER']))
        self.assertEqual(res['type'], 'ANONYMOUS')

    def test_history(self):
        res = self.api.history(rows=1)
        self.assertIsInstance(res, dict)

        with self.assertRaises(ValueError):
            self.api.history(operation='wrong')

        with self.assertRaises(ValueError):
            self.api.history(sources='wrong')

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

    def test_transaction_info(self):
        res = self.api.transaction_info(os.environ['TRANSACTION'])
        self.assertIsInstance(res, dict)

        self.assertEqual(res['status'], 'SUCCESS')
        self.assertEqual(res['sum']['amount'], 1.0)

    def test_balance(self):
        res = self.api.balance()
        self.assertIsInstance(res, list)

        res2 = self.api.balance(only_balance=True)
        self.assertIsInstance(res2, list)

    def test_comission(self):
        res = self.api.comission(Providers.QIWI)
        self.assertIsInstance(res, dict)

        self.assertEqual(
            res['content']['terms']['commission']['ranges'][0]['rate'],
            0
        )

    def test_fill_form(self):
        res = self.api.fill_form(
            99,
            amount=12.74,
            comment='test comment'
        )

        url = 'https://qiwi.com/payment/form/99?amountInteger=12&' \
              'amountFraction=74&currency=643&extra%5B%27comment%27%5D=test+comment'

        self.assertEqual(res, url)

        with self.assertRaises(ValueError):
            self.api.fill_form(99, blocked='wrong')

    def test_method(self):
        res = self.api.method('person-profile/v1/profile/current')
        self.assertIsInstance(res, dict)

        self.assertEqual(res['authInfo']['personId'], int(os.environ['NUMBER']))

    def test_detect_operator(self):
        res = self.api.detect_operator(os.environ['NUMBER'])
        self.assertIsInstance(res, str)

        self.assertEqual(res, '42')

    def test_format_date(self):
        self.assertEqual(
            self.api._format_date('2018-07-28-+0300'),
            '2018-07-28T00:00:00+03:00'
        )


if __name__ == '__main__':
    unittest.main()
