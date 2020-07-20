import csv
import math as mt
from numpy import mean
import numpy as np
import matplotlib.pyplot as plt
import sys
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
from datetime import datetime
import pandas


stocklist = []
 # targetfile = 'stocklist.csv'
targetfile = 'smp100.csv'
with open(targetfile, 'r') as stocks:
    stockreader = csv.reader(stocks, delimiter='\n')
    for row in stockreader:
        stocklist.append(row[0])


class Eq:
    def __init__(self, slope, n):
        self.slope = slope
        self.n = n
        self.nums = None

    # TODO implement into the function constructor
    """
    def findeq(xpoints, ypoints):  # eq is eq[0] = slope  eq[1] = n
        x1 = float(xpoints[0])
        x2 = float(xpoints[1])
        y1 = float(ypoints[0])
        y2 = float(ypoints[1])
        m = (y2 - y1) / (x2 - x1)
        n = y1 - m * x1
        return m, n
    """


def main():
    choose = input('for stocks with line press 1 for stock plot press 2: ')
    if int(choose) == 2:
        stock = input("the stock m'lady: ").upper()
        plotforstock(stock)
    if int(choose) == 1:
        # changevars()
        findtheones()


def changevars(h, edge, ext):
    global hfromline, edgedays, extfac
    hfromline = h        # length from the trendline that it make it close to it
    edgedays = edge      # amount of days it checks after 3rd point
    extfac = ext         # how many bars the extremum has to be above from each side


def plotforstock(stock):  # to show plot of desired stock with trendline
    data = getdailydata(stock)
    if data == 'bad':
        exit(1)
    openpoints = data[0]
    highpoints = data[1]
    lowpoints = data[2]
    closepoints = data[3]
    days = data[4]
    stockname = data[5]
    volumes = data[6]
    alltogether = [openpoints, highpoints, lowpoints, closepoints, volumes]

    maxima = findmax(highpoints)
    minima = findmin(lowpoints)
    maxima.append(len(highpoints) - 1)
    minima.append(len(lowpoints) - 1)
    print("maximums:")
    for points in maxima:
        print(f'{points, str(datetime.fromtimestamp(int(days[points]) / 1000)), highpoints[points]}', end=", ")
    print("")
    print("minimums")
    for points in minima:
        print(f'{points, str(datetime.fromtimestamp(int(days[points]) / 1000)), lowpoints[points]}', end=", ")
    print("")
    # print(days)
    # print("")
    maxhighpoints = []
    minlowpoints = []
    for point in maxima:
        maxhighpoints.append(highpoints[point])
    for point in minima:
        minlowpoints.append(lowpoints[point])

    trendlinemax = findtrendline(maxhighpoints, maxima)
    trendlinemin = findtrendline(minlowpoints, minima)

    goodmaxeqs = goodmaxtrendline(trendlinemax, data)
    goodmineqs = goodmintrendline(trendlinemin, data)
    print('len tops = ' + str(len(goodmaxeqs)))
    print('len minss = ' + str(len(goodmineqs)))
    goodeqs = checkparallel(goodmaxeqs, goodmineqs)
    maxgoodeqs = list(goodeqs[0])
    mingoodeqs = list(goodeqs[1])
    print('len parallels: ' + str(len(maxgoodeqs)))
    print('len trenline max = ' + str(len(trendlinemax)))
    print('len trenline min = ' + str(len(trendlinemin)))
    showpar = True    # if you want the parallels do true if just lines do false
    if len(maxgoodeqs) == 0 and showpar:   # if you want the parallels but there are none
        print(f'{stockname} no parallels god damn')
    else:
        if showpar: # if you want the parallels and there are some
            print('maxs: ')
            for i in range(len(maxgoodeqs)):    # print max parallels
                print(f'{i}: {maxgoodeqs[i].slope, maxgoodeqs[i].n, maxgoodeqs[i].nums}', end="   ")
                if i % 2 == 1 and i > 0:
                    print('')
            print('')
            print('mins: ')
            for i in range(len(mingoodeqs)):    # print min paralleles
                print(f'{i}: {mingoodeqs[i].slope, mingoodeqs[i].n, mingoodeqs[i].nums}', end="   ")
                if i % 2 == 1 and i > 0:
                    print('')
            print('\n')
            theone = int(input("the parallel pls: "))  # which parallel would you like
            eqmax = maxgoodeqs[theone]     # actual plot
            eqmin = mingoodeqs[theone]
        else:     # if you want just some trendlines
            print('maxs: ')     # print max trendlines
            for i in range(len(goodmaxeqs)):
                print(f'{i}: {goodmaxeqs[i].slope, goodmaxeqs[i].n, goodmaxeqs[i].nums}', end=", ")
                if i % 2 == 1 and i > 0:
                    print('')
            print('')
            print('mins: ')    # print top trendline
            for i in range(len(goodmineqs)):
                print(f'{i}: {goodmineqs[i].slope, goodmineqs[i].n, goodmineqs[i].nums}', end=", ")
                if i % 2 == 1 and i > 0:
                    print('')
            print('')
            top = int(input('which top line: '))
            bot = int(input('which bot line: '))
            eqmax = goodmaxeqs[top]
            eqmin = goodmineqs[bot]

        xmax = np.array(range(len(highpoints) + 10))     # show lines on plot
        ymax = xmax * eqmax.slope + eqmax.n
        xmin = np.array(range(len(lowpoints)))
        ymin = xmin * eqmin.slope + eqmin.n
        plt.plot(xmax, ymax)  # show trend line max
        plt.plot(xmin, ymin)  # same but min
        plotshow(alltogether)  # for candles
        plt.scatter(maxima, maxhighpoints, color='cyan', s=7)  # for highlighting the maximums and minimums
        plt.scatter(minima, minlowpoints, color='cyan', s=7)
        plt.title('Candle Graph: ' + str(stockname))
        plt.xlabel('date')
        plt.ylabel('price')
        addticks(data)
        plt.show()


