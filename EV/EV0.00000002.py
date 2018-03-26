#=======================================================================
VERSION = 'EXTINCTION EVENT v0.00000002 alpha release'
#=======================================================================

# python modules
import os
import sys
import json
import time
import math
import random
import warnings
import requests
import matplotlib
import numpy as np
from random import random, shuffle, randint
from getpass import getpass
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import matplotlib.dates as mdates
from ast import literal_eval as literal
from statistics import mean, median, mode
from multiprocessing import Process, Value, Array

# bitshares modules
from bitshares import BitShares
from bitshares.market import Market
from bitshares.account import Account
from bitshares.blockchain import Blockchain
SATOSHI = 0.00000001
ANTISAT = 1 / SATOSHI

def banner():
    #===================================================================
    '''

    March 2018:

    Possible Hack Of Third-Party Tools Affects Binance Exchange Users.
    : Cointelegraph

    Statement on Potentially Unlawful Online Digital Asset Platforms
    : SEC.gov

    I stand upon the shoulders of giants and as such,
    invite you to stand upon mine.
    Use my work with or without attribution;
    I make no claim of "intellectual property."
    My ideas are the result of countless millenia of evolution
    - they belong to humanity.
    : Jameson Lopp @lopp

    NOTE THIS IS ALPHA RELEASE TO PUBLIC DOMAIN WITH NO WARRANTY

    #
    # https://www.youtube.com/watch?v=5xouOnHxYUw
    # https://www.youtube.com/watch?v=jJxKXOTNXjc
    #
    # Rated R Under 17 NOT Admitted Without Parent
    #
    # My liability is ZERO; "this script licenced: don't be a bitch^TM"
    #
    # WTFPLv2 March 1765
    #

    use this, get lambo, deposit 7.777% skriptbunny tithing here:

    (BTS) litepresence1
    (BTC) 374gjPuhokrWj8KJu8NnMBGzpbHWcVeE1k

    #
    # 0.05 BTC each for AI tuned to last 365 days of any alt/btc pair
    # 1 BTC each for machine optimized algo for top 100 alt/btc pair
    #
    # litepresence @ pastecoin.com for sales
    # finitestate@tutamail for inquiries
    #
    ########################
    #
    # THE DESTROYER,
    # litepresence - 2018
    #

    '''
    #===================================================================
    ''' FEATURES '''
    #===================================================================
    '''

    ALT/BTC data from cryptocompare.com as signal

    Bitshares DEX open.ALT/open.BTC for trading

    - Play simple effective 4 state 50 day cross

        - uses live 2h arrays to generate moving averages
        - ma1xma2 is about 17x50 day simple moving average cross
        - cross plus +/- threshold changes state logic from bull to bear
        - Bull Logic
            buy 17 day support
            sell 17 day x ~1.5 selloff
        - Bear logic
            sell 17 day resistance
            buy 17 day x ~0.75 despair
        - dynamic stoploss upon market shift
        - approximately 7-20 day trade frequency depending upon pair
        - announces machine state on plot

    - Make Markets, Close Margins, Support Trends

    - Iceberg entry and exit

    - Bot runs local

    - Backtest Engine Included

    - Maintains storage from backtest to live session
    '''
    #===================================================================
    ''' FEATURES v0.00000002'''
    #===================================================================
    '''

    Rogue Node Immunity:

        A background daemon process maintains a list of low latency nodes
        for buy/sell/cancel/orders ops in a text file

        distributed exchange prices and orderbook are verified and curated
        using multinode statistical approach with daemon processes

        open orders are checked in triplicate on multiple nodes

        dex() definitions have been upgraded after consultation with
        Bitshares core developers and node admin

    Move to github:

        https://github.com/litepresence/extinction-event

    New MODES:

        SALES mode backtest only plots buy/sell actions; no state machine
        LATENCY mode connect to all nodes and reports on latency
        PAPER mode runs live, but does not trade

    '''
    #===================================================================
    ''' DEPENDENCIES'''
    #===================================================================
    '''
    python 3.4
    python-tk
    matplotlib 1.4
    pybitshares

    h/t @ cryptocompare.com
    '''

# USER CONTROLS

def tune_install():  # Basic User Controls

    global CURRENCY, ASSET, MA1, MA2
    global SELLOFF, SUPPORT, RESISTANCE, DESPAIR
    global MIN_CROSS, MAX_CROSS, BULL_STOP, BEAR_STOP
    global DPT, ROI, APY
    APY = DPT = ROI = 1.0
    CURRENCY = "BTC"

    # INSTALL KEYS
    ASSET = "BTS"
    MA1 = 17.00
    MA2 = 50.00
    SELLOFF = 2.250
    SUPPORT = 1.000
    RESISTANCE = 1.000
    DESPAIR = 0.525
    MIN_CROSS = 1.000
    MAX_CROSS = 1.000
    BULL_STOP = 1.000
    BEAR_STOP = 1.000
    
def control_panel():  # Advanced User Controls

    global LIVE, CURRENCY, ASSET, MA1, MA2, MA3, MA4, RECYCLE
    global PETTY, MIN_MARGIN, TICK, TICK_TIMING, TICK_MINIMUM, DUMP
    global CANDLE, START_ASSETS, START_CURRENCY, ICEBERG
    global ANIMATE, STORAGE_RESET, CURRENCY_STOP, MAX_CURRENCY, PUMP
    global LIVE_PLOT_DEPTH, BELL, FORCE_ALPHA, PAPER, LATENCY
    global DEPTH, BACKTEST, PAIR, MAX_ASSETS, SALES
    global RESOLUTION, OPTIMIZATIONS, MARKET_CROSS, OPTIMIZE, SCALP
    global MANUAL_OVERRIDE, MANUAL_BUY, MANUAL_SELL

    # optimizer
    RESOLUTION = 20
    OPTIMIZATIONS = 10000

    # backtest
    START_ASSETS = 0
    START_CURRENCY = 1

    # initial backtest market state (True is "BULL")
    MARKET_CROSS = True

    # max percent may invest in:
    # 100 = "all in" ; 10 = "10 percent in"
    MAX_ASSETS = 50
    MAX_CURRENCY = 100

    # iceberg
    ICEBERG = 1  # currency terms
    PETTY = 100000  # assets terms

    # scalp thresholds
    # ENTER OWN RISK &&&&
    SCALP = False       # maintain market maker iceberg margins
    PUMP = False        # paint candles green (this costs money)
    DUMP = False        # paint candles red (this costs money)
    RECYCLE = False     # maintain funding for pump/dump ops
    SCALP_FUND = 0.010  # 0.01 = 1% of holdings reserved for scalping
    MIN_MARGIN = 0.030  # about 0.030
    MA3 = 0.500         # about 0.500
    MA4 = 0.166         # about 0.166

    # force buy/sell thresholds manually
    MANUAL_OVERRIDE = False
    MANUAL_BUY = SATOSHI
    MANUAL_SELL = ANTISAT
    # Manual Override Alpha State when live
    FORCE_ALPHA = False  # Options: ( False, 'BULL', 'BEAR' )

    # hft timing in seconds
    TICK = 60
    TICK_TIMING = 51
    TICK_MINIMUM = 30

    # backtest
    ANIMATE = False
    STORAGE_RESET = False
    CURRENCY_STOP = False

    # live window
    LIVE_PLOT_DEPTH = 86400  # 86400 = 1 day
    BELL = False  # sound linux alarm when tick fails

    # constants
    # 0 1 2 3 4 5
    CANDLE = 86400
    OPTIMIZE = BACKTEST = PAPER = LIVE = SALES = LATENCY = False

    if MODE == 0:
        OPTIMIZE = True
    if MODE == 1:
        BACKTEST = True
        OPTIMIZATIONS = 0
    if MODE == 2:
        PAPER = True
        MAX_ASSETS = 0
        MAX_CURRENCY = 0
    if MODE in [2, 3]:
        LIVE = True
        CANDLE = 7200
        OPTIMIZATIONS = 0
        print(('BOT MAY SPEND:     ', MAX_ASSETS, 'PERCENT CURRENCY'))
        print(('BOT MAY LIQUIDATE: ', MAX_CURRENCY, 'PERCENT ASSETS'))
    if MODE == 4:
        BACKTEST = True
        SALES = True
        OPTIMIZATIONS = 0
    if MODE == 5:
        LATENCY = True
    DEPTH = int(max(MA1, MA2) * (86400 / CANDLE) + 50)
    PAIR = ('%s_%s' % (CURRENCY, ASSET))

# BITSHARES DEX

def keys_install():  # Bitshares Keys

    global BitCURRENCY, BitASSET, ACCOUNT, PASS_PHRASE
    global BitPAIR, MARKET, CHAIN, MODE
    MODE = 999
    print('0:OPTIMIZE, 1:BACKTEST, 2:PAPER, 3:LIVE, 4:SALES, 5: LATENCY')
    while MODE not in [0, 1, 2, 3, 4, 5]:
        MODE = int(input('TRADING MODE: '))
    print('')
    BitCURRENCY = 'OPEN.' + CURRENCY
    if ASSET == 'BTS':
        BitASSET = 'BTS'
    else:
        BitASSET = 'OPEN.' + ASSET
    BitPAIR = BitASSET + ":" + BitCURRENCY
    if MODE in [2, 3]:
        try:
            ACCOUNT = Account(input('     account: '))
        except Exception as ex:
            print (type(ex).__name__)
            sys.exit()
        PASS_PHRASE = getpass(prompt=' pass phrase: ')
        n = ['wss://us.nodes.bitshares.works/wss',
             'wss://us.nodes.bitshares.ws/wss',
             'wss://eu-west-1.bts.crypto-bridge.org/wss',
             'wss://eu.nodes.bitshares.ws/wss',
             'wss://us-east-1.bts.crypto-bridge.org/wss']
        MARKET = Market(BitPAIR, bitshares_instance=BitShares(n), mode='head')
        try:
            MARKET.bitshares.wallet.unlock(PASS_PHRASE)
        except Exception as ex:
            print (type(ex).__name__)
            sys.exit()
        print('')
        CHAIN = Blockchain(bitshares_instance=BitShares(n), mode='head')
        nodes_update()

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
            with open('doc', 'a+') as f:
                f.write(str(text))
                opened = 1
        except Exception as e:
                print (e, type(e).__name__, e.args)
                print (str(doc) + ' RACE APPEND, try again...')
                pass

