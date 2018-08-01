# -*- coding: utf-8 -*-
from enum import IntEnum

OPERATIONS = ['ALL', 'IN', 'OUT', 'QIWI_CARD']  #: Типы операций

SOURCES = ['QW_RUB', 'QW_USD', 'QW_EUR', 'CARD', 'MK']  #: Источники платежей


class Providers(IntEnum):
    QIWI = 99  #: Киви
    ALFABANK = 464  #: Альфа-Банк
    TINKOFFBANK = 466  #: Тинькофф Банк
    RSBANK = 815  #: Банк Русский Стандарт
    PSBANK = 821  #: Промсвязьбанк
    VISA_CIS = 1960  #: Visa СНГ
    VISA_RUSSIA = 1963  #: Visa Россия
    MASTERCARD_CIS = 21012  #: MasterCard СНГ
    MASTERCARD_RUSSIA = 21013  #: MasterCard Россия
    MIR = 31652  #: Мир
