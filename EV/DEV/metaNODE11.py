' litepresence 2018 '

def WTFPL_v0_March_1765():
    if any([stamps, licenses, taxation, regulation, fiat, etat]):
        try:
            print('no thank you')
        except:
            return [tar, feathers]


from random import random, shuffle, randint, choice
from ast import literal_eval as literal
from multiprocessing import Process
from datetime import datetime
from statistics import mode
import traceback
import numpy
import time
import json
import sys
import os

try:
    import websocket
    websocket.enableTrace(True)
except:
    raise ValueError('pip install websocket-client')


def banner():
    print("\033c")
    if 1:
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
    global BOOK_DEPTH, HISTORY_DEPTH, PAUSE, BLIP

                            #As Tested
    WHITE           = 20    #20
    BLACK           = 30    #30
    TIMEOUT         = 300   #300
    PROCESSES       = 20    #20
    MAVENS          = 7     #7
    BOOK_DEPTH      = 10    #10
    HISTORY_DEPTH   = 50    #50
    PAUSE           = 4     #2
    BLIP            = 0.05  #0.05

def public_nodes():

    global nodes, node_count
    nodes = ['wss://ap-northeast-1.bts.crypto-bridge.org/wss',
             'wss://ap-northeast-2.bts.crypto-bridge.org/wss',
             'wss://ap-southeast-1.bts.crypto-bridge.org/wss',
             'wss://ap-southeast-2.bts.crypto-bridge.org/wss',
             'wss://api-ru.bts.blckchnd.com/wss',
             'wss://api.bitshares.bhuz.info/ws',
             'wss://api.bitsharesdex.com',
             'wss://api.bts.ai/',
             'wss://api.bts.blckchnd.com/wss',
             'wss://api.bts.mobi/wss',
             'wss://api.bts.network',
             'wss://api.btsgo.net/ws',
             'wss://api.btsxchng.com',
             'wss://atlanta.bitshares.apasia.tech/ws',
             'wss://australia.bitshares.apasia.tech/ws',
             'wss://b.mrx.im/wss',
             'wss://bit.btsabc.org/ws',
             'wss://bitshares-api.wancloud.io/ws',
             'wss://bitshares.apasia.tech/ws',
             'wss://bitshares.bts123.cc:15138/',
             'wss://bitshares.crypto.fans/ws',
             'wss://bitshares.cyberit.io/',
             'wss://bitshares.dacplay.org/wss',
             'wss://bitshares.dacplay.org:8089/wss',
             'wss://bitshares.neocrypto.io/wss',
             'wss://bitshares.nu/ws',
             'wss://bitshares.openledger.info/ws',
             'wss://blockzms.xyz/ws',
             'wss://bts-api.lafona.net/ws',
             'wss://bts-seoul.clockwork.gr',
             'wss://bts.ai.la/wss',
             'wss://bts.proxyhosts.info/wss',
             'wss://bts.open.icowallet.net/ws',
             'wss://bts.to0l.cn:4443/ws',
             'wss://bts.transwiser.com/wss',
             'wss://btsws.roelandp.nl/ws',
             'wss://btsza.co.za:8091/ws',
             'wss://canada6.daostreet.com/ws',
             'wss://capetown.bitshares.africa/ws',
             'wss://chicago.bitshares.apasia.tech/ws',
             'wss://crazybit.online',
             'wss://croatia.bitshares.apasia.tech/ws',
             'wss://dallas.bitshares.apasia.tech/ws',
             'wss://dele-puppy.com/wss',
             'wss://dex.rnglab.org/wss',
             'wss://dexnode.net/wss',
             'wss://england.bitshares.apasia.tech/ws',
             'wss://eu-central-1.bts.crypto-bridge.org/wss',
             'wss://eu-west-1.bts.crypto-bridge.org/wss',
             'wss://eu.nodes.bitshares.ws/wss',
             'wss://eu.openledger.info/ws',
             'wss://france.bitshares.apasia.tech/ws',
             'wss://frankfurt8.daostreet.com/ws',
             'wss://freedom.bts123.cc:15138/',
             'wss://japan.bitshares.apasia.tech/ws',
             'wss://kc-us-dex.xeldal.com/wss',
             'wss://kimziv.com/ws',
             'wss://la.dexnode.net/wss',
             'wss://miami.bitshares.apasia.tech/ws',
             'wss://ncali5.daostreet.com/ws',
             'wss://new-york.bitshares.apasia.tech/ws',
             'wss://node.bitshares.eu/wss',
             'wss://node.btscharts.com/ws',
             'wss://node.market.rudex.org/wss',
             'wss://nohistory.proxyhosts.info/wss',
             'wss://ohio4.daostreet.com/ws',
             'wss://openledger.hk/ws',
             'wss://oregon2.daostreet.com/ws',
             'wss://paris7.daostreet.com/ws',
             'wss://relinked.com/ws',
             'wss://sa-east-1.bts.crypto-bridge.org/wss',
             'wss://scali10.daostreet.com/ws',
             'wss://seattle.bitshares.apasia.tech/ws',
             'wss://seoul9.daostreet.com/ws',
             'wss://sg.nodes.bitshares.ws/wss',
             'wss://singapore.bitshares.apasia.tech/ws',
             'wss://slovenia.bitshares.apasia.tech/wss',
             'wss://this.uptick.rocks/ws',
             'wss://us-east-1.bts.crypto-bridge.org/wss',
             'wss://us-la.bitshares.apasia.tech/ws',
             'wss://us-ny.bitshares.apasia.tech/wss',
             'wss://us-west-1.bts.crypto-bridge.org/wss',
             'wss://us.nodes.bitshares.ws/wss',
             'wss://valen-tin.fr:8090/wss',
             'wss://valley.bitshares.apasia.tech/ws',
             'wss://virginia3.daostreet.com/ws',
             'wss://ws.gdex.io',
             'wss://ws.gdex.top/wss',
             'wss://ws.hellobts.com/',
             'wss://ws.winex.pro/wss',
             'wss://za.bitshares.africa/ws', ]
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
    asset    = input('       asset: ').strip('"').strip("'").upper()
    print('')

    if account_name == '':
        account_name = 'abc123'
    if currency == '':
        currency = 'GDEX.BTC'
    if asset == '':
        asset = 'BTS'

