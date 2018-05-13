
#pip install websocket-client
import websocket

from random import random, shuffle, randint
from ast import literal_eval as literal
from multiprocessing import Process
from threading import Thread

from datetime import datetime
from statistics import mode
import logging
import time
import json

# Solid State Drive (SSD) recommended
logging.basicConfig(level=logging.DEBUG)
websocket.enableTrace(False)

MAINNET = '4018d7844c78f6a6c41c6a552b898022310fc5dec06da467ee7905a8dad512c8'
Z = '{"id":1,"method":"call","params":["database",'
BEGIN = int(time.time())

WHITE = 10
BLACK = 30
TIMEOUT = 60
PROCESSES = 8

def logo():
    global nodes
    print('''

########################################################################
                             ____  _____   ___   ______   ________
Bitshares Trustless Client  (_   \(_   _).'   `.(_   _ `.(_   __  \ 
  __  __  ____  ____   __     |   \ | | /  .-.  \ | | `. \ | |_ \_|    
 (  \/  )( ___)(_  _) /  \    | |\ \| | | |   | | | |  | | |  _) _  
  )    ( | __)   ||  / <> \  _| |_\   |_\  `-'  /_| |_.' /_| |__/ | 
 (_/\/\_)(____) (__)(__)(__)(_____|\____)`.___.'(______.'(________/
                                         
########################################################################
''')
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
        'wss://za.bitshares.africa/ws',]

# TEXT PIPE
# ======================================================================
def race_read(doc=''):  # Concurrent Read from File Operation

    i=0
    while 1:
        time.sleep(0.05*random()*i**2)
        i+=1
        try:
            with open(doc, 'r') as f:
                ret = literal(f.read())
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
    return ret

def race_write(doc='', text=''):  # Concurrent Write to File Operation

    i=0
    while 1:
        time.sleep(0.05*random()*i**2)
        i+=1
        try:
            with open(doc, 'w+') as f:
                f.write(str(text))
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
    i=0
    while 1:
        time.sleep(0.05*random()*i**2)
        i+=1
        try:
            with open(doc, 'a+') as f:
                f.write(str(text))
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

def database_call(call):

    while 1:
        try:
            black = race_read(doc='blacklist.txt')
            white = race_read(doc='whitelist.txt')
            # switch nodes
            shuffle(nodes)
            node = nodes[0]
            print(node)
            if node in black:
                raise ValueError ('blacklisted')
            if node in white:
                raise ValueError ('whitelisted')
            call = call.replace("'",'"') # never use single quotes
            if 0:
                print('')
                print((call.split(',"params":')[1]).rstrip('}'))
                print('-------------------------------------------------------')
            ws = websocket.create_connection(node, timeout=4)

            ws.send(call)
            # 'result' key of literally evaluated
            # string representation of dictionary from websocket
            ret = json.loads(ws.recv())['result']
            # print (ret)
            ws.close()
            winnow('whitelist', node)
            return ret
        except Exception as e:
            print (type(e).__name__, e.args, 'switching nodes...')
            winnow('blacklist', node)
            pass

def cache():

    global account_id, asset_id, currency_id, asset_precision, currency_precision
    # establish request header
    print("\033c")
    logo()
    print('')
    print(time.ctime())
    print('')
    print('Winnowing Websocket Connections...')
    print('==================================')
    lookup_accounts = Z + '"lookup_accounts",["%s", "%s"]]}' % (account_name, 1)
    lookup_asset_symbols = Z + '"lookup_asset_symbols",[["%s", "%s"]]]}' % (asset, currency)
    account_ids, asset_ids, currency_ids, asset_precisions, currency_precisions = [],[],[],[],[]

    for i in range(5):
        shuffle(nodes)
        node = nodes[0]

        account_id = (database_call(lookup_accounts))[0][1]

        ret = database_call(lookup_asset_symbols)
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

    print_market()

def flywheel(a):

    # continually respawn terminal children
    p = {}
    b = 0
    while True:
        timeout = randint(TIMEOUT, 2*TIMEOUT)
        try:
            b += 1
            p[str(b)] = Process(target=thresh, args=(a, b))
            p[str(b)].daemon = False
            p[str(b)].start()
            time.sleep(timeout)           
            p[str(b)].terminate()
        except:
            pass

def spawn():

    multinode = {}
    for a in range(PROCESSES):
        multinode[str(a)] = Thread(target=flywheel, args=(a,))
        multinode[str(a)].daemon = False
        multinode[str(a)].start()
        time.sleep(0.1)


