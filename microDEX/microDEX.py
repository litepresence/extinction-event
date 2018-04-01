
VERSION = 'microDEX v0.00000010 - low latency minimalist UI'

' (BTS) litpresence1 '

# WTFPLv0 - March 1765

import os
import sys
import time
import requests
import datetime
import numpy as np
from tkinter import *
from getpass import getpass
from datetime import datetime
from dateutil.parser import parser
from random import random, shuffle
from decimal import Decimal as decimal
from ast import literal_eval as literal
from multiprocessing import Process, active_children, Value, Array

from bitshares.utils import *
from bitshares import BitShares
from bitshares.wallet import Wallet
from bitshares.market import Market
from bitshares.account import Account
from bitshares.blockchain import Blockchain

import matplotlib.pyplot as plt
import warnings
import matplotlib
import matplotlib.cbook as cbook
import matplotlib.dates as mdates

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
TIMEOUT = 120
CONNECTIONS = 6
BitPAIR = BitASSET + ':' + BitCURRENCY

ID = '4018d7844c78f6a6c41c6a552b898022310fc5dec06da467ee7905a8dad512c8'

def nodes_process(  # sorts nodes for lowest latency
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
        race_write(doc='nodes.txt', text=str(ret))
    return (ret)

def nodes_loop():  # repeats nodes process

    while True:
        try:
            nodes_process(
                timeout=5, pings=999, crop=10, noprint=True, write=True,
                include=True, exclude=False, suffix=True, master=False)
            time.sleep(30)

        # no matter what happens just keep verifying book
        except Exception as e:
            print (type(e).__name__, e.args, e)
            pass

def nodes_update():  # single run of nodes process

    print('Acquiring low latency connection to Bitshares DEX' +
          ', this may take a few minutes...')
    updated = 0
    try:
        while not updated:
            nodes_process(
                timeout=5, pings=999, crop=10, noprint=False, write=True,
                include=True, exclude=False, suffix=True, master=False)
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

def zprint(z):  # prints 10X to flash orderbook
    OFFSET = '                                                      '
    z = '\n' + OFFSET + z
    for i in range(10):
        time.sleep(0.03)
        print("\033c")
        for i in range(50):
            print(z)

def reconnect(BitPAIR, USERNAME, PASS_PHRASE):

    # create fresh websocket connection
    connected = 0
    while not connected:
        nds = race_read('nodes.txt')
        if isinstance(nds, list):
            nodes = nds
        shuffle(nodes)
        try:
            account = Account(USERNAME,
                              bitshares_instance=BitShares(nodes, num_retries=0))
            market = Market(BitPAIR,
                            bitshares_instance=BitShares(nodes, num_retries=0),
                            mode='head')
            connected = 1
        except:
            pass
    try:
        market.bitshares.wallet.unlock(PASS_PHRASE)
    except:
        pass
    #zprint('CONNECTED')
    return account, market, nodes

def book(a=None, b=None):  # updates orderbook details

    account, market, nodes = reconnect(BitPAIR, USERNAME, PASS_PHRASE)
    node = nodes[0]
    begin = time.time()
    while time.time() < (begin + TIMEOUT):
        time.sleep(random())
        try:
            # add unix time to trades dictionary
            trades = market.trades(limit=100)
            for t in range(len(trades)):
                ts = time.strptime(str(trades[t]['time']), '%Y-%m-%d %H:%M:%S')
                trades[t]['unix'] = int(time.mktime(ts))
                fprice = '%.16f' % float(trades[t]['price'])
                trades[t]['fprice'] = fprice[:10] + ',' + fprice[10:]
            # last price
            # last = market.ticker()['latest']
            last = float(trades[0]['price'])
            slast = '%.16f' % last
            # complete account balances
            call = decimal(time.time())
            raw = list(account.balances)
            elapsed = float(decimal(time.time()) - call)
            if elapsed > 1:
                continue
            elapsed = '%.17f' % elapsed
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
            # dictionary of currency and assets in this market
            currency = float(account.balance(BitCURRENCY))
            assets = float(account.balance(BitASSET))
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
                else:
                    amount = amount / price
                orders.append({'orderNumber': orderNumber,
                               'orderType': orderType,
                               'market': BitPAIR,
                               'amount': amount,
                               'price': ('%.16f' % price)})
            trades = trades[:10]
            stale = int(time.time() - float(trades[0]['unix']))
            # display orderbooks
            print("\033c")
            print(time.ctime(), '                            RUN TIME',
                (int(time.time())-BEGIN), 'EPOCH', b, 'PROCESS', a)
            print('                        PING',
                 (elapsed), '   ', node)
            print('')
            print(
                '                        LAST',
                slast[:10] + ',' + slast[10:],
                '   ',
                BitPAIR)
            print('')
            print(
                '            ', sbidv[0], '  ', (
                    sbidp[0])[:10] + ',' + (sbidp[0])[10:],
                '   ',
                (saskp[0])[:10] + ',' + (saskp[0])[10:], (saskv[0]))
            print('                                           ',
                  'BIDS',
                  '   ',
                  'ASKS')
            for i in range(1, len(sbidp)):
                print(
                    cbidv[i], sbidv[i], '  ', (
                        sbidp[i])[:10] + ',' + (sbidp[i])[10:],
                    '   ',
                    (saskp[i])[:10] + ',' + (saskp[i])[10:],
                    saskv[i], caskv[i])
            print('')
            for o in orders:
                print (o)
            if len(orders) == 0:
                print ('                                  NO OPEN ORDERS')
            print('')
            print('%s BALANCE:' % BitPAIR)
            print (balances)
            print('')
            print('MARKET HISTORY:', stale, 'since last trade')
            for t in trades:
                # print(t.items())
                print(t['unix'],
                      str(t['time'])[11:19],
                      t['fprice'],
                      ('%.4f' % float(t['quote']['amount'])).rjust(12, ' '))
            print('')
            print('ctrl+shift+\ will EXIT to terminal')
            print('')
            print('COMPLETE HOLDINGS:')
            print(cbalances)
        except:
            zprint('BOOK')
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
        account=account)