def dex(  # Public AND Private API Bitshares
        command, amount=ANTISAT, price=None,
        depth=1, expiration=ANTISAT):

    attempt = 1
    nds = nodes()
    while attempt:
        try:
            MARKET = Market(
                BitPAIR, bitshares_instance=BitShares(nds), mode='head')
            CHAIN = Blockchain(
                bitshares_instance=BitShares(nds), mode='head')
            MARKET.bitshares.wallet.unlock(PASS_PHRASE)
            ACCOUNT.refresh()
            attempt = 0
        except Exception as ex:
            print (type(ex).__name__, ex.args)
            print (nds)
            print (BitPAIR, attempt, time.ctime())
            attempt += 1
            nd = nds.pop(0)
            nds.append(nd)
            print (nd)
            pass

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

        # cycle through nodes until triplicate-consecutive is found
        servers = nodes()
        orders_list = []
        satisfied = 0
        while not satisfied:
            sorders = [str(i) for i in orders_list]
            if (len(sorders) >= 3) and len(set(sorders[-3:])) == 1:
                orders = orders_list[-1]
                satisfied = 1
            else:
                try:
                    market = Market(
                        BitPAIR,
                        bitshares_instance=BitShares(
                            servers[0],
                            num_retries=0))
                except:
                    print('dex orders server down %s' % server[0])
                    pass
                market.bitshares.wallet.unlock(PASS_PHRASE)
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
                                   'market': BitPAIR,
                                   'amount': amount,
                                   'price': price})
                orders_list.append(orders)
            servers.append(servers.pop(0))  # cycle server list

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

        return race_read('book.txt')

    if command == 'last':

        return race_read('last.txt')

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

        start = time.time()
        current_block = CHAIN.get_current_block_num()
        ping = time.time() - start
        blocktime = CHAIN.block_time(current_block)
        blocktimestamp = CHAIN.block_timestamp(current_block)
        now = time.time()
        block_latency = now - blocktimestamp
        print(('block               :', current_block))
        # print(('blocktime           :', blocktime))
        # print(('stamp               :', blocktimestamp))
        # print(('ctime(stamp)        :', time.ctime(blocktimestamp)))
        # print(('now                 :', now))
        print(('dex blocktime    :', ('%.2f' % block_latency)))
        print(('dex ping         :', ('%.2f' % ping)))
        return current_block, blocktimestamp, block_latency, ping

def nodes():  # Fetch nodes.txt

    return race_read('nodes.txt')

def nodes_process(  # Write nodes.txt
        timeout=20, pings=999999, crop=99, noprint=False, write=False,
        include=False, exclude=False, suffix=True, master=False):

    ID = '4018d7844c78f6a6c41c6a552b898022310fc5dec06da467ee7905a8dad512c8'

    # timeout : seconds to ping until abort per node
    # pings   : # of good nodes to find until satisfied (0 none, 999 all)
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
        print(('%s pinging %s nodes; timeout %s sec; est %.1f minutes' % (
            time.ctime(), pinging, timeout, timeout * len(validated) / 60.0)))
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
        if pinging:
            print('')
            print((len(pinged), 'of', len(validated),
                   'nodes are active with latency less than', timeout))
            print('')
            print(
                ('fastest node',
                 pinged[0],
                    'with latency',
                    ('%.2f' % timed[0])))
            print('')
        ret = pinged[:crop]
    else:
        ret = validated[:crop]
    print ('')
    enablePrint()
    elapsed = time.time() - begin
    print ('elapsed:', ('%.1f' % elapsed), 'TOP ', len(ret))
    print('')
    print (ret)
    if write and (len(ret) == crop):
        race_write('nodes.txt', text=ret)
    return (ret)

def nodes_loop():  # Run nodes process in loop

    while True:
        try:
            nodes_process(
                timeout=5, pings=999, crop=10, noprint=True, write=True,
                include=True, exclude=False, suffix=False, master=False)
            time.sleep(300)

        # no matter what happens just keep verifying book
        except Exception as e:
            print (type(e).__name__, e.args, e)
            pass

def nodes_update():  # Run nodes process once

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
    print('DEX CONNECTION ESTABLISHED - will refresh every 5 minutes')
    print('')

def last_process():  # Write last.txt

    def dex_last(market):  # returns latest price on given market(node)
        return float(market.ticker()['latest'])

    def market(n):  # returns market class using node "n"
        return Market(BitPAIR, bitshares_instance=BitShares(n, num_retries=0))

    # fetch list of good nodes from file maintained by nodes.py
    node_list = nodes()
    # fetch last price from 5 dex nodes
    start = time.time()
    last_list = []
    nodes_used = []
    for i in range(len(node_list)):
        if len(last_list) < 5:
            try:
                m = market(node_list[i])
                ret = satoshi(dex_last(m))
                last_list.append(ret)
                nodes_used.append(node_list[i])
            except:
                pass
    # calculate relative range
    rrange = (max(last_list) - min(last_list)) / mean(last_list)
    # check last list and return best last price with message
    msg = ''
    if len(set(last_list)) == 1:
        last = last_list[-1]
        msg += 'common'
    else:
        try:
            last = mode(last_list)
            msg += 'mode'
        except:
            last = median(last_list)
            msg += 'median'
        # override median or mode with latest if less than 2%
        # difference
        if rrange < 0.02:
            last = last_list[-1]
            msg = 'latest (' + msg + ')'
        else:
            # create blacklist.txt if relative range too wide
            print('')
            print(time.ctime(), str(last), str(rrange))
            print(str(last_list))
            print(str(nodes_used))
            blacklist = ''
            blacklist += "\n" + "\n" + str(time.ctime())
            blacklist += "\n" + str(last)
            blacklist += "\n" + str(rrange)
            blacklist += "\n" + str(last_list)
            blacklist += "\n" + str(nodes_used)
            race_append('blacklist.txt', blacklist)

    # maintain a log of last price, relative range, and statistics type
    last = satoshi(last)
    elapsed = '%.1f' % (time.time() - start)
    print (('%.8f' % last), clock(), 'elapsed: ', elapsed,
           'nodes: ', len(last_list), 'type: ', ('%.3f' % rrange), msg)
    # update communication file last.txt
    race_write('last.txt', text=last)

def last_loop():  # Run last process in loop

    while True:
        try:
            last_process()
            time.sleep(30)

        # no matter what happens just keep verifying book
        except Exception as e:
            print (type(e).__name__, e.args, e)
            pass

def last_update():  # Run last process once

    updated = 0
    try:
        while not updated:
            last_process()
            updated = 1

    # not satisfied until verified once
    except Exception as e:
        print (type(e).__name__, e.args, e)
        pass

def book_process():  # Write book.txt

    DFLOAT = 0.0000000000000001
    NODES = 5

    def dex_book(market, depth=10):  # returns latest orderbook

        # dictionary of 4 lists containing bid/ask volume/price
        raw = market.orderbook(limit=depth)
        bids = raw['bids']
        asks = raw['asks']
        bidp = [float(bids[i]['price']) for i in range(len(bids))]
        bidv = [float(bids[i]['quote']) for i in range(len(bids))]
        askp = [float(asks[i]['price']) for i in range(len(asks))]
        askv = [float(asks[i]['quote']) for i in range(len(asks))]
        book = {'bidp': bidp, 'bidv': bidv, 'askp': askp, 'askv': askv}

        if sum(bidp) > sum(askp):
            print ('WTF IS THIS SHIT?')
            print (book)

        return book

    def market(n):  # returns market class using node "n"
        return Market(BitPAIR, bitshares_instance=BitShares(
            n, num_retries=0))

    tally = {'triple': 0, 'mode': 0, 'median': 0, 'built': 0}
    # fetch list of good nodes from file maintained by nodes.py
    node_list = nodes()
    # fetch last price from 5 dex nodes
    start = time.time()
    middles = []
    book_list = []
    nodes_used = []
    test = []
    msg = ''
    for i in range(len(node_list)):
        triplicate = 0
        if (len(book_list) < NODES) and not triplicate:

            try:
                m = market(node_list[i])
                ret = dex_book(m)
                book_list.append(ret)
                nodes_used.append(node_list[i])
                test.append(i)

            except:
                pass
            sbooks = [str(i) for i in book_list]

            if (len(sbooks) >= 3) and len(set(sbooks[-3:])) == 1:
                book = book_list[-1]
                asksort = sorted(book['askp'])
                bidsort = sorted(book['bidp'], reverse=True)
                if ((asksort == book['askp']) and
                    (bidsort == book['bidp']) and
                    (len(set(asksort)) == len(asksort)) and
                    (len(set(bidsort)) == len(bidsort)) and
                        (bidsort[0] < asksort[0])):
                    msg += 'triplicate book'
                    triplicate = 1
                    tally['triple'] += 1
                    break
                else:
                    msg += 'triplicate book error - '

    if triplicate == 0:
        # check last list and return best last price with message
        try:
            book = literal(mode([str(i) for i in book_list]))
            asksort = sorted(book['askp'])
            bidsort = sorted(book['bidp'], reverse=True)
            if 0:
                if (asksort != book['askp']):
                    print('asksort')
                if (bidsort != book['bidp']):
                    print('bidsort')
                if (len(set(asksort)) != len(asksort)):
                    print('askmatch')
                if (len(set(bidsort)) != len(bidsort)):
                    print('bidmatch')
                if (bidsort[0] > asksort[0]):
                    print('mismatched')
            if ((asksort == book['askp']) and
                (bidsort == book['bidp']) and
                (len(set(asksort)) == len(asksort)) and
                (len(set(bidsort)) == len(bidsort)) and
                    (bidsort[0] < asksort[0])):
                msg += 'mode book'
                tally['mode'] += 1
            else:
                raise
        except:

            book = {i: list(np.median([x[i] for x in book_list], axis=0))
                    for i in ['bidp', 'bidv', 'askp', 'askv']}
            asksort = sorted(book['askp'])
            bidsort = sorted(book['bidp'], reverse=True)
            if 0:
                if (asksort != book['askp']):
                    print('asksort')
                if (bidsort != book['bidp']):
                    print('bidsort')
                if (len(set(asksort)) != len(asksort)):
                    print('askmatch')
                if (len(set(bidsort)) != len(bidsort)):
                    print('bidmatch')
                if (bidsort[0] > asksort[0]):
                    print('mismatched')
            if ((asksort == book['askp']) and
                (bidsort == book['bidp']) and
                (len(set(asksort)) == len(asksort)) and
                (len(set(bidsort)) == len(bidsort)) and
                    (bidsort[0] < asksort[0])):
                    msg += '!!! MEDIAN BOOK !!!'
                    tally['median'] += 1

            else:
                # print ((book['bidp'][:3])[::-1], 'BIDS <> ASKS',
                # book['askp'][:3],1)
                msg += '!!! RECONSTRUCTED BOOK !!!                  *****'
                tally['built'] += 1
                # assure median comprehension did not reorganize book
                # prices
                prices = []
                prices = prices + book['askp'] + book['bidp']
                prices = sorted(prices)
                z = len(prices)
                book['askp'] = prices[int(z / 2):z]
                book['bidp'] = prices[0:int(z / 2)]
                book['askp'] = sorted(book['askp'])
                book['bidp'] = sorted(book['bidp'], reverse=True)
                # print ((book['bidp'][:3])[::-1], 'BIDS <> ASKS',
                # book['askp'][:3],2)
                if book['bidp'][0] == book['askp'][0]:
                    book['askp'] = [(i + DFLOAT)
                                    for i in book['askp']]
                    book['bidp'] = [(i - DFLOAT)
                                    for i in book['bidp']]
                # print ((book['bidp'][:3])[::-1], 'BIDS <> ASKS',
                # book['askp'][:3],3)
                for i in list(range(1, len(book['askp']))):
                    if book['askp'][i] <= book['askp'][i - 1]:
                        book['askp'][i] = max(
                            (book['askp'][i - 1] + DFLOAT),
                            book['askp'][i])
                # print ((book['bidp'][:3])[::-1], 'BIDS <> ASKS',
                # book['askp'][:3],4)
                for i in list(range(1, len(book['bidp']))):
                    if book['bidp'][i] >= book['bidp'][i - 1]:
                        book['bidp'][i] = min(
                            book['bidp'][i - 1] - DFLOAT,
                            book['bidp'][i])
                # print ((book['bidp'][:3])[::-1], 'BIDS <> ASKS',
                # book['askp'][:3],4)

    rrange = (sum(book['bidp']) + sum(book['askp'])) / (
        (len(book['bidp']) + len(book['askp']))) / (
        ((book['bidp'][0]) + (book['askp'][0]) / 2))

    # maintain a log of last price, relative range, and statistics type
    elapsed = '%.1f' % (time.time() - start)
    '''
    sbids = [('%.8f' % i) for i in book['bidp'][:3]]
    sbids = sbids[::-1]
    sasks = [('%.8f' % i) for i in book['askp'][:3]]
    print (sbids, 'BIDS <> ASKS', sasks)
    '''
    try:

        s = sum(tally.values())
        ptally = {k: ('%.2f' % (v / s)) for k, v in tally.items()}
        # print (tally)
        # print (clock(), ptally, 'elapsed: ', elapsed,
        #       'nodes: ', len(book_list), 'type: ',
        #       ('%.3f' % rrange), msg)

    except:
        pass
    # update communication file book.txt
    race_write('book.txt', text=book)

