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

Markets def markets():
~~~~~~~~~~~~~~~~~~~~~~

-  This returns tuple like (‘ETHBTC’, ‘LTCBTC’).

.. code:: python

    markets = binance.markets()
    print(markets)
     
    ('ETHBTC', 'LTCBTC', 'BNBBTC', 'NEOBTC', '123456', 'QTUMETH', 'EOSETH', 'SNTETH', 'BNTETH', 'BCCBTC', 'GASBTC', 'BNBETH', 'BTCUSDT', 'ETHUSDT', 'HSRBTC', 'OAXETH', 'DNTETH', 'MCOETH', 'ICNETH', 'MCOBTC', 'WTCBTC', 'WTCETH', 'LRCBTC', 'LRCETH', 'QTUMBTC', 'YOYOBTC', 'OMGBTC', 'OMGETH', 'ZRXBTC', 'ZRXETH', 'STRATBTC', 'STRATETH', 'SNGLSBTC', 'SNGLSETH', 'BQXBTC', 'BQXETH', 'KNCBTC', 'KNCETH', 'FUNBTC', 'FUNETH', 'SNMBTC', 'SNMETH', 'NEOETH', 'IOTABTC', 'IOTAETH', 'LINKBTC', 'LINKETH', 'XVGBTC', 'XVGETH', 'CTRBTC', 'CTRETH', 'SALTBTC', 'SALTETH', 'MDABTC', 'MDAETH', 'MTLBTC', 'MTLETH', 'SUBBTC', 'SUBETH', 'EOSBTC', 'SNTBTC', 'ETCETH', 'ETCBTC', 'MTHBTC', 'MTHETH', 'ENGBTC', 'ENGETH', 'DNTBTC', 'ZECBTC', 'ZECETH', 'BNTBTC', 'ASTBTC', 'ASTETH', 'DASHBTC', 'DASHETH', 'OAXBTC', 'ICNBTC', 'BTGBTC', 'BTGETH', 'EVXBTC', 'EVXETH', 'REQBTC', 'REQETH', 'VIBBTC', 'VIBETH', 'HSRETH', 'TRXBTC', 'TRXETH', 'POWRBTC', 'POWRETH', 'ARKBTC', 'ARKETH', 'YOYOETH', 'XRPBTC', 'XRPETH', 'MODBTC', 'MODETH', 'ENJBTC', 'ENJETH', 'STORJBTC', 'STORJETH', 'BNBUSDT', 'VENBNB', 'YOYOBNB', 'POWRBNB', 'VENBTC', 'VENETH', 'KMDBTC', 'KMDETH', 'NULSBNB', 'RCNBTC', 'RCNETH', 'RCNBNB', 'NULSBTC', 'NULSETH', 'RDNBTC', 'RDNETH', 'RDNBNB', 'XMRBTC', 'XMRETH', 'DLTBNB', 'WTCBNB', 'DLTBTC', 'DLTETH', 'AMBBTC', 'AMBETH', 'AMBBNB', 'BCCETH', 'BCCUSDT', 'BCCBNB', 'BATBTC', 'BATETH', 'BATBNB', 'BCPTBTC', 'BCPTETH', 'BCPTBNB', 'ARNBTC', 'ARNETH', 'GVTBTC', 'GVTETH', 'CDTBTC', 'CDTETH', 'GXSBTC', 'GXSETH', 'NEOUSDT', 'NEOBNB', 'POEBTC', 'POEETH', 'QSPBTC', 'QSPETH', 'QSPBNB', 'BTSBTC', 'BTSETH', 'BTSBNB', 'XZCBTC', 'XZCETH', 'XZCBNB', 'LSKBTC', 'LSKETH', 'LSKBNB', 'TNTBTC', 'TNTETH', 'FUELBTC', 'FUELETH', 'MANABTC', 'MANAETH', 'BCDBTC', 'BCDETH', 'DGDBTC', 'DGDETH', 'IOTABNB', 'ADXBTC', 'ADXETH', 'ADXBNB', 'ADABTC', 'ADAETH', 'PPTBTC', 'PPTETH', 'CMTBTC', 'CMTETH', 'CMTBNB', 'XLMBTC', 'XLMETH', 'XLMBNB', 'CNDBTC', 'CNDETH', 'CNDBNB', 'LENDBTC', 'LENDETH', 'WABIBTC', 'WABIETH', 'WABIBNB', 'LTCETH', 'LTCUSDT', 'LTCBNB', 'TNBBTC', 'TNBETH', 'WAVESBTC', 'WAVESETH', 'WAVESBNB', 'GTOBTC', 'GTOETH', 'GTOBNB', 'ICXBTC', 'ICXETH', 'ICXBNB', 'OSTBTC', 'OSTETH', 'OSTBNB', 'ELFBTC', 'ELFETH', 'AIONBTC', 'AIONETH', 'AIONBNB', 'NEBLBTC', 'NEBLETH', 'NEBLBNB', 'BRDBTC', 'BRDETH', 'BRDBNB', 'MCOBNB', 'EDOBTC', 'EDOETH', 'WINGSBTC', 'WINGSETH', 'NAVBTC', 'NAVETH', 'NAVBNB', 'LUNBTC', 'LUNETH', 'TRIGBTC', 'TRIGETH', 'TRIGBNB', 'APPCBTC', 'APPCETH', 'APPCBNB', 'VIBEBTC', 'VIBEETH', 'RLCBTC', 'RLCETH', 'RLCBNB', 'INSBTC', 'INSETH', 'PIVXBTC', 'PIVXETH', 'PIVXBNB', 'IOSTBTC', 'IOSTETH', 'CHATBTC', 'CHATETH', 'STEEMBTC', 'STEEMETH', 'STEEMBNB', 'NANOBTC', 'NANOETH', 'NANOBNB', 'VIABTC', 'VIAETH', 'VIABNB', 'BLZBTC', 'BLZETH', 'BLZBNB', 'AEBTC', 'AEETH', 'AEBNB')