def addticks(data):
    openpoints = data[0]
    i = 0
    xtick = []
    labels = []
    result_ms = pandas.to_datetime(data[4][0], unit='ms')
    result_ms = str(result_ms)[:-9]
    labels.append(str(result_ms))
    x = np.array(range(len(openpoints)))
    xtick.append(x[0])
    for spot in range(1, len(x)):
        i += 1
        if not i == 10:
            continue
        xtick.append(x[spot])
        result_ms = pandas.to_datetime(data[4][spot], unit='ms')
        result_ms = str(result_ms)[:-9]
        labels.append(str(result_ms))
        i = 0
    plt.xticks(xtick, labels, rotation='vertical')
    plt.margins(0.2)
    plt.subplots_adjust(bottom=0.15)


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


hfromline = 0.1  #  height the maximum or minimum has to be from the trendline in percentage of topline - botline


def findtheones():
    myfile = open('100stocks.txt', 'w')
    start = 0
    end = len(stocklist)
    for number in range(start, end):
        if (number - 100) % 10 == 0:
            print(number)
        stock = stocklist[number]
        data = getdailydata(stock)
        if data == 'bad':
            continue
        openpoints = data[0]
        highpoints = data[1]
        lowpoints = data[2]
        closepoints = data[3]
        stockname = data[5]
        if not (openpoints or highpoints or lowpoints or closepoints or stockname):
            continue
        try:
            goodeqs = getgoodeqs(data)  # get the tunnels
        except TypeError:
            print('this stock is bad: ' + str(stock))
            continue
        except IndexError:
            print('this stock is bad: ' + str(stock))
            continue
        maxgoodeqs = list(goodeqs[0])
        mingoodeqs = list(goodeqs[1])
        closetotopeqs, closetoboteqs = checkclose(goodeqs, highpoints, lowpoints)

        closetop = ','.join(closetotopeqs)
        closebot = ','.join(closetoboteqs)

        if len(maxgoodeqs) == 0:
            # print(f'{stockname} no parallels god damn')
            pass
        else:
            stockinfo = str(str(stockname) + ', len of eqs:' + str(len(maxgoodeqs)) +' stock open price: ' +
                            str(openpoints[-1]) + ' closetopeqs: ' + closetop + ' closeboteqs: ' + closebot)
            myfile.write(stockinfo)
            myfile.write('\n')
    myfile.close()


