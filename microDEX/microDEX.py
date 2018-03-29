
VERSION = 'microDEX v0.00000004 - low latency minimalist UI'

' (BTS) litpresence1 '

import sys
import time
import datetime
import numpy as np
from tkinter import *
from random import shuffle
from getpass import getpass
from ast import literal_eval as literal
from bitshares.utils import *
from dateutil.parser import parser
from decimal import Decimal as decimal
from multiprocessing import Process, active_children

from bitsharesbase import account
from bitshares import BitShares
from bitshares.market import Market
from bitshares.account import Account
from bitshares.blockchain import Blockchain
from bitshares.wallet import Wallet

SATOSHI = 0.00000001
ANTISAT = 1 / SATOSHI
sys.stdout.write('\x1b]2;' + VERSION + '\x07')

nodes = [
    'wss://relinked.com/ws',
    'wss://dexnode.net/wss',
    'wss://la.dexnode.net/wss',
    'wss://api.bts.blckchnd.com/wss',
    'wss://eu.openledger.info/wss',
    'wss://us.nodes.bitshares.ws/wss',
    'wss://us.nodes.bitshares.works/wss',
    'wss://this.uptick.rocks/ws',
    'wss://bitshares.nu/wss',
    'wss://eu.nodes.bitshares.works/wss']

BitCURRENCY = 'OPEN.BTC'
BitASSET = 'BTS'
TIMEOUT = 60

from multiprocessing import Process, Value, Array
from bitshares.blockchain import Blockchain
from bitshares import BitShares
from datetime import datetime
import requests
import time
import sys
import os

ID = '4018d7844c78f6a6c41c6a552b898022310fc5dec06da467ee7905a8dad512c8'


