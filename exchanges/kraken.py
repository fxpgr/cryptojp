#!/usr/bin/python
# -*- coding: utf-8 -*-
from .base.exchange import *
import time
import requests
from datetime import datetime
from urllib.parse import urlencode
import calendar
import hmac
import hashlib
import base64

KRAKEN_REST_URL = 'api.kraken.com'


class Kraken(Exchange):
    def __init__(self, apikey, secretkey):
        def httpPost(url, resource, params, apikey):
            nonce = int("{:.6f}".format(
                time.time()).replace('.', ''))
            message = resource + \
                hashlib.sha256(str(nonce) + urlencode(params)).digest()
            headers = {
                "API-Key": apikey,
                "API-Sign": base64.b64encode((hmac.new(base64.b64decode(secretkey), message, hashlib.sha512)).digest()),
            }
            return self.session.post('https://' + url + resource,
                                     headers=headers).json()
        super().__init__(apikey, secretkey)
        self.session = requests.session()
        self.httpPost = httpPost

    def markets(self):
        MARKETS_RESOURCE = "/0/public/AssetPairs"
        json = self.session.get('https://' + KRAKEN_REST_URL +
                                MARKETS_RESOURCE).json()
        return tuple([c for c in json['result']])

    def ticker(self, pair='XXBTZJPY'):
        TICKER_RESOURCE = "/0/public/Ticker?pair=" + pair
        json = self.session.get('https://' + KRAKEN_REST_URL +
                                TICKER_RESOURCE).json()

        utc = datetime.utcfromtimestamp(time.time())
        return Ticker(
            timestamp=calendar.timegm(utc.timetuple()),
            last=float(json["result"][pair]["c"][0]),
            bid=float(json["result"][pair]["b"][0]),
            ask=float(json["result"][pair]["a"][0]),
            high=float(json["result"][pair]["h"][0]),
            low=float(json["result"][pair]["l"][0]),
            volume=float(json["result"][pair]["v"][0])
        )

    def board(self, pair='XXBTZJPY'):
        BOARD_RESOURCE = "/0/public/Depth?pair=" + pair
        json = self.session.get('https://' + KRAKEN_REST_URL +
                                BOARD_RESOURCE).json()
        return Board(
            asks=[Ask(price=float(ask[0]), size=float(ask[1]))
                  for ask in json["result"][pair]["asks"]],
            bids=[Bid(price=float(bid[0]), size=float(bid[1]))
                  for bid in json["result"][pair]["bids"]],
            mid_price=(float(json["result"][pair]["asks"][0][0]) +
                       float(json["result"][pair]["bids"][0][0])) / 2
        )

    def order(self, item, order_type, side, price, size):
        ORDER_RESOURCE = "/0/private/AddOrder"
        params = {
            "pair": item,
            "type": side,
            "order_type": order_type,
            "price": price,
            "volume": size,
        }
        json = self.httpPost(KRAKEN_REST_URL,
                             ORDER_RESOURCE, params, self._apikey, self._secretkey)
        return json["txid"]

    def balance(self):
        BALANCE_RESOURCE = "/api/v1/balance/"
        params = {
        }
        json = self.httpPost(KRAKEN_REST_URL,
                             BALANCE_RESOURCE, params, self._apikey, self._secretkey)
        return json["result"]["tb"]
