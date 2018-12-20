
' metaNODE '

# Curates data from all known public API's in the Bitshares network

' litepresence 2018 '


def WTFPL_v0_March_1765():
    if any([stamps, licenses, taxation, regulation, fiat, etat]):
        try:
            print('no thank you')
        except:
            return [tar, feathers]

from random import random, shuffle, randint, choice
from multiprocessing import Process
from datetime import datetime
from statistics import mode
import traceback
import numpy
import time
import json
import sys
import os

DEV = False

try:
    import websocket
    if DEV:
        websocket.enableTrace(True)
except:
    raise ValueError('pip install websocket-client')


def version():

    global VERSION, version

    version = 'v0.00000013-JSON'
    VERSION = 'metaNODE ' + version + ' - Bitshares Trustless Client'

    sys.stdout.write(
        '\x1b]2;' +
        'Bitshares metaNODE' +  # terminal title bar
        '\x07')


def banner():
    print("\033c")
    if not DEV:
        print(
            '''

        Do this:

            metaNODE = Bitshares_Trustless_Client()
        ''')
        time.sleep(4)
        print("\033c")
        print(
            '''

        Get these curated Bitshares DEX feeds:

        ''')
        time.sleep(0.5)
        print("        metaNODE['last']      #" +
              " float; latest price \n")
        time.sleep(0.5)
        print("        metaNODE['bids']      #" +
              " list of (price,amount) tuples; [0][0]=highest bid price \n")
        time.sleep(0.5)
        print("        metaNODE['asks']      #" +
              " list of (price,amount) tuples; [0][0]=lowest ask price \n")
        time.sleep(0.5)
        print("        metaNODE['history']   #" +
              " list of (unix,price,amount) tuples; [0][0]=last trade time \n")
        time.sleep(0.5)
        print("        metaNODE['currency']  #" +
              " float; quantity of currency \n")
        time.sleep(0.5)
        print("        metaNODE['assets']    #" +
              " float; quantity of assets \n")
        print("        metaNODE['orders']    #" +
              " list of dicts of human readable orders \n")
        time.sleep(0.5)
        print("        metaNODE['whitelist'] #" +
              " list; [0]=most recently whitelisted node \n")
        time.sleep(0.5)
        print("        metaNODE['blacklist'] #" +
              " list; [0]=most recently blacklisted node \n")
        time.sleep(0.5)
        print("        metaNODE['blocktime'] #" +
              " oldest blockchain time in metaNODE data \n\n\n\n")
        time.sleep(1)
        print("to watch data feed, in second terminal type:")
        print('')
        print('>>> tail -f metaNODE.txt')
        print('')
        print("to watch error report, in third terminal type:")
        print('')
        print('>>> tail -f metaNODElog.txt')
        print('')
        time.sleep(2)

# GLOBALS
# ======================================================================


def controls():

    global WHITE, BLACK, TIMEOUT, PROCESSES, MAVENS
    global BOOK_DEPTH, HISTORY_DEPTH, PAUSE, BLIP, SKIP_INTRO

    # suggested values
    WHITE = 10  # 20
    BLACK = 10  # 30
    TIMEOUT = 300  # 300
    PROCESSES = 20  # 20
    MAVENS = 7  # 7
    BOOK_DEPTH = 10  # 10
    HISTORY_DEPTH = 50  # 50
    PAUSE = 4  # 4
    BLIP = 0.05  # 0.05
    SKIP_INTRO = False