def dex_buy():

    # update wallet unlock to low latency node
    zprint('BUY')
    account, market, nodes = reconnect(BitPAIR, USERNAME, PASS_PHRASE)
    try:
        market.bitshares.wallet.unlock(PASS_PHRASE)
    except:
        pass
    # attempt buy 10X or until satisfied

    def buy(price, amount):
        confirm.destroy()
        zprint('CONFIRMED')
        attempt = 1
        while attempt:
            try:
                details = (market.buy(price, amount))
                print (details)
                attempt = 0
            except:
                zprint(("buy attempt %s failed" % attempt))
                attempt += 1
                if attempt > 10:
                    zprint('buy aborted')
                    return
                pass
    # interact with tkinter
    confirm = Tk()
    if market.bitshares.wallet.unlocked():
        price = buy_price.get()
        amount = buy_amount.get()
        if price == '':
            price = 2 * float(market.ticker()['latest'])
            sprice = 'market RATE'
        if amount == '':
            amount = ANTISAT
        try:
            price = float(price)
            amount = float(amount)
            if price != ANTISAT:
                sprice = '%.16f' % price
            currency = float(account.balance(BitCURRENCY))
            if amount > (0.998) * currency / float(price):
                amount = (0.998) * currency / float(price)
            samount = str(amount)
            sorder = str(
                'CONFIRM BUY ' +
                samount +
                ' ' +
                BitASSET +
                ' @ ' +
                sprice)
            if amount > 0:
                confirm.title(sorder)
                Button(
                    confirm,
                    text='CONFIRM BUY',
                    command=lambda: buy(price, amount)).grid(
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
        confirm.geometry('500x100+800+175')
        confirm.lift()
        confirm.call('wm', 'attributes', '.', '-topmost', True)
    else:
        confirm.title('YOUR WALLET IS LOCKED')
        Button(
            confirm,
            text='OK',
            command=confirm.destroy).grid(
            row=2,
            column=0,
            pady=8)
    confirm.geometry('500x100+800+175')
    confirm.lift()
    confirm.call('wm', 'attributes', '.', '-topmost', True)

def dex_sell():

    # update wallet unlock to low latency node
    zprint('SELL')
    account, market, nodes = reconnect(BitPAIR, USERNAME, PASS_PHRASE)

    # attempt to sell 10X or until satisfied
    def sell(price, amount):
        confirm.destroy()
        zprint('CONFIRMED')
        attempt = 1
        while attempt:
            try:
                details = market.sell(price, amount)
                print (details)
                attempt = 0
            except:
                zprint(("sell attempt %s failed" % attempt))
                attempt += 1
                if attempt > 10:
                    zprint('sell aborted')
                    return
                pass
    # interact with tkinter
    confirm = Tk()
    if market.bitshares.wallet.unlocked():
        price = sell_price.get()
        amount = sell_amount.get()
        if price == '':
            price = 0.5 * float(market.ticker()['latest'])
            sprice = 'market RATE'
        if amount == '':
            amount = ANTISAT
        try:
            price = float(price)
            amount = float(amount)
            if price != SATOSHI:
                sprice = '%.16f' % price
            assets = float(account.balance(BitASSET))
            if amount > (0.998 * assets):
                amount = 0.998 * assets
            samount = str(amount)
            sorder = str(
                'CONFIRM SELL ' +
                samount +
                ' ' +
                BitASSET +
                ' @ ' +
                sprice)

            if amount > 0:
                confirm.title(sorder)
                Button(
                    confirm,
                    text='CONFIRM SELL',
                    command=lambda: sell(price, amount)).grid(
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
    else:
        confirm.title('YOUR WALLET IS LOCKED')
        Button(
            confirm,
            text='OK',
            command=confirm.destroy).grid(
            row=2,
            column=0,
            pady=8)
    confirm.geometry('500x100+800+175')
    confirm.lift()
    confirm.call('wm', 'attributes', '.', '-topmost', True)

def dex_cancel():

    # update wallet unlock to low latency node
    zprint('CANCEL')
    account, market, nodes = reconnect(BitPAIR, USERNAME, PASS_PHRASE)
    orders = market.accountopenorders()
    # attempt cancel all 10X or until satisfied
    def cancel():
        confirm.destroy()
        zprint('CONFIRMED')
        attempt = 1
        order_list = []
        for order in orders:
            order_list.append(order['id'])
        while attempt:
            try:
                details = market.cancel(order_list)
                print (details)
                attempt = 0
            except:
                zprint((attempt, 'cancel failed', order_list))
                attempt += 1
                if attempt > 10:
                    zprint('cancel aborted')
                    return
                pass
    # interact with tkinter
    confirm = Tk()
    if len(orders):
        if market.bitshares.wallet.unlocked():
            if len(orders) > 1:
                title = str(len(orders)) + ' ORDERS TO CANCEL'
            else:
                title = str(len(orders)) + ' ORDER TO CANCEL'
            confirm.title(title)
            Button(
                confirm,
                text='CONFIRM CANCEL ALL',
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
            confirm.geometry('500x100+800+175')
            confirm.lift()
            confirm.call('wm', 'attributes', '.', '-topmost', True)
        else:
            confirm.title('YOUR WALLET IS LOCKED')
            Button(
                confirm,
                text='OK',
                command=confirm.destroy).grid(
                row=2,
                column=0,
                pady=8)
    else:
        confirm.title('NO OUTSTANDING ORDERS')
        Button(
            confirm,
            text='OK',
            command=confirm.destroy).grid(
            row=2,
            column=0,
            pady=8)
    confirm.geometry('500x100+800+175')
    confirm.lift()
    confirm.call('wm', 'attributes', '.', '-topmost', True)

def dex_auth_gui():

    # unlock wallet from gui
    global PASS_PHRASE
    PASS_PHRASE = str(login.get())
    login.delete(0, END)
    account, market, nodes = reconnect(BitPAIR, USERNAME, PASS_PHRASE)
    try:
        market.bitshares.wallet.unlock(PASS_PHRASE)
        lock.set('UNLOCKED')
        zprint('AUTHENTICATED')
    except Exception as ex:
        if PASS_PHRASE != '':
            zprint(type(ex).__name__)
        market.bitshares.wallet.lock()
        lock.set('LOCKED')
        zprint('WALLET LOCKED')
        pass

def launch_book(a):

    # continually respawn child processes to update order book
    p = {}
    b = 0
    while True:
        try:
            b += 1
            p[str(b)] = Process(target=book, args=(a, b,))
            p[str(b)].daemon = True
            p[str(b)].start()
            p[str(b)].join(TIMEOUT * 0.5 + TIMEOUT * random())
        except:
            pass

def float_sma(array, period):  # floating point periods accepted

    def moving_average(array, period):  # numpy array moving average
        csum = np.cumsum(array, dtype=float)
        csum[period:] = csum[period:] - csum[:-period]
        return csum[period - 1:] / period

    if period == int(period):
        return moving_average(array, int(period))
    else:
        floor_period = int(period)
        ceil_period = int(floor_period + 1)
        floor_ratio = ceil_period - period
        ceil_ratio = 1.0 - floor_ratio
        floor = moving_average(array, floor_period)
        ceil = moving_average(array, ceil_period)
        depth = min(len(floor), len(ceil))
        floor = floor[-depth:]
        ceil = ceil[-depth:]
        ma = (floor_ratio * floor) + (ceil_ratio * ceil)
        return ma

def chartdata(pair, start, stop, period):  # Public API cryptocompare

    #{"time","close","high","low","open","volumefrom","volumeto"}
    # docs at https://www.cryptocompare.com/api/

    if period in [60, 300, 900, 1800, 3600, 7200, 14400, 43200, 86400]:

        uri = 'https://min-api.cryptocompare.com/data/'
        if period <= 1800:
            uri += 'histominute'
            aggregate = period / 60.0
        if 3600 <= period <= 43200:
            uri += 'histohour'
            aggregate = period / 3600.0
        if period >= 86400:
            uri += 'histoday'
            aggregate = period / 86400.0
        aggregate = int(aggregate)
        pair_split = pair.split('_')
        fsym = pair_split[1]
        tsym = pair_split[0]
        toTs = int(stop)
        limit = int((stop - start) / float(period))
        if limit > 2000:
            limit = 2000
        params = {'fsym': fsym, 'tsym': tsym, 'limit': 2000,
                  'aggregate': aggregate, 'toTs': toTs}
        ret = requests.get(uri, params=params).json()
        d = ret['Data']
        clean_d = clean_d1 = [i for i in d if i['close'] > 0]

        if (period == 7200) and ((stop - start) / 7200.0 > 1000):
            toTs -= period * len(clean_d)
            params = {'fsym': fsym, 'tsym': tsym, 'limit': 2000,
                      'aggregate': aggregate, 'toTs': toTs}
            ret = requests.get(uri, params=params).json()
            d = ret['Data']
            clean_d2 = [i for i in d if i['close'] > 0]
            clean_d = clean_d2 + clean_d1
            clean_d = [i for i in clean_d if i['time'] > start]

        return clean_d

    else:
        print('invalid period')
        return None

def live_candles(pair, candle, depth):  # Current HLOCV arrays

    # gather latest data to a given depth
    now = int(time.time())
    raw = chartdata(pair, (now - (depth + 10) * candle), now, candle)
    d = {}
    d['unix'] = []
    d['high'] = []
    d['low'] = []
    d['open'] = []
    d['close'] = []
    d['volume'] = []
    for i in range(len(raw)):
        d['unix'].append(raw[i]['time'])
        d['high'].append(raw[i]['high'])
        d['low'].append(raw[i]['low'])
        d['open'].append(raw[i]['open'])
        d['close'].append(raw[i]['close'])
        d['volume'].append(raw[i]['volumefrom'])
    # filter absurd wicks
    for i in range(len(d['unix'])):
        if d['high'][i] > 2*d['close'][i]:
                d['high'][i] = 2*d['close'][i]
        if d['low'][i] < 0.5*d['close'][i]:
                d['low'][i] = 0.5*d['close'][i]
    d['unix'] = np.array(d['unix'][-depth:])
    d['high'] = np.array(d['high'][-depth:])
    d['low'] = np.array(d['low'][-depth:])
    d['open'] = np.array(d['open'][-depth:])
    d['close'] = np.array(d['close'][-depth:])
    d['volume'] = np.array(d['volume'][-depth:])

    return d

def plot_format(log):

    warnings.filterwarnings("ignore", category=cbook.mplDeprecation)
    ax = plt.gca()
    ax.patch.set_facecolor('0.1')
    ax.yaxis.tick_right()
    ax.spines['bottom'].set_color('0.5')
    ax.spines['top'].set_color(None)
    ax.spines['right'].set_color('0.5')
    ax.spines['left'].set_color(None)
    ax.tick_params(axis='x', colors='0.7', which='both')
    ax.tick_params(axis='y', colors='0.7', which='both')
    ax.yaxis.label.set_color('0.9')
    ax.xaxis.label.set_color('0.9')
    plt.minorticks_on
    plt.grid(b=True, which='major', color='0.2', linestyle='-')
    plt.grid(b=True, which='minor', color='0.2', linestyle='-')

    if log == 1:
        plt.ylabel('LOGARITHMIC PRICE SCALE')
        plt.yscale('log')
    ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.yaxis.set_minor_formatter(matplotlib.ticker.ScalarFormatter())
    ax.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%.8f"))
    ax.yaxis.set_minor_formatter(matplotlib.ticker.FormatStrFormatter("%.8f"))
    plt.autoscale(enable=True, axis='y')
    plt.tight_layout()

    if log == 1:
        # force 'autoscale'
        yd = []  # matrix of y values from all lines on plot
        xd = []  # matrix of x values from all lines on plot
        for n in range(len(plt.gca().get_lines())):
            line = plt.gca().get_lines()[n]
            yd.append((line.get_ydata()).tolist())
            xd.append((line.get_xdata()).tolist())
        yd = [item for sublist in yd for item in sublist]
        ymin, ymax = np.min(yd), np.max(yd)
        ax.set_ylim([0.95 * ymin, 1.05 * ymax])
        xd = [item for sublist in xd for item in sublist]
        xmin, xmax = np.min(xd), np.max(xd)
        ax.set_xlim([xmin, xmax])
        # add sub minor ticks
        set_sub_formatter = []
        sub_ticks = [10, 11, 12, 14, 16, 18, 22, 25, 35, 45]
        sub_range = [-8, 8]
        for i in sub_ticks:
            for j in range(sub_range[0], sub_range[1]):
                set_sub_formatter.append(i * 10 ** j)
        k = []
        for l in set_sub_formatter:
            if ymin < l < ymax:
                k.append(l)
        ax.set_yticks(k)



    def timestamp(x, pos):
        return (datetime.fromtimestamp(x)).strftime('%m/%d %H:%M')
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(timestamp))
    plt.gcf().autofmt_xdate(rotation=30)
    plt.gcf().canvas.set_window_title('microDEX CHART')

def charts():

    def draw_chart():
        zprint('UPDATING CHART DATA')
        ASSET = BitASSET.replace('OPEN.', '')
        CURRENCY = BitCURRENCY.replace('OPEN.', '')
        PAIR = ('%s_%s' % (CURRENCY, ASSET))
        ret = live_candles(PAIR, 300, 1999)
        cex_5m_x = ret['unix']
        cex_5m_close = ret['close']
        cex_5m_high = ret['high']
        cex_5m_low = ret['low']
        cex_5m_x = [(i + 150) for i in cex_5m_x]
        ret = live_candles(PAIR, 7200, 3999)
        cex_2h_x = ret['unix']
        cex_2h_close = ret['close']
        cex_2h_high = ret['high']
        cex_2h_low = ret['low']
        cex_2h_x = [(i + 3600) for i in cex_2h_x]
        ret = live_candles(PAIR, 86400, 1000)
        cex_d_x = ret['unix']
        cex_d_close = ret['close']
        cex_d_high = ret['high']
        cex_d_low = ret['low']
        crop = len(cex_d_x) - 90
        cex_d_x = cex_d_x[-crop:-50]
        cex_d_close = cex_d_close[-crop:-50]
        cex_d_high = cex_d_high[-crop:-50]
        cex_d_low = cex_d_low[-crop:-50]
        cex_d_x = [(i + 43400) for i in cex_d_x]
        try:
            ma1_2h_period = 12.0 * float(MA1.get())
            ma2_2h_period = 12.0 * float(MA2.get())
        except:
            ma1_2h_period = 120
            ma2_2h_period = 600
        ma1_2h = float_sma(cex_2h_close, ma1_2h_period)
        ma2_2h = float_sma(cex_2h_close, ma2_2h_period)
        min_len = min(len(ma1_2h), len(ma2_2h))
        ma1_2h = ma1_2h[-min_len:]
        ma2_2h = ma2_2h[-min_len:]
        ma_x_2h = cex_2h_x[-min_len:]
        ma_x_2h = [(i + 7200) for i in ma_x_2h]
        ma1_d_period = ma1_2h_period /12.0
        ma2_d_period = ma2_2h_period /12.0
        if min(ma1_d_period, ma2_d_period) > 2:
            ma1_d = float_sma(cex_d_close, ma1_d_period)
            ma2_d = float_sma(cex_d_close, ma2_d_period)
            min_len = min(len(ma1_d), len(ma2_d))
            ma1_d = ma1_d[-min_len:]
            ma2_d = ma2_d[-min_len:]
            ma_x_d = cex_d_x[-min_len:]
            ma_x_d = [(i + 86400) for i in ma_x_d]

        account, market, nodes = reconnect(BitPAIR, USERNAME, PASS_PHRASE)
        trades = market.trades(limit=100)
        for t in range(len(trades)):
            ts = time.strptime(str(trades[t]['time']), '%Y-%m-%d %H:%M:%S')
            trades[t]['unix'] = int(time.mktime(ts))
        dex_x, dex_y = [],[]
        for t in range(len(trades)):
            dex_x.append(float(trades[t]['unix']))
            dex_y.append(float(trades[t]['price']))
        plt.cla
        ax = plt.gca()
        log = int((scale.var).get())
        for l in ax.get_lines():
                l.remove()
        fig.patch.set_facecolor('0.15')
        plt.plot(cex_5m_x, cex_5m_high,
            markersize=1, marker='.', color='magenta')
        plt.plot(cex_5m_x, cex_5m_low,
            markersize=1, marker='.', color='magenta')
        plt.plot(cex_5m_x, cex_5m_close,
            markersize=1, marker='.', color='yellow')
        plt.plot(cex_2h_x, cex_2h_high,
            markersize=1, marker='.', color='magenta')
        plt.plot(cex_2h_x, cex_2h_low,
            markersize=1, marker='.', color='magenta')
        plt.plot(cex_2h_x, cex_2h_close,
            markersize=1, marker='.', color='yellow')
        plt.plot(cex_d_x, cex_d_high,
            markersize=1, marker='.', color='magenta')
        plt.plot(cex_d_x, cex_d_low,
            markersize=1, marker='.', color='magenta')
        plt.plot(cex_d_x, cex_d_close,
            markersize=1, marker='.', color='yellow')
        plt.plot(ma_x_2h, ma1_2h,
            markersize=1, marker='.', color='pink')
        plt.plot(ma_x_2h, ma2_2h,
            markersize=1, marker='.', color='aqua')
        if min(ma1_d_period, ma2_d_period) > 2:
            plt.plot(ma_x_d, ma1_d,
                markersize=1, marker='.', color='pink')
            plt.plot(ma_x_d, ma2_d,
                markersize=1, marker='.', color='aqua')
        plt.plot(dex_x, dex_y, markersize=6, marker='.', color='white')
        interface.after(60000, draw_chart)        
        plot_format(log)
        plt.show()
    fig = plt.figure()
    interface = Tk()
    MA1 = Scale(
        from_=0.2,
        to=100,
        resolution=0.01,
        orient=HORIZONTAL,
        length=800,
        label='Moving Average 1')
    MA2 = Scale(
        from_=0.2,
        to=100,
        resolution=0.01,
        orient=HORIZONTAL,
        length=800,
        label='Moving Average 2')
    v = IntVar()
    scale = Checkbutton(text="LOG SCALE", variable=v)
    scale.var = v
    Label(interface, text="CHART UPDATE WIDGET, DO NOT CLOSE").grid(row=0, column=0)
    MA1.set(10)
    MA2.set(50)
    MA1.pack()
    MA2.pack()
    scale.pack()
    Button(text='UPDATE CHART', command=draw_chart).pack()
    interface.after(1, draw_chart)
    interface.title('PLOT WIDGET: DO NOT CLOSE')
    interface.geometry("0x0+0+0")
    interface.mainloop()

# run nodes latency test as background process
servers = Process(target=nodes_loop)
servers.daemon = True
servers.start()

# sign in
print("\033c")
print('')
print('')
print("")
print("                                     ______   ________  ____  ____  ")
print("                                    (_   _ `.(_   __  |(_  _)(_  _) ")
print("     __  __  ____  ___  ____   ___    | | `. \ | |_ \_|  \ \__/ /   ")
print("    (  \/  )(_  _)/ __)(  _ \ / _ \   | |  | | |  _) _    ) __ (    ")
print("     )    (  _||_( (__  )   /( (_) ) _| |_.' /_| |__/ | _/ /  \ \_  ")
print("    (_/\/\_)(____)\___)(_)\_) \___/ (______.'(________|(____)(____) ")
print('   =================================================================')
print('           ' + VERSION)
print('   =================================================================')
print('')
print('')

valid = 0
while not valid:
    try:
        USERNAME =input('           Account: ')
        account = Account(
            USERNAME,
            bitshares_instance=BitShares(
                nodes,
                num_retries=0))
        valid = 1
    except Exception as ex:
        print (type(ex).__name__, 'try again...')
        pass
print('')
print('      Welcome Back: %s' % account)
print('')
print(' Default market is: %s' % BitPAIR)
print('')
print('Input new Bitshares DEX market below or press ENTER to skip')
print('e.g.: BTS:CNY, BTS:OPEN.BTC, OPEN.LTC:OPEN.BTC, OPEN.BTC:USD')
print('')
valid = 0
default = BitPAIR
while not valid:
    try:
        BitPAIR = input('  Change market to: ') or default
        BitASSET = BitPAIR.split(':')[0]
        BitCURRENCY = BitPAIR.split(':')[1]
        market = Market(
            BitPAIR,
            bitshares_instance=BitShares(
                nodes,
                num_retries=0),
            mode='head')
        valid = 1
    except Exception as ex:
        print (type(ex).__name__, 'try again...')
        pass
print('')
print('Enter PASS PHRASE below to unlock your wallet or press ENTER to skip')
print('')
valid = 0
default = ''
while not valid:
    try:
        PASS_PHRASE = getpass(prompt='       Pass Phrase: ') or default
        if PASS_PHRASE != '':
            market.bitshares.wallet.unlock(PASS_PHRASE)
            print('')
            print('AUTHENTICATED - YOUR WALLET IS UNLOCKED')
            valid = 1
        else:
            print('')
            print('SKIP AUTHENTICATION - YOUR WALLET IS LOCKED')
            valid = 1
    except Exception as ex:
        print (type(ex).__name__, 'try again...')
        pass
print('')
print('Connecting to the Bitshares Distributed Exchange, please wait...')
print('')

# begin several concurrent background processes of launch_book()
BEGIN = int(time.time())
multinode = {}
for a in range(CONNECTIONS):
    multinode[str(a)] = Process(target=launch_book, args=(a,))
    multinode[str(a)].start()
    time.sleep(0.1)

# begin live charts
try:
    c = Process(target=charts)
    c.daemon = True
    c.start()
except:
    print('WARN: plotting only available for crypto altcoins')

time.sleep(2)
print("\033c")
print('')
print('')
print('')
print('initializing microDEX...')

# tkinter primary busybox
time.sleep(15)
master = Tk()
lock = StringVar()
lock.set('UNLOCKED')
if market.bitshares.wallet.locked():
    lock.set('LOCKED')
master.title(VERSION)
Label(master, text="PRICE:").grid(row=0, column=0, sticky=E)
Label(master, text="AMOUNT:").grid(row=1, column=0, sticky=E)
Label(master, text="PRICE:").grid(row=0, column=2, sticky=E)
Label(master, text="AMOUNT:").grid(row=1, column=2, sticky=E)
Label(master, textvariable=lock).grid(row=6, column=2, sticky=W)
Label(master, text=
      "   *ORDERS TAKE A FEW SECONDS TO APPEAR; CLICK ONCE, THEN CONFIRM*"
      ).grid(row=7, column=0, columnspan=4, sticky=W)
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
master.geometry('+550+700')
master.lift()
master.call('wm', 'attributes', '.', '-topmost', True)
mainloop()
