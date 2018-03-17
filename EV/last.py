# creates output file last.txt of dex price

# reads file nodes.txt to get list of latency sorted nodes from nodes.py
# contacts 5 different nodes 
# if all same returns price
# else tries to return mode of price
# except if no mode returns median of price
# however latest less than 2% away from mode or median, 
# returns latest price instead

# use inconjuction with nodes.py which maintains list of high latency nodes.txt

# if data spread too wide appends report to file blacklist.txt

# typical elapsed 30 seconds per loop

# (BTS) litepresence1


from bitshares import BitShares
from bitshares.market import Market
import ast
from statistics import mean,median,mode
import time

BitCURRENCY = 'USD'
BitASSET = 'BTS'
BitPAIR = BitASSET + ":" + BitCURRENCY
SATOSHI = 0.00000001
ANTISAT = 1 / SATOSHI


def dex(  # Public AND Private API Bitshares
        command, amount=ANTISAT, price=None,
        depth=1, expiration=ANTISAT):

    if command == 'last':

        # the most recent transation in this MARKET
        #print(('Bitshares API', command))
        raw = MARKET.ticker()['latest']
        price = float(raw)
        # print (price)
        return price

def market(n):
    global MARKET
    MARKET = Market(BitPAIR, bitshares_instance=BitShares(n, num_retries=0))

def satoshi(n):
    return float('%.8f' % float(n))

def clock():
    return str(time.ctime())[11:19]
    

while 1:

    with open('nodes.txt','r') as f:
        node_list = f.read()
    node_list = list(ast.literal_eval(node_list))
    # ensure works w/ bad node
    node_list.append('wss://some.shitty.node/wss') 



    start = time.time()
    redundant_last = []
    for i in range(len(node_list)):
        if len(redundant_last) < 5:
            ret = 'No data from node: '
            try:
                market(node_list[i])
                ret = satoshi(dex('last'))
                redundant_last.append(ret)
            except:
                pass
            #print (ret, node_list[i])
    #print (node_list)
    #print (redundant_last)

    msg = ''
    if len(set(redundant_last)) ==1:
        last = redundant_last[0]
        msg += 'common'
    else:
        try:
            last = mode(redundant_last)
            msg += 'mode'
        except:
            last = median(redundant_last)
            msg += 'median'
    if (abs(last-redundant_last[-1])/last < 0.02) and (msg != 'common'):
        last = redundant_last[-1]
        msg = 'latest (' + msg + ')'

    # create blacklist.txt if data is spread too wide
    spread = (max(redundant_last) - min(redundant_last)) / mean(redundant_last)
    if spread > 0.02:
        print(str(last))
        print('?!? BLACKLIST - LAST ?!? ')
        print(str(redundant_last))
        print(str(node_list))
        with open('blacklist.txt', 'a+') as file:
            file.write(str(last))
            file.write('?!? BLACKLIST - LAST ?!? ')
            file.write(str(redundant_last))
            file.write(str(node_list))


    last = satoshi(last)
    elapsed = '%.1f' % (time.time()-start)
    checked = len(redundant_last)
    print (('%.8f' % last), clock(),'elapsed: ', elapsed, 
            'nodes: ', checked, 'type: ', ('%.3f' % spread), msg)

    with open('last.txt', 'w+') as file:
        file.write(str(last))

