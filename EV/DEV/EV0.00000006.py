' litepresence 2018 '

def WTFPL_v0_March_1765():
    if any([stamps, licenses, taxation, regulation, fiat, etat]):
        try:
            print('no thank you')
        except:
            return [tar, feathers]

# dependencies
import matplotlib
import numpy as np
from tkinter import *

# pybitshares modules
from bitshares import BitShares
from bitshares.market import Market
from bitshares.account import Account
from bitshares.blockchain import Blockchain

# standard python modules
import os
import sys
import json
import time
import math
import warnings
import requests
import websocket
import traceback
from getpass import getpass
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import matplotlib.dates as mdates
from ast import literal_eval as literal
from statistics import mean, median, mode
from random import random, shuffle, randint
from multiprocessing import Process, Value, Array

# Google Agorism
SATOSHI = 0.00000001
ANTISAT = 1 / SATOSHI

def banner():

    print("\033c") 
    print('''

        # EXTINCTION EVENT

        # Backtesting and Live Algo Trading Framework for Bitshares DEX

        ' (BTS) litpresence1 '

        v0.00000003_beta

        Ensure what I want happens, 
        when I want it to happen, 
        and assure me it actually happened.

        * featuring trustless client side Bitshares public node access *

        Installation:

        https://github.com/litepresence/extinction-event/blob/master/README.md

        ''')
    time.sleep(0)
    print("\033c") 
    print('''
        Bitshares Decentralized Development April 2018

        BitShares Core Release 2.0.180328
        https://github.com/bitshares/bitshares-core/releases/tag/2.0.180328

        PUBLIC NODES - 65 responding to east coast US; 2X in past 30 days

        EASYDEX - Bitshares fiat gateway for USD and EUR
        CITADEL - Bitshare UI and stealth wallet
        PALMPAY - Chain Agnostic 3 Second Point of Sale App
        MORPHIT - Fee Free app like shapeshift/blocktrades
        LOCALBTS - Decentralized Local Bitshares to Fiat Reputation App
        BENCH -
        GRAPHENEJ - A Java library for mobile Bitsshares app Developers
        
        DEXBOT - Scalping / Market Making UI
        CARBON - Multichain Mobile Wallet
        STEALTH - ??? sent ??? amount to ??? BTS Transactions

        BTS added to HUOBI and COINTIGER exchanges

        bitsharestalk.io new chat forum
        apasia, leading public node provider, aquires bitshares.org
        ''')

    time.sleep(0)
    print("\033c") 
    print('''

        running metaNODE and EV concurrently live will use:

        50kbit/s upload
        600kbit/s download
        <2 GB RAM
        4 CPU cores at <10%

        Initializing EV.py live:

        3 GB RAM
        100% of 1 cpu for a few minutes
        ''')

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
    # WTFPLv0 March 1765
    #

    use this, get lambo, deposit 7.777% skriptbunny tithing here:

    (BTS) litepresence1
    (BTC) 374gjPuhokrWj8KJu8NnMBGzpbHWcVeE1k

    #
    # 0.05 BTC each for AI tuned to last 365 days of any alt/btc pair
    # 1 BTC each for machine optimized algo for top 100 alt/btc pair

    # !@#$%^&*()!@#$%^&*()!@#$%^&*()!@#$%^&*()!@#$%^&*()!@#$%^&*()

    # this algo can be tuned to between:

    # 50X and 50,000X

    # in BOTH currency and asset terms
    # for ANY* crypto-crypto pair, over past 365 days of data

    # !@#$%^&*()!@#$%^&*()!@#$%^&*()!@#$%^&*()!@#$%^&*()!@#$%^&*()

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
    ''' FEATURES v0.00000001 alpha release March 8, 2018'''
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
    ''' FEATURES v0.00000002 alpha April 1, 2018 '''
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
    ''' FEATURES v0.00000003 dare I say beta April 20, 2018'''
    #===================================================================
    '''

    - microDEX.py was created to monitor EV.py in realtime. 
    - solid doubletime week live testing and de bugging EV.py afterwards
    - completely reworked all dex() calls
    - reconnect() is a thing - client side wss handshake verification

    - simplified scalp(), it works, enjoy
    - do what I say, when I say, and announce when done: LIVE $$$ DEX'd
    - new mode TEST ORDERS
    - generates EV_log.py microDEX_log.py with stacktrace + buy/sell
    - new easy install to virtual environment by @sschiessl

    - with microDEX multinode animation and EV.py statistical curation
        user and bots have VIP seats on public DEX network

    '''
    #===================================================================
    ''' FEATURES v0.00000004 beta-alt-alt-meta May 23, 2018'''
    #===================================================================
    '''

    - metaNODE
        - data curation for public database calls
        - stand alone app independently watches full public network 
        - performs statistical analysis on data feeds
        - maintains whitelisted nodes list
        - acts as 'monit' type duplex watchdog to EV

    - dexBOT collaboration
        - metaNODE framework built to work with other bot applications
        - funding earmarked for metaNODE implementation into dexBOT

    - altcoin-altcoin trading via btc common base
        - ie simulated STEEM:BTS pair historic backtest data
    '''

    #===================================================================
    ''' DEPENDENCIES'''
    #===================================================================
    '''
    python 3

    numpy
    tkinter
    matplotlib
    pybitshares

    *h/t @ cryptocompare.com w/ 2000+ altcoin pairs of market data
    **h/t to crew at bitshares dev and node admin telegram
    '''

def version():

    global VERSION
    #===================================================================
    VERSION = 'EXTINCTION EVENT v0.00000006 regression'
    #===================================================================
    print ('Python3 and Linux Required; your system:', sys.version.split(' ')[0], sys.platform)
    sys.stdout.write('\x1b]2;' + VERSION + '\x07')
    print('')
    print(VERSION)
    print('')

# USER CONTROLS
# ======================================================================

def tune_install():  # Basic User Controls

    global CURRENCY, ASSET, MA1, MA2
    global SELLOFF, SUPPORT, RESISTANCE, DESPAIR
    global MIN_CROSS, MAX_CROSS, BULL_STOP, BEAR_STOP
    global DPT, ROI, APY
    global METHOD

    APY = DPT = ROI = 1.0
    METHOD = 0
    #===================================================================

    CURRENCY        = "BTC"
    ASSET           = "BTS"
    MA1            = 10
    MA2            = 50
    SELLOFF        = 2
    SUPPORT        = 1
    RESISTANCE     = 1
    DESPAIR        = 0.75
    MIN_CROSS      = 1
    MAX_CROSS      = 1
    BULL_STOP      = 1
    BEAR_STOP      = 1