def thresh(process, epoch):

    while 1:
        try:
            time.sleep(random())
            black = race_read(doc='blacklist.txt')
            white = race_read(doc='whitelist.txt')
            # switch nodes
            shuffle(nodes)
            node = nodes[0]
            print(node)
            if node in black:
                raise ValueError ('blacklisted')
            if node in white:
                raise ValueError ('whitelisted')
            # request arguments
            coins = [currency_id, asset_id]
            now = to_iso_date(time.time()) 
            then = to_iso_date(time.time()-3*86400)
            get_chain_id = Z + '"get_chain_id",[]]}'
            get_dynamic_global_properties   = Z + '"get_dynamic_global_properties",[]]}'
            get_ticker = Z + '"get_ticker",["%s","%s","%s"]]}' % (currency, asset, False)
            get_trade_history = Z + '"get_trade_history",["%s","%s","%s","%s","%s"]]}' % (currency, asset, now, then, 3)
            get_named_account_balances = Z + '"get_named_account_balances",["%s", ["%s","%s"]]]}' % (account_name, currency_id, asset_id)
            get_order_book = Z + '"get_order_book",["%s","%s","%s"]]}' % (currency, asset, 3)

            #####################
            # WEBSOCKET HANDSHAKE
            start = time.time()
            ws = websocket.create_connection(node, timeout=4)
            handshake_elapsed = time.time()-start
            if handshake_elapsed > 4:
                raise ValueError ('handshake_elapsed', handshake_elapsed)
            #####################

            for i in range(randint(8,12)):
                time.sleep(1+random())
                # CHAIN ID
                start = time.time()
                ws.send(get_chain_id)
                chain_id = json.loads(ws.recv())['result']
                ping_elapsed = time.time()-start
                if chain_id != MAINNET:
                    raise ValueError ('chain_id != MAINNET')
                if ping_elapsed > 1:
                    raise ValueError ('ping_elapsed', ping_elapsed)

                # BLOCKTIME
                time.sleep(0.1)
                ws.send(get_dynamic_global_properties)
                dynamic_global_properties = json.loads(ws.recv())['result']
                block_time = from_iso_date(dynamic_global_properties['time'])
                block_latency = tz+time.time()-block_time
                if block_latency > 6:
                    raise ValueError('blocktime is stale', block_latency)

                # LAST
                time.sleep(0.1)
                ws.send(get_ticker)
                ticker = json.loads(ws.recv())['result']
                last = precision(ticker['latest'], 16)
                if float(last) == 0:
                    raise ValueError('zero price last')

                # MARKET HISTORY
                time.sleep(0.1)
                ws.send(get_trade_history)
                trade_history = json.loads(ws.recv())['result']
                history = []
                for i in range(len(trade_history)):
                    unix = from_iso_date(trade_history[i]['date'])
                    price = precision(trade_history[i]['price'], 16)
                    if float(price) == 0:
                        raise ValueError ('zero price in history')
                    amount = precision(trade_history[i]['amount'], asset_precision)                
                    history.append((unix, price, amount))

                # ACCOUNT BALANCES
                time.sleep(0.1)
                ws.send(get_named_account_balances)
                named_account_balances = json.loads(ws.recv())['result']
                currency_balance = 0
                asset_balance = 0
                for i in range(len(named_account_balances)):
                    if named_account_balances[i]['asset_id'] == asset_id:
                        asset_balance+=float(named_account_balances[i]['amount'])/10**asset_precision
                    elif named_account_balances[i]['asset_id'] == currency_id:
                        currency_balance+=float(named_account_balances[i]['amount'])/10**currency_precision

                # ORDER BOOK
                time.sleep(0.1)
                ws.send(get_order_book)
                order_book = json.loads(ws.recv())['result']
                asks = []
                bids = []
                for i in range(len(order_book['asks'])):
                    price = precision(order_book['asks'][i]['price'], 16)
                    if float(price) == 0:
                        raise ValueError ('zero price in asks')
                    volume = precision(order_book['asks'][i]['quote'], asset_precision)
                    asks.append((price,volume))
                for i in range(len(order_book['bids'])):
                    price = precision(order_book['bids'][i]['price'], 16)
                    if float(price) == 0:
                        raise ValueError ('zero price in bids')
                    volume = precision(order_book['bids'][i]['quote'], asset_precision)
                    bids.append((price,volume))
                if bids[0][0] >= asks[0][0]:
                    raise ValueError ('mismatched orderbook')
                runtime = int(time.time()) - BEGIN

                print_market()
                print('runtime        ', runtime)
                print('epoch          ', epoch)
                print('process        ', process)
                print('')
                print('node           ', node)
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
                print('history')
                for i in range(3):
                    print(history[i])
                print('')
                print('asks')
                for i in range(3):
                    print(asks[i])
                print('bids')
                for i in range(3):
                    print(bids[i])
                print('')

                winnow('whitelist', node)
                whitelist = race_read(doc='whitelist.txt')
                blacklist = race_read(doc='blacklist.txt')

                metaNODE = {}
                metaNODE['bids'] = bids
                metaNODE['asks'] = asks
                metaNODE['currency_balance'] = currency_balance
                metaNODE['asset_balance'] = asset_balance
                metaNODE['market_history'] = history
                metaNODE['last'] = last
                metaNODE['whitelist'] = whitelist
                metaNODE['blacklist'] = blacklist
                race_write(doc='metaNODE.txt', text=metaNODE)

            ws.close()
            continue


        except Exception as e:
            try:
                time.sleep(0.1)
                ws.close()
            except:
                pass
            msg = str(type(e).__name__) + str(e.args)
            print(msg)
            race_append(doc='metaNODElog.txt', text = msg)
            winnow('blacklist', node)
            continue

    call = call.replace("'",'"') # never use single quotes

