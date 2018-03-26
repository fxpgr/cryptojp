#!/usr/bin/python
# -*- coding: utf-8 -*-
from .base.exchange import *
import time
import requests
from datetime import datetime
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
            sign = hmac.new((bytes(hashId.digest())).lower(
            ), str.encode(text), hashlib.sha256).hexdigest()
            params['signature'] = sign
            params['key'] = apikey
            params['nonce'] = timestamp
            return self.session.get('https://' + url + resource, data=params).json()

        def httpPost(url, resource, params, apikey, secretkey):
            timestamp = str(time.time())
            coin = params['coin']
            text = "key={}&coin={}&nonce={}".format(apikey, coin, timestamp)
            hashId = hashlib.md5()
            hashId.update(repr(secretkey).encode('utf-8'))
            sign = hmac.new((bytes(hashId.digest())).lower(
            ), str.encode(text), hashlib.sha256).hexdigest()
            params['signature'] = sign
            params['key'] = apikey
            params['nonce'] = timestamp
            return self.session.post('https://' + url + resource, data=json.dumps(params)).json()

        super(Btcbox, self).__init__(apikey, secretkey)
        self.session = requests.session()
        self.httpPost = httpPost
        self.httpGet = httpGet

    def __del__(self):
        self.session.close()

    def markets(self):
        ret = []
        ret.append(CurrencyPair(trading="BTC", settlement="JPY"))
        ret.append(CurrencyPair(trading="LTC", settlement="JPY"))
        ret.append(CurrencyPair(trading="DOGE", settlement="JPY"))
        ret.append(CurrencyPair(trading="BCH", settlement="JPY"))
        return ret

    def ticker(self, trading, settlement):
        TICKER_RESOURCE = "/api/v1/ticker"
        params = {
            "coin": trading.lower()
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

    def order(self, trading, settlement, order_type, side, price, size):
        ORDER_RESOURCE = "/api/v1/trade_add"
        params = {
            "amount": size,
            "side": side.lower(),
            "price": price,
            "coin": trading.lower() + "_" + settlement.upper(),
        }
        json = self.httpPost(BTCBOX_REST_URL, ORDER_RESOURCE,
                             params, self._apikey, self._secretkey)
        return json["id"]

    def get_open_orders(self, symbol="btc"):
        OPEN_ORDERS_RESOURCE = "/api/v1/trade_list"
        params = {
            "coin": symbol,
            "type": "open",
        }
        json = self.httpGet(BTCBOX_REST_URL,
                            OPEN_ORDERS_RESOURCE, params, self._apikey, self._secretkey)
        return json

    def cancel_order(self, symbol, order_id):
        CANCEL_ORDERS_RESOURCE = "/api/v1/trade_cancel"
        params = {
            "coin": symbol,
            "id": order_id,
        }
        self.httpGet(BTCBOX_REST_URL,
                     CANCEL_ORDERS_RESOURCE, params, self._apikey, self._secretkey)

    def get_fee(self):
        return 0

    def balance(self, currency_code="btc"):
        BALANCE_RESOURCE = "/api/v1/balance/"
        params = {'coin': currency_code.lower()}
        json = self.httpGet(BTCBOX_REST_URL, BALANCE_RESOURCE,
                            params, self._apikey, self._secretkey)

        balances = {currency_code.upper(): [float(json[currency_code.lower() + '_balance']) +
                                            float(json[currency_code.lower() + '_lock']),
                                            float(json[currency_code.lower() + '_balance'])]}
        return balances