def public_nodes():

    global nodes, node_count
    nodes = [
        'wss://api-ru.bts.blckchnd.com/wss',
        'wss://api.bitshares.bhuz.info/wss',
        'wss://api.bitsharesdex.com',
        'wss://api.bts.ai/wss',
        'wss://api.bts.blckchnd.com/ws',
        'wss://api.bts.mobi/ws',
        'wss://api.bts.network/wss',
        'wss://api.btsgo.net/wss',
        'wss://api.dex.trading/ws',
        'wss://api.fr.bitsharesdex.com',
        'wss://atlanta.bitshares.apasia.tech/wss',
        'wss://b.mrx.im/ws',
        'wss://bit.btsabc.org/ws',
        'wss://bitshares.cyberit.io/wss',
        'wss://bitshares.openledger.info/ws',
        'wss://blockzms.xyz/wss',
        'wss://bts-api.lafona.net/ws',
        'wss://bts-seoul.clockwork.gr/wss',
        'wss://bts.liuye.tech:4443',
        'wss://bts.open.icowallet.net/wss',
        'wss://bts.proxyhosts.info/wss',
        'wss://btsfullnode.bangzi.info/wss',
        'wss://btsws.roelandp.nl/wss',
        'wss://chicago.bitshares.apasia.tech/wss',
        'wss://crazybit.online/ws',
        'wss://dexnode.net/wss',
        'wss://england.bitshares.apasia.tech/ws',
        'wss://eu.nodes.bitshares.ws/ws',
        'wss://eu.openledger.info/wss',
        'wss://kc-us-dex.xeldal.com/wss',
        'wss://kimziv.com/ws',
        'wss://la.dexnode.net/ws',
        'wss://na.openledger.info/ws',
        'wss://netherlands.bitshares.apasia.tech/ws',
        'wss://new-york.bitshares.apasia.tech/wss',
        'wss://node.bitshares.eu/wss',
        'wss://node.market.rudex.org/wss',
        'wss://openledger.hk/wss',
        'wss://relinked.com/ws',
        'wss://seattle.bitshares.apasia.tech/wss',
        'wss://sg.nodes.bitshares.ws/ws',
        'wss://us-la.bitshares.apasia.tech/ws',
        'wss://us-ny.bitshares.apasia.tech/wss',
        'wss://us.nodes.bitshares.ws/wss',
        'wss://ws.gdex.io/wss',
        'wss://ws.gdex.top/ws',
        'wss://ws.hellobts.com/ws']

    nodes = race_read(doc='nodes.txt')

    node_count = len(nodes)


def constants():

    global Z, TZ, MAINNET, BEGIN

    TZ = time.altzone
    MAINNET = ('4018d7844c78f6a6c41c6a552b89802' +
               '2310fc5dec06da467ee7905a8dad512c8')
    Z = '{"id":1,"method":"call","params":["database",'
    BEGIN = int(time.time())


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

    now = int(time.time())
    race_write(doc='blacklist.txt', text=json.dumps([]))
    race_write(doc='whitelist.txt', text=json.dumps([]))
    race_write(doc='metaNODElog.txt', text=json.dumps(''))
    race_write(doc='metaNODE.txt', text=json.dumps({}))
    race_write(doc='mavens.txt', text=json.dumps([]))
    race_write(doc='watchdog.txt', text=json.dumps([now, now]))

# TEXT PIPE
# ======================================================================


def Bitshares_Trustless_Client():  # Your access to the metaNODE
    # Include this definition in your script to access metaNODE.txt
    # Deploy your bot script in the same folder as metaNODE.py
    i = 0
    while True:
        time.sleep(0.05 * i ** 2)
        i += 1
        try:
            with open('metaNODE.txt', 'r') as f:
                ret = f.read()  # .replace("'",'"')
                f.close()
                metaNODE = json.loads(ret)
                break
        except Exception as e:
            msg = str(type(e).__name__) + str(e.args)
            if DEV:
                msg += str(traceback.format_exc())
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
                    # ret = json.loads(ret)
                    ret = json.loads(ret)
                except:
                    try:
                        ret = ret.split(']')[0] + ']'
                        # ret = json.loads(ret)
                        ret = json.loads(ret)
                    except:
                        try:
                            ret = ret.split('}')[0] + '}'
                            # ret = ljson.loads(ret)
                            ret = json.loads(ret)
                        except:
                            print ('race_read() failed %s' % str(ret))
                            if '{' in ret:
                                ret = {}
                            else:
                                ret = []
                break
        except Exception as e:
            msg = str(type(e).__name__) + str(e.args)
            if DEV:
                msg += str(traceback.format_exc())
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
            msg = str(type(e).__name__) + str(e.args)
            if DEV:
                msg += str(traceback.format_exc())
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


