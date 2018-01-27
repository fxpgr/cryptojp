#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from .base.exchange import *
from datetime import datetime
import time
import calendar

KRAKEN_REST_URL = 'api.kraken.com'


class Kraken(Exchange):
    def markets(self):
        MARKETS_RESOURCE = "/0/public/AssetPairs"
        json = self.httpGet(
            KRAKEN_REST_URL, MARKETS_RESOURCE, {}, self._apikey, {})
        return tuple([c for c in json['result']])

    def ticker(self, pair='XXBTZJPY'):
        TICKER_RESOURCE = "/0/public/Ticker?pair=" + pair
        params = {}
        sign = self.buildMySign(params, self._secretkey,
                                KRAKEN_REST_URL + TICKER_RESOURCE)
        json = self.httpGet(KRAKEN_REST_URL, TICKER_RESOURCE,
                            params, self._apikey, sign)

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
        params = {}
        json = self.httpGet(KRAKEN_REST_URL, BOARD_RESOURCE,
                            params, self._apikey, params)
        return Board(
            asks=[Ask(price=float(ask[0]), size=float(ask[1]))
                  for ask in json["result"][pair]["asks"]],
            bids=[Bid(price=float(bid[0]), size=float(bid[1]))
                  for bid in json["result"][pair]["bids"]],
            mid_price=(float(json["result"][pair]["asks"][0][0]) +
                       float(json["result"][pair]["bids"][0][0])) / 2
        )

    def order(self, item, order_type, side, price, size, *args, **kwargs):
        ORDER_RESOURCE = "/0/private/AddOrder"
        params = {
            "pair": item,
            "type": side,
            "order_type": order_type,
            "price": price,
            "volume": size,
        }
        sign = self.buildMySign(params, self._secretkey,
                                KRAKEN_REST_URL + ORDER_RESOURCE)
        json = self.httpPost(KRAKEN_REST_URL, ORDER_RESOURCE,
                             params, self._apikey, sign)
        return json["txid"]
