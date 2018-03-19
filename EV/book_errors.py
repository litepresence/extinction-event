# testing orderbook issues
# I'm finding moments where 

# the bid prices are higher than ask prices 
# on multiple nodes

'''MINIMAL REPRODUCABLE CODE FOLLOWS'''


'''
Mon Mar 19 16:27:13 2018 {'askp': [0.12439796, 0.12439946], 'askv': [430.8, 438.4], 'bidv': [20.2, 19.5], 'bidp': [0.12439671, 0.12439628]} 0
Mon Mar 19 16:27:17 2018 {'askp': [0.12439796, 0.12439946], 'askv': [430.8, 438.4], 'bidv': [20.2, 19.5], 'bidp': [0.12439671, 0.12439628]} 0
Mon Mar 19 16:27:21 2018 {'askp': [0.12439796, 0.12439946], 'askv': [430.8, 438.4], 'bidv': [20.2, 19.5], 'bidp': [0.12439671, 0.12439628]} 0
Mon Mar 19 16:27:26 2018 {'askp': [0.12439796, 0.12439946], 'askv': [430.8, 438.4], 'bidv': [20.2, 19.5], 'bidp': [0.12439671, 0.12439628]} 0
Mon Mar 19 16:27:32 2018 {'askp': [0.12439796, 0.12439946], 'askv': [430.8, 438.4], 'bidv': [20.2, 19.5], 'bidp': [0.12439671, 0.12439628]} 0
BIDS > ASKS ???????????????????????????
wss://bitshares-api.wancloud.io/wss
Mon Mar 19 16:27:38 2018 {'askp': [0.12439796, 0.12439946], 'askv': [430.8, 438.4], 'bidv': [0.0, 19.5], 'bidp': [0.125, 0.12439628]} 1
BIDS > ASKS ???????????????????????????
wss://ws.gdex.top/wss
Mon Mar 19 16:27:43 2018 {'askp': [0.12439796, 0.12439946], 'askv': [430.8, 438.4], 'bidv': [0.0, 19.5], 'bidp': [0.125, 0.12439628]} 2
BIDS > ASKS ???????????????????????????
wss://sg.nodes.bitshares.works/wss
Mon Mar 19 16:27:47 2018 {'askp': [0.12439796, 0.12439946], 'askv': [430.8, 438.4], 'bidv': [25.4, 0.0], 'bidp': [0.12439709, 0.125]} 3
Mon Mar 19 16:27:50 2018 {'askp': [0.12439663, 0.12439796], 'askv': [135.6, 430.8], 'bidv': [19.5, 22.3], 'bidp': [0.12439628, 0.12439606]} 3
Mon Mar 19 16:27:55 2018 {'askp': [0.12439663, 0.12439946], 'askv': [135.6, 438.4], 'bidv': [16.4, 22.3], 'bidp': [0.12439608, 0.12439542]} 3
Mon Mar 19 16:28:01 2018 {'askp': [0.12439663, 0.12439946], 'askv': [135.6, 438.4], 'bidv': [16.4, 22.3], 'bidp': [0.12439608, 0.12439542]} 3
Mon Mar 19 16:28:05 2018 {'askp': [0.12439515, 0.12439663], 'askv': [430.8, 135.6], 'bidv': [22.3, 2840.8], 'bidp': [0.12439421, 0.1238]} 3

'''



