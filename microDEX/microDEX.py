
# microDEX v0.00000001  - low latency minimalist UI

' (BTS) litpresence1'

import time
from bitsharesbase import account
from bitshares import BitShares
from bitshares.market import Market
from bitshares.account import Account
from bitshares.blockchain import Blockchain
from bitshares.wallet import Wallet
from decimal import Decimal
from random import shuffle
from multiprocessing import Process, active_children
import numpy as np
from getpass import getpass
from tkinter import *
SATOSHI = 0.00000001
ANTISAT = 1 / SATOSHI
from decimal import Decimal as decimal
import datetime
from bitshares.utils import *

nodes = ['wss://relinked.com/ws', 'wss://dexnode.net/wss', 'wss://la.dexnode.net/wss', 'wss://api.bts.blckchnd.com/wss', 'wss://eu.openledger.info/wss', 'wss://us.nodes.bitshares.ws/wss', 'wss://us.nodes.bitshares.works/wss', 'wss://this.uptick.rocks/ws', 'wss://bitshares.nu/wss', 'wss://eu.nodes.bitshares.works/wss']
BitCURRENCY = 'OPEN.BTC'
BitASSET = 'BTS'

def launch():

    nodes = ['wss://relinked.com/ws', 'wss://dexnode.net/wss', 'wss://la.dexnode.net/wss', 'wss://api.bts.blckchnd.com/wss', 'wss://eu.openledger.info/wss', 'wss://us.nodes.bitshares.ws/wss', 'wss://us.nodes.bitshares.works/wss', 'wss://this.uptick.rocks/ws', 'wss://bitshares.nu/wss', 'wss://eu.nodes.bitshares.works/wss']
    p={}
    n=1
    while 1:
        shuffle(nodes)
        node = str(nodes[0])
        p[str(n)] = Process(target=book, args=(node,n))
        p[str(n)].daemon = False
        p[str(n)].start()
        n+=1
        if n > 8: time.sleep(15)

def book(node='',n=''):

    now = begin = time.time()
    while now < (begin + 60):
        try:
            now = time.time()
            # update data fields
            time.sleep(1)
            ACCOUNT.refresh()
            market = Market(BitPAIR,
                bitshares_instance=BitShares(node, num_retries=0),
                    mode='head')
            trades = market.trades(limit=10)
            # last price
            call = Decimal(time.time())
            last = market.ticker()['latest']
            slast = '%.16f' % last
            elapsed = Decimal(time.time()) - call
            # orderbook
            raw = market.orderbook(limit=20)
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
            # dictionary of currency and assets in this MARKET
            currency = float(ACCOUNT.balance(BitCURRENCY))
            assets = float(ACCOUNT.balance(BitASSET))
            balances = {'currency': currency, 'assets': assets}
            # dictionary of open orders in traditional format:
            # orderNumber, orderType, market, amount, price
            orders = []
            for order in market.accountopenorders():
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
                               'market': BitPAIR,
                               'amount': amount,
                               'price': ('%.16f' % price)})

            # display orderbooks
            print("\033c")
            print(time.ctime(),'   ',int(time.time()))
            print('                            ',
                    ('%.17f' % elapsed),'   ', n, node)
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
            print('')
            for o in orders:
                print (o)
            if len(orders) == 0:
                print ('                                  NO OPEN ORDERS')
            print('')
            print (balances)
            print('')
            for t in trades:
                print(t)
        except:
            pass


def dex_withdraw():

    from bitshares import BitShares
    bitshares = BitShares()
    bitshares.wallet.unlock("wallet-passphrase")
    bitshares.transfer("<to>", "<amount>", "<asset>", "[<memo>]", account="<from>")

def dex_buy():

    def buy():

        confirm.destroy()
        if MARKET.bitshares.wallet.unlocked():
            price = decimal(buy_price.get())
            amount = decimal(buy_amount.get())
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
                        details = (MARKET.buy(price, amount))
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
            print('YOUR WALLET IS LOCKED')

    confirm = Tk()
    confirm.title("CONFIRM SELL TRANSACTION")
    Button(confirm, text='CONFIRM', command=buy).grid(row=0, column=0, sticky=W, pady=4)
    Button(confirm, text='CANCEL', command=confirm.destroy).grid(row=2, column=0, sticky=W, pady=4)
    confirm.lift()
    confirm.call('wm', 'attributes', '.', '-topmost', True)

