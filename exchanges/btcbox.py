#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
from tools.HttpHMACUtil import buildMySign, httpGet, httpPost, getnonce
from .base.exchange import *
from datetime import datetime
import time
import calendar

BTCBOX_REST_URL = 'www.btcbox.co.jp'


class Btcbox(Exchange):
    def markets(self):
        return ("btc_jpy", "ltc_jpy", "doge_jpy", "bch_jpy")

    def ticker(self, item=''):
        TICKER_RESOURCE = "/api/v1/ticker"
        params = {
            "coin": item.replace("_jpy", "") if item else "btc"
        }
        json = self.httpGet(BTCBOX_REST_URL, TICKER_RESOURCE,
                            params, self._apikey, params)
        utc = datetime.utcfromtimestamp(time.time())
        return Ticker(
            timestamp=calendar.timegm(utc.timetuple()),
            last=float(json["last"]),
            bid=None,
            ask=None,
            high=float(json["high"]),
            low=float(json["low"]),
            volume=float(json["vol"])
        )

    def board(self, item=''):
        BOARD_RESOURCE = "/api/v1/depth"
        params = {}
        json = self.httpGet(BTCBOX_REST_URL, BOARD_RESOURCE,
                            params, self._apikey, params)
        return Board(
            asks=[Ask(price=float(ask[0]), size=float(ask[1]))
                  for ask in json["asks"]],
            bids=[Bid(price=float(bid[0]), size=float(bid[1]))
                  for bid in json["bids"]],
            mid_price=float(json["asks"][-1][0] + json["bids"][0][0]) / 2
        )

    def order(self, item, order_type, side, price, size, *args, **kwargs):
        ORDER_RESOURCE = "/api/v1/trade_add"
        params = {
            "amount": size,
            "side": side.lower(),
            "price": price,
        }
        sign = buildMySign(params, self._secretkey,
                           BTCBOX_REST_URL + ORDER_RESOURCE)
        params['signature'] = sign
        params['nonce'] = self.getnonce()
        params['key'] = self._apikey
        json = self.httpPost(BTCBOX_REST_URL, ORDER_RESOURCE,
                             params, self._apikey, sign)
        return json["id"]
