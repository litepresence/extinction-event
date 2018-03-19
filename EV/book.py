# creates output file book.txt of latest dex price for given market

' (BTS) litepresence1 '

# unlicensed - WTFPL v0 March 1765

from bitshares import BitShares
from bitshares.market import Market
from statistics import mean, median, mode
from ast import literal_eval as literal
import numpy as np
import time

BitCURRENCY = 'USD'
BitASSET = 'BTS'
BitPAIR = BitASSET + ":" + BitCURRENCY

def dex_book(market, depth=2):  # returns latest price on given market(node)

    # dictionary of 4 lists containing bid/ask volume/price
    raw = market.orderbook(limit=depth)
    bids = raw['bids']
    asks = raw['asks']
    bidp = [satoshi(bids[i]['price']) for i in range(len(bids))]
    bidv = [float(bids[i]['quote']) for i in range(len(bids))]
    askp = [satoshi(asks[i]['price']) for i in range(len(asks))]
    askv = [float(asks[i]['quote']) for i in range(len(asks))]
    book = {'bidp': bidp, 'bidv': bidv, 'askp': askp, 'askv': askv}
    print(book)
    #print(('ask', ('%.8f' % book['askp'][0])))  # lowest ask price
    #print(('bid', ('%.8f' % book['bidp'][0])))  # highest bid price
    #print(book['bidv'][0]) #highest bid volume
    #print(book['askv'][0]) #lowest ask volume
    return book


def market(n):  # returns market class using node "n"
    return Market(BitPAIR, bitshares_instance=BitShares(n, num_retries=0))


def satoshi(n):  # format prices to satoshi type
    return float('%.5f' % float(n))


def clock():  # 24 hour clock formatted HH:MM:SS
    return str(time.ctime())[11:19]


def verify_book():

    while 1:
        print('==========================================================')
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
            for i in range(len(node_list)):
                if len(book_list) < 3:
                    try:
                        m = market(node_list[i])
                        ret = dex_book(m)
                        middles.append((ret['askp'][0]+ret['bidp'][0])/2)
                        book_list.append(ret)
                        nodes_used.append(node_list[i])
                    except:
                        pass
            # calculate relative range
            rrange = (max(middles) - min(middles)) / mean(middles)

            # check last list and return best last price with message
            msg = ''
            book = {'bidp':[],'bidv':[],'askp':[],'askv':[]}
            try:
                book = literal(mode([str(i) for i in book_list]))
                msg += 'mode'
            except:
                print(3)
                book = {i : list(np.median([x[i] for x in book_list], axis=0)) for i in ['bidp','bidv','askp','askv']}
                print(3.1)
                msg += 'median'
                if book['bidp'][0] < book['askp'][0]:
                    msg += ' good'
                else:
                    msg += ' bad'
                print(3.5)   
            # override median or mode with latest if less than 2%
            # difference

            if rrange < 0.02:

                #book = book_list[-1]
                print(4)
            else:
                print(5)
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
            print (6)        
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
        except Exception as e:
            print (e)
            print ('verify_book failed')
            pass
        #time.sleep(30)


if __name__ == '__main__':

    verify_book()