def book_loop():  # Run book process in loop

    while True:
        try:
            book_process()
            time.sleep(30)

        # no matter what happens just keep verifying book
        except Exception as e:
            print (type(e).__name__, e.args, e)
            pass

def book_update():  # Run book process once

    updated = 0
    try:
        while not updated:
            book_process()
            updated = 1

    # not satisfied until verified once
    except Exception as e:
        print (type(e).__name__, e.args, e)
        pass

# CANDLES

def backtest_candles(pair, start, stop, candle):  # HLOCV arrays

    # gather complete dataset so only one API call is required
    raw = chartdata(pair, start, stop, candle)
    d = {}
    d['unix'] = []
    d['high'] = []
    d['low'] = []
    d['open'] = []
    d['close'] = []
    for i in range(len(raw)):
        d['unix'].append(raw[i]['time'])
        d['high'].append(raw[i]['high'])
        d['low'].append(raw[i]['low'])
        d['open'].append(raw[i]['open'])
        d['close'].append(raw[i]['close'])
    d['unix'] = np.array(d['unix'])
    d['high'] = np.array(d['high'])
    d['low'] = np.array(d['low'])
    d['open'] = np.array(d['open'])
    d['close'] = np.array(d['close'])

    # normalize high and low data
    for i in range(len(d['close'])):
        if d['high'][i] > 2 * d['close'][i]:
            d['high'][i] = 2 * d['close'][i]
        if d['low'][i] < 0.5 * d['close'][i]:
            d['low'][i] = 0.5 * d['close'][i]

    return d

def slice_candles(now, data):  # Window backtest arrays

    # window backtest_candles() data to test each candle
    d = {}
    for i in range(len(data['unix'])):
        if now <= data['unix'][i] < (now + CANDLE):
            h = []
            l = []
            o = []
            c = []
            for j in range(DEPTH):
                try:
                    h.append(data['high'][i - j])
                    l.append(data['low'][i - j])
                    o.append(data['open'][i - j])
                    c.append(data['close'][i - j])
                except:
                    print("append failed")
                    pass
            # print close
            d['high'] = np.array(h[::-1])
            d['low'] = np.array(l[::-1])
            d['open'] = np.array(o[::-1])
            d['close'] = np.array(c[::-1])
    return d

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
    d['unix'] = np.array(d['unix'][-depth:])
    d['high'] = np.array(d['high'][-depth:])
    d['low'] = np.array(d['low'][-depth:])
    d['open'] = np.array(d['open'][-depth:])
    d['close'] = np.array(d['close'][-depth:])
    d['volume'] = np.array(d['volume'][-depth:])

    return d

def chartdata(pair, start, stop, period):  # Public API cryptocompare

    #{"time","close","high","low","open","volumefrom","volumeto"}
    # docs at https://www.cryptocompare.com/api/
    # print(('API call for chartdata %s %ss %se CANDLE %s DAYS %s' % (
    #    pair, start, stop, period, int((stop - start) / 86400.0))))

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
            clean_d = clean_d1 + clean_d2
            clean_d = [i for i in clean_d if i['time'] > start]
            print((len(clean_d),
                 (clean_d2[-1]['time'], clean_d1[0]['time']),
                (clean_d1[0]['time'] - clean_d2[-1]['time'])))
            print()
        return clean_d

    else:
        print('invalid period')
        return None

def currencies():  # Public API cryptocompare

    uri = 'https://min-api.cryptocompare.com/data/all/coinlist'
    params = {}
    ret = requests.get(uri, params=params).json()
    print(('API currencies', len(ret['Data']),
           'coins at cryptocompare'))
    return ret['Data']

def cryptocompare_time():  # CEX latency test

    try:
        # print('Cryptocompare API candle time')
        uri = 'https://www.cryptocompare.com/api/data/coinsnapshot'
        params = {'fsym': ASSET, 'tsym': CURRENCY}
        ret = requests.get(uri, params=params).json()
        timestamps = []
        for i in range(len(ret['Data']['Exchanges'])):
            timestamps.append(float(
                ret['Data']['Exchanges'][i]['LASTUPDATE']))
        cc_time = max(timestamps)
        latency = time.time() - cc_time
        print(('candle latency      :', ('%.2f' % latency)))
        return latency
    except:
        return -1

def cryptocompare_last():  # CEX last price

    # print('Cryptocompare API last')
    uri = 'https://min-api.cryptocompare.com/data/pricemultifull'
    params = {'fsyms': ASSET, 'tsyms': CURRENCY}
    ret = requests.get(uri, params=params).json()
    raw = ret['RAW'][ASSET][CURRENCY]
    price = float(raw['PRICE'])
    volume = float(raw['LASTVOLUME'])
    cc_time = float(raw['LASTUPDATE'])
    latency = time.time() - cc_time
    print(('cex_rate latency    :', ('%.2f' % latency)))
    return price, volume, latency

def marketcap():  # Public API coinmarketcap

    asset_cap = asset_dominance = asset_rank = 0
    print('API marketcap')
    uri = 'https://api.coinmarketcap.com/v1/ticker/'
    params = {'limit': 0}
    caps = requests.get(uri, params=params).json()
    asset_cap = 0
    total_cap = 0
    for c in caps:
        if c['market_cap_usd'] is None:
            cap = 0
        else:
            cap = float(c['market_cap_usd']) / 1000000.0
        if c['symbol'] == ASSET:
            asset_cap = cap
            asset_rank = c['rank']
        total_cap += cap

    asset_dominance = 100 * asset_cap / total_cap
    return asset_cap, asset_dominance, asset_rank

# LIVE

def live_initialize():  # Begin live session

    print(VERSION)
    print('~====== BEGIN LIVE SESSION =====================~')
    global storage
    global portfolio
    global info
    global data
    info = {}
    data = {}
    portfolio = {}
    if STORAGE_RESET:
        storage = {}

    # initialize storage
    storage['trades'] = 0
    storage['HFT'] = False
    storage['previous_v'] = SATOSHI
    # initialize info
    info['begin'] = int(time.time())
    info['tick'] = 0
    info['five_minute'] = 0
    info['hour'] = 0
    info['day'] = 0
    info['current_time'] = info['begin']
    info['completion_time'] = info['begin'] - 60
    info['end'] = None
    info['live'] = True

    live_chart_latest()
    plot_format()