def control_panel():  # Advanced User Controls

    global LIVE, CURRENCY, ASSET, MA1, MA2, MA3, MA4, SCALP_PIECES
    global MIN_MARGIN, TICK, TICK_TIMING, TICK_MINIMUM, OPTIMIZE_DAYS
    global CANDLE, START_ASSETS, START_CURRENCY, ORDER_TEST, WARMUP
    global ANIMATE, STORAGE_RESET, CURRENCY_STOP, MAX_CURRENCY
    global LIVE_PLOT_DEPTH, BELL, FORCE_ALPHA, PAPER, LATENCY
    global DEPTH, BACKTEST, PAIR, MAX_ASSETS, SALES, SCALP_FUND
    global RESOLUTION, OPTIMIZATIONS, MARKET_CROSS, OPTIMIZE, SCALP
    global MANUAL_OVERRIDE, MANUAL_BUY, MANUAL_SELL, MIN_AMOUNT
    global LIVE_PLOT_PROJECTION

    # optimizer
    RESOLUTION = 25
    OPTIMIZATIONS = 10000
    OPTIMIZE_DAYS = 1000

    # backtest
    START_ASSETS = 0
    START_CURRENCY = 1000

    # initial backtest market state (True is "BULL")
    MARKET_CROSS = True

    # max percent may invest in:
    # 100 = "all in" ; 10 = "10 percent in"
    # to let bot do its thing with full bank use 100, 100
    MAX_ASSETS = 100
    MAX_CURRENCY = 100

    # minimum order size in asset terms
    MIN_AMOUNT = 2

    # scalp thresholds
    # ENTER OWN RISK &&&&
    SCALP = True        # maintain market maker iceberg margins
    SCALP_PIECES = 4    # number of pieces to break up scalp orders
    SCALP_FUND = 0.250  # 0.010 = 1% of holdings reserved for scalping
    MIN_MARGIN = 0.020  # about 0.030
    MA3 = 0.500         # about 0.500
    MA4 = 0.166         # about 0.166

    # force buy/sell thresholds manually
    MANUAL_OVERRIDE = False
    MANUAL_BUY = SATOSHI
    MANUAL_SELL = ANTISAT
    # Manual Override Alpha State when live
    FORCE_ALPHA = False  # Options: ( False, 'BULL', 'BEAR' )

    # hft timing in seconds
    TICK = 300
    TICK_TIMING = 51
    TICK_MINIMUM = 30

    # backtest
    ANIMATE = False
    STORAGE_RESET = False
    CURRENCY_STOP = False
    WARMUP = 5

    # live window
    LIVE_PLOT_DEPTH = 86400  # 86400 = 1 day
    LIVE_PLOT_PROJECTION = 1*86400
    BELL = False  # sound linux alarm when tick fails

    # constants
    CANDLE = 86400


    # 0        1          2       3      4       5         6
    OPTIMIZE = BACKTEST = PAPER = LIVE = SALES = LATENCY = ORDER_TEST = False

    if MODE == 0:
        OPTIMIZE = True
    if MODE == 1:
        BACKTEST = True
        OPTIMIZATIONS = 0
    if MODE == 2:
        PAPER = True
        MAX_ASSETS = 0
        MAX_CURRENCY = 0
    if MODE == 6:
        ORDER_TEST = True
        MAX_ASSETS = 0
        MAX_CURRENCY = 0
    if MODE in [2, 3, 6]:
        LIVE = True
        CANDLE = 7200
        OPTIMIZATIONS = 0
        print(('BOT MAY SPEND:     ', MAX_ASSETS, 'PERCENT CURRENCY'))
        print(('BOT MAY LIQUIDATE: ', MAX_CURRENCY, 'PERCENT ASSETS'))
        print('')
        print('gathering 2h candle data...')
    if MODE == 4:
        BACKTEST = True
        SALES = True
        OPTIMIZATIONS = 0
    if MODE == 5:
        LATENCY = True

    DEPTH = int(max(MA1, MA2) * (86400 / CANDLE) + 50)
    PAIR = ('%s_%s' % (CURRENCY, ASSET))

# BITSHARES DEX TRADING API
# ======================================================================

def keys_install():  # Bitshares Keys

    global BitCURRENCY, BitASSET, ACCOUNT, PASS_PHRASE
    global BitPAIR, MARKET, CHAIN, MODE, USERNAME, ID, LATENCY_LOOP
    ID = '4018d7844c78f6a6c41c6a552b898022310fc5dec06da467ee7905a8dad512c8'
    MODE = 999
    print('0:OPTIMIZE, 1:BACKTEST, 2:PAPER, 3:LIVE, 4:SALES, 6: TEST ORDERS')
    while MODE not in [0, 1, 2, 3, 4, 6]:
        MODE = int(input('TRADING MODE: '))
    print('')
    if MODE ==6:
        print('WARNING:')
        print('This mode will repeatedly LIVE TEST buy/sell/cancel 0.1 assets on 20% spread.')
        print('Monitor with microDEX.py')
        print('')
    if CURRENCY in ['BTS', 'USD', 'CNY']:
        BitCURRENCY = CURRENCY
    else:
        BitCURRENCY = 'OPEN.' + CURRENCY
    if ASSET in ['BTS', 'USD', 'CNY']:
        BitASSET = ASSET
    else:
        BitASSET = 'OPEN.' + ASSET
    BitPAIR = BitASSET + ":" + BitCURRENCY
    if MODE in [2, 3,6]:
        nodes = nodes_fetch()
        shuffle(nodes)
        try:
            USERNAME = input('     account: ')
            print('')
            print('accessing account...')
            print('')
            ACCOUNT = Account(USERNAME,
                bitshares_instance=BitShares(nodes))
        except Exception as ex:
            print (type(ex).__name__)
            sys.exit()
        if MODE in [3, 6]:
            print('DO NOT ENTER PASSWORD WITHOUT READING, UNDERSTANDING,')
            print('AND TAKING PERSONAL RESPONSIBILITY FOR THE CODE')
            print('')
            PASS_PHRASE = getpass(prompt=' pass phrase: ')
        else:
            PASS_PHRASE = ''
        MARKET = Market(BitPAIR, bitshares_instance=BitShares(nodes), mode='head')
        if MODE in [3, 6]:
            try:
                MARKET.bitshares.wallet.unlock(PASS_PHRASE)
                print('')
                print('AUTHENTICATED')
                time.sleep(1)
                print("\033c")
            except Exception as ex:
                print (type(ex).__name__)
                sys.exit()
        CHAIN = Blockchain(bitshares_instance=BitShares(nodes), mode='head')
        ACCOUNT = MARKET = CHAIN = 0
        
def reconnect( # client side, validate wss handshake 
        BitPAIR, USERNAME, PASS_PHRASE):

    # create fresh websocket connection
    i = 0
    while True:
        try:
            time.sleep(0.05 * i ** 2)
            i += 1
            print(time.ctime(), 'connecting, attempt:', i)
            # fetch fresh nodes list from subprocess and shuffle it
            '*************************************'
            metaNODE = Bitshares_Trustless_Client()
            '*************************************'
            nodes = metaNODE['whitelist']
            shuffle(nodes)
            node = nodes[0]

            # create a temporary handshake to confirm good node
            def chain_test(node, num):
                try:
                    chain = Blockchain(
                        bitshares_instance=BitShares(node, num_retries=0), mode='head')
                    num.value = 1
                except:
                    pass
            num = Value('i', 0)
            p = Process(target=chain_test, args=(node, num,))
            p.daemon = False
            p.start()
            p.join(6)
            if num.value == 0:
                raise ValueError('reconnect timed out')

            # create handshake
            chain = Blockchain(
                bitshares_instance=BitShares(node, num_retries=0), mode='head')
            market = Market(BitPAIR,
                bitshares_instance=BitShares(node, num_retries=0), mode='head')
            account = Account(USERNAME,
                bitshares_instance=BitShares(node, num_retries=0))

            current_block = chain.get_current_block_num()
            start = time.time()
            blocktimestamp = chain.block_timestamp(current_block)
            ping = time.time() - start
            block_latency = start - blocktimestamp

            # Confirm the connection is good
            if ping > 2:
                raise ValueError('ping > 2')
            if block_latency > 5:
                raise ValueError('block latency > 5')
            if chain.get_network()['chain_id'] != ID:
                raise ValueError('Not Mainnet Chain')
            if float(market.ticker()['latest']) == 0:
                raise ValueError('ZERO price')

            break
        except Exception as e:
            msg = msg_(e) + str(node)
            race_append(doc='EV_log.txt', text=msg)
            print(time.ctime(), type(e).__name__, e.args, node)
            continue
    try:
        market.bitshares.wallet.unlock(PASS_PHRASE)
    except:
        pass

    print(time.time(), node, market, str(chain).split(' ')[-1])

    return account, market, node, chain

def dex_auth(command, amount=ANTISAT, price=None, expiration=ANTISAT):

    # insistent timed process wrapper for dex_auth2()
    # covers all buy/sell/cancel pybitshares authenticated requests
    # if command does not execute in time: kill process, start anew
    # serves to force disconnect websockets if done; also if hung
    # signal.value is switched to 0 at end of dex_auth2()

    timeout = 60
        
    signal = Value('i', 1)
    i = 0
    plt.pause(0.01)
    while signal.value:
        i+=1
        print('')
        print('pybitshares authentication attempt:', i)
        process = Process(target=dex_auth2,
                    args=(signal, command, amount, price, expiration))
        process.daemon = False
        process.start()
        process.join(timeout)
        print('pybitshares authentication terminated')
        print('')
    watchdog()
    plt.pause(0.01)

