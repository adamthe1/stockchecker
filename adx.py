from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import numpy as np
import matplotlib.pyplot as plt
import csv
from datetime import datetime
from threading import Thread

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

    choose = input('for stock plot 1, for all stocks good 2, 3 for testing: ')
    if int(choose) == 1:
        stockplot()
    if int(choose) == 2:
        allstocks()
    if int(choose) == 3:
        stockname = input('i need a name: ')
        stockinfo = getdailydata(stockname)
        x = caladx(stockinfo)
        for i in x:
            print(len(i))
        # print(ema(stockinfo[3]))

def stockplot():
    stockname = input('i need a name: ')
    stockinfo = getdailydata(stockname)
    if data == 'bad':
        exit(1)
    dip, dim, adxlist = caladx(stockinfo)


    for i in range(len(dip) - len(adxlist)):
        dip.pop(0)
        dim.pop(0)
    dispot = np.array(range(len(dip)))

    lines = []
    xaxis = []

    plt.plot(dispot, dip, color='green')
    plt.plot(dispot, dim, color='red')
    plt.plot(dispot, adxlist, color='black')

    plt.show()

def allstocks():
    start = 0
    end = 5000
    for spot in range(start, end):
        threader(spot)
        for i in range(5):
            if i == 0:
                if data.data1 == 'bad':
                    print('this stock aint it: ' + str(stock))
                    continue





def writetofile(name, stockinfo):
    linetofile = str(name) + ','
    dip, dim, adx = caladx(stockinfo)
    for i in range(len(dip) - len(adx)):
        dip.pop(0)
        dim.pop(0)



period = 14


def caladx(stockprices):  # calculate adx and dip and dim
    opens = stockprices[0]
    high = stockprices[1]
    low = stockprices[2]
    close = stockprices[3]
    dmpluslist = []
    dmminuslist =[]
    trlist = []
    for spot in range(len(opens)):
        # for the dm+ and dm-
        if spot == 0:
            continue
        upmove = high[spot] - high[spot - 1]
        downmove = low[spot - 1] - low[spot]
        dmplus = 0
        dmminus = 0
        if upmove > downmove and upmove > 0:
            dmplus = upmove
        if downmove > upmove and downmove > 0:
            dmminus = downmove
        dmpluslist.append(dmplus)
        dmminuslist.append(dmminus)

        # for the atr
        tr = max(high[spot]-low[spot], abs(high[spot] - close[spot - 1]), abs(low[spot] - close[spot - 1]))
        trlist.append(tr)

    # calculate atr they should all be same len

    atrlist = atr(trlist)

     # smooth them

    smmadmplus = smma(dmpluslist)
    smmadmminus = smma(dmminuslist)

    if len(smmadmminus) != len(smmadmplus):
        print('lengths of the dms not the same ' + stockprices[5])
        exit(-1)

    if len(smmadmplus) != len(atrlist):
       print('lengths of smmaplus and atr not the same ' + stockprices[5])
       exit(-1)

    # make two new lists that have dmplus smoothed / atr and dmminus smoothed/ atr
    atrdmplus = []
    atrdmminus = []

    for i in range(len(atrlist)):
        atrdmplus.append(smmadmplus[i] / atrlist[i])
        atrdmminus.append(smmadmminus[i] / atrlist[i])


    # calculate the +di and -di


    plusdilist = []
    minusdilist = []

    for spot in range(len(atrdmplus)):
        plusdilist.append(100 * atrdmplus[spot])  # equation for plus and minus di
        minusdilist.append(100 * atrdmminus[spot])

    # adx

    adxlist = []
    special = []   # calculate the "slope" of dis

    for i in range(len(plusdilist)):
        special.append(abs((plusdilist[i] - minusdilist[i]) / (plusdilist[i] + minusdilist[i])))
    smspecial = smma(special)   # smooth it

    # calculate adx
    for i in range(len(smspecial)):
        adxlist.append(100 * smspecial[i])

    return(plusdilist, minusdilist, adxlist)



def smma(list):  # smoothed moving average
    avglist = []    # calculate sma of first 14 days
    didsma = False
    smmalist = []
    for spot, item in enumerate(list):
        if spot < period:
            avglist.append(item)
            continue
        if not didsma:
            smaperiod = sum(avglist)/len(avglist)
            smma = ((period - 1) * smaperiod + item) / period
            smmalist.append(smma)
            didsma = True
        else:
            smma = ((period - 1) * smmalist[-1] + item) / period
            smmalist.append(smma)
    # print(smmalist)
    return smmalist


def ema(list):
    avglist = []  # calculate sma of first 14 days
    didsma = False
    emalist = []
    smoothing = 2
    for spot, item in enumerate(list):
        if spot < period - 1:
            avglist.append(item)
            continue
        if not didsma:
            print(len(avglist))
            smaperiod = sum(avglist) / len(avglist)
            ema = (item * (smoothing / (1 + period))) + smaperiod * (1 - (smoothing / (1 + period)))
            emalist.append(ema)
            didsma = True
        else:
            ema = (item * (smoothing / (1 + period))) + emalist[-1] * (1 - (smoothing / (1 + period)))
            emalist.append(ema)
    # print(smmalist)
    # print(emalist)
    return emalist

def atr(list):
    atrlist = []
    didfirst = False
    for spot, item in enumerate(list):
        if spot < period:
            continue
        if not didfirst:
            atr = (list[spot - 1] * (period - 1) + item)/period
            atrlist.append(atr)
            didfirst = True
        else:
            atr = (atrlist[-1] * (period - 1) + item)/period
            atrlist.append(atr)
    # print(atrlist)
    return atrlist






def findsma(smadays, stockdata):
    points = stockdata
    sumsma = 0
    sma = []
    for point in range(smadays, len(points)):
        amount = 0
        for i in range(point - smadays, point):
            sumsma += float(points[i])
            amount += 1
        sma.append(sumsma/amount)
    return sma










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
    except TypeError:
        print("this stock didnt compute: ")
    except IndexError:
        print("this stock didnt compute: ")



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
