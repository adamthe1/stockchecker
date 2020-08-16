pricenow = float(input('what is the price now: '))
getoutbuy = float(input('what is your get profit price? (num) : '))

getoutlose = float(input('what is your stop loss price? (num) : '))
buyper = (getoutbuy/pricenow) * 100 - 100
loseper = (getoutlose/pricenow) * 100 - 100

print('buy percent: ' + str(buyper))
print('lose percent: ' + str(loseper))
print('chance lose: ' + str(buyper/abs(loseper)))