def checkclose(goodeqs, highpoints, lowpoints):
    closetotopeqs = []
    closetoboteqs = []
    maxgoodeqs = list(goodeqs[0])
    mingoodeqs = list(goodeqs[1])
    for spot in range(len(maxgoodeqs)):
        if abs(height(maxgoodeqs[spot], len(highpoints) - 1, float(highpoints[-1]))) \
                < (maxgoodeqs[spot].n - mingoodeqs[spot].n) * hfromline:
            isclose = True
            closetotopeqs.append(str(spot))
        if abs(height(mingoodeqs[spot], len(lowpoints) - 1, float(lowpoints[-1]))) \
                < (maxgoodeqs[spot].n - mingoodeqs[spot].n) * hfromline:
            closetoboteqs.append(str(spot))
    return closetotopeqs, closetoboteqs

def getgoodeqs(data):
    openpoints = data[0]
    highpoints = data[1]
    lowpoints = data[2]
    closepoints = data[3]
    stockname = data[5]

    maxima = findmax(highpoints)  # find spot of maximum points
    minima = findmin(lowpoints)

    maxhighpoints = []
    minlowpoints = []
    for point in maxima:  # add maximum point
        maxhighpoints.append(highpoints[point])
    for point in minima:  # add minimum point
        minlowpoints.append(lowpoints[point])
    maxhighpoints.append(highpoints[-1])  # add last point
    minlowpoints.append(lowpoints[-1])
    maxima.append(len(highpoints) - 1)
    minima.append(len(highpoints) - 1)  # till here

    trendlinemax = findtrendline(maxhighpoints, maxima)  # find trendlines where [0] is the eq and
    trendlinemin = findtrendline(minlowpoints, minima)    # [1] is the 3 points

    goodmaxeqs = goodmaxtrendline(trendlinemax, data)   # find the good eqs
    goodmineqs = goodmintrendline(trendlinemin, data)

    goodeqs = checkparallel(goodmaxeqs, goodmineqs)  # find the tunnels

    return goodeqs


def checkparallel(maxeqs, mineqs):
    parallelmaxeqs = []
    parallelmineqs = []
    for maxeq in maxeqs:
        for mineq in mineqs:
            if mineq.slope * maxeq.slope < 0:
                continue
            fac = 0.25
            minang = abs(mt.degrees(mt.atan(mineq.slope)))  # absolute value of minline angle
            maxang = abs(mt.degrees(mt.atan(maxeq.slope)))  # absolute value of maxline angle
            if minang + fac > maxang > minang - fac:
                parallelmaxeqs.append(maxeq)
                parallelmineqs.append(mineq)
            """
            if maxeq.slope > 0 and mineq.slope > 0:
                if (mineq.slope + mineq.slope * 0.05) > maxeq.slope > (mineq.slope - mineq.slope * 0.05):
                    # print('max= ' + str(maxeq) + 'min =' + str(mineq))
                    parallelmaxeqs.append(maxeq)
                    parallelmineqs.append(mineq)
                    # if maxeq[0] < 0:
                    # print('nice' + str(len(parallelmaxeqs)))
                    # print(maxeq, mineq)
            elif maxeq.slope < 0 and mineq.slope < 0:
                if (abs(mineq.slope) + abs(mineq.slope) * 0.05) > abs(maxeq.slope) > (
                        abs(mineq.slope) - abs(mineq.slope) * 0.05):
                    parallelmaxeqs.append(maxeq)
                    parallelmineqs.append(mineq)
                    # print(f'oh yea {maxeq} {mineq}')
                """

    return parallelmaxeqs, parallelmineqs

