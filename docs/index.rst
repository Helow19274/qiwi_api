Документация qiwi_api
=====================

qiwi_api - модуль для взаимодействия с Qiwi API

Установка:

.. code-block:: shell-session

   $ pip install --upgrade qiwi_api

Пример:

.. code-block:: python

  from qiwi_api import Qiwi

  api = Qiwi('your_token_here')
  print(api.balance(only_balance=True))

.. toctree::
   :maxdepth: 4
   :caption: Содержание:

   qiwi_api
   enums
   exceptions

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
