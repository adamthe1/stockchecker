

from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import numpy as np
import matplotlib.pyplot as plt
import csv
from threading import Thread
from trendline import getgoodeqs, changevars, checkclose, height
from macddone import findmacd, findemaofmacd
from adx import caladx
from findhammers import ishammer
from eater import eater
from time import time


class Data4stocks():
    def __init__(self):
        data1 = []
        data2 = []
        data3 = []
        data4 = []
        data5 = []
        data6 = []
        data7 = []
        data8 = []


data = Data4stocks()  # class to thread 5 stock datas together
def gettickerlist(choice):
    if choice == 0:
        stocklist = []
        targetlist = 'smp100.csv'
        with open(targetlist, 'r') as stocks:
            stockreader = csv.reader(stocks, delimiter='\n')
            for row in stockreader:
                stocklist.append(row[0])
    elif choice == 1:
        stocklist = []
        targetlist = 'nasdaq.csv'
        with open(targetlist, 'r') as stocks:
            stockreader = csv.reader(stocks, delimiter='\n')
            for row in stockreader:
                stocklist.append(row[0])
    elif choice == 2:
        stocklist = []
        targetlist = 'amex.csv'
        with open(targetlist, 'r') as stocks:
            stockreader = csv.reader(stocks, delimiter='\n')
            for row in stockreader:
                stocklist.append(row[0])
    elif choice == 3:
        stocklist = []
        targetlist = 'nyse.csv'
        with open(targetlist, 'r') as stocks:
            stockreader = csv.reader(stocks, delimiter='\n')
            for row in stockreader:
                stocklist.append(row[0])
    elif choice == 4:
        stocklist = []
        targetlist = 'stocklist.csv'
        with open(targetlist, 'r') as stocks:
            stockreader = csv.reader(stocks, delimiter='\n')
            for row in stockreader:
                stocklist.append(row[0])
    elif choice == 5:
        stocklist = []
        targetlist = 'goodvolume.csv'
        with open(targetlist, 'r') as stocks:
            stockreader = csv.reader(stocks, delimiter='\n')
            for row in stockreader:
                stocklist.append(row[0])
    print(stocklist)
    return stocklist


def main():
    choose = input('for stock plot 1, for 4 step check stocks good 2: ')
    firsttime = time()
    if int(choose) == 1:
        stockplot()
    if int(choose) == 2:
        scoredict = {}  # dictionary where the key is the ticker of the stock and the value will be the score of the
        # stock and the check dictionary of the stock
        changevars(0.1, 8, 4, 100)
        sumofgoods = 0
        marketchoose = 6
        while not 6 > marketchoose > -1:
            marketchoose = int(input('for smp100 press 0 for nasdaq press 1 for amex press 2 for nyse press 3\n '
                                     'for all press 4, for volume over 800000 press 5: '))
        stocklist = gettickerlist(marketchoose)
        for spot in range(0, len(stocklist), 8):
            if spot - 50 > 0:
                print(str((spot / len(stocklist)) * 100) + '%')
            print(stocklist[spot:spot + 8])
            if len(stocklist) - spot > 8 and len(stocklist) - spot != 0:
                ts = threader(spot, stocklist)  #returns how many threads there are
                for t in range(ts):
                    if len(stocklist) < spot + t:
                        break
                    if t == 0:
                        stockdata = data.data1
                    elif t == 1:
                        stockdata = data.data2
                    elif t == 2:
                        stockdata = data.data3
                    elif t == 3:
                        stockdata = data.data4
                    elif t == 4:
                        stockdata = data.data5
                    elif t == 5:
                        stockdata = data.data6
                    elif t == 6:
                        stockdata = data.data7
                    elif t == 7:
                        stockdata = data.data8
                    if stockdata == 'bad':
                        print('bad')
                        continue
                    """
                    if stockdata[6][-1] < 1000000:
                        print('not enough volume')
                        continue
                    if len(stockdata[0]) < 82:
                        print('not enough data')
                        continue
                    """


                    try:
                        stock1 = Stock(stockdata)
                    except TypeError:
                        print('type error')
                        continue
                    except ZeroDivisionError:
                        print('zero division error')
                        continue

                    score = isstockgood(stock1)
                    scoredict[stocklist[spot + t]] = {'score': score, 'info': stock1.checks}
            else:
                for i in range(spot, len(stocklist)):
                    stockdata = getdailydata(stocklist[i])
                    if stockdata == 'bad':
                        print('bad')
                        continue
                    """
                    if stockdata[6][-1] < 1000000:
                        print('not enough volume')
                        continue
                    if len(stockdata[0]) < 82:
                        print('not enough data')
                        continue
                    """
                    try:
                        stock1 = Stock(stockdata)
                    except TypeError:
                        print('type error')
                        continue
                    except ZeroDivisionError:
                        print('zero division error')
                        continue
                    score = isstockgood(stock1)
                    scoredict[stocklist[i]] = {'score': score, 'info': stock1.checks}
        sorteddict = {k: v for k, v in sorted(scoredict.items(), key=lambda item: item[1]['score'], reverse=True)}

            #for keys, values in sorteddict.items():
             #   print(keys)
              #  print(values)
        writetofile(sorteddict, marketchoose)
    lasttime = time()
    print(lasttime - firsttime)



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


