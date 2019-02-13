
#=======================================================================
VERSION = 'Bitshares metaNODE 0.00000018'
#=======================================================================

# Trustless Public Node Statistical Curation Utility

' litepresence 2019 '


def WTFPL_v0_March_1765():
    if any([stamps, licenses, taxation, regulation, fiat, etat]):
        try:
            print('no thank you')
        except:
            return [tar, feathers]

' ********** ALPHA RELEASE TO PUBLIC DOMAIN WITH NO WARRANTY ********* '

# 99.99% uptime
# no rogue data, no stale data
# no hung processes, no runaway processes
# maintains whitelist of validated tested nodes for buy/sell/cancel ops
# no pybitshares dependencies

' metaNODE '

# is a dict of account history and market conditions for one DEX pair
# stored in json format in file metaNODE.txt
# it can be accessed by ANY script in ANY language
# this statistically curated data is updated every few seconds
# you can tail any of these live updated texts:

'metaNODE.txt'
'metaNODElog.txt'
'whitelist.txt'
'blacklist.txt'
'nodes.txt'
'account_history.txt'  # you may wish to back this up from time to time

# to access metaNODE data from any python scirpt:

''' metaNODE = Bitshares_Trustless_Client() '''

# access time with SSD is about 0.0002 seconds

DEV = False
COLOR = True

' STANDARD PYTHON MODULES '

from random import random, shuffle, randint, choice
from multiprocessing import Process, Value
from json import loads as json_loads
from json import dumps as json_dumps
from datetime import datetime
from statistics import mode
import traceback
import requests
import psutil
import numpy
import time
import sys
import os

' MODULES WHICH MAY REQUIRE INSTALLATION '

print('pip3 install websocket-client')
from websocket import create_connection as wss  # handshake to node
import websocket

if DEV:
    websocket.enableTrace(True)

print("\033c")  # clear screen


def version():

    global version

    version = "".join(i for i in VERSION if i in "0123456789.")

    sys.stdout.write(
        '\x1b]2;' +
        'Bitshares metaNODE' +  # terminal title bar
        '\x07')


def it(style, text):

    emphasis = {'red': 91,
                'green': 92,
                'yellow': 93,
                'blue': 94,
                'purple': 95,
                'cyan': 96}

    return (('\033[%sm' % emphasis[style]) + str(text) + '\033[0m')

# GLOBALS
# ======================================================================


def controls():

    global TIMEOUT, PROCESSES, MAVENS, UTILIZATIONS
    global BOOK_DEPTH, HISTORY_DEPTH, THRESH_PAUSE, BLIP
    global BIFURCATION_PAUSE, LATENCY_TIMEOUT, LATENCY_REPEAT

    # suggested values
    BLIP = 0.0001  # 0.0001
    MAVENS = 7  # 7
    TIMEOUT = 100  # 100
    PROCESSES = 20  # 20
    BOOK_DEPTH = 10  # 10
    THRESH_PAUSE = 4  # 4
    UTILIZATIONS = 30  # 30
    HISTORY_DEPTH = 30  # 30
    LATENCY_REPEAT = 3600  # 3600
    LATENCY_TIMEOUT = 7  # 7
    BIFURCATION_PAUSE = 2  # 2


def public_nodes():

    global nodes, node_count, static, static_nodes
    static = ''
    # SEEN LIVE SINCE 181127
    static_nodes = [
        'wss://altcap.io/wss',
        'wss://api-ru.bts.blckchnd.com/ws',
        'wss://api.bitshares.bhuz.info/wss',
        'wss://api.bitsharesdex.com/ws',
        'wss://api.bts.ai/ws',
        'wss://api.bts.blckchnd.com/wss',
        'wss://api.bts.mobi/wss',
        'wss://api.bts.network/wss',
        'wss://api.btsgo.net/ws',
        'wss://api.btsxchng.com/wss',
        'wss://api.dex.trading/ws',
        'wss://api.fr.bitsharesdex.com/ws',
        'wss://api.open-asset.tech/wss',
        'wss://atlanta.bitshares.apasia.tech/wss',
        'wss://australia.bitshares.apasia.tech/ws',
        'wss://b.mrx.im/wss',
        'wss://bit.btsabc.org/wss',
        'wss://bitshares.crypto.fans/wss',
        'wss://bitshares.cyberit.io/ws',
        'wss://bitshares.dacplay.org/wss',
        'wss://bitshares.dacplay.org:8089/wss',
        'wss://bitshares.openledger.info/wss',
        'wss://blockzms.xyz/ws',
        'wss://bts-api.lafona.net/ws',
        'wss://bts-seoul.clockwork.gr/ws',
        'wss://bts.liuye.tech:4443/wss',
        'wss://bts.open.icowallet.net/ws',
        'wss://bts.proxyhosts.info/wss',
        'wss://btsfullnode.bangzi.info/ws',
        'wss://btsws.roelandp.nl/ws',
        'wss://chicago.bitshares.apasia.tech/ws',
        'wss://citadel.li/node/wss',
        'wss://crazybit.online/wss',
        'wss://dallas.bitshares.apasia.tech/wss',
        'wss://dex.iobanker.com:9090/wss',
        'wss://dex.rnglab.org/ws',
        'wss://dexnode.net/ws',
        'wss://england.bitshares.apasia.tech/ws',
        'wss://eu-central-1.bts.crypto-bridge.org/wss',
        'wss://eu.nodes.bitshares.ws/ws',
        'wss://eu.openledger.info/ws',
        'wss://france.bitshares.apasia.tech/ws',
        'wss://frankfurt8.daostreet.com/wss',
        'wss://japan.bitshares.apasia.tech/wss',
        'wss://kc-us-dex.xeldal.com/ws',
        'wss://kimziv.com/ws',
        'wss://la.dexnode.net/ws',
        'wss://miami.bitshares.apasia.tech/ws',
        'wss://na.openledger.info/ws',
        'wss://ncali5.daostreet.com/wss',
        'wss://netherlands.bitshares.apasia.tech/ws',
        'wss://new-york.bitshares.apasia.tech/ws',
        'wss://node.bitshares.eu/ws',
        'wss://node.market.rudex.org/wss',
        'wss://nohistory.proxyhosts.info/wss',
        'wss://openledger.hk/wss',
        'wss://paris7.daostreet.com/wss',
        'wss://relinked.com/wss',
        'wss://scali10.daostreet.com/wss',
        'wss://seattle.bitshares.apasia.tech/wss',
        'wss://sg.nodes.bitshares.ws/ws',
        'wss://singapore.bitshares.apasia.tech/ws',
        'wss://status200.bitshares.apasia.tech/wss',
        'wss://us-east-1.bts.crypto-bridge.org/ws',
        'wss://us-la.bitshares.apasia.tech/ws',
        'wss://us-ny.bitshares.apasia.tech/ws',
        'wss://us.nodes.bitshares.ws/wss',
        'wss://valley.bitshares.apasia.tech/ws',
        'wss://ws.gdex.io/ws',
        'wss://ws.gdex.top/wss',
        'wss://ws.hellobts.com/wss',
        'wss://ws.winex.pro/wss'
    ]

    try:
        nodes = race_read(doc='nodes.txt')
    except:
        nodes = []
        race_write('nodes.txt', json_dumps(static_list))
        print('nodes.txt not found using list stored in public_nodes()')
        pass
    if len(nodes) < 20:
        nodes = static_nodes
        static = ' ::WARN:: USING STATIC NODE LIST'
    node_count = len(nodes)