def race_append(doc='', text=''):  # Concurrent Append to File Operation

    text = ('{"ctime":"' +
            str(time.ctime()) +
            '", "comment":' +
            str(text) +
            '}')
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
            msg = str(type(e).__name__) + str(e.args)
            if DEV:
                msg += str(traceback.format_exc())
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


def watchdog():

    identity = 1  # metaNODE:1, botscript:0
    max_latency = 600

    while True:
        try:
            try:
                with open('watchdog.txt', 'r') as f:
                    ret = f.read()
                    f.close()

                ret = json.loads(ret)
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
                    bell()
                    gmail()
                    msg += ' !!!!! WARNING: the other app is not responding !!!!!'
                return msg

            except Exception as e:
                msg = str(type(e).__name__) + str(e.args)
                if DEV:
                    msg += str(traceback.format_exc())
                print(msg)
                now = int(time.time())
                with open('watchdog.txt', 'w+') as f:
                    f.write(str([now, now]))
                    f.close()
                    break  # exit while loop
        except Exception as e:
            msg = str(type(e).__name__) + str(e.args)
            if DEV:
                msg += str(traceback.format_exc())
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

# CURATION
# ======================================================================


def history():

    # Tomorrow race_list():

    while True:
        metaNODE = Bitshares_Trustless_Client()
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
                        text=json.dumps(snapshot))
            time.sleep(3600)
        except Exception as e:
            msg = str(type(e).__name__) + str(e.args)
            if DEV:
                msg += str(traceback.format_exc())
            print(msg)
            race_append(doc='metaNODElog.txt', text=msg)
            time.sleep(2)


def inquire(call):  # single use public node database api call

    while True:
        try:
            black = race_read(doc='blacklist.txt')
            white = race_read(doc='whitelist.txt')
            # switch nodes
            shuffle(nodes)
            node = nodes[0]
            print(node)
            if node in black:
                raise ValueError('blacklisted')
            if node in white:
                raise ValueError('whitelisted')
            call = call.replace("'", '"')  # never use single quotes
            ws = websocket.create_connection(node, timeout=6)
            ws.send(call)
            ret = json.loads(ws.recv())['result']
            ws.close()
            winnow('whitelist', node)
            return ret
        except Exception as e:
            msg = str(type(e).__name__) + str(e.args) + node
            if DEV:
                msg += str(traceback.format_exc())
            print(msg)
            race_append(doc='metaNODElog.txt', text=msg)
            winnow('blacklist', node)
            pass


def cache():  # acquire asset id and asset amount decimal place

    # given account name, currency and asset symbols, lookup these globals
    global account_id, asset_id, currency_id
    global asset_precision, currency_precision

    lookup_accounts = Z + \
        '"lookup_accounts",["%s", "%s"]]}' % (account_name, 1)
    lookup_asset_symbols = Z + \
        '"lookup_asset_symbols",[["%s", "%s"]]]}' % (asset, currency)
    account_ids, asset_ids, currency_ids = [], [], []
    asset_precisions, currency_precisions = [], []

    def wwc():
        print("\033c")
        logo()
        print('')
        print(time.ctime())
        print('')
        print('Winnowing Websocket Connections...')
        print('==================================')
        print('')

    # trustless of multiple nodes
    for i in range(3):
        wwc()
        account_id = (inquire(lookup_accounts))[0][1]
        wwc()
        ret = inquire(lookup_asset_symbols)
        asset_id = ret[0]['id']
        asset_precision = ret[0]['precision']
        currency_id = ret[1]['id']
        currency_precision = ret[1]['precision']
        account_ids.append(account_id)
        asset_ids.append(asset_id)
        currency_ids.append(currency_id)
        asset_precisions.append(asset_precision)
        currency_precisions.append(currency_precision)
    account_id = mode(account_ids)
    asset_id = mode(asset_ids)
    currency_id = mode(currency_ids)
    asset_precision = mode(asset_precisions)
    currency_precision = mode(currency_precisions)
    websocket.enableTrace(False)
    print_market()


