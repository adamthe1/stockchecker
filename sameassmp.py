from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import numpy as np
import matplotlib.pyplot as plt
import csv
from datetime import datetime
from threading import Thread

stocklist = []
# targetfile = 'stocklist.csv'
targetfile = 'smp100.csv'
with open(targetfile, 'r') as stocks:
    stockreader = csv.reader(stocks, delimiter='\n')
    for row in stockreader:
        stocklist.append(row[0])


def main():
    # name = input('name of stock: ')
    smpdata = getdailydata('^gspc')
    difflist = []
    samelist = []
    for name in stocklist:
        stockdata = getdailydata(name)
        if stockdata == 'bad':
            samelist.append(0)
            difflist.append(0)
            continue
        same = 0
        diff = 0
        amn = 50
        for i in range(-1 * amn, 0):
            if (float(stockdata[3][i]) - float(stockdata[3][i - 1])) > 0 > (float(smpdata[3][i]) - float(smpdata[3][i - 1])):
                diff += 1
            if (float(stockdata[3][i]) - float(stockdata[3][i - 1])) < 0 < (float(smpdata[3][i]) - float(smpdata[3][i - 1])):
                diff += 1
            if (float(stockdata[3][i]) - float(stockdata[3][i - 1])) > 0 < (float(smpdata[3][i]) - float(smpdata[3][i - 1])):
                same += 1
            if (float(stockdata[3][i]) - float(stockdata[3][i - 1])) < 0 > (float(smpdata[3][i]) - float(smpdata[3][i - 1])):
                same += 1
        difflist.append(diff)
        samelist.append(same)
    for i in range(len(difflist)):
        print(str(stocklist[i]) + ' same: ' + str(samelist[i]) + ' diff: ' + str(difflist[i]))

    print('top diff: ')
    maxdiff = max(difflist)
    maxsame = max(samelist)
    for i, item in enumerate(stocklist):
        if maxdiff == difflist[i]:
            print(item)
    print('top same: ')
    for i, item in enumerate(stocklist):
        if maxsame == samelist[i]:
            print(item)

    print(len(stocklist), len(difflist), len(samelist))



def getdailydata(name):
    my_share = share.Share(name)
    symbol_data = None
    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_MONTH, 10, share.FREQUENCY_TYPE_DAY, 1)
    except YahooFinanceError as e:
        print(e.message)
        return 'bad'
    # print(len(symbol_data['open']))
    try:
        if not symbol_data['open']:
            print('no data: ' + str(name))
            return 'bad'
        return (symbol_data['open'], symbol_data['high'], symbol_data['low'],
                symbol_data['close'], symbol_data['timestamp'], name, symbol_data['volume'])
    except TypeError:
        print(" non subscriptable: " + str(name), end=' ')
        return 'bad'

if __name__ == "__main__":
    main()