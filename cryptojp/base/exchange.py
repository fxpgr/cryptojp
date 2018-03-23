from collections import namedtuple


class Exchange(object):
    def __init__(self, apikey, secretkey):
        self._apikey = apikey
        self._secretkey = secretkey

    def markets(self):
        raise Exception("not implemented")

    def ticker(self, item='BTCUSDT'):
        raise Exception("not implemented")

    def board(self,item='BTCUSDT'):
        raise Exception("not implemented")

    def order(self,item, order_type, side, price, size):
        raise Exception("not implemented")

    def balance(self):
        raise Exception("not implemented")

    def get_open_orders(self, symbol="BTCUSDT"):
        raise Exception("not implemented")

    def cancel_order(self, symbol,order_id):
        raise Exception("not implemented")


Ticker = namedtuple("Ticker", ("timestamp", "last", "bid",
                               "ask", "high", "low", "volume"))
CurrencyPair = namedtuple("CurrencyPair", ("trading","settlement"))

Markets = namedtuple("Markets", ())
Ask = namedtuple("Ask", ("price", "size"))
Bid = namedtuple("Bid", ("price", "size"))
Board = namedtuple("Board", ("asks", "bids", "mid_price"))
Balance = namedtuple("Balance", ("amount", "available"))

ALL_EXCHANGES = (
    "bitflyer",
    "coincheck",
    "btcbox",
    "kraken",
    "quoine",
    "hitbtc"
)
TEST_EXCHANGES = (
    "bitflyer",
    "coincheck",
    "btcbox",
    "hitbtc"
)