def live():  # Primary live event loop

    global storage
    live_initialize()
    attempt = 0
    msg = ''

    while True:

        plt.pause(1)  # prevent inadvertent attack on API's
        info['current_time'] = now = int(time.time())
        print('')
        print(('______________________________%s_cex %s_dex %s' %
             (ASSET, BitASSET, time.ctime())))
        print('')

        # DEBUG LIVE SESSION
        debug = 0
        if debug:
            dex('blocktime')
            price, volume, latency = cryptocompare_last()
            storage['cc_last'] = {
                'price': price, 'volume': volume, 'latency': latency}
            cryptocompare_time()
            live_data()
            indicators()
            state_machine()
            hourly()
            daily()
            trade()
            scalp()
            live_chart()
            plot_format()
            live_plot()
            time.sleep(10)

        else:

            # RAISE ALARM
            if attempt > 2:
                time_msg = datetime.fromtimestamp(
                    now).strftime('%H:%M')
                print(
                    ('%s FAIL @@@@@@@ ATTEMPT: %s %s' %
                     (msg, attempt, time_msg)))
                if BELL:
                    bell(attempt, 432)
            # GATHER AND POST PROCESS DATA
            try:
                dex('blocktime')
            except:
                msg += 'dex(blocktime) '
                attempt += 1
                continue
            try:
                price, volume, latency = cryptocompare_last()
                storage['cc_last'] = {
                    'price': price, 'volume': volume, 'latency': latency}
            except:
                msg += 'cryptocompare_last() '
                attempt += 1
                continue
            try:
                cryptocompare_time()
            except:
                msg += 'cryptocompare_time() '
                attempt += 1
                continue
            print('')
            try:
                live_data()
            except:
                msg += 'live_data() '
                attempt += 1
                continue
            try:
                indicators()
            except:
                msg += 'indicators() '
                attempt += 1
                continue
            try:
                state_machine()
            except:
                msg += 'state_machine() '
                attempt += 1
                continue
            # LOWER FREQENCY EVENTS
            check_hour = (info['current_time'] - info['begin']) / 3600.0
            if check_hour > info['hour']:

                try:
                    hourly()
                    info['hour'] += 1
                except:
                    msg += 'hourly() '
                    attempt += 1
                    continue
            check_day = (info['current_time'] - info['begin']) / 86400.0
            if check_day > info['day']:
                try:
                    daily()
                    info['day'] += 1
                except:
                    msg += 'daily() '
                    attempt += 1
                    continue
            # TRADE
            try:
                trade()
            except:
                msg += 'trade() '
                attempt += 1
                continue
            # SCALP
            try:
                scalp()
            except:
                msg += 'scalp() '
                attempt += 1
                continue
            # PLOT
            try:
                live_chart()
            except:
                msg += 'live_chart() '
                attempt += 1
                continue
            try:
                plot_format()
            except:
                msg += 'plot_format() '
                attempt += 1
                continue
            try:
                live_plot()
            except:
                msg += 'live_plot() '
                attempt += 1
                continue

            # END PRIMARY TICK
            msg = ''
            info['tick'] += 1
            info['completion_time'] = int(time.time())
            attempt = 0

            # DELAY NEXT TICK
            if not PUMP:
                if storage['HFT']:
                    print('HFT True')
                    set_timing()
                else:
                    plt.pause(300)

