from numpy import mean

def main():
    listpointsx = []
    listpointsy = []

    usinputx = 0
    usinputy = 0
    while not usinputx == 'stop':
        usinputx = input("enter num x: ")
        if usinputx == 'stop':
            pass
        elif float(usinputx) in listpointsx:
            print("cannot have 2 same x var")
        else:
            usinputy = input("enter num y: ")
            if not usinputx.isnumeric():
                print("not numeric redo")
            else:
                listpointsx.append(float(usinputx))
            if not usinputx.isnumeric() or not usinputy.isnumeric():
                print("not numeric redo")
            else:
                listpointsy.append(float(usinputy))

    print(regression(list(listpointsx), listpointsy))

def regression(listpointsx, listpointsy):
    meanx = mean(listpointsx)
    meany = mean(listpointsy)
    sumtop = 0
    sumbot = 0
    for i in range(len(listpointsx)):
        sumtop += (listpointsx[i] - meanx) * (listpointsy[i] - meany)
        sumbot += (listpointsx[i] - meanx) ** 2
    slope = sumtop/sumbot
    n = meany - meanx * slope
    return(slope, n)

if __name__ == "__main__":
    main()