def findeq(xpoints, ypoints):  # eq is eq[0] = slope  eq[1] = n
    x1 = float(xpoints[0])
    x2 = float(xpoints[1])
    y1 = float(ypoints[0])
    y2 = float(ypoints[1])
    m = (y2 - y1) / (x2 - x1)
    n = y1 - m * x1
    return m, n


def findtrendline(points, pointspots):
    length = len(points)
    goodeqs = []
    if int(points[0]/100) == 0:
        spliter = 0.05
    else:
        spliter = 0.01
    for i in range(length - 2):
        for j in range(i + 1, i + 10):
            ypoints = [points[i], points[j]]
            xpoints = [pointspots[i], pointspots[j]]
            eq1 = Eq(findeq(xpoints, ypoints)[0], findeq(xpoints, ypoints)[1])
            for t in range(i + 1, j + 5):
                if t == j:
                    continue
                if t > length - 1:
                    break
                if distance(pointspots[t], points[t], eq1.slope, eq1.n) < (points[t] * spliter):
                    if goodeqs:
                        chk = goodeqs[len(goodeqs) - 1]
                        #if pointspots[i] == 3 and pointspots[j] == 59:
                        # print(f'oh shit: {pointspots[t]}, {goodeqs[len(goodeqs) - 1].nums}')
                        if not (chk.slope == eq1.slope and chk.n == eq1.n):
                            item = [pointspots[i], pointspots[j], pointspots[t]]
                            eq1.nums = item
                            goodeqs.append(eq1)
                    else:
                        item = [pointspots[i], pointspots[j], pointspots[t]]
                        eq1.nums = item
                        goodeqs.append(eq1)
            if j == length - 1:
                break
    #for i in range(len(goodeqs)):
     #   print(f'{goodeqs[i].slope, goodeqs[i].n, goodeqs[i].nums}')
    #print(f'len is: {len(goodeqs)}')
    return goodeqs

edgedays = 10

def goodmaxtrendline(eqs, data):
    highpoints = data[1]
    goodlines = []
    for eqspot in range(len(eqs)):
        #print(eqs[eqspot].nums, eqs[eqspot].slope)
        isgood = True
        if int(eqs[eqspot].nums[2]) > int(eqs[eqspot].nums[1]):
            edge = int(eqs[eqspot].nums[2]) + edgedays
        else:
            edge = int(eqs[eqspot].nums[1]) + edgedays
        if edge + edgedays > len(highpoints):
            edge = len(highpoints)
        for point in range(int(eqs[eqspot].nums[0]) + 1, edge):
            if height(eqs[eqspot], point, highpoints[point]) > highpoints[point] * 0.02:    # check wrong ones
                isgood = False                                                    # ^ the height percentage above
                break
        if isgood:
            goodlines.append(eqs[eqspot])
    return goodlines


def goodmintrendline(eqs, data):
    lowpoints = data[2]
    goodlines = []
   # print('mins')
    for eqspot in range(len(eqs)):
        #print(eqs[eqspot].nums, eqs[eqspot].slope)
        isgood = True
        if int(eqs[eqspot].nums[2]) > int(eqs[eqspot].nums[1]):
            edge = int(eqs[eqspot].nums[2]) + edgedays
        else:
            edge = int(eqs[eqspot].nums[1]) + edgedays
        if edge + edgedays > len(lowpoints):
            edge = len(lowpoints)
        for point in range(int(eqs[eqspot].nums[0]), edge):  #checks for wrong ones
            if height(eqs[eqspot], point, lowpoints[point]) < (lowpoints[point] * 0.02) * (-1):
                isgood = False
                break
        if isgood:
            goodlines.append(eqs[eqspot])
            #if 38 == eqs[eqspot].nums[2]:
              #  print(f'this is {eqs[eqspot].nums, eqs[eqspot].slope, eqs[eqspot].n}')
    return goodlines


def height(eq, point, pointvalue):
    x = float(point)
    m = eq.slope
    n = eq.n
    heightpoint = x * m + n
    theheight = pointvalue - heightpoint
    return theheight