def set_timing():  # Limits HFT to 1 minute interval at end of minute

    now = time.time()
    elapsed = now - info['begin']
    minutes = math.floor(elapsed / TICK)
    tick_elapsed = now - info['completion_time']
    if (info['tick'] + 1) > minutes:
        wait = max(0, (TICK_TIMING - (time.time() % TICK)))
        print(('standard wait: %.2f' % wait))
        if wait > 0:
            plt.pause(wait)
    elif tick_elapsed < TICK_MINIMUM:
        wait = TICK_MINIMUM - tick_elapsed
        print(('minimum wait: %.2f' % wait))
        if wait > 0:
            plt.pause(wait)
    else:
        print ('skip set_timing(); no wait')
    drift = ((time.time() - info['begin']) - info['tick'] * TICK -
             TICK_TIMING + info['begin'] % TICK)
    drift_minutes = int(drift // TICK)
    print(('drift: %.6f drift minutes %s' % (drift, drift_minutes)))

def live_data():  # Gather live data from public and private api

    global portfolio
    global data
    global storage

    # populate 2h candles, 5m candles, and market rate
    data['7200'] = live_candles(PAIR, candle=7200, depth=int(MA2 * 13))
    data['300'] = live_candles(PAIR, candle=300, depth=300)
    cex_rate = storage['cex_rate'] = storage['cc_last']['price']
    dex_rate = storage['dex_rate'] = dex('last')

    print('')
    print(('cex_rate: ', ('%.8f' % cex_rate)))
    print(('dex_rate: ', ('%.8f' % dex_rate)))
    print(('delta   : ', ('%.8f' % (cex_rate - dex_rate))))
    print('')

    # update portfolio assets and currency
    market_balances = dex('market_balances')
    portfolio['currency'] = market_balances['currency']
    portfolio['assets'] = market_balances['assets']
    # Check bitcoin value of account
    bts, btc, usd = dex('account_value')
    portfolio['btcValue'] = btc
    # derive value of assets held and percent invested
    portfolio['btcValue_asset'] = cex_rate * portfolio['assets']
    portfolio['percent_invested'] = portfolio['btcValue_asset'] / btc

    print(('%.2f Bitcoin Value Portfolio' % portfolio['btcValue']))
    print(('%.2f Bitcoin Value Asset' % portfolio['btcValue_asset']))
    print(('%.2f Percent Invested' % portfolio['percent_invested']))

def scalp():  # Initiate secondary order placement

    # localize data
    global storage
    now = int(time.time())
    ask_p = book['askp'][0]
    ask_v = book['askv'][0]
    bid_p = book['bidp'][0]
    bid_v = book['bidv'][0]
    ask_p2 = book['askp'][1]
    bid_p2 = book['bidp'][1]
    cex_rate = storage['cex_rate']
    dex_rate = storage['dex_rate']
    assets = portfolio['assets']
    buying = storage['buying']
    selling = storage['selling']
    high = storage['high']
    low = storage['low']
    asset_ratio = storage['asset_ratio']
    currency = portfolio['currency']
    means = storage['means']
    ma3 = storage['ma3'][-1]
    ma4 = storage['ma4'][-1]
    market_cross = storage['market_cross']
    asset_ratio = storage['asset_ratio']
    mid_market = storage['mid_market']
    min_order = 0.00011 / dex_rate
    max_currency = storage['max_currency']
    max_assets = storage['max_assets']

    # alpha pump/dump signal
    penny = None
    if cex_rate > mid_market:  # RUNNING TO TOP
        if asset_ratio > 0.10:  # if any assets
            penny = 'pump'
        if asset_ratio < 0.10:  # if not much assets
            penny = 'dump'
    if cex_rate < mid_market:  # IF FALLING TO SUPPORT
        if asset_ratio < 0.90:  # if any currency
            penny = 'dump'
        if asset_ratio > 0.90:  # if not much currency
            penny = 'pump'

    # random List integers for scalp placement
    x = [i for i in range(4)]
    shuffle(x)

    # define scalp support and resistance
    scalp_resistance = max(high, ma3, ma4)
    scalp_support = min(low, ma3, ma4)

    # limit scalp ops to buying/selling window
    max_scalp_support = ((1 - MIN_MARGIN) * selling)  # 97% of selling
    min_scalp_resistance = ((1 + MIN_MARGIN) * buying)  # 103% of buying
    scalp_support = min(scalp_support, max_scalp_support)
    scalp_resistance = max(scalp_resistance, min_scalp_resistance)

    # limit scalp ops to dex bid/ask
    scalp_resistance = max(scalp_resistance, bid_p)
    scalp_support = min(scalp_support, ask_p)

    # adjust scalp margins if too thin
    scalp_margin = (scalp_resistance - scalp_support) / scalp_support
    if scalp_margin < MIN_MARGIN:
        if penny == 'pump':
            scalp_resistance = (1 + MIN_MARGIN) * scalp_support
        if penny == 'dump':
            scalp_support = (1 - MIN_MARGIN) * scalp_resistance
        if penny is None:
            midscalp = (scalp_resistance + scalp_support)
            scalp_resistance = (1 + MIN_MARGIN / 2) * midscalp
            scalp_support = (1 - MIN_MARGIN / 2) * midscalp

    # store scalp thresholds globally
    storage['scalp_resistance'] = scalp_resistance
    storage['scalp_support'] = scalp_support

    if RECYCLE:
        if penny == 'pump':
            # recycle currency
            if asset_ratio > (1 - SCALP_FUND):
                qty = SCALP_FUND * max_currency * scalp_resistance
                qty -= currency * scalp_resistance
                print('RECYCLE CURRENCY')
                print(('price %.8f qty %s' % (scalp_resistance, qty)))
                try:
                    dex('sell', price=scalp_resistance, amount=qty)
                    plt.plot(
                        now, scalp_resistance,
                        markersize=2 * math.log10(qty),
                        marker='v', ls='', color='red',
                        label='RECYCLE')
                except:
                    pass

        if penny == 'dump':
            # recycle assets
            if asset_ratio < SCALP_FUND:
                qty = SCALP_FUND * max_currency * scalp_support
                qty -= assets
                print('RECYCLE ASSETS')
                print(('price %.8f qty %s' % (scalp_support, qty)))
                try:
                    dex('buy', price=scalp_support, amount=qty)
                    plt.plot(
                        now, scalp_support,
                        markersize=2 * math.log10(qty),
                        marker='^', ls='', color='lime',
                        label='RECYCLE')
                except:
                    pass

    if SCALP:
        if penny == 'pump':
            for i in x:
                # SCALP BUY
                scalp = scalp_support - i * SATOSHI
                qty = (0.0001 / scalp) * 10
                qty = (qty * (1 + random())) * (1 + i)
                try:
                    dex('buy', price=scalp, amount=qty)
                except:
                    pass
                # SCALP SELL
                scalp = scalp_resistance + i * SATOSHI
                qty = (0.0001 / scalp) * 10
                qty = (qty * (1 + random())) * (1 + i)
                try:
                    dex('sell', price=scalp, amount=qty)
                except:
                    pass

        if penny == 'dump':
            for i in x:
                # SCALP BUY
                scalp = scalp_support - i * SATOSHI
                qty = (0.0001 / scalp) * 10
                qty = (qty * (1 + random())) * (1 + i)
                try:
                    dex('buy', price=scalp, amount=qty)
                except:
                    pass
                # SCALP SELL
                scalp = scalp_resistance + i * SATOSHI
                qty = (0.0001 / scalp) * 10
                qty = (qty * (1 + random())) * (1 + i)
                try:
                    dex('sell', price=scalp, amount=qty)
                except:
                    pass

    if PUMP:
        if penny == 'pump':
            set_timing()
            # clear spam pump
            if ask_v < 5 * (0.00011 / cex_rate):
                qty1 = (ask_v)           # spam size
                qty2 = (0.00011 / cex_rate)  # min order
                qty = max(qty1, qty2)
                print('PUMP 1 - CLEAR SPAM')
                print(('pump %.8f qty %.8f' % (ask_p2, qty)))
                try:
                    dex('buy', price=ask_p2, amount=qty)
                    dex('buy', price=(ask_p - SATOSHI), amount=qty2)
                    plt.plot(now, ask_p, markersize=5 * math.log10(qty),
                             marker='^', ls='', color='lime', label='SPAM')
                except:
                    pass
            # walk forward pump
            elif (ask_p > cex_rate) or (storage['recycle_trigger']):
                qty = (0.00011 / cex_rate)
                print('PUMP 2 - WALK FORWARD')
                print(('pump %.8f qty %.8f' % (ask_p, qty)))
                try:
                    dex('buy', price=ask_p2, amount=qty)
                    dex('buy', price=(ask_p - SATOSHI), amount=qty)
                    plt.plot(now, ask_p, markersize=5 * math.log10(qty),
                             marker='^', ls='', color='lime', label='WALK')
                except:
                    pass
            # close gap pump
            elif (ask_p - bid_p > 3 * SATOSHI):
                qty = (0.00011 / cex_rate)
                r = (ask_p - SATOSHI)
                print('PUMP 3 - CLOSE GAP')
                print(('pump %.8f qty %.8f' % (r, qty)))
                try:
                    dex('buy', price=r, amount=qty)
                    plt.plot(now, r, markersize=5 * math.log10(qty),
                             marker='^', ls='', color='lime', label='WALK')
                except:
                    pass

        if penny == 'dump':
            set_timing()
            # clear spam dump
            if bid_v < 0.350:
                qty1 = bid_v           # spam size
                qty2 = (0.00011 / bid_p)  # min order
                qty = max(qty1, qty2)
                print('DUMP 1 - CLEAR SPAM')
                print(('dump %.8f qty %s' % (bid_p2, qty)))
                try:
                    dex('sell', price=bid_p2, amount=qty)
                    plt.plot(now, bid_p2, markersize=5 * math.log10(qty),
                             marker='v', ls='', color='red', label='SPAM')
                except:
                    pass
            # walk forward dump
            elif (bid_p < cex_rate) or (storage['recycle_trigger']):
                qty = (0.00011 / bid_p)
                print('DUMP 2 - WALK FORWARD')
                print(('dump %.8f qty %s' % (bid_p, qty)))
                try:
                    dex('sell', price=bid_p2, amount=qty)
                    plt.plot(now, bid_p, markersize=5 * math.log10(qty),
                             marker='v', ls='', color='red', label='WALK')
                except:
                    pass
            # close gap dump
            elif (ask_p - bid_p > 3 * SATOSHI):
                qty = (0.00011 / cex_rate)
                r = (bid_p + SATOSHI)
                print('DUMP 3 - CLOSE GAP')
                print(('dump %.8f qty %.8f' % (r, qty)))
                try:
                    dex('sell', price=r, amount=qty)
                    plt.plot(now, r, markersize=5 * math.log10(qty),
                             marker='^', ls='', color='lime', label='WALK')
                except:
                    pass

    # Print trade pair and time
    time_LOCAL = datetime.fromtimestamp(
        int(time.time())).strftime('%H:%M:%S')
    time_UTC = datetime.fromtimestamp(
        int(time.time()) + 18000).strftime('%H:%M:%S')
    print(('%.2f %s %.2f %s' % (currency, CURRENCY, assets, ASSET)))
    print(('%s UTC                                             %s' %
         (time_UTC, time_LOCAL)))
    print(('(buying: %.8f selling %.8f) (scalp buy %.8f, scalp sell %.8f)' %
         (buying, selling, scalp_support, scalp_resistance)))

def trade():  # Initiate primary order placement

    global storage
    # localize data
    buying = storage['buying']
    selling = storage['selling']
    mid_market = storage['mid_market']
    market_cross = storage['market_cross']
    buying_r = buying
    selling_r = selling

    if info['live']:  # localize additional data for live session

        storage['recycle_trigger'] = False
        ask_p = book['askp'][0]
        bid_p = book['bidp'][0]
        dex_rate = storage['dex_rate']
        cex_rate = storage['cex_rate']
        assets = portfolio['assets']
        asset_ratio = storage['asset_ratio']
        means = storage['means']
        invested = portfolio['percent_invested']
        divested = 100 - invested
        min_order = 0.00011 / dex_rate
        dex('cancel')

        max_assets = (MAX_ASSETS / 100.0) * portfolio['btcValue'] / dex_rate
        max_currency = (MAX_CURRENCY / 100.0) * portfolio['btcValue']

        print(('assets %.1f, max assets %.1f' % (assets, max_assets)))
        pieces = 10.0  # order size

        if MANUAL_OVERRIDE:
            storage['selling'] = selling = MANUAL_SELL
            storage['buying'] = buying = MANUAL_BUY

        storage['HFT'] = False
        if SCALP or DUMP or PUMP or RECYCLE:
            storage['HFT'] = True

        qty = max_assets / pieces
        if (dex_rate > 0.90 * selling):
            print('APPROACHING SELL POINT')
            if BELL:
                bell(0.5, 800)
            if (portfolio['assets'] > 0.1):
                if (divested < MAX_CURRENCY):
                    storage['HFT'] = True
                    selling_r = max(selling, (dex_rate + ask_p) / 2)
                    try:
                        # iceberg
                        dex('sell', price=selling_r, amount=qty)
                        print(
                            ('SELLING', PAIR, 'RATE', ('%.8f' %
                             selling_r), 'AMOUNT', ('%.1f' %
                             qty)))
                        # liquidate
                        if portfolio['assets'] < qty:
                            qty = (portfolio['assets'] - SATOSHI)
                        # iceberg
                        dex('sell', price=selling_r, amount=qty)
                        print(
                            ('SELLING', PAIR, 'RATE', ('%.8f' %
                             selling_r), 'AMOUNT', ('%.1f' %
                             qty)))
                        # iceberg front limit
                        selling_r *= 0.985
                        qty /= 92.0
                        if random() > 0.5:
                            dex('sell', price=selling_r, amount=qty)
                            print(
                                ('SELLING', PAIR, 'RATE', ('%.8f' %
                                 selling_r), 'AMOUNT', ('%.1f' %
                                 qty)))
                    except:
                        print('SELL FAILED')
                        pass
                else:
                    print('MAX DIVESTED')
            else:
                print('NO ASSETS')

        qty = max_assets / pieces
        if dex_rate < 1.20 * buying:
            print('APPROACHING BUY POINT')
            if BELL:
                bell(0.5, 800)
            if (portfolio['currency'] > 0.1):
                if (invested < MAX_ASSETS):
                    storage['HFT'] = True
                    buying_r = min(buying, (dex_rate + bid_p) / 2)
                    try:
                        dex('buy', price=buying_r, amount=qty)
                        print(
                            ('BUYING', PAIR, 'RATE', ('%.8f' %
                             buying_r), 'AMOUNT', ('%.1f' %
                             qty)))
                        buying_r *= 1.015
                        qty /= 92.0
                        if random() > 0.5:
                            dex('buy', price=buying_r, amount=qty)
                            print(
                                ('BUYING', PAIR, 'RATE', ('%.8f' %
                                 buying_r), 'AMOUNT', ('%.1f' %
                                 qty)))
                    except:
                        print('buy FAIL')
                        pass
                else:
                    print('MAX INVESTED')
            else:
                print ('NO CURRENCY')

    else:
        # test trade
        if portfolio['currency'] > 0:
            if (storage['low'][-1] < buying):

                buying_r = min(storage['high'][-1], buying)
                test_buy(buying_r)

        elif portfolio['assets'] > 0:
            if storage['high'][-1] > selling:
                selling_r = max(storage['low'][-1], selling)
                test_sell(selling_r)

def hourly():  # Do this every hour
    now = int(time.time())
    cex_rate = storage['cex_rate']
    print(('hour: %s' % info['hour']))
    plt.plot(now, cex_rate, markersize=5, marker='.',
             color='white', label='daily')

def daily():  # Do this every day
    now = int(time.time())
    cex_rate = storage['cex_rate']
    print(('day: %s' % info['day']))
    plt.plot(now, cex_rate, markersize=10, marker='.',
             color='white', label='daily')

# BACKTEST

def initialize():  # Open plot, set backtest days

    global DAYS

    if MODE == 0:
        print('~=== OPTIMIZING ======================~')
    if MODE == 1:
        print('~=== BEGIN BACKTEST ==================~')
    if MODE == 2:
        print('~=== WARMING UP PAPER SESSION ========~')
    if MODE == 3:
        print('~=== WARMING UP LIVE MACHINE =========~')
    if MODE == 4:
        print('~=== BEGIN SALES BACKTEST ============~')

    if LIVE:
        DAYS = 90
    else:
        DAYS = len(chartdata(PAIR, 1390000000, int(time.time()), 86400))
        if ASSET == 'BTS':  # filter glitch in dataset
            DAYS -= 250
            if CURRENCY == 'BITCNY':
                DAYS -= 200
        elif ASSET == 'DASH':  # filter glitch in dataset
            DAYS -= 360
        elif ASSET == 'NXT':  # filter glitch in dataset
            DAYS -= 300
        else:
            DAYS -= 100

    if (SALES or OPTIMIZE) and (DAYS >= 365):
        DAYS = 365
    if LIVE or BACKTEST:
        plt.ion()
        fig = plt.figure()
        fig.patch.set_facecolor('0.15')

def holdings():  # Calculate starting portfolio

    if info['tick'] == 0:
        close = data['close'][-DAYS]
    else:
        close = storage['close'][-1]

    storage['max_assets'] = (portfolio['assets'] +
                             (portfolio['currency'] / close))
    storage['max_currency'] = (portfolio['currency'] +
                               (portfolio['assets'] * close))

    if info['tick'] == 0:
        storage['begin_max_assets'] = storage['max_assets']
        storage['begin_max_currency'] = storage['max_currency']
        storage['start_price'] = close

def test_initialize():  # Begin backtest session

    now = int(time.time())

    global storage
    global portfolio
    global info
    global data
    # initialize storage
    storage['trades'] = 0
    storage['buys'] = [[], []]
    storage['sells'] = [[], []]
    # initialize portfolio balances
    portfolio['assets'] = float(START_ASSETS)
    portfolio['currency'] = float(START_CURRENCY)
    # initialize info dictionary objects
    info['begin'] = now - DAYS * 86400
    info['end'] = now
    info['tick'] = 0
    info['current_time'] = info['begin']
    info['origin'] = info['begin'] - int(1.1 * MA2 * 86400)
    info['live'] = False

    print(('Dataset.....: %s DAYS' %
           int((now - info['origin']) / 86400.0)))
    print(('Backtesting.: %s DAYS' %
           int((now - info['begin']) / 86400.0)))

    # check for compatible interval
    if CANDLE not in [300, 900, 1800, 7200, 14400, 86400]:
        print(('Tick Interval must be in [300, 900,' +
               '1800, 7200, 14400, 86400]'))
        raise stop()

    # gather complete data set for backtest
    if LIVE or BACKTEST:

        # print(((now - info['origin']) / float(CANDLE)))

        data = backtest_candles(PAIR, info['origin'], now, CANDLE)

        # print(CANDLE)
        # print((len(data['unix']), (data['unix'][1] - data['unix'][0])))
        # print((min(data['unix']), time.ctime(min(data['unix'])), 'mindate'))
        # print((info['origin'], time.ctime(info['origin']), 'origin'))

        print('')
        print(('PAIR......: %s' % PAIR))
        print(('BitPAIR...: %s' % BitPAIR))
        print('')

        print(('CANDLE....: %s' % CANDLE))
        # print(('ORIGIN....: %s %s' % (info['origin'],
        #                              time.ctime(info['origin']))))
        # print(('BEGIN.....: %s %s' % (info['begin'],
        #                              time.ctime(info['begin']))))
        plot_format()

    if LIVE:
        test_chart_latest()

def backtest():  # Primary backtest event loop; the cost funtion
    #===================================================================
    ''' BACKTEST EVENT LOOP '''
    #===================================================================
    global storage
    while True:
        # print(info['current_time'], 'current_time')
        # print(info['end'], 'end')
        if info['current_time'] < info['end']:

            # print info['current_time'], time.ctime(info['current_time'])
            # print (data)
            # print (len(data['unix']))

            # print (data)
            # print (info['current_time'])
            data_slice = slice_candles(info['current_time'], data)
            storage['high'] = data_slice['high']
            storage['low'] = data_slice['low']
            storage['open'] = data_slice['open']
            storage['close'] = data_slice['close']

            holdings()
            indicators()
            state_machine()
            trade()

            if LIVE or BACKTEST:
                test_chart()
            info['current_time'] += CANDLE
            info['tick'] += 1
        else:
            test_stop()
            print_tune()
            if LIVE or BACKTEST:
                test_plot()
                plt.pause(0.0001)
                if BACKTEST:
                    plt.ioff()
                try:
                    plot_format()
                except:
                    pass
                plt.show()
            break

def test_buy(price):  # Execute a backtest buy

    storage['trades'] += 1
    now = time.ctime(info['current_time'])
    storage['buys'][0].append(info['current_time'])
    storage['buys'][1].append(price)
    portfolio['assets'] = portfolio['currency'] / price
    if LIVE or BACKTEST:
        plot_text()
        if storage['market_cross'] is True:
            call = 'BULL SUPPORT'
        else:
            call = 'BEAR DESPAIR'
        print(('[%s] %s BUY %s %.2f %s at %s sat value %.2f %s' %
             (now, storage['trades'], call,
              portfolio['assets'], ASSET,
              int(price * ANTISAT), portfolio['currency'], CURRENCY)))

        plt.plot(info['current_time'], (price), markersize=10,
                 marker='^', color='lime', label='buy')
    portfolio['currency'] = 0
    if LIVE:
        plt.pause(0.0001)

def test_sell(price):  # Execute a backtest sell

    storage['trades'] += 1
    now = info['current_time']
    storage['sells'][0].append(info['current_time'])
    storage['sells'][1].append(price)
    portfolio['currency'] = portfolio['assets'] * price

    if LIVE or BACKTEST:
        plot_text()
        plt.plot(info['current_time'], (price), markersize=10,
                 marker='v', color='coral', label='sell')
        if storage['market_cross'] is True:
            call = 'BULL OVERBOUGHT'
        else:
            call = 'BEAR RESISTANCE'
        if storage['buys'][1][-1]:
            buy_price = storage['buys'][1][-1]
            buy_time = storage['buys'][0][-1]
            if price > buy_price:
                plt.plot((buy_time, now), (buy_price, price),
                         color='lime', label='win', lw=2)
            else:
                plt.plot((buy_time, now), (buy_price, price),
                         color='coral', label='loss', lw=2)

        print(('[%s] %s SELL %s %.2f %s at %s sat value %.2f %s' %
             (time.ctime(now), storage['trades'], call,
              portfolio['assets'], ASSET,
              int(price * ANTISAT), portfolio['currency'], CURRENCY)))
    portfolio['assets'] = 0
    if LIVE:
        plt.pause(0.0001)

# PLOT, PRINT, ALARM

def draw_state_machine(  # Plots primary trade indications
        now, selloff, support, resistance, despair,
        buying, selling, min_cross, max_cross,
        market_cross, ma2):

    if not SALES:
        if market_cross:
            plt.plot((now, now), (selloff, support),
                     color='lime', label='state', alpha=0.2)
            plt.plot((now, now), (resistance, despair),
                     color='darkorchid', label='state', alpha=0.2)
        else:
            plt.plot((now, now), (resistance, despair),
                     color='red', label='state', alpha=0.2)
            plt.plot((now, now), (selloff, support),
                     color='darkorchid', label='state', alpha=0.2)

        plt.plot((now, now), ((max_cross), (min_cross)),
                 color='white', label='cross', alpha=1.0)
        plt.plot(now, (ma2), markersize=6, marker='.',
                 color='aqua', label='ma2')
        plt.plot(now, max_cross, markersize=3, marker='.',
                 color='white', label='cross')
        plt.plot(now, min_cross, markersize=3, marker='.',
                 color='white', label='cross')

        # plot market extremes
        plt.plot(now, selloff, markersize=3, marker='.',
                 color='darkorchid', label='selloff')
        plt.plot(now, despair, markersize=3, marker='.',
                 color='darkorchid', label='despair')
        plt.plot(now, resistance, markersize=3, marker='.',
                 color='darkorchid', label='resistance')
        plt.plot(now, support, markersize=3, marker='.',
                 color='darkorchid', label='support')

        plt.plot(now, buying, markersize=6, marker='.',
                 color='lime', label='buying')
        plt.plot(now, selling, markersize=6, marker='.',
                 color='red', label='selling')

def test_rechart_orders():  # Set buy/sell markers on top

    for i in range(len(storage['sells'][0])):
        plt.plot(storage['sells'][0][i], (storage['sells'][1][i]),
                 markersize=10, marker='v', color='coral', label='sell')
    for i in range(len(storage['buys'][0])):
        plt.plot(storage['buys'][0][i], (storage['buys'][1][i]),
                 markersize=10, marker='^', color='lime', label='buy')
    chart_star()
    plt.pause(0.001)

def live_chart_latest():  # Plot last 24hrs of 5m candles

    now = int(time.time())
    days = 1
    candle = 300
    d = backtest_candles(PAIR, (now - days * 86400), now, candle)
    high = d['high']
    low = d['low']
    close = d['close']
    unix = d['unix']
    for i in range(len(unix)):
        now = unix[i]
        if low[i] < close[i]:
            plt.plot(now, low[i], markersize=6, marker='.',
                     color='m', label='low')
        if high[i] > close[i]:
            plt.plot(now, high[i], markersize=6, marker='.',
                     color='m', label='high')
        plt.plot(now, close[i], markersize=2, marker='.',
                 color='y', label='close')
    plt.pause(0.001)

def test_chart_latest():  # Plot high resolution end of backtest

    # plot 1 day of 5m candles
    days = 1
    candle = 300
    d = backtest_candles(
        PAIR, (info['end'] - days * 86400), info['end'], candle)
    high = d['high']
    low = d['low']
    close = d['close']
    unix = d['unix']
    for i in range(len(unix)):
        now = unix[i]
        if low[i] < close[i]:
            plt.plot((now), (high[i]), markersize=4, marker='.',
                     color='m', label='high')
        if high[i] > close[i]:
            plt.plot((now), (low[i]), markersize=4, marker='.',
                     color='m', label='low')
        plt.plot((now), (close[i]), markersize=4, marker='.',
                 color='y', label='close')
    # plot last 30 days of 2h
    days = 30
    candle = 7200
    d = backtest_candles(
        PAIR, (info['end'] - days * 86400), info['end'], candle)
    high = d['high']
    low = d['low']
    close = d['close']
    unix = d['unix']
    for i in range(len(unix)):
        now = unix[i]
        if low[i] < close[i]:
            plt.plot((now), (high[i]), markersize=4, marker='.',
                     color='m', label='high')
        if high[i] > close[i]:
            plt.plot((now), (low[i]), markersize=4, marker='.',
                     color='m', label='low')
        plt.plot((now), (close[i]), markersize=4, marker='.',
                 color='y', label='close')
    plt.pause(0.001)

def test_chart():  # Add objects to backtest plot

    # localize data
    now = info['current_time']
    ma1 = storage['ma1'][-1]
    ma2 = storage['ma2'][-1]
    close = storage['close']
    high = storage['high']
    low = storage['low']
    selloff = storage['selloff']
    despair = storage['despair']
    resistance = storage['resistance']
    support = storage['support']
    max_cross = storage['max_cross']
    min_cross = storage['min_cross']
    market_cross = storage['market_cross']
    buying = storage['buying']
    selling = storage['selling']

    draw_state_machine(now, selloff, support,
                       resistance, despair, buying, selling,
                       min_cross, max_cross, market_cross, ma2)

    # plot candles
    plt.plot((now, now), ((high[-1]), (low[-1])),
             color='m', label='high_low', alpha=0.5)
    plt.plot(now, (close[-1]), markersize=4, marker='.',
             color='y', label='close')

    if info['tick'] == 0:
        chart_star()

def live_chart():  # Add objects to live plot

    cex_rate = storage['cex_rate']
    dex_rate = storage['dex_rate']
    m_volume = storage['m_volume']
    ma1 = storage['ma1'][-1]
    ma2 = storage['ma2'][-1]
    ma3 = storage['ma3'][-1]
    ma4 = storage['ma4'][-1]
    selloff = storage['selloff']
    despair = storage['despair']
    resistance = storage['resistance']
    support = storage['support']
    buying = storage['buying']
    selling = storage['selling']
    ask = book['askp'][0]
    bid = book['bidp'][0]
    scalp_resistance = storage['scalp_resistance']
    scalp_support = storage['scalp_support']
    max_cross = storage['max_cross']
    min_cross = storage['min_cross']
    market_cross = storage['market_cross']
    now = info['current_time']
    high = storage['high']
    low = storage['low']

    # plot state machine
    draw_state_machine(now, selloff, support,
                       resistance, despair, buying, selling,
                       min_cross, max_cross, market_cross, ma2)

    plt.plot(now, high,
             markersize=3, marker='.', color='m', label='high')
    plt.plot(now, low,
             markersize=3, marker='.', color='m', label='low')

    plt.plot(now, scalp_resistance, markersize=4, marker='.',
             color='tomato', label='scalp_resistance')
    plt.plot(now, scalp_support, markersize=4, marker='.',
             color='palegreen', label='scalp_support')

    plt.plot(now, ask, markersize=3, marker='.',
             color='aqua', label='ask')
    plt.plot(now, bid, markersize=3, marker='.',
             color='aqua', label='bid')

    plt.plot(now, dex_rate, markersize=4 * m_volume, marker='.',
             color='khaki', label='dex_rate')
    plt.plot(now, cex_rate, markersize=4 * m_volume, marker='.',
             color='yellow', label='cex_rate')

    if info['tick'] == 0:

        # clone the backtest in higher resolution for last 24hrs
        plt.plot((now, now), (selloff, despair),
                 color='white', label='vertical start', lw=5, alpha=0.2)

        ma1_period = MA1 * 86400 / 7200.0
        ma2_period = MA2 * 86400 / 7200.0
        ma1_arr = float_sma(data['7200']['close'], ma1_period)
        ma2_arr = float_sma(data['7200']['close'], ma2_period)
        unix = data['7200']['unix']
        for i in range(-1, -20, -1):
            for z in range(0, 7200, 300):
                try:
                    now = unix[i] + z
                    ma1 = ma1_arr[i]
                    ma2 = ma2_arr[i]

                    # state machine clone
                    min_cross = MIN_CROSS * ma1
                    max_cross = MAX_CROSS * min_cross
                    bull_stop = BULL_STOP * ma2
                    bear_stop = BEAR_STOP * ma2
                    selloff = SELLOFF * ma1
                    despair = DESPAIR * ma1
                    support = max((SUPPORT * ma1), bull_stop)
                    resistance = min((RESISTANCE * ma1), bear_stop)
                    if market_cross:
                        selling = selloff
                        buying = support
                    else:
                        buying = despair
                        selling = resistance

                    # plot state machine
                    draw_state_machine(now, selloff, support,
                                       resistance, despair, buying, selling,
                                       min_cross, max_cross, market_cross, ma2)
                except:
                    print ('plot ma_arr failed')
                    pass
        chart_star()
    plt.pause(0.001)

def chart_star():  # Plot a star at begin and end of backtest

    now = info['current_time']
    if info['live']:
        cex_rate = storage['cex_rate']
    else:
        cex_rate = (storage['close'][-1])

    plt.plot(now, cex_rate, markersize=50,
             marker='1', color='w', label='cex_rate')
    plt.plot(now, cex_rate, markersize=40,
             marker='2', color='y', label='cex_rate')
    plt.plot(now, cex_rate, markersize=40,
             marker='3', color='w', label='cex_rate')
    plt.plot(now, cex_rate, markersize=50,
             marker='4', color='y', label='cex_rate')
    plt.plot(now, cex_rate, markersize=15,
             marker='.', color='y', label='cex_rate')

def plot_format():  # Set plot colors and attributes

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

    if (info['live'] is False) and (info['tick'] > 1):
        plt.ylabel('LOGARITHMIC PRICE SCALE')
        plt.yscale('log')
    if info['live'] is True:
        plt.ylabel('MARKET PRICE')
    ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.yaxis.set_minor_formatter(matplotlib.ticker.ScalarFormatter())

    ax.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%.8f"))
    ax.yaxis.set_minor_formatter(matplotlib.ticker.FormatStrFormatter("%.8f"))

    if info['live']:
        stepsize = 3600
    else:
        if DAYS > 100:
            stepsize = 2592000
        elif DAYS > 20:
            stepsize = 864000
        else:
            stepsize = 86400

    start, end = ax.get_xlim()
    ax.xaxis.set_ticks(np.arange((end - end % 3600), start, -stepsize))

    def timestamp(x, pos):
        if not info['live']:
            return (datetime.fromtimestamp(x)).strftime('%Y-%m-%d')
        else:
            return (datetime.fromtimestamp(x)).strftime('%m/%d %H:%M')

    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(timestamp))

    if info['tick'] > 1:

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

        if (info['live'] is False):

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

    if info['live']:
        start, end = ax.get_ylim()
        stepsize = abs(start - end) / 25
        ax.yaxis.set_ticks(np.arange(end, start, -stepsize))

    plt.gcf().autofmt_xdate(rotation=30)
    ax.title.set_color('darkorchid')
    plt.title(('%s ' % PAIR) + VERSION)
    plt.tight_layout()