def dex_sell():

    def sell():

        confirm.destroy()
        if MARKET.bitshares.wallet.unlocked():
            price = decimal(sell_price.get())
            amount = decimal(sell_amount.get())
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
                        details = (MARKET.sell(price, amount))
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
        else:
            print('YOUR WALLET IS LOCKED')

    confirm = Tk()
    confirm.title("CONFIRM SELL TRANSACTION")
    Button(confirm, text='CONFIRM', command=sell).grid(row=0, column=0, sticky=W, pady=4)
    Button(confirm, text='CANCEL', command=confirm.destroy).grid(row=2, column=0, sticky=W, pady=4)
    confirm.lift()
    confirm.call('wm', 'attributes', '.', '-topmost', True)


def dex_cancel():

    def cancel():
        confirm.destroy()
        if MARKET.bitshares.wallet.unlocked():
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
        else:
            print('YOUR WALLET IS LOCKED')

    confirm = Tk()
    confirm.title("CONFIRM SELL TRANSACTION")
    Button(confirm, text='CONFIRM', command=cancel).grid(row=0, column=0, sticky=W, pady=4)
    Button(confirm, text='CANCEL', command=confirm.destroy).grid(row=2, column=0, sticky=W, pady=4)
    confirm.lift()
    confirm.call('wm', 'attributes', '.', '-topmost', True)

def dex_auth_gui():
    global MARKET
    try:
        MARKET.bitshares.wallet.unlock(str(login.get()))
        lock.set('UNLOCKED')
    except Exception as ex:
        print (type(ex).__name__)
        MARKET.bitshares.wallet.lock()
        lock.set('LOCKED')
        pass

# sign in
BitPAIR = BitASSET + ':' + BitCURRENCY
MARKET = Market(BitPAIR, bitshares_instance=BitShares(nodes), mode='head')
ACCOUNT = Account(input('           account: '))
AUTH = input('Unlock Wallet? Y/N: ')
if AUTH.lower() == 'y':
    PASS_PHRASE = getpass(prompt='       pass phrase: ')
    try:
        MARKET.bitshares.wallet.unlock(PASS_PHRASE)
    except Exception as ex:
        print (type(ex).__name__)
        sys.exit()
print('')
print('Connecting to DEX, please wait...')
print('')

# multinode orderbooks
l = Process(target=launch)
l.start()

# busybox
master = Tk()
lock = StringVar()
lock.set('UNLOCKED')
if MARKET.bitshares.wallet.locked():
    lock.set('LOCKED')
master.title("microDEX: low latency minimalist UI")
Label(master, text="PRICE  :").grid(row=0,column=0)
Label(master, text="AMOUNT :").grid(row=1,column=0)
Label(master, text="PRICE  :").grid(row=0,column=2)
Label(master, text="AMOUNT :").grid(row=1,column=2)
Label(master, text="LOGIN  :").grid(row=6,column=0)
Label(master, textvariable=lock).grid(row=6,column=3)
buy_price = Entry(master)
buy_amount = Entry(master)
sell_price = Entry(master)
sell_amount = Entry(master)
login = Entry(master)
buy_price.grid(    row=0, column=1)
buy_amount.grid(   row=1, column=1)
sell_price.grid(   row=0, column=3)
sell_amount.grid(  row=1, column=3)
login.grid(        row=6,column=1)
Button(master, text='BUY', command=dex_buy              ).grid(row=3, column=1, sticky=W, pady=4)
Button(master, text='SELL', command=dex_sell            ).grid(row=3, column=3, sticky=W, pady=4)
Button(master, text='CANCEL ALL', command=dex_cancel    ).grid(row=5, column=0, sticky=W, pady=4)
Button(master, text='LOCK/UNLOCK', command=dex_auth_gui ).grid(row=6, column=2, sticky=W, pady=4)
master.lift()
master.call('wm', 'attributes', '.', '-topmost', True)
mainloop( )