def nodes_process(
    timeout=20, pings=999999, crop=99, noprint=False, write=False,
        include=False, exclude=False, suffix=True, master=False):

    # timeout : seconds to ping until abort per node
    # pings   : number of good nodes to find until satisfied (0 none, 999 all)
    # suffix  : checks each node for no suffix plus with /ws or /wss
    # noprint : disables printing, only returns list of good nodes
    # master  : check only nodes listed in bitshares/ui/master
    # crop    : return only best nodes
    # write   : maintains an output file nodes.txt with list of best nodes

    # include and exclude custom nodes
    included, excluded = [], []
    if include:
        included = ['wss://bts-seoul.clockwork.gr']

    if exclude:
        excluded = []

    # web scraping methods
    def clean(raw):
        return ((str(raw).replace('"', " "))
                .replace("'", " ")).replace(',', ' ')

    def parse(cleaned):
        return [t for t in cleaned.split() if t.startswith('wss')]

    def validate(parsed):
        v = parsed
        for i in range(len(v)):
            if v[i].endswith('/'):
                v[i] = v[i][:-1]
        for i in range(len(v)):
            if v[i].endswith('/ws'):
                v[i] = v[i][:-3]
        for i in range(len(v)):
            if v[i].endswith('/wss'):
                v[i] = v[i][:-4]
        # these are known to require /ws extension
        ws = ['wss://relinked.com',
              'wss://bitshares.crypto.fans',
              'wss://this.uptick.rocks']
        if suffix:
            wss = [(i + '/wss') for i in v]
            ws = [(i + '/ws') for i in v]
            v = v + wss + ws
        else:
            for i in range(len(v)):
                if v[i] in ws:
                    v[i] += '/ws'
                else:
                    v[i] += '/wss'
        return v

    # ping the blockchain and return latency

    def ping(n, num, arr):

        try:
            start = time.time()
            chain = Blockchain(
                bitshares_instance=BitShares(n, num_retries=0), mode='head')

            # print(n,chain.rpc.chain_params["chain_id"])
            ping_latency = time.time() - start
            current_block = chain.get_current_block_num()
            blocktimestamp = abs(
                chain.block_timestamp(current_block))  # + utc_offset)
            block_latency = time.time() - blocktimestamp
            # print (blocktimestamp)
            # print (time.time())
            # print (block_latency)
            # print (ping_latency)
            # print (time.ctime())
            # print (utc_offset)
            # print (chain.get_network())
            if chain.get_network()['chain_id'] != ID:
                num.value = 333333
            elif block_latency < (ping_latency + 4):
                num.value = ping_latency
            else:
                num.value = 111111
        except:
            num.value = 222222
            pass

    # Disable / Enable printing
    def blockPrint():
        if noprint:
            sys.stdout = open(os.devnull, 'w')

    def enablePrint():
        if noprint:
            sys.stdout = sys.__stdout__

    # gather list of nodes from github
    blockPrint()
    begin = time.time()
    utc_offset = (datetime.fromtimestamp(begin) -
                  datetime.utcfromtimestamp(begin)).total_seconds()
    print ('=====================================')
    print(('found %s nodes stored in script' % len(included)))
    urls = []
    # scrape from github
    git = 'https://raw.githubusercontent.com'
    url = git + '/bitshares/bitshares-ui/master/app/api/apiConfig.js'
    urls.append(url)
    if not master:
        url = git + '/bitshares/bitshares-ui/staging/app/api/apiConfig.js'
        urls.append(url)
        url = git + '/CryptoBridge/cryptobridge-ui/'
        url += 'e5214ad63a41bd6de1333fd98d717b37e1a52f77/app/api/apiConfig.js'
        urls.append(url)
        url = git + '/litepresence/extinction-event/master/bitshares-nodes.py'
        urls.append(url)

    # searched selected sites for Bitshares nodes
    validated = [] + included
    for u in urls:
        attempts = 3
        while attempts > 0:
            try:
                raw = requests.get(u).text
                v = validate(parse(clean(raw)))
                print(('found %s nodes at %s' % (len(v), u[:65])))
                validated += v
                attempts = 0
            except:
                print(('failed to connect to %s' % u))
                attempts -= 1
                pass

    # remove known bad nodes from test
    if len(excluded):
        excluded = sorted(excluded)
        print(('remove %s known bad nodes' % len(excluded)))
        validated = [i for i in validated if i not in excluded]

    validated = sorted(list(set(validate(parse(clean(validated))))))

    # attempt to contact each websocket
    print ('=====================================')
    print(('found %s total nodes - no duplicates' % len(validated)))
    print ('=====================================')
    print (validated)
    pinging = min(pings, len(validated))
    if pinging:
        print ('=====================================')
        enablePrint()
        # print(('%s pinging %s nodes; timeout %s sec; est %.1f minutes' % (
        #    time.ctime(), pinging, timeout, timeout * len(validated) / 60.0)))
        blockPrint()
        print ('=====================================')
        pinged, timed, down, stale, expired, testnet = [], [], [], [], [], []
        for n in validated:
            if len(pinged) < pinging:
                # use multiprocessing module to enforce timeout
                num = Value('d', 999999)
                arr = Array('i', list(range(0)))
                p = Process(target=ping, args=(n, num, arr))
                p.start()
                p.join(timeout)
                if p.is_alive() or (num.value > timeout):
                    p.terminate()
                    p.join()
                    if num.value == 111111:  # head block is stale
                        stale.append(n)
                    elif num.value == 222222:  # connect failed
                        down.append(n)
                    elif num.value == 333333:  # connect failed
                        testnet.append(n)
                    elif num.value == 999999:  # timeout reached
                        expired.append(n)
                else:
                    pinged.append(n)        # connect success
                    timed.append(num.value)  # connect success time
                print(('ping:', ('%.2f' % num.value), n))

        # sort websockets by latency
        pinged = [x for _, x in sorted(zip(timed, pinged))]
        timed = sorted(timed)
        unknown = sorted(
            list(set(validated).difference(
                pinged + down + stale + expired + testnet)))

        # report outcome
        print('')
        print((len(pinged), 'of', len(validated),
               'nodes are active with latency less than', timeout))
        print('')
        print(('fastest node', pinged[0], 'with latency', ('%.2f' % timed[0])))
        if len(excluded):
            for i in range(len(excluded)):
                print(('EXCLUDED', excluded[i]))
        if len(unknown):
            for i in range(len(unknown)):
                print(('UNTESTED', unknown[i]))
        if len(testnet):
            for i in range(len(testnet)):
                print(('TESTNET', testnet[i]))
        if len(expired):
            for i in range(len(expired)):
                print(('TIMEOUT', expired[i]))
        if len(stale):
            for i in range(len(stale)):
                print(('STALE', stale[i]))
        if len(down):
            for i in range(len(down)):
                print(('DOWN', down[i]))
        if len(pinged):
            print ('')
            print ('GOOD nodes:')
            print ('')
            for i in range(len(pinged)):
                print((('%.2f' % timed[i]), pinged[i]))

        ret = pinged[:crop]
        # print (pinged[0])
        # print (ret[0])
        # print (timed[0])
    else:
        ret = validated[:crop]

    print ('')
    enablePrint()
    elapsed = time.time() - begin
    # print ('elapsed:', ('%.1f' % elapsed),
    #       'fastest:', ('%.3f' % timed[0]), ret[0])
    # print (ret)

    if write and (len(ret) == crop):
        opened = 0
        while not opened:
            try:
                with open('nodes.txt', 'w+') as file:
                    file.write(str(ret))

                opened = 1
            except:
                pass
    return (ret)