def threader(spot, stocklist):
    check = 0
    try:
        t1 = Thread(target=first, args=(stocklist[spot],))
        t2 = Thread(target=second, args=(stocklist[spot + 1],))
        t3 = Thread(target=third, args=(stocklist[spot + 2],))
        t4 = Thread(target=fourth, args=(stocklist[spot + 3],))
        t5 = Thread(target=fifth, args=(stocklist[spot + 4],))
        t6 = Thread(target=sixth, args=(stocklist[spot + 5],))
        t7 = Thread(target=seventh, args=(stocklist[spot + 6],))
        t8 = Thread(target=eight, args=(stocklist[spot + 7],))
        threads = [t1, t2, t3, t4, t5, t6, t7, t8]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print('we out boys')
        exit(-1)
    return len(threads)


class Stock:
    def __init__(self, stockdata):

        self.stockdata = stockdata

        # get all data needed from stockdata
        self.openpoints = stockdata[0]
        self.highpoints = stockdata[1]
        self.lowpoints = stockdata[2]
        self.closepoints = stockdata[3]

        self.checks = {}  # dictionary of all the checks
        # chk1 - check if candle close to line 2 - check if slope is up
        # 3 - check if macd is cutting or close 4 - adx good 5 - if +di and -di cuts  6 - candles
        # for check 4 - checks if good trend (more than 25)
        # 3, 4, 5, 6 have info

        time = -100  # how long ago for trendlines to check 82 is 4 months
        if len(self.openpoints) < -time:
            time = -len(self.openpoints)
        stockforlines = [self.openpoints[time:], self.highpoints[time:], self.lowpoints[time:],
                         self.closepoints[time:], self.stockdata[4][time:], self.stockdata[5], self.stockdata[6][time:]]
        self.goodeqs = getgoodeqs(stockforlines)  # find the eqs that are trendline and parallel
        self.topeqs = list(self.goodeqs[0])  # split them into top and bot
        self.boteqs = list(self.goodeqs[1])

        # check if last candle is close to the trendline returns list of all stock trendlines
        # that the last one is close to
        self.closetop, self.closebot = checkclose(self.goodeqs, self.highpoints[time:], self.lowpoints[time:],
                                                  self.closepoints[time:])   #TODO fix
        # self.closebot = [int(i) for i in self.closebot]  # convert them to integers
        # self.closetop = [int(i) for i in self.closetop]

        self.macd = findmacd(stockdata)  # get macd
        self.emamacd = findemaofmacd(self.macd, 9)
        for i in range(len(self.macd) - len(self.emamacd)):  # fix length macd
            self.macd.pop(0)

        self.plusdi, self.minusdi, self.adx = caladx(stockdata)  # get adx

        self.checkdays = 4
        self.hammerlist = []
        self.gethammerlist()  # get hammers
        for i, item in enumerate(reversed(self.hammerlist)):
            if item != 'no':
                self.checks['check6'] = -i - 1  # i care only about the most recent one and its how long ago it was
                self.checks['check6info'] = item
                break

        self.eaterlist = None
        self.geteaterlist()  # get eater
        for i, item in enumerate(reversed(self.eaterlist)):  # i care more about eaters then hammers
            if item != 'no':
                self.checks['check6'] = -i - 1  # i care only about the most recent one and its how long ago it was
                self.checks['check6info'] = item
                break
        if 'check6' not in self.checks.keys():
            self.checks['check6'] = False

        self.isbetweeneqs = []  # check eqs the last one is between
        self.isbetween()

        if self.closebot or self.closetop:
            self.checks['check1'] = (self.closetop, self.closebot)
            if self.closebot and self.closetop:
                self.checks['check1info'] = 'dual'
            elif self.closetop:
                self.checks['check1info'] = 'top'
            else:
                self.checks['check1info'] = 'bot'
        else:
            self.checks['check1'] = False

        self.bitup = self.closepoints[-1] * 0.002  # amount the slope has #TODO
        # to be above to be very up or a bit up for down its the same just minus
        self.veryup = self.closepoints[-1] * 0.007  # if go up by 0.8% every day
        self.upordown = []  # check if slope of eq is up or down -
        # list the same size of eqs list that has up or down for each
        # when do checks just see if up or down for the if
        self.checkupordown()
        self.checkchk2()

        self.macdcuts = self.checkmacdcut()
        if not self.checks['check3']:
            self.predictmacdclose()

        self.dicross = self.checkpdcuts()  # list of past checkdays to see if the pdi and mdi crossed
        self.adxstren()

    #def isclose(self):
        tdays = 15
        self.great = (sum(self.closepoints[-tdays:]) / tdays) * 0.01  # greatslope is when it goes up everyday 1 percent of the
        # price
        self.good = (sum(self.closepoints[-tdays:]) / tdays) * 0.006  # goodslope is when it goes up 0.6 % of the price



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
            if self.topeqs[i].slope > self.veryup:
                self.upordown.append('vup')
            elif self.topeqs[i].slope > self.bitup:
                self.upordown.append('bup')
            elif self.topeqs[i].slope < -self.veryup:
                self.upordown.append('vdown')
            elif self.topeqs[i].slope < -self.bitup:
                self.upordown.append('bdown')
            else:
                self.upordown.append('norm')

    def checkchk2(self):
        upchk2 = []
        downchk2 = []
        for i in range(len(self.upordown)):  # upchk2 look up def
            if i in self.isbetweeneqs:
                if self.upordown[i] == 'vup' or self.upordown[i] == 'bup':
                    upchk2.append(i)
                if self.upordown[i] == 'vdown':
                    downchk2.append(i)
        if upchk2:
            self.checks['check2'] = True
        else:
            self.checks['check2'] = False

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
                day = i
                if self.macd[i] > 0:  # if above 0 its strong
                    chk3cut.append('sbuy')
                elif self.macd[i] < 0:  # if under 0 its weak
                    chk3cut.append('wbuy')
            elif nowdif < 0 < yesdif:  # same just opposite
                day = 1
                if self.macd[i] < 0:
                    chk3cut.append('ssell')
                elif self.macd[i] > 0:
                    chk3cut.append('wsell')
            else:  # for the days its nothing in the 3 days
                chk3cut.append(0)
        for i in chk3cut:
            if i == 'sbuy' or i == 'wbuy':  # means it cut and make the check true
                self.checks['check3'] = day
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
        if not 'check3' in self.checks.keys():
            self.checks['check3'] = False
        return chk3cut

    def predictmacdclose(self):
        yes3dif = self.macd[-4] - self.emamacd[-4]
        yes2dif = self.macd[-3] - self.emamacd[-3]
        yesdif = self.macd[-2] - self.emamacd[-2]
        nowdif = self.macd[-1] - self.emamacd[-1]
        closefac = 2.5  # how much the now dif has to be than the yesdif

        # if past four days the macd has been getting closer and today it got close by at least 2.5 more than last time
        # its getting close so its almost like cut
        if abs(yes3dif) > abs(yes2dif) > abs(yesdif) > abs(nowdif) and abs(yesdif) / closefac > abs(nowdif):
            self.checks['check3'] = 0
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
                    chk4cuts.append('dip**')
                elif self.plusdi[i] - self.plusdi[i - 1] > strong:
                    chk4cuts.append('dip*')
                else:
                    chk4cuts.append('dip')
            elif yesdif > 0 > nowdif:
                if self.minusdi[i] - self.minusdi[i - 1] > vstrong:
                    chk4cuts.append('dim**')
                elif self.minusdi[i] - self.minusdi[i - 1] > strong:
                    chk4cuts.append('dim*')
                else:
                    chk4cuts.append('dim')
            else:
                chk4cuts.append(0)
        for i in chk4cuts:  # checks if adx cut and says the info i only care about last cut
            if not i == 0:
                self.checks['check5'] = True
                self.checks['check5info'] = i
        if not 'check5' in self.checks.keys():
            self.checks['check5'] = False
        return chk4cuts

    def adxstren(self):  # check how strong the slope is by checking adx: > 25 strong. > 40 - vstrong.
        days = 15
        start = len(self.closepoints) - days  # the days is how many days back to check the regression for strength adx
        end = len(self.closepoints)
        greatslope = (sum(self.closepoints[-days:]) / days) * 0.01  # greatslope is when it goes up everyday 1 percent of the
        # price

        goodslope = (sum(self.closepoints[-days:]) / days) * 0.006  # goodslope is when it goes up 0.6 % of the price

        slopedays = regression(np.array(range(start, end)), self.closepoints[-days:])  # gives me the slope and n of
        # past days as [0] = slope [1] = n
        strong = 25
        vstrong = 40
        toostrong = 60
        absslope = abs(slopedays[0])  # doesn't matter if the slope os up or down its the same principal
        self.checks['check4'] = False
        if self.adx[-1] > toostrong and absslope > greatslope:
            self.checks['check4s'] = True  # this is an extra check that the adx signals that the price is too strong
            # of an up and might go down
        elif self.adx[-1] > vstrong:
            if absslope > greatslope:
                self.checks['check4'] = True
                self.checks['check4info'] = 'adxs*'  # adx strong, * is that slope is strong
            elif absslope > goodslope:
                self.checks['check4'] = True
                self.checks['check4info'] = 'adxs'  # adx strong, slope ok
        elif self.adx[-1] > strong:
            if absslope > greatslope:
                self.checks['check4'] = True
                self.checks['check4info'] = 'adxw*'  # adx weak but still good, * slope strong
            elif absslope > goodslope:
                self.checks['check4'] = True
                self.checks['check4info'] = 'adxw'  # adx weak, slope ok