def constants():

    global TZ, ID, SATOSHI

    TZ = time.timezone
    SATOSHI = 0.00000001
    ID = '4018d7844c78f6a6c41c6a552b898022310fc5dec06da467ee7905a8dad512c8'


def sign_in():

    global account_name, currency, asset

    print('''
    (BTS) litepresence1

    Resistance and Disobedience in Economic Activity
    is the Most Moral Human Action Possible
    -SEK3''')

    print('')
    print('Input Account and Market, or press Enter for demo')
    print('')

    account_name = input('account name: ').strip('"').strip("'")
    print('')
    currency = input('    currency: ').strip('"').strip("'").upper()
    print('')
    asset = input('       asset: ').strip('"').strip("'").upper()
    print('')

    if account_name == '':
        account_name = 'abc123'
    if currency == '':
        currency = 'OPEN.BTC'
    if asset == '':
        asset = 'BTS'


def initialize():

    global mean_ping
    global BEGIN, access, data_latency
    data_latency = 0
    BEGIN = time.time()
    access = 0
    mean_ping = 0.5
    now = int(time.time())
    race_write(doc='blacklist.txt', text=json_dumps([]))
    race_write(doc='whitelist.txt', text=json_dumps([]))
    race_write(doc='metaNODElog.txt', text=json_dumps(''))
    race_write(doc='metaNODE.txt', text=json_dumps({}))
    race_write(doc='mavens.txt', text=json_dumps([]))
    race_write(doc='watchdog.txt', text=json_dumps([now, now]))

# TEXT PIPE
# ======================================================================


def Bitshares_Trustless_Client():  # Your access to the metaNODE
    # Include this definition in your script to access metaNODE.txt
    # Deploy your bot script in the same folder as metaNODE.py
    while True:
        try:
            with open('metaNODE.txt', 'r') as f:
                ret = f.read()  # .replace("'",'"')
                f.close()
                metaNODE = json_loads(ret)
                break
        except Exception as e:
            msg = trace(e)
            race_condition = ['Unterminated', "Expecting"]
            if any([x in str(e.args) for x in race_condition]):
                print('metaNODE = Bitshares_Trustless_Client() RACE READ')
            elif 'metaNODE is blank' in str(e.args):
                continue
            else:
                print('metaNODE = Bitshares_Trustless_Client() ' + msg)
            try:
                f.close()
            except:
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
        time.sleep(BLIP * i ** 2)
        i += 1
        try:
            with open(doc, 'r') as f:
                ret = f.read().replace("'", '"')
                f.close()
                try:
                    # ret = json_loads(ret)
                    ret = json_loads(ret)
                except:
                    try:
                        ret = ret.split(']')[0] + ']'
                        # ret = json_loads(ret)
                        ret = json_loads(ret)
                    except:
                        try:
                            ret = ret.split('}')[0] + '}'
                            # ret = ljson_loads(ret)
                            ret = json_loads(ret)
                        except:
                            print ('race_read() failed %s' % str(ret))
                            if '{' in ret:
                                ret = {}
                            else:
                                ret = []
                break
        except Exception as e:
            if DEV:
                print(trace(e))
            try:
                f.close()
            except:
                pass
        finally:
            try:
                f.close()
            except:
                pass
    return ret


def race_write(doc='', text=''):  # Concurrent Write to File Operation

    if not isinstance(text, str):
        text = str(text)

    i = 0
    while True:
        time.sleep(BLIP * i ** 2)
        i += 1
        try:
            with open(doc, 'w+') as f:
                f.write(text)
                f.close()
                break
        except Exception as e:
            print(trace(e))
            try:
                f.close()
            except:
                pass
        finally:
            try:
                f.close()
            except:
                pass


def race_append(doc='', text=''):  # Concurrent Append to File Operation

    text = ('{"ctime":"' +
            str(time.ctime()) +
            '", "comment":' +
            str(text) +
            '}\n')
    i = 0
    while True:
        time.sleep(BLIP * i ** 2)
        i += 1
        try:
            if i > 10:
                break
            with open(doc, 'a+') as f:
                f.write(text)
                f.close()
                break
        except Exception as e:
            print(trace(e))
            try:
                f.close()
            except:
                pass
        finally:
            try:
                f.close()
            except:
                pass


def watchdog():

    identity = 1  # metaNODE:1, botscript:0
    max_latency = 600

    while True:
        try:
            try:
                with open('watchdog.txt', 'r') as f:
                    ret = f.read()
                    f.close()

                ret = json_loads(ret)
                response = int(ret[identity])
                now = int(time.time())
                latency = now - response

                if identity == 0:
                    msg = str([response, now])
                if identity == 1:
                    msg = str([now, response])

                with open('watchdog.txt', 'w+') as f:
                    f.write(msg)
                    f.close()

                msg = str(latency)
                if latency > max_latency:
                    msg += ' !!!!! WARNING: app is not responding !!!!!'
                return msg

            except Exception as e:
                print(trace(e))
                now = int(time.time())
                with open('watchdog.txt', 'w+') as f:
                    f.write(str([now, now]))
                    f.close()
                    break  # exit while loop
        except Exception as e:
            print(trace(e))
            try:
                f.close()
            except:
                pass
        finally:
            try:
                f.close()
            except:
                pass

