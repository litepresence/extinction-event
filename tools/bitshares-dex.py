# python3.4

' Wrapper for Common PyBitshares DEX Algo Trading API Calls '

# data is in easy to quant float / list of floats / dict of floats format

    # buy / sell / cancel
    # outstanding orders 
    # account balance for pair 
    # complete account balance
    # orderbook 
    # last_price
    # account value
    # latency

# if no price / amount specified executes market order buy/sell
# if no expiration specified default is 3.2 years
# cancels all outstanding orders in market

' BTS: litepresence1 '

# http://docs.pybitshares.com
from bitshares.market import Market
from bitshares.account import Account
from bitshares import BitShares
from bitshares.blockchain import Blockchain
import time


ACCOUNT = Account("")
PASS_PHRASE = ""

BitCURRENCY = 'OPEN.BTC'
BitASSET = 'BTS'
BitPAIR = BitASSET + ":" + BitCURRENCY
MARKET = Market(BitPAIR, bitshares_instance=BitShares(nodes()))
CHAIN = Blockchain(bitshares_instance=BitShares(
    nodes()), mode='head')

SATOSHI = 0.00000001
ANTISAT = 1 / SATOSHI

def nodes():  # Public Nodes List

    nodes = [
        'wss://b.mrx.im/ws',
        'wss://bitshares.openledger.info/ws',
        'wss://bitshares.dacplay.org:8089/ws',
        'wss://dele-puppy.com/ws',
        'wss://eu.openledger.info/ws',
        'wss://bit.btsabc.org/ws',
        'wss://eu.openledger.info/ws',
        'wss://dexnode.net/ws',
        'wss://ws.gdex.top',
        'wss://kc-us-dex.xeldal.com/ws',
        'wss://bts.ai.la/ws',
        'wss://btsza.co.za:8091/ws',
        'wss://japan.bitshares.apasia.tech/ws',
        'wss://api.bts.blckchnd.com',
        'wss://bitshares-api.wancloud.io/ws',
        'wss://eu.nodes.bitshares.ws',
        'wss://bitshares.crypto.fans/ws',
        'wss://dex.rnglab.org',
        'wss://bitshares.openledger.info/ws',
        'wss://ws.winex.pro',
        'wss://sg.nodes.bitshares.ws',
        'wss://us.nodes.bitshares.ws',
        'wss://bitshares.apasia.tech/ws',
        'wss://openledger.hk/ws',
        'wss://bitshares.dacplay.org/ws',
    ]
    return nodes