def isstockgood(stockchk):
    # TODO need take dictionary of checks of stocks and decide how good is stock and if to add to list or file of
    #  good stocks TODO by which order. order: check the notes in class stock start
    bestbuy = []  # where there are trendlines that the last is close to bot. macd has cut is amazing then
    # adx, 2 kind adx the +di is very up is good and if trendline slope is up the adx is over 30 is very good
    # the eater and hammer but only if its close to bot or top
    # eater then hammer

    # first check if theres a trendline and how close
    score = 0  # score of stock close to line = 3 (check1) macd* = 2 macd = 1.5 (check 3)
    # dip** = 1.6 dip* = 1.2 dip = 1  (check5)
    #  eater strong if today = 0.7 weak 0.65. not today strong 0.5 weak 0.45.
    #  hammer today = 0.4 not today 0.3

    # now all the checks for an long (buy)
    if stockchk.checks['check1']:
        if stockchk.checks['check1info'] == 'dual' or stockchk.checks['check1info'] == 'bot':
                score += 4
    if stockchk.checks['check3']:
        if stockchk.checks['check3info'][-1] == '*':
            if stockchk.checks['check3info'][-2] == 'b':
                score += 2
        elif stockchk.checks['check3info'][-1] == 'b':
            score += 1.5
    if stockchk.checks['check5']:
        if stockchk.checks['check5info'][-3:] == 'p**':
            score += 1.6
        elif stockchk.checks['check5info'][-2:] == 'p*':
            score += 1.2
        elif stockchk.checks['check5info'][-1] == 'p':
            score += 1

    if stockchk.checks['check6'] == -1:
        if stockchk.checks['check6info'][0:2] == 'es':
            score += 0.7
        elif stockchk.checks['check6info'][0:2] == 'ew':
            score += 0.6
        elif stockchk.checks['check6info'][0:2] == 'hs' or stockchk.checks['check6info'][0:3] == 'hw':
            score += 0.4

    elif stockchk.checks['check6'] != False:
        if stockchk.checks['check6info'][0:2] == 'es':
            score += 0.5
        elif stockchk.checks['check6info'][0:2] == 'ew':
            score += 0.45
        elif stockchk.checks['check6info'][0:2] == 'hs' or stockchk.checks['check6info'][0:3] == 'hw':
            score += 0.3

    if 'check4s' in stockchk.checks.keys():
        score += 1.3
    if stockchk.checks['check4']:
        if stockchk.isbetweeneqs:
            for eqspot in stockchk.isbetweeneqs:
                if stockchk.topeqs[eqspot].slope > stockchk.great:
                    score += 2

    return score










