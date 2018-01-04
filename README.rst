CryptoCoinTradeClient
=====================

Description
-----------

-  CryptoCoinTradeClient is a python client for crypto coin trade.

HOW TO install
--------------

``pip install cryptojp``

or

``pip install https://github.com/airking05/cryptojp``

HOW TO USE
----------

Ticker
~~~~~~

\`\`\` >>> from exchanges.base.initializer import NewExchange >>> APIKEY
= "aaaaaaaaaaaaaa" >>> SECRET\_KEY = "bbbbbbbbbbbbbb"

            bitflyer=NewExchange("bitflyer", API\_KEY, SECRET\_KEY)
            bitflyer.markets() ('BTC\_JPY', 'FX\_BTC\_JPY', 'ETH\_BTC',
            'BCH\_BTC', 'BTCJPY05JAN2018', 'BTCJPY12JAN2018')

            for market in bitflyer.markets(): ...
            print(bitflyer.ticker(market)) ...
            Ticker(timestamp='2018-01-04T10:54:01.677', last=1779000.0,
            bid=1779000.0, ask=1779099.0, high=None, low=None,
            volume=99020.50507241)
            Ticker(timestamp='2018-01-04T10:54:01.24', last=1779013.0,
            bid=1779001.0, ask=1779099.0, high=None, low=None,
            volume=99019.20607241)
            Ticker(timestamp='2018-01-04T10:54:01.303', last=1779013.0,
            bid=1779001.0, ask=1779099.0, high=None, low=None,
            volume=99019.33707241)
            Ticker(timestamp='2018-01-04T10:54:01.677', last=1779000.0,
            bid=1779000.0, ask=1779099.0, high=None, low=None,
            volume=99019.83707241)
            Ticker(timestamp='2018-01-04T10:54:02.163', last=1779000.0,
            bid=1779000.0, ask=1779099.0, high=None, low=None,
            volume=99019.73707241)
            Ticker(timestamp='2018-01-04T10:54:02.367', last=1779000.0,
            bid=1779000.0, ask=1779099.0, high=None, low=None,
            volume=99020.77707241)\`\`\`
