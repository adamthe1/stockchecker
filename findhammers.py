import csv
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
from datetime import datetime

stocklist = []
with open('stocklist.csv', 'r') as stocks:
    stockreader = csv.reader(stocks, delimiter='\n')
    for row in stockreader:
        stocklist.append(row[0])

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





def main():
    stockname = input('pls stock name quick boi: ')
    data = getdailydata(stockname)
    openlist = data[0]
    closelist = data[3]
    highlist = data[1]
    lowlist = data[2]
    print('len days: ' + str(len(data[4])))
    for spot in range(len(openlist)):
        Open = float(openlist[spot])
        Close = float(closelist[spot])
        High = float(highlist[spot])
        Low = float(lowlist[spot])
        allthem = [Open, High, Low, Close]
        if Open - Close < 0:
            first = isgreenhammer(allthem)
            second = isgreenhammer2(allthem)
            if first == True and second == True:
                print(f"g: {str(datetime.fromtimestamp(int(data[4][spot]) / 1000))[:-9]} {Open - Low} {High - Close}")
                pass
            elif first == True and second == False:
                print(f"g1: {str(datetime.fromtimestamp(int(data[4][spot]) / 1000))[:-9]} {Open - Low} {High - Close}")
                # i+= 1
                pass
            elif first == False and second == True:
                # i += 1
                print(f"g2: {str(datetime.fromtimestamp(int(data[4][spot]) / 1000))[:-9]} {Open - Low} {High - Close}")
                pass

        else:
            firstr = isredhammer(allthem)
            secondr = isredhammer2(allthem)
            if firstr == True and secondr == True:
                print(f"r: {str(datetime.fromtimestamp(int(data[4][spot]) / 1000))[:-9]} {Close - Low} {High - Open}")
                pass
            elif firstr == True and secondr == False:
                # i += 1
                print(f"r1: {str(datetime.fromtimestamp(int(data[4][spot]) / 1000))[:-9]} {Close - Low} {High - Open}")
                pass
            elif firstr == False and secondr == True:
                # i += 1
                print(f"r2: {str(datetime.fromtimestamp(int(data[4][spot]) / 1000))[:-9]} {Close - Low} {High - Open}")
                pass

def ishammer(spotdata):  # spot data is a list of [open, high, low, close] of the spot its checking
    """

    :rtype:
    """
    openp, high, low, close = spotdata
    if close - openp > 0:
        first = isgreenhammer(spotdata)
        second = isgreenhammer2(spotdata)
        if first and second:
            return 'hsgreen'
        elif first or second:
            return 'hwgreen'
    else:
        first = isredhammer(spotdata)
        second = isredhammer2(spotdata)
        if first and second:
            return 'hsred'
        elif first or second:
            return 'hwred'
    return 'no'



def isgreenhammer(them):
    Open = them[0]
    Close = them[3]
    High = them[1]
    Low = them[2]
    if High - Low < Close * 0.01:
        pass
    elif not ((Low > (Open - (Open * 0.003))) or (High - Close < (Close * 0.003))):
        pass
    elif (((Open - Low) / 1.75) > (Close - Open)) or (((High - Close) / 1.75) > (Close - Open)):
        # if row['Date'] == thedate:
        # print("hi2")
        return True
    return False


def isgreenhammer2(them):
    Open = them[0]
    Close = them[3]
    High = them[1]
    Low = them[2]
    if High - Low < Close * 0.01:
        pass
    elif not (((Open - Low) < (Close - Open) * 0.7) or ((High - Close) < ((Close - Open) * 0.7))):
        pass
    elif (((Open - Low) / 1.75) > (Close - Open)) or (((High - Close) / 1.75) > (Close - Open)):
        # if row['Date'] == thedate:
        # print("hi2")
        return True
    return False


def isredhammer(them):
    Open = them[0]
    Close = them[3]
    High = them[1]
    Low = them[2]
    if High - Low < Close * 0.01:
        pass
    elif not (((Close - Low) < (Close * 0.003)) or (High < (Open + (Open * 0.003)))):
        pass
    elif (((Close - Low) / 1.75) > (Open - Close)) or (((High - Open) / 1.75) > (Open - Close)):
        return (True)
    return (False)


def isredhammer2(them):
    Open = them[0]
    Close = them[3]
    High = them[1]
    Low = them[2]
    if High - Low < Close * 0.01:
        pass
    elif not (((Close - Low) < (Open - Close) * 0.5) or ((High - Open) < (Open - Close) * 0.5)):
        pass
    elif (((Close - Low) / 1.75) > (Open - Close)) or (((High - Open) / 1.75) > (Open - Close)):
        return True
    return False


if __name__ == "__main__":
    main()
