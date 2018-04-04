
# microDEX low latency UI for Bitshares Decentralized Exchange

' (BTS) litpresence1 '

# WTFPLv0 - March 1765

import os
import sys
import time
import warnings
import requests
import datetime
import numpy as np
from tkinter import *
from getpass import getpass
from datetime import datetime
import matplotlib.ticker as tkr
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from random import random, shuffle
from decimal import Decimal as decimal
from ast import literal_eval as literal
from multiprocessing import Process, Value, Array
from bitshares import BitShares
from bitshares.market import Market
from bitshares.account import Account
from bitshares.blockchain import Blockchain

def version():

    global VERSION
    VERSION = 'microDEX v0.00000011 - low latency minimalist UI'

def constants():

    global BitCURRENCY, BitASSET, BitPAIR
    global ID, SATOSHI, ANTISAT, nodes

    # default market
    BitCURRENCY = 'OPEN.BTC'
    BitASSET = 'BTS'
    BitPAIR = BitASSET + ':' + BitCURRENCY
    # mainnet ID
    ID = '4018d7844c78f6a6c41c6a552b898022310fc5dec06da467ee7905a8dad512c8'
    SATOSHI = 0.00000001
    ANTISAT = 1 / SATOSHI
    sys.stdout.write('\x1b]2;' + VERSION + '\x07')
    # default nodes for first use; auto updates thereafter
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

def timing():

    global TIMEOUT, LATENCY_TEST, PAUSE, CONNECTIONS, MASTER, DEV
    TIMEOUT = 180
    LATENCY_TEST = 600
    PAUSE = 0.5
    CONNECTIONS = 8
    MASTER = 10
    DEV = 0  # ALWAYS ZERO WHEN LIVE; SLOWS ANIMATION

def nodes_process(  # sorts nodes for lowest latency
        timeout=5, pings=999, crop=10, write=True,
        include=True, exclude=False, suffix=True, master=False):

    # timeout : seconds to ping until abort per node
    # pings   : number of good nodes to find until satisfied (0 none, 999 all)
    # suffix  : checks each node for no suffix plus with /ws or /wss
    # master  : check only nodes listed in bitshares/ui/master
    # crop    : return only best nodes
    # write   : maintains an output file nodes.txt with list of best nodes

    # include and exclude custom nodes
    included, excluded = [], []
    if include:
        included = []
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
            ping_latency = time.time() - start
            current_block = chain.get_current_block_num()
            blocktimestamp = abs(
                chain.block_timestamp(current_block))  # + utc_offset)
            block_latency = time.time() - blocktimestamp
            if chain.get_network()['chain_id'] != ID:
                num.value = 333333  # testnet
            elif block_latency < (ping_latency + 4):
                num.value = ping_latency
            else:
                num.value = 111111  # stale
        except:
            num.value = 222222  # invalid
            pass

    # gather list of nodes from github
    begin = time.time()
    utc_offset = (datetime.fromtimestamp(begin) -
                  datetime.utcfromtimestamp(begin)).total_seconds()
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
                validated += v
                attempts = 0
            except Exception as e:
                msg = '\n\n' + str(type(e).__name__, e.args, e, u)
                race_append(doc='microDEX_log.txt', text=msg)
                attempts -= 1
                pass

    # remove known bad nodes from test
    if len(excluded):
        excluded = sorted(excluded)
        validated = [i for i in validated if i not in excluded]

    validated = sorted(list(set(validate(parse(clean(validated))))))

    # attempt to contact each websocket
    pinging = min(pings, len(validated))
    if pinging:
        pinged, timed, down, stale, expired, testnet = [], [], [], [], [], []
        for n in validated:
            if len(pinged) < pinging:
                # use multiprocessing module to enforce timeout
                num = Value('d', 999999)
                arr = Array('i', list(range(0)))
                p = Process(target=ping, args=(n, num, arr))
                p.daemon = True
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

        # sort websockets by latency
        pinged = [x for _, x in sorted(zip(timed, pinged))]
        timed = sorted(timed)
        unknown = sorted(
            list(set(validated).difference(
                pinged + down + stale + expired + testnet)))

        ret = pinged[:crop]
    else:
        ret = validated[:crop]

    elapsed = time.time() - begin
    if write and (len(ret) == crop):
        race_write(doc='nodes.txt', text=str(ret))

