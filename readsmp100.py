file = open('notmain/smp100.txt', 'r')
smp100 = []
for line in file:
    stockname = []
    for letter in line:
        if letter == '\t':
            break
        stockname.append(letter)
    smp100.append("".join(stockname))
print(smp100)
newfile = open('smp100.csv', 'w')
for stock in smp100:
    newfile.write(str(stock) + '\n')
file.close()
newfile.close()