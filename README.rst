cryptojp
========

|made-with-python| |PyPI pyversions| |Build Status| |Coverage Status|
|Maintenance| |PyPI status|

-  == Python client for cryptocoin exchanges
-  cryptojp is a python client for crypto coin trade.
-  You can use this library on Python2/3.
-  welcome your contributions.
-  document :http://cryptojp.readthedocs.io/en/latest/

HOW TO install
--------------

``pip install cryptojp``

or

``pip install git+https://github.com/fxpgr/cryptojp``

HOW TO USE
----------

Initalizing
~~~~~~~~~~~

.. code:: python

    from cryptojp import NewExchange
     
    APIKEY = "YOUR_API_KEY"
    SECRET_KEY = "YOUR_SECRET_KEY"

    binance = NewExchange("binance", APIKEY, SECRET_KEY)
    poloniex = NewExchange("poloniex", APIKEY, SECRET_KEY)

--------------

Ticker def ticker(item = currency_pair):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  item arg is optional.
-  You can use currency_pair getting from markets() func.
-  This returns namedtuple(“Ticker”, (“timestamp”, “last”, “bid”, “ask”,
   “high”, “low”, “volume”)).

.. code:: python

     
    tick = bitflyer.ticker("btc_jpy")
    print(tick)
      
    Ticker(timestamp='2018-01-04T10:54:01.677', last=1779000.0, bid=1779000.0, ask=1779099.0, high=None, low=None, volume=99020.50507241)
     
    print(tick.last)
    # tick.last is a float data 
    1779000.0

--------------

Exchanges
---------

+-------------------+----------+-----------+--------+--------+--------+--------+---------+
|                   | Bitflyer | Coincheck | Btcbox | Quoine | Kraken | Hitbtc | Binance |
+===================+==========+===========+========+========+========+========+=========+
| ticker()          | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      | ✓       |
+-------------------+----------+-----------+--------+--------+--------+--------+---------+
| markets()         | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      | ✓       |
+-------------------+----------+-----------+--------+--------+--------+--------+---------+
| board()           | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      | ✓       |
+-------------------+----------+-----------+--------+--------+--------+--------+---------+
| order()           | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      | ✓       |
+-------------------+----------+-----------+--------+--------+--------+--------+---------+
| balance()         | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      | ✓       |
+-------------------+----------+-----------+--------+--------+--------+--------+---------+
| get_open_orders() | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      | ✓       |
+-------------------+----------+-----------+--------+--------+--------+--------+---------+
| cancel_order()    | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      | ✓       |
+-------------------+----------+-----------+--------+--------+--------+--------+---------+
| get_fee()         | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      | ✓       |
+-------------------+----------+-----------+--------+--------+--------+--------+---------+

+-------------------+----------+----------+
|                   | Poloniex | Bitfinex |
+===================+==========+==========+
| ticker()          | ✓        | ✓        |
+-------------------+----------+----------+
| markets()         | ✓        | ✓        |
+-------------------+----------+----------+
| board()           | ✓        | ✓        |
+-------------------+----------+----------+
| order()           | ✓        | ☓        |
+-------------------+----------+----------+
| balance()         | ✓        | ☓        |
+-------------------+----------+----------+
| get_open_orders() | ✓        | ☓        |
+-------------------+----------+----------+
| cancel_order()    | ✓        | ☓        |
+-------------------+----------+----------+
| get_fee()         | ✓        | ☓        |
+-------------------+----------+----------+

.. |made-with-python| image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
   :target: https://www.python.org/
.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/cryptojp.svg
   :target: https://pypi.python.org/pypi/cryptojp/
.. |Build Status| image:: https://travis-ci.org/fxpgr/cryptojp.svg?branch=master
   :target: https://travis-ci.org/fxpgr/cryptojp
.. |Coverage Status| image:: https://coveralls.io/repos/github/fxpgr/cryptojp/badge.svg?branch=master&date=20180130_2
   :target: https://coveralls.io/github/fxpgr/cryptojp?branch=master
.. |Maintenance| image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
   :target: https://github.com/fxpgr/cryptojp/graphs/commit-activity
.. |PyPI status| image:: https://img.shields.io/pypi/status/cryptojp.svg
   :target: https://pypi.python.org/pypi/cryptojp/
