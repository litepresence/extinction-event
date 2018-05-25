# I/O intensive; Solid State Drive (SSD) recommended

' (BTS) litepresence1 '

# pip install websocket-client
import websocket
websocket.enableTrace(True)

from random import random, shuffle, randint, choice
from ast import literal_eval as literal
from multiprocessing import Process
from threading import Thread
import numpy
from datetime import datetime
from statistics import mode
import time
import json
import sys

# GLOBALS
#
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
    PAUSE           = 2     #2
    BLIP            = 0.05  #0.05

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

def Bitshares_Trustless_Client():

    # Include this definition in your script to access metaNODE.txt
    # Deploy your bot script in the same folder as metaNODE.py

    from ast import literal_eval as literal
    i = 0
    while True:
        time.sleep(BLIP * i ** 2)
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

def version():

    global VERSION, version

    version = 'v0.00000008'
    VERSION = 'metaNODE ' + version + ' - Bitshares Trustless Client'

    sys.stdout.write('\x1b]2;' + VERSION + '\x07')  # terminal #title

def public_nodes():

    global nodes
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

def constants():

    global Z, TZ, MAINNET, BEGIN

    TZ = time.altzone
    MAINNET = ('4018d7844c78f6a6c41c6a552b89802' +
               '2310fc5dec06da467ee7905a8dad512c8')
    Z = '{"id":1,"method":"call","params":["database",'
    BEGIN = int(time.time())

def sign_in():

    global account_name, currency, asset

    print('')
    print('Input Account and Market, or press Enter for demo')
    print('')

    account_name = input('account name:')
    if account_name == '':
        account_name = 'abc123'
        currency = 'OPEN.BTC'
        asset = 'BTS'
    else:
        currency = input('currency:')
        asset = input('asset:')

def initialize():

    race_write(doc='blacklist.txt', text=[])
    race_write(doc='whitelist.txt', text=[])
    race_write(doc='metaNODElog.txt', text='')
    race_write(doc='metaNODE.txt', text={})
    race_write(doc='mavens.txt', text=[])

# TEXT PIPE
# ======================================================================

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

def inquire(call):

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
            ws = websocket.create_connection(node, timeout=4)
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

def cache():

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

    # trustless of 5 nodes
    for i in range(5):
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

def spawn():  # multiprocessing watchdog

    # initialize background bifurcation process
    b_process = Process(target=bifurcation)
    b_process.daemon = False
    b_process.start()

    # initialize  multiple threshing processes
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
            

