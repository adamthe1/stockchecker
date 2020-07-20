from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
from get_all_tickers import get_tickers as gt


def main():
    listy = gt.get_tickers()
    with open('../stocklist.csv', "w") as outfile:
        for entries in listy:
            if getdailydata(entries) == 'cool':
                outfile.write(entries)
                outfile.write("\n")


def getdailydata(name):
    stockname = name
    my_share = share.Share(stockname)
    symbol_data = None
    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_MONTH,3,share.FREQUENCY_TYPE_DAY,1)
    except YahooFinanceError as e:
        print(e.message)
        return('bad')
    #print(len(symbol_data['open']))
    return('cool')


if __name__ == '__main__':
    main()