# RPC DATABASE CALLS
# ======================================================================


def wss_handshake(node):
    global ws
    start = time.time()
    handshake_max = min(9.999, 10 * mean_ping)
    ws = wss(node, timeout=handshake_max)
    handshake_latency = min(9.999, (time.time() - start))
    if 0 > handshake_latency > handshake_max:
        raise ValueError('slow handshake', handshake_latency)
    return handshake_latency, handshake_max


def wss_query(params):
    query = json_dumps({"method": "call",
                        "params": params,
                        "jsonrpc": "2.0",
                        "id": 1})
    ws.send(query)
    ret = json_loads(ws.recv())
    try:
        return ret['result']  # if there is result key take it
    except:
        return ret


def rpc_lookup_accounts():
    ret = wss_query(['database',
                     'lookup_accounts',
                     [account_name, 1]])
    account_id = ret[0][1]
    return account_id


def rpc_lookup_asset_symbols():
    ret = wss_query(['database',
                     'lookup_asset_symbols',
                     [[asset, currency]]])
    asset_id = ret[0]['id']
    asset_precision = ret[0]['precision']
    currency_id = ret[1]['id']
    currency_precision = ret[1]['precision']

    return asset_id, asset_precision, currency_id, currency_precision


def rpc_ping_latency():
    start = time.time()
    chain_id = wss_query(['database',
                          'get_chain_id',
                          []])
    ping_latency = min(9.999, (time.time() - start))
    ping_max = min(2, 2 * mean_ping)
    if chain_id != ID:
        raise ValueError('chain_id != ID')
    if 0 > ping_latency > ping_max:
        raise ValueError('slow ping', ping_latency)
    return ping_latency, ping_max


def rpc_block_latency():
    dgp = wss_query(['database',
                     'get_dynamic_global_properties',
                     []])
    blocktime = from_iso_date(dgp['time'])
    block_latency = min(9.999, (TZ + time.time() - blocktime))
    block_max = min(9.999, (3 + 3 * mean_ping))
    if 0 > block_latency > block_max:
        raise ValueError('stale blocktime', block_latency)
    return block_latency, block_max, int(blocktime)


def rpc_last(currency, asset):
    ticker = wss_query(['database',
                        'get_ticker',
                        [currency, asset, False]])
    last = precision(ticker['latest'], 16)
    if float(last) == 0:
        raise ValueError('zero price last')
    return last


def rpc_market_history(currency, asset, now, then, depth=100):
    trade_history = wss_query(['database',
                               'get_trade_history',
                               [currency, asset, now, then, depth]])
    history = []
    for i in range(len(trade_history)):
        unix = int(from_iso_date(trade_history[i]['date']))
        price = precision(trade_history[i]['price'], 16)
        if float(price) == 0:
            raise ValueError('zero price in history')
        amount = precision(
            trade_history[i]['amount'], asset_precision)
        history.append([unix, price, amount])
    if not len(history):
        raise ValueError('no history')
    return history


def rpc_account_balances(account_name,
                         asset_ids=[],
                         asset_precisions=[]):
    if '1.3.0' not in asset_ids:
        asset_ids.append('1.3.0')
        asset_precisions.append(5)
    ret = wss_query(['database',
                     'get_named_account_balances',
                     [account_name, asset_ids]])
    balances = {}
    for j in range(len(asset_ids)):
        balances[asset_ids[j]] = 0
    for j in range(len(asset_ids)):
        for k in range(len(ret)):
            if ret[k]['asset_id'] == asset_ids[j]:
                balances[asset_ids[j]] += float(
                    ret[k]['amount']) / 10 ** asset_precisions[j]
    return balances


def rpc_open_orders(asset, asset_id, asset_precision,
                    currency, currency_id, currency_precision):
    # a databnase call to the api returns price as fraction
    # with unreferenced decimal point locations on both amounts
    # they're also reference by A.B.C instead of ticker symbol
    ret = wss_query(['database',
                     'get_full_accounts',
                     [[account_name], False]])
    try:
        limit_orders = ret[0][1]['limit_orders']
    except:
        limit_orders = []
    BitPAIR = asset + ":" + currency
    orders = []
    for order in limit_orders:
        orderNumber = order['id']
        base_id = order['sell_price']['base']['asset_id']
        quote_id = order['sell_price']['quote']['asset_id']
        if ((base_id in [currency_id, asset_id]) and
                (quote_id in [currency_id, asset_id])):
            amount = float(order['for_sale'])
            base_amount = float(order['sell_price']['base']['amount'])
            quote_amount = float(order['sell_price']['quote']['amount'])
            if base_id == currency_id:
                base_precision = currency_precision
                quote_precision = asset_precision
            else:
                base_precision = asset_precision
                quote_precision = currency_precision
            base_amount /= 10 ** base_precision
            quote_amount /= 10 ** quote_precision
            if base_id == asset_id:
                orderType = 'sell'
                price = quote_amount / base_amount
                amount = (amount / 10 ** base_precision)
            else:
                orderType = 'buy'
                price = base_amount / quote_amount
                amount = (amount / 10 ** base_precision) / price
            orders.append({'orderNumber': orderNumber,
                           'orderType': orderType,
                           'market': BitPAIR,
                           'amount': precision(amount, asset_precision),
                           'price': precision(price, 16)})
    return sorted(orders, key=lambda k: k['price'])


def rpc_book(currency, asset, depth=3):
    order_book = wss_query(['database',
                            'get_order_book',
                            [currency, asset, depth]])
    askp = []
    bidp = []
    askv = []
    bidv = []
    for i in range(len(order_book['asks'])):
        price = precision(order_book['asks'][i]['price'], 16)
        if float(price) == 0:
            raise ValueError('zero price in asks')
        volume = precision(
            order_book['asks'][i]['quote'], asset_precision)
        askp.append(price)
        askv.append(volume)
    for i in range(len(order_book['bids'])):
        price = precision(order_book['bids'][i]['price'], 16)
        if float(price) == 0:
            raise ValueError('zero price in bids')
        volume = precision(
            order_book['bids'][i]['quote'], asset_precision)
        bidp.append(price)
        bidv.append(volume)
    if float(bidp[0]) >= float(askp[0]):
        raise ValueError('mismatched orderbook')

    return askp, bidp, askv, bidv

# CURATION
# ======================================================================


