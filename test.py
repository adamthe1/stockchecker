import matplotlib.pyplot as plt
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import numpy as np
import pandas
import math as m
from eater import eater
from findhammers import ishammer
from adx import caladx
from macddone import findmacd, findemaofmacd
from trendline import getgoodeqs, changevars, checkclose, height


class stock():
    def __init__(self, stockdata):
        self.stockdata = stockdata

        # get all data needed from stockdata
        self.openpoints = stockdata[0]
        self.highpoints = stockdata[1]
        self.lowpoints = stockdata[2]
        self.closepoints = stockdata[3]
        self.volume = stockdata[6]

        self.checkdays = 5
        self.gethammerlist()
        self.geteaterlist()

        self.goodeqs = getgoodeqs(stockdata)  # find the eqs that are trendline and parallel
        self.topeqs = list(self.goodeqs[0])  # split them into top and bot
        self.boteqs = list(self.goodeqs[1])
        # print(self.topeqs[0].nums)

        self.macd = findmacd(stockdata)  # get macd
        self.emamacd = findemaofmacd(self.macd, 9)
        for i in range(len(self.macd) - len(self.emamacd)):  # fix length macd
            self.macd.pop(0)

    def gethammerlist(self):
        self.hammerlist = []
        for i in range(self.checkdays, 0, -1):
            spotdata = [self.openpoints[-i], self.highpoints[-i], self.lowpoints[-i], self.closepoints[-i]]
            self.hammerlist.append(ishammer(spotdata))

    def geteaterlist(self):
        x = - self.checkdays - 1
        checklist = [self.openpoints[x:], self.highpoints[x:], self.lowpoints[x:],
                     self.closepoints[x:]]  # the first one isnt checked but is needed
        self.eaterlist = eater(checklist)
        self.eaterlist.pop(0)  # because first one wasnt even checked so we need only past checkdays days


# listofstocks = []


def main():
    listofstocks = []
    for i in ['LOW', 'NFLX', 'CMCSA']:
        stock1 = stock(getdailydata(i))
        for j in stock1.eaterlist:
            if j != 'no':
                print(stock1.eaterlist)
                listofstocks.append(stock1)
    for i in listofstocks:
        print(i.stockdata[5])
    """
    them = stock1.openpoints, stock1.highpoints, stock1.lowpoints, stock1.closepoints, stock1.volume
    plotshow(them)
    eq = regression(range(len(stock1.closepoints) - 30, len(stock1.closepoints)), stock1.closepoints[-30:])

    xmin = np.array(range(len(stock1.closepoints) - 30, len(stock1.closepoints)))
    ymin = xmin * eq[0] + eq[1]
    plt.plot(xmin, ymin)  # same but min
    plt.show()
    """




def regression(listpointsx, listpointsy):
    meanx = np.mean(listpointsx)
    meany = np.mean(listpointsy)
    sumtop = 0
    sumbot = 0
    for i in range(len(listpointsx)):
        sumtop += (listpointsx[i] - meanx) * (listpointsy[i] - meany)
        sumbot += (listpointsx[i] - meanx) ** 2
    slope = sumtop / sumbot
    n = meany - meanx * slope
    return slope, n



def plotshow(them):     # show graph of stock in candles
    for spot in range(len(them[0])):
        firstpointx = spot
        secondpointx = spot
        firstpointy = them[1][spot]
        secondpointy = them[2][spot]
        yvalues = [firstpointy, secondpointy]
        xvalues = [firstpointx, secondpointx]
        plt.plot(xvalues, yvalues, linewidth=1, color='black')
        firstpointy = them[0][spot]
        secondpointy = them[3][spot]
        yvalues = [firstpointy, secondpointy]
        volumevalue = them[4][spot]
        if firstpointy < 10:
            amount = 1
        elif firstpointy < 100:
            amount = 10
        else:
            amount = 100
        while int(volumevalue / amount) > 0:
            volumevalue = volumevalue / 10
        yvolumevalues = (0, volumevalue)
        if firstpointy > secondpointy:
            plt.plot(xvalues, yvalues, linewidth=5, color='red')
            plt.plot(xvalues, yvolumevalues, linewidth=3, color='red')
        else:
            plt.plot(xvalues, yvalues, linewidth=5, color='green')
            plt.plot(xvalues, yvolumevalues, linewidth=3, color='green')
        firstpointy = them[2][spot]
        secondpointy = them[3][spot]
        yvalues = [firstpointy, secondpointy]
        plt.plot(xvalues, yvalues, linewidth=1, color='black')


def getdailydata(name):
    my_share = share.Share(name)
    symbol_data = None
    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_MONTH, 4, share.FREQUENCY_TYPE_DAY, 1)
    except YahooFinanceError as e:
        print(e.message)
        return 'bad'
    # print(len(symbol_data['open']))
    return (symbol_data['open'], symbol_data['high'], symbol_data['low'],
            symbol_data['close'], symbol_data['timestamp'], name, symbol_data['volume'])




if __name__ == '__main__':
    main()