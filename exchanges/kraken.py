#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from tools.HttpHMACUtil import buildMySign,httpGet,httpPost,getnonce
from .base.exchange import *
import time
from datetime import datetime
import time,calendar

KRAKEN_REST_URL = 'api.kraken.com'

class Kraken(Exchange):
    def markets(self):
        MARKETS_RESOURCE = "/0/public/AssetPairs"
        json = httpGet(KRAKEN_REST_URL,MARKETS_RESOURCE,{},self._apikey,{})
        return tuple([c for c in json['result']])

    def ticker(self,pair = 'XXBTZJPY'):
        TICKER_RESOURCE = "/0/public/Ticker?pair="+pair
        params = {}
        sign = buildMySign(params,self._secretkey,KRAKEN_REST_URL+TICKER_RESOURCE)
        json = httpGet(KRAKEN_REST_URL,TICKER_RESOURCE,params,self._apikey,sign)

        utc = datetime.utcfromtimestamp(time.time())
        return Ticker(
            timestamp = calendar.timegm(utc.timetuple()),
            last = float(json["result"][pair]["c"][0]),
            bid = float(json["result"][pair]["b"][0]),
            ask = float(json["result"][pair]["a"][0]),
            high = float(json["result"][pair]["h"][0]),
            low = float(json["result"][pair]["l"][0]),
            volume = float(json["result"][pair]["v"][0])
        )

    def board(self,pair = 'XXBTZJPY'):
        BOARD_RESOURCE = "/0/public/Depth?pair="+pair
        params = {}
        json = self.httpGet(KRAKEN_REST_URL,BOARD_RESOURCE,params,self._apikey,params)
        return Board(
            asks=[Ask(price=float(ask[0]),size=float(ask[1])) for ask in json["result"][pair]["asks"]],
            bids=[Bid(price=float(bid[0]),size=float(bid[1])) for bid in json["result"][pair]["bids"]],
            mid_price= (float(json["result"][pair]["asks"][0][0])+float(json["result"][pair]["bids"][0][0]))/2
        )

    def trades(self,symbol = ''):
        TRADES_RESOURCE = "/api/trades"
        params = {}
        sign = buildMySign(params,self._secretkey,self._url+TRADES_RESOURCE)
        return httpGet(self._url,TRADES_RESOURCE,params,self._apikey,sign)

    def history(self):
        USERINFO_RESOURCE = "/api/exchange/orders/transactions"
        params = {}
        sign = buildMySign(params,self._secretkey,self._url+USERINFO_RESOURCE)
        return httpGet(self._url,USERINFO_RESOURCE,params,self._apikey,sign)

    def ordersinfo(self):
        ORDERS_INFO_RESOURCE = "/api/exchange/orders/opens"
        params = {
         'api_key':self._apikey,
        }
        params['sign'] = buildMySign(params,self._secretkey,self._url+ORDERS_INFO_RESOURCE)
        sign = buildMySign(params,self._secretkey,self._url+ORDERS_INFO_RESOURCE)
        return httpPost(self._url,ORDERS_INFO_RESOURCE,params,self._apikey,sign)

    def trade(self,symbol,tradeType,price='',amount='',limit=''):
        TRADE_RESOURCE = "/api/exchange/orders"
        params = {
            'pair':symbol,
            'order_type':tradeType
        }
        if price:
            params['rate'] = price
        if amount:
            params['amount'] = amount
        sign = buildMySign(params,self._secretkey,self._url+TRADE_RESOURCE)
        return httpPost(self._url,TRADE_RESOURCE,params,self._apikey,sign)

    def balance(self):
        BALANCE_RESOURCE = "/api/accounts/balance"
        params = {}
        sign = buildMySign(params,self._secretkey,self._url+BALANCE_RESOURCE)
        return httpGet(self._url,BALANCE_RESOURCE,params,self._apikey,sign)

    def depth(self):
        DEPTH_RESOURCE = "/api/order_books"
        params = {}
        sign = buildMySign(params,self._secretkey,self._url+DEPTH_RESOURCE)
        return httpGet(self._url,DEPTH_RESOURCE,params,self._apikey,sign)
