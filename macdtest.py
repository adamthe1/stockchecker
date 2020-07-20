from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import numpy as np
import matplotlib.pyplot as plt
import csv
from datetime import datetime
from threading import Thread
import time
from tqdm import tqdm



stocklist = []
# targetfile = 'stocklist.csv'
targetfile = 'smp100.csv'
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


def main():
    choose = input('choose 1 for plotforone 2 for all')
    if choose == '1':
        plotforone()
    if choose == '2':
        findthem()


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

def plotforone():
    stockname = input('pls stock name quick boi: ')
    data = getdailydata(stockname)
    if data == 'bad':
        exit(1)
    choose = int(input('1 for ema 2 for macd: '))
    if choose == 2:
        pass
    elif choose == 1:
        plotforema(data)
        exit(0)

    macd = findmacd(data)
    sma = findsma(20, data)
    ema = findemaofmacd(macd, 9)

    # plt.axis(0, 40, -30, 30)
    macdplot = []
    for num in range(len(macd) - len(ema)):
        macd.pop(num)
    for some in range(len(macd) - 20, len(macd)):
        macdplot.append(macd[some])
    print(macd)
    print(ema)
    macdspot = np.array(range(len(macd)))
    emaspot = np.array(range(len(ema)))
    nicenice = []        # this is for the green and red lines at bottom its just macd - signal line its green
    xaxis = []           # if the current one is bigger than the last one then its green otherwise red
    for num in range(len(ema)):
        xaxis.append(0)
        nicenice.append(macd[num] - ema[num])
        xvalues = [num, num]
        yvalues = [0, nicenice[num]]
        if num > 0:
            if nicenice[num] > nicenice[num - 1]:
                plt.plot(xvalues, yvalues, color='green')
            else:
                plt.plot(xvalues, yvalues, color='red')    # till here
    plt.plot(emaspot, xaxis, color='black', linewidth=1)
    plt.plot(emaspot, ema, color='orange')
    plt.plot(macdspot, macd, color='blue')

    plt.show()

def plotforema(data):
    ema = findema(26, data)
    print(data[3])
    print(ema)


def findthem():
    global myfile
    global data
    firstspot = 0
    endspot = len(stocklist)
    myfile = open('macd100.csv', 'w')
    print(datetime.now())
    for spot in range(firstspot, endspot, 4):
        try:
                print(spot, end=",")
                t1 = Thread(target=first, args=(spot,))
                t2 = Thread(target=second, args=(spot + 1,))
                t3 = Thread(target=third, args=(spot + 2,))
                t4 = Thread(target=fourth, args=(spot + 3,))
                threads = [t1, t2, t3, t4]
                for x in threads:
                    x.start()
                for x in threads:
                    x.join()
                for j in range(len(threads)):
                    if j == 0:
                        try:
                            stockname = stocklist[spot]
                            if len(data.data1[3]) < 70:
                                continue
                            if data.data1 == 'bad':
                                continue
                            writetofile(stockname, data.data1)
                        except TypeError:
                            print("this stock didnt compute: " + str(stockname))
                            continue
                        except IndexError:
                            print("this stock didnt compute: " + str(stockname))
                            continue
                    if j == 1:
                        try:
                            stockname = stocklist[spot + j]
                            if len(data.data2[3]) < 70:
                                continue
                            if data.data2 == 'bad':
                                continue
                            writetofile(stockname, data.data2)
                        except TypeError:
                            print("this stock didnt compute: " + str(stockname))
                            continue
                        except IndexError:
                            print("this stock didnt compute: " + str(stockname))
                            continue
                    if j == 2:
                        try:
                            stockname = stocklist[spot + j]
                            if len(data.data3[3]) < 70:
                                continue
                            if data.data3 == 'bad':
                                continue
                            writetofile(stockname, data.data3)
                        except TypeError:
                            print("this stock didnt compute: " + str(stockname))
                            continue
                        except IndexError:
                            print("this stock didnt compute: " + str(stockname))
                            continue
                    if j == 3:
                        try:
                            stockname = stocklist[spot + j]
                            if len(data.data4[3]) < 70:
                                continue
                            if data.data4 == 'bad':
                                continue
                            writetofile(stockname, data.data4)
                        except TypeError:
                            print("this stock didnt compute: " + str(stockname))
                            continue
                        except IndexError:
                            print("this stock didnt compute: " + str(stockname))
                            continue
        except KeyboardInterrupt:
            print('ok then')
            exit(1)
    myfile.close()
    print(datetime.now())

