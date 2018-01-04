from unittest import TestCase
from exchanges import bitflyer
from exchanges.base.initializer import NewExchange
from exchanges.base.initializer import EXCHANGES
import os,json,logging

KEYS_GLOBAL = './keys.json'
KEYS_LOCAL = './keys.local.json'
KEYS_FILE = KEYS_LOCAL if os.path.exists(KEYS_LOCAL) else KEYS_GLOBAL

class TestExchanges(TestCase):
    @classmethod
    def setUpClass(cls):
        with open(KEYS_FILE) as file:
            cls.config = json.load(file)

    def test_ticker(self):
        for e in EXCHANGES:
            API_KEY = self.config[e]["apikey"]
            SECRET_KEY = self.config[e]["secretkey"]
            ex = NewExchange(e,API_KEY,SECRET_KEY)
            markets = ex.markets()
            self.assertEqual(type(markets), tuple)
            for m in markets:
                self.assertEqual(len(ex.ticker(m)), 7)

if __name__ == "__main__":
    unittest.main()