def thresh(process, epoch, pid):  # shake out value errors

    while True:
        try:
            ws = 0
            time.sleep(random())
            # REQUEST ARGUMENTS
            coins = [currency_id, asset_id]
            now = to_iso_date(time.time())
            then = to_iso_date(time.time() - 3 * 86400)
            get_chain_id = Z + '"get_chain_id",[]]}'
            get_dynamic_global_properties = Z + \
                '"get_dynamic_global_properties",[]]}'
            get_ticker = Z + \
                '"get_ticker",["%s","%s","%s"]]}' % (
                    currency, asset, False)
            get_trade_history = Z + \
                '"get_trade_history",["%s","%s","%s","%s","%s"]]}' % (
                    currency, asset, now, then, HISTORY_DEPTH)
            get_named_account_balances = Z + \
                '"get_named_account_balances",["%s", ["%s","%s"]]]}' % (
                    account_name, currency_id, asset_id)
            get_order_book = Z + \
                '"get_order_book",["%s","%s","%s"]]}' % (
                    currency, asset, BOOK_DEPTH)

            # CHECK BLACK AND WHITE LISTS
            black = race_read(doc='blacklist.txt')
            white = race_read(doc='whitelist.txt')
            shuffle(nodes)
            node = nodes[0]
            if node in black:
                raise ValueError('blacklisted')
            if node in white:
                raise ValueError('whitelisted')

            # WEBSOCKET HANDSHAKE
            handshake_time = time.time()
            ws = websocket.create_connection(node, timeout=4)
            handshake_elapsed = time.time() - handshake_time
            if handshake_elapsed > 4:
                raise ValueError('handshake_elapsed', handshake_elapsed)

            for i in range(randint(8, 12)):
                time.sleep(PAUSE)
                # CHAIN ID
                start = time.time()
                ws.send(get_chain_id)
                chain_id = json.loads(ws.recv())['result']
                ping_elapsed = time.time() - start
                if chain_id != MAINNET:
                    raise ValueError('chain_id != MAINNET')
                if ping_elapsed > 1:
                    raise ValueError('ping_elapsed', ping_elapsed)
                # BLOCKTIME
                time.sleep(BLIP)
                ws.send(get_dynamic_global_properties)
                dynamic_global_properties = json.loads(ws.recv())['result']
                block_time = from_iso_date(dynamic_global_properties['time'])
                block_latency = TZ + time.time() - block_time
                if block_latency > 6:
                    raise ValueError('blocktime is stale', block_latency)
                # LAST
                time.sleep(BLIP)
                ws.send(get_ticker)
                ticker = json.loads(ws.recv())['result']
                last = precision(ticker['latest'], 16)
                if float(last) == 0:
                    raise ValueError('zero price last')
                # MARKET HISTORY
                time.sleep(BLIP)
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
                # ACCOUNT BALANCES
                time.sleep(BLIP)
                ws.send(get_named_account_balances)
                named_account_balances = json.loads(ws.recv())['result']
                currency_balance = 0
                asset_balance = 0
                for i in range(len(named_account_balances)):
                    if named_account_balances[i]['asset_id'] == asset_id:
                        asset_balance += float(
                            named_account_balances[i]['amount']
                        ) / 10 ** asset_precision
                    elif named_account_balances[i]['asset_id'] == currency_id:
                        currency_balance += float(
                            named_account_balances[i]['amount']
                        ) / 10 ** currency_precision
                # ORDER BOOK
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

                '''
                if str(sorted(bidp)) != str(bidp):
                    raise ValueError('orderbook bid disorder')
                if str(sorted(askp)) != str(askp.reverse()):
                    raise ValueError('orderbook ask disorder')
                '''
                runtime = int(time.time()) - BEGIN

                print_market()
                if (len(white) < WHITE) or (len(black) < BLACK):
                    alert = ' * building lists *'
                else:
                    alert = ''
                print('runtime        ', runtime)
                print('epoch          ', epoch, 'pid', pid)
                print('process        ', process, 'of', PROCESSES)
                print('')
                print('node           ', node)
                print('total nodes    ', len(nodes))
                print('white : black  ', len(white), ':', len(black), alert)
                print('')
                print('block latency  ', ('%.3f' % block_latency))
                print('handshake      ', ('%.3f' % handshake_elapsed))
                print('ping           ', ('%.3f' % ping_elapsed))
                print('')
                print('currency       ', currency_balance, currency)
                print('assets         ', asset_balance, asset)
                print('')
                print('last           ', ('%.16f' % float(last)))
                print('')
                print('history depth', len(history))
                for i in range(3):
                    print(history[i])
                print('')

                print('asks depth', len(askp))
                for i in range(3):
                    print(askp[i], askv[i])
                print('bids depth', len(bidp))
                for i in range(3):
                    print(bidp[i], bidv[i])
                print('')

                winnow('whitelist', node)

                maven = {}
                maven['bidv'] = bidv
                maven['askv'] = askv
                maven['bidp'] = bidp
                maven['askp'] = askp
                maven['currency_balance'] = currency_balance
                maven['asset_balance'] = asset_balance
                maven['market_history'] = history
                maven['last'] = last
                maven['whitelist'] = white
                maven['blacklist'] = black
                maven['blocktime'] = block_time

                nascent_trend(maven)

            try:
                time.sleep(BLIP)
                ws.close()
            except Exception as e:
                msg = str(type(e).__name__) + str(e.args)
                print(msg)
            continue

        except Exception as e:
            try:
                time.sleep(BLIP)
                ws.close()
            except:
                pass
            msg = str(type(e).__name__) + str(e.args) + node
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
            currency_balance = []
            asset_balance = []
            history = []
            last = []
            whitelist = []
            blacklist = []
            blocktime = []
            # initialize the metaNODE dictionary
            metaNODE = {}

            # sort maven data for statistical analysis by key
            for i in range(len(mavens)):
                maven = literal(mavens[i])
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

            # find the oldest bitshares blocktime in our dataset
            blocktime = min(blocktime)
            # get the mode of the mavens for each metric
            # allow 1 or 2 less than total & most recent for mode
            # accept "no mode" statistics error as possibility
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

            # attempt a full whitelist and blacklist
            wl = []
            for i in whitelist:
                wl += i
            whitelist = list(set(wl))[-WHITE:]
            bl = []
            for i in blacklist:
                bl += i
            blacklist = list(set(bl))[-BLACK:]

            # if you made it this far without statistics error
            # populate the metaNODE with curated data
            metaNODE['bidp'] = bidp
            metaNODE['askp'] = askp
            metaNODE['bidv'] = bidv
            metaNODE['askv'] = askv
            metaNODE['currency_balance'] = currency_balance
            metaNODE['asset_balance'] = asset_balance
            metaNODE['market_history'] = history
            metaNODE['last'] = last
            metaNODE['whitelist'] = whitelist
            metaNODE['blacklist'] = blacklist
            metaNODE['blocktime'] = blocktime
            metaNODE['account_name'] = account_name
            metaNODE['account_id'] = account_id
            metaNODE['asset'] = asset
            metaNODE['asset_id'] = asset_id
            metaNODE['asset_precision'] = asset_precision
            metaNODE['currency'] = currency
            metaNODE['currency_id'] = currency_id
            metaNODE['currency_precision'] = currency_precision

            # solitary process with write access to metaNODE.txt            
            race_write(doc='metaNODE.txt', text=metaNODE)
        
        except Exception as e: # wait a second and try again
            msg = str(type(e).__name__) + str(e.args)
            print(msg)
            race_append(doc='metaNODElog.txt', text=msg)
            pass

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
    print('currency  ', currency, currency_id,
          1 / 10 ** currency_precision)
    print('asset     ', asset, asset_id,
          1 / 10 ** asset_precision)
    print('=======================================')
    print('')

def banner():
    print("\033c")
    print(
    '''

    Do this:

        metaNODE = Bitshares_Trustless_Client()
    ''')
    time.sleep(4)
    print("\033c")
    print(
    '''

    Get these curated public node Bitshares DEX feeds:

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

def welcome():

    version()
    print("\033c")
    logo()
    banner()
    time.sleep(5)
    for i in range(5):
        print("\033c")
        logo()
        time.sleep(0.5)
    print('(BTS) litepresence1')

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