def dex_auth2(signal, command, amount, price, expiration):

    if 'BTS' in BitPAIR:
        MIN_AMOUNT = 2
    attempt = 1
    # BUY/SELL/CANCEL OPS
    if amount > MIN_AMOUNT:
        if command == 'buy':
            # buy relentlessly until satisfied or currency exhausted
            print(('Bitshares API', command, satoshi_str(amount), 'at', satoshi_str(price)))
            while 1:
                try:
                    time.sleep(0.05 * attempt ** 2)
                    if attempt > 1:
                        print('buy attempt:', attempt)
                    # Gather curated public data
                    '*************************************'
                    metaNODE = Bitshares_Trustless_Client()
                    '*************************************'
                    last = metaNODE['last']
                    currency = metaNODE['currency_balance']
                    assets = metaNODE['asset_balance']
                    # Authenticate via pybitshares
                    account, market, node, chain = reconnect(BitPAIR, USERNAME, PASS_PHRASE)
                    # Final check, buy no more than 110% market price
                    if (price is None) or (price > 1.1*last):
                        price = 1.1*last
                    # Save last bitshare for fees
                    if BitCURRENCY == 'BTS':
                        currency -= 1
                    # No negative currency
                    currency = max(0,currency)
                    # means to buy is currency in hand divided by order price
                    means = currency/price
                    # order amount no more than 99.8% means
                    if amount > 0.998 * means:
                        print('not enough currency')
                        amount = 0.998 * means
                    # if order amounts to more than dust, place order
                    if amount > MIN_AMOUNT:
                        print(('order final check', command, satoshi_str(amount), 'at', satoshi_str(price)))
                        print('Currency: ', currency, 'Means: ', means)
                        print(market, price, amount, expiration)
                        details = (market.buy(price, amount, expiration))
                        print (details)
                        break
                except Exception as e:
                    if 'balance' in str(e).lower():
                        print('Insufficient Balance')
                        break
                    else:
                        msg = msg_(e)
                        msg += ('\n\n' + str(attempt) + ' ' + ' BUY FAILED, RECONNECTING '
                        + str(node) + ' ' + str(price) + ' ' + str(amount))
                        race_append(doc='EV_log.txt', text=msg)
                        print("buy attempt %s failed" % attempt)
                        attempt += 1
                        if attempt > 10:
                            diagnostics(level=[1,2,3])
                            print(("buy attempt %s WARN: ABORTED" % attempt))
                            break
                        continue
                else:
                    print('no currency to buy')
                    break

        if command == 'sell':
            # sell relentlessly until satisfied or assets exhausted
            print(('Bitshares API', command, satoshi_str(amount), 'at', satoshi_str(price)))
            while 1:
                try:
                    time.sleep(0.05 * attempt ** 2)
                    if attempt > 1:
                        print('sell attempt:', attempt)
                    # Gather curated public data
                    '*************************************'
                    metaNODE = Bitshares_Trustless_Client()
                    '*************************************'
                    last = metaNODE['last']
                    currency = metaNODE['currency_balance']
                    assets = metaNODE['asset_balance']
                    # Authenticate via pybitshares
                    account, market, node, chain = reconnect(BitPAIR, USERNAME, PASS_PHRASE)
                    # Final check, sell no less than 90% market price
                    if (price is None) or (price < 0.9*last):
                        price = 0.9*last
                    # Final check, amount no more than 99.8% assets
                    if BitASSET == 'BTS':
                        assets -= 1 # Save last bitshare for fees
                    assets = max(0,assets)
                    if amount > 0.998 * assets:
                        print('not enough assets')
                        amount = 0.998 * assets
                    # Final Check, min bid size
                    if amount > MIN_AMOUNT:
                        print(('order final check', command, satoshi_str(amount), 'at', satoshi_str(price)))
                        details = (market.sell(price, amount, expiration))
                        details = str(details)
                        print (details)
                        race_append(doc='EV_log.txt', text=details)
                        break
                except Exception as e:
                    if 'balance' in str(e).lower():
                        print('Insufficient Balance')
                        break
                    else:
                        msg = msg_(e)
                        msg += ('\n\n' + str(attempt) + ' ' + ' SELL FAILED, RECONNECTING '
                        + str(node) + ' ' + str(price) + ' ' + str(amount))
                        race_append(doc='EV_log.txt', text=msg)
                        print(("sell attempt %s failed" % attempt))
                        attempt += 1
                        if attempt > 10:
                            diagnostics(level=[1,2,3])
                            print(("sell attempt %s WARN: ABORTED" % attempt))
                            break
                        continue
                else:
                    print('no assets to sell')
                    break

    else:
        print('buy/sell request under MIN_AMOUNT')

    if command == 'cancel':
        # cancel reapeatedly until arrive at server with nothing to cancel
        print(('Bitshares API', command))
        i = 0
        while 1:
            try:
                i+=1
                time.sleep(0.05 * i ** 2)
                '*************************************'
                metaNODE = Bitshares_Trustless_Client()
                '*************************************'
                orders = metaNODE['orders']
                break
            except:
                continue
        while len(orders):
            time.sleep(0.05 * attempt ** 2)
            if attempt > 1:
                print('cancel attempt:', attempt)
            try:
                account, market, node, chain = reconnect(BitPAIR, USERNAME, PASS_PHRASE)
                '*************************************'
                metaNODE = Bitshares_Trustless_Client()
                '*************************************'
                orders = metaNODE['orders']
                i += 1
                print((len(orders), 'open orders to cancel'))
                order_list = []
                for order in orders:
                    order_list.append(order['orderNumber'])
                details = market.cancel(order_list)
                print (details)
            except Exception as e:
                msg = msg_(e)
                race_append(doc='EV_log.txt', text=msg)
                print(("cancel attempt %s failed" % attempt))
                attempt += 1
                if attempt > 10:
                    diagnostics(level=[1,2,3])
                    print ('cancel aborted')
                continue
        print('no orders to cancel')

    signal.value = 0

def nodes_fetch():

        metaNODE = Bitshares_Trustless_Client()
        return metaNODE['whitelist']

# TEXT PIPE
# ======================================================================

def Bitshares_Trustless_Client(): # creates metaNODE dictionary

    # Include this definition in your script to access metaNODE.txt
    # Deploy your bot script in the same folder as metaNODE.py
    i = 0
    while True:
        try:
            time.sleep(0.05 * i ** 2)
            i += 1
            with open('metaNODE.txt', 'r') as f:
                #diagnostics(level=[1])
                ret = f.read()
                f.close()
                try:
                    metaNODE = literal(ret)
                    break
                except:
                    pass
                try:
                    ret = ret.split('}')[0] + '}'
                    metaNODE = literal(ret)
                    break
                except:
                    raise
        except Exception as e:
            msg = str(type(e).__name__) + str(e.args)
            msg += ' Bitshares_Trustless_Client()'
            print(msg)
            diagnostics(level=[1,2,3])
            try:
                f.close()
            except:
                pass
            pass
        finally:
            try:
                f.close()
            except:
                pass
    return metaNODE

def race_read(doc=''):  # Concurrent Read from File Operation

    i = 0
    while True:
        try:
            time.sleep(0.05 * i ** 2)
            i += 1
            with open(doc, 'r') as f:
                ret = f.read()
                f.close()
                try:
                    ret = literal(ret)
                except:
                    pass
                try:
                    ret = ret.split(']')[0] + ']'
                    ret = literal(ret)
                except:
                    pass
                try:
                    ret = ret.split('}')[0] + '}'
                    ret = literal(ret)
                except:
                    if '{' in ret:
                        ret = {}
                    else:
                        ret = []
                break
        except Exception as e:
            msg = str(type(e).__name__) + str(e.args)
            msg += ' race_read()'
            print(msg)
            try:
                f.close()
            except:
                pass
            continue
        finally:
            try:
                f.close()
            except:
                pass
    return ret

