# creates output file book.txt of latest dex orderbook for given market

# 90% checks 5 nodes, seeks 3 the same
# 4% if no 3 then gives matching 2
# 3% if no matching 2 then gives columnwise median
# <1% if anything goes wrong w/ median, renders statistical reconstruction 
# averages 15 seconds per loop



# alpha testing



' (BTS) litepresence1 '

# unlicensed - WTFPL v0 March 1765

from bitshares import BitShares
from bitshares.market import Market
from statistics import mean, median, mode
from ast import literal_eval as literal
from random import random
import numpy as np
import time
DFLOAT = 0.0000000000000001

BitCURRENCY = 'USD'
BitASSET = 'BTS'
BitPAIR = BitASSET + ":" + BitCURRENCY


NODES = 5


def dex_book(market, depth=10):  # returns latest price on given market(node)

    # dictionary of 4 lists containing bid/ask volume/price
    raw = market.orderbook(limit=depth)
    bids = raw['bids']
    asks = raw['asks']
    bidp = [float(bids[i]['price']) for i in range(len(bids))]
    bidv = [float(bids[i]['quote']) for i in range(len(bids))]
    askp = [float(asks[i]['price']) for i in range(len(asks))]
    askv = [float(asks[i]['quote']) for i in range(len(asks))]
    book = {'bidp': bidp, 'bidv': bidv, 'askp': askp, 'askv': askv}

    if sum(bidp) > sum(askp):
        print ('WTF IS THIS SHIT?')
        print (book)

    return book

def market(n):  # returns market class using node "n"
    return Market(BitPAIR, bitshares_instance=BitShares(n, num_retries=0))

def clock():  # 24 hour clock formatted HH:MM:SS
    return str(time.ctime())[11:19]

FUCK_BOOK = False  # True ruins orderbook data to test RECONSTRUCTED method
def fuck_book(ret):
    ret['askp'] = [((0.99 + 0.02 * random()) * i)
                   for i in ret['askp']]
    ret['bidp'] = [((0.99 + 0.02 * random()) * i)
                   for i in ret['bidp']]
    return ret

