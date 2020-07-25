from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas


stocklist = []
with open('stocklist.csv', 'r') as stocks:
    stockreader = csv.reader(stocks, delimiter='\n')
    for row in stockreader:
        stocklist.append(row[0])


def main():
    choose = int(input('1 for getforone 2 for getall: '))
    if choose == 1:
        getforone()
    if choose == 2:
        getall()


def getforone():
    stockname = input('pls stock name quick boi: ')
    data = getdailydata(stockname)
    openpoints = data[0]
    highpoints = data[1]
    lowpoints = data[2]
    closepoints = data[3]
    days = data[4]
    name = data[5]
    volumes = data[6]
    alltogether = [openpoints, highpoints, lowpoints, closepoints, volumes]
    plotshow(alltogether)  # for candles
    eaterlist = eater(data)
    xvalues1eaters = []
    yvalues1eaters = []
    xvalues2eaters = []
    yvalues2eaters = []
    for spot in range(len(eaterlist)):
        if eaterlist[spot] == 'sred' or eaterlist[spot] == 'sgreen':
            xvalues2eaters.append(spot)
            yvalues2eaters.append(float(highpoints[spot]) + 10)
        if eaterlist[spot] == 'wred' or eaterlist[spot] == 'wgreen':
            xvalues1eaters.append(spot)
            yvalues1eaters.append(float(highpoints[spot]) + 10)
    plt.scatter(xvalues1eaters, yvalues1eaters, color='yellow', s=5)
    plt.scatter(xvalues2eaters, yvalues2eaters, color='red', s=10)
    plt.show()


def getall():
    myfile = open('goodstockseater.csv', 'w')
    for stockname in stocklist:
        data = getdailydata(stockname)
        if data == 'bad':
            continue
        days = data[4]
        eaterlist = eater(data)
        stockinfo = str(str(stockname) + ',' + str(eaterlist[len(eaterlist) - 1]) + ',')
        hadeater = False
        for num in range(len(eaterlist) - 20, len(eaterlist)):
            if 0 < eaterlist[num] < 3:
                stockinfo = stockinfo + days[num] + ','
                hadeater = True
        if hadeater:
            stockinfo = stockinfo[:-1]
            myfile.write(stockinfo)
            myfile.write('\n')
    myfile.close()


def eater(data):    # send back list where each spot tells you if strong eater or normal eater or not
    openlist = data[0]    # if spot is 0:not eater, 1:normal, 2: strong
    highlist = data[1]
    lowlist = data[2]
    closelist = data[3]
    eaterlist = ['no']   # starts with a 0 because you cant check the first day but you have to have it in the list
    for i in range(len(openlist)):
        if i == 0:
            continue
        iseater = 'no'
        if openlist[i] > closelist[i]:
            if openlist[i - 1] < closelist[i - 1]:
                if openlist[i] > highlist[i -1] and closelist[i] < lowlist[i - 1]:
                    iseater = 'sred'
                elif openlist[i] > closelist[i - 1] and closelist[i] < openlist[i - 1]:
                    iseater = 'wred'
        else:
            if openlist[i - 1] > closelist[i - 1]:
                if closelist[i] > highlist[i - 1] and openlist[i] < lowlist[i - 1]:
                    iseater = 'sgreen'
                elif closelist[i] > openlist[i - 1] and openlist[i] < closelist[i - 1]:
                    iseater = 'wgreen'
        eaterlist.append(iseater)


    return eaterlist


def plotshow(them):
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
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_MONTH, 12, share.FREQUENCY_TYPE_DAY, 1)
    except YahooFinanceError as e:
        print(e.message)
        return 'bad'
    # print(len(symbol_data['open']))
    return (symbol_data['open'], symbol_data['high'], symbol_data['low'],
            symbol_data['close'], symbol_data['timestamp'], name, symbol_data['volume'])


if __name__ == '__main__':
    main()