from typing import Union

from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import numpy as np
import matplotlib.pyplot as plt
import csv
from datetime import datetime
from threading import Thread
from trendline import getgoodeqs, changevars, checkclose, height
from macddone import findmacd, findemaofmacd
from adx import caladx
from findhammers import ishammer
from eater import eater


class Data4stocks():
    def __init__(self):
        data1 = []
        data2 = []
        data3 = []
        data4 = []
        data5 = []


data = Data4stocks()  # class to thread 5 stock datas together

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
        pass


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
        ts = threader(spot)  # amount of stocks data4stocks is storing
        for t in ts:
            try:
                if t == 0:
                    pass
                if t == 1:
                    pass
                if t == 2:
                    pass
                if t == 3:
                    pass
                if t == 4:
                    pass
            except TypeError:
                print('(TypeError) this stock nope: ' + stocklist[spot + t])
            except IndexError:
                print('(IndexError) this stock shits: ' + stocklist[spot + t])


veryup = 0.7
bitup = 0.35  # amount the slope has to be above to be very up or a bit up for down its the same just minus


class stock():
    def __init__(self, stockdata):

        self.stockdata = stockdata

        # get all data needed from stockdata
        self.openpoints = stockdata[0]
        self.highpoints = stockdata[1]
        self.lowpoints = stockdata[2]
        self.closepoints = stockdata[3]

        self.checks = {}  # dictionary of all the checks
        # chk1 - check if candle close to line 2 - check if slope is up
        # 3 - check if macd is cutting or close 4 - adx good 5 - check if candles
        # for check 4 - checks 2 things if +di and -di cuts and if good trend (more than 25)

        self.goodeqs = getgoodeqs(stockdata)  # find the eqs that are trendline and parallel
        self.topeqs = list(self.goodeqs[0])  # split them into top and bot
        self.boteqs = list(self.goodeqs[1])

        # check if last candle is close to the trendline returns list of all stock trendlines
        # that the last one is close to
        self.closebot = None
        self.closetop = None
        self.isclose()

        self.macd = findmacd(stockdata)  # get macd
        self.emamacd = findemaofmacd(self.macd, 9)
        for i in range(len(self.macd) - len(self.emamacd)):  # fix length macd
            self.macd.pop(0)

        self.plusdi, self.minusdi, self.adx = caladx(stockdata)  # get adx

        self.checkdays = 4
        self.hammerlist = []
        self.gethammerlist()  # get hammers

        self.eaterlist = None
        self.geteaterlist()  # get eater

        self.isbetweeneqs = []  # check eqs the last one is between
        self.isbetween()

        if self.closebot or self.closetop:
            self.checks['check1'] = True

        self.upordown = []  # check if slope of eq is up or down -
        # list the same size of eqs list that has up or down for each
        # when do checks just see if up or down for the if
        self.checkupordown()

        self.macdcuts = self.checkmacdcut()
        if not self.checks['check3'] == True:
            self.checkmacdcut()

    def isclose(self):
        closetop, closebot = checkclose(self.goodeqs, self.highpoints, self.lowpoints)
        self.closebot = [int(i) for i in closebot]  # convert them to integers
        self.closetop = [int(i) for i in closetop]

    def gethammerlist(self):
        self.hammerlist = []  # so that if i call it again with diffrent vars its empty
        for i in range(self.checkdays, 0, -1):
            spotdata = [self.openpoints[-i], self.highpoints[-i], self.lowpoints[-i], self.closepoints[-i]]
            self.hammerlist.append(ishammer(spotdata))

    def geteaterlist(self):
        x = - self.checkdays - 1
        checklist = [self.openpoints[x:], self.highpoints[x:], self.lowpoints[x:],
                     self.closepoints[x:]]  # the first one isn't checked but is needed
        self.eaterlist = eater(checklist)
        self.eaterlist.pop(0)  # because first one wasn't even checked so we need only past checkdays days

    def isbetween(self):
        self.isbetweeneqs = []  # so that if i call it again with diffrent vars its empty
        # checks if last candle is between the eqs and saves the spot of the eqs it is between
        for i in range(len(self.topeqs)):
            x = len(self.closepoints) - 1
            if (yofx(self.boteqs[i], x) < self.closepoints[-1] < yofx(self.topeqs[i], x)) \
                    or (yofx(self.boteqs[i], x) < self.openpoints[-1] < yofx(self.topeqs[i], x)):
                self.isbetweeneqs.append(i)

    def checkupordown(self):  # checks if the trendline is an upslope or downslope (bull or bear)
        for i in range(len(self.topeqs)):  # maybe fix make dictionary
            if self.topeqs[i].slope > veryup:
                self.upordown.append('vup')
            elif self.topeqs[i].slope > bitup:
                self.upordown.append('bup')
            elif self.topeqs[i].slope < -veryup:
                self.upordown.append('vdown')
            elif self.topeqs[i].slope < -bitup:
                self.upordown.append('bdown')
            else:
                self.upordown.append('norm')

    def checkchk2(self):
        upchk2 = []
        downchk2 = []
        for i in range(len(self.upordown)):  # upchk2 look up def
            if i in self.isbetweeneqs:
                if self.upordown[i] == 'vup':
                    upchk2.append(i)
                if self.upordown[i] == 'vdown':
                    downchk2.append(i)
        if upchk2:
            self.checks['check2'] = True

    def checkmacdcut(self):
        chk3cut = []  # if macd is cut fully list of last 3 days sbuy/wbuy/ssell/wsell
        start = -3  # how many days before the end to check macd cuts and adx
        end = 0
        once = False
        for i in range(start, end):
            yes2dif = self.macd[i - 2] - self.emamacd[i - 2]
            yesdif = self.macd[i - 1] - self.emamacd[i - 1]
            nowdif = self.macd[i] - self.emamacd[i]
            if nowdif > 0 > yesdif:  # if its a cut up its buy
                if self.macd[i] > 0:  # if above 0 its strong
                    chk3cut.append('sbuy')
                elif self.macd[i] < 0:  # if under 0 its weak
                    chk3cut.append('wbuy')
            elif nowdif < 0 < yesdif:  # same just opposite
                if self.macd[i] < 0:
                    chk3cut.append('ssell')
                elif self.macd[i] > 0:
                    chk3cut.append('wsell')
            else:  # for the days its nothing in the 3 days
                chk3cut.append(0)
        for i in chk3cut:
            if i == 'sbuy' or i == 'wbuy':  # means it cut and make the check true
                self.checks['check3'] = True
                if i == 'sbuy':  # check if strong or weak
                    self.checks['check3info'] = 'macdb*'
                else:
                    self.checks['check3info'] = 'macdb'  # TODO add later when shorts
            """   
            if i == 'ssell' or i == 'wsell':    
                self.checks['check'] = True
                if i == 'ssell':
                    self.checks['check3info'] = 'macds*'
                else:
                    self.checks['check3info'] = 'macds'
            """
        return chk3cut

    def checkmacdclose(self):
        yes3dif = self.macd[-4] - self.emamacd[-4]
        yes2dif = self.macd[-3] - self.emamacd[-3]
        yesdif = self.macd[-2] - self.emamacd[-2]
        nowdif = self.macd[-1] - self.emamacd[-1]
        closefac = 2.5  # how much the now dif has to be than the yesdif

        # if past four days the macd has been getting closer and today it got close by at least 2.5 more than last time
        # its getting close so its almost like cut
        if abs(yes3dif) > abs(yes2dif) > abs(yesdif) > abs(nowdif) and abs(yesdif) / closefac > abs(nowdif):
            self.checks['check3'] = True
            if yesdif < 0:  # same as normal cut macd
                if self.macd[-1] > 0:
                    self.checks['check3info'] = 'pmacdb*'
                if self.macd[-1] < 0:
                    self.checks['check3info'] = 'pmacdb'
            if yesdif > 0:
                if self.macd[-1] < 0:
                    self.checks['check3info'] = 'pmacds*'
                if self.macd[-1] > 0:
                    self.checks['check3info'] = 'pmacds'

    def checkpdcuts(self):  # check cuts between +di and -di
        chk4cuts = []  # list of cuts of +di -di last 3 days
        start = -3  # how many days ago to check
        end = 0
        vstrong = 7  # how strong the slope at the cut is
        strong = 3.5
        for i in range(start, end):
            yesdif = self.plusdi[i - 1] - self.minusdi[i - 1]
            nowdif = self.plusdi[i] - self.minusdi[i]
            if yesdif < 0 < nowdif:  # if +di cut the -di upwards
                if self.plusdi[i] - self.plusdi[i - 1] > vstrong:
                    chk4cuts.append('adxb**')
                elif self.plusdi[i] - self.plusdi[i - 1] > strong:
                    chk4cuts.append('adxb*')
                else:
                    chk4cuts.append('adxb')
            elif yesdif > 0 > nowdif:
                if self.minusdi[i] - self.minusdi[i - 1] > vstrong:
                    chk4cuts.append('adxs**')
                elif self.minusdi[i] - self.minusdi[i - 1] > strong:
                    chk4cuts.append('adxs*')
                else:
                    chk4cuts.append('adxs')
            else:
                chk4cuts.append(0)

        for i in chk4cuts:  # checks if adx cut and says the info i only care about last cut
            if not i == 0:
                self.checks['check4'] = True
                self.checks['check4info'] = i

    def adxstren(self):  # check how strong the slope is by checking adx: > 25 strong. > 40 - vstrong.
        pass


