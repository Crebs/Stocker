# import libraries
import json
from typing_extensions import IntVar

class StockData:
    def __init__(self, symbol, df, intrinsicValue, currentMarketValue):
        self.symbol = symbol
        self.df = df
        self.iv = intrinsicValue
        self.mv = currentMarketValue