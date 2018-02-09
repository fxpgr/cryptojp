[![Build Status](https://travis-ci.org/airking05/cryptojp.svg?branch=master)](https://travis-ci.org/airking05/cryptojp)
[![Coverage Status](https://coveralls.io/repos/github/airking05/cryptojp/badge.svg?branch=master&date=20180130_2)](https://coveralls.io/github/airking05/cryptojp?branch=master)

# cryptojp == Python client for cryptocoin exchanges

## Description

- cryptojp is a python client for crypto coin trade.

## HOW TO install

```pip install cryptojp```

or

```pip install git+https://github.com/airking05/cryptojp```


## Development Status

|           | Bitflyer | Coincheck | Btcbox | Quoine | Kraken | Hitbtc | Binance | Poloniex |
|-----------|----------|-----------|--------|--------|--------|--------|---------|----------|
| ticker()  | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      | ✓       | ✓        |
| markets() | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      | ✓       | ✓        |
| board()   | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      | ✓       | ✓        |
| order()   | ✓        | ✓         | ✓      | ✓      | ✓      | ✓      | ✓       | ✓        |
| balance()   | ✓        | ✓         | ✓      | ✓      | ✓     | ✓      | ✓       | ✓        |
| is_excuted()   |          |           |        |        |       |        |         |          |

next binance...

## HOW TO USE

### Ticker

```python
from exchanges import NewExchange
 
APIKEY = "aaaaaaaaaaaaaa"
SECRET_KEY = "bbbbbbbbbbbbbb"

binance = NewExchange("binance", APIKEY, SECRET_KEY)
poloniex = NewExchange("poloniex", APIKEY, SECRET_KEY)

 
bitflyer=NewExchange("bitflyer", APIKEY, SECRET_KEY)
print(bitflyer.markets())
 
('BTC_JPY', 'FX_BTC_JPY', 'ETH_BTC', 'BCH_BTC', 'BTCJPY05JAN2018', 'BTCJPY12JAN2018')
 
tick = bitflyer.ticker("btc_jpy")
print(tick)
  
Ticker(timestamp='2018-01-04T10:54:01.677', last=1779000.0, bid=1779000.0, ask=1779099.0, high=None, low=None, volume=99020.50507241)
 
print(tick.last)
 
 1779000.0



```