def nodes_loop():

    while True:
        try:
            nodes_process(
                timeout=5, pings=999, crop=10, noprint=True, write=True,
                include=True, exclude=False, suffix=False, master=False)
            time.sleep(30)

        # no matter what happens just keep verifying book
        except Exception as e:
            print (type(e).__name__, e.args, e)
            pass


def nodes_update():

    print('Acquiring low latency connection to Bitshares DEX' +
          ', this may take a few minutes...')
    updated = 0
    try:
        while not updated:
            nodes_process(
                timeout=5, pings=999, crop=10, noprint=False, write=True,
                include=True, exclude=False, suffix=False, master=False)
            updated = 1

    # not satisfied until verified once
    except Exception as e:
        print (type(e).__name__, e.args, e)
        pass

    print('')
    print('DEX CONNECTION ESTABLISHED - will refresh every 10 minutes')
    print('')


def race_write(doc='', text=''):  # Concurrent Write to File Operation

    opened = 0
    while not opened:
        try:
            with open(doc, 'w+') as f:
                f.write(str(text))
                opened = 1
        except Exception as e:
                print (e, type(e).__name__, e.args)
                print (str(doc) + ' RACE WRITE, try again...')
                pass


def race_read(doc=''):  # Concurrent Read from File Operation

    opened = 0
    while not opened:
        try:
            with open(doc, 'r') as f:
                ret = literal(f.read())
                opened = 1
        except Exception as e:
            print (e, type(e).__name__, e.args)
            print (str(doc) + ' RACE READ, try again...')
            pass
    return ret


def zprint(z):
    for i in range(10):
        print(z)


