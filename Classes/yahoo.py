#!/usr/bin/python
import yfinance as yf

#https://github.com/ranaroussi/yfinance

class Yahoo(object):

    def print(self, name):
        stock = yf.Ticker(name)
        print(stock.info["regularMarketPrice"])
        print(stock.info)
        # print(stock.cashflow.loc['Total Cash From Operating Activities'] - stock.cashflow.loc['Capital Expenditures']) 
        print(stock.shares)

if __name__ == "__main__":
    yahoo = Yahoo()
    yahoo.print("VIAC")