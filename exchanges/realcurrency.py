import requests
import json

from .base.exchange import *


class RealCurrency(Exchange):
    def __init__(self, apikey, secretkey):
        super().__init__(apikey, secretkey)
        self.session = requests.session()
