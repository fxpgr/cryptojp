import json
import os
import unittest
from unittest import TestCase

from mock import Mock

from exchanges import NewExchange

KEYS_GLOBAL = './keys.json'
KEYS_LOCAL = './keys.local.json'
KEYS_FILE = KEYS_LOCAL if os.path.exists(KEYS_LOCAL) else KEYS_GLOBAL

BITFLYER_MOCK_ORDER = """{"child_order_acceptance_id": "JRF20150707-050237-639234"}"""
BITFLYER_MOCK_BALANCE = """[{"currency_code":"JPY","amount":1024078,"available":508000},{"currency_code":"BTC","amount":10.24,"available":4.12},{"currency_code":"ETH","amount":20.48,"available":16.38}]"""

HITBTC_MOCK_BALANCE = """[{"currency":"ETH","available":"10.000000000","reserved":"0.560000000"},{"currency":"BTC","available":"0.010205869","reserved":"0"}]"""
HITBTC_MOCK_ORDER = """{"id":0,"clientOrderId":"d8574207d9e3b16a4a5511753eeef175","symbol":"ETHBTC","side":"sell","status":"new","type":"limit","timeInForce":"GTC","quantity":"0.063","price":"0.046016","cumQuantity":"0.000","createdAt":"2017-05-15T17:01:05.092Z","updatedAt":"2017-05-15T17:01:05.092Z"}"""

BINANCE_MOCK_MARKETS = """[{"symbol":"ETHBTC","price":"0.09664900"},{"symbol":"LTCBTC","price":"0.01598000"},{"symbol":"BNBBTC","price":"0.00117900"},{"symbol":"NEOBTC","price":"0.01234500"},{"symbol":"123456","price":"0.00030000"},{"symbol":"QTUMETH","price":"0.03630400"},{"symbol":"EOSETH","price":"0.01322500"},{"symbol":"SNTETH","price":"0.00026412"},{"symbol":"BNTETH","price":"0.00668800"},{"symbol":"BCCBTC","price":"0.14402000"},{"symbol":"GASBTC","price":"0.00445600"},{"symbol":"BNBETH","price":"0.01219000"},{"symbol":"BTCUSDT","price":"11113.02000000"},{"symbol":"ETHUSDT","price":"1074.99000000"},{"symbol":"HSRBTC","price":"0.00156500"},{"symbol":"OAXETH","price":"0.00116130"},{"symbol":"DNTETH","price":"0.00014662"},{"symbol":"MCOETH","price":"0.01130900"},{"symbol":"ICNETH","price":"0.00231930"},{"symbol":"MCOBTC","price":"0.00110100"},{"symbol":"WTCBTC","price":"0.00344200"},{"symbol":"WTCETH","price":"0.03552100"}]"""

BINANCE_MOCK_TICKER = """[[1502928000000,"4261.48000000","4485.39000000","4200.74000000","4285.08000000","795.15037700",1503014399999,"3454770.05073206",3427,"616.24854100","2678216.40060401","8733.91139481"],[1503014400000,"4285.08000000","4371.52000000","3938.77000000","4108.37000000","1199.88826400",1503100799999,"5086958.30617151",5233,"972.86871000","4129123.31651808","9384.14140858"],[1503100800000,"4108.37000000","4184.69000000","3850.00000000","4139.98000000","381.30976300",1503187199999,"1549483.73542151",2153,"274.33604200","1118001.87008735","9184.08552906"],[1503187200000,"4120.98000000","4211.08000000","4032.62000000","4086.29000000","467.08302200",1503273599999,"1930364.39032646",2321,"376.79594700","1557401.33373730","10125.41408414"],[1503273600000,"4069.13000000","4119.62000000","3911.79000000","4016.00000000","691.74306000",1503359999999,"2797231.71402728",3972,"557.35610700","2255662.55315837","11706.76997007"],[1503360000000,"4016.00000000","4104.82000000","3400.00000000","4040.00000000","966.68485800",1503446399999,"3752505.77214051",6494,"423.99518100","1637188.36934226","11773.27950025"],[1503446400000,"4040.00000000","4265.80000000","4013.89000000","4114.01000000","1001.13656500",1503532799999,"4148686.46581968",8629,"309.41909200","1293567.09519463","12724.37533462"],[1503532800000,"4147.00000000","4371.68000000","4085.01000000","4316.01000000","787.41875300",1503619199999,"3296476.41316476",6247,"206.82041200","868379.06413120","14231.32630532"],[1503619200000,"4316.01000000","4453.91000000","4247.48000000","4280.68000000","573.61274000",1503705599999,"2484637.34936327",6554,"100.09797400","434577.13574645","12945.43630782"],[1503705600000,"4280.71000000","4367.00000000","4212.41000000","4337.44000000","228.10806800",1503791999999,"977865.73333210",2260,"56.19014100","241363.80050245","11789.06750167"]]"""