def latency():

    # in loop, latency test the static list to produce nodes.txt
    # qualify round 1 = good chain id, 1000ms ping, 5000ms handshake
    # all three ending suffixes are tested for each static list domain
    # only one of each suffix is allowed to pass
    # latency() itself is a is a multiprocess child of spawn
    # all tests done by latency() are multiprocess timeout wrapped

    global mean_ping  # within this latency() process

    def test(node, signal):
        try:
            wss_handshake(node)  # < 5 second hanshake
            rpc_ping_latency()  # < 1 second ping AND good chain id
            rpc_block_latency()  # < 4.5 second blocktime
            signal.value = 1  # if no exceptions pipe true response
        except Exception as e:
            signal.value = 0
            # print('********',trace(e))

    def validate(nodes):  # remove suffixes for each domain
        v = nodes[:]
        for i in range(len(v)):
            if v[i].endswith('/'):
                v[i] = v[i][:-1]
        for i in range(len(v)):
            if v[i].endswith('/ws'):
                v[i] = v[i][:-3]
        for i in range(len(v)):
            if v[i].endswith('/wss'):
                v[i] = v[i][:-4]
        return sorted(list(set(v)))

    def suffix(v):  # add suffixes for each validated domain

        wss = [(i + '/wss') for i in v]
        ws = [(i + '/ws') for i in v]
        v = v + wss + ws
        return sorted(v)

    mean_ping = 0.5
    while True:
        start = time.time()
        whitelist = []
        blacklist = []
        suffixed_nodes = suffix(validate(static_nodes))
        for node in suffixed_nodes:
            # do not retest whitelisted domains with another suffix
            if validate([node])[0] not in validate(whitelist):
                # wrap test in timed multiprocess
                signal = Value('d', 0)
                t_process = Process(target=test, args=(node, signal,))
                t_process.daemon = False
                t_process.start()
                t_process.join(LATENCY_TIMEOUT)
                # kill hung process and blacklist the node
                if t_process.is_alive():
                    t_process.join()
                    t_process.terminate()
                    blacklist.append(node)
                # bad chain id, ping, handshake, or blocktime
                elif (signal.value == 0):
                    blacklist.append(node)
                # good chain id, ping, handshake, and blocktime
                elif (signal.value == 1):
                    # if domain is not already in list
                    whitelist.append(node)
        # nodes.txt is used as metaNODE's primary universe
        race_write('nodes.txt', json_dumps(whitelist))
        race_write('blacklist2.txt', json_dumps(blacklist))
        # repeat latency testing periodically per LATENCY_REPEAT
        time.sleep(max(0, (LATENCY_REPEAT - (time.time() - start))))


def cache():  # acquire account id; asset ids, and asset precisions

    # given account name, currency and asset symbols, lookup these globals
    global account_id, asset_id, currency_id, bw_depth
    global asset_precision, currency_precision, BEGIN

    bw_depth = 10

    def wwc():
        print("\033c")
        logo()
        print('')
        print(time.ctime(), '\n')
        print('Winnowing Websocket Connections...')
        print('==================================', '\n')

    account_ids, asset_ids, currency_ids = [], [], []
    asset_precisions, currency_precisions = [], []

    # trustless of multiple nodes
    while True:
        try:
            wwc()
            black = race_read(doc='blacklist.txt')
            white = race_read(doc='whitelist.txt')
            # switch nodes
            public_nodes()
            shuffle(nodes)
            node = nodes[0]
            print(node)
            if node in black:
                raise ValueError('blacklisted')
            if node in white:
                raise ValueError('whitelisted')
            # reconnect and make calls
            wss_handshake(node)
            account_id = rpc_lookup_accounts()
            asset_id, asset_precision, currency_id, currency_precision = (
                rpc_lookup_asset_symbols())
            # prepare for statistical mode of cache items
            asset_ids.append(asset_id)
            account_ids.append(account_id)
            currency_ids.append(currency_id)
            asset_precisions.append(asset_precision)
            currency_precisions.append(currency_precision)
            # mode of cache
            if len(asset_ids) > 4:
                try:
                    asset_id = mode(asset_ids)
                    account_id = mode(account_ids)
                    currency_id = mode(currency_ids)
                    asset_precision = mode(asset_precisions)
                    currency_precision = mode(currency_precisions)
                    websocket.enableTrace(False)
                    print_market()
                    BEGIN = int(time.time())
                    winnow('whitelist', node)
                    break
                except:
                    winnow('blacklist', node)
                    continue
        except Exception as e:
            print(trace(e))
            continue


def spawn():  # multiprocessing handler

    # initialize latency testing process
    l_process = Process(target=latency)
    l_process.daemon = False
    l_process.start()

    # initialize bifurcation process
    b_process = Process(target=bifurcation)
    b_process.daemon = False
    b_process.start()

    # initialize portfolio history log
    h_process = Process(target=history)
    h_process.daemon = False
    h_process.start()

    # initialize multiple threshing processes
    b = 0
    c = 0
    multinode = {}
    for a in range(PROCESSES):
        c += 1
        multinode[str(a)] = Process(target=thresh, args=(a, b, c))
        multinode[str(a)].daemon = False
        multinode[str(a)].start()
        time.sleep(BLIP)
    # kill and respawn threshing processes periodically for durability
    # even if anything gets hung metaNODE always moves on
    # a = process of PROCESSES; b = respawn epoch; c = process id
    # every time a process is respawned it gets new process id

    while True:
        public_nodes()
        b += 1
        race_write(doc='metaNODElog.txt', text='')
        for a in range(PROCESSES):
            c += 1
            time.sleep(TIMEOUT / 2 + TIMEOUT * random())
            try:
                multinode[str(a)].terminate()
            except Exception as e:
                msg = trace(e)
                print('terminate() WARNING', msg)
                race_append(doc='metaNODElog.txt', text=msg)
                pass
            try:
                multinode[str(a)] = Process(target=thresh, args=(a, b, c))
                multinode[str(a)].daemon = False
                multinode[str(a)].start()
            except Exception as e:
                msg = trace(e)
                print('process() WARNING', msg)
                race_append(doc='metaNODElog.txt', text=msg)
                pass