'''
Mon Mar 19 16:36:43 2018 {'askp': [0.1246389, 0.1246427], 'askv': [43.6, 212.8], 'bidv': [31.8, 438.9], 'bidp': [0.12463814, 0.12439508]} 3
Mon Mar 19 16:36:48 2018 {'askp': [0.12470312, 0.12479997], 'askv': [160.0, 40.0], 'bidv': [39.0, 31.8], 'bidp': [0.12470313, 0.12463814]} 3
Mon Mar 19 16:36:53 2018 {'askp': [0.12464269, 0.12469997], 'askv': [162.1, 40.0], 'bidv': [31.8, 438.9], 'bidp': [0.12463814, 0.12439508]} 3
Mon Mar 19 16:36:59 2018 {'askp': [0.12470306, 0.12479997], 'askv': [10.4, 40.0], 'bidv': [31.8, 438.9], 'bidp': [0.12463814, 0.12439508]} 3
BIDS > ASKS ???????????????????????????
wss://ap-southeast-2.bts.crypto-bridge.org/wss
Mon Mar 19 16:37:04 2018 {'askp': [0.1242236, 0.12479997], 'askv': [0.0, 40.0], 'bidv': [31.8, 31.8], 'bidp': [0.12463978, 0.12463814]} 4
BIDS > ASKS ???????????????????????????
wss://ws.winex.pro/wss
Mon Mar 19 16:37:09 2018 {'askp': [0.1242236, 0.12479997], 'askv': [0.0, 40.0], 'bidv': [31.8, 31.8], 'bidp': [0.12463978, 0.12463814]} 5
BIDS > ASKS ???????????????????????????
wss://sg.nodes.bitshares.ws/wss
Mon Mar 19 16:37:15 2018 {'askp': [0.1242236, 0.12479997], 'askv': [0.0, 40.0], 'bidv': [31.8, 31.8], 'bidp': [0.12463978, 0.12463814]} 6
BIDS > ASKS ???????????????????????????
wss://ap-southeast-1.bts.crypto-bridge.org/wss
Mon Mar 19 16:37:22 2018 {'askp': [0.1242236, 0.12479997], 'askv': [0.0, 40.0], 'bidv': [31.8, 31.8], 'bidp': [0.12463978, 0.12463814]} 7
BIDS > ASKS ???????????????????????????
wss://bitshares.dacplay.org:8089/wss
Mon Mar 19 16:37:29 2018 {'askp': [0.1242236, 0.12479997], 'askv': [0.0, 40.0], 'bidv': [31.8, 31.8], 'bidp': [0.12463978, 0.12463814]} 8
Mon Mar 19 16:37:37 2018 {'askp': [0.12479997, 0.12489997], 'askv': [40.0, 40.0], 'bidv': [31.8, 31.8], 'bidp': [0.12479847, 0.12463978]} 8
Mon Mar 19 16:38:18 2018 {'askp': [0.12495459, 0.12499997], 'askv': [317.9, 40.0], 'bidv': [15.9, 31.8], 'bidp': [0.12495178, 0.12479847]} 8
Mon Mar 19 16:38:26 2018 {'askp': [0.12495459, 0.12499997], 'askv': [317.9, 40.0], 'bidv': [15.9, 31.8], 'bidp': [0.12495178, 0.12479847]} 8


'''