def distance(pointx, pointy, slope, n):
    x = float(pointx)
    y = float(pointy)
    m = float(slope)
    dis = (m * x - y + float(n)) / mt.sqrt(m ** 2 + 1)
    return abs(float(dis))

extfac = 4 # factor for how many points the extremum has to be above

def findmax(points):
    maximums = []
    for i in range(len(points) - extfac):
        if i < extfac - 1:
            continue
        checker = []
        for j in range(-1 * extfac, extfac):
            checker.append(points[i + j])
        if checker.index(max(checker)) == extfac:
            maximums.append(i)
    return maximums


def findmin(points):
    minimums = []
    for i in range(len(points) - extfac):
        if i < extfac - 1:
            continue
        checker = []
        for j in range(-1 * extfac, extfac):
            checker.append(points[i + j])
        if checker.index(min(checker)) == extfac:
            minimums.append(i)
       # x = i
    #print(x)
    """
    minimums1 = []

    for i in range(len(points) - 25):
        checker = []
        if i < 25:
            continue
        for j in range(i - 19, i + 20):
            checker.append(points[j])
        if checker.index(min(checker)) == 19:
            minimums1.append(i)
    """
    return minimums


def regression(listpointsx, listpointsy):
    meanx = mean(listpointsx)
    meany = mean(listpointsy)
    sumtop = 0
    sumbot = 0
    for i in range(len(listpointsx)):
        sumtop += (listpointsx[i] - meanx) * (listpointsy[i] - meany)
        sumbot += (listpointsx[i] - meanx) ** 2
    slope = sumtop / sumbot
    n = meany - meanx * slope
    return slope, n


def getdailydata(name):
    stockname = name
    my_share = share.Share(stockname)
    symbol_data = None
    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_MONTH, 4, share.FREQUENCY_TYPE_DAY, 1)
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


def gethourlydata(name):
    my_share = share.Share(name)
    symbol_data = None
    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_DAY, 30, share.FREQUENCY_TYPE_MINUTE, 60)
    except YahooFinanceError as e:
        print(e.message)
        sys.exit(1)
    goodhoursspot = []
    for i in range(len(symbol_data['timestamp'])):
        strdata = str(datetime.fromtimestamp(symbol_data['timestamp'][i] / 1000))
        checker = strdata[14]
        if checker == '3':
            goodhoursspot.append(i)
    # print(goodhoursspot)
    # print(symbol_data['open'][5])
    goodopenprices = []
    goodhighprices = []
    goodlowprices = []
    goodcloseprices = []
    goodhours = []
    goodvolumes = []
    for i in goodhoursspot:
        # print(str(datetime.fromtimestamp(symbol_data['timestamp'][i] / 1000)))
        goodopenprices.append(symbol_data['open'][i])
        goodhighprices.append(symbol_data['high'][i])
        goodlowprices.append(symbol_data['low'][i])
        goodcloseprices.append(symbol_data['close'][i])
        goodhours.append(symbol_data['timestamp'][i])
        goodvolumes.append(symbol_data['volume'][i])
    # print(goodopenprices, goodhighprices, goodlowprices, goodcloseprices)
    return goodopenprices, goodhighprices, goodlowprices, goodcloseprices, goodhours, name, goodvolumes


"""
def getdatafromcsv():
    with open("SBUX.csv", "r") as stock:
        reader = csv.DictReader(stock)
        days = []  # list of the days to have an x line in the graph
        openpoints = []  # list of the points so easier
        highpoints = []
        lowpoints = []
        closepoints = []
        for row in reader:
            Day = row['Date'][5] + row['Date'][6] + row['Date'][7] + row['Date'][8] + row['Date'][9]
            days.append(Day)
            Open = float(row['Open'])
            openpoints.append(Open)
            Close = float(row['Close'])
            closepoints.append(row['Close'])
            High = float(row['High'])
            highpoints.append(High)
            Low = float(row['Low'])
            lowpoints.append(Low)
    return (openpoints, highpoints, lowpoints, closepoints, days)
"""

if __name__ == "__main__":
    main()