def verify_book():

    tally = {'triple':0, 'mode':0, 'median':0, 'built':0}
    while True:


        try:
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
            test = []
            msg = ''
            for i in range(len(node_list)):
                triplicate = 0
                if (len(book_list) < NODES) and not triplicate:


                    try:
                        m = market(node_list[i])
                        ret = dex_book(m)
                        if FUCK_BOOK:
                            ret = fuck_book(ret)
                        #print(ret)
                        book_list.append(ret)
                        nodes_used.append(node_list[i])
                        test.append(i)

                    except:
                        pass
                    sbooks = [str(i) for i in book_list]

                    #print ((test[:3]))
                    #print ((test[-3:]))
                    if (len(sbooks) >= 3) and len(set(sbooks[-3:])) == 1:
                        book = book_list[-1]
                        asksort = sorted(book['askp'])
                        bidsort = sorted(book['bidp'], reverse=True)
                        if ((asksort == book['askp']) and
                            (bidsort == book['bidp']) and
                            (len(set(asksort)) == len(asksort)) and
                            (len(set(bidsort)) == len(bidsort)) and
                                (bidsort[0] < asksort[0])):
                            msg += 'triplicate book'
                            triplicate = 1
                            tally['triple']+=1
                            break
                        else:
                            msg += 'triplicate book error - '


            #book_list = [{'askp': [0.14779781, 0.14779781, 0.14779781, 0.14779781], 'bidv': [530.3, 67.7], 
            #    'bidp': [0.14779781, 0.14779781, 0.14779781, 0.14779781], 'askv': [10044.5, 420.0]},]

            if triplicate == 0:
                # check last list and return best last price with message
                try:
                    book = literal(mode([str(i) for i in book_list]))
                    asksort = sorted(book['askp'])
                    bidsort = sorted(book['bidp'], reverse=True)
                    if (asksort != book['askp']):
                        print('asksort')
                    if (bidsort != book['bidp']):
                        print('bidsort')
                    if (len(set(asksort)) != len(asksort)):
                        print('askmatch')
                    if (len(set(bidsort)) != len(bidsort)):
                        print('bidmatch')
                    if (bidsort[0] > asksort[0]):
                        print('mismatched')
                    if ((asksort == book['askp']) and
                        (bidsort == book['bidp']) and
                        (len(set(asksort)) == len(asksort)) and
                        (len(set(bidsort)) == len(bidsort)) and
                            (bidsort[0] < asksort[0])):
                        msg += 'mode book'
                        tally['mode']+=1
                    else:
                        raise
                except:

                    book = {i: list(np.median([x[i] for x in book_list], axis=0))
                            for i in ['bidp', 'bidv', 'askp', 'askv']}
                    asksort = sorted(book['askp'])
                    bidsort = sorted(book['bidp'], reverse=True)
                    if (asksort != book['askp']):
                        print('asksort')
                    if (bidsort != book['bidp']):
                        print('bidsort')
                    if (len(set(asksort)) != len(asksort)):
                        print('askmatch')
                    if (len(set(bidsort)) != len(bidsort)):
                        print('bidmatch')
                    if (bidsort[0] > asksort[0]):
                        print('mismatched')
                    if ((asksort == book['askp']) and
                        (bidsort == book['bidp']) and
                        (len(set(asksort)) == len(asksort)) and
                        (len(set(bidsort)) == len(bidsort)) and
                            (bidsort[0] < asksort[0])):
                            msg += '!!! MEDIAN BOOK !!!'
                            tally['median']+=1

                    else:
                        print ((book['bidp'][:3])[::-1], 'BIDS <> ASKS', book['askp'][:3],1)
                        msg += '!!! RECONSTRUCTED BOOK !!!                  *****'
                        tally['built']+=1
                        # assure median comprehension did not reorganize book
                        # prices
                        prices = []
                        prices = prices + book['askp'] + book['bidp']
                        prices = sorted(prices)
                        z = len(prices)  # will except if odd... shouldn't be, so let it fail
                        book['askp'] = prices[int(z / 2):z]
                        book['bidp'] = prices[0:int(z / 2)]
                        book['askp'] = sorted(book['askp'])
                        book['bidp'] = sorted(book['bidp'], reverse=True)
                        print ((book['bidp'][:3])[::-1], 'BIDS <> ASKS', book['askp'][:3],2)
                        if book['bidp'][0] == book['askp'][0]:
                            book['askp'] = [(i + DFLOAT)
                                            for i in book['askp']]
                            book['bidp'] = [(i - DFLOAT)
                                            for i in book['bidp']]
                        print ((book['bidp'][:3])[::-1], 'BIDS <> ASKS', book['askp'][:3],3)
                        for i in list(range(1, len(book['askp']))):
                            if book['askp'][i] <= book['askp'][i-1]:
                                book['askp'][i] = max(
                                    (book['askp'][i-1] + DFLOAT),
                                    book['askp'][i])
                        print ((book['bidp'][:3])[::-1], 'BIDS <> ASKS', book['askp'][:3],4)
                        for i in list(range(1, len(book['bidp']))):
                            if book['bidp'][i] >= book['bidp'][i - 1]:
                                book['bidp'][i] = min(
                                    book['bidp'][i - 1] - DFLOAT,
                                    book['bidp'][i])
                        print ((book['bidp'][:3])[::-1], 'BIDS <> ASKS', book['askp'][:3],5)
                        print('====================================================================')

            rrange = sum(book['bidp']) + sum(book['askp'])





            # maintain a log of last price, relative range, and statistics type
            elapsed = '%.1f' % (time.time() - start)

            #print (book['bidp'][::-1], 'BIDS <> ASKS', book['askp'])
            print ((book['bidp'][:3])[::-1], 'BIDS <> ASKS', book['askp'][:3])
            try:
                
                s=sum(tally.values())
                ptally = {k:('%.2f' % (v/s)) for k,v in tally.items()}
                #print (tally)
                print (clock(), ptally, 'elapsed: ', elapsed,
                       'nodes: ', len(book_list), 'type: ', ('%.3f' % rrange), msg)
                print('===================================================================='+
                      '====================================================================')
            except:
                pass
            # update communication file book.txt
            try:
                opened = 0
                while not opened:
                    with open('book.txt', 'w+') as file:
                        file.write(str(book))
                        opened = 1
            except Exception as e:
                print (e)
                print ('book.txt failed, try again...')
                pass
        #no matter what happens just keep attempting to update last price
        except Exception as e:
            print (e)
            print ('verify_book failed')
            pass
        time.sleep(30)



if __name__ == '__main__':

    verify_book()
