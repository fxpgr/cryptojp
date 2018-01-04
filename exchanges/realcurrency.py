import requests,json

class Spot():
    def ticker(self,symbol='USDJPY'):
        r = requests.get('https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.xchange%20where%20pair%20in%20(%22'+symbol+'%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys')
        data = json.loads(r.text)
        self.rate = float(data["query"]["results"]["rate"]["Rate"])
        self.vol = 0