def thresh(process, epoch, pid):  # make calls, shake out errors

    global bw_depth, mean_ping, access, data_latency

    handshake_bs = []
    ping_bs = []
    block_bs = []
    reject_bs = []
    access = 0
    data_latency = 0
    while True:
        mean_ping = 0.5
        try:
            public_nodes()
            shuffle(nodes)
            node = nodes[0]
            bw_depth = max(int(node_count / 6), 1)

            # CHECK BLACK AND WHITE LISTS
            black = race_read(doc='blacklist.txt')[-bw_depth:]
            white = race_read(doc='whitelist.txt')[-bw_depth:]
            try:
                start = time.time()
                metaNODE = Bitshares_Trustless_Client()
                access = time.time() - start
                ping = mean_ping = metaNODE['ping']
                blacklist = metaNODE['blacklist'][-bw_depth:]
                whitelist = metaNODE['whitelist'][-bw_depth:]
                blocktime = metaNODE['blocktime']
                data_latency = TZ + time.time() - blocktime
                del metaNODE
                if len(blacklist) > len(black):
                    black = blacklist
                    race_write('blacklist.txt', json_dumps(black))

                if len(whitelist) > len(white):
                    white = whitelist
                    race_write('whitelist.txt', json_dumps(white))
            except:
                pass

            if node in black:
                raise ValueError('blacklisted')
            if node in white:
                raise ValueError('whitelisted')

            # connect to websocket
            handshake_latency, handshake_max = wss_handshake(node)
            # use each node several times
            utilizations = UTILIZATIONS
            if (time.time() - BEGIN) < 100:
                utilizations = 1
            for i in range(utilizations):
                time.sleep(THRESH_PAUSE)
                # Database calls w/ data validations
                ping_latency, ping_max = rpc_ping_latency()
                block_latency, block_max, blocktime = rpc_block_latency()
                set_timing = ('                  ' +
                              'speed/max/ratio/cause/rate')
                if handshake_max == 5:
                    set_timing = ('                  ' +
                                  it('red',
                                     'RESOLVING MEAN NETWORK SPEED'))
                # timing analysis for development
                ping_r = ping_latency / ping_max
                block_r = block_latency / block_max
                handshake_r = handshake_latency / handshake_max
                ping_b = int(bool(int(ping_r)))
                block_b = int(bool(int(block_r)))
                handshake_b = int(bool(int(handshake_r)))
                reject_b = int(bool(ping_b + block_b + handshake_b))
                ping_bs.append(ping_b)
                block_bs.append(block_b)
                reject_bs.append(reject_b)
                handshake_bs.append(handshake_b)
                ping_bs = ping_bs[-100:]
                block_bs = block_bs[-100:]
                reject_bs = reject_bs[-100:]
                handshake_bs = handshake_bs[-100:]
                ping_p = sum(ping_bs) / len(ping_bs)
                block_p = sum(block_bs) / len(block_bs)
                reject_p = sum(reject_bs) / len(reject_bs)
                handshake_p = sum(handshake_bs) / len(handshake_bs)
                ping_b = str(ping_b).ljust(7)
                block_b = str(block_b).ljust(7)
                handshake_b = str(handshake_b).ljust(7)
                reject = ''.ljust(7)
                if reject_b:
                    reject = it('red', 'X'.ljust(7))
                optimizing = it('red', 'OPTIMIZING'.ljust(7))
                if (time.time() - BEGIN) > 200:
                    optimizing = ''.ljust(7)

                # last, history, orderbook, balances, orders
                last = float(rpc_last(currency, asset))
                now = to_iso_date(time.time())
                then = to_iso_date(time.time() - 3 * 86400)
                history = rpc_market_history(
                    currency, asset, now, then, depth=HISTORY_DEPTH)
                askp, bidp, askv, bidv = rpc_book(
                    currency, asset, depth=BOOK_DEPTH)
                ids = [asset_id, currency_id]
                precisions = [asset_precision, currency_precision]
                balances = rpc_account_balances(
                    account_name, asset_ids=ids,
                    asset_precisions=precisions)
                bts_balance = float(balances['1.3.0'])
                asset_balance = float(balances[asset_id])
                currency_balance = float(balances[currency_id])
                orders = rpc_open_orders(
                    asset, asset_id, asset_precision,
                    currency, currency_id, currency_precision)
                # CPU, RAM, IO data REQUIRES MODULE INSTALL
                try:
                    proc = psutil.Process()
                    descriptors = proc.num_fds()
                    usage = ("grep 'cpu ' /proc/stat | awk " +
                             "'{usage=($2+$4)*100/($2+$4+$5)}" +
                             " END {print usage }' ")
                    cpu = '%.3f' % (
                        float(os.popen(usage).readline()))
                    ram = '%.3f' % (100 * float(proc.memory_percent()))
                    io = list(proc.io_counters())[:2]
                except Exception as e:
                    if DEV:
                        print(trace(e))

                watchdog_latency = watchdog()
                metaNODE = Bitshares_Trustless_Client()
                buy_orders = 0
                currency_holding = 0
                currency_max = 0
                sell_orders = 0
                asset_holding = 0
                asset_max = 0
                invested = 0
                divested = 0
                ping = 0.5
                keys = ['bifurcating the metaNODE....']

                m_orders = orders
                m_history = history
                m_last = last
                m_askp = askp
                m_bidp = bidp
                m_askv = askv
                m_bidv = bidv
                m_bts_balance = bts_balance
                m_asset_balance = asset_balance
                m_currency_balance = currency_balance


                try:
                    buy_orders = metaNODE['buy_orders']
                    currency_holding = metaNODE['currency_holding']
                    currency_max = metaNODE['currency_max']
                    sell_orders = metaNODE['sell_orders']
                    asset_holding = metaNODE['asset_holding']
                    asset_max = metaNODE['asset_max']
                    invested = metaNODE['invested']
                    divested = metaNODE['divested']
                    keys = metaNODE['keys']
                    ping = mean_ping = metaNODE['ping']

                    m_orders = metaNODE['orders']
                    m_history = metaNODE['history']
                    m_last = metaNODE['last']
                    m_askp = metaNODE['book']['askp']
                    m_bidp = metaNODE['book']['bidp']
                    m_askv = metaNODE['book']['askv']
                    m_bidv = metaNODE['book']['bidv']
                    m_bts_balance =  metaNODE['bts_balance']
                    m_asset_balance =  metaNODE['asset_balance']
                    m_currency_balance =  metaNODE['currency_balance']

                except:
                    pass
                del metaNODE

                runtime = int(time.time()) - BEGIN
                # bw_depth = max(int(len(nodes) / 6), 1)

                if (len(white) < bw_depth) or (len(black) < bw_depth):
                    alert = it('red',
                               '    BUILDING BLACK AND WHITE LISTS')
                else:
                    alert = ''
                alert += static

                # in the event data passes all tests, then:
                # print, winnow the node, and nascent trend the maven
                print_market()
                print(keys)
                print('')
                print('runtime:epoch:pid', runtime, epoch, pid)
                try:
                    print('fds:processes    ',
                          descriptors,
                          process,
                          'of',
                          PROCESSES)
                except:
                    print('processes    ',
                          process,
                          'of',
                          PROCESSES)
                try:
                    print('cpu:ram:io       ', cpu, ram, io)
                except:
                    pass
                print('utilization:node ', str(i + 1).ljust(3), node)
                print(
                    'total:white:black',
                    len(static_nodes),
                    node_count,
                    len(white),
                    len(black),
                    alert)
                print(set_timing)
                print('block latency    ',
                     ('%.2f %.1f %.1f %s %.2f' % (
                      block_latency,
                      block_max,
                      block_r,
                      block_b,
                      block_p)))
                print('handshake        ',
                     ('%.2f %.1f %.1f %s %.2f' % (
                      handshake_latency,
                      handshake_max,
                      handshake_r,
                      handshake_b,
                      handshake_p)))
                print('ping             ',
                     ('%.2f %.1f %.1f %s %.2f' % (
                      ping_latency,
                      ping_max,
                      ping_r,
                      ping_b,
                      ping_p)))
                print('mean ping        ',
                     (it('yellow', ('%.3f' % ping))),
                      '       %s %.2f' % (reject, reject_p), optimizing)

                print('                 ', [x.rjust(16, ' ')
                      for x in ['name', 'balance', 'orders', 'holding',
                                'max', 'percent']])
                print(
                    'currency         ',
                    it('cyan', [str(x).rjust(16,
                                             ' ') for x in [currency,
                                                            m_currency_balance,
                                                            buy_orders,
                                                            currency_holding,
                                                            currency_max,
                                                            divested]]))
                print(
                    'assets           ',
                    it('cyan', [str(x).rjust(16,
                                             ' ') for x in [asset,
                                                            m_asset_balance,
                                                            sell_orders,
                                                            asset_holding,
                                                            asset_max,
                                                            invested]]))
                print('bitshares        ', m_bts_balance, 'BTS')
                print('')
                print(
                    'history      ',
                    it('yellow', ('%.16f' % m_last)),
                    'LAST with depth',
                    len(m_history))
                for i in range(3):
                    print(it('blue', m_history[i]))
                print('')
                print('asks depth       ', len(m_askp))
                for i in range(3):
                    print(it('red', precision(m_askp[i],16)), m_askv[i])
                print('bids depth       ', len(m_bidp))
                for i in range(3):
                    print(it('green', precision(m_bidp[i],16)), m_bidv[i])
                print('')
                print('open orders      ', len(m_orders))
                for order in m_orders:
                    print(it('yellow', order))
                print('')
                print('watchdog latency:', watchdog_latency)
                print('')

                # send the maven dictionary to nascent_trend()
                # Must be JSON type
                # 'STRING', 'INT', 'FLOAT', '{DICT}', or '[LIST]'
                maven = {}
                maven['ping'] = (19 * mean_ping + ping_latency) / 20  # FLOAT
                maven['bidv'] = bidv  # LIST of precision() STRINGS
                maven['askv'] = askv  # LIST of precision() STRINGS
                maven['bidp'] = bidp  # LIST of precision() STRINGS
                maven['askp'] = askp  # LIST of precision() STRINGS
                maven['bts_balance'] = bts_balance  # FLOAT
                maven['currency_balance'] = currency_balance  # FLOAT
                maven['asset_balance'] = asset_balance  # FLOAT
                maven['market_history'] = history  # LIST OF LISTS
                maven['orders'] = orders  # LIST
                maven['last'] = last  # precision() STRING
                maven['whitelist'] = white  # LIST
                maven['blacklist'] = black  # LIST
                maven['blocktime'] = blocktime  # INT

                nascent_trend(maven)

                # winnow this node to the whitelist
                winnow('whitelist', node)

                # clear namespace
                del maven
                del bidv
                del askv
                del bidp
                del askp
                del bts_balance
                del currency_balance
                del asset_balance
                del history
                del orders
                del last
                del io
                del alert
                del currency_max
                del balances
                del buy_orders
                del ram
                del sell_orders
                del cpu
                del i
                del asset_max
                del keys
                del watchdog_latency
                del asset_holding
                del divested
                del now
                del invested
                del runtime
                del currency_holding
                del descriptors
                del proc

            try:
                time.sleep(BLIP)
                ws.close()
            except Exception as e:
                if DEV:
                    print(trace(e))
                pass
            continue

        except Exception as e:
            try:
                if DEV:
                    print(trace(e))
                time.sleep(BLIP)
                ws.close()
            except:
                pass
            try:
                msg = trace(e) + node
                if (('ValueError' not in msg) and
                    ('StatisticsError' not in msg) and
                    ('result' not in msg) and
                    ('timeout' not in msg) and
                    ('SSL' not in msg) and
                    ('WebSocketTimeoutException' not in msg) and
                    ('WebSocketBadStatusException' not in msg) and
                    ('WebSocketAddressException' not in msg) and
                    ('ConnectionResetError' not in msg) and
                        ('ConnectionRefusedError' not in msg)):
                    msg += '\n' + str(traceback.format_exc())

                if DEV or ((time.time() - BEGIN) > 60):
                    # print(msg)
                    pass
                if 'listed' not in msg:
                    race_append(doc='metaNODElog.txt', text=msg)
                winnow('blacklist', node)
                del msg
            except:
                pass
            continue

    call = call.replace("'", '"')  # never use single quotes


