def main():
    trendys = open('100stocks.txt', 'r')
    tog = open('togethers.txt', 'w')
    amn = 0
    for trline in trendys:
        trendname = []
        for trletter in trline:
            if trletter == ',':
                break
            trendname.append(str(trletter))
        trstock = "".join(trendname)
        macds = open('macd100.csv', 'r')
        for macdline in macds:
            macdname = []
            for mcletter in macdline:
                if mcletter == ',':
                    break
                macdname.append(str(mcletter))
            mcstock = ''.join(macdname)
            if trstock == mcstock:
                tog.write(macdline + trline + '\n')
                amn += 1
    print(amn)

    tog.close()







if __name__ == '__main__':
    main()