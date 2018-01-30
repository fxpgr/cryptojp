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


QUOINE_REST_URL = 'api.quoine.com'
import jwt


class Quoine(Exchange):
    def __init__(self, apikey, secretkey):
        def httpGet(url, resource, params, apikey, sign, *args, **kwargs):
            payload = {}
            payload['nonce'] = str(int("{:.6f}".format(
                time.time()).replace('.', '')))
            payload['path'] = resource
            payload['token_id'] = self._apikey
            headers = {
                'Accept': 'application/json',
                'X-Quoine-API-Version': '2',
                "X-Quoine-Auth": apikey,
                "Sign": jwt.encode(payload, self._secretkey, 'HS256'),
            }
            return self.session.get('https://' + url + resource,
                                    headers=headers, data=params).json()

        def httpPost(url, resource, params, apikey, sign, *args, **kwargs):
            payload = {}
            payload['nonce'] = str(int("{:.6f}".format(
                time.time()).replace('.', '')))
            payload['path'] = resource
            payload['token_id'] = self._apikey
            headers = {
                'Accept': 'application/json',
                'X-Quoine-API-Version': '2',
                "X-Quoine-Auth": apikey,
                "Sign": jwt.encode(payload, self._secretkey, 'HS256'),
            }
            return self.session.post('https://' + url + resource,
                                     headers=headers, data=params).json()
        super().__init__(apikey, secretkey)
        self.session = requests.session()
        self.httpPost = httpPost
        self.httpGet = httpGet

    def markets(self):
        MARKETS_RESOURCE = "/products"
        json = self.session.get('https://' + QUOINE_REST_URL +
                                MARKETS_RESOURCE).json()
        self.market_dict = dict(
            [[j['id'], j['currency_pair_code']] for j in json])
        return tuple([j['currency_pair_code'] for j in json])

    def ticker(self, pair='BTCUSD'):
        TICKER_RESOURCE = "/products/code/CASH/%s" % (pair)
        params = {}
        json = self.session.get('https://' + QUOINE_REST_URL +
                                TICKER_RESOURCE).json()

        utc = datetime.utcfromtimestamp(time.time())
        return Ticker(
            timestamp=calendar.timegm(utc.timetuple()),
            last=float(json["last_traded_price"]),
            ask=float(json["market_ask"]),
            bid=float(json["market_bid"]),
            high=float(json["high_market_ask"]),
            low=float(json["low_market_bid"]),
            volume=float(json["volume_24h"]),
        )

    def board(self, item='BTCUSD'):
        if not self.market_dict:
            self.markets()
        product_id = tuple(self.market_dict.keys())[
            tuple(self.market_dict.values()).index(item)]
        BOARD_RESOURCE = "/products/%s/price_levels" % product_id
        params = {}
        json = self.session.get('https://' + QUOINE_REST_URL +
                                BOARD_RESOURCE).json()
        return Board(
            asks=[Ask(price=float(ask[0]), size=float(ask[1]))
                  for ask in json["buy_price_levels"]],
            bids=[Bid(price=float(bid[0]), size=float(bid[1]))
                  for bid in json["sell_price_levels"]],
            mid_price=(float(json["buy_price_levels"][0][0]) +
                       float(json["sell_price_levels"][0][0])) / 2
        )

    def balance(self):
        BALANCE_RESOURCE = "/accounts/balance"
        params = {
        }
        json = self.httpGet(QUOINE_REST_URL,
                            BALANCE_RESOURCE, params, self._apikey, self._secretkey)

        balances = {}
        for j in json:
            balances[j['currency']] = [
                float(j["balance"]), float(j["balance"])]
        return balances

    def order(self, item, order_type, side, price, size, *args, **kwargs):
        ORDER_RESOURCE = "/orders"
        params = {
            "order_type": order_type.lower(),
            "product_id": item,
            "side": side.lower(),
            "price": price,
            "quantity": size
        }
        json = self.httpPost(QUOINE_REST_URL,
                             ORDER_RESOURCE, params, self._apikey, self._secretkey)
        return json["id"]
