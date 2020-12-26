import threading

a = 0

def add():
    global a
    for i in range(1000000):
        a += 1


def minus():
    global a
    for i  in range(1000000):
        a -= 1


def main():


    threading.Thread(target=add).start()


    threading.Thread(target=minus).start()



if __name__ == '__main__':
    main()

    print(a)




