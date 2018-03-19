# creates output file book.txt of latest dex price for given market

' (BTS) litepresence1 '

# unlicensed - WTFPL v0 March 1765

from bitshares import BitShares
from bitshares.market import Market
from statistics import mean, median, mode
from ast import literal_eval as literal
from random import random
import numpy as np
import time
SATOSHI = 0.00000001

BitCURRENCY = 'USD'
BitASSET = 'BTS'
BitPAIR = BitASSET + ":" + BitCURRENCY

NODES = 5

def dex_book(market, depth=2):  # returns latest price on given market(node)

    # dictionary of 4 lists containing bid/ask volume/price
    raw = market.orderbook(limit=depth)
    bids = raw['bids']
    asks = raw['asks']
    bidp = [satoshi(bids[i]['price']) for i in range(len(bids))]
    bidv = [blur(bids[i]['quote']) for i in range(len(bids))]
    askp = [satoshi(asks[i]['price']) for i in range(len(asks))]
    askv = [blur(asks[i]['quote']) for i in range(len(asks))]
    book = {'bidp': bidp, 'bidv': bidv, 'askp': askp, 'askv': askv}

    if sum (bidp) > sum(askp):
        print ('WTF IS THIS SHIT?')


    #print(('ask', ('%.8f' % book['askp'][0])))  # lowest ask price
    #print(('bid', ('%.8f' % book['bidp'][0])))  # highest bid price
    #print(book['bidv'][0]) #highest bid volume
    #print(book['askv'][0]) #lowest ask volume
    return book


def market(n):  # returns market class using node "n"
    return Market(BitPAIR, bitshares_instance=BitShares(n, num_retries=0))


def satoshi(n):  # format prices to satoshi type
    return float('%.8f' % float(n))

def blur(n): # FOR DEV ONLY!!!! , replace w/ float for production on volumes
    return float('%.1f' % float(n))

def clock():  # 24 hour clock formatted HH:MM:SS
    return str(time.ctime())[11:19]