def race_write(doc='', text=''):  # Concurrent Write to File Operation

    text = str(text)
    i = 0
    while True:
        try:
            time.sleep(0.05 * i ** 2)
            i += 1
            with open(doc, 'w+') as f:
                f.write(text)
                f.close()
                break
        except Exception as e:
            msg = str(type(e).__name__) + str(e.args)
            msg += ' race_write()'
            print(msg)
            try:
                f.close()
            except:
                pass
            continue
        finally:
            try:
                f.close()
            except:
                pass

def race_append(doc='', text=''):  # Concurrent Append to File Operation

    text = '\n' + str(time.ctime()) + ' ' + str(text) + '\n'
    i = 0
    while True:
        time.sleep(0.05 * i ** 2)
        i += 1
        if i > 10:
            break
        try:
            with open(doc, 'a+') as f:
                f.write(text)
                f.close()
                break
        except Exception as e:
            msg = str(type(e).__name__) + str(e.args)
            msg += ' race_append()'
            print(msg)
            try:
                f.close()
            except:
                pass
            continue
        finally:
            try:
                f.close()
            except:
                pass

def watchdog():

    identity = 0 # metaNODE:1, botscript:0
    max_latency = 60

    while 1:
        try:
            try:
                with open('watchdog.txt', 'r') as f:
                    ret = f.read()
                    f.close()

                ret = literal(ret)
                response = int(ret[identity])
                now = int(time.time())
                latency = now-response

                if identity == 0:
                    msg = str([response, now])
                if identity == 1:
                    msg = str([now, response])

                with open('watchdog.txt', 'w+') as f:
                    f.write(msg)
                    f.close()

                msg = str(latency)
                if latency > max_latency:
                    bell()
                    gmail()
                    msg += ' !!!!! WARNING: the other app is not responding !!!!!'
                return msg
   
            except Exception as e:
                msg = str(type(e).__name__) + str(e.args)
                print(msg)
                now = int(time.time())
                with open('watchdog.txt', 'w+') as f:
                    f.write(str([now, now]))
                    f.close()
                    break # exit while loop
        except Exception as e:
            msg = str(type(e).__name__) + str(e.args)
            print(msg)
            try:
                f.close()
            except:
                pass 
        finally:
            try:
                f.close()
            except:
                pass

# CANDLES and CEX DATA
# ======================================================================

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

def chartdata(pair, start, stop, period):

    # before sending request on to chartdata2
    # allow for altcoin/altcoin pair
    # (ASSET1/BTC) / (ASSET2/BTC)

    # this synthetic process can introduce abberations in dataset
    # METHOD in tune_install allows for reconstruction method control

    if CURRENCY in ['BTC', 'USD', 'CNY']:

        return chartdata2(pair, start, stop, period)
    else:

        PAIR1 = ('%s_%s' % ('BTC', ASSET))
        PAIR2 = ('%s_%s' % ('BTC', CURRENCY))

        dataset1 = chartdata2(PAIR1, start, stop, period)
        dataset2 = chartdata2(PAIR2, start, stop, period)

        minlen = min(len(dataset1), len(dataset2))

        dataset1 = (dataset1)[-minlen:]
        dataset2 = (dataset2)[-minlen:]

        #{"time","close","high","low","open","volumefrom","volumeto"}

        dataset3 = []

        method = METHOD

        for i in range(len(dataset1)):
            print(i)

            d1_h = dataset1[i]['high']
            d2_h = dataset2[i]['high']
            d1_l = dataset1[i]['low']
            d2_l = dataset2[i]['low']
            d1_o = dataset1[i]['open']
            d2_o = dataset2[i]['open']
            d1_c = dataset1[i]['close']
            d2_c = dataset2[i]['close']
            
            time = dataset1[i]['time']
            _close = d1_c/d2_c
            _open = d1_o/d2_o

            # in this section various methods can be entertained
            # ##################################################
            if method == 0: # most likely
                _high = d1_h/d2_c
                _low = d1_l/d2_c

            if method == 1: # most unrealistic profitable
                _high = d1_h/d2_l
                _low = d1_l/d2_h              

            if method == 2:
                _high = d1_h/d2_h # most conservative least profitable
                _low = d1_l/d2_l 

            if method == 3: # halfway between 1 and 2
                _high = ((d1_h+d1_c)/2) / ((d2_l+d2_c)/2)
                _low = ((d1_l+d1_c)/2) / ((d2_h+d2_c)/2)

            # if method == 4: # etc...
            # ##################################################

            _low = min(_high, _low, _open, _close)
            _high = max(_high, _low, _open, _close)

            volumefrom = dataset1[i]['volumefrom'] / dataset2[i]['volumefrom']
            volumeto = dataset1[i]['volumeto'] / dataset2[i]['volumeto']
            candle = {  'time':time,
                        'close':_close,
                        'high':_high,
                        'low':_low,
                        'open':_open,
                        'volumefrom':volumefrom,
                        'volumeto':volumeto}
            dataset3.append(candle)

        print(dataset1)
        print('')
        print(dataset2)
        print('')
        print(dataset3)
        print('')
        print(dataset1[0])
        print('')
        print(dataset2[0])
        print('')
        print(dataset3[0])
        
        return dataset3

def chartdata2(pair, start, stop, period):  # Public API cryptocompare

    #{"time","close","high","low","open","volumefrom","volumeto"}
    # docs at https://www.cryptocompare.com/api/
    # print(('API call for chartdata %s %ss %se CANDLE %s DAYS %s' % (
    #    pair, start, stop, period, int((stop - start) / 86400.0))))
    connected = 0
    while not connected:
        try:
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
                    print((len(clean_d),
                         (clean_d2[-1]['time'], clean_d1[0]['time']),
                        (clean_d1[0]['time'] - clean_d2[-1]['time'])))
                    print()
                if len(clean_d):
                    return clean_d

            else:
                print('invalid period')
                return None
        except Exception as e:
            msg = msg_(e)
            race_append(doc='EV_log.txt', text=msg)
            print (msg, 'chartdata() failed; try again...')
            plt.pause(5)
            pass

def currencies():  # Public API cryptocompare

    try:
        uri = 'https://min-api.cryptocompare.com/data/all/coinlist'
        params = {}
        ret = requests.get(uri, params=params).json()
        print(('API currencies', len(ret['Data']),
               'coins at cryptocompare'))
        return ret['Data']
    except Exception as e:
        msg = msg_(e)
        race_append(doc='EV_log.txt', text=msg)
        print ('currencies() failed; skipping...')
        return {}

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
    except Exception as e:
        msg = msg_(e)
        race_append(doc='EV_log.txt', text=msg)
        print ('cryptocompare_time() failed; skipping...')
        return -1

def cryptocompare_last():  # CEX last price

    connected = 0
    while not connected:
        try:
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
            connected = 1
            return price, volume, latency
        except Exception as e:
            msg = msg_(e)
            race_append(doc='EV_log.txt', text=msg)
            print ('cryptocompare_last() failed; try again...')
            plt.pause(5)
            pass
            
def marketcap():  # Public API coinmarketcap

    try:
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
    except Exception as e:
        msg = msg_(e)
        race_append(doc='EV_log.txt', text=msg)
        print ('marketcap() failed; skip...')
        return 999,999,999