def winnow(x, node):  # seperate good nodes from bad

    if x == 'blacklist':
        black = race_read(doc='blacklist.txt')
        if isinstance(black, list):
            if node in black:
                black.remove(node)
            black.append(node)
            black = black[-bw_depth:]
            race_write(doc='blacklist.txt', text=black)
        else:
            race_write(doc='blacklist.txt', text=[node])

    if x == 'whitelist':
        white = race_read(doc='whitelist.txt')
        if isinstance(white, list):
            if node in white:
                white.remove(node)
            white.append(node)
            white = white[-bw_depth:]
            race_write(doc='whitelist.txt', text=white)
        else:
            race_write(doc='whitelist.txt', text=[node])
    try:
        del white
        del black
        del node
    except:
        pass


def nascent_trend(maven):  # append latest data

    mavens = race_read(doc='mavens.txt')
    if isinstance(mavens, list):
        mavens.append(maven)
        mavens = mavens[-MAVENS:]
        race_write(doc='mavens.txt', text=json_dumps(mavens))
    else:
        race_write(doc='mavens.txt', text=json_dumps([maven]))
    del mavens


def bifurcation():  # statistically curate data

    while True:
        try:

            time.sleep(BIFURCATION_PAUSE)  # take a deep breath
            # initialize the metaNODE dictionary
            metaNODE = {}
            # initialize lists to sort data from each maven by key
            bidp = []
            askp = []
            bidv = []
            askv = []
            bts_balance = []
            currency_balance = []
            asset_balance = []
            history = []
            last = []
            whitelist = []
            blacklist = []
            blocktime = []
            orders = []
            pings = []

            # gather list of maven opinions from the nascent_trend()
            mavens = race_read(doc='mavens.txt')

            # sort maven data for statistical mode analysis by key
            l = len(mavens)
            for i in range(l):
                maven = mavens[i]
                bts_balance.append(maven['bts_balance'])
                currency_balance.append(maven['currency_balance'])
                asset_balance.append(maven['asset_balance'])
                last.append(maven['last'])
                blocktime.append(maven['blocktime'])
                whitelist.append(maven['whitelist'])
                blacklist.append(maven['blacklist'])
                pings.append(maven['ping'])
                # stringify lists for statistical mode of json text
                bidp.append(json_dumps(maven['bidp']))
                askp.append(json_dumps(maven['askp']))
                bidv.append(json_dumps(maven['bidv']))
                askv.append(json_dumps(maven['askv']))
                history.append(json_dumps(maven['market_history']))
                orders.append(json_dumps(maven['orders']))

            # the mean ping of the mavens is passed to the metaNODE
            ping = int(1000 * sum(pings) / (len(pings) + SATOSHI)) / 1000.0
            ping = min(1, ping)

            # find the youngest bitshares blocktime in our dataset
            try:
                blocktime = max(blocktime)
            except:
                print('validating the nascent trend...')
                continue
            # get the mode of the mavens for each metric
            # allow 1 or 2 less than total & most recent for mode
            # accept "no mode" statistics error as possibility
            try:
                bts_balance = mode(bts_balance)
            except:
                try:
                    bts_balance = mode(bts_balance[-(l - 1):])
                except:
                    bts_balance = mode(bts_balance[-(l - 2):])
            try:
                currency_balance = mode(currency_balance)
            except:
                try:
                    currency_balance = mode(currency_balance[-(l - 1):])
                except:
                    currency_balance = mode(currency_balance[-(l - 2):])
            try:
                asset_balance = mode(asset_balance)
            except:
                try:
                    asset_balance = mode(asset_balance[-(l - 1):])
                except:
                    asset_balance = mode(asset_balance[-(l - 2):])
            try:
                last = mode(last)
            except:
                try:
                    last = mode(last[-(l - 1):])
                except:
                    last = mode(last[-(l - 2):])

            try:
                bidp = (mode(bidp))
            except:
                try:
                    bidp = (mode(bidp[-(l - 1):]))
                except:
                    bidp = (mode(bidp[-(l - 2):]))
            try:
                askp = (mode(askp))
            except:
                try:
                    askp = (mode(askp[-(l - 1):]))
                except:
                    askp = (mode(askp[-(l - 2):]))
            try:
                bidv = (mode(bidv))
            except:
                try:
                    bidv = (mode(bidv[-(l - 1):]))
                except:
                    bidv = (mode(bidv[-(l - 2):]))
            try:
                askv = (mode(askv))
            except:
                try:
                    askv = (mode(askv[-(l - 1):]))
                except:
                    askv = (mode(askv[-(l - 2):]))

            try:
                history = (mode(history))
            except:
                try:
                    history = (mode(history[-(l - 1):]))
                except:
                    history = (mode(history[-(l - 2):]))

            try:
                orders = (mode(orders))
            except:
                try:
                    orders = (mode(orders[-(l - 1):]))
                except:
                    orders = (mode(orders[-(l - 2):]))

            # convert statistical mode string back to python object
            history = json_loads(history)
            orders = json_loads(orders)
            bidp = json_loads(bidp)
            askp = json_loads(askp)
            bidv = json_loads(bidv)
            askv = json_loads(askv)

            # attempt a full whitelist and blacklist
            wl = []
            for i in whitelist:
                wl += i
            whitelist = list(set(wl))[-bw_depth:]
            bl = []
            for i in blacklist:
                bl += i
            blacklist = list(set(bl))[-bw_depth:]
            # rebuild orderbook as 4 key dict with lists of floats
            bidp = [float(i) for i in bidp]
            bidv = [float(i) for i in bidv]
            askp = [float(i) for i in askp]
            askv = [float(i) for i in askv]
            book = {'bidp': bidp, 'bidv': bidv, 'askp': askp, 'askv': askv}
            # calculate total outstanding orders
            buy_orders = 0
            sell_orders = 0
            for order in orders:
                if order['orderType'] == 'buy':
                    buy_orders += float(
                        order['amount']) * float(order['price'])
                if order['orderType'] == 'sell':
                    sell_orders += float(order['amount'])
            buy_orders = float(precision(buy_orders, currency_precision))
            sell_orders = float(precision(sell_orders, asset_precision))
            # provide some metadata regarding account balances
            currency_holding = float(currency_balance) + float(buy_orders)
            asset_holding = float(asset_balance) + float(sell_orders)
            currency_max = currency_holding + asset_holding * float(last)
            asset_max = currency_max / float(last)
            invested = 100 * asset_holding / asset_max
            divested = 100 - invested
            currency_holding = float(
                precision(
                    currency_holding,
                    currency_precision))
            asset_holding = float(precision(asset_holding, asset_precision))
            currency_max = float(precision(currency_max, currency_precision))
            asset_max = float(precision(asset_max, asset_precision))
            invested = float(precision(invested, 1))
            divested = float(precision(divested, 1))
            # if you made it this far without statistics error
            # truncate and rewrite the metaNODE with curated data
            # Must be JSON type
            # 'STRING', 'INT', 'FLOAT', '{DICT}', or '[LIST]'
            metaNODE['ping'] = ping  # FLOAT about 0.500
            metaNODE['book'] = book  # DICTIONARY
            metaNODE['bts_balance'] = float(bts_balance)  # FLOAT
            metaNODE['currency_balance'] = float(currency_balance)  # FLOAT
            metaNODE['asset_balance'] = float(asset_balance)  # FLOAT
            metaNODE['history'] = history  # LIST
            metaNODE['orders'] = orders  # LIST
            metaNODE['last'] = float(last)  # FLOAT
            metaNODE['whitelist'] = whitelist  # LIST
            metaNODE['blacklist'] = blacklist  # LIST
            metaNODE['blocktime'] = int(blocktime)  # INT
            metaNODE['account_name'] = account_name  # STRING
            metaNODE['account_id'] = account_id  # STRING A.B.C
            metaNODE['asset'] = asset  # STRING SYMBOL
            metaNODE['asset_id'] = asset_id  # STRING A.B.C
            metaNODE['asset_precision'] = int(asset_precision)  # INT
            metaNODE['currency'] = currency  # STRING SYMBOL
            metaNODE['currency_id'] = currency_id  # STRING A.B.C
            metaNODE['currency_precision'] = int(currency_precision)
            metaNODE['buy_orders'] = float(buy_orders)  # FLOAT
            metaNODE['sell_orders'] = float(sell_orders)  # FLOAT
            metaNODE['currency_holding'] = currency_holding  # FLOAT
            metaNODE['asset_holding'] = asset_holding  # FLOAT
            metaNODE['currency_max'] = currency_max  # FLOAT
            metaNODE['asset_max'] = asset_max  # FLOAT
            metaNODE['invested'] = invested  # FLOAT 0 to 1
            metaNODE['divested'] = divested  # FLOAT 0 to 1
            # add index to metaNODE
            metaNODE['keys'] = list(metaNODE.keys())
            # solitary process with write access to metaNODE.txt
            metaNODE = json_dumps(metaNODE)
            race_write(doc='metaNODE.txt', text=metaNODE)
            print ('metaNODE.txt updated')

            # clear namespace
            del metaNODE
            del mavens
            del maven
            del bidp
            del askp
            del bidv
            del askv
            del bts_balance
            del currency_balance
            del asset_balance
            del history
            del last
            del whitelist
            del blacklist
            del blocktime
            del orders
            del l
            del currency_max
            del i
            del book
            del bl
            del wl
            del currency_holding
            del asset_max
            del divested
            del invested
            del buy_orders
            del asset_holding
            del sell_orders

        except Exception as e:  # wait a second and try again
            # common msg is "no mode statistics error"
            if DEV:
                print(trace(e))
                race_append(doc='metaNODElog.txt', text=msg)
            continue  # from top of while loop NOT pass through error


