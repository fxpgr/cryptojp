# cryptojp

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/cryptojp.svg)](https://pypi.python.org/pypi/cryptojp/)
[![Build Status](https://travis-ci.org/fxpgr/cryptojp.svg?branch=master)](https://travis-ci.org/fxpgr/cryptojp)
[![Coverage Status](https://coveralls.io/repos/github/fxpgr/cryptojp/badge.svg?branch=master&date=20180130_2)](https://coveralls.io/github/fxpgr/cryptojp?branch=master)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/fxpgr/cryptojp/graphs/commit-activity)
[![PyPI status](https://img.shields.io/pypi/status/cryptojp.svg)](https://pypi.python.org/pypi/cryptojp/)

- == Python client for cryptocoin exchanges
- cryptojp is a python client for crypto coin trade.
- You can use this library on Python2/3.
- welcome your contributions.
- document :http://cryptojp.readthedocs.io/en/latest/


## HOW TO install

```pip install cryptojp```

or

```pip install git+https://github.com/fxpgr/cryptojp```


## HOW TO USE

### Initalizing

```python
from cryptojp import NewExchange
 
APIKEY = "YOUR_API_KEY"
SECRET_KEY = "YOUR_SECRET_KEY"

binance = NewExchange("binance", APIKEY, SECRET_KEY)
poloniex = NewExchange("poloniex", APIKEY, SECRET_KEY)
```

- - -

- See document :http://cryptojp.readthedocs.io/en/latest/

- - -


## Exchanges

|                   | Bitflyer | Coincheck | Btcbox | Quoine | Kraken | Hitbtc | Binance |
|-------------------|----------|-----------|--------|--------|--------|--------|---------|
| ticker()          | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      | ✓       |
| markets()         | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      | ✓       |
| settlements()     | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      | ✓       |
| board()           | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      | ✓       |
| order()           | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      | ✓       |
| balance()         | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      | ✓       |
| get_open_orders() | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      | ✓       |
| cancel_order()    | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      | ✓       |
| get_fee()         | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      | ✓       |


|                   | Poloniex | Bitfinex  |
|-------------------|----------|-----------|
| ticker()          | ✓        | ✓         |
| markets()         | ✓        | ✓         |
| settlements()     | ✓        | ✓         |
| board()           | ✓        | ✓         |
| order()           | ✓        | ☓         |
| balance()         | ✓        | ☓         |
| get_open_orders() | ✓        | ☓         |
| cancel_order()    | ✓        | ☓         |
| get_fee()         | ✓        | ☓         |
