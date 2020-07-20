def calculatervi(stockdata):   # i get 1 stock data
    opens = stockdata[0]
    highs = stockdata[1]
    lows = stockdata[2]
    closes = stockdata[3]
    numerlist = []
    denomerlist = []
    period = 10
    for spot in range(4, len(opens)):
        a = closes[spot] - opens[spot]
        b = closes[spot - 1] - opens[spot - 1]
        c = closes[spot - 2] - opens[spot - 2]
        d = closes[spot - 3] - opens[spot - 3]
        e = highs[spot] - lows[spot]
        f = highs[spot - 1] - lows[spot - 1]
        g = highs[spot - 2] - lows[spot - 2]
        h = highs[spot - 3] - lows[spot - 3]
        numerlist.append((a + (2*b) + (2*c) + d)/6)
        denomerlist.append((e + (2*f) + (2*g) + h)/6)

    rvilist = []
    signallist = []
    smanumer = findsma(period, numerlist)
    smadenomer = findsma(period, denomerlist)
    for num in range(len(smanumer)):
        rvi = smanumer[num] / smadenomer[num]
        rvilist.append(rvi)
        if num < 4:
            continue
        i = rvilist[num - 1]
        j = rvilist[num - 2]
        k = rvilist[num - 3]
        signallist.append((rvi + (2+i) + (2*j) + k)/6)

    while len(rvilist) > len(signallist):
        rvilist.pop(0)
    print(rvilist)
    return (rvilist, signallist)



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