POLONIEX_MOCK_BALANCE = """{"LTC":{"available":"5.015","onOrders":"1.0025","btcValue":"0.078"}}"""
POLONIEX_MOCK_ORDER = """{"orderNumber":31226040,"resultingTrades":[{"amount":"338.8732","date":"2014-10-18 23:03:21","rate":"0.00000173","total":"0.00058625","tradeID":"16164","type":"buy"}]}"""

COINCHECK_MOCK_BALANCE = """{"success":true,"jpy":"0.8401","btc":"7.75052654","jpy_reserved":"3000.0","btc_reserved":"3.5002","jpy_lend_in_use":"0","btc_lend_in_use":"0.3","jpy_lent":"0","btc_lent":"1.2","jpy_debt":"0","btc_debt":"0"}"""
COINCHECK_MOCK_ORDER = """{"success":true,"id":12345,"rate":"30010.0","amount":"1.3","order_type":"sell","stop_loss_rate":null,"pair":"btc_jpy","created_at":"2015-01-10T05:55:38.000Z"}"""

BTCBOX_MOCK_ORDER = """{"result":true,"id":"11"}"""
BTCBOX_MOCK_BALANCE = """{"uid":8,"nameauth":0,"moflag":0,"btc_balance":4234234,"btc_lock":0,"ltc_balance":32429.6,"ltc_lock":2.4,"doge_balance":0,"doge_lock":0,"jpy_balance":2344581.519,"jpy_lock":868862.481}"""

QUOINE_MOCK_BALANCE = """[{"currency":"BTC","balance":"0.04925688"},{"currency":"USD","balance":"7.17696"},{"currency":"JPY","balance":"356.01377"}]"""
QUOINE_MOCK_ORDER = """{"id":2157474,"order_type":"limit","quantity":"0.01","disc_quantity":"0.0","iceberg_total_quantity":"0.0","side":"sell","filled_quantity":"0.0","price":"500.0","created_at":1462123639,"updated_at":1462123639,"status":"live","leverage_level":1,"source_exchange":"QUOINE","product_id":1,"product_code":"CASH","funding_currency":"USD","currency_pair_code":"BTCUSD","order_fee":"0.0"}"""


