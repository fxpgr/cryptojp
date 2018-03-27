#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from .base.exchange import *
from .errors import *
import sys
if sys.version_info.major <= 2:
    from urllib import urlencode
else:
    from urllib.parse import urlencode
import requests
import hmac
import hashlib
import json
import base64
BITFINEX_REST_URL = 'api.bitfinex.com'


class Bitfinex(Exchange):
    def __init__(self, apikey, secretkey):
        def httpGet(url, resource, params, apikey, secretkey):
            nonce = str(int(round(time.time() * 10000)))
            params["nonce"] = nonce
            params["request"] = resource
            data = base64.b64encode(json.dumps(params).encode())
            sign = hmac.new(self._secretkey, data, hashlib.sha384).hexdigest()

            headers = {
                "X-BFX-APIKEY": self._apikey,
                "X-BFX-SIGNATURE": sign,
                "AX-BFX-PAYLOAD": data,
            }
            return self.session.get('https://' + url + resource,
                                    headers=headers, data=json.dumps(params)).json()

        def httpPost(url, resource, params, apikey, secretkey):
            nonce = str(int(round(time.time() * 10000)))
            params["nonce"] = nonce
            params["request"] = resource
            data = base64.b64encode(json.dumps(params).encode())
            sign = hmac.new(self._secretkey, data, hashlib.sha384).hexdigest()

            headers = {
                "X-BFX-APIKEY": self._apikey,
                "X-BFX-SIGNATURE": sign,
                "AX-BFX-PAYLOAD": data,
            }
            return self.session.post('https://' + url + resource,
                                     headers=headers, data=json.dumps(params)).json()
        super(Bitfinex, self).__init__(apikey, secretkey)
        self.session = requests.session()
        self.httpPost = httpPost
        self.httpGet = httpGet

    def __del__(self):
        self.session.close()

    def markets(self):
        MARKETS_RESOURCE = "/v1/symbols"
        json = self.session.get('https://' + BITFINEX_REST_URL +
                                MARKETS_RESOURCE).json()
        return tuple([j.upper() for j in json])

    def settlements(self):
        return ("BTC", "USD", "ETH")

    def ticker(self, trading, settlement):
        TICKER_RESOURCE = "/v1/pubticker/" + trading.lower() + '_' + settlement.lower()

        json = self.session.get('https://' + BITFINEX_REST_URL +
                                TICKER_RESOURCE).json()
        return Ticker(
            timestamp=int(float(json["timestamp"])),
            last=float(json["last_price"]),
            high=float(json["high"]),
            low=float(json["low"]),
            bid=float(json["bid"]),
            ask=float(json["ask"]),
            volume=float(json["volume"])
        )

    def board(self, symbol=''):
        BOARD_RESOURCE = "/v1/book/" + symbol
        params = {}
        params["group"] = 1
        json = self.session.get('https://' + BITFINEX_REST_URL +
                                BOARD_RESOURCE, data=params).json()

        return Board(
            asks=[Ask(price=float(ask["price"]), size=float(ask["amount"]))
                  for ask in json["asks"]],
            bids=[Bid(price=float(bid["price"]), size=float(bid["amount"]))
                  for bid in json["bids"]],
            mid_price=(float(json["bids"][0]["price"]) + float(json["asks"][0]["price"])) / 2
        )

    def order(self, item, order_type, side, price, size):
        raise Exception("not implemented")

    def get_open_orders(self, symbol="btcusd"):
        raise Exception("not implemented")

    def cancel_order(self, symbol, order_id):
        raise Exception("not implemented")

    def get_fee(self, symbol="btcusd"):
        raise Exception("not implemented")

    def balance(self):
        raise Exception("not implemented")