def verify_book():

    while 1:
            print('==========================================================')
            #try:
            # fetch list of good nodes from file maintained by nodes.py
            try:
                opened = 0
                while not opened:
                    with open('nodes.txt', 'r') as f:
                        node_list = f.read()
                        opened = 1
            except Exception as e:
                print (e)
                print ('nodes.txt failed, try again...')
                pass
            node_list = list(literal(node_list))

            # fetch last price from 5 dex nodes
            start = time.time()
            middles = []
            book_list = []
            nodes_used = []
            msg = ''
            for i in range(len(node_list)):
                triplicate = 0
                if (len(book_list) < NODES) and not triplicate:
                    try:
                        m = market(node_list[i])
                        ret = dex_book(m)
                        ##############################################################################
                        ##############################################################################
                        ##############################################################################
                        FUCK_BOOK = False # True ruins orderbook data to test RECONSTRUCTED method
                        def fuck_book():                           
                            ret['askp'] = [satoshi((0.99+0.02*random())*i) for i in ret['askp']]
                            ret['bidp'] = [satoshi((1.01-0.02*random())*i) for i in ret['bidp']]
                            return ret
                        if FUCK_BOOK: 
                            print ('intentionally ruining orderbook for dev')
                            ret = fuck_book()
                        ##############################################################################
                        ##############################################################################
                        ##############################################################################
                        print(ret)
                        book_list.append(ret)
                        nodes_used.append(node_list[i])
                    except:
                        pass
                    sbooks = [str(i) for i in book_list]
                    #print (len(sbooks))
                    if (len(sbooks) >= 3) and len(set(sbooks[-3:])) == 1:
                        book = book_list[-1]
                        msg += 'triplicate book'
                        triplicate = 1
                        break





            if triplicate == 0:
                # check last list and return best last price with message
                book = {'bidp':[],'bidv':[],'askp':[],'askv':[]}
                try:
                    book = literal(mode([str(i) for i in book_list]))
                    msg += 'mode book'
                except:

                    book = {i : list(np.median([x[i] for x in book_list], axis=0)) for i in ['bidp','bidv','askp','askv']}


                    

                    book['askp'] = [satoshi(i) for i in book['askp']]
                    book['bidp'] = [satoshi(i) for i in book['bidp']]
                    # REMEMBER TO REMOVE BLUR FOR PRODUCTION
                    book['askv'] = [blur(i) for i in book['askv']]
                    book['bidv'] = [blur(i) for i in book['bidv']]

                    asksort = sorted(book['askp'])
                    bidsort = sorted(book['bidp'], reverse=True)


                    if (asksort != book['askp']): print('asksort')
                    if (bidsort != book['bidp']): print('bidsort')
                    if (len(set(asksort)) != len(asksort)): print('askmatch')
                    if (len(set(bidsort)) != len(bidsort)): print('bidmatch')
                    if (bidsort[0] > asksort[0]): print('mismatched')


                    if ((asksort == book['askp']) and 
                        (bidsort == book['bidp']) and
                        (len(set(asksort)) == len(asksort)) and
                        (len(set(bidsort)) == len(bidsort)) and
                        (bidsort[0] < asksort[0])):
                            msg += '!!! MEDIAN BOOK !!!'
        
                    #if 0: pass

                    else:
                        msg += '!!! RECONSTRUCTED BOOK !!!'
                        # assure median comprehension did not reorganize book prices
                        prices = []
                        prices = prices + book['askp'] + book['bidp']

                        prices = sorted(prices)
                        z = len(prices) #will except if odd... shouldn't be, so let it fail
                        prices = [satoshi(i) for i in prices]

                        book['askp'] = prices[int(z/2):z]
                        book['bidp'] = prices[0:int(z/2)]
                        book['askp'] = sorted(book['askp'])
                        book['bidp'] = sorted(book['bidp'], reverse=True) 

                        if book['bidp'][0] == book['askp'][0]:
                            book['askp'] = [(i+SATOSHI) for i in book['askp']]
                            book['bidp'] = [(i-SATOSHI) for i in book['bidp']]

                        for i in range(1,len(book['askp'])):
                            if book['askp'][i] < book['askp'][i-1]:
                                book['askp'][i] = max(book['askp'][i-1]+SATOSHI, book['askp'][i])

                        for i in range(1,len(book['bidp'])):
                            if book['bidp'][i] < book['bidp'][i-1]:
                                book['bidp'][i] = min(book['bidp'][i-1]-SATOSHI, book['bidp'][i])


                        # REMEMBER TO REMOVE BLUR FOR PRODUCTION
                        book['askv'] = [blur(i) for i in book['askv']]
                        book['bidv'] = [blur(i) for i in book['bidv']]

            rrange = sum(book['bidp'])+sum(book['askp'])                    
            if 1: 
                pass
            else:
                # create blacklist.txt if relative range too wide
                print('BLACKLIST last' + str(book))
                print(str(book_list))
                print(str(nodes_used))
                try:
                    opened = 0
                    while not opened:
                        with open('blacklist.txt', 'a+') as file:
                            file.write("\n" + 'BLACKLIST last' + str(book))
                            file.write("\n" + str(book_list))
                            file.write("\n" + str(nodes_used))
                            opened = 1
                except Exception as e:
                    print (e)
                    print ('blacklist.txt failed, try again...')
                    pass    
            # maintain a log of last price, relative range, and statistics type
            elapsed = '%.1f' % (time.time() - start)
            print (clock(), 'elapsed: ', elapsed,
                   'nodes: ', len(book_list), 'type: ', ('%.3f' % rrange), msg)
            print (book)
            # update communication file last.txt
            try:
                opened = 0
                while not opened:
                    with open('book.txt', 'w+') as file:
                        file.write(str(book))
                        opened = 1
            except Exception as e:
                print (e)
                print ('last.txt failed, try again...')
                pass
        # no matter what happens just keep attempting to update last price
        #except Exception as e:
        #    print (e)
        #    print ('verify_book failed')
        #    pass
        #time.sleep(30)


if __name__ == '__main__':

    verify_book()