def plot_text():  # Display market condition on plot

    # clear text
    storage['text'] = storage.get('text', [])
    for text in storage['text']:
        try:
            text.remove()
        except:
            pass

    # static text
    textx = 0.1 * (plt.xlim()[1] - plt.xlim()[0]) + plt.xlim()[0]
    texty = 0.8 * (plt.ylim()[1] - plt.ylim()[0]) + plt.ylim()[0]
    storage['text'].append(plt.text(textx, texty,
                                    'litepresence', color='aqua',
                                    alpha=0.2, size=70))
    textx = 0.27 * (plt.xlim()[1] - plt.xlim()[0]) + plt.xlim()[0]
    texty = 0.7 * (plt.ylim()[1] - plt.ylim()[0]) + plt.ylim()[0]
    storage['text'].append(plt.text(textx, texty,
                                    'EXTINCTION EVENT', color='aqua',
                                    alpha=0.3, size=25, weight='extra bold'))
    textx = 0.1 * (plt.xlim()[1] - plt.xlim()[0]) + plt.xlim()[0]
    texty = 0.08 * (plt.ylim()[1] - plt.ylim()[0]) + plt.ylim()[0]
    storage['text'].append(
        plt.text(textx, texty, '(BTS) litepresence1',
                 color='white', alpha=0.5, size=10, weight='extra bold'))
    textx = 0.4 * (plt.xlim()[1] - plt.xlim()[0]) + plt.xlim()[0]
    texty = 0.1 * (plt.ylim()[1] - plt.ylim()[0]) + plt.ylim()[0]
    storage['text'].append(
        plt.text(textx, texty, (ASSET + CURRENCY),
                 color='yellow', alpha=0.1, size=70, weight='extra bold'))
    textx = 0.6 * (plt.xlim()[1] - plt.xlim()[0]) + plt.xlim()[0]
    texty = 0.05 * (plt.ylim()[1] - plt.ylim()[0]) + plt.ylim()[0]
    text = 'BACKTEST '
    if info['live']:
        text = 'LIVE '
    text += storage['asset_name']
    storage['text'].append(
        plt.text(textx, texty, text,
                 color='yellow', alpha=0.25, size=20, weight='extra bold'))

    # dynamic text
    if info['live']:
        high = storage['cex_rate']
        low = storage['cex_rate']
    else:
        high = storage['high'][-1]
        low = storage['low'][-1]
    textx = 0.1 * (plt.xlim()[1] - plt.xlim()[0]) + plt.xlim()[0]
    texty = 0.1 * (plt.ylim()[1] - plt.ylim()[0]) + plt.ylim()[0]
    if storage['market_cross']:
        storage['text'].append(
            plt.text(textx, texty, 'BULL MARKET',
                     color='lime', alpha=0.3, size=30, weight='extra bold'))
        textx = 0.125 * (plt.xlim()[1] - plt.xlim()[0]) + plt.xlim()[0]
        texty = 0.05 * (plt.ylim()[1] - plt.ylim()[0]) + plt.ylim()[0]
        if low < storage['buying']:
            storage['text'].append(
                plt.text(textx, texty, 'BUY SUPPORT',
                         color='lime', alpha=0.5, size=20,
                         weight='extra bold'))
        elif high > storage['selling']:
            storage['text'].append(
                plt.text(textx, texty, 'SELL OVERBOUGHT',
                         color='red', alpha=0.5, size=20,
                         weight='extra bold'))
    else:
        storage['text'].append(
            plt.text(textx, texty, 'BEAR MARKET',
                     color='red', alpha=0.3, size=30, weight='extra bold'))
        textx = 0.125 * (plt.xlim()[1] - plt.xlim()[0]) + plt.xlim()[0]
        texty = 0.05 * (plt.ylim()[1] - plt.ylim()[0]) + plt.ylim()[0]
        if low < storage['buying']:
            storage['text'].append(
                plt.text(textx, texty, 'BUY DESPAIR',
                         color='lime', alpha=0.5, size=20,
                         weight='extra bold'))
        elif high > storage['selling']:
            storage['text'].append(
                plt.text(textx, texty, 'SELL RESISTANCE',
                         color='red', alpha=0.5, size=20, weight='extra bold'))
    plt.tight_layout()