def dex(  # Public AND Private API Bitshares
        command, amount=ANTISAT, price=None,
        depth=1, expiration=ANTISAT):

    MARKET.bitshares.wallet.unlock(PASS_PHRASE)
    ACCOUNT.refresh()

    if command == 'buy':

        # buy relentlessly until satisfied or currency exhausted
        print(('Bitshares API', command))
        if price is None:
            price = ANTISAT
        print(('buying', amount, 'at', price))
        attempt = 1
        currency = float(ACCOUNT.balance(BitCURRENCY))
        if amount > 0.998 * currency * price:
            amount = 0.998 * currency * price
        if amount > 0:
            while attempt:
                try:
                    details = (MARKET.buy(price, amount, expiration))
                    print (details)
                    attempt = 0
                except:
                    print(("buy attempt %s failed" % attempt))
                    attempt += 1
                    if attempt > 10:
                        print ('buy aborted')
                        return
                    pass
        else:
            print('no currency to buy')

    if command == 'sell':

        # sell relentlessly until satisfied or assets exhausted
        expiration = 86400 * 7
        print(('Bitshares API', command))
        if price is None:
            price = SATOSHI
        print(('selling', amount, 'at', price))
        attempt = 1
        assets = float(ACCOUNT.balance(BitASSET))
        if amount > 0.998 * assets:
            amount = 0.998 * assets
        if amount > 0:
            while attempt:
                try:
                    details = (MARKET.sell(price, amount, expiration))
                    print (details)
                    attempt = 0
                except:
                    print(("sell attempt %s failed" % attempt))
                    attempt += 1
                    if attempt > 10:
                        print ('sell aborted')
                        return
                    pass
        else:
            print('no assets to sell')

    if command == 'cancel':

        # cancel all orders in this MARKET relentlessly until satisfied
        print(('Bitshares API', command))  
        orders = MARKET.accountopenorders()
        print((len(orders), 'open orders to cancel'))
        if len(orders):
            attempt = 1   
            order_list = []      
            for order in orders:
                order_list.append(order['id'])
            while attempt:
                try:
                    details = MARKET.cancel(order_list)
                    print (details)
                    attempt = 0
                except:
                    print((attempt, 'cancel failed', order_list))
                    attempt += 1
                    if attempt > 10:
                        print ('cancel aborted')
                        return
                    pass    

    if command == 'orders':

        # dictionary of open orders in traditional format:
        # orderNumber, orderType, market, amount, price
        print(('Bitshares API', command))
        orders = []
        for order in MARKET.accountopenorders():
            orderNumber = order['id']
            asset = order['base']['symbol']
            currency = order['quote']['symbol']
            amount = float(order['base'])
            price = float(order['price'])
            orderType = 'buy'
            if asset == BitASSET:
                orderType = 'sell'
                price = 1 / price
            orders.append({'orderNumber': orderNumber,
                           'orderType': orderType,
                           'market': BitPAIR, 'amount': amount,
                           'price': price})
        for o in orders:
            print (o)
        if len(orders) == 0:
            print ('no open orders')
        return orders

    if command == 'market_balances':

        # dictionary of currency and assets in this MARKET
        print(('Bitshares API', command))
        currency = float(ACCOUNT.balance(BitCURRENCY))
        assets = float(ACCOUNT.balance(BitASSET))
        balances = {'currency': currency, 'assets': assets}
        print (balances)
        return balances

    if command == 'complete_balances':

        # dictionary of ALL account balances
        print(('Bitshares API', command))
        raw = list(ACCOUNT.balances)
        balances = {}
        for i in range(len(raw)):
            balances[raw[i]['symbol']] = float(raw[i]['amount'])
        print (balances)
        return balances

    if command == 'book':

        # dictionary of 4 lists containing bid/ask volume/price
        print(('Bitshares API', command))
        raw = MARKET.orderbook(limit=depth)
        bids = raw['bids']
        asks = raw['asks']
        bidp = [float(bids[i]['price']) for i in range(len(bids))]
        bidv = [float(bids[i]['quote']) for i in range(len(bids))]
        askp = [float(asks[i]['price']) for i in range(len(asks))]
        askv = [float(asks[i]['quote']) for i in range(len(asks))]
        book = {'bidp': bidp, 'bidv': bidv, 'askp': askp, 'askv': askv}
        # print(book)
        print(('ask', ('%.8f' % book['askp'][0])))  # lowest ask price
        print(('bid', ('%.8f' % book['bidp'][0])))  # highest bid price
        # print(book['bidv'][0]) #highest bid volume
        # print(book['askv'][0]) #lowest ask volume
        return book

    if command == 'last':

        # the most recent transation in this MARKET
        print(('Bitshares API', command))
        raw = MARKET.ticker()['latest']
        price = float(raw)
        # print (price)
        return price

    if command == 'account_value':

        # dictionary account value in BTS BTC and USD
        print(('Bitshares API', command))
        raw = list(ACCOUNT.balances)
        balances = {}
        for i in range(len(raw)):
            balances[raw[i]['symbol']] = float(raw[i]['amount'])
        btc_value = 0
        for asset, amount in list(balances.items()):
            market_pair = 'OPEN.BTC:' + asset
            market = Market(market_pair)
            price = float(market.ticker()['latest'])
            try:
                value = amount / price
            except:
                value = 0
            if value < 0.0001:
                value = 0
            else:
                if asset != 'USD':
                    price = 1 / (price + SATOSHI)
                print((('%.4f' % value), 'OPEN.BTC', ('%.2f' % amount),
                       asset, '@', ('%.8f' % price)))
                btc_value += value

        market_pair = 'OPEN.BTC:USD'
        market = Market(market_pair)
        price = float(market.ticker()['latest'])
        usd_value = btc_value * price
        market_pair = 'OPEN.BTC:BTS'
        market = Market(market_pair)
        price = float(market.ticker()['latest'])
        bts_value = btc_value * price
        print((('%.2f' % bts_value), 'BTS',
             ('%.4f' % btc_value), 'OPEN.BTC',
             ('%.2f' % usd_value), 'bitUSD'))
        return bts_value, btc_value, usd_value

    if command == 'blocktime':

        current_block = CHAIN.get_current_block_num()
        blocktime = CHAIN.block_time(current_block)
        blocktimestamp = CHAIN.block_timestamp(current_block) - 18000
        now = time.time()
        latency = now - blocktimestamp
        print(('block               :', current_block))
        # print(('blocktime           :', blocktime))
        # print(('stamp               :', blocktimestamp))
        # print(('ctime(stamp)        :', time.ctime(blocktimestamp)))
        # print(('now                 :', now))
        print(('dex_rate latency    :', ('%.2f' % latency)))
        return current_block, blocktimestamp, latency



'''
dex('buy')
dex('sell')
dex('orders')
dex('cancel')
dex('market_balances')
dex('complete_balances')
dex('last')
dex('book')
dex('account_value')
dex('blocktime')
'''
