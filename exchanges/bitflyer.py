#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from .base.exchange import *
from .errors import *
from urllib.parse import urlencode
import requests
import hmac
import hashlib
import json
BITFLYER_REST_URL = 'api.bitflyer.jp'


class Bitflyer(Exchange):
    def __init__(self, apikey, secretkey):
        def httpGet(url, resource, params, apikey, secretkey):
            timestamp = str(time.time())
            text = str.encode(timestamp + "GET" + resource + urlencode(params))
            headers = {
                "ACCESS-KEY": apikey,
                "ACCESS-TIMESTAMP": timestamp,
                "ACCESS-SIGN":  hmac.new(str.encode(secretkey), text, hashlib.sha256).hexdigest(),
                'Content-Type': 'application/json',
            }
            return self.session.get('https://' + url + resource,
                                    headers=headers, data=params).json()

        def httpPost(url, resource, params, apikey, secretkey):
            timestamp = str(time.time())
            text = str.encode(timestamp + "POST" +
                              resource + json.dumps(params))
            headers = {
                "ACCESS-KEY": apikey,
                "ACCESS-TIMESTAMP": timestamp,
                "ACCESS-SIGN": hmac.new(str.encode(secretkey), text, hashlib.sha256).hexdigest(),
                'Content-Type': 'application/json',
            }
            return self.session.post('https://' + url + resource,
                                     headers=headers, data=json.dumps(params)).json()
        super().__init__(apikey, secretkey)
        self.session = requests.session()
        self.httpPost = httpPost
        self.httpGet = httpGet

    @http_exception
    def markets(self):
        MARKETS_RESOURCE = "/v1/markets"
        json = self.session.get('https://' + BITFLYER_REST_URL +
                                MARKETS_RESOURCE).json()
        return tuple([j["product_code"] for j in json])

    def ticker(self, item=''):
        TICKER_RESOURCE = "/v1/ticker"
        params = {}
        if item:
            params["product_code"] = item[0:3] + "_" + item[3:6]
        json = self.session.get('https://' + BITFLYER_REST_URL +
                                TICKER_RESOURCE, data=params).json()
        return Ticker(
            timestamp=json["timestamp"],
            last=float(json["ltp"]),
            high=None,
            low=None,
            bid=float(json["best_bid"]),
            ask=float(json["best_ask"]),
            volume=float(json["volume"])
        )

    def board(self, item=''):
        BOARD_RESOURCE = "/v1/board"
        params = {}
        json = self.session.get('https://' + BITFLYER_REST_URL +
                                BOARD_RESOURCE, data=params).json()
        return Board(
            asks=[Ask(price=float(ask["price"]), size=float(ask["size"]))
                  for ask in json["asks"]],
            bids=[Bid(price=float(bid["price"]), size=float(bid["size"]))
                  for bid in json["bids"]],
            mid_price=float(json["mid_price"])
        )

    def order(self, item, order_type, side, price, size):
        ORDER_RESOURCE = "/v1/me/sendchildorder"
        params = {
            "product_code": item,
            "child_order_type": order_type.upper(),
            "side": side.upper(),
            "price": price,
            "size": size
        }
        if order_type.lower() != "limit":
            params.pop('price')

        json = self.httpPost(BITFLYER_REST_URL,
                             ORDER_RESOURCE, params, self._apikey, self._secretkey)
        return json["child_order_acceptance_id"]

    def get_order(self, symbol, order_id):
        print("not implemented!")

    def balance(self):
        BALANCE_RESOURCE = "/v1/me/getbalance"
        params = {
        }
        json = self.httpGet(BITFLYER_REST_URL,
                            BALANCE_RESOURCE, params, self._apikey, self._secretkey)
        balances = {}
        for j in json:
            balances[j['currency_code']] = [j["amount"], j["available"]]
        return balances