def initialize():

    now = int(time.time())
    race_write(doc='blacklist.txt', text=[])
    race_write(doc='whitelist.txt', text=[])
    race_write(doc='metaNODElog.txt', text='')
    race_write(doc='metaNODE.txt', text={})
    race_write(doc='mavens.txt', text=[])
    race_write(doc='watchdog.txt', text=[now, now])


# TEXT PIPE
# ======================================================================

def Bitshares_Trustless_Client(): # Your access to the metaNODE

    # Include this definition in your script to access metaNODE.txt
    # Deploy your bot script in the same folder as metaNODE.py

    'from ast import literal_eval as literal'
    i = 0
    while True:
        time.sleep(0.05 * i ** 2)
        i += 1
        try:
            with open('metaNODE.txt', 'r') as f:
                ret = f.read()
                f.close()
                metaNODE = literal(ret)
                break
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
    return metaNODE

def race_read(doc=''):  # Concurrent Read from File Operation

    i = 0
    while True:
        time.sleep(BLIP * i ** 2)
        i += 1
        try:
            with open(doc, 'r') as f:
                ret = f.read()
                f.close()
                try:
                    ret = literal(ret)
                except:
                    try:
                        ret = ret.split(']')[0] + ']'
                        ret = literal(ret)
                    except:
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

    text = '\n' + str(time.ctime()) + ' ' + str(text) + '\n'
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

    identity = 1 # metaNODE:1, botscript:0
    max_latency = 600

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

# CURATION
# ======================================================================

def inquire(call): # single use public node database api call

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
            print(msg)
            race_append(doc='metaNODElog.txt', text=msg)
            winnow('blacklist', node)
            pass

