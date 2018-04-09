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
from ast import literal_eval as literal
import time


ACCOUNT = Account("")
PASS_PHRASE = ""
BitCURRENCY = 'OPEN.BTC'
BitASSET = 'BTS'
BitPAIR = BitASSET + ":" + BitCURRENCY


SATOSHI = 0.00000001
ANTISAT = 1 / SATOSHI

def nodes():  # Public Nodes List

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
    return literal(node_list)

def dex(  # Public AND Private API Bitshares
        command, amount=ANTISAT, price=None,
        depth=1, expiration=ANTISAT):

    MARKET = Market(BitPAIR, bitshares_instance=BitShares(nodes(), num_retries=0))
    CHAIN = Blockchain(bitshares_instance=BitShares(nodes(), num_retries=0), mode='head')
    #MARKET.bitshares.wallet.unlock(PASS_PHRASE)
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

        servers = nodes()
        orders_list =[]
        satisfied = 0
        while not satisfied: #while len set triplicate
            for n in servers:
                sorders = [str(i) for i in orders_list]
                if (len(sorders) >= 3) and len(set(sorders[-3:])) == 1:
                    orders = orders_list[-1]
                    satisfied = 1
                else:
                    MARKET = Market(BitPAIR, bitshares_instance=BitShares(n, num_retries=0))
                    MARKET.bitshares.wallet.unlock(PASS_PHRASE)
                    ACCOUNT.refresh()

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
                    orders_list.append(orders)


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

        try:
            opened = 0
            while not opened:
                with open('book.txt', 'r') as f:
                    book = f.read()
                    opened = 1
        except Exception as e:
            print (e)
            print ('book.txt failed, try again...')
            pass
        return literal(book)

    if command == 'last':

        try:
            opened = 0
            while not opened:
                with open('last.txt', 'r') as f:
                    last = f.read()
                    opened = 1
        except Exception as e:
            print (e)
            print ('last.txt failed, try again...')
            pass
        return literal(last)

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

while 1:
    print(dex('last'))
    print(dex('book'))
    print('')
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
