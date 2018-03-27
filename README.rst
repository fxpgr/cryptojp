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

-  See document :http://cryptojp.readthedocs.io/en/latest/

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
| settlements()     | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      | ✓       |
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
| settlements()     | ✓        | ✓        |
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
