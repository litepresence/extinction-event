# Low Latency Live Bitshares DEX Orderbooks

' (BTS) litpresence1 '

import time
from bitshares import BitShares
from bitshares.market import Market
from bitshares.account import Account
from bitshares.blockchain import Blockchain
from decimal import Decimal
from multiprocessing import Process
import numpy as np

BitPAIR = 'BTS:OPEN.BTC'

nodes = ['wss://relinked.com/ws',
        'wss://us.nodes.bitshares.ws/wss',
        'wss://la.dexnode.net/wss',
        'wss://this.uptick.rocks/ws',
        'wss://eu.openledger.info/wss',
        'wss://node.market.rudex.org/wss',
        'wss://us.nodes.bitshares.works/wss',
        'wss://eu.nodes.bitshares.ws/wss',
        'wss://slovenia.bitshares.apasia.tech/wss',
        'wss://us-east-1.bts.crypto-bridge.org/wss']

def book(node=''):

    while 1:
        time.sleep(1)
        market = Market(BitPAIR, bitshares_instance=BitShares(node), mode='head')
        call = Decimal(time.time())
        last = market.ticker()['latest']
        slast = '%.16f' % last
        elapsed = Decimal(time.time()) - call
        raw = market.orderbook(limit=40)
        bids = raw['bids']
        asks = raw['asks']
        sbidp = [('%.16f' % bids[i]['price']) for i in range(len(bids))]
        saskp = [('%.16f' % asks[i]['price']) for i in range(len(asks))]
        sbidv = [('%.2f' %float(bids[i]['quote'])).rjust(12, ' ') for i in range(len(bids))]
        saskv = [('%.2f' %float(asks[i]['quote'])).rjust(12, ' ') for i in range(len(asks))]
        bidv = [float(bids[i]['quote']) for i in range(len(bids))]
        askv = [float(asks[i]['quote']) for i in range(len(asks))]
        cbidv = list(np.cumsum(bidv))
        caskv = list(np.cumsum(askv))
        cbidv = [('%.2f' % i).rjust(12, ' ') for i in cbidv]
        caskv = [('%.2f' % i).rjust(12, ' ') for i in caskv]

        print("\033c")
        print('')
        print('litepresence - microDEX - proof of concept')
        print('')
        print(time.ctime(),)
        print('                            ',
                ('%.17f' % elapsed),'   ', node)
        print('')
        print('                        LAST',slast[:10],slast[10:],'   ',BitPAIR)
        print('')
        print('            ',sbidv[0],'  ',(sbidp[0])[:10], (sbidp[0])[10:], 
                '   ',
                (saskp[0])[:10], (saskp[0])[10:],(saskv[0]))
        print('                                           ',
              'BIDS',
              '   ',
              'ASKS')
        for i in range(1, len(sbidp)):    
            print(cbidv[i], sbidv[i],'  ',(sbidp[i])[:10], (sbidp[i])[10:], 
                    '   ',
                    (saskp[i])[:10], (saskp[i])[10:],saskv[i],caskv[i])
p={}
for n in range(len(nodes)):
    node = str(nodes[n])
    p[str(n)] = Process(target=book, args=(node,))
    p[str(n)].daemon = False
    p[str(n)].start()