'''
BIDS > ASKS ???????????????????????????
wss://bit.btsabc.org/wss
Mon Mar 19 16:42:37 2018 {'askp': [0.12551, 0.12557921], 'askv': [1837.5, 457.0], 'bidv': [0.0, 42.0], 'bidp': [0.12658228, 0.12532597]} 14
BIDS > ASKS ???????????????????????????
wss://ap-southeast-2.bts.crypto-bridge.org/wss
Mon Mar 19 16:42:42 2018 {'askp': [0.12550999, 0.12557921], 'askv': [716.8, 457.0], 'bidv': [0.0, 42.0], 'bidp': [0.12658228, 0.12532597]} 15
BIDS > ASKS ???????????????????????????
wss://ws.winex.pro/wss
Mon Mar 19 16:42:46 2018 {'askp': [0.12557764, 0.12557921], 'askv': [435.1, 400.3], 'bidv': [0.0, 42.0], 'bidp': [0.12658228, 0.12532597]} 16
BIDS > ASKS ???????????????????????????
wss://sg.nodes.bitshares.ws/wss
Mon Mar 19 16:42:51 2018 {'askp': [0.12557764, 0.12557921], 'askv': [435.1, 400.3], 'bidv': [42.0, 0.0], 'bidp': [0.12557746, 0.12658228]} 17
BIDS > ASKS ???????????????????????????
wss://ap-southeast-1.bts.crypto-bridge.org/wss
Mon Mar 19 16:42:55 2018 {'askp': [0.12557764, 0.12557921], 'askv': [435.1, 400.3], 'bidv': [42.0, 0.0], 'bidp': [0.12557746, 0.12658228]} 18
BIDS > ASKS ???????????????????????????
wss://bitshares.dacplay.org:8089/wss
Mon Mar 19 16:43:01 2018 {'askp': [0.12557764, 0.12557921], 'askv': [435.1, 400.3], 'bidv': [42.0, 0.0], 'bidp': [0.12557746, 0.12658228]} 19
BIDS > ASKS ???????????????????????????
wss://bitshares.dacplay.org/wss
Mon Mar 19 16:43:06 2018 {'askp': [0.12557764, 0.12557921], 'askv': [435.1, 400.3], 'bidv': [42.0, 0.0], 'bidp': [0.12557746, 0.12658228]} 20
BIDS > ASKS ???????????????????????????
wss://bitshares-api.wancloud.io/wss
Mon Mar 19 16:43:14 2018 {'askp': [0.12557764, 0.12557921], 'askv': [435.1, 400.3], 'bidv': [0.0, 0.0], 'bidp': [0.12658228, 0.12658228]} 21
BIDS > ASKS ???????????????????????????
wss://ws.gdex.top/wss
Mon Mar 19 16:43:20 2018 {'askp': [0.12557764, 0.12557921], 'askv': [435.1, 400.3], 'bidv': [0.0, 0.0], 'bidp': [0.12658228, 0.12658228]} 22
BIDS > ASKS ???????????????????????????
wss://sg.nodes.bitshares.works/wss
Mon Mar 19 16:43:26 2018 {'askp': [0.12557764, 0.12557921], 'askv': [435.1, 400.3], 'bidv': [0.0, 42.0], 'bidp': [0.12658228, 0.12557605]} 23
BIDS > ASKS ???????????????????????????
wss://bit.btsabc.org/wss
Mon Mar 19 16:43:30 2018 {'askp': [0.12557764, 0.12557921], 'askv': [435.1, 400.3], 'bidv': [0.0, 42.0], 'bidp': [0.12658228, 0.12557605]} 24
BIDS > ASKS ???????????????????????????
wss://ap-southeast-2.bts.crypto-bridge.org/wss
Mon Mar 19 16:43:36 2018 {'askp': [0.12557764, 0.12557921], 'askv': [409.0, 400.3], 'bidv': [0.0, 42.0], 'bidp': [0.12658228, 0.12557605]} 25
BIDS > ASKS ???????????????????????????
wss://ws.winex.pro/wss
Mon Mar 19 16:43:44 2018 {'askp': [0.12557764, 0.12557921], 'askv': [409.0, 400.3], 'bidv': [0.0, 42.0], 'bidp': [0.12658228, 0.12557605]} 26
BIDS > ASKS ???????????????????????????
wss://sg.nodes.bitshares.ws/wss
Mon Mar 19 16:43:49 2018 {'askp': [0.12557764, 0.12557921], 'askv': [409.0, 400.3], 'bidv': [0.0, 42.0], 'bidp': [0.12658228, 0.12557605]} 27
BIDS > ASKS ???????????????????????????
wss://ap-southeast-1.bts.crypto-bridge.org/wss
Mon Mar 19 16:43:54 2018 {'askp': [0.12557764, 0.12557921], 'askv': [409.0, 400.3], 'bidv': [0.0, 42.0], 'bidp': [0.12658228, 0.12557605]} 28
BIDS > ASKS ???????????????????????????
wss://bitshares.dacplay.org:8089/wss
Mon Mar 19 16:44:00 2018 {'askp': [0.12557763, 0.12557921], 'askv': [408.6, 400.3], 'bidv': [0.0, 42.0], 'bidp': [0.12658228, 0.1255762]} 29

'''


# format of askp list should be ascending always
# format of bidp list should be descending always
# bids should always be less than asks

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

def blur(n):  
    return float('%.1f' % float(n))

def dex_book(node, depth=2):  # returns latest price on given market(node)

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

        if sum(bidp) > sum(askp):
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