def test_plot():  # Display backtest plot

    begin = info['begin']
    end = info['end']
    while (end - begin) > LIVE_PLOT_DEPTH:
        # PLOT FORMAT
        try:
            ax = plt.gca()
            # Window Plot
            left, right = ax.set_xlim(left=begin - 50, right=end + 50)
            # Prevent Memory Leak Outside Plot Window
            for l in ax.get_lines():
                xval = l.get_xdata()[0]
                if (xval < begin):
                    l.remove()
            if LIVE:
                begin = begin + 0.3 * (end - begin)
            else:
                begin = end
            plt.tight_layout()
            plt.pause(0.0001)
        except:
            print('animated test plot failed')
    plot_text()
    plot_format()

    # if LIVE: plt.clf()  # clear the plotted figure; end log scale
    if BACKTEST:
        try:
            plt.autoscale(enable=True, axis='y')
            plt.pause(0.0001)

        except:
            print('static test plot failed')

def live_plot():  # Display live plot

    now = int(time.time())
    ax = plt.gca()
    # Window Plot
    ax.set_xlim(([(now - LIVE_PLOT_DEPTH), (now)]))
    # Prevent Memory Leak Outside Plot Window; remove unnecessary data
    for l in ax.get_lines():
        xval = l.get_xdata()[0]
        if (xval < (ax.get_xlim()[0])):
            l.remove()
    plot_text()
    plt.tight_layout()
    plt.pause(0.0001)

