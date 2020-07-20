from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import numpy as np
import matplotlib.pyplot as plt
import csv
from datetime import datetime
from threading import Thread
from trendline import getgoodeqs, changevars, checkclose
from macdtest import findmacd, findemaofmacd
from adx import caladx
from findhammers import ishammer
from eater import eater

class data4stocks():
    def __init__(self):
        data1 = []
        data2 = []
        data3 = []
        data4 = []
        data5 = []

data = data4stocks()  # class to thread 5 stock datas together

stocklist = []
targetlist = 'stocklist.csv'

with open(targetlist, 'r') as stocks:
    stockreader = csv.reader(stocks, delimiter='\n')
    for row in stockreader:
        stocklist.append(row[0])


def main():
    choose = input('for stock plot 1, for 4 step check stocks good 2: ')
    if int(choose) == 1:
        stockplot()
    if int(choose) == 2:
        fourstepcheck()

def stockplot():
    stockname = input('i need a name: ')
    stockinfo = getdailydata(stockname)
    if data == 'bad':
        exit(1)
    list, signal = [0], [0]
    listspot = np.array(range(len(list)))
    signalspot = np.array(range(len(signal)))

    lines = []
    xaxis = []

    for num in range(len(list)):
        xaxis.append(0)
        lines.append(list[num] - signal[num])
        xvalues = [num, num]
        yvalues = [0, lines[num]]
        if num == 0:
            continue
        if lines[num] > lines[num - 1]:
            plt.plot(xvalues, yvalues, color='green')
        else:
            plt.plot(xvalues, yvalues, color='red')
    plt.plot(listspot, xaxis, linewidth=0, color='black')
    plt.plot(listspot, list, color='black')
    plt.plot(signalspot, signal, color='red')

    plt.show()


def checkstocks():
    start = 0
    end = len(stocklist)
    for spot in range(start, end):
        ts = threader(spot)   # amount of stocks data4stocks is storing
        for t in ts:
            try:
                if t == 0:
                    fourstepcheck(data.data1)
                if t == 1:
                    fourstepcheck(data.data2)
                if t == 2:
                    fourstepcheck(data.data3)
                if t == 3:
                    fourstepcheck(data.data4)
                if t == 4:
                    fourstepcheck(data.data5)
            except TypeError:
                print('(TypeError) this stock nope: ' + stocklist[spot + t])
            except IndexError:
                print('(IndexError) this stock shits: ' + stocklist[spot + t])


def fourstepcheck(stockdata):   # chk1 - check if candle close to line 2 - check if slope is up
    chk1 = False           # 3 - check if macd is cutting and adx good 4 - check if candles
    chk2 = None  # its a string of 'up' or 'down' or 'norm'
    chk3 = False
    chk4 = False

    #Get all data needed for checks.
    openpoints = stockdata[0]
    highpoints = stockdata[1]
    lowpoints = stockdata[2]
    closepoints = stockdata[3]

    changevars(0.1, 8, 4)
    goodeqs = getgoodeqs(stockdata)
    topeqs = list(goodeqs[0])
    boteqs = list(goodeqs[1])
    closetop, closebot = checkclose(goodeqs, highpoints, lowpoints)

    macdlist = findmacd(stockdata)
    emamacd = findemaofmacd(macdlist, 9)

    plusdi, minusdi, adx = caladx(stockdata)

    checkdays = 3  # amount of days to check if they're a hammer or eater
    hammerlist = []  # list of hammerdays strings to check if theyre a hammer ex: ['sred', 'no', 'ngreen'
    spotdata = [openpoints[-checkdays], highpoints[-checkdays], lowpoints[-checkdays], closepoints[-checkdays]]
    checklist = [spotdata]
    for i in range(checkdays, 0, -1):
        spotdata = [openpoints[-i], highpoints[-i], lowpoints[-i], closepoints[-i]]
        hammerlist.append(ishammer(spotdata))
        checklist.append(spotdata)
    eaterlist = eater(checklist)


















    pass



def threader(spot):
    try:
        t1 = Thread(target=first, args=(spot,))
        t2 = Thread(target=second, args=(spot + 1,))
        t3 = Thread(target=third, args=(spot + 2,))
        t4 = Thread(target=fourth, args=(spot + 3,))
        t5 = Thread(target=fifth, args=(spot + 4,))
        threads = [t1, t2, t3, t4, t5]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print('we out boys')
        exit(-1)
    return len(threads)


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

def fifth(spot):
    global data
    data.data5 = getdailydata(stocklist[spot])



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
            return 'bad'
        return (symbol_data['open'], symbol_data['high'], symbol_data['low'],
                symbol_data['close'], symbol_data['timestamp'], name, symbol_data['volume'])
    except TypeError:
        print(" non subscriptable: " + str(name), end=' ')
        return 'bad'


if __name__ == '__main__':
    main()