--------------

Order def order(item, order_type, side, price, size):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  This function execute order and returns order_id.

**item** - use currency_pair getting from markets() func.

**order_type** - use “LIMIT” or “MARKET”

**side** - use “BUY” or “SELL”

**price** - input price at which you want to trade

**size** - input size on which you want to trade

.. code:: python

    order_id = bitflyer.order("btc_jpy","MARKET","BUY",0,1)
    print(order_id)
     
    "JRF20150707-050237-639234"

--------------

Cancel Order def cancel_order(item, order_id:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**item** - use currency_pair getting from markets() func.

**order_id**

-  the id you got when you orderd

.. code:: python

    bitflyer.cancel_order("btc_jpy",order_id)

Function list
-------------

+-------------------+------+------+------+------+------+------+------+------+------+
|                   | Bitf | Coin | Btcb | Quoi | Krak | Hitb | Bina | Polo | Bitf |
|                   | lyer | chec | ox   | ne   | en   | tc   | nce  | niex | inex |
|                   |      | k    |      |      |      |      |      |      |      |
+===================+======+======+======+======+======+======+======+======+======+
| ticker()          | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    |
+-------------------+------+------+------+------+------+------+------+------+------+
| markets()         | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    |
+-------------------+------+------+------+------+------+------+------+------+------+
| board()           | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    |
+-------------------+------+------+------+------+------+------+------+------+------+
| order()           | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    | ☓    |
+-------------------+------+------+------+------+------+------+------+------+------+
| balance()         | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    | ☓    |
+-------------------+------+------+------+------+------+------+------+------+------+
| get_open_orders() | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    | ☓    |
+-------------------+------+------+------+------+------+------+------+------+------+
| cancel_order()    | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    | ☓    |
+-------------------+------+------+------+------+------+------+------+------+------+
| get_fee()         | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    | ✓    | ☓    |
+-------------------+------+------+------+------+------+------+------+------+------+


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
