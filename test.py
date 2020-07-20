import matplotlib.pyplot as plt
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import numpy as np
# import pandas
import math as m
from eater import eater

class eq:
    def __init__(self, slope, n):
        self.slope = slope
        self.n = n

def main():
    stockdata = getdailydata(str(input('name thing ')))
    openpoints = stockdata[0]
    highpoints = stockdata[1]
    lowpoints = stockdata[2]
    closepoints = stockdata[3]
    checkdays = 3  # amount of days to check if they're a hammer or eater
    hammerlist = []  # list of hammerdays strings to check if theyre a hammer ex: ['sred', 'no', 'ngreen'
    spotdata = [openpoints[-checkdays], highpoints[-checkdays], lowpoints[-checkdays], closepoints[-checkdays]]
    checklist = [spotdata]
    for i in range(checkdays, 0, -1):
        print()
        spotdata = [openpoints[-i], highpoints[-i], lowpoints[-i], closepoints[-i]]
        checklist.append(spotdata)
    eaterlist = eater(checklist)
    print(eaterlist)





def getdailydata(name):
    my_share = share.Share(name)
    symbol_data = None
    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_MONTH, 12, share.FREQUENCY_TYPE_DAY, 1)
    except YahooFinanceError as e:
        print(e.message)
        return 'bad'
    # print(len(symbol_data['open']))
    return (symbol_data['open'], symbol_data['high'], symbol_data['low'],
            symbol_data['close'], symbol_data['timestamp'], name, symbol_data['volume'])




if __name__ == '__main__':
    main()