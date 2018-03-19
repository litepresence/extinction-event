# testing orderbook issues
# I'm finding moments where 

# the bid prices are higher than ask prices 
# on multiple nodes, sometimes persists for several minutes


'''
Mon Mar 19 16:51:43 2018 {'bidp': [0.12571077, 0.12569934, 0.12569762], 'askp': [0.12579997, 0.12589245, 0.12589965]} 0
Mon Mar 19 16:51:49 2018 {'bidp': [0.12571077, 0.12569934, 0.12569762], 'askp': [0.12579997, 0.12589245, 0.12589965]} 0
Mon Mar 19 16:51:56 2018 {'bidp': [0.12571077, 0.12569934, 0.12569762], 'askp': [0.12579997, 0.12589245, 0.12589965]} 0
Mon Mar 19 16:52:06 2018 {'bidp': [0.12579945, 0.12571077, 0.12569934], 'askp': [0.12579997, 0.12589245, 0.12589965]} 0
Mon Mar 19 16:52:11 2018 {'bidp': [0.12579945, 0.12571077, 0.12569934], 'askp': [0.12579997, 0.12589245, 0.12589965]} 0
Mon Mar 19 16:52:15 2018 {'bidp': [0.12579945, 0.12571077, 0.12569934], 'askp': [0.12579997, 0.12589245, 0.12589965]} 0
Mon Mar 19 16:52:18 2018 {'bidp': [0.12579945, 0.12571077, 0.12569934], 'askp': [0.12579997, 0.12589245, 0.12589965]} 0
BIDS > ASKS ???????????????????????????
wss://ap-southeast-2.bts.crypto-bridge.org/wss
Mon Mar 19 16:52:23 2018 {'bidp': [0.12658228, 0.12571077, 0.12569934], 'askp': [0.12579997, 0.12589245, 0.12589965]} 1
BIDS > ASKS ???????????????????????????
wss://ws.winex.pro/wss
Mon Mar 19 16:52:27 2018 {'bidp': [0.12658228, 0.12571077, 0.12569934], 'askp': [0.12579997, 0.12589245, 0.12589965]} 2
BIDS > ASKS ???????????????????????????
wss://sg.nodes.bitshares.ws/wss
Mon Mar 19 16:52:32 2018 {'bidp': [0.12658228, 0.12571077, 0.12569934], 'askp': [0.12579997, 0.12589245, 0.12589965]} 3
Mon Mar 19 16:52:37 2018 {'bidp': [0.125799, 0.12571077, 0.12569934], 'askp': [0.12579997, 0.12589245, 0.12589965]} 3
Mon Mar 19 16:52:42 2018 {'bidp': [0.125799, 0.12571077, 0.12569934], 'askp': [0.12579997, 0.12589245, 0.12589965]} 3


'''



# format of askp list should be ascending always
# format of bidp list should be descending always
# bids should always be less than asks

# I'm also finding times with the prices in each side are not in order

'events occur about once every 15 mintues or so'



' (BTS) litepresence1 '

# unlicensed - WTFPL v0 March 1765

import time
from bitshares import BitShares
from bitshares.market import Market

BitCURRENCY = 'USD'
BitASSET = 'BTS'
BitPAIR = BitASSET + ":" + BitCURRENCY

def satoshi(n):  
    return float('%.8f' % float(n))

def blur(n):  # FOR DEV ONLY!!!!
    return float('%.1f' % float(n))

def dex_book(node, depth=3):  # returns latest price on given market(node)

    try:
        market = Market(BitPAIR, bitshares_instance=BitShares(node, num_retries=0))
        # dictionary of 4 lists containing bid/ask volume/price
        raw = market.orderbook(limit=depth)
        bids = raw['bids']
        asks = raw['asks']
        bidp = [satoshi(bids[i]['price']) for i in range(len(bids))]
        bidv = [blur(bids[i]['quote']) for i in range(len(bids))]
        askp = [satoshi(asks[i]['price']) for i in range(len(asks))]
        askv = [blur(asks[i]['quote']) for i in range(len(asks))]
        book = {'bidp': bidp, 'bidv': bidv, 'askp': askp, 'askv': askv}

        if (sum(bidp) > sum(askp)) or (bidp[0] > askp[0]):
            print ('BIDS > ASKS ???????????????????????????')
            print (node)
            global events
            events +=1

        print (time.ctime(), book, events)
    except:
        pass



nodes = ['wss://sg.nodes.bitshares.works/wss', 'wss://bit.btsabc.org/wss', 'wss://ap-southeast-2.bts.crypto-bridge.org/wss', 'wss://ws.winex.pro/wss', 'wss://sg.nodes.bitshares.ws/wss', 'wss://ap-southeast-1.bts.crypto-bridge.org/wss', 'wss://bitshares.dacplay.org:8089/wss', 'wss://bitshares.dacplay.org/wss', 'wss://bitshares-api.wancloud.io/wss', 'wss://ws.gdex.top/wss']

events = 0

while 1:

    for node in nodes:
        dex_book(node)