# LIVE
# ======================================================================

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
    global info
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
            print('$$$$$$$$$$$$$$$$$$')
            print('WARN: DEBUG - RUNTIME: %s' % (info['current_time']-info['begin']))
            print('$$$$$$$$$$$$$$$$$$')
            print('')
            print('WATCHDOG LATENCY:', watchdog())
            price, volume, latency = cryptocompare_last()
            storage['cc_last'] = {
                'price': price, 'volume': volume, 'latency': latency}
            cryptocompare_time()
            live_data()
            indicators()
            state_machine()
            hourly()
            daily()
            dex_auth('cancel')
            scalp()
            trade()
            live_chart()
            plot_format()
            live_plot()
            plt.pause(10)
            info['tick'] += 1


        else:
            plt.pause(0.05)
            print('')
            print('RUNTIME: %s' % (info['current_time']-info['begin']))
            print('')
            print('WATCHDOG LATENCY:', watchdog())
            print('')
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
                plt.pause(0.05)
                price, volume, latency = cryptocompare_last()
                storage['cc_last'] = {
                    'price': price, 'volume': volume, 'latency': latency}
            except:
                msg += 'cryptocompare_last() '
                attempt += 1
                continue
            try:
                plt.pause(0.05)
                cryptocompare_time()
            except:
                msg += 'cryptocompare_time() '
                attempt += 1
                continue
            print('')
            try:
                plt.pause(0.05)
                live_data()
            except:
                msg += 'live_data() '
                attempt += 1
                continue
            try:
                plt.pause(0.05)
                indicators()
            except:
                msg += 'indicators() '
                attempt += 1
                continue
            try:
                plt.pause(0.05)
                state_machine()
            except:
                msg += 'state_machine() '
                attempt += 1
                continue
            # LOWER FREQENCY EVENTS
            plt.pause(0.05)
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

            # CANCEL ALL OUTSTANDING ORDERS IN THIS MARKET
            plt.pause(0.05)
            try:
                dex_auth('cancel')
            except:
                msg += 'cancel() '
                attempt += 1
                continue

            if 1.02*storage['buying'] < price < 0.98*storage['selling']:

                # SCALP OPS
                plt.pause(0.05)
                try:
                    scalp()
                except:
                    msg += 'scalp() '
                    attempt += 1
                    continue

                # TRADE OPS
                plt.pause(0.05)
                try:
                    trade()
                except:
                    msg += 'trade() '
                    attempt += 1
                    continue
            else:

                # TRADE OPS
                plt.pause(0.05)
                try:
                    trade()
                except:
                    msg += 'trade() '
                    attempt += 1
                    continue

                # SCALP OPS
                plt.pause(0.05)
                try:
                    scalp()
                except:
                    msg += 'scalp() '
                    attempt += 1
                    continue




            # PLOT
            plt.pause(0.05)
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
            plt.pause(0.05)
            msg = ''
            print('tick', info['tick'])
            info['tick'] += 1
            info['completion_time'] = int(time.time())
            attempt = 0

            # DELAY NEXT TICK

            if storage['HFT']:
                print('HFT True')
                set_timing(TICK)
            else:
                plt.pause(300)

def set_timing(tick_size):  # Limits live tick interval (seconds)

    print('set_timing()')
    now = time.time()
    elapsed = now - info['begin']
    # ticks that should have occurred
    ticks = int(elapsed / tick_size)
    # ticks that should have, less ticks that actually did
    tick_drift = ticks - info['tick']
    # duration of the latest tick
    tick_elapsed = now - info['completion_time']

    drift = info['tick']*tick_size - elapsed
    wait = min(drift, tick_size)
    print(('wait: %.2f, drift: %.2f, tick: %s, tick drift %s, tick elapsed, %.2f' % (
            wait, drift, info['tick'], tick_drift, tick_elapsed)))
    if wait > 0:
        plt.pause(wait)

def live_data():  # Gather live data from public and private api

    global portfolio
    global data
    global storage

    print('live_data()')
    '*************************************'
    metaNODE = Bitshares_Trustless_Client()
    '*************************************'
    print('metaNODE()')
    orders = metaNODE['orders']
    dex_rate = storage['dex_rate'] = float(metaNODE['last'])
    book = storage['book'] = metaNODE['book']
    portfolio['currency'] = float(metaNODE['currency_balance'])
    portfolio['assets'] = float(metaNODE['asset_balance'])
    book = metaNODE['book']

    # orderbook and last price
    sbids = [('%.8f' % i) for i in book['bidp'][:3]]
    sbids = sbids[::-1]
    sasks = [('%.8f' % i) for i in book['askp'][:3]]
    print (sbids, 'BIDS <> ASKS', sasks)

    # populate 2h candles, 5m candles, and market rate
    data['7200'] = live_candles(PAIR, candle=7200, depth=int(MA2 * 13))
    data['300'] = live_candles(PAIR, candle=300, depth=300)
    cex_rate = storage['cex_rate'] = storage['cc_last']['price']

    print('')
    print(('cex_rate: ', ('%.8f' % cex_rate)))
    print(('dex_rate: ', ('%.8f' % dex_rate)))
    print(('delta   : ', ('%.8f' % (cex_rate - dex_rate))))
    print('')

