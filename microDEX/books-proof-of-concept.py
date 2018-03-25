# Minimalist Live Orderbooks for Bitshares DEX

# (BTS) litepresence1

import time
from bitshares import BitShares
from bitshares.market import Market
from bitshares.account import Account
from bitshares.blockchain import Blockchain
from decimal import Decimal

BitPAIR = 'BTS:OPEN.BTC'

n = ['wss://us.nodes.bitshares.works/wss',
     'wss://us.nodes.bitshares.ws/wss',
     'wss://eu-west-1.bts.crypto-bridge.org/wss',
     'wss://eu.nodes.bitshares.ws/wss',
     'wss://us-east-1.bts.crypto-bridge.org/wss']

market = Market(BitPAIR, bitshares_instance=BitShares(n), mode='head')


while 1:
    call = Decimal(time.time())
    last = market.ticker()['latest']
    elapsed = Decimal(time.time()) - call
    raw = market.orderbook(limit=25)
    bids = raw['bids']
    asks = raw['asks']
    sbidp = [('%.16f' % bids[i]['price']) for i in range(len(bids))]
    sbidv = [(str(bids[i]['quote'])).rjust(20, ' ') for i in range(len(bids))]
    saskp = [('%.16f' % asks[i]['price']) for i in range(len(asks))]
    saskv = [(str(asks[i]['quote'])).ljust(20, ' ') for i in range(len(asks))]
    print("\033c")
    print(BitPAIR)
    print('')
    print(last)
    print('')
    print('litepresence - microDEX - proof of concept')
    print('')
    print(time.ctime(), elapsed)
    print('')
    print((sbidv[0]), (sbidp[0])[:10], (sbidp[0])[10:], 
            '              ',
            (saskp[0])[:10], (saskp[0])[10:],(saskv[0]))
    print('')
    for i in range(1, len(sbidp)):    
        print((sbidv[i]), (sbidp[i])[:10], (sbidp[i])[10:], 
                '              ',
                (saskp[i])[:10], (saskp[i])[10:],(saskv[i]))
