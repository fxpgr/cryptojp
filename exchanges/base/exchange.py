from collections import namedtuple
from tools.HttpHMACUtil import buildMySign, httpGet, httpPost, getnonce


class Exchange(object):
    def __init__(self, apikey, secretkey):
        self._apikey = apikey
        self._secretkey = secretkey
        self.httpGet = httpGet
        self.httpPost = httpPost
        self.buildMySign = buildMySign


Ticker = namedtuple("Ticker", ("timestamp", "last", "bid",
                               "ask", "high", "low", "volume"))

Markets = namedtuple("Markets", ())

Ask = namedtuple("Ask", ("price", "size"))
Bid = namedtuple("Bid", ("price", "size"))
Board = namedtuple("Board", ("asks", "bids", "mid_price"))

Balance = namedtuple("Balance", ("amount", "available"))


EXCHANGES = (
    "bitflyer",
    "coincheck",
    "zaif",
    "btcbox",
    "kraken",
    "quoine"
)
