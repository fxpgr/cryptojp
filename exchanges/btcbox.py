#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
from tools.HttpHMACUtil import buildMySign,httpGet,httpPost,getnonce
from .base.exchange import *
from datetime import datetime
import time,calendar

BTCBOX_REST_URL = 'www.btcbox.co.jp'

class Btcbox(Exchange):
    def markets(self):
        return ("btc_jpy","ltc_jpy","doge_jpy","bch_jpy")

    def ticker(self,item = ''):
        TICKER_RESOURCE = "/api/v1/ticker/"
        params = {
            "coin": item.replace("_jpy","") if item else "btc"
        }
        json = httpGet(BTCBOX_REST_URL,TICKER_RESOURCE,params,self._apikey,params)
        utc = datetime.utcfromtimestamp(time.time())
        return Ticker(
            timestamp = calendar.timegm(utc.timetuple()),
            last = float(json["last"]),
            bid = None,
            ask = None,
            high = float(json["high"]),
            low = float(json["low"]),
            volume = float(json["vol"])
        )

    def trade(self,symbol,tradeType,price='',amount='',*args,**kwargs):
        TRADES_RESOURCE = "/api/v1/trade_add/"
        params = {
            'type':tradeType,
            'price':price,
            'amount':amount,
        }
        sign = buildMySign(params,self._secretkey,self._url+TRADES_RESOURCE)
        try:
            json = httpGet(self._url,TRADES_RESOURCE,params,self._apikey,sign)
            self.order_id = json['id']
            if json['result'] == "false":
                return False
            return self.order_id
        except:
            return False

    def check_trade(self,i):
        CHECK_ORDER_RESOURCE = "/api/v1/trade_add/"
        params = {
            'id':i,
        }
        sign = buildMySign(params,self._secretkey,self._url+CHECK_ORDER_RESOURCE)
        try:
            json = httpPost(self._url,CHECK_ORDER_RESOURCE,params,self._apikey,sign)
            status = json['status']
            if status == "closed":
                return True
            return False
        except:
            return False

    def cancel_trade(self,i):
        CHECK_ORDER_RESOURCE = "/api/v1/trade_add/"
        params = {
            'id':i,
        }
        sign = buildMySign(params,self._secretkey,self._url+CHECK_ORDER_RESOURCE)
        try:
            json = httpPost(self._url,CHECK_ORDER_RESOURCE,params,self._apikey,sign)
            result = json['result']
            if result == "true":
                return True
            return False
        except:
            return False


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