def cache(): # acquire asset id and asset amount decimal place

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
                print('terminate() WARNING', msg)
                race_append(doc='metaNODElog.txt', text=msg)
                pass
            try:
                multinode[str(a)] = Process(target=thresh, args=(a, b, c))
                multinode[str(a)].daemon = False
                multinode[str(a)].start()
            except Exception as e:
                msg = str(type(e).__name__) + str(e.args)
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
        return block_latency, blocktime

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
            unix = from_iso_date(trade_history[i]['date'])
            price = precision(trade_history[i]['price'], 16)
            if float(price) == 0:
                raise ValueError('zero price in history')
            amount = precision(
                trade_history[i]['amount'], asset_precision)
            history.append((unix, price, amount))
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
                        ret[k]['amount'])/10**asset_precisions[j]
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
                base_amount /= 10**base_precision
                quote_amount /= 10**quote_precision
                if base_id == asset_id:
                    orderType = 'sell'
                    price = quote_amount / base_amount
                    amount = (amount/10**base_precision)
                else:
                    orderType = 'buy'
                    price = base_amount / quote_amount
                    amount = (amount/10**base_precision)/price
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
                last = dex_last(ws, currency, asset)
                now = to_iso_date(time.time())
                then = to_iso_date(time.time() - 3 * 86400)
                history = dex_market_history(ws, currency, asset, now, then)
                askp, bidp, askv, bidv = dex_book(ws, currency, asset, depth=3)
                balances = dex_account_balances(ws, account_name,
                        asset_ids=[asset_id, currency_id],
                        asset_precisions=[asset_precision, currency_precision])
                bts_balance = balances['1.3.0']
                asset_balance = balances[asset_id]
                currency_balance = balances[currency_id]
                orders = dex_open_orders(ws, asset, asset_id, asset_precision,
                                            currency, currency_id, currency_precision)

                try:
                    import psutil # REQUIRES MODULE INSTALL
                    proc = psutil.Process()
                    descriptors = proc.num_fds()
                    cpu = '%.3f' % (float(os.popen('''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline()))
                    ram = '%.3f' % (100*float(proc.memory_percent()))
                    io = list(proc.io_counters())[:2]
                except Exception as e: 
                    msg = str(type(e).__name__) + str(e.args)
                    print(msg)

                watchdog_latency = watchdog()

                runtime = int(time.time()) - BEGIN

                # in the event data passes all tests, then:
                # print, winnow the node, and nascent trend the maven
                print_market()
                if (len(white) < WHITE) or (len(black) < BLACK):
                    alert = ' * building lists *'
                else:
                    alert = ''
                print('runtime          ', runtime)
                print('epoch            ', epoch, 'pid', pid)
                print('fds, processes   ', descriptors, process, 'of', PROCESSES)
                try:
                    print('cpu ram          ', cpu , ram)
                except:
                    pass
                try:
                    print('read write       ', io)
                except:
                    pass
                print('node             ', node)
                print('total:white:black', node_count, len(white), len(black), alert)
                print('')
                print('block latency    ', ('%.3f' % block_latency))
                print('handshake        ', ('%.3f' % handshake_latency))
                print('ping             ', ('%.3f' % ping_latency))
                print('')
                print('bitshares        ', bts_balance, 'BTS')
                print('currency         ', currency_balance, currency)
                print('assets           ', asset_balance, asset)
                print('')
                print('last             ', ('%.16f' % float(last)))
                print('')
                print('history depth    ', len(history))
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

                # winnow whitelist the node and nascent trend the maven
                maven = {}
                maven['bidv'] = bidv
                maven['askv'] = askv
                maven['bidp'] = bidp
                maven['askp'] = askp
                maven['bts_balance'] = bts_balance
                maven['currency_balance'] = currency_balance
                maven['asset_balance'] = asset_balance
                maven['market_history'] = history
                maven['orders'] = orders
                maven['last'] = last
                maven['whitelist'] = white
                maven['blacklist'] = black
                maven['blocktime'] = blocktime
                nascent_trend(maven)
                winnow('whitelist', node)

            try:
                time.sleep(BLIP)
                ws.close()
            except Exception as e:
                msg = str(type(e).__name__) + str(e.args)
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
                ('ConnectionRefusedError' not in msg)) :
                    msg += '\n'+ str(traceback.format_exc())

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
        mavens.append(str(maven))
        mavens = mavens[-MAVENS:]
        race_write(doc='mavens.txt', text=mavens)
    else:
        race_write(doc='mavens.txt', text=[str(maven)])

def bifurcation():  # statistically curate data

    while True:
        try:
            time.sleep(1)

            mavens = race_read(doc='mavens.txt')

            l = len(mavens)

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
            # initialize the metaNODE dictionary
            metaNODE = {}

            # sort maven data for statistical analysis by key
            for i in range(len(mavens)):
                maven = literal(mavens[i])
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

            # find the oldest bitshares blocktime in our dataset
            blocktime = min(blocktime)
            # get the mode of the mavens for each metric
            # allow 1 or 2 less than total & most recent for mode
            # accept "no mode" statistics error as possibility
            try:
                bts_balance = mode(bts_balance)
            except:
                try:
                    bts_balance = mode(bts_balance[-(l-1):])
                except:
                    bts_balance = mode(bts_balance[-(l-2):])
            try:
                currency_balance = mode(currency_balance)
            except:
                try:
                    currency_balance = mode(currency_balance[-(l-1):])
                except:
                    currency_balance = mode(currency_balance[-(l-2):])
            try:
                asset_balance = mode(asset_balance)
            except:
                try:
                    asset_balance = mode(asset_balance[-(l-1):])
                except:
                    asset_balance = mode(asset_balance[-(l-2):])
            try:
                last = mode(last)
            except:
                try:
                    last = mode(last[-(l-1):])
                except:
                    last = mode(last[-(l-2):])
            try:
                bidp = literal(mode(bidp))
            except:
                try:
                    bidp = literal(mode(bidp[-(l-1):]))
                except:
                    bidp = literal(mode(bidp[-(l-2):]))
            try:
                askp = literal(mode(askp))
            except:
                try:
                    askp = literal(mode(askp[-(l-1):]))
                except:
                    askp = literal(mode(askp[-(l-2):]))
            try:
                bidv = literal(mode(bidv))
            except:
                try:
                    bidv = literal(mode(bidv[-(l-1):]))
                except:
                    bidv = literal(mode(bidv[-(l-2):]))
            try:
                askv = literal(mode(askv))
            except:
                try:
                    askv = literal(mode(askv[-(l-1):]))
                except:
                    askv = literal(mode(askv[-(l-2):]))

            try:
                history = literal(mode(history))
            except:
                try:
                    history = literal(mode(history[-(l-1):]))
                except:
                    history = literal(mode(history[-(l-2):]))

            try:
                orders = literal(mode(orders))
            except:
                try:
                    orders = literal(mode(orders[-(l-1):]))
                except:
                    orders = literal(mode(orders[-(l-2):]))

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
            book = {'bidp':bidp, 'bidv':bidv, 'askp':askp, 'askv':askv}

            # if you made it this far without statistics error
            # truncate and rewrite the metaNODE with curated data
            metaNODE['book'] = book
            metaNODE['bts_balance'] = float(bts_balance)
            metaNODE['currency_balance'] = float(currency_balance)
            metaNODE['asset_balance'] = float(asset_balance)
            metaNODE['history'] = history #LIST
            metaNODE['orders'] = orders #LIST
            metaNODE['last'] = float(last)
            metaNODE['whitelist'] = whitelist #LIST
            metaNODE['blacklist'] = blacklist #LIST
            metaNODE['blocktime'] = float(blocktime)
            metaNODE['account_name'] = account_name #STRING
            metaNODE['account_id'] = account_id #STRING A.B.C
            metaNODE['asset'] = asset  #STRING SYMBOL
            metaNODE['asset_id'] = asset_id #STRING A.B.C
            metaNODE['asset_precision'] = int(asset_precision)
            metaNODE['currency'] = currency #STRING SYMBOL
            metaNODE['currency_id'] = currency_id #STRING A.B.C
            metaNODE['currency_precision'] = int(currency_precision)

            # solitary process with write access to metaNODE.txt            
            race_write(doc='metaNODE.txt', text=metaNODE)
            print ('metaNODE.txt updated')
        
        except Exception as e: # wait a second and try again
            # common msg is "no mode statistics error"
            msg = str(type(e).__name__) + str(e.args)
            print(msg)
            race_append(doc='metaNODElog.txt', text=msg)
            continue # from top of while loop NOT pass through error

# HELPER FUNCTIONS
# ======================================================================
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
    logo()
    banner()
    time.sleep(3)
    for i in range(5):
        print("\033c")
        logo()
        time.sleep(0.5)
    
def logo():

    def wxyz():
        a = 'abcdef1234567890'
        b = ''
        for i in range(17):
            b = str(b + r'\x' + choice(a) + choice(a))
        return b
    w,x,y,z = wxyz(),wxyz(),wxyz(),wxyz()
    print(w)
    print(x)
    print(
'''                             ____  _____   ___   ______   ________
Bitshares Trustless Client  (_   \(_   _).'   `.(_   _ `.(_   __  \   
  __  __  ____  ____   __     |   \ | | /  .-.  \ | | `. \ | |_ \_|   
 (  \/  )( ___)(_  _) /  \    | |\ \| | | |   | | | |  | | |  _) _
  )    ( | __)   ||  / <> \  _| |_\   |_\  `-'  /_| |_.' /_| |__/ |
 (_/\/\_)(____) (__)(__)(__)(_____|\____)`.___.'(______.'(________/
                                                        ''' + version)
    print(y)
    print(z)

def version():

    global VERSION, version

    version = 'v0.00000011'
    VERSION = 'metaNODE ' + version + ' - Bitshares Trustless Client'

    sys.stdout.write('\x1b]2;' + VERSION + '\x07')  # terminal #title

def main(): # script primary backbone

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