def writetofile(stockname, stockdata):
    stockinfo = str(str(stockname) + ',')
    days = stockdata[4]
    macd = findmacd(stockdata)
    ema = findemaofmacd(macd, 9)
    for num in range(len(macd) - len(ema)):
        macd.pop(0)
    for num in range(len(days) - len(ema)):
        days.pop(0)
    passedfirst = False
    haddate = False
    for numb in range(len(macd) - 4, len(macd)):
        if not passedfirst:
            passedfirst = True
            continue
        nowdif = macd[numb] - ema[numb]
        yesdif = macd[numb - 1] - ema[numb - 1]
        if nowdif > 0 and yesdif < 0:
            if macd[numb] > 0 and ema[numb] > 0:
                stockinfo = stockinfo + str(datetime.fromtimestamp(int(days[numb]) / 1000))[:-9] + '(buy*),'
            else:
                stockinfo = stockinfo + str(datetime.fromtimestamp(int(days[numb]) / 1000))[:-9] + '(buy),'
            haddate = True
        if nowdif < 0 and yesdif > 0:
            if macd[numb] < 0 and ema[numb] < 0:
                stockinfo = stockinfo + str(datetime.fromtimestamp(int(days[numb]) / 1000))[:-9] + '(sell*),'
            else:
                stockinfo = stockinfo + str(datetime.fromtimestamp(int(days[numb]) / 1000))[:-9] + '(sell),'
            haddate = True
        if nowdif < 0 and yesdif > 0:
            pass
    if haddate:
        stockinfo = stockinfo[:-1]
        myfile.write(stockinfo)
        myfile.write('\n')




def findsma(smadays, data):
    closepoints = data[3]
    sumsma = 0
    sma = []
    for points in range(smadays, len(closepoints)):
        amount = 0
        for i in range(points - smadays, points):
            sumsma += float(closepoints[i])
            amount += 1
        sma.append(sumsma/amount)
    return sma


def findema(emadays, data):
    sma = findsma(emadays, data)
    closepoints = data[3]
    ema = []
    smoothing = 2
    for points in range(emadays, len(closepoints)):
        if not ema:
            ematoday = (closepoints[points] * (smoothing/(1 + emadays))) + sma[points - emadays] * (1 - (smoothing/(1 + emadays)))
            ema.append(ematoday)
        else:
            ematoday = (closepoints[points] * (smoothing/(1 + emadays))) + \
                       ema[points - emadays - 1] * (1 - (smoothing/(1 + emadays)))
            ema.append(ematoday)
    return ema


def findmacd(thisdata):
    closepoints = thisdata[3]
    macd = []
    for i in range(len(closepoints) - 25):
        macd.append(findemaformacd(12, thisdata)[i] - findemaformacd(26, thisdata)[i])
    return macd


def findsmaofmacd(macd, smadays):      # of macd
    sumsma = 0
    sma = []
    for points in range(smadays, smadays + 1):
        amount = 0
        for i in range(points - smadays, points):
            sumsma += float(macd[i])
            amount += 1
        sma.append(sumsma / amount)
    return sma


def findemaofmacd(macd, emadays):     # of macd
    sma = findsmaofmacd(macd, emadays)
    ema = []
    smoothing = 2
    for points in range(emadays, len(macd)):
        if not ema:
            ematoday = (macd[points] * (smoothing/(1+emadays))) + \
                       sma[points - emadays] * (1 - (smoothing/(1+emadays)))
            ema.append(ematoday)
        else:
            ematoday = (macd[points] * (smoothing/(1+emadays))) + \
                       ema[points - emadays - 1] * (1 - (smoothing/(1+emadays)))
            ema.append(ematoday)
    return ema


def findsmaformacd(smadays, stockdata):       # for macd
    closepoints = stockdata[3]
    sumsma = 0
    sma = []
    for points in range(26, len(closepoints)):
        amount = 0
        for i in range(points - smadays, points):
            sumsma += float(closepoints[i])
            amount += 1
        sma.append(sumsma/amount)
    return sma


def findemaformacd(emadays, stockdata):       # for macd
    sma = findsmaformacd(emadays, stockdata)
    closepoints = stockdata[3]
    ema = []
    smoothing = 2
    for points in range(25, len(closepoints)):
        if not ema:
            ematoday = (closepoints[points] * (smoothing/(1+emadays))) + sma[0] * (1 - (smoothing/(1+emadays)))
            ema.append(ematoday)
        else:
            ematoday = (closepoints[points] * (smoothing/(1+emadays)))\
                       + ema[points - 26] * (1 - (smoothing/(1+emadays)))
            ema.append(ematoday)
    return ema


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
