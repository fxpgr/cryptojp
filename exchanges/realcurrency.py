import requests
from .base.exchange import *


class RealCurrency(Exchange):
    def __init__(self, apikey, secretkey):
        super(RealCurrency, self).__init__(apikey, secretkey)
        self.session = requests.session()
