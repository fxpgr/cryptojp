#!/usr/bin/python
# -*- coding: utf-8 -*-
from .base.exchange import *
import time
import requests
import sys
if sys.version_info.major <= 2:
    from urllib import urlencode
else:
    from urllib.parse import urlencode
import hmac
import hashlib

COINCHECK_REST_URL = 'coincheck.jp'


class Coincheck(Exchange):
    def __init__(self, apikey, secretkey):
        def httpGet(url, resource, params, apikey, secretkey):
            nonce = int("{:.6f}".format(
                time.time()).replace('.', ''))
            text = str.encode(str(nonce) + "https://" + url +
                              resource + urlencode(params))
            headers = {
                "ACCESS-KEY": apikey,
                "ACCESS-NONCE": str(nonce),
                "ACCESS-SIGN":  hmac.new(str.encode(secretkey), text, hashlib.sha256).hexdigest(),
            }
            return self.session.get('https://' + url + resource,
                                    headers=headers, data=urlencode(params)).json()

        def httpPost(url, resource, params, apikey, secretkey):
            nonce = int("{:.6f}".format(
                time.time()).replace('.', ''))
            text = str.encode(str(nonce) + "https://" + url +
                              resource + urlencode(params))
            headers = {
                "ACCESS-KEY": apikey,
                "ACCESS-NONCE": str(nonce),
                "ACCESS-SIGN":  hmac.new(str.encode(secretkey), text, hashlib.sha256).hexdigest(),
            }
            return self.session.post('https://' + url + resource,
                                     headers=headers, data=urlencode(params)).json()

        def httpDelete(url, resource, params, apikey, secretkey):
            nonce = int("{:.6f}".format(
                time.time()).replace('.', ''))
            text = str.encode(str(nonce) + "https://" + url +
                              resource + urlencode(params))
            headers = {
                "ACCESS-KEY": apikey,
                "ACCESS-NONCE": str(nonce),
                "ACCESS-SIGN":  hmac.new(str.encode(secretkey), text, hashlib.sha256).hexdigest(),
            }
            return self.session.delete('https://' + url + resource, headers=headers, data=urlencode(params)).json()

        super(Coincheck, self).__init__(apikey, secretkey)
        self.session = requests.session()
        self.httpPost = httpPost
        self.httpGet = httpGet
        self.httpDelete = httpDelete

    def __del__(self):
        self.session.close()

    def markets(self):
        return (CurrencyPair(trading="BTC", settlement="JPY"),)

    def ticker(self, item=''):
        TICKER_RESOURCE = "/api/ticker"
        json = self.session.get('https://' + COINCHECK_REST_URL +
                                TICKER_RESOURCE).json()

        return Ticker(
            timestamp=int(json["timestamp"]),
            last=float(json["last"]),
            bid=float(json["bid"]),
            ask=float(json["ask"]),
            high=float(json["high"]),
            low=float(json["low"]),
            volume=float(json["volume"])
        )

    def board(self, item=''):
        BOARD_RESOURCE = "/api/order_books"
        params = {}
        json = self.session.get('https://' + COINCHECK_REST_URL +
                                BOARD_RESOURCE).json()
        return Board(
            asks=[Ask(price=float(ask[0]), size=float(ask[1]))
                  for ask in json["asks"]],
            bids=[Bid(price=float(bid[0]), size=float(bid[1]))
                  for bid in json["bids"]],
            mid_price=(float(json["asks"][0][0]) +
                       float(json["bids"][0][0])) / 2
        )

    def order(self, trading, settlement, order_type, side, price, size):
        ORDER_RESOURCE = "/api/exchange/orders"
        if order_type.lower() == 'market':
            side = 'market_' + side
            if 'buy' in side.lower():
                params = {
                    "pair": trading.lower()+"_"+settlement.upper(),
                    "order_type": side,
                    "market_buy_amount": size
                }
            else:
                params = {
                    "pair": trading.lower()+"_"+settlement.upper(),
                    "order_type": side,
                    "amount": size
                }
        else:
            params = {
                "pair": trading.lower()+"_"+settlement.upper(),
                "order_type": side,
                "rate": price,
                "amount": size
            }
        json = self.httpPost(COINCHECK_REST_URL,
                             ORDER_RESOURCE, params, self._apikey, self._secretkey)
        return json["id"]

    def get_open_orders(self, symbol="BTC_JPY"):
        OPEN_ORDERS_RESOURCE = "/api/exchange/orders/opens"
        json = self.httpGet(COINCHECK_REST_URL,
                            OPEN_ORDERS_RESOURCE, {}, self._apikey, self._secretkey)
        return json

    def cancel_order(self, symbol,order_id):
        CANCEL_ORDERS_RESOURCE = "/api/exchange/orders/"+order_id
        self.httpDelete(COINCHECK_REST_URL,
                        CANCEL_ORDERS_RESOURCE, {}, self._apikey, self._secretkey)

    def get_fee(self, symbol = "BTC_JPY"):
        GET_FEE_RESOURCE = "/api/accounts"
        json = self.httpGet(COINCHECK_REST_URL, GET_FEE_RESOURCE, {}, self._apikey, self._secretkey)

        return [json["taker_fee"],json["maker_fee"]]

    def balance(self):
        BALANCE_RESOURCE = "/api/accounts/balance"
        params = {
        }
        json = self.httpGet(COINCHECK_REST_URL,
                            BALANCE_RESOURCE, params, self._apikey, self._secretkey)
        balances = {'JPY': [
            float(json['jpy']) + float(json['jpy_reserved']), float(json['jpy'])], 'BTC': [
            float(json['btc']) + float(json['btc_reserved']), float(json['btc'])]}
        return balances
