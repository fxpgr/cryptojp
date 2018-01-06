#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from tools.HttpHMACUtil import buildMySign, httpGet, httpPost, getnonce
from .base.exchange import *
import time
from datetime import datetime
import time
import calendar

KEYS_GLOBAL = '../keys.json'
KEYS_LOCAL = '../keys.local.json'
QUOINE_REST_URL = 'developers.quoine.com' if os.path.exists(
    KEYS_LOCAL) else 'api.quoine.com'


class Quoine(Exchange):
    market_dict = {}

    def markets(self):
        MARKETS_RESOURCE = "/products"
        json = httpGet(QUOINE_REST_URL, MARKETS_RESOURCE, {}, self._apikey, {})
        self.market_dict = dict(
            [[j['id'], j['currency_pair_code']] for j in json])
        return tuple([j['currency_pair_code'] for j in json])

    def ticker(self, pair='BTCUSD'):
        TICKER_RESOURCE = "/products/code/CASH/%s" % (pair)
        params = {}
        sign = buildMySign(params, self._secretkey,
                           QUOINE_REST_URL + TICKER_RESOURCE)
        json = httpGet(QUOINE_REST_URL, TICKER_RESOURCE,
                       params, self._apikey, sign)

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
        json = self.httpGet(QUOINE_REST_URL, BOARD_RESOURCE,
                            params, self._apikey, params)
        return Board(
            asks=[Ask(price=float(ask[0]), size=float(ask[1]))
                  for ask in json["buy_price_levels"]],
            bids=[Bid(price=float(bid[0]), size=float(bid[1]))
                  for bid in json["sell_price_levels"]],
            mid_price=(float(json["buy_price_levels"][0][0]) +
                       float(json["sell_price_levels"][0][0])) / 2
        )

    def order(self, item, order_type, side, price, size, *args, **kwargs):
        if not self.market_dict:
            self.markets()
        product_id = tuple(self.market_dict.keys())[
            tuple(self.market_dict.values()).index(item)]
        ORDER_RESOURCE = "/orders"
        params = {
            "order_type": order_type.lower(),
            "product_id": product_id,
            "side": side.lower(),
            "price": price,
            "quantity": size
        }
        sign = buildMySign(params, self._secretkey,
                           QUOINE_REST_URL + ORDER_RESOURCE)
        json = self.httpPost(QUOINE_REST_URL, ORDER_RESOURCE,
                             params, self._apikey, sign)
        return json["id"]