def book(node='', a=None, b=None):

    if 0:  # x ==1:
        plt.ion()
    begin = time.time()
    while time.time() < (begin + 60):
        try:
            # update data fields
            time.sleep(1)
            ACCOUNT.refresh()
            market = Market(BitPAIR,
                            bitshares_instance=BitShares(node, num_retries=0),
                            mode='head')
            trades = market.trades(limit=100)
            last = float(trades[0]['price'])
            # add unix time to trades dictionary
            for t in range(len(trades)):
                ts = time.strptime(str(trades[t]['time']), '%Y-%m-%d %H:%M:%S')
                trades[t]['unix'] = int(time.mktime(ts))
            # last price
            # last = market.ticker()['latest']
            slast = '%.16f' % last
            # complete account balances
            call = decimal(time.time())
            raw = list(ACCOUNT.balances)
            elapsed = '%.17f' % float(decimal(time.time()) - call)
            cbalances = {}
            for i in range(len(raw)):
                cbalances[raw[i]['symbol']] = float(raw[i]['amount'])
            # orderbook
            raw = market.orderbook(limit=20)
            bids = raw['bids']
            asks = raw['asks']
            sbidp = [('%.16f' % bids[i]['price']) for i in range(len(bids))]
            saskp = [('%.16f' % asks[i]['price']) for i in range(len(asks))]
            sbidv = [('%.2f' % float(bids[i]['quote'])).rjust(12, ' ')
                     for i in range(len(bids))]
            saskv = [('%.2f' % float(asks[i]['quote'])).rjust(12, ' ')
                     for i in range(len(asks))]
            bidv = [float(bids[i]['quote']) for i in range(len(bids))]
            askv = [float(asks[i]['quote']) for i in range(len(asks))]
            cbidv = list(np.cumsum(bidv))
            caskv = list(np.cumsum(askv))
            cbidv = [('%.2f' % i).rjust(12, ' ') for i in cbidv]
            caskv = [('%.2f' % i).rjust(12, ' ') for i in caskv]
            # dictionary of currency and assets in this MARKET
            currency = float(ACCOUNT.balance(BitCURRENCY))
            assets = float(ACCOUNT.balance(BitASSET))
            balances = {BitCURRENCY: currency, BitASSET: assets}
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
            trades = trades[:10]
            stale = int(time.time() - float(trades[0]['unix']))

            # display orderbooks
            print("\033c")
            print(time.ctime(), '            ', int(time.time()), '   ', a, b)
            print('                            ',
                 (elapsed), '   ', node)
            print('')
            print(
                '                        LAST',
                slast[:10],
                slast[10:],
                '   ',
                BitPAIR)
            print('')
            print(
                '            ', sbidv[0], '  ', (
                    sbidp[0])[:10], (sbidp[0])[10:],
                '   ',
                (saskp[0])[:10], (saskp[0])[10:], (saskv[0]))
            print('                                           ',
                  'BIDS',
                  '   ',
                  'ASKS')
            for i in range(1, len(sbidp)):
                print(
                    cbidv[i], sbidv[i], '  ', (sbidp[i])[:10], (sbidp[i])[10:],
                    '   ',
                    (saskp[i])[:10], (saskp[i])[10:], saskv[i], caskv[i])
            print('')
            for o in orders:
                print (o)
            if len(orders) == 0:
                print ('                                  NO OPEN ORDERS')
            print('')
            print('%s BALANCE:' % BitPAIR)
            print (balances)
            print('')
            print('MARKET HISTORY:              SECONDS STALE:', stale)
            for t in trades:
                # print(t.items())
                print(t['unix'],
                      str(t['time'])[11:19],
                     ('%.16f' % float(t['price'])),
                     ('%.2f' % float(t['quote']['amount'])).rjust(12, ' '))
            print('')
            print('ctrl+shift+\ will EXIT to terminal')
            print('')
            print('YOUR COMPLETE HOLDINGS')
            print(cbalances)
        except:
            pass


def dex_withdraw():

    # undeveloped definition for withdrawals
    from bitshares import BitShares
    bitshares = BitShares()
    bitshares.wallet.unlock("wallet-passphrase")
    bitshares.transfer(
        to=send_to,
        amount=send_amount,
        asset=BTS,
        memo=None,
        account=ACCOUNT)

