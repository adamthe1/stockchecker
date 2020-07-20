import requests
from get_all_tickers import get_tickers as gt
from datetime import datetime
from threading import Thread
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import csv
from time import sleep
from sys import exit

stocklist = []
targetfile = 'stocklist.csv'
# targetfile = 'smp100.csv'
with open(targetfile, 'r') as stocks:
    stockreader = csv.reader(stocks, delimiter='\n')
    for row in stockreader:
        stocklist.append(row[0])

class data4stocks():
    def __init__(self):
        self.data1 = []
        self.data2 = []
        self.data3 = []
        self.data4 = []

data = data4stocks()


def main(stocklist):
    try:
        for i in range(0, len(stocklist), 4):
            print(i)
            Thread(target=first, args=(i,)).start()
            Thread(target=second, args=(i+1,)).start()
            Thread(target=third, args=(i+2,)).start()
            Thread(target=fourth, args=(i+3,)).start()
            sleep(0.5)

    except KeyboardInterrupt:
        print('ok then')
        exit(1)

def first(spot):
    global data
    data.data1 = getdailydata(stocklist[spot])

def second(spot):
    global data
    data.data2 = getdailydata(stocklist[spot])

def third(spot):
    global data
    data.data3 = getdailydata(stocklist[spot])

def fourth(spot):
    global data
    data.data4 = getdailydata(stocklist[spot])


def getdailydata(name):
    stockname = name
    my_share = share.Share(stockname)
    symbol_data = None
    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_MONTH, 4, share.FREQUENCY_TYPE_DAY, 1)
    except YahooFinanceError as e:
        print(e.message)
        exit(1)
        # print(len(symbol_data['open']))
    return (symbol_data['open'], symbol_data['high'], symbol_data['low'],
           symbol_data['close'], symbol_data['timestamp'], stockname, symbol_data['volume'])




if __name__ == '__main__':
    main(stocklist)