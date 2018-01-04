from collections import namedtuple

class Exchange(object):
    def __init__(self,apikey,secretkey):
        self._apikey = apikey
        self._secretkey = secretkey


Ticker = namedtuple("Ticker",("timestamp","last","bid","ask","high","low","volume"))

Markets = namedtuple("Markets",())
