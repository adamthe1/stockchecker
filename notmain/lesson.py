

def main():
    x = [1, 2, 3, 52, 108, 16, 34]
    scum = 0
    camut = 0
    for i in x:
        scum = scum + i
        camut = camut + 1
    memuza = scum/camut
    print(memuza)

    reshima = ['hi', 'hell', 'yolo', 'nice', 'hello', 'nonono', 'hate']
    reshima2 = []
    for word in reshima:
        if word[0] == 'n':
            reshima2.append(word)
    print(reshima2)
    mispar = 8
    for i in range(mispar):
        for j in range(mispar - (i + 1)):
            print(' ', end='')
        for j in range(i+1):
            print('#', end='')
        print(' ', end='')
        for j in range(i + 1):
            print('#', end='')
        print('')






if __name__ == '__main__':
    main()