def test_stop():  # Display results of backtest session

    close = storage['close'][-1]

    # ctime_tick_labels()
    # move to currency
    if BACKTEST and (portfolio['assets'] > 0.1) and CURRENCY_STOP:
        print('stop() EXIT TO CURRENCY')
        test_sell(price=close)
    # calculate return on investment
    end_max_assets = portfolio['assets'] + (portfolio['currency'] / close)
    end_max_currency = portfolio['currency'] + (portfolio['assets'] * close)
    roi_assets = end_max_assets / storage['begin_max_assets']
    roi_currency = end_max_currency / storage['begin_max_currency']
    storage['roi_currency'] = roi_currency
    days = (info['end'] - info['begin']) / 86400.0
    frequency = (SATOSHI + storage['trades']) / days
    storage['dpt'] = 1.0 / frequency

    # A = P*(1+(r/n))**(n*t)
    P = storage['begin_max_currency']
    t = DAYS / 365.0
    A = end_max_currency
    n = 1.0
    r = n * ((A / P) ** (1 / (n * t)) - 1)
    storage['apy_currency'] = r

    if LIVE or BACKTEST:

        print(
            '===============================================================')
        print(('START DATE........: %s' % time.ctime(info['begin'])))
        print(('END DATE..........: %s' % time.ctime(info['end'])))
        print(('DAYS..............: %.1f' % days))
        print(('TRADES............: %s' % storage['trades']))
        print(('DAYS PER TRADE....: %.1f' % storage['dpt']))

        print(('START PRICE.......: %.8f ' % data['close'][-DAYS]))
        print(('END PRICE.........: %.8f' % close))
        print(('START PORTFOLIO...: %.1f %s %.1f %s' %
             (START_CURRENCY, CURRENCY, START_ASSETS, ASSET)))
        print(
            ('START MAX ASSETS..: %s %s' %
             (storage['begin_max_assets'], ASSET)))
        print(('END MAX ASSETS....: %s %s' % (end_max_assets, ASSET)))
        print(('ROI ASSETS........: %.2fX' % roi_assets))
        print(('START MAX CURRENCY: %s %s' %
             (storage['begin_max_currency'], CURRENCY)))
        print(('END MAX CURRENCY..: %s %s' % (end_max_currency, CURRENCY)))
        print(('ROI CURRENCY......: %.2fX' % roi_currency))
        # print(('APY CURRENCY......: %.2f' % storage['apy_currency']))
        print(
            '===============================================================')
        print(VERSION)
        print('~===END BACKTEST=========================~')
        test_rechart_orders()

def print_tune():  # Display input thresholds

    storage['roi_currency'] = storage.get('roi_currency', ROI)
    storage['apy_currency'] = storage.get('apy_currency', APY)
    storage['dpt'] = storage.get('dpt', DPT)
    storage['trades'] = storage.get('trades', 0)

    frequency = (SATOSHI + storage['trades']) / DAYS

    z = '+=' if OPTIMIZE else '='

    print('#######################################')
    print(('CURRENCY        = "%s"' % CURRENCY))
    print(('ASSET           = "%s"' % ASSET))
    print(('MA1            %s %.2f' % (z, MA1)))
    print(('MA2            %s %.2f' % (z, MA2)))
    print(('SELLOFF        %s %.3f' % (z, SELLOFF)))
    print(('SUPPORT        %s %.3f' % (z, SUPPORT)))
    print(('RESISTANCE     %s %.3f' % (z, RESISTANCE)))
    print(('DESPAIR        %s %.3f' % (z, DESPAIR)))
    print(('MIN_CROSS      %s %.3f' % (z, MIN_CROSS)))
    print(('MAX_CROSS      %s %.3f' % (z, MAX_CROSS)))
    print(('BULL_STOP      %s %.3f' % (z, BULL_STOP)))
    print(('BEAR_STOP      %s %.3f' % (z, BEAR_STOP)))
    print('#######################################')
    # print(('# RESOLUTION    : %s' % RESOLUTION))
    print(('# DAYS          : %s' % DAYS))
    print(('DPT             = %.1f' % storage['dpt']))
    print(('# MARKET CAP....: %.1fM' % asset_cap))
    print(('# DOMINANCE.....: %.4f - RANK %s' % (asset_dominance, asset_rank)))
    print(('ROI             = %.2fX' % storage['roi_currency']))
    # print(('APY             = %.2f' % storage['apy_currency']))
    print('#######################################')

def bell(duration, frequency):  # Activate linux audible bell
    os.system('play --no-show-progress --null --channels 1 synth' +
              ' %s sine %f' % (duration, frequency))

# DATA PROCESSING

def clock():  # 24 hour clock formatted HH:MM:SS
    return str(time.ctime())[11:19]

def satoshi(n):  # format prices to satoshi type
    return float('%.8f' % float(n))

def dictionaries():  # Global info, data, portfolio, and storage

    global info, storage, portfolio, book
    info = {}
    book = {}
    storage = {}
    portfolio = {}

def coin_name():  # Convert ticker symbols to coin names

    curr = currencies()
    storage['asset_name'] = curr[ASSET]['CoinName']
    storage['currency_name'] = curr[CURRENCY]['CoinName']
    print((storage['asset_name']))

def ctime_tick_labels():  # X axis timestamps formatting
    ax = plt.gca()
    fig.canvas.draw()
    labels = ax.get_xticklabels()
    xlabels = []
    for label in labels:
        x = label.get_text()
        print(x)
        try:
            xlabels.append(float(x))
        except:
            xlabels.append(str(x))
    for i in range(len(xlabels)):
        try:
            if isinstance(xlabels[i], float):
                xlabels[i] = time.ctime(float(xlabels[i]))
        except:
            pass
    ax.set_xticklabels(xlabels)

def indicators():  # Post process data

    global storage
    global book

    ma1_period = MA1 * 86400.0 / CANDLE
    ma2_period = MA2 * 86400.0 / CANDLE
    if not info['live']:

        # alpha moving averages
        storage['ma1'] = float_sma(storage['close'], ma1_period)
        storage['ma2'] = float_sma(storage['close'], ma2_period)

    if info['live']:

        # alpha moving averages
        storage['ma1'] = float_sma(
            data['7200']['close'], ma1_period)
        storage['ma2'] = float_sma(
            data['7200']['close'], ma2_period)

        # scalp moving averages
        storage['ma3'] = float_sma(data['300']['close'], 288 * MA3)
        storage['ma4'] = float_sma(data['300']['close'], 288 * MA4)

        # 20 minute high and low
        storage['high'] = max(data['300']['high'][-4:])
        storage['low'] = min(data['300']['low'][-4:])

        # orderbook and last price
        book = dex('book')
        sbids = [('%.8f' % i) for i in book['bidp'][:3]]
        sbids = sbids[::-1]
        sasks = [('%.8f' % i) for i in book['askp'][:3]]
        print (sbids, 'BIDS <> ASKS', sasks)

        cex_rate = storage['cex_rate']

        # means to buy and percent invested
        assets = portfolio['assets']
        currency = portfolio['currency']
        means = storage['means'] = (currency + SATOSHI) / cex_rate
        storage['asset_ratio'] = assets / (assets + means)

        # recent volume ratio for plotting
        depth = 100
        mv = ((depth * data['300']['volume'][-1]) /
              sum(data['300']['volume'][-depth:]))
        storage['m_volume'] = 1 if mv < 1 else 5 if mv > 5 else mv

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

# ARTIFICIAL INTELLEGENCE

def state_machine():  # Alpha and beta market finite state

    # localize primary indicators
    ma1 = storage['ma1'][-1]
    ma2 = storage['ma2'][-1]
    min_cross = storage['min_cross'] = MIN_CROSS * ma1
    max_cross = storage['max_cross'] = MAX_CROSS * storage['min_cross']

    # set alpha state
    storage['market_cross'] = storage.get('market_cross', MARKET_CROSS)

    if storage['market_cross'] is False:
        if (min_cross > ma2):
            storage['market_cross'] = True
    if storage['market_cross'] is True:
        if (max_cross < ma2):
            storage['market_cross'] = False

    # Manual override alpha state
    if info['live']:
        if FORCE_ALPHA == 'BULL':
            storage['market_cross'] = True
        if FORCE_ALPHA == 'BEAR':
            storage['market_cross'] = False

    # establish beta thresholds

    storage['selloff'] = (ma1 * SELLOFF)
    storage['support'] = max(ma1 * SUPPORT, ma2 * BULL_STOP)
    storage['resistance'] = min(ma1 * RESISTANCE, ma2 * BEAR_STOP)
    storage['despair'] = (ma1 * DESPAIR)

    # initialize backtest per MARKET_CROSS
    if (info['live'] is False) and (info['tick'] == 0):
        close = storage['close'][-1]
        storage['selling'] = storage['buying'] = close
        if MARKET_CROSS is True:
            if START_CURRENCY > 0:
                test_buy(close)
        if MARKET_CROSS is False:
            if START_ASSETS > 0:
                test_sell(close)

    # set beta state
    if storage['market_cross']:
        storage['buying'] = storage['support']
        storage['selling'] = storage['selloff']
    else:
        storage['buying'] = storage['despair']
        storage['selling'] = storage['resistance']
    storage['mid_market'] = (storage['buying'] + storage['selling']) / 2

# PRIMARY PROCESS
if __name__ == "__main__":

    print('')
    print(VERSION)
    print('')
    tune_install()
    keys_install()

    asset_cap, asset_dominance, asset_rank = marketcap()
    optimize = False
    data = {}
    control_panel()

    if LATENCY:

        nodes_update()
        price, volume, latency = cryptocompare_last()
        cryptocompare_time()
        sys.exit()

    if MODE in [2, 3]:

        # initialize data feeds
        last_update()
        book_update()

    dictionaries()
    initialize()
    test_initialize()
    coin_name()
    if (MODE in [2, 3]) or BACKTEST:
        backtest()
    print_tune()

    if MODE in [2, 3]:

        # begin background processes
        p_node = Process(target=nodes_loop)
        p_node.daemon = False
        p_node.start()
        p_last = Process(target=last_loop)
        p_last.daemon = False
        p_last.start()
        p_book = Process(target=book_loop)
        p_book.daemon = False
        p_book.start()
        # start live event loop
        live()

    if OPTIMIZE:
        print ('https://www.youtube.com/watch?v=5ydqjqZ_3oc')
        sys.exit()
#=======================================================================
''' EXTINCTION EVENT '''
#=======================================================================
#
# THE DESTROYER,
# litepresence - 2018
#
