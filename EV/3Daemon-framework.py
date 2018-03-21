# 3 daemon parallel processing with text file communication

' (BTS) litepresence1 '

# unlicensed - WTFPL v0 March 1765

from multiprocessing import Process
from random import random
import time

def clock():  # 24 hour clock formatted HH:MM:SS
    return str(time.ctime())[11:19]

def sub_a():

    a = 0
    while 1:
        time.sleep(2*random())
        a+=1
        print(a, 'a')
        try:
            opened = 0
            while not opened:
                with open('test.txt', 'w+') as file:
                    file.write('a ' + str(a))
                    opened = 1
        except Exception as e:
            print (e)
            print ('a test.txt failed, try again...')
            pass

def sub_b():

    b = 0
    while 1:
        time.sleep(6*random())
        b += 1
        print(b, 'bbb')
        try:
            opened = 0
            while not opened:
                with open('test.txt', 'w+') as file:
                    file.write('bbb ' + str(b))
                    opened = 1
        except Exception as e:
            print (e)
            print ('b test.txt failed, try again...')
            pass

def sub_c():

    c = 0
    while 1:
        time.sleep(18*random())
        c += 1
        print(c, 'ccccccccc')
        try:
            opened = 0
            while not opened:
                with open('test.txt', 'w+') as file:
                    file.write('ccccccccc ' + str(c))
                    opened = 1
        except Exception as e:
            print (e)
            print ('c test.txt failed, try again...')
            pass

sa = Process(target=sub_a)
sa.daemon = True
sb = Process(target=sub_b)
sb.daemon = True
sc = Process(target=sub_c)
sc.daemon = True

sa.start()
sb.start()
sc.start()

m = 0
while 1:

    m += 1
    time.sleep(1)
    
    try:
        opened = 0
        while not opened:
            with open('test.txt', 'r') as f:
                ret = f.read()
                print(clock(), '========', ret)
                opened = 1
    except Exception as e:
        print (e)
        print ('c test.txt failed, try again...')
        pass