def scalp():  # Initiate secondary order placement


    # localize data
    global storage
    now = int(time.time())

    '*************************************'
    metaNODE = Bitshares_Trustless_Client()
    '*************************************'
    book = metaNODE['book']

    ask_p = book['askp'][0]
    ask_v = book['askv'][0]
    bid_p = book['bidp'][0]
    bid_v = book['bidv'][0]
    ask_p2 = book['askp'][1]
    bid_p2 = book['bidp'][1]

    dex_rate = metaNODE['last']

    cex_rate = storage['cex_rate']
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
    max_currency = storage['max_currency']
    max_assets = storage['max_assets']

    # force dex market under/over cex market per market cross
    offset = 0.98
    if market_cross:
        offset = 1.02
    # define scalp support and resistance
    scalp_resistance = offset*max(high, ma3, ma4)
    scalp_support = offset*min(low, ma3, ma4)
    # limit scalp ops to buying/selling window
    max_scalp_support = ((1 - MIN_MARGIN) * selling)  # 97% of selling
    min_scalp_resistance = ((1 + MIN_MARGIN) * buying)  # 103% of buying
    scalp_support = min(scalp_support, max_scalp_support)
    scalp_resistance = max(scalp_resistance, min_scalp_resistance)
    # limit scalp ops to dex bid/ask
    scalp_resistance = min(scalp_resistance, 0.99999*ask_p)
    scalp_support = max(scalp_support, 1.000001*bid_p)
    # adjust scalp margins if too thin
    scalp_margin = (scalp_resistance - scalp_support) / scalp_support
    if scalp_margin < MIN_MARGIN:
        midscalp = (scalp_resistance + scalp_support)/2
        scalp_resistance = (1 + MIN_MARGIN / 2) * midscalp
        scalp_support = (1 - MIN_MARGIN / 2) * midscalp
    # store scalp thresholds globally
    storage['scalp_resistance'] = scalp_resistance
    storage['scalp_support'] = scalp_support

    # update portfolio assets and currency
    '*************************************'
    metaNODE = Bitshares_Trustless_Client()
    '*************************************'
    currency = portfolio['currency'] = float(metaNODE['currency_balance'])
    assets = portfolio['assets'] = float(metaNODE['asset_balance'])

    # means to buy and percent invested
    means = storage['means'] = currency / dex_rate
    max_assets = storage['max_assets'] = (assets + means)
    storage['max_currency'] = max_assets * dex_rate
    invested = assets / max_assets
    holding = storage['holding']

    if holding: # primary trade() function
        max_holding = 1
        min_holding = 1-SCALP_FUND
    else:
        max_holding = SCALP_FUND
        min_holding = 0

    buy_qty = max(0, max_assets * (max_holding-invested))
    sell_qty = max(0, max_assets * (invested - min_holding))


    buy_qty = min(buy_qty, max_assets*SCALP_FUND)
    sell_qty = min(sell_qty, max_assets*SCALP_FUND)

    pieces = SCALP_PIECES
    pie = []
    for i in range (pieces):
        pie.append(random())
    total = sum(pie)
    for i in range (pieces):
        pie[i] = pie[i]/total

    if info['tick'] == 0:
        storage['begin_max_assets'] = max_assets
        storage['begin_max_currency'] = max_currency
        storage['start_price'] = dex_rate

    roi_assets = max_assets / storage['begin_max_assets']
    roi_currency = max_currency / storage['begin_max_currency']
    buy_hold = dex_rate/storage['start_price']
    sell_wait = 1/buy_hold

    if SCALP:
        print('')
        print('begin scalp() ops')
        print('')
        print('assets        ', satoshi_str(assets))
        print('currency      ', satoshi_str(currency))
        print('invested      ', ('%.2f' % invested))
        print('means         ', satoshi_str(means))
        print('max assets    ', satoshi_str(max_assets))
        print('max currency  ', satoshi_str(max_currency))
        print('start assets  ', satoshi_str(storage['begin_max_assets']))
        print('start currency', satoshi_str(storage['begin_max_currency']))
        print('start price   ', satoshi_str(storage['start_price']))
        print('roi assets    ', ('%.2f' % roi_assets))
        print('roi currency  ', ('%.2f' % roi_currency))
        print('buy_hold      ', ('%.2f' % buy_hold))
        print('sell_wait     ', ('%.2f' % sell_wait))



        print('holding       ', holding)
        print('max_holding   ', max_holding)
        print('min holding   ', min_holding)
        print('buy qty       ', buy_qty)
        print('sell_qty      ', sell_qty)
        print('scalp s       ', satoshi_str(scalp_support))
        print('scalp r       ', satoshi_str(scalp_resistance))
        print('pieces        ', pieces, pie)
        print('')

        for i in range(pieces):

            # SCALP BUY
            qty = buy_qty*pie[i]
            scalp = scalp_support - i *2*random()*SATOSHI
            try:
                print(('scalp buy', satoshi_str(qty), 'at', satoshi_str(scalp)))
                dex_auth('buy', price=scalp, amount=qty)
            except:
                pass

            # SCALP SELL
            qty = sell_qty*pie[i]
            scalp = scalp_resistance + i *2*random()*SATOSHI
            try:
                print(('scalp sell', satoshi_str(qty), 'at', satoshi_str(scalp)))
                dex_auth('sell', price=scalp, amount=qty)
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

        print('')
        print('begin trade() ops')
        print('')

        book = storage['book']
        ask_p = book['askp'][0]
        bid_p = book['bidp'][0]
        dex_rate = storage['dex_rate']
        cex_rate = storage['cex_rate']
        assets = portfolio['assets']
        currency = portfolio['currency']
        asset_ratio = storage['asset_ratio']
        means = storage['means']
        invested = portfolio['percent_invested']
        divested = portfolio['percent_divested']
        min_order = 0.00011 / dex_rate
        max_assets = (MAX_ASSETS / 100.0) * (assets + (currency / dex_rate))
        max_currency = (MAX_CURRENCY / 100.0) * (currency + (assets * dex_rate))

        print(('assets %.1f, max assets %.1f' % (assets, max_assets)))
        pieces = 10.0  # order size

        if MANUAL_OVERRIDE:
            storage['selling'] = selling = MANUAL_SELL
            storage['buying'] = buying = MANUAL_BUY

        storage['HFT'] = False
        if SCALP or RECYCLE:
            storage['HFT'] = True

        if ORDER_TEST:
            dex_auth('buy',  price=0.9*dex_rate, amount=1)
            dex_auth('sell', price=1.1*dex_rate, amount=1)

        if dex_rate > selling:
            storage['holding'] = False
        if dex_rate < buying:
            storage['holding'] = True

        qty = max_assets / pieces
        if (dex_rate > 0.90 * selling):
            print('')
            print('APPROACHING SELL POINT')
            if BELL:
                bell(0.5, 800)
            if (portfolio['assets'] > 0.1):
                if (divested < MAX_CURRENCY):
                    storage['HFT'] = True
                    selling_r = max(selling, (dex_rate + ask_p) / 2)
                    try:
                        # iceberg
                        print(
                            ('SELLING', PAIR, 'RATE', ('%.8f' %
                             selling_r), 'AMOUNT', ('%.1f' %
                             qty)))
                        dex_auth('sell', price=selling_r, amount=qty)
                        # iceberg front limit
                        selling_r *= 1.0 - 0.015*random()
                        qty /= randint(69,99)
                        if random() > 0.5:
                            print(
                                ('SELLING MINI', PAIR, 'RATE', ('%.8f' %
                                 selling_r), 'AMOUNT', ('%.1f' %
                                 qty)))
                            dex_auth('sell', price=selling_r, amount=qty)
                    except:
                        print('SELL FAILED')
                        pass
                else:
                    print('MAX DIVESTED')
            else:
                print('NO ASSETS')

        qty = max_assets / pieces
        if dex_rate < 1.20 * buying:
            print('')
            print('APPROACHING BUY POINT')
            if BELL:
                bell(0.5, 800)
            if (portfolio['currency'] > 0.1):
                if (invested < MAX_ASSETS):
                    storage['HFT'] = True
                    buying_r = min(buying, (dex_rate + bid_p) / 2)
                    try:
                        print(
                            ('BUYING', PAIR, 'RATE', ('%.8f' %
                             buying_r), 'AMOUNT', ('%.1f' %
                             qty)))
                        dex_auth('buy', price=buying_r, amount=qty)
                        buying_r *= 1.0 + 0.015*random()
                        qty /= randint(69,99)
                        if random() > 0.5:
                            print(
                                ('BUYING MINI', PAIR, 'RATE', ('%.8f' %
                                 buying_r), 'AMOUNT', ('%.1f' %
                                 qty)))
                            dex_auth('buy', price=buying_r, amount=qty)
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
# ======================================================================

def initialize():  # Open plot, set backtest days

    global DAYS

    if MODE == 0:
        print('~=== OPTIMIZING 1D CANDLES =================~')
    if MODE == 1:
        print('~=== BEGIN BACKTEST 1D CANDLES =============~')
    if MODE == 2:
        print('~=== WARMING UP PAPER SESSION 2H CANDLES ===~')
    if MODE == 3:
        print('')
        print('')
        print('NOTE: THIS IS ALPHA RELEASE TO PUBLIC DOMAIN WITH NO WARRANTY')
        print('')
        print('')
        print('~=== WARMING UP LIVE MACHINE 2H CANDLES ====~')
    if MODE == 4:
        print('~=== BEGIN SALES BACKTEST 1D CANDLES =======~')
    if MODE in [2,3]:
        print('This will require a cpu core and 2.5 gigs RAM for a few minutes...')
    if MODE == 6:
        print('~=== BEGIN LIVE BUY/SELL/CANCEL TEST =======~')
    if LIVE:
        DAYS = WARMUP
        watchdog()
        dex_auth('cancel')
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

    if (SALES or OPTIMIZE) and (DAYS >= OPTIMIZE_DAYS): # 365
        DAYS = OPTIMIZE_DAYS
    if LIVE or BACKTEST:
        plt.ion()
        fig = plt.figure()
        fig.patch.set_facecolor('0.15')
        fig.canvas.set_window_title(VERSION)

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
    storage['holding'] = True
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
            if LIVE and (info['tick']%50==0):
                plt.pause(0.0001)
        else:
            test_stop()
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
    storage['holding'] = True
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
        watchdog()

def test_sell(price):  # Execute a backtest sell

    storage['trades'] += 1
    now = info['current_time']
    storage['sells'][0].append(info['current_time'])
    storage['sells'][1].append(price)
    portfolio['currency'] = portfolio['assets'] * price
    storage['holding'] = False
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
        watchdog()

# PLOT, PRINT, ALARM
# ======================================================================