def spawn():  # multiprocessing handler

    # initialize background bifurcation process
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
    while True:
        b += 1
        race_write(doc='metaNODElog.txt', text='')
        for a in range(PROCESSES):
            c += 1
            time.sleep(TIMEOUT / 2 + TIMEOUT * random())
            try:
                multinode[str(a)].terminate()
            except Exception as e:
                msg = str(type(e).__name__) + str(e.args)
                if DEV:
                    msg += str(traceback.format_exc())
                print('terminate() WARNING', msg)
                race_append(doc='metaNODElog.txt', text=msg)
                pass
            try:
                multinode[str(a)] = Process(target=thresh, args=(a, b, c))
                multinode[str(a)].daemon = False
                multinode[str(a)].start()
            except Exception as e:
                msg = str(type(e).__name__) + str(e.args)
                if DEV:
                    msg += str(traceback.format_exc())
                print('process() WARNING', msg)
                race_append(doc='metaNODElog.txt', text=msg)
                pass


def thresh(process, epoch, pid):  # make calls, shake out errors

    # DATABASE CALLS

    def dex_handshake(node):
        start = time.time()
        ws = websocket.create_connection(node, timeout=4)
        handshake_latency = time.time() - start
        if 0 > handshake_latency > 4:
            raise ValueError('handshake_latency', handshake_latency)
        return handshake_latency, ws

    def dex_ping_latency(ws):
        get_chain_id = Z + '"get_chain_id",[]]}'
        start = time.time()
        ws.send(get_chain_id)
        chain_id = json.loads(ws.recv())['result']
        ping_latency = time.time() - start
        if chain_id != MAINNET:
            raise ValueError('chain_id != MAINNET')
        if 0 > ping_latency > 1:
            raise ValueError('ping_latency', ping_latency)
        return ping_latency

    def dex_block_latency(ws):
        get_dynamic_global_properties = Z + \
            '"get_dynamic_global_properties",[]]}'
        ws.send(get_dynamic_global_properties)
        dynamic_global_properties = json.loads(ws.recv())['result']
        blocktime = from_iso_date(dynamic_global_properties['time'])
        block_latency = TZ + time.time() - blocktime
        if 0 > block_latency > 6:
            raise ValueError('blocktime is stale', block_latency)
        return float(block_latency), int(blocktime)

    def dex_last(ws, currency, asset):
        get_ticker = Z + \
            '"get_ticker",["%s","%s","%s"]]}' % (
                currency, asset, False)
        ws.send(get_ticker)
        ticker = json.loads(ws.recv())['result']
        last = precision(ticker['latest'], 16)
        if float(last) == 0:
            raise ValueError('zero price last')
        return last

    def dex_market_history(ws, currency, asset, now, then, depth=100):
        get_trade_history = Z + \
            '"get_trade_history",["%s","%s","%s","%s","%s"]]}' % (
                currency, asset, now, then, depth)
        ws.send(get_trade_history)
        trade_history = json.loads(ws.recv())['result']
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

    def dex_account_balances(ws, account_name,
                             asset_ids=[],
                             asset_precisions=[]):

        if '1.3.0' not in asset_ids:
            asset_ids.append('1.3.0')
            asset_precisions.append(5)

        get_balances = Z + (
            '"get_named_account_balances",["%s", [' %
            account_name)
        for i in range(len(asset_ids)):
            get_balances += ('"' + asset_ids[i] + '",')
        get_balances += ']]]}'
        ws.send(get_balances)
        ret = json.loads(ws.recv())['result']
        balances = {}
        for j in range(len(asset_ids)):
            balances[asset_ids[j]] = 0
        for j in range(len(asset_ids)):
            for k in range(len(ret)):
                if ret[k]['asset_id'] == asset_ids[j]:
                    balances[asset_ids[j]] += float(
                        ret[k]['amount']) / 10 ** asset_precisions[j]
        return balances

    def dex_open_orders(ws, asset, asset_id, asset_precision,
                        currency, currency_id, currency_precision):
        get_full_accounts = Z + \
            '"get_full_accounts",[["%s",],%s]]}' % (
                account_name, 'false')
        # a databnase call to the api returns price as fraction
        # with unreferenced decimal point locations on both amounts
        # they're also reference by A.B.C instead of ticker symbol
        time.sleep(BLIP)
        ws.send(get_full_accounts)
        ret = ws.recv()
        BitPAIR = asset + ":" + currency
        print (BitPAIR)
        try:
            limit_orders = json.loads(ret)['result'][0][1]['limit_orders']
        except:
            limit_orders = []
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

    def dex_book(ws, currency, asset, depth=3):
        get_order_book = Z + \
            '"get_order_book",["%s","%s","%s"]]}' % (
                currency, asset, depth)
        time.sleep(BLIP)
        ws.send(get_order_book)
        order_book = json.loads(ws.recv())['result']
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

    # THRESHING EVENT LOOP

    while True:
        try:
            ws = 0
            time.sleep(random())
            # CHECK BLACK AND WHITE LISTS
            black = race_read(doc='blacklist.txt')
            white = race_read(doc='whitelist.txt')
            shuffle(nodes)
            node = nodes[0]
            if node in black:
                raise ValueError('blacklisted')
            if node in white:
                raise ValueError('whitelisted')

            # connect to websocket
            handshake_latency, ws = dex_handshake(node)
            # use node a dozen times
            for i in range(12):
                time.sleep(PAUSE)
                # Database calls
                ping_latency = dex_ping_latency(ws)
                block_latency, blocktime = dex_block_latency(ws)
                last = float(dex_last(ws, currency, asset))
                now = to_iso_date(time.time())
                then = to_iso_date(time.time() - 3 * 86400)
                history = dex_market_history(ws, currency, asset, now, then)
                askp, bidp, askv, bidv = dex_book(
                    ws, currency, asset, depth=30)
                balances = dex_account_balances(ws, account_name,
                                                asset_ids=[
                                                asset_id,
                                                currency_id],
                                                asset_precisions=[asset_precision, currency_precision])
                bts_balance = float(balances['1.3.0'])
                asset_balance = float(balances[asset_id])
                currency_balance = float(balances[currency_id])
                orders = dex_open_orders(ws, asset, asset_id, asset_precision,
                                         currency, currency_id, currency_precision)

                try:
                    import psutil  # REQUIRES MODULE INSTALL
                    proc = psutil.Process()
                    descriptors = proc.num_fds()
                    cpu = '%.3f' % (
                        float(os.popen('''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline()))
                    ram = '%.3f' % (100 * float(proc.memory_percent()))
                    io = list(proc.io_counters())[:2]
                except Exception as e:
                    msg = str(type(e).__name__) + str(e.args)
                    if DEV:
                        msg += str(traceback.format_exc())
                    print(msg)

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
                keys = ['bifurcating the metaNODE....']

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
                except:
                    pass

                runtime = int(time.time()) - BEGIN

                if (len(white) < WHITE) or (len(black) < BLACK):
                    alert = ' * building lists *'
                else:
                    alert = ''

                # in the event data passes all tests, then:
                # print, winnow the node, and nascent trend the maven
                print_market()
                print(keys)
                print('')
                print('runtime:epoch:pid', runtime, epoch, pid)
                print('fds:processes    ',
                      descriptors,
                      process,
                      'of',
                      PROCESSES)
                try:
                    print('cpu:ram:io       ', cpu, ram, io)
                except:
                    pass
                print('node             ', node)
                print(
                    'total:white:black',
                    node_count,
                    len(white),
                    len(black),
                    alert)
                print('')
                print('block latency    ', ('%.3f' % block_latency))
                print('handshake        ', ('%.3f' % handshake_latency))
                print('ping             ', ('%.3f' % ping_latency))

                print('                 ', [x.rjust(16, ' ')
                      for x in ['name', 'balance', 'orders', 'holding',
                                'max', 'percent']])
                print(
                    'currency         ',
                    [str(x).rjust(16,
                     ' ') for x in [currency,
                     currency_balance,
                     buy_orders,
                     currency_holding,
                     currency_max,
                     divested]])
                print(
                    'assets           ',
                    [str(x).rjust(16,
                     ' ') for x in [asset,
                     asset_balance,
                     sell_orders,
                     asset_holding,
                     asset_max,
                     invested]])
                print('bitshares        ', bts_balance, 'BTS')
                print('')
                print(
                    'history      ',
                    ('%.16f' % last),
                    'LAST with depth',
                    len(history))
                for i in range(3):
                    print(history[i])
                print('')
                print('asks depth       ', len(askp))
                for i in range(3):
                    print(askp[i], askv[i])
                print('bids depth       ', len(bidp))
                for i in range(3):
                    print(bidp[i], bidv[i])
                print('')
                print('open orders      ', len(orders))
                for order in orders:
                    print(order)
                print('')
                print('watchdog latency:', watchdog_latency)
                print('')

                # send the maven dictionary to nascent_trend()
                # Must be JSON type
                # 'STRING', 'INT', 'FLOAT', '{DICT}', or '[LIST]'
                maven = {}
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

                # winnow whitelist this node
                winnow('whitelist', node)

            try:
                time.sleep(BLIP)
                ws.close()
            except Exception as e:
                msg = str(type(e).__name__) + str(e.args)
                if DEV:
                    msg += str(traceback.format_exc())
                print(msg)
                pass
            continue

        except Exception as e:
            try:
                time.sleep(BLIP)
                ws.close()
            except:
                pass
            msg = str(type(e).__name__) + str(e.args) + node
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

            print(msg)
            if 'listed' not in msg:
                race_append(doc='metaNODElog.txt', text=msg)
            winnow('blacklist', node)
            continue

    call = call.replace("'", '"')  # never use single quotes


def winnow(x, node):  # seperate good nodes from bad

    if x == 'blacklist':
        black = race_read(doc='blacklist.txt')
        if isinstance(black, list):
            if node in black:
                black.remove(node)
            black.append(node)
            black = black[-BLACK:]
            race_write(doc='blacklist.txt', text=black)
        else:
            race_write(doc='blacklist.txt', text=[node])

    if x == 'whitelist':
        white = race_read(doc='whitelist.txt')
        if isinstance(white, list):
            if node in white:
                white.remove(node)
            white.append(node)
            white = white[-WHITE:]
            race_write(doc='whitelist.txt', text=white)
        else:
            race_write(doc='whitelist.txt', text=[node])


def nascent_trend(maven):  # append latest data

    mavens = race_read(doc='mavens.txt')
    if isinstance(mavens, list):
        mavens.append(maven)
        mavens = mavens[-MAVENS:]
        race_write(doc='mavens.txt', text=json.dumps(mavens))
    else:
        race_write(doc='mavens.txt', text=json.dumps([maven]))


def bifurcation():  # statistically curate data

    while True:
        try:

            # initialize / clear the metaNODE dictionary
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

            time.sleep(1)  # take a deep breath

            # gather list of maven opinions from the nascent_trend()
            mavens = race_read(doc='mavens.txt')

            # sort maven data for statistical analysis by key
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

                # stringify lists for statistical mode
                bidp.append(str(maven['bidp']))
                askp.append(str(maven['askp']))
                bidv.append(str(maven['bidv']))
                askv.append(str(maven['askv']))
                history.append(str(maven['market_history']))
                orders.append(str(maven['orders']))

            # find the youngest bitshares blocktime in our dataset
            try:
                blocktime = max(blocktime)
            except:
                raise ValueError('validating the nascent trend...')
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

            from ast import literal_eval as literal

            # race_append(doc='metaNODElog.txt', text=bidp)

            bidp = json.loads(str(bidp).replace("'", '"'))
            askp = json.loads(str(askp).replace("'", '"'))
            bidv = json.loads(str(bidv).replace("'", '"'))
            askv = json.loads(str(askv).replace("'", '"'))
            history = json.loads(str(history).replace("'", '"'))
            orders = json.loads(str(orders).replace("'", '"'))

            # attempt a full whitelist and blacklist
            wl = []
            for i in whitelist:
                wl += i
            whitelist = list(set(wl))[-WHITE:]
            bl = []
            for i in blacklist:
                bl += i
            blacklist = list(set(bl))[-BLACK:]

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
            metaNODE = json.dumps(metaNODE)
            race_write(doc='metaNODE.txt', text=metaNODE)
            print ('metaNODE.txt updated')

        except Exception as e:  # wait a second and try again
            # common msg is "no mode statistics error"
            msg = str(type(e).__name__) + str(e.args)
            if DEV:
                msg += str(traceback.format_exc())
            print(msg)
            race_append(doc='metaNODElog.txt', text=msg)
            continue  # from top of while loop NOT pass through error


# ALERT FUNCTIONS
# ======================================================================

def bell(duration=2, frequency=432):  # Activate linux audible bell

    pass
    '''
    os.system('play --no-show-progress --null --channels 1 synth' +
                  ' %s sine %f' % (duration*1000, frequency))
    '''


def gmail():  # Send Mail to a Gmail Account

    # sorry no subject lines with this API
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

# HELPER FUNCTIONS
# ======================================================================


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
    print(time.ctime())
    print('=======================================')
    print('account   ', account_name, account_id)
    print('currency  ', currency, currency_id, currency_precision)
    print('asset     ', asset, asset_id, asset_precision)
    print('=======================================')
    print('')


def welcome():

    version()
    print("\033c")
    race_write(doc='metaNODElog.txt', text=str(time.ctime()))
    logo()
    if not SKIP_INTRO:
        banner()
        time.sleep(3)
        for i in range(5):
            print("\033c")
            logo()
            time.sleep(0.5)


def logo():

    COLOR = True

    def blue(text):
        return ('\033[94m' + text + '\033[0m') if COLOR else text

    def cyan(text):
        return ('\033[96m' + text + '\033[0m') if COLOR else text

    def red(text):
        return ('\033[91m' + text + '\033[0m') if COLOR else text

    def purple(text):
        return ('\033[95m' + text + '\033[0m') if COLOR else text

    def wxyz():
        a = 'abcdef1234567890'
        b = ''
        for i in range(17):
            b = str(b + r'\x' + choice(a) + choice(a))

        return b
    w, x, y, z = wxyz(), wxyz(), wxyz(), wxyz()

    print(blue(w))
    print(blue(x))
    print(cyan(
          '''                             ____  _____   ___   ______   ________
Bitshares Trustless Client  (_   \(_   _).'   `.(_   _ `.(_   __  \
  __  __  ____  ____   __     |   \ | | /  .-.  \ | | `. \ | |_ \_|
 (  \/  )( ___)(_  _) /  \    | |\ \| | | |   | | | |  | | |  _) _
  )    ( | __)   ||  / <> \  _| |_\   |_\  `-'  /_| |_.' /_| |__/ |
 (_/\/\_)(____) (__)(__)(__)(_____|\____)`.___.'(______.'(________/
                                                        ''' + version))
    print(blue(y))
    print(blue(z))
    if DEV:
        print(
            red('DEV DEV DEV DEV DEV DEV DEV DEV DEV DEV DEV DEV DEV DEV DEV DEV DEV'))


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