def dex_buy():

    def buy(price, amount):
        confirm.destroy()
        attempt = 1
        while attempt:
            try:
                details = (MARKET.buy(price, amount))
                print (details)
                attempt = 0
            except:
                zprint(("buy attempt %s failed" % attempt))
                attempt += 1
                if attempt > 10:
                    zprint('buy aborted')
                    return
                pass
    if MARKET.bitshares.wallet.unlocked():
        zprint('BUY')
        price = sell_price.get()
        amount = sell_amount.get()
        if price == '':
            price=2*float(MARKET.ticker()['latest'])
            sprice = 'MARKET RATE'
        if amount == '':
            amount = ANTISAT
        confirm = Tk()
        try:
            price = float(price)
            amount= float(amount)
            if price != ANTISAT:
                sprice= '%.16f' % price
            currency = float(ACCOUNT.balance(BitCURRENCY))
            if amount > (0.998) * currency * float(price):
                amount = (0.998) * currency * float(price)
            samount = str(amount)
            sorder = str('CONFIRM BUY ' + samount + ' ' + BitASSET + ' @ '+ sprice)
            if amount > 0:
                confirm.title(sorder)
                Button(
                    confirm,
                    text='CONFIRM',
                    command= lambda:buy(price,amount)).grid(
                    row=1,
                    column=0,
                    pady=8)
                Button(
                    confirm,
                    text='INVALIDATE',
                    command=confirm.destroy).grid(
                    row=2,
                    column=0,
                    pady=8)
            else:
                confirm.title('NO CURRENCY TO BUY')
                Button(
                    confirm,
                    text='OK',
                    command=confirm.destroy).grid(
                    row=2,
                    column=0,
                    pady=8)
        except:
            confirm.title('INVALID BUY ORDER')
            Button(
                confirm,
                text='OK',
                command=confirm.destroy).grid(
                row=2,
                column=0,
                pady=8)
        confirm.geometry('500x100+800+150')
        confirm.lift()
        confirm.call('wm', 'attributes', '.', '-topmost', True)
    else:
        zprint('YOUR WALLET IS LOCKED')



def dex_sell():

    def sell(price, amount):
        confirm.destroy()
        attempt = 1
        while attempt:
            try:
                details = (MARKET.sell(price, amount))
                print (details)
                attempt = 0
            except:
                zprint(("sell attempt %s failed" % attempt))
                attempt += 1
                if attempt > 10:
                    zprint('sell aborted')
                    return
                pass
    if MARKET.bitshares.wallet.unlocked():
        zprint('SELL')
        price = sell_price.get()
        amount = sell_amount.get()
        if price == '':
            price = 0.5*float(MARKET.ticker()['latest'])
            sprice = 'MARKET RATE'
        if amount == '':
            amount = ANTISAT
        confirm = Tk()
        try:
            price = float(price)
            amount = float(amount)
            if price != SATOSHI:
                sprice= '%.16f' % price
            assets = float(ACCOUNT.balance(BitASSET))
            if amount > (0.998*assets):
                amount = 0.998 * assets
            samount=str(amount)
            sorder = str('CONFIRM SELL ' + samount + ' ' + BitASSET + ' @ '+ sprice)

            if amount > 0:
                confirm.title(sorder)
                Button(
                    confirm,
                    text='CONFIRM',
                    command= lambda:sell(price,amount)).grid(
                    row=1,
                    column=0,
                    pady=8)
                Button(
                    confirm,
                    text='INVALIDATE',
                    command=confirm.destroy).grid(
                    row=2,
                    column=0,
                    pady=8)
            else:
                confirm.title('NO ASSETS TO SELL')
                Button(
                    confirm,
                    text='OK',
                    command=confirm.destroy).grid(
                    row=2,
                    column=0,
                    pady=8)
        except:
            confirm.title('INVALID SELL ORDER')
            Button(
                confirm,
                text='OK',
                command=confirm.destroy).grid(
                row=2,
                column=0,
                pady=8)
        confirm.geometry('500x100+800+150')
        confirm.lift()
        confirm.call('wm', 'attributes', '.', '-topmost', True)
    else:
        zprint('YOUR WALLET IS LOCKED')


def dex_cancel():

    def cancel():

        confirm.destroy()
        orders = MARKET.accountopenorders()
        zprint('CANCEL')
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
                    zprint((attempt, 'cancel failed', order_list))
                    attempt += 1
                    if attempt > 10:
                        zprint('cancel aborted')
                        return
                    pass

    if MARKET.bitshares.wallet.unlocked():
        confirm = Tk()
        confirm.title('')
        Label(confirm, text='CONFIRM CANCEL ALL').grid(row=0, column=0)
        Button(
            confirm,
            text='CONFIRM',
            command=cancel).grid(
            row=1,
            column=0,
            pady=8)
        Button(
            confirm,
            text='INVALIDATE',
            command=confirm.destroy).grid(
            row=2,
            column=0,
            pady=8)
        confirm.geometry('150x150+900+250')
        confirm.lift()
        confirm.call('wm', 'attributes', '.', '-topmost', True)
    else:
        zprint('YOUR WALLET IS LOCKED')