def winnow(x, node):

    if x == 'blacklist':
        black = race_read(doc='blacklist.txt')
        if node in black:
            black.remove(node)
        black.append(node)
        black = black[-BLACK:]
        race_write(doc='blacklist.txt', text=black)

    if x == 'whitelist':
        white = race_read(doc='whitelist.txt')
        if node in white:
            white.remove(node)
        white.append(node)
        white = white[-WHITE:]
        race_write(doc='whitelist.txt', text=white)



# HELPER FUNCTIONS
# ======================================================================
def to_iso_date(unix): #'2017-01-01T11:22:33'

    return datetime.utcfromtimestamp(int(unix)).isoformat()

def from_iso_date(date):

    return int(time.mktime(time.strptime(str(date), '%Y-%m-%dT%H:%M:%S')))

def precision(x,n):

    return ('%.' + str(n) + 'f') % float(x)

def print_market():


    print("\033c")
    logo()
    print('')

    print(time.ctime())
    print('=======================================')
    print('account   ', account_name, account_id)
    print('currency  ', currency, currency_id, 1/10**currency_precision)
    print('asset     ', asset, asset_id, 1/10**asset_precision)
    print('=======================================')
    print('')

def run_forever():
    while 1:
        time.sleep(1000)

def banner():

    print(
    '''

    do this:

        metaNODE = race_read(doc='metaNODE.txt')

    get this curated live Bitshares DEX data:

    metaNODE['last']      # float; latest price
    metaNODE['bids']      # list of (price,amount) tuples; [0][0]=highest bid price
    metaNODE['asks']      # list of (price,amount) tuples; [0][0]=lowest ask price
    metaNODE['history']   # list of (unix,price,amount) tuples; [0][0]=last trade time
    metaNODE['currency']  # float; quantity of currency
    metaNODE['assets']    # float; quantity of assets
    metaNODE['whitelist'] # list; [0]=most recently whitelisted node
    metaNODE['blacklist'] # list; [0]=most recently blacklisted node
    metaNODE['orders']    # list; open order_id's (...orders coming soon...)
    ''')


print("\033c")
logo()
banner()
time.sleep(3)
print("\033c")
logo()
time.sleep(1)
race_write(doc='blacklist.txt', text=[])
race_write(doc='whitelist.txt', text=[])
race_write(doc='metaNODElog.txt', text='')
tz = time.altzone
account_name = 'litepresence1'
currency = 'OPEN.BTC'
asset = 'BTS'
cache()
spawn()

run_forever()

'''
API CALLS:

lookup_accounts = Z + '"lookup_accounts",["%s", "%s"]]}' % (account_name, 1)
lookup_asset_symbols = Z + '"lookup_asset_symbols",[["%s", "%s"]]]}' % (asset, currency)

get_chain_id = Z + '"get_chain_id",[]]}'
get_dynamic_global_properties   = Z + '"get_dynamic_global_properties",[]]}'

get_ticker = Z + '"get_ticker",["%s","%s","%s"]]}' % (currency, asset, False)
get_trade_history = Z + '"get_trade_history",["%s","%s","%s","%s","%s"]]}' % (currency, asset, now, then, limit)
get_named_account_balances = Z + '"get_named_account_balances",["%s", ["%s","%s"]]]}' % (account_name, currency_id, asset_id)
get_order_book = Z + '"get_order_book",["%s","%s","%s"]]}' % (currency, asset, limit)
'''
