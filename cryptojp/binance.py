#!/usr/bin/python
# -*- coding: utf-8 -*-
from .base.exchange import *
from .errors import *
import requests
import sys
if sys.version_info.major <= 2:
    from urllib import urlencode
else:
    from urllib.parse import urlencode
import time
import hmac
import hashlib
import base64

BINANCE_REST_URL = 'api.binance.com'
BINANCE_NEW_REST_URL = 'www.binance.com/api'


class Binance(Exchange):
    def __init__(self, apikey, secretkey):
        def httpPost(url,resource, params):
            params["timestamp"] = int(round(time.time() * 1000))
            query = urlencode(params)
            params["signature"] = hmac.new(self._secretkey.encode("utf8"), query.encode("utf8"), digestmod=hashlib.sha256).hexdigest()
            url = 'https://' + url + resource + "?" + urlencode(params)

            headers = {
                "X-MBX-APIKEY": self._apikey,
            }
            return self.session.post(url, headers=headers).json()

        def httpGet(url,resource, params):
            params["timestamp"] = int(round(time.time() * 1000))
            query = urlencode(params)
            params["signature"] = hmac.new(self._secretkey.encode("utf8"), query.encode("utf8"), digestmod=hashlib.sha256).hexdigest()
            url = 'https://' + url + resource + "?" + urlencode(params)

            headers = {
                "X-MBX-APIKEY": self._apikey,
            }
            return self.session.get(url, headers=headers).json()

        super(Binance, self).__init__(apikey, secretkey)
        self.session = requests.session()
        self.httpPost = httpPost
        self.httpGet = httpGet

    def __del__(self):
        self.session.close()

    def markets(self):
        MARKETS_RESOURCE = "/api/v1/ticker/allBookTickers"
        json = self.session.get('https://' + BINANCE_REST_URL +
                                MARKETS_RESOURCE).json()
        return tuple([j["symbol"] for j in json])

    def ticker(self, item='BTCUSDT'):
        TICKER_RESOURCE = "/api/v1/klines"
        params = {
            'symbol': item,
            'interval': '1d',
        }
        json = self.session.get('https://' + BINANCE_REST_URL +
                                TICKER_RESOURCE, params=params).json()
        return Ticker(
            timestamp=float(json[-1][0]),
            last=float(json[-1][4]),
            high=float(json[-1][2]),
            low=float(json[-1][3]),
            bid=None,
            ask=None,
            volume=float(json[-1][5])
        )

    def board(self,item='BTCUSDT'):
        BOARD_RESOURCE = "/v1/depth"
        params = {
            "symbol": item,
            "limit": 100
        }
        json = self.session.get('https://' + BINANCE_REST_URL +
                                BOARD_RESOURCE, data=params).json()
        return Board(
            asks=[Ask(price=float(ask[0]), size=float(ask[1]))
                  for ask in json["asks"]],
            bids=[Bid(price=float(bid[0]), size=float(bid[1]))
                  for bid in json["bids"]],
            mid_price=(float(json["asks"][0][0])+float(json["bids"][0][0]))/2
        )

    def order(self,item, order_type, side, price, size):
        ORDER_RESOURCE = "/v3/order"
        if not item:
            raise SymbolNotFound
        params = {
            "symbol": item,
            "side": side,
            "type": order_type.upper(),
            "timeInForce": "GTC",
            "quantity": size,
            "price": price
        }
        json = self.httpPost(BINANCE_NEW_REST_URL,ORDER_RESOURCE, params=params)
        return json[0]["orderId"]

    def balance(self):
        BALANCE_RESOURCE = "/v3/account"

        json = self.httpGet(BINANCE_NEW_REST_URL,BALANCE_RESOURCE, {})
        balances = {}
        for j in json["balances"]:
            balances[j["asset"]]=[float(j["free"])+float(j["locked"]),float(j["free"])]
        return balances