def draw_state_machine(  # Plots primary trade indications
        now, selloff, support, resistance, despair,
        buying, selling, min_cross, max_cross,
        market_cross, ma1, ma2, ma1poly, ma2poly):

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

        plt.plot((now, now), (max_cross, min_cross),
                 color='white', label='cross', alpha=1.0)

        plt.plot(now, ma1, markersize=0.5, marker='.',
                 color='aqua', label='ma1')
        plt.plot(now, ma2, markersize=6, marker='.',
                 color='aqua', label='ma2')

        plt.plot(now, ma1poly, markersize=0.5, marker='.',
                 color='aqua', label='ma1poly_')
        plt.plot(now, ma2poly, markersize=6, marker='.',
                 color='aqua', label='ma2poly_')

        plt.plot(now, max_cross, markersize=3, marker='.',
                 color='white', label='max_cross')
        plt.plot(now, min_cross, markersize=3, marker='.',
                 color='white', label='min_cross')

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
    ma1 = ma1poly = storage['ma1'][-1]
    ma2 = ma2poly = storage['ma2'][-1]
    if info['live']:
           ma1poly = storage['ma1poly'][-1]
           ma2poly = storage['ma2poly'][-1]
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

    draw_state_machine(  # Plots primary trade indications
            now, selloff, support, resistance, despair,
            buying, selling, min_cross, max_cross,
            market_cross, ma1, ma2, ma1poly, ma2poly)

    # plot candles
    plt.plot((now, now), ((high[-1]), (low[-1])),
             color='m', label='high_low', alpha=0.5)
    plt.plot(now, (close[-1]), markersize=4, marker='.',
             color='y', label='close')

    if info['tick'] == 0:
        chart_star()