def writetofile(stockdict, choice):   # gets a sorted dictionary of the tickers and their scores
    # TODO write to file stock ticker and info why its a good stock ex.
    # NFLX trendlines: 9 (7 up) (2 ok) closebot: 0,1,3 closetop: 4 hammer/eater: (date) macdcut: (date).
    # adx good/bad +DI cut.
    numofchecks = 6
    tickers = stockdict.keys()
    if choice != 5:
        file = open('longtest.txt', 'w')
    else:
        file = open('volumestocks.txt', 'w')
    for spot, tick in enumerate(tickers):
        # print(tick, spot)
        title = f'{spot}: {tick} score = {str(stockdict[tick]["score"])}\n'
        info = ['info: ']
        checks = stockdict[tick]['info']
        once = True
        for i in range(1, numofchecks + 1):
            value = stockdict[tick]['info'][f'check{i}']
            if value:
                info.append(f'{str(i)}: was {value} days ago')
                if i != 2:
                    valueinfo = stockdict[tick]['info'][f'check{i}info']
                    info.append(f'what: {str(valueinfo)}')
                info.append('|')
            if len(info) / 6 >= 1:
                if once:
                    info.append('\n')
                    info.append(' ' * (len(info[0]) - 2))
                    once = False
        info.append('\n\n')
        infostr = '  '.join(info)
        file.write(str(title) + str(infostr))




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





def first(stock):
    global data
    data.data1 = getdailydata(stock)


def second(stock):
    global data
    data.data2 = getdailydata(stock)


def third(stock):
    global data
    data.data3 = getdailydata(stock)


def fourth(stock):
    global data
    data.data4 = getdailydata(stock)


def fifth(stock):
    global data
    data.data5 = getdailydata(stock)


def sixth(stock):
    global data
    data.data6 = getdailydata(stock)


def seventh(stock):
    global data
    data.data7 = getdailydata(stock)


def eight(stock):
    global data
    data.data8 = getdailydata(stock)


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
