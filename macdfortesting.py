from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import numpy as np
import matplotlib.pyplot as plt
import csv
from datetime import datetime

stocklist = []
targetfile = 'stocklist.csv'
# targetfile = 'smp100.csv'
with open(targetfile, 'r') as stocks:
    stockreader = csv.reader(stocks, delimiter='\n')
    for row in stockreader:
        stocklist.append(row[0])



def main():
    choose = input('choose 1 for plotforone 2 for all')
    if choose == '1':
        plotforone()
    if choose == '2':
        findthem()


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
    # print(macd)
    # print(ema)
    macdspot = np.array(range(len(macd)))
    emaspot = np.array(range(len(ema)))
    nicenice = []
    xaxis = []
    xvaluestest = []
    yvaluestest = []
    print(len(ema))
    for num in range(len(ema)):
        xaxis.append(0)
        nicenice.append(macd[num] - ema[num])
        xvalues = [num, num]
        yvalues = [0, nicenice[num]]
        if num > 0:
            if nicenice[num] > nicenice[num - 1]:
                plt.plot(xvalues, yvalues, color='green')
            else:
                plt.plot(xvalues, yvalues, color='red')
        if num < 3:
            continue

        chk3close = False
        yes3dif = macd[num - 3] - ema[num - 3]
        yes2dif = macd[num - 2] - ema[num - 2]
        yesdif = macd[num - 1] - ema[num - 1]
        nowdif = macd[num] - ema[num]
        closefac = 2.5  # how much the now dif has to be than the yesdif

        # if past four days the macd has been getting closer and today it got close by at least 2.5 more than last time
        # its getting close so its almost like cut
        if abs(yes3dif) > abs(yes2dif) > abs(yesdif) > abs(nowdif) and abs(yesdif) / closefac > abs(nowdif):
            xvaluestest.append(num)
            yvaluestest.append(macd[num] + 0.5)

    print(xvaluestest)
    print(yvaluestest)
    plt.scatter(xvaluestest, yvaluestest, color='cyan', s=5)

    plt.plot(emaspot, xaxis, color='black', linewidth=1)
    plt.plot(emaspot, ema, color='orange')
    plt.plot(macdspot, macd, color='blue')

    plt.show()

def plotforema(data):
    ema = findema(26, data)
    print(data[3])
    print(ema)


def findthem():
    myfile = open('macd100.csv', 'w')
    first = 2800
    end = 3000
    print(datetime.now())
    for spot in range(first, end):
        if (spot - 100) % 10 == 0:
            print(spot, end=", ")
        stockname = stocklist[spot]
        stockdata = getdailydata(stockname)
        stockinfo = str(str(stockname) + ',')
        if stockdata == 'bad':
            continue
        try:
            if len(stockdata[3]) < 70:
                continue
            days = stockdata[4]
            macd = findmacd(stockdata)
            ema = findemaofmacd(macd, 9)
        except TypeError:
            print("this stock didnt compute: " + str(stockname))
            continue
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
    myfile.close()
    print(datetime.now())


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
        return (symbol_data['open'], symbol_data['high'], symbol_data['low'],
                symbol_data['close'], symbol_data['timestamp'], name, symbol_data['volume'])
    except TypeError:
        print(" non subscriptable: " + str(name), end=' ')
        return 'bad'


if __name__ == '__main__':
    main()
