#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from tools.HttpMD5Util import buildMySign,httpGet,httpPost
from settings import *

class Spot():
    def __init__(self):
        self._url = okcoinRESTURL
        self._apikey = okcoinapikey
        self._secretkey = okcoinsecretkey

    def ticker(self,symbol = ''):
        #ticker
        TICKER_RESOURCE = "/api/v1/ticker.do"
        params=''
        symbol=symbol.lower()
        symbol = symbol[0:3]+"_"+symbol[3:6]
        if symbol:
            params = 'symbol=%(symbol)s' %{'symbol':symbol}
            if symbol in ["btc_cny"]:
                self._url = "www.okcoin.cn"
                TICKER_RESOURCE = "/api/ticker.do"
            else:
                self._url = okcoinRESTURL
        json = httpGet(self._url,TICKER_RESOURCE,params)

        self.timestamp = int(json["date"])
        self.rate = float(json["ticker"]["last"])
        self.bid = float(json["ticker"]["buy"])
        self.ask = float(json["ticker"]["sell"])
        self.high = float(json["ticker"]["high"])
        self.low = float(json["ticker"]["low"])
        self.vol = 0
        #float(json["ticker"]["vol"])

    def depth(self,symbol = ''):
        DEPTH_RESOURCE = "/api/v1/depth.do"
        params=''
        if symbol:
            params = 'symbol=%(symbol)s' %{'symbol':symbol}
        return httpGet(self._url,DEPTH_RESOURCE,params)

    def trades(self,symbol = ''):
        TRADES_RESOURCE = "/api/v1/trades.do"
        params=''
        if symbol:
            params = 'symbol=%(symbol)s' %{'symbol':symbol}
        return httpGet(self._url,TRADES_RESOURCE,params)

    def balance(self):
        USERINFO_RESOURCE = "/api/v1/userinfo.do"
        params ={}
        params['api_key'] = self._apikey
        params['sign'] = buildMySign(params,self._secretkey)
        return httpPost(self._url,USERINFO_RESOURCE,params)

    def trade(self,symbol,tradeType,price='',amount=''):
        TRADE_RESOURCE = "/api/v1/trade.do"
        params = {
            'api_key':self._apikey,
            'symbol':symbol,
            'type':tradeType
        }
        if price:
            params['price'] = price
        if amount:
            params['amount'] = amount

        params['sign'] = buildMySign(params,self._secretkey)
        return httpPost(self._url,TRADE_RESOURCE,params)

    def batchTrade(self,symbol,tradeType,orders_data):
        BATCH_TRADE_RESOURCE = "/api/v1/batch_trade.do"
        params = {
            'api_key':self._apikey,
            'symbol':symbol,
            'type':tradeType,
            'orders_data':orders_data
        }
        params['sign'] = buildMySign(params,self._secretkey)
        return httpPost(self._url,BATCH_TRADE_RESOURCE,params)

    def cancelOrder(self,symbol,orderId):
        CANCEL_ORDER_RESOURCE = "/api/v1/cancel_order.do"
        params = {
             'api_key':self._apikey,
             'symbol':symbol,
             'order_id':orderId
        }
        params['sign'] = buildMySign(params,self._secretkey)
        return httpPost(self._url,CANCEL_ORDER_RESOURCE,params)

    def orderinfo(self,symbol,orderId):
         ORDER_INFO_RESOURCE = "/api/v1/order_info.do"
         params = {
             'api_key':self._apikey,
             'symbol':symbol,
             'order_id':orderId
         }
         params['sign'] = buildMySign(params,self._secretkey)
         return httpPost(self._url,ORDER_INFO_RESOURCE,params)

    def ordersinfo(self,symbol,orderId,tradeType):
         ORDERS_INFO_RESOURCE = "/api/v1/orders_info.do"
         params = {
             'api_key':self._apikey,
             'symbol':symbol,
             'order_id':orderId,
             'type':tradeType
         }
         params['sign'] = buildMySign(params,self._secretkey)
         return httpPost(self._url,ORDERS_INFO_RESOURCE,params)

    def orderHistory(self,symbol,status,currentPage,pageLength):
           ORDER_HISTORY_RESOURCE = "/api/v1/order_history.do"
           params = {
              'api_key':self._apikey,
              'symbol':symbol,
              'status':status,
              'current_page':currentPage,
              'page_length':pageLength
           }
           params['sign'] = buildMySign(params,self._secretkey)
           return httpPost(self._url,ORDER_HISTORY_RESOURCE,params)