def isstockgood(stockchk):
    # TODO need take dictionary of checks of stocks and decide how good is stock and if to add to list or file of
    #  good stocks TODO by which order. order: check the notes in class stock start
    bestbuy = []  # where there are trendlines that the last is close to bot. macd has cut is amazing then
    # eater then
    pass


def writetofile(stock):

    # TODO write to file stock ticker and info why its a good stock ex.
    # NFLX trendlines: 9 (7 up) (2 ok) closebot: 0,1,3 closetop: 4 hammer/eater: (date) macdcut: (date). adx good/bad +DI cut.

    pass

"""
def fourstepcheck(stockdata):  # chk1 - check if candle close to line 2 - check if slope is up
    chk1 = False  # 3 - check if macd is cutting 4 - adx good 5 - check if candles
    upchk2 = []  # list of eqs that are up and last candle is between the eqs
    downchk2 = []  # list of eqs that are down and last candle is between the eqs
    chk2 = False  # if upchk isnt empty its True
    chk3cut = []  # if macd is cut fully list of last 3 days sbuy/wbuy/ssell/wsell
    chk3close = False  # if macd is getting close to cutting only if its today
    chk4 = False
    chk5 = False

    # Get all data needed for checks.
    openpoints = stockdata[0]
    highpoints = stockdata[1]
    lowpoints = stockdata[2]
    closepoints = stockdata[3]

    changevars(0.1, 8, 4)  # changes global variables in trendline by your choice
    # (height from line(percentage of top - bot line), amount of candles to check for trendline, check for max points)
    goodeqs = getgoodeqs(stockdata)  # find the eqs that are trendline and parallel
    topeqs = list(goodeqs[0])  # split them into top and bot
    boteqs = list(goodeqs[1])

    # check if last candle is close to the trendline returns list of all stock trendlines that the last one is close to
    closetop, closebot = checkclose(goodeqs, highpoints, lowpoints)
    closebot = [int(i) for i in closebot]  # convert them to integers
    closetop = [int(i) for i in closetop]

    macdlist = findmacd(stockdata)  # get macd
    emamacd = findemaofmacd(macdlist, 9)
    for i in range(len(macdlist) - len(emamacd)):  # fix length macd
        macdlist.pop(0)

    plusdi, minusdi, adx = caladx(stockdata)  # get adx

    checkdays = 6  # amount of days to check if they're a hammer or eater

    hammerlist = []  # list of hammerdays strings to check if theyre a hammer ex: ['sred', 'no', 'ngreen'
    for i in range(checkdays, 0, -1):
        spotdata = [openpoints[-i], highpoints[-i], lowpoints[-i], closepoints[-i]]
        hammerlist.append(ishammer(spotdata))

    # check for eaters same amount of days as  hammers

    x = - checkdays - 1
    checklist = [openpoints[x:], highpoints[x:], lowpoints[x:],
                 closepoints[x:]]  # the first one isnt checked but is needed
    eaterlist = eater(checklist)
    eaterlist.pop(0)  # because first one wasnt even checked so we need only past 3 days

    isbetweeneqs = []  # checks if last candle is between the eqs and saves the spot of the eqs it is between
    for i in range(len(topeqs)):
        x = len(closepoints) - 1
        if (yofx(boteqs[i], x) < closepoints[-1] < yofx(topeqs[i], x)) \
                or (yofx(boteqs[i], x) < openpoints[-1] < yofx(topeqs[i], x)):
            isbetweeneqs.append(i)

    if closebot or closetop:
        chk1 = True

    upordown = []  # check if slope of eq is up or down - list the same size of eqs list that has up or down for each
    for i in range(len(topeqs)):  # maybe fix make dictionary
        if topeqs[i].slope > veryup:
            upordown.append('vup')
        elif topeqs[i].slope > bitup:
            upordown.append('bup')
        elif topeqs[i].slope < -veryup:
            upordown.append('vdown')
        elif topeqs[i].slope < -bitup:
            upordown.append('bdown')
        else:
            upordown.append('norm')

    for i in range(len(upordown)):  # upchk2 look up def
        if i in isbetweeneqs:
            if upordown[i] == 'vup':
                upchk2.append(i)
            if upordown[i] == 'vdown':
                downchk2.append(i)
    if upchk2:
        chk2 = True

    start = -3  # how many days before the end to check macd cuts and adx
    end = 0
    once = False
    for i in range(start, end):
        yes2dif = macdlist[i - 2] - emamacd[i - 2]
        yesdif = macdlist[i - 1] - emamacd[i - 1]
        nowdif = macdlist[i] - emamacd[i]
        if nowdif > 0 > yesdif:
            if macdlist[i] > 0:
                chk3cut.append('sbuy')
            if macdlist[i] < 0:
                chk3cut.append('')
"""


def yofx(eq, x):
    return x * eq.slope + eq.n


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