def nodes_loop():  # repeats nodes process

    while True:
        try:
            nodes_process()
            time.sleep(600)

        # no matter what happens just keep verifying book
        except Exception as e:
            msg = '\n\n' + str(type(e).__name__) + str(e.args) + str(e)
            race_append(doc='microDEX_log.txt', text=msg)
            pass

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

def race_append(doc='', text=''):  # Concurrent Append to File Operation

    opened = 0
    while not opened:
        try:
            with open(doc, 'a+') as f:
                f.write(str(text))
                opened = 1
        except Exception as e:
                print (e, type(e).__name__, e.args)
                print (str(doc) + ' RACE APPEND, try again...')
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
    z = '\n\n' + OFFSET + str(z)
    for i in range(10):
        time.sleep(0.03)
        print("\033c")
        for i in range(50):
            print(z)

def reconnect(BitPAIR, USERNAME, PASS_PHRASE):

    # create fresh websocket connection
    connected = 0
    while not connected:
        # fetch fresh nodes list from subprocess and shuffle it
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
    return account, market, nodes

def book(a=None, b=None):  # updates orderbook data

    account, market, nodes = reconnect(BitPAIR, USERNAME, PASS_PHRASE)
    node = nodes[0]
    begin = time.time()
    while time.time() < (begin + TIMEOUT):
        time.sleep(PAUSE)
        time.sleep(DEV)  # SLOWS ANIMATION FOR DEVELOPMENT
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
                 (int(time.time()) - BEGIN),
                  'EPOCH', b, 'PROCESS', a, '/', CONNECTIONS)
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

        except Exception as ex:
            msg = ('\n\n' + str(time.ctime()) + ' ' + str(type(ex).__name__) +
                   ' BOOK FAILED, RECONNECTING ' + str(node) +
                   ' EPOCH ' + str(b) + ' PROCESS ' + str(a))
            race_append(doc='microDEX_log.txt', text=msg)
            account, market, nodes = reconnect(BitPAIR, USERNAME, PASS_PHRASE)
            pass

def dex_withdraw():

    # FIXME
    # undeveloped definition for withdrawals
    bitshares.transfer(
        to=None,
        amount=None,
        asset=None,
        memo=None,
        account=None)

