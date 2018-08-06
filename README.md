qiwi_api [![Travis](https://img.shields.io/travis/Helow19274/qiwi_api.svg)](https://travis-ci.org/Helow19274/qiwi_api/) [![Docs](https://img.shields.io/readthedocs/qiwi_api.svg)](https://qiwi-api.readthedocs.io/ru/latest/) [![PyPI](https://img.shields.io/pypi/v/qiwi_api.svg)](https://pypi.org/project/qiwi-api/) ![Python Version](https://img.shields.io/pypi/pyversions/qiwi_api.svg)
=====

qiwi_api - модуль для взаимодействия с Qiwi API

* [Документация](https://qiwi-api.readthedocs.io/ru/latest/)
* [Документация на сайте Qiwi](https://developer.qiwi.com/ru/qiwi-wallet-personal/)

Установка
========

```bash
$ pip install --upgrade qiwi_api
```

Пример
======

```python
from qiwi_api import Qiwi

api = Qiwi('your_token_here')
print(api.balance(only_balance=True))
```
