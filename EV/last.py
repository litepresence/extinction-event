# creates output file last.txt of dex price

# reads file nodes.txt to get list of latency sorted nodes from nodes.py
# contacts 5 different nodes
# if all same returns price
# else tries to return mode of price
# except if no mode returns median of price
# however if relative range < 2% 
# returns latest price instead
# use in conjuction with nodes.py which maintains list of low latency nodes.txt
# if relative range > 2 % appends report to file blacklist.txt
# typical elapsed 30 seconds per loop

' (BTS) litepresence1 '

# unlicensed - WTFPL v0 March 1765

from bitshares import BitShares
from bitshares.market import Market
from statistics import mean, median, mode
from ast import literal_eval as literal
import time

BitCURRENCY = 'USD'
BitASSET = 'BTS'
BitPAIR = BitASSET + ":" + BitCURRENCY

def dex_last(market):  # returns latest price on given market(node)
    return float(market.ticker()['latest'])

def market(n):  # returns market class using node "n"
    return Market(BitPAIR, bitshares_instance=BitShares(n, num_retries=0))

def satoshi(n):  # format prices to satoshi type
    return float('%.8f' % float(n))

def clock():  # 24 hour clock formatted HH:MM:SS
    return str(time.ctime())[11:19]

while True:

    try:
        # fetch list of good nodes from file maintained by nodes.py
        with open('nodes.txt', 'r') as f:
            node_list = f.read()
        node_list = list(literal(node_list))

        # fetch last price from 5 dex nodes
        start = time.time()
        last_list = []
        nodes_used = []
        for i in range(len(node_list)):
            if len(last_list) < 5:
                ret = 'No data from node: '
                try:
                    m = market(node_list[i])
                    ret = satoshi(dex_last(m))
                    last_list.append(ret)
                    nodes_used.append(node_list[i])
                except:
                    pass

        # check last list and return best last price with message
        msg = ''
        if len(set(last_list)) == 1:
            last = last_list[-1]
            msg += 'common'
        else:
            try:
                last = mode(last_list)
                msg += 'mode'
            except:
                last = median(last_list)
                msg += 'median'
            # calculate relative range
            rrange = (max(last_list) - min(last_list)) / mean(last_list)
            # override median or mode with latest if less than 2% difference
            if rrange < 0.02:
                last = last_list[-1]
                msg = 'latest (' + msg + ')'
            else:
                # create blacklist.txt if data is rrange too wide
                print('?!? BLACKLIST - LAST ?!? ' + str(last))
                print(str(last_list))
                print(str(nodes_used))
                with open('blacklist.txt', 'a+') as file:
                    file.write("\n" + '?!? BLACKLIST - LAST ?!? ' + str(last))
                    file.write("\n" + str(last_list))
                    file.write("\n" + str(nodes_used))

        # maintain a log of last price, note relative range and statistics type
        last = satoshi(last)
        elapsed = '%.1f' % (time.time() - start)
        print (('%.8f' % last), clock(), 'elapsed: ', elapsed,
               'nodes: ', len(last_list), 'type: ', ('%.3f' % rrange), msg)

        # update communication file last.txt
        with open('last.txt', 'w+') as file:
            file.write(str(last))

    # no matter what happens just keep attempting to update last price
    except:
        print ('error')
        pass