def dex_buy():

    # update wallet unlock to low latency node
    zprint('BUY')
    account, market, nodes = reconnect(BitPAIR, USERNAME, PASS_PHRASE)
    # attempt buy 10X or until satisfied

    def buy(price, amount, market):
        confirm.destroy()
        zprint('CONFIRMED')
        attempt = 1
        while attempt:
            try:
                msg = market.buy(price, amount)
                msg = ('\n\n' + str(time.ctime()) + ' BUY ' +
                       str(amount) + ' of ' + str(BitPAIR) + ' @ ' +
                       str(price) + '\n' + str(msg))
                print (msg)
                attempt = 0
            except Exception as ex:
                msg = ('\n\n' + str(time.ctime()) + ' ' + str(attempt)
                       + ' ' + str(type(ex).__name__) +
                       ' BUY FAILED, RECONNECTING '
                       + str(nodes[0]) + ' ' + str(price) + ' ' + str(amount))
                zprint(msg)
                race_append(doc='microDEX_log.txt', text=msg)
                account, market, nodes = reconnect(
                    BitPAIR, USERNAME, PASS_PHRASE)
                attempt += 1
                if attempt > 10:
                    zprint('BUY ABORTED')
                    return
                pass
        race_append(doc='microDEX_log.txt', text=msg)

    # interact with tkinter
    confirm = Tk()
    if market.bitshares.wallet.unlocked():
        price = buy_price.get()
        amount = buy_amount.get()
        if price == '':
            price = 1.1 * float(market.ticker()['latest'])
        if amount == '':
            amount = ANTISAT
        try:
            price = decimal(price)
            amount = float(amount)
            currency = float(account.balance(BitCURRENCY))
            if amount > (0.998) * currency / float(price):
                amount = (0.998) * currency / float(price)
            sprice = str(price)[:16]
            samount = str(amount)[:16]
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
                    command=lambda: buy(price, amount, market)).grid(
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

    def sell(price, amount, market):
        confirm.destroy()
        zprint('CONFIRMED')
        attempt = 1
        while attempt:
            try:
                msg = market.sell(price, amount)
                msg = ('\n\n' + str(time.ctime()) + ' SELL ' +
                       str(amount) + ' of ' + str(BitPAIR) + ' @ ' +
                       str(price) + '\n' + str(msg))
                print (msg)
                attempt = 0
            except Exception as ex:
                msg = ('\n\n' + str(time.ctime()) + ' ' + str(attempt)
                       + ' ' + str(type(ex).__name__) +
                       ' SELL FAILED, RECONNECTING '
                       + str(nodes[0]) + ' ' + str(price) + ' ' + str(amount))
                zprint(msg)
                race_append(doc='microDEX_log.txt', text=msg)
                account, market, nodes = reconnect(
                    BitPAIR, USERNAME, PASS_PHRASE)
                attempt += 1
                if attempt > 10:
                    zprint('SELL ABORTED')
                    return
                pass
        race_append(doc='microDEX_log.txt', text=msg)

    # interact with tkinter
    confirm = Tk()
    if market.bitshares.wallet.unlocked():
        price = sell_price.get()
        amount = sell_amount.get()
        if price == '':
            price = 0.9 * float(market.ticker()['latest'])
        if amount == '':
            amount = ANTISAT
        try:
            price = decimal(price)
            amount = float(amount)
            assets = float(account.balance(BitASSET))
            if amount > (0.998 * assets):
                amount = 0.998 * assets
            sprice = str(price)[:16]
            samount = str(amount)[:16]
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
                    command=lambda: sell(price, amount, market)).grid(
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

    def cancel(market):
        confirm.destroy()
        zprint('CONFIRMED')
        attempt = 1
        order_list = []
        for order in orders:
            order_list.append(order['id'])
        while attempt:
            try:
                msg = market.cancel(order_list)
                msg = ('\n\n' + str(time.ctime()) + ' CANCEL ' +
                       str(order_list) + ' of ' + str(BitPAIR) +
                       '\n' + str(msg))
                print (msg)
                attempt = 0
            except Exception as ex:
                msg = ('\n\n' + str(time.ctime()) + ' ' + str(attempt)
                       + ' ' + str(type(ex).__name__) +
                       ' CANCEL FAILED, RECONNECTING '
                       + str(nodes[0]) + ' ' + str(order_list))
                zprint(msg)
                race_append(doc='microDEX_log.txt', text=msg)
                account, market, nodes = reconnect(
                    BitPAIR, USERNAME, PASS_PHRASE)
                attempt += 1
                if attempt > 10:
                    zprint('CANCEL ABORTED')
                    return
                pass
        race_append(doc='microDEX_log.txt', text=msg)

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
                command=lambda: cancel(market)).grid(
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
            # assign each child a random lifespan
            p[str(b)].join(TIMEOUT * 0.5 + TIMEOUT * random())

        except Exception as ex:
            msg = ('\n\n' + str(time.ctime()) + ' ' + str(a, b)
                   + ' ' + str(type(ex).__name__) +
                   ' LAUNCH BOOK')
            race_append(doc='microDEX_log.txt', text=msg)
            pass

def float_sma(array, period):

    def moving_average(array, period):  # numpy array moving average
        csum = np.cumsum(array, dtype=float)
        csum[period:] = csum[period:] - csum[:-period]
        return csum[period - 1:] / period

    if period == int(period):  # simple moving average
        return moving_average(array, int(period))
    else:  # simple moving average w/ decimal period
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
        if d['high'][i] > 3 * d['close'][i]:
                d['high'][i] = 3 * d['close'][i]
        if d['low'][i] < 0.4 * d['close'][i]:
                d['low'][i] = 0.4 * d['close'][i]
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
    ax.yaxis.set_major_formatter(tkr.ScalarFormatter())
    ax.yaxis.set_minor_formatter(tkr.ScalarFormatter())
    ax.yaxis.set_major_formatter(tkr.FormatStrFormatter("%.8f"))
    ax.yaxis.set_minor_formatter(tkr.FormatStrFormatter("%.8f"))
    plt.autoscale(enable=True, axis='y')
    plt.tight_layout()
    if log == 1:
        # manifest 'logarithmic autoscale'
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
        # add sub minor ticks on log scale
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

    # Format X axis
    def timestamp(x, pos):
        return (datetime.fromtimestamp(x)).strftime('%m/%d %H:%M')
    ax.xaxis.set_major_formatter(tkr.FuncFormatter(timestamp))
    plt.gcf().autofmt_xdate(rotation=30)
    plt.gcf().canvas.set_window_title('microDEX CHART')

def charts():

    def draw_chart():
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
        ma1_d_period = float(MA1.get())
        ma2_d_period = float(MA2.get())
        ma1_2h_period = 12.0 * ma1_d_period
        ma2_2h_period = 12.0 * ma2_d_period
        ma1_c1 = float(MA1c1.get())
        ma2_c1 = float(MA2c1.get())
        ma1_2h = float_sma(cex_2h_close, ma1_2h_period)
        ma2_2h = float_sma(cex_2h_close, ma2_2h_period)
        min_len = min(len(ma1_2h), len(ma2_2h))
        ma1_2h = ma1_2h[-min_len:]
        ma2_2h = ma2_2h[-min_len:]
        ma_x_2h = cex_2h_x[-min_len:]
        ma1_2h = [i * ma1_c1 for i in ma1_2h]
        ma2_2h = [i * ma2_c1 for i in ma2_2h]
        if min(ma1_d_period, ma2_d_period) > 2:
            ma1_d = float_sma(cex_d_close, ma1_d_period)
            ma2_d = float_sma(cex_d_close, ma2_d_period)
            min_len = min(len(ma1_d), len(ma2_d))
            ma1_d = ma1_d[-min_len:]
            ma2_d = ma2_d[-min_len:]
            ma_x_d = cex_d_x[-min_len:]
            ma_x_d = [(i + 86400) for i in ma_x_d]
            ma1_d = [i * ma1_c1 for i in ma1_d]
            ma2_d = [i * ma2_c1 for i in ma2_d]

        account, market, nodes = reconnect(BitPAIR, USERNAME, PASS_PHRASE)
        trades = market.trades(limit=100)
        for t in range(len(trades)):
            ts = time.strptime(str(trades[t]['time']), '%Y-%m-%d %H:%M:%S')
            trades[t]['unix'] = int(time.mktime(ts))
        dex_x, dex_y = [], []
        for t in range(len(trades)):
            if float(trades[t]['price']) > 0:
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
        plot_format(log)
        interface.after(300000, draw_chart)  # refresh in milliseconds
        plt.show()
    fig = plt.figure()
    interface = Tk()
    MA1 = Scale(
        from_=0.2,
        to=100,
        resolution=0.01,
        orient=HORIZONTAL,
        length=500)
    MA2 = Scale(
        from_=0.2,
        to=100,
        resolution=0.01,
        orient=HORIZONTAL,
        length=500)
    MA1c1 = Scale(
        from_=0.333,
        to=3,
        resolution=0.01,
        orient=HORIZONTAL,
        length=200)
    MA2c1 = Scale(
        from_=0.333,
        to=3,
        resolution=0.01,
        orient=HORIZONTAL,
        length=200)

    v = IntVar()
    scale = Checkbutton(text="LOG SCALE", variable=v)
    scale.var = v
    MA1.set(10)
    MA2.set(50)
    MA1c1.set(1)
    MA2c1.set(1)
    Label(text='Moving Average 1 and Coeff').pack()
    MA1.pack()
    MA1c1.pack()
    Label(text='Moving Average 2 and Coeff').pack()
    MA2.pack()
    MA2c1.pack()
    scale.pack()
    Button(text='UPDATE CHART', command=draw_chart).pack()
    interface.after(1, draw_chart)
    interface.title('microDEX plot updater')
    interface.geometry("0x0+0+0")
    interface.lift()
    interface.call('wm', 'attributes', '.', '-topmost', True)
    interface.mainloop()

def main():

    global USERNAME, BitPAIR, BitASSET, BitCURRENCY, BEGIN
    global account, market, PASS_PHRASE
    global login, buy_price, buy_amount, sell_price, sell_amount, lock

    version()
    constants()
    timing()

    # run nodes latency test as background process
    servers = Process(target=nodes_loop)
    servers.daemon = False
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
            USERNAME = input('           Account: ')
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
        multinode[str(a)].daemon = False
        multinode[str(a)].start()
        time.sleep(PAUSE)

    # begin live charts
    try:
        c = Process(target=charts)
        c.daemon = True
        c.start()
    except:
        print('WARN: plotting only available for crypto altcoins')

    print("\033c")
    print('')
    print('')
    print('')
    print('initializing microDEX...')

    # tkinter primary busybox
    time.sleep(MASTER)
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

if __name__ == "__main__":

    main()