def dex_auth_gui():
    global MARKET
    global PASS_PHRASE
    PASS_PHRASE = str(login.get())
    login.delete(0, END)
    try:
        MARKET.bitshares.wallet.unlock(PASS_PHRASE)
        lock.set('UNLOCKED')
    except Exception as ex:
        if PASS_PHRASE != '':
            zprint(type(ex).__name__)
        MARKET.bitshares.wallet.lock()
        lock.set('LOCKED')
        pass


def launch(a):

    nds = race_read('nodes.txt')
    if isinstance(nds, list):
        ns = nds
    else:
        ns = nodes
    p = {}
    b = 0
    while True:
        try:
            b += 1
            shuffle(ns)
            n = str(ns[0])
            p[str(b)] = Process(target=book, args=(n, a, b,))
            p[str(b)].daemon = True
            p[str(b)].start()
            p[str(b)].join(TIMEOUT)
        except:
            pass

servers = Process(target=nodes_loop)
servers.start()


# sign in
BitPAIR = BitASSET + ':' + BitCURRENCY
print("\033c")
print('')
print('')
print(VERSION)
print('=================================================')
print('')
print('')
ACCOUNT = Account(input('           Account: '))
print('')
print('      Welcome Back: %s' % ACCOUNT)
print('')
print(' Default MARKET is: %s' % BitPAIR)
print('')
print('Input new MARKET below or press ENTER to skip')
print('')
BitPAIR = (input('  Change MARKET to: ') or BitPAIR)

BitASSET = BitPAIR.split(':')[0]
BitCURRENCY = BitPAIR.split(':')[1]
MARKET = Market(BitPAIR, bitshares_instance=BitShares(nodes), mode='head')
print('')
print('Enter PASS PHRASE below to unlock your wallet or press ENTER to skip')
print('')
PASS_PHRASE = getpass(prompt='       Pass Phrase: ')
if PASS_PHRASE != '':
    try:
        MARKET.bitshares.wallet.unlock(PASS_PHRASE)
    except Exception as ex:
        print (type(ex).__name__)
        sys.exit()
print('')
print('Connecting to the Bitshares Distributed Exchange, please wait...')
print('')

multinode = {}
for a in range(1, 7):
    # multinode orderbooks
    multinode[str(a)] = Process(target=launch, args=(a,))
    multinode[str(a)].start()


# busybox
master = Tk()
lock = StringVar()
lock.set('UNLOCKED')
if MARKET.bitshares.wallet.locked():
    lock.set('LOCKED')
master.title(VERSION)
Label(master, text="PRICE:").grid(row=0, column=0, sticky=E)
Label(master, text="AMOUNT:").grid(row=1, column=0, sticky=E)
Label(master, text="PRICE:").grid(row=0, column=2, sticky=E)
Label(master, text="AMOUNT:").grid(row=1, column=2, sticky=E)
Label(master, textvariable=lock).grid(row=6, column=2, sticky=W)

buy_price = Entry(master)
buy_amount = Entry(master)
sell_price = Entry(master)
sell_amount = Entry(master)
login = Entry(master)

buy_price.grid(row=0, column=1)
buy_amount.grid(row=1, column=1)
sell_price.grid(row=0, column=3)
sell_amount.grid(row=1, column=3)
login.grid(row=6, column=1)

Button(
    master,
    text='BUY',
    command=dex_buy).grid(
    row=3,
    column=1,
    sticky=W,
    pady=4)
Button(
    master,
    text='SELL',
    command=dex_sell).grid(
    row=3,
    column=3,
    sticky=W,
    pady=4)
Button(
    master,
    text='CANCEL ALL',
    command=dex_cancel).grid(
    row=5,
    column=0,
    sticky=E,
    pady=4)
Button(
    master,
    text='LOCK/UNLOCK',
    command=dex_auth_gui).grid(
    row=6,
    column=0,
    sticky=E,
    pady=4)
master.geometry('600x200+600+700')

master.lift()
master.call('wm', 'attributes', '.', '-topmost', True)
mainloop()
