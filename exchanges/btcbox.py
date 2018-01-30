#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from .base.exchange import *
import time
import requests
from datetime import datetime
from urllib.parse import urlencode
import calendar
import hmac
import hashlib
import json

BTCBOX_REST_URL = 'www.btcbox.co.jp'


class Btcbox(Exchange):
    def __init__(self, apikey, secretkey):
        def httpGet(url, resource, params, apikey, secretkey):
            timestamp = str(time.time())
            coin = params['coin']
            text = "key={}&coin={}&nonce={}".format(apikey, coin, timestamp)
            hashId = hashlib.md5()
            hashId.update(repr(secretkey).encode('utf-8'))
            sign = hmac.new(str.encode(str(hashId.digest())).lower(
            ), str.encode(text), hashlib.sha256).hexdigest()
            params['signature'] = sign
            params['key'] = apikey
            params['nonce'] = timestamp
            return self.session.get('https://' + url + resource,  data=params).json()

        def httpPost(url, resource, params, apikey, secretkey, *args, **kwargs):
            timestamp = str(time.time())
            coin = params['coin']
            text = "key={}&coin={}&nonce={}".format(apikey, coin, timestamp)
            hashId = hashlib.md5()
            hashId.update(repr(secretkey).encode('utf-8'))
            sign = hmac.new(str.encode(str(hashId.digest())).lower(
            ), str.encode(text), hashlib.sha256).hexdigest()
            params['signature'] = sign
            params['key'] = apikey
            params['nonce'] = timestamp
            return self.session.post('https://' + url + resource, data=json.dumps(params)).json()
        super().__init__(apikey, secretkey)
        self.session = requests.session()
        self.httpPost = httpPost
        self.httpGet = httpGet

    def markets(self):
        return ("btc_jpy", "ltc_jpy", "doge_jpy", "bch_jpy")

    def ticker(self, item=''):
        TICKER_RESOURCE = "/api/v1/ticker"
        params = {
            "coin": item.replace("_jpy", "") if item else "btc"
        }
        json = self.session.get('https://' + BTCBOX_REST_URL +
                                TICKER_RESOURCE).json()
        utc = datetime.utcfromtimestamp(time.time())
        return Ticker(
            timestamp=calendar.timegm(utc.timetuple()),
            last=float(json["last"]),
            bid=float(json["sell"]),
            ask=float(json["buy"]),
            high=float(json["high"]),
            low=float(json["low"]),
            volume=float(json["vol"])
        )

    def board(self, item=''):
        BOARD_RESOURCE = "/api/v1/depth"
        params = {}
        json = self.session.get('https://' + BTCBOX_REST_URL +
                                BOARD_RESOURCE).json()
        return Board(
            asks=[Ask(price=float(ask[0]), size=float(ask[1]))
                  for ask in json["asks"]],
            bids=[Bid(price=float(bid[0]), size=float(bid[1]))
                  for bid in json["bids"]],
            mid_price=(float(json["asks"][-1][0]) +
                       float(json["bids"][0][0])) / 2
        )

    def order(self, item, order_type, side, price, size, *args, **kwargs):
        ORDER_RESOURCE = "/api/v1/trade_add"
        params = {
            "amount": size,
            "side": side.lower(),
            "price": price,
            "coin": item,
        }
        json = self.httpPost(BTCBOX_REST_URL, ORDER_RESOURCE,
                             params, self._apikey, self._secretkey)
        return json["id"]

    def balance(self, currency_code="btc"):
        BALANCE_RESOURCE = "/api/v1/balance/"
        params = {
        }
        params['coin'] = currency_code.lower()
        json = self.httpGet(BTCBOX_REST_URL, BALANCE_RESOURCE,
                            params, self._apikey, self._secretkey)

        balances = {}
        balances[currency_code.upper()] = [float(json[currency_code.lower() + '_balance']) +
                                           float(json[currency_code.lower() + '_lock']), float(json[currency_code.lower() + '_balance'])]
        return balances