class TestExchanges(TestCase):

    def test_realcurrency(self):
        realcurrency = NewExchange("realcurrency", "", "")

    def test_bitflyer(self):
        bitflyer = NewExchange("bitflyer", "", "")
        bitflyer.markets()
        bitflyer.board()
        bitflyer.ticker()
        bitflyer.ticker("BTC_JPY")

        bitflyer = NewExchange("bitflyer", "", "")
        bitflyer.httpPost = Mock()
        bitflyer.httpPost.return_value = json.loads(BITFLYER_MOCK_ORDER)
        bitflyer.order("ETHBTC", "limit", "buy", 100, 10000)
        bitflyer.order("ETHBTC", "market", "buy", 100, 10000)
        bitflyer.get_order("BTC_JPY", "order_id")

        bitflyer.httpGet = Mock()
        bitflyer.httpGet.return_value = json.loads(BITFLYER_MOCK_BALANCE)
        bitflyer.balance()

        bitflyer = NewExchange("bitflyer", "", "")
        bitflyer.session.get = Mock()
        balance_return = Mock()
        balance_return.json.return_value = json.loads(BITFLYER_MOCK_BALANCE)
        bitflyer.session.get.return_value = balance_return
        bitflyer.session.post = Mock()
        order_return = Mock()
        order_return.json.return_value = json.loads(BITFLYER_MOCK_ORDER)
        bitflyer.session.post.return_value = order_return
        bitflyer.balance()
        bitflyer.order("ETHBTC", "limit", "buy", 100, 10000)

    def test_poloniex(self):
        poloniex = NewExchange("poloniex", "", "")
        poloniex.ticker()
        poloniex.markets()
        poloniex.board()
        poloniex.httpPost = Mock()
        poloniex.httpPost.return_value = json.loads(POLONIEX_MOCK_BALANCE)
        poloniex.balance()
        poloniex.httpPost.return_value = json.loads(POLONIEX_MOCK_ORDER)
        poloniex.order("BTC_ETC", "limit",  "sell", 0.00356515, 2)
        poloniex.order("BTC_ETC", "fillOrKill",  "sell", 0.00356515, 2)

        poloniex = NewExchange("poloniex", "", "")
        poloniex.session.post = Mock()
        balance_return = Mock()
        balance_return.json.return_value = json.loads(POLONIEX_MOCK_BALANCE)
        poloniex.session.post.return_value = balance_return
        poloniex.balance()
        order_return = Mock()
        order_return.json.return_value = json.loads(POLONIEX_MOCK_ORDER)
        poloniex.session.post.return_value = order_return
        poloniex.order("ETHBTC", "limit", "buy", 100, 10000)

    def test_hitbtc(self):
        hitbtc = NewExchange("hitbtc", "", "")
        hitbtc.markets()
        hitbtc.board()
        hitbtc.ticker()

        hitbtc.session = Mock()
        balance_return = Mock()
        balance_return.json.return_value = json.loads(HITBTC_MOCK_BALANCE)
        hitbtc.session.get.return_value = balance_return
        hitbtc.balance()

        order_return = Mock()
        order_return.json.return_value = json.loads(HITBTC_MOCK_ORDER)
        hitbtc.session.post.return_value = order_return
        hitbtc.order("ETHBTC", "limit", "buy", 100, 10000)
        hitbtc.order("ETHBTC", "market", "buy", 100, 10000)

    def test_binance(self):
        binance = NewExchange("binance", "", "")
        binance.httpGet = Mock()
        binance.httpGet.return_value = json.loads(BINANCE_MOCK_MARKETS)
        binance.markets()

        binance.httpGet.return_value = json.loads(BINANCE_MOCK_TICKER)
        binance.ticker()

        binance.board()
        binance.order("BTCUSDT", "limit", "buy", 100, 10000)
        binance.balance()

    def test_coincheck(self):
        coincheck = NewExchange("coincheck", "", "")
        coincheck.ticker()
        coincheck.markets()
        coincheck.board()

        coincheck.session.get = Mock()
        balance_return = Mock()
        balance_return.json.return_value = json.loads(COINCHECK_MOCK_BALANCE)
        coincheck.session.get.return_value = balance_return
        coincheck.balance()

        coincheck.session.post = Mock()
        order_return = Mock()
        order_return.json.return_value = json.loads(COINCHECK_MOCK_ORDER)
        coincheck.session.post.return_value = order_return
        coincheck.order("btc_jpy", "market", "buy", 100, 10000)
        coincheck.order("btc_jpy", "market", "sell", 100, 10000)
        coincheck.order("btc_jpy", "limit", "sell", 100, 10000)

    def test_btcbox(self):
        btcbox = NewExchange("btcbox", "", "")
        btcbox.ticker()
        btcbox.markets()
        btcbox.board()

        btcbox.session.get = Mock()
        balance_return = Mock()
        balance_return.json.return_value = json.loads(BTCBOX_MOCK_BALANCE)
        btcbox.session.get.return_value = balance_return
        btcbox.balance()

        btcbox.session.post = Mock()
        order_return = Mock()
        order_return.json.return_value = json.loads(BTCBOX_MOCK_ORDER)
        btcbox.session.post.return_value = order_return
        btcbox.order("btc_jpy", "market", "buy", 100, 10000)
        btcbox.order("btc_jpy", "market", "sell", 100, 10000)
        btcbox.order("btc_jpy", "limit", "sell", 100, 10000)

    def test_kraken(self):
        kraken = NewExchange("kraken", "", "")
        kraken.ticker()
        kraken.markets()
        kraken.board()

    def test_quoine(self):
        quoine = NewExchange("quoine", "", "")
        quoine.ticker()
        quoine.markets()
        quoine.board()

        quoine.session.get = Mock()
        balance_return = Mock()
        balance_return.json.return_value = json.loads(QUOINE_MOCK_BALANCE)
        quoine.session.get.return_value = balance_return
        quoine.balance()

        quoine.session.post = Mock()
        order_return = Mock()
        order_return.json.return_value = json.loads(QUOINE_MOCK_ORDER)
        quoine.session.post.return_value = order_return
        quoine.order("btc_jpy", "market", "buy", 100, 10000)
        quoine.order("btc_jpy", "market", "sell", 100, 10000)
        quoine.order("btc_jpy", "limit", "sell", 100, 10000)


if __name__ == "__main__":
    unittest.main(warnings='ignore')


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestExchanges))
    return suite
