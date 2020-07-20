import sys
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
from datetime import datetime



def gethourlydata():
    my_share = share.Share('NFLX')
    symbol_data = None
    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_DAY,4,share.FREQUENCY_TYPE_MINUTE,60)
    except YahooFinanceError as e:
        print(e.message)
        sys.exit(1)
    goodhoursspot = []
    for i in range(len(symbol_data['timestamp'])):
        strdata = str(datetime.fromtimestamp(symbol_data['timestamp'][i]/1000))
        checker = strdata[14]
        if checker == '3':
            goodhoursspot.append(i)
    print(goodhoursspot)
    for i in goodhoursspot:
        print(str(datetime.fromtimestamp(symbol_data['timestamp'][i] / 1000)))
        print(symbol_data['open'][i])
    #for i in symbol_data:
        #print(i)
        #if i == "open":
          #  for spot in range(len(symbol_data[i])):
           #     print(symbol_data[i][spot], end= ': ')
            #    print(symbol_data['timestamp'][spot], end= "/ ")
             #   print(datetime.fromtimestamp(symbol_data['timestamp'][spot]/1000))

def main():
    gethourlydata()

if __name__ == "__main__":
    main()