def history():

    # logs snapshot of account balance to file periodically
    while True:
        time.sleep(3)
        metaNODE = Bitshares_Trustless_Client()
        if metaNODE:
            try:
                keys = [
                    'currency',
                    'asset',
                    'currency_max',
                    'asset_max',
                    'invested']
                snapshot = {k: metaNODE[k] for k in keys}
                snapshot['unix'] = int(time.time())
                race_append(doc='account_history.txt',
                            text=json_dumps(snapshot))
                time.sleep(3600)
            except Exception as e:
                msg = trace(e)
                if DEV:
                    print(msg)
                race_append(doc='metaNODElog.txt', text=msg)
                time.sleep(30)

# HELPER FUNCTIONS
# ======================================================================


def remove_chars(string, chars):
    return ''.join([c for c in string if c not in set(chars)])


def trace(e):  # traceback message

    msg = str(type(e).__name__) + str(e.args)
    if DEV:
        msg += str(traceback.format_exc()) + ' ' + time.ctime()
    if DEV or ((time.time() - BEGIN) > 60):
        return msg
    else:
        return ''


def to_iso_date(unix):  # returns iso8601 datetime given unix epoch

    return datetime.utcfromtimestamp(int(unix)).isoformat()


def from_iso_date(date):  # returns unix epoch given iso8601 datetime

    return int(time.mktime(time.strptime(str(date),
                                         '%Y-%m-%dT%H:%M:%S')))


