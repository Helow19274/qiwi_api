# -*- coding: utf-8 -*-
import json
import datetime

import requests

from .enums import OPERATIONS, SOURCES, Providers
from .exceptions import ApiError, WrongToken, PermissionError


class Qiwi(object):
    """ Класс для работы с Qiwi API

    `Получить ключ
    <https://qiwi.com/api>`_

    `Подробнее об API
    <https://developer.qiwi.com/ru/qiwi-wallet-personal>`_

    :param token: Ключ доступа к api
    :type token: str
    """
    __slots__ = ('session', 'number')

    def __init__(self, token):
        self.session = requests.Session()
        self.session.headers['Accept'] = 'application/json'
        self.session.headers['Content-Type'] = 'application/json'
        self.session.headers['Authorization'] = 'Bearer {}'.format(token)

        self.number = self.get_profile(True, False, False)['authInfo']['personId']

    def __str__(self):
        return '<Wallet {}>'.format(self.number)

    def __del__(self):
        self.session.close()

    def get_profile(self, auth_info=True, contract_info=True, user_info=True):
        """ Получить информацию о профиле

        :param auth_info: Информация об авторизации
        :type auth_info: bool

        :param contract_info: Информация о кошельке
        :type contract_info: bool

        :param user_info: Прочие данные
        :type user_info: bool
        """

        url = 'person-profile/v1/profile/current'
        payload = {
            'authInfoEnabled': auth_info,
            'contractInfoEnabled': contract_info,
            'userInfoEnabled': user_info
        }

        return self.method(url, payload)

    def get_identification(self):
        """ Данные идентификации """

        url = 'identification/v1/persons/{}/identification'

        return self.method(url.format(self.number))

    def identification(self, birth_date, first_name, middle_name, last_name,
                       passport, inn=None, snils=None, oms=None):
        """ Упрощённая идентификация

        :param birth_date: Дата рождения в формате ГГГГ-ММ-ДД
        :type birth_date: str

        :param first_name: Имя
        :type first_name: str

        :param middle_name: Отчество
        :type middle_name: str

        :param last_name: Фамилия
        :type last_name: str

        :param passport: Серия и номер паспорта (цифры без пробела)
        :type passport: str

        :param inn: ИНН
        :type inn: str

        :param snils: СНИЛС
        :type snils: str

        :param oms: ОМС
        :type oms: str
        """

        url = 'identification/v1/persons/{}/identification'
        payload = {
            'birthDate': birth_date,
            'firstName': first_name,
            'middleName': middle_name,
            'lastName': last_name,
            'passport': passport,
            'inn': inn,
            'snils': snils,
            'oms': oms
        }

        return self.method(url.format(self.number), payload, 'post')

    def history(self, rows=10, operation='ALL', sources=None, from_date=None,
                to_date=None, next_txn_date=None, next_txn_id=None):
        """ Получить историю транзакций.

        Ограничение - 100 запросов в минуту.

        :param rows: Число транзакций. Максимальное количество - 50
        :type rows: int

        :param operation: Тип операций, учитываемых при подсчете статистики.
            см. OPERATIONS
        :type operation: str

        :param sources: Источники платежа, учитываемые при подсчете статистики
        :type sources: list or str

        :param from_date: Начальная дата периода статистики.
            ГГГГ-ММ-ДД-<часовой пояс>. Указывается так:
            +0000(UTC), +0300(Москва) и т.д.
        :type from_date: str

        :param to_date: Конечная дата периода статистики.
            ГГГГ-ММ-ДД-<часовой пояс>
        :type to_date: str

        :param next_txn_date: Дата транзакции для отсчета от предыдущего списка.
            Используется только вместе с nextTxnId
        :type next_txn_date: str

        :param next_txn_id: Номер транзакции для отсчета от предыдущего списка.
            Используется только вместе с nextTxnDate
        :type next_txn_id: int
        """

        if sources is None:
            sources = []
        elif not isinstance(sources, list):
            sources = [sources]

        url = 'payment-history/v2/persons/{}/payments'
        payload = {
            'rows': rows,
            'operation': operation,
            'startDate': self._format_date(from_date),
            'endDate': self._format_date(to_date),
            'nextTxnDate': next_txn_date,
            'nextTxnId': next_txn_id
        }

        if operation not in OPERATIONS:
            raise ValueError('Unexpected operation: {}'.format(operation))

        for x, source in enumerate(sources):
            if source not in SOURCES:
                raise ValueError('Unexpected source: {}'.format(source))

            payload['sources[{}]'.format(x)] = source

        return self.method(url.format(self.number), payload)

    def statistics(self, from_date, to_date, operation='ALL', sources=None):
        """ Получить статистику транзакций

        :param from_date: Начальная дата периода статистики.
            ГГГГ-ММ-ДД-<часовой пояс>. Указывается так:
            +0000(UTC), +0300(Москва) и т.д.
        :type from_date: str

        :param to_date: Конечная дата периода статистики.
            ГГГГ-ММ-ДД-<часовой пояс>
        :type to_date: str

        :param operation: Тип операций, учитываемых при подсчете статистики
            см. OPERATIONS
        :type operation: list or str

        :param sources: Источники платежа, учитываемые при подсчете статистики
        :type sources: str
        """

        if sources is None:
            sources = []
        elif not isinstance(sources, list):
            sources = [sources]

        url = 'payment-history/v2/persons/{}/payments/total'
        payload = {
            'startDate': self._format_date(from_date),
            'endDate': self._format_date(to_date),
            'operation': operation,
        }

        if operation not in OPERATIONS:
            raise ValueError('Unexpected operation: {}.'.format(operation))

        for x, source in enumerate(sources):
            if source not in SOURCES:
                raise ValueError('Unexpected source: {}'.format(source))

            payload['sources[{}]'.format(x)] = source

        return self.method(url.format(self.number), payload)

    def transaction_info(self, transaction_id):
        """ Получить информацию о транзакции

        :param transaction_id: Номер транзакции
        :type transaction_id: int
        """

        url = 'payment-history/v2/transactions/{}'

        return self.method(url.format(transaction_id))

    def balance(self, only_balance=False):
        """ Получить баланс кошельков

        :param only_balance: если True, вернётся только название кошелька и его баланс
        :type only_balance: bool
        """

        url = 'funding-sources/v2/persons/{}/accounts'

        json = self.method(url.format(self.number))['accounts']

        if only_balance:
            balances = []
            for x, account in enumerate(json):
                if account['balance']:
                    balances.append({})
                    balances[x][account['alias']] = account['balance']['amount']

            return balances

        return json

    def comission(self, provider):
        """ Комиссионные условия провайдера

        :param provider: id провайдера
        :type provider: str, int or :class:`Providers`
        """

        url = 'sinap/providers/{}/form'

        if isinstance(provider, Providers):
            provider = provider.value

        return self.method(url.format(provider))

    def send_qiwi(self, recipient, amount, comment=None):
        """ Перевод на кошелёк Киви

        :param recipient: Номер получателя в формате 71234567890
        :type recipient: str

        :param amount: Сумма в рублях. Минимум 1 рубль
        :type amount: int or float

        :param comment: Комментарий
        :type comment: str
        """

        url = 'sinap/api/v2/terms/99/payments'
        payload = {
            'id': self._transaction_id(),
            'sum': {
                'amount': amount,
                'currency': '643'
            },
            'paymentMethod': {
                'type': 'Account',
                'accountId': '643'
            },
            'fields': {
                'account': recipient,
            },
            'comment': comment
        }

        json = self.method(url, payload, 'post')

        if hasattr(json, 'message'):
            raise ApiError(json['message'])

        return json

    def send_mobile(self, recipient, amount):
        """ Оплата мобильной связи

        :param recipient: Номер телефона для пополнения в формате 71234567890
        :type recipient: str

        :param amount: Сумма в рублях
        :type amount: int or float
        """

        url = 'sinap/api/v2/terms/{}/payments'
        payload = {
            'id': self._transaction_id(),
            'sum': {
                'amount': amount,
                'currency': '643'
            },
            'paymentMethod': {
                'type': 'Account',
                'accountId': '643'
            },
            'fields': {
                'account': recipient[1:]
            }
        }

        json = self.method(
            url.format(self.detect_operator(recipient)),
            payload,
            'post'
        )

        if hasattr(json, 'message'):
            raise ApiError(json['message'])

        return json

    def method(self, method_name, payload=None, method='get'):
        """ Вызов метода API

        :param method_name: Часть url после https://edge.qiwi.com/
        :type method_name: str

        :param payload: json параметры
        :type payload: str or dict

        :param method: Метод запроса (get, post)
        :type method: str
        """

        url = 'https://edge.qiwi.com/{}'.format(method_name)

        if payload is None:
            payload = {}

        if method == 'get':
            res = self.session.get(url, params=payload)
        elif method == 'post':
            if isinstance(payload, dict):
                payload = json.dumps(payload, ensure_ascii=False)

            res = self.session.post(url, json=payload)

        if res.status_code == 401:
            raise WrongToken('Wrong token')
        elif res.status_code == 403:
            raise PermissionError('Not enough permissions to access this method')

        return res.json()

    def detect_operator(self, number):
        """ Узнать id оператора

        :param number: номер телефона в формате 71234567890
        :type number: str
        """

        url = 'https://qiwi.com/mobile/detect.action'

        self.session.headers['Content-type'] = 'application/x-www-form-urlencoded'
        res = self.session.post(url, data={'phone': number})
        self.session.headers['Content-type'] = 'application/json'
        json = res.json()

        if json['code']['value'] == '2':
            raise ApiError('Can\'t detect phone operator')

        return json['message']

    def _format_date(self, date):
        if date:
            return datetime.datetime.strptime(date, '%Y-%m-%d-%z').isoformat()

        return None

    def _transaction_id(self):
        return str(int(datetime.datetime.utcnow().timestamp()) * 1000)
