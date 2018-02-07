|Build Status| |Coverage Status|

cryptojp == Python client for cryptocoin exchanges
==================================================

Description
-----------

-  cryptojp is a python client for crypto coin trade.

HOW TO install
--------------

``pip install cryptojp``

or

``pip install git+https://github.com/airking05/cryptojp``

Development Status
------------------

+--------------+----------+-----------+--------+--------+--------+--------+---------+----------+
|              | Bitflyer | Coincheck | Btcbox | Quoine | Kraken | Hitbtc | Binance | Poloniex |
+==============+==========+===========+========+========+========+========+=========+==========+
| ticker()     | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      | ✓       | ✓        |
+--------------+----------+-----------+--------+--------+--------+--------+---------+----------+
| markets()    | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      | ✓       | ✓        |
+--------------+----------+-----------+--------+--------+--------+--------+---------+----------+
| board()      | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      |         | ✓        |
+--------------+----------+-----------+--------+--------+--------+--------+---------+----------+
| order()      | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      |         | ✓        |
+--------------+----------+-----------+--------+--------+--------+--------+---------+----------+
| balance()    | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      |         | ✓        |
+--------------+----------+-----------+--------+--------+--------+--------+---------+----------+
| is_excuted() |          |           |        |        |        |        |         |          |
+--------------+----------+-----------+--------+--------+--------+--------+---------+----------+

next binance…

HOW TO USE
----------

Ticker
~~~~~~

.. code:: python

    >>> from exchanges import NewExchange
    >>> APIKEY = "aaaaaaaaaaaaaa"
    >>> SECRET_KEY = "bbbbbbbbbbbbbb"

    >>> bitflyer=NewExchange("bitflyer", API_KEY, SECRET_KEY)
    >>> bitflyer.markets()
    ('BTC_JPY', 'FX_BTC_JPY', 'ETH_BTC', 'BCH_BTC', 'BTCJPY05JAN2018', 'BTCJPY12JAN2018')

    >>> for market in bitflyer.markets():
    ...     print(bitflyer.ticker(market))
    ...
    Ticker(timestamp='2018-01-04T10:54:01.677', last=1779000.0, bid=1779000.0, ask=1779099.0, high=None, low=None, volume=99020.50507241)
    Ticker(timestamp='2018-01-04T10:54:01.24', last=1779013.0, bid=1779001.0, ask=1779099.0, high=None, low=None, volume=99019.20607241)
    Ticker(timestamp='2018-01-04T10:54:01.303', last=1779013.0, bid=1779001.0, ask=1779099.0, high=None, low=None, volume=99019.33707241)
    Ticker(timestamp='2018-01-04T10:54:01.677', last=1779000.0, bid=1779000.0, ask=1779099.0, high=None, low=None, volume=99019.83707241)
    Ticker(timestamp='2018-01-04T10:54:02.163', last=1779000.0, bid=1779000.0, ask=1779099.0, high=None, low=None, volume=99019.73707241)
    Ticker(timestamp='2018-01-04T10:54:02.367', last=1779000.0, bid=1779000.0, ask=1779099.0, high=None, low=None, volume=99020.77707241)

.. |Build Status| image:: https://travis-ci.org/airking05/cryptojp.svg?branch=master
   :target: https://travis-ci.org/airking05/cryptojp
.. |Coverage Status| image:: https://coveralls.io/repos/github/airking05/cryptojp/badge.svg?branch=master&date=20180130_2
   :target: https://coveralls.io/github/airking05/cryptojp?branch=master