def precision(x, n):  # string representation of float to n decimal places

    return ('%.' + str(n) + 'f') % float(x)


def print_market():  # terminal header with cached values

    print("\033c")
    logo()
    print('')
    print(time.ctime(),
          it('yellow', ('%.5f' % access)), 'read',
          it('yellow', ('%.1f' % data_latency)), 'data')
    print('==================================================')
    print('account   ', account_name, account_id)
    print('currency  ', currency, currency_id, currency_precision)
    print('asset     ', asset, asset_id, asset_precision)
    print('==================================================')
    print('')


def welcome():

    version()
    print("\033c")
    race_write(doc='metaNODElog.txt', text=str(time.ctime()))
    logo()


def ascii_logo(design):

    urls = {'bitshares': 'https://pastebin.com/raw/xDJkyBrS',
            'microdex': 'https://pastebin.com/raw/3DYAUqQR',
            'extinction-event': 'https://pastebin.com/raw/5YuEHcC4',
            'metanode': 'https://pastebin.com/raw/VALMtPjL'}
    try:
        return (requests.get(urls[design], timeout=(6, 30))).text
    except:
        return ''


def logo():

    global metanode_logo

    def wxyz():
        a = 'abcdef1234567890'
        b = ''
        for i in range(17):
            b = str(b + r'\x' + choice(a) + choice(a))

        return b
    w, x, y, z = wxyz(), wxyz(), wxyz(), wxyz()

    try:
        metanode_logo
    except:
        metanode_logo = ascii_logo('metanode')

    print(it('blue', w))
    print(it('blue', x))
    print(it('cyan', metanode_logo))
    print('                                                          ' +
          version)
    print(it('blue', y))
    print(it('blue', z))

    if DEV:
        msg = ''
        for i in range(17):
            msg += 'DEV '
        print(
            it('red', msg))


def main():  # script primary backbone

    controls()
    welcome()
    initialize()
    public_nodes()
    constants()
    sign_in()
    cache()
    spawn()

if __name__ == "__main__":

    main()