def live_chart():  # Add objects to live plot

    book = storage['book']
    cex_rate = storage['cex_rate']
    dex_rate = storage['dex_rate']
    m_volume = storage['m_volume']
    ma1 = storage['ma1'][-1]
    ma2 = storage['ma2'][-1]
    ma1poly = storage['ma1poly'][-1]
    ma2poly = storage['ma2poly'][-1]
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
    draw_state_machine(  
            now, selloff, support, resistance, despair,
            buying, selling, min_cross, max_cross,
            market_cross, ma1, ma2, ma1poly, ma2poly)

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
                    ma1 = ma1poly = ma1_arr[i]
                    ma2 = ma2poly = ma2_arr[i]
                    

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
                    draw_state_machine(  
                            now, selloff, support, resistance, despair,
                            buying, selling, min_cross, max_cross,
                            market_cross, ma1, ma2, ma1poly, ma2poly)
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
    #plt.title(('%s ' % PAIR) + VERSION)
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
    '''
    textx = 0.1 * (plt.xlim()[1] - plt.xlim()[0]) + plt.xlim()[0]
    texty = 0.8 * (plt.ylim()[1] - plt.ylim()[0]) + plt.ylim()[0]
    storage['text'].append(plt.text(textx, texty,
                                    'litepresence', color='aqua',
                                    alpha=0.2, size=70))
    '''
    textx = 0.1 * (plt.xlim()[1] - plt.xlim()[0]) + plt.xlim()[0]
    texty = 0.7 * (plt.ylim()[1] - plt.ylim()[0]) + plt.ylim()[0]
    storage['text'].append(plt.text(textx, texty,
                                    'EXTINCTION EVENT', color='aqua',
                                    alpha=0.3, size=25, weight='extra bold'))
    '''
    textx = 0.1 * (plt.xlim()[1] - plt.xlim()[0]) + plt.xlim()[0]
    texty = 0.08 * (plt.ylim()[1] - plt.ylim()[0]) + plt.ylim()[0]
    storage['text'].append(
        plt.text(textx, texty, '(BTS) litepresence1',
                 color='white', alpha=0.5, size=10, weight='extra bold'))
    '''
    textx = 0.4 * (plt.xlim()[1] - plt.xlim()[0]) + plt.xlim()[0]
    texty = 0.1 * (plt.ylim()[1] - plt.ylim()[0]) + plt.ylim()[0]
    pair = PAIR
    if info['live']:
        pair = BitPAIR

    storage['text'].append(
        plt.text(textx, texty, pair,
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
    ax.set_xlim(([(now - LIVE_PLOT_DEPTH), (now + LIVE_PLOT_PROJECTION)]))
    # Prevent Memory Leak Outside Plot Window; remove unnecessary data
    for line in ax.get_lines():
        xval = line.get_xdata()[0]
        if (xval < (ax.get_xlim()[0])):
            line.remove()
            del line
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
    print(('# DPT           : %.1f' % storage['dpt']))
    print(('# MARKET CAP    : %.1fM' % asset_cap))
    print(('# DOMINANCE     : %.4f - RANK %s' % (asset_dominance, asset_rank)))
    print(('# ROI           : %.2fX' % storage['roi_currency']))
    # print(('APY             = %.2f' % storage['apy_currency']))
    print('#######################################')

def bell(duration=2, frequency=432):  # Activate linux audible bell

    pass
    '''
    os.system('play --no-show-progress --null --channels 1 synth' +
                  ' %s sine %f' % (duration*1000, frequency))
    '''

def gmail():

    pass
    '''
    send_to     = "THE EMAIL ADDRESS TO SEND TO"
    send_from   = "YOUR EMAIL ADDRESS"
    pass        = "YOUR PASSWORD"
    msg         = "YOUR MESSAGE!"

    import smtplib
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(send_from, pass)
    server.sendmail(send_from, send_to, msg)
    server.quit()
    '''

# DIAGNOSTICS
# ======================================================================

def msg_(e):  # traceback message
    print('                                                                 !@#$%^&*(){}[]{}()*&^%$#@!')
    print('send questions, comments, and pastebin of pertinent logs')
    print('to @litepresence on telegram for faster development')
    print('')
    return ('=========================================================================='+
            '\n\n' + str(time.ctime()) + ' ' + str(type(e).__name__) +
            '\n\n' + str(e.args) +
            '\n\n' + str(traceback.format_exc()) +
            '\n\n' )

def diagnostics(level=[]):

    try:
        import psutil # REQUIRES MODULE INSTALL
        proc = psutil.Process()
    
        if 1 in level:
            num_open_files = proc.num_fds()
            print('')
            print('file descriptors:', num_open_files)
            print('connections:', len(proc.connections()))
        if 2 in level:
            import psutil
            proc = psutil.Process()
            n = 1
            open_files = proc.open_files()
            for i in range(len(open_files)):
                if 'ttf' not in str(open_files[i]):
                    print (n, str(open_files[i]).split('/')[-1])
                    n+=1
            print(proc.io_counters())
            connections = proc.connections()
            for i in range(len(connections)):
                print (i, connections[i])
            print('')
            processes = psutil.process_iter()
            for i in range(len(processes)):
                print (i, processes[i])
            print('')
    except Exception as e:
        msg = str(type(e).__name__) + str(e.args) + 'psutil'
        print(msg)

    if 3 in level:
        fds = {}
        base = '/proc/self/fd'
        for num in os.listdir(base):
            try:
                fds[int(num)] = os.readlink(os.path.join(base, num))
            except:
                pass
        print(fds)
    print('')

# DATA PROCESSING
# ======================================================================

def clock():  # 24 hour clock formatted HH:MM:SS
    return str(time.ctime())[11:19]

def satoshi(n):  # format prices to satoshi type
    return float('%.8f' % float(n))

def satoshi_str(n):
    return ('%.8f' % float(n))

def dictionaries():  # Global info, data, portfolio, and storage

    global info, storage, portfolio, book
    info = {}
    book = {}
    storage = {}
    portfolio = {}

def coin_name():  # Convert ticker symbols to coin names

    curr = currencies()
    if ASSET in ['USD', 'CNY']:
        storage['asset_name'] = ASSET
    else:
        storage['asset_name'] = curr[ASSET]['CoinName']

    if CURRENCY in ['USD', 'CNY']:
        storage['currency_name'] = CURRENCY
    else:
        storage['currency_name'] = curr[CURRENCY]['CoinName']
    print((storage['asset_name']), storage['currency_name'])

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

def float_sma(array, period):  # floating point period moving average

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
# ======================================================================

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
        ma1 = storage['ma1'] = float_sma(
            data['7200']['close'], ma1_period)
        ma2 = storage['ma2'] = float_sma(
            data['7200']['close'], ma2_period)

        # scalp moving averages
        storage['ma3'] = float_sma(data['300']['close'], 288 * MA3)
        storage['ma4'] = float_sma(data['300']['close'], 288 * MA4)

        # 20 minute high and low
        storage['high'] = max(data['300']['high'][-4:])
        storage['low'] = min(data['300']['low'][-4:])
        cex_rate = storage['cex_rate']

        # means to buy and percent invested
        assets = portfolio['assets']
        currency = portfolio['currency']
        means = storage['means'] = currency / cex_rate
        max_assets = storage['max_assets'] = (assets + means)
        storage['max_currency'] = max_assets * cex_rate

        storage['asset_ratio'] = assets / max_assets
        portfolio['percent_invested'] = 100 * storage['asset_ratio']
        portfolio['percent_divested'] = 100 - portfolio['percent_invested']

        # recent volume ratio for plotting
        depth = 100
        mv = ((depth * data['300']['volume'][-1]) /
              sum(data['300']['volume'][-depth:]))
        storage['m_volume'] = 1 if mv < 1 else 5 if mv > 5 else mv

        ax = plt.gca()

        for line in ax.lines:
            if str(line.get_label()) in ['ma2poly', 'ma1poly']:
                line.remove()
                del line


        if info['tick']==0:
            storage['ma1poly'] = ma1
            storage['ma2poly'] = ma2
        else:
            ma1x = []
            ma1y = []
            for line in ax.lines:
                if str(line.get_label()) == 'ma1':
                    ma1x = ma1x + list(line.get_xdata())
                    ma1y = ma1y + list(line.get_ydata())
            ma1poly = np.polyfit(ma1x,ma1y,2)
            stop = time.time()
            start = stop-86400
            ma1poly_x = np.linspace(start, stop, num=13)
            ma1poly_y = np.polyval(ma1poly, ma1poly_x)
            plt.plot(ma1poly_x,ma1poly_y*MIN_CROSS, markersize=1, marker='.',
                     color='yellow', label='ma1poly')
            plt.plot(ma1poly_x,ma1poly_y*MIN_CROSS*MAX_CROSS, markersize=1, marker='.',
                     color='yellow', label='ma1poly')
            #plt.plot(ma1poly_x[-1], ma1poly_y[-1], markersize=0.5, marker='.',
            #         color='magenta', label='ma1_')
            start = time.time()
            stop = start + LIVE_PLOT_PROJECTION
            ma1poly_x_ = np.linspace(start, stop, num=13)
            ma1poly_y_ = np.polyval(ma1poly, ma1poly_x_)
            plt.plot(ma1poly_x_,ma1poly_y_*MIN_CROSS, markersize=1, marker='.',
                     color='yellow', label='ma1poly')
            plt.plot(ma1poly_x_,ma1poly_y_*MIN_CROSS*MAX_CROSS, markersize=1, marker='.',
                     color='yellow', label='ma1poly')
            plt.plot(ma1poly_x_[-1], ma1poly_y_[-1]*MIN_CROSS*MAX_CROSS, markersize=2, marker='.',
                     color='magenta', label='ma1poly_shadow')
            plt.plot(ma1poly_x_[-1], ma1poly_y_[-1]*MIN_CROSS, markersize=2, marker='.',
                     color='magenta', label='ma1poly_shadow')
            ma2x = []
            ma2y = []
            for line in ax.lines:
                if str(line.get_label()) == 'ma2':
                    ma2x = ma2x + list(line.get_xdata())
                    ma2y = ma2y + list(line.get_ydata())
            ma2poly = np.polyfit(ma2x,ma2y,2)
            stop = time.time()
            start = stop-86400
            ma2poly_x = np.linspace(start, stop, num=13)
            ma2poly_y = np.polyval(ma2poly, ma2poly_x)
            plt.plot(ma2poly_x, ma2poly_y, markersize=1, marker='.',
                     color='yellow', label='ma2poly')
            #plt.plot(ma2poly_x[-1], ma2poly_y[-1], markersize=6, marker='.',
            #         color='magenta', label='ma2_')
            start = time.time()
            stop = start + LIVE_PLOT_PROJECTION
            ma2poly_x_ = np.linspace(start, stop, num=13)
            ma2poly_y_ = np.polyval(ma2poly, ma2poly_x_)
            plt.plot(ma2poly_x_, ma2poly_y_, markersize=1, marker='.',
                     color='yellow', label='ma2poly')
            plt.plot(ma2poly_x_[-1], ma2poly_y_[-1], markersize=1, marker='.',
                     color='magenta', label='ma2poly_shadow')

            plt.pause(0.0001)
            storage['ma1poly'] = ma1poly_y
            storage['ma2poly'] = ma2poly_y


def state_machine():  # Alpha and beta market finite state

    # localize primary indicators

    
    ma1 = storage['ma1'][-1]
    ma2 = storage['ma2'][-1]
    if info['live']:
        ma1 = storage['ma1poly'][-1]
        ma2 = storage['ma2poly'][-1]
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


    # calculate slope, concavity, and divergence to print only
    if info['live']:
        ma1 = storage['ma1poly']
        ma2 = storage['ma2poly']
        ma1_slope = ma1[-1]-ma1[-13]
        ma2_slope = ma2[-1]-ma2[-13]
        ma1_concavity = (ma1[-1]-ma1[-7])-(ma1[-7]-ma1[-13])
        ma2_concavity = (ma2[-1]-ma2[-7])-(ma2[-7]-ma2[-13])

        ma1_ = storage['ma1poly'][-13]
        ma2_ = storage['ma2poly'][-13]
        min_cross_ = MIN_CROSS * ma1_
        max_cross_ = MAX_CROSS * min_cross_
        signal = min_cross
        signal_ = min_cross_
        if storage['market_cross']:
            signal = max_cross
            signal_ = max_cross_

        mesh = abs(ma2[-1]-signal)
        mesh_ = abs(ma2_-signal_)
        if mesh_-mesh < 0:
            next_cross = 99999
        else:
            next_cross = mesh/(mesh_-mesh)
        ma2 = '%.8f' % ma2[-1]
        ma2_slope = '%.8f' % ma2_slope
        ma2_concavity = '%.8f' % ma2_concavity
        signal = '%.8f' % signal
        ma1_slope = '%.8f' % ma1_slope
        ma1_concavity = '%.8f' % ma1_concavity
        mesh = '%.8f' % mesh
        next_cross = '%.2f' % next_cross
        print('days to next crossing:', next_cross)
        print('long average (aqua): ', ma2, 'slope:', ma2_slope, 'concavity:', ma2_concavity)
        print('signal line (white): ', signal, 'slope:', ma1_slope, 'concavity:', ma1_concavity)
        print('divergence:   ', mesh)
        print('')

def optimizer():  # Stochastic ROI assent backpropagation

    pass


# PRIMARY PROCESS
# ======================================================================
if __name__ == "__main__":

    race_write(doc='EV_log.txt', text=time.ctime())
    banner()
    version()
    tune_install()
    keys_install()
    asset_cap, asset_dominance, asset_rank = marketcap()
    optimize = False
    data = {}
    control_panel()
    dictionaries()
    initialize()
    test_initialize()
    coin_name()
    if (MODE in [2, 3, 6]) or BACKTEST:
        backtest()
    print_tune()
    if MODE in [2, 3, 6]:
        print('')
        print('report errors to litepresence for faster development')
        print('')
        live()

    if OPTIMIZE:
        optimizer()
        print ('https://www.youtube.com/watch?v=5ydqjqZ_3oc')
        sys.exit()
# ======================================================================
''' EXTINCTION EVENT '''
# ======================================================================
#
# THE DESTROYER,
# litepresence - 2018
#
