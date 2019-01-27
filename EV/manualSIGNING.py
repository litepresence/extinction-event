
' manualSIGNING '

# Authenticated BUY/SELL/CANCEL without Pybitshares(MIT) Architecture

' litepresence 2019 '

' ***** WARN: THIS SCRIPT IS FEATURE COMPLETE ALPHA ***** '

# Joe CEX algo trader finds bitshares DEX and asks:

# How do I get good public API data that never goes stale?
' metaNODE.py'
# How do I authenticate?
' manualSIGNING.py ' 
# What nodes to use?
' latencyTEST.py'

# three 50KB scripts and DEX algo trading barriers to entry defeated:
# buy/sell/cancel - six sigma connectivity - simple auth - cex like data   

' ********************************************** '
' ****** API CHANGE IN VERSION 0.00000003 ****** '
' ********************************************** '

# order is now a dictionary of:
"['edicts', 'header', 'nodes']"
# see sample_orders() for examples

' NEW FEATURES '

# edicts can be any mixed list of buy/sell/cancel 
# autoscale buy/sell orders to account means if overbudget
# autoscale buy/sell orders to retain last two bitshares for fees
# multiprocessing ensures websockets and faulty orders timeout
# control_panel() advanced user controls to alter execution behaviors

' HOW DO I USE THIS THING? '

' from manualSIGNING import broker '
' broker(order) '


def WTFPL_v0_March_1765():
    if any([stamps, licenses, taxation, regulation, fiat, etat]):
        try:
            print('no thank you')
        except:
            return [tar, feathers]

' OBJECTIVES '

'import only standard python objects' # DONE
'gather needed pybitshares objects: copy, paste, and cite' # DONE
'strip pybitshares objects of unused methods' # DONE
'restack classes and definitions chronologically' # DONE
'allow orders to be placed in human terms' # DONE
'build tx in graphene terms' # DONE
'serialize tx' # DONE
'validate serialization via get_transaction_hex_without_sig()' # DONE
'sign tx with ECDSA' # DONE
'validate signed tx' # DONE
'broadcast tx to rpc node' # DONE
'allow this script to be imported as module; broker(order)' # DONE
'allow list of buy/sell/cancel edicts' # DONE
'allow cancel-all' # DONE
'heavy line-by-line commentary' # DONE
'extinctionEVENT implementation' # DONE

'simplify and condense pybitshares methods' # ONGOING
'whitepaper readme.md' # 5200 word rough draft, editing ongoing

'microDEX implementation' # TODO

' DEPENDENCIES '

# python 3 on a linux box
# pip3 install: ecdsa, secp256k1, websocket-client

' LICENSE: '

# citations to pybitshares(MIT) & @xeroc where pertinent
# h/t @vvk123 @sschiessl @harukaff_bot
# remainder WTFPL 1765

DEV = False
COLOR = True
VERSION = 0.00000003

' STANDARD PYTHON MODULES '

from time import time, ctime, mktime, strptime, sleep
from multiprocessing import Process, Value # encapsulate processes
from decimal import Decimal as decimal  # higher precision than float
from json import dumps as json_dumps  # serialize object to string
from json import loads as json_loads  # deserialize string to object
from collections import OrderedDict
from traceback import format_exc # stack trace in terminal
from datetime import datetime
from calendar import timegm
from getpass import getpass  # hidden input()
from random import shuffle
from pprint import pprint  # pretty printing

import sys
import os

' STANDARD CONVERSION UTILITIES '

from binascii import hexlify  # binary text to hexidecimal
from binascii import unhexlify  # hexidecimal to binary text
from zlib import decompress  # aka gzip inflate; only used for logo
from hashlib import sha256  # message digest algorithm
from hashlib import new as hashlib_new  # access algorithm library
from struct import pack  # convert to string representation of C struct
from struct import unpack, unpack_from  # convert back to PY variable

' NON STANDARD MODULES WHICH REQUIRE INSTALLATION '

print('sudo apt update')
print('sudo apt install python3-pip')
print('pip3 install websocket-client')
print('pip3 install secp256k1')
print('pip3 install ecdsa')
from websocket import create_connection as wss  # handshake to node
from secp256k1 import PrivateKey as secp256k1_PrivateKey  # class
from secp256k1 import PublicKey as secp256k1_PublicKey  # class
from secp256k1 import ffi as secp256k1_ffi  # compiled ffi object
from secp256k1 import lib as secp256k1_lib  # library
from ecdsa import numbertheory as ecdsa_numbertheory  # largest import
from ecdsa import VerifyingKey as ecdsa_VerifyingKey  # class
from ecdsa import SigningKey as ecdsa_SigningKey  # class
from ecdsa import SECP256k1 as ecdsa_SECP256k1  # curve
from ecdsa import util as ecdsa_util  # module
from ecdsa import der as ecdsa_der  # module
print("\033c") # clear screen if they are all installed 

' LINUX AND PYTHON 3 REQUIRED '

# require a serious professional audience on linux/py3 installation
from sys import platform, version_info
if 'linux' not in platform:
    raise Exception('not a linux box, format drive and try again...')
if version_info[0] < 3:
    raise Exception("% is DED, long live Python 3.4+" % version_info[0])

' PRINT CONTROL ' 

def blockPrint():
    # temporarily disable printing
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    # re-enable printing
    sys.stdout = sys.__stdout__

def trace(e):
    # print stack trace upon exception
    msg = str(type(e).__name__) + '\n'
    msg += str(e.args) + '\n'
    msg += str(format_exc()) + '\n'
    print(msg)

' GLOBALS '

def sample_orders():

    global order1, order2, order3

    # cancel all and place two buy orders
    order1 =  {
              'edicts': [   {'op':'cancel',
                            'ids': ['1.7.X']}, # cancel all
                            {'op':'buy',
                            'amount': 10.0,
                            'price': 0.00000100,
                            'expiration': 0},
                            {'op':'buy',
                            'amount': 30.0,
                            'price': 0.00000150,
                            'expiration': 0},

                        ],
              'header': {   'asset_id': '1.3.0',
                            'currency_id': '1.3.861',
                            'asset_precision': 5,
                            'currency_precision': 8,
                            'account_id': '1.2.x',
                            'account_name': '',
                            'wif':'',
                            },
              'nodes': [
                            'wss://chicago.bitshares.apasia.tech/wss',
                            'wss://new-york.bitshares.apasia.tech/wss',
                            'wss://seattle.bitshares.apasia.tech/wss',
                            'wss://us-ny.bitshares.apasia.tech/wss',
                            'wss://us-la.bitshares.apasia.tech/wss',
                       ]}
    # place one sell order
    order2 =  {
              'edicts': [   
                            {'op':'sell',
                            'amount': 10.0,
                            'price': 0.00020000,
                            'expiration': 0},
                        ],
              'header': {   'asset_id': '1.3.0',
                            'currency_id': '1.3.861',
                            'asset_precision': 5,
                            'currency_precision': 8,
                            'account_id': '1.2.x',
                            'account_name': '',
                            'wif':'',
                            },
              'nodes': [
                            'wss://chicago.bitshares.apasia.tech/wss',
                            'wss://new-york.bitshares.apasia.tech/wss',
                            'wss://seattle.bitshares.apasia.tech/wss',
                            'wss://us-ny.bitshares.apasia.tech/wss',
                            'wss://us-la.bitshares.apasia.tech/wss',
                       ]}
    # cancel all
    order3 =  {
              'edicts': [   {'op':'cancel',
                            'ids': ['1.7.X']}, # cancel all
                            # or cancel specific order numbers:
                            #{'op':'cancel',
                            #'ids':['1.7.101','1.7.102','1.7.103']},
                            {'op':'buy',
                            'amount': 10.0,
                            'price': 0.00000100,
                            'expiration': 0},
                            {'op':'sell',
                            'amount': 10.0,
                            'price': 0.00020000,
                            'expiration': 0},
                        ],
              'header': {   'asset_id': '1.3.0',
                            'currency_id': '1.3.861',
                            'asset_precision': 5,
                            'currency_precision': 8,
                            'account_id': '1.2.x',
                            'account_name': '',
                            'wif':'',
                            },
              'nodes': [
                            'wss://chicago.bitshares.apasia.tech/wss',
                            'wss://new-york.bitshares.apasia.tech/wss',
                            'wss://seattle.bitshares.apasia.tech/wss',
                            'wss://us-ny.bitshares.apasia.tech/wss',
                            'wss://us-la.bitshares.apasia.tech/wss',
                       ]}

def global_variables():

    global info

    info = {}
    info['id'] = 1  # will be used to increment rpc request id

def global_constants():

    global OP_IDS, OP_NAMES, ID, TYPES
    global BASE58, HEXDIGITS, ISO8601, END_OF_TIME
    # bitsharesbase/operationids.py
    OP_IDS = {"Limit_order_create": 1,
              "Limit_order_cancel": 2}
    # swap keys/values to index names by number
    OP_NAMES = {v: k for k, v in OP_IDS.items()}
    # bitsharesbase/chains.py
    ID = "4018d7844c78f6a6c41c6a552b898022310fc5dec06da467ee7905a8dad512c8"
    # bitsharesbase/objecttypes.py used by ObjectId() to confirm a.b.c
    TYPES = {"account": 2, # 1.2.x
             "asset": 3, # 1.3.x
             "limit_order": 7} # 1.7.x
    # base58 encoding and decoding; this is alphabet defined:
    BASE58 = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    # hex encoding and decoding
    HEXDIGITS = "0123456789abcdefABCDEF"
    # ISO8601 timeformat; 'graphene time'
    ISO8601 = '%Y-%m-%dT%H:%M:%S%Z'
    # MAX is 4294967295; year 2106 due to 4 byte unsigned integer
    END_OF_TIME = 4*10**9 # about 75 years in future

def control_panel():

    global HANDSHAKE_TIMEOUT, PROCESS_TIMEOUT, AUTOSCALE, BTS_FEES
    global KILL_OR_FILL, ATTEMPTS, JOIN, LIMIT, DUST

    ' advanced user controls to alter execution behaviors '
    # timeout during websocket handshake; default 4 seconds
    HANDSHAKE_TIMEOUT = 4
    # multiprocessing handler lifespan, default 20 seconds
    PROCESS_TIMEOUT = 20
    # default False for persistent limit orders
    KILL_OR_FILL = False
    # default True scales elements of oversize gross order to means
    AUTOSCALE = True
    # default True to never spend last 2 bitshares
    BTS_FEES = True
    # multiprocessing incarnations, default 3 attempts
    ATTEMPTS = 3
    # prevent extreme number of AI generated edicts; default 20
    LIMIT = 20
    # default True to execute order in primary script process
    JOIN = True
    # ignore orders value less than ~X bitshares; 0 to disable
    DUST = 20

' COLOR TERMINAL '

def red(text):
    return ('\033[91m' + text + '\033[0m') if COLOR else text

def green(text):
    return ('\033[92m' + text + '\033[0m') if COLOR else text

def yellow(text):
    return ('\033[93m' + text + '\033[0m') if COLOR else text

def blue(text):
    return ('\033[94m' + text + '\033[0m') if COLOR else text

def purple(text):
    return ('\033[105m' + text + '\033[0m') if COLOR else text

def cyan(text):
    return ('\033[96m' + text + '\033[0m') if COLOR else text

' REMOTE PROCEDURE CALLS TO PUBLIC API NODES'

def wss_handshake():

    # create a wss handshake in less than X seconds, else try again
    print(purple('wss_handshake - node list is hard coded'))
    print('in production use latencyTEST.py to generate list')
    global ws, nodes  # the websocket is created and node list shuffled

    shuffle(nodes)
    handshake = 999
    while handshake > HANDSHAKE_TIMEOUT:
        try:
            try:
                ws.close # attempt to close open stale connection
                print(purple('connection terminated'))
            except:
                pass
            start = time()
            nodes.append(nodes.pop(0))  # rotate list
            node = nodes[0]
            print(purple('connecting:'), node)
            ws = wss(node, timeout=HANDSHAKE_TIMEOUT)
            handshake = (time() - start)
        except:
            continue
    print(purple('connected:'), node, ws)
    print('elapsed %.3f sec' % (time() - start))

def wss_query(params):

    # this definition will place all remote procedure calls (RPC)
    i = 0 # this will keep track of iterations to increase sleep time
    start = time() # this for elapsed time calculation at end 
    while True:
        i += 1
        try:
            # print(purple('RPC ' + params[0]), cyan(params[1]))
            # this is the 4 part format of EVERY rpc request
            # params format is ["location", "object", []]
            query = json_dumps({"method": "call",
                                "params": params,
                                "jsonrpc": "2.0",
                                "id": 1})

            # print(query)
            # ws is the websocket connection created by wss_handshake()
            # we will use this connection to send query and receive json
            ws.send(query)
            ret = json_loads(ws.recv())
            try:
                ret = ret['result'] # if there is result key take it
            except:
                pass
            # print(ret)
            # print('elapsed %.3f sec' % (time() - start))
            return ret
        except Exception as e: 
            try: # attempt to terminate the connection
                ws.close()
            except:
                pass
            trace(e) # tell me what happened
            # sleep for an ever increasing amount of time between loops
            sleep(0.05 ** (1.0 / i))
            # switch nodes
            wss_handshake()
            continue

def rpc_block_number():
    # block number and block prefix
    ret = wss_query(["database",
                     "get_dynamic_global_properties",
                     []])
    return ret

def rpc_account_id():
    # given an account name return an account id
    ret = wss_query(["database",
                     "lookup_accounts",
                     [account_name, 1]])
    account_id = ret[0][1]
    return account_id

def rpc_fees():
    # returns fee for limit order create and cancel without 10^precision
    query = ["database",
             "get_required_fees",[[
                ['1', {"from": str(account_id)}],
                ['2', {"from": str(account_id)}]], "1.3.0"  ]]
    ret = wss_query(query)
    create = ret[0]['amount']
    cancel = ret[1]['amount']
    return {'create': create, 'cancel': cancel}

def rpc_balances():

    balances = wss_query(["database",
                     "get_named_account_balances",
                     [account_name, [currency_id, asset_id, '1.3.0']]])

    #print(balances)
    for balance in balances:
        if balance['asset_id'] == currency_id:
            currency = balance['amount'] / 10 ** currency_precision
        if balance['asset_id'] == asset_id:
            assets = balance['amount'] / 10 ** asset_precision
        if balance['asset_id'] == '1.3.0':
            bitshares = balance['amount'] / 10 ** 5

    #print(currency, assets, bitshares)
    return currency, assets, bitshares

def rpc_open_orders():
    # return a list of open orders, for one account, in one market
    ret = wss_query(["database",
                     "get_full_accounts",
                    [[account_name],"false"]])
    try:
        limit_orders = ret[0][1]['limit_orders']
    except:
        limit_orders = []
    market = [currency_id, asset_id]
    orders = []
    for order in limit_orders:
        base_id = order['sell_price']['base']['asset_id']
        quote_id = order['sell_price']['quote']['asset_id']
        if (base_id in market) and (quote_id in market):
            orders.append(order['id'])
    return(orders)

def rpc_get_transaction_hex_without_sig(tx):
    # use this to verify the manually serialized tx buffer
    ret = wss_query(["database",
                     "get_transaction_hex_without_sig",
                     [tx]])
    return bytes(ret, 'utf-8')

def rpc_broadcast_transaction(tx):
    # upload the signed transaction to the blockchain
    ret = wss_query(["network_broadcast",
                     "broadcast_transaction",
                     [tx]])
    if ret == None:
        print(yellow('*************************************'))
        print('manualSIGNING' + red(' has placed your order'))
        print(yellow('*************************************'))
        return tx
    pprint(ret)
    return ret

' DATE FORMATTING '

def to_iso_date(unix):
    # returns iso8601 datetime given unix epoch
    iso = datetime.utcfromtimestamp(int(unix)).isoformat()
    return iso

def from_iso_date(iso):
    # returns unix epoch given iso8601 datetime
    unix = int(timegm(strptime((iso + "UTC"), ISO8601)))
    return unix

' GRAPHENEBASE TYPES '  # graphenebase/types.py

def types_README():
    # graphenebase types use python "dunder" / "magic" methods
    # these are a little abstract and under documented; to elucidate:
    # bytes() is a "built in" function like str(), int(), list()
    # it returns byte strings like: b'\x00\x00\x00'
    # these methods will redefine the type of byte string
    # returned by the "built in" bytes() in global space
    # but only when bytes() is called on an object that has passed
    # through a class with a "magic" __bytes__ method
    # these methods are used to serialize OrderDicts of various elements

    # graphenebase  __str__() methods have been removed
    # as they are unused for limit order operations

    # Set() has been merged into Array()
    # Bool() has been merged into Uint8()
    # Varint32() has been merged into both Id() and Array()

    'consider the following "magic method" example'
    # this would have no effect on the way bytes() normally behaves
    class normal():
        def __init__(self, d):
            self.data = int(d)
        def __bytes__(self):
            return bytes(self.data)
    # this redifines bytes() in global to pack unsigned 8 bit integers
    # but only in the case of bytes(Uint8(x))
    class Uint8():
        def __init__(self, d):
            self.data = int(d)
        def __bytes__(self):
            return pack("<B", self.data)
    # this is a definition method to accomplish the same "magic"
    def bytes_Uint8(data):
        return pack("<B", int(data))
    # apply each of these methods to x=3 to show what happens
    x = 3
    print(bytes(x))
    print(bytes(normal(x)))
    print(bytes(Uint8(x)))
    print(bytes_Uint8(x))
    '''
    # >>>
    # b'\x00\x00\x00'
    # b'\x00\x00\x00'
    # b'\x03'
    # b'\x03'
    '''

class ObjectId():

    # encodes a.b.c object ids - serializes the *instance* only!
    def __init__(self, object_str, type_verify=None):
        # if after splitting a.b.c there are 3 pieces:
        if len(object_str.split(".")) == 3:
            # assign those three pieces to a, b, and c
            a, b, c = object_str.split(".")
            # assure they are integers
            self.a = int(a)
            self.b = int(b)
            self.c = int(c)
            # serialize the c element; the "instance"
            self.instance = Id(self.c)
            self.abc = object_str
            # 1.2.x:account, 1.3.x:asset, or 1.7.x:limit
            if type_verify:                
                assert (TYPES[type_verify] == int(b)), (
                    # except raise error showing mismatch
                    "Object id does not match object type! " +
                    "Excpected %d, got %d" %
                    (TYPES[type_verify], int(b)))
        else:
            raise Exception("Object id is invalid")

    def __bytes__(self):
        # b'\x00\x00\x00' of serialized c element; the "instance"
        return bytes(self.instance)  

class Id():
    # serializes the c element of "a.b.c" types
    # merged with Varint32()
    def __init__(self, d):
        self.data = int(d)

    def __bytes__(self):
        return bytes(varint(self.data))

class Array():
    # serializes lists as byte strings
    # merged with Set() and Varint32()
    def __init__(self, d):
        self.data = d
        self.length = int(len(self.data))

    def __bytes__(self):
        return bytes(varint(self.length)) + b"".join([bytes(a) for a in self.data])

class Uint8():
    # byte string of 8 bit unsigned integers
    # merged with Bool()
    def __init__(self, d):
        self.data = int(d)

    def __bytes__(self):
        return pack("<B", self.data)

class Uint16():
    # byte string of 16 bit unsigned integers
    def __init__(self, d):
        self.data = int(d)

    def __bytes__(self):
        return pack("<H", self.data)

class Uint32():
    # byte string of 32 bit unsigned integers
    def __init__(self, d):
        self.data = int(d)

    def __bytes__(self):
        return pack("<I", self.data)

class Int64():
    # byte string of 64 bit unsigned integers
    def __init__(self, d):
        self.data = int(d)

    def __bytes__(self):
        return pack("<q", self.data)

class Signature():
    # used to disable bytes() method on Signatures in OrderedDicts
    def __init__(self, d):
        self.data = d

    def __bytes__(self):
        return self.data # note does NOT return bytes(self.data)

class PointInTime():
    # used to pack ISO8601 time as 4 byte unix epoch integer as bytes
    def __init__(self, d):
        self.data = d

    def __bytes__(self):
        return pack("<I", from_iso_date(self.data))

' VARINT '

def varint(n):
    # varint encoding normally saves memory on smaller numbers
    # yet retains ability to represent numbers of any magnitude
    data = b''
    while n >= 0x80:
        data += bytes([(n & 0x7f) | 0x80])
        n >>= 7
    data += bytes([n])
    return data

' BASE 58 ENCODE, DECODE, AND CHECK '  # graphenebase/base58.py

class Base58(object):

    """
    This class serves as an abstraction layer
    to deal with base58 encoded strings
    and their corresponding hex and binary representation
    """

    def __init__(self, data, prefix='BTS'):

        print(green('Base58'))
        print(blue(data))
        self._prefix = prefix
        if all(c in HEXDIGITS for c in data):
            self._hex = data
        elif data[0] == "5" or data[0] == "6":
            self._hex = base58CheckDecode(data)
        elif data[0] == "K" or data[0] == "L":
            self._hex = base58CheckDecode(data)[:-2]
        elif data[:len(self._prefix)] == self._prefix:
            self._hex = gphBase58CheckDecode(data[len(self._prefix):])
        else:
            raise ValueError("Error loading Base58 object")

    def __format__(self, _format):

        if _format.upper() == 'BTS':
            return _format.upper() + str(self)
        else:
            print("Format %s unkown. You've been warned!\n" % _format)
            return _format.upper() + str(self)

    def __repr__(self):  # hex string of data
        return self._hex

    def __str__(self):  # base58 string of data
        return gphBase58CheckEncode(self._hex)

    def __bytes__(self):  # raw bytes of data
        return unhexlify(self._hex)

def base58decode(base58_str):
    print(green('base58decode'))
    base58_text = bytes(base58_str, "ascii")
    n = 0
    leading_zeroes_count = 0
    for b in base58_text:
        n = n * 58 + BASE58.find(b)
        if n == 0:
            leading_zeroes_count += 1
    res = bytearray()
    while n >= 256:
        div, mod = divmod(n, 256)
        res.insert(0, mod)
        n = div
    else:
        res.insert(0, n)
    return hexlify(bytearray(1) * leading_zeroes_count + res).decode('ascii')

def base58encode(hexstring):
    print(green('base58encode'))
    byteseq = bytes(unhexlify(bytes(hexstring, 'ascii')))
    n = 0
    leading_zeroes_count = 0
    for c in byteseq:
        n = n * 256 + c
        if n == 0:
            leading_zeroes_count += 1
    res = bytearray()
    while n >= 58:
        div, mod = divmod(n, 58)
        res.insert(0, BASE58[mod])
        n = div
    else:
        res.insert(0, BASE58[n])
    ret = (BASE58[0:1] * leading_zeroes_count + res).decode('ascii')

    print(purple('BTS' + str(ret)), "public key")
    print('len(ret)', len(ret))
    return ret

def ripemd160(s):
    # 160-bit cryptographic hash function
    ripemd160 = hashlib_new('ripemd160') # import the library
    ripemd160.update(unhexlify(s))
    ret = ripemd160.digest()
    print('use hashlib to perform a ripemd160 message digest')
    print(ret)
    return ret

def doublesha256(s):
    # double sha256 cryptographic hash function
    ret = sha256(sha256(unhexlify(s)).digest()).digest()
    print('use hashlib to perform a doublesha26 message digest')
    print(ret)
    return ret
    
def base58CheckEncode(version, payload):

    print(green('base58CheckEncode'))
    print(payload, version)
    s = ('%.2x' % version) + payload
    print(s)
    checksum = doublesha256(s)[:4]
    result = s + hexlify(checksum).decode('ascii')
    return base58encode(result)

def gphBase58CheckEncode(s):
    print(yellow('gphBase58CheckEncode'))
    print(s)
    checksum = ripemd160(s)[:4]
    result = s + hexlify(checksum).decode('ascii')
    return base58encode(result)

def base58CheckDecode(s):
    print(green('base58CheckDecode'))
    print(s)
    s = unhexlify(base58decode(s))
    dec = hexlify(s[:-4]).decode('ascii')
    checksum = doublesha256(dec)[:4]
    assert(s[-4:] == checksum)
    return dec[2:]

def gphBase58CheckDecode(s):
    print(yellow('gphBase58CheckDecode'))
    print(s)
    s = unhexlify(base58decode(s))
    dec = hexlify(s[:-4]).decode('ascii')
    checksum = ripemd160(dec)[:4]
    assert(s[-4:] == checksum)
    return dec

' ADDRESS AND KEYS '

class Address(object):  # cropped litepresence2019

    """
    Example :: Address("BTSFN9r6VYzBK8EKtMewfNbfiGCr56pHDBFi")
    """
    # graphenebase/account.py

    def __init__(self, address=None, pubkey=None, prefix="BTS"):
        print(red('Address'), 'pubkey', pubkey)
        self.prefix = prefix
        self._pubkey = Base58(pubkey, prefix=prefix)
        self._address = None

class PublicKey(Address):  # graphenebase/account.py

    """
    This class deals with Public Keys and inherits ``Address``.

    :param str pk: Base58 encoded public key
    :param str prefix: Network prefix (defaults to ``BTS``)
    """

    def __init__(self, pk, prefix="BTS"):
        print(red('PublicKey'))
        self.prefix = prefix
        self._pk = Base58(pk, prefix=prefix)
        self.address = Address(pubkey=pk, prefix=prefix)
        self.pubkey = self._pk

    def _derive_y_from_x(self, x, is_even):
        print(purple('           y^2 = x^3 + ax + b          '))
        print(self, x)
        """ Derive y point from x point """
        curve = ecdsa_SECP256k1.curve
        a, b, p = curve.a(), curve.b(), curve.p()
        alpha = (pow(x, 3, p) + a * x + b) % p
        beta = ecdsa_numbertheory.square_root_mod_prime(alpha, p)
        if (beta % 2) == is_even:
            beta = p - beta
        print(beta)
        return beta

    def compressed(self):
        print('PublicKey.compressed')
        """ Derive compressed public key """
        order = ecdsa_SECP256k1.generator.order()
        p = ecdsa_VerifyingKey.from_string(
            bytes(self),
            curve=ecdsa_SECP256k1).pubkey.point
        x_str = ecdsa_util.number_to_string(p.x(), order)
        # y_str = ecdsa_util.number_to_string(p.y(), order)
        compressed = hexlify(
            bytes(chr(2 + (p.y() & 1)),
                  'ascii') + x_str).decode('ascii')
        return(compressed)

    def unCompressed(self):
        print('PublicKey.unCompressed')
        """ Derive uncompressed key """
        public_key = repr(self._pk)
        prefix = public_key[0:2]
        if prefix == "04":
            return public_key
        assert prefix == "02" or prefix == "03"
        x = int(public_key[2:], 16)
        y = self._derive_y_from_x(x, (prefix == "02"))
        key = '04' + '%064x' % x + '%064x' % y
        return key

    def __repr__(self):
        # print('PublicKey.__repr__')
        """ Gives the hex representation of the Graphene public key. """
        return repr(self._pk)

    def __format__(self, _format):
        # print('PublicKey.__format__')
        """ Formats the instance of:doc:`Base58 <base58>
        ` according to ``_format`` """
        return format(self._pk, _format)

    def __bytes__(self):
        # print('PublicKey.__bytes__')
        """ Returns the raw public key (has length 33)"""
        return bytes(self._pk)

class PrivateKey(PublicKey):  # merged litepresence2019

    # Bitshares(MIT) graphenebase/account.py
    # Bitshares(MIT) bitsharesbase/account.py

    """ Derives the compressed and uncompressed public keys and
        constructs two instances of ``PublicKey``:
    """

    def __init__(self, wif=None, prefix="BTS"):

        print(prefix)
        print(red('PrivateKey'))
        print(PublicKey)
        if wif is None:
            import os
            self._wif = Base58(hexlify(os.urandom(32)).decode('ascii'))
        elif isinstance(wif, Base58):
            self._wif = wif
        else:
            self._wif = Base58(wif)
        # compress pubkeys only
        self._pubkeyhex, self._pubkeyuncompressedhex = self.compressedpubkey()
        self.pubkey = PublicKey(self._pubkeyhex, prefix=prefix)
        self.uncompressed = PublicKey(
            self._pubkeyuncompressedhex,
            prefix=prefix)
        self.uncompressed.address = Address(
            pubkey=self._pubkeyuncompressedhex,
            prefix=prefix)
        self.address = Address(pubkey=self._pubkeyhex, prefix=prefix)

    def compressedpubkey(self):
        print('PrivateKey.compressedpubkey')
        """ Derive uncompressed public key """
        secret = unhexlify(repr(self._wif))
        order = ecdsa_SigningKey.from_string(
            secret,
            curve=ecdsa_SECP256k1).curve.generator.order()
        p = ecdsa_SigningKey.from_string(
            secret,
            curve=ecdsa_SECP256k1).verifying_key.pubkey.point
        x_str = ecdsa_util.number_to_string(p.x(), order)
        y_str = ecdsa_util.number_to_string(p.y(), order)
        compressed = hexlify(
            chr(2 + (p.y() & 1)).encode('ascii') + x_str).decode('ascii')
        uncompressed = hexlify(
            chr(4).encode('ascii') + x_str + y_str).decode('ascii')
        return([compressed, uncompressed])

    def __bytes__(self):
        # print('PrivateKey.__bytes__')
        """ Returns the raw private key """
        return bytes(self._wif)

' SERIALIZATION '

class GrapheneObject(object):  # Bitshares(MIT) graphenebase/objects.py

    def __init__(self, data=None):
        self.data = data

    def __bytes__(self):
        # encodes data into wire format'
        if self.data is None:
            return bytes()
        b = b""
        for name, value in self.data.items():
            if isinstance(value, str):
                b += bytes(value, 'utf-8')
            else:
                b += bytes(value)
        return b

class Asset(GrapheneObject):  # bitsharesbase/objects.py

    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('amount', Int64(kwargs["amount"])),
                ('asset_id', ObjectId(kwargs["asset_id"], "asset"))
            ]))

class Operation():  # refactored  litepresence2019

    'class GPHOperation():'
    # Bitshares(MIT) graphenebase/objects.py
    'class Operation(GPHOperation):'
    # Bitshares(MIT) bitsharesbase/objects.py

    def __init__(self, op):

        if not (isinstance(op, list)):
            raise ValueError('expecting op to be a list')
        if not (len(op) == 2):
            raise ValueError('expecting op to be two items')
        if not (isinstance(op[0], int)):
            raise ValueError('expecting op[0] to be integer')

        self.opId = op[0]
        name = OP_NAMES[self.opId]
        self.name = name[0].upper() + name[1:]

        if op[0] == 1:
            self.op = Limit_order_create(op[1])
        if op[0] == 2:
            self.op = Limit_order_cancel(op[1])

    def __bytes__(self):
        print(yellow('GPHOperation.__bytes__'))
        return bytes(Id(self.opId)) + bytes(self.op)

class Signed_Transaction(GrapheneObject):  # merged litepresence2019

    # Bitshares(MIT) graphenebase/signedtransactions.py
    # Bitshares(MIT) bitsharesbase/signedtransactions.py

    def __init__(self, *args, **kwargs):
        print(red('Signed_Transaction'))
        print(
            """ Create a signed transaction and
                offer method to create the signature

            (see ``getBlockParams``)
            :param num refNum: parameter ref_block_num
            :param num refPrefix: parameter ref_block_prefix
            :param str expiration: expiration date
            :param Array operations:  array of operations
        """
        )
        print('args, kwargs', args, kwargs)
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "extensions" not in kwargs:
                kwargs["extensions"] = Array([])
            elif not kwargs.get("extensions"):
                kwargs["extensions"] = Array([])
            if "signatures" not in kwargs:
                kwargs["signatures"] = Array([])
            else:
                kwargs["signatures"] = Array(
                    [Signature(unhexlify(a)) for a in kwargs["signatures"]])

            if "operations" in kwargs:
                opklass = self.getOperationKlass()
                if all([not isinstance(a, opklass)
                        for a in kwargs["operations"]]):
                    kwargs['operations'] = Array(
                        [opklass(a) for a in kwargs["operations"]])
                else:
                    kwargs['operations'] = Array(kwargs["operations"])

            super().__init__(OrderedDict([
                ('ref_block_num', Uint16(kwargs['ref_block_num'])),
                ('ref_block_prefix', Uint32(kwargs['ref_block_prefix'])),
                ('expiration', PointInTime(kwargs['expiration'])),
                ('operations', kwargs['operations']),
                ('extensions', kwargs['extensions']),
                ('signatures', kwargs['signatures']),
            ]))

    @property
    def id(self):
        print('Signed_Transaction.id')
        """
        The transaction id of this transaction
        """
        # Store signatures temporarily
        sigs = self.data["signatures"]
        self.data.pop("signatures", None)
        # Generage Hash of the seriliazed version
        h = sha256(bytes(self)).digest()
        # Recover signatures
        self.data["signatures"] = sigs
        # Return properly truncated tx hash
        return hexlify(h[:20]).decode("ascii")

    def getOperationKlass(self):
        print('Signed_Transaction.get_operationKlass')
        return Operation

    def derSigToHexSig(self, s):
        print('Signed_Transaction.derSigToHexSig')
        s, junk = ecdsa_der.remove_sequence(unhexlify(s))
        if junk:
            log.debug('JUNK: %s', hexlify(junk).decode('ascii'))
        assert(junk == b'')
        x, s = ecdsa_der.remove_integer(s)
        y, s = ecdsa_der.remove_integer(s)
        return '%064x%064x' % (x, y)

    def deriveDigest(self, chain):
        print('Signed_Transaction.deriveDigest')
        print(self, chain)
        # Do not serialize signatures
        sigs = self.data["signatures"]
        self.data["signatures"] = []
        # Get message to sign
        #   bytes(self) will give the wire formated data according to
        #   GrapheneObject and the data given in __init__()
        self.message = unhexlify(ID) + bytes(self)
        self.digest = sha256(self.message).digest()
        # restore signatures
        self.data["signatures"] = sigs

    def verify(self, pubkeys=[], chain="BTS"):
        print(green('###############################################'))
        print('Signed_Transaction.verify')
        print(green('self, pubkeys, chain'), self, pubkeys, chain)

        self.deriveDigest(chain)
        print(green('self'))
        print(self)
        signatures = self.data["signatures"].data
        print(green('signatures'))
        print(signatures)
        pubKeysFound = []

        for signature in signatures:
            p = verify_message(
                self.message,
                bytes(signature)
            )
            phex = hexlify(p).decode('ascii')
            print('')
            print('')
            print(green('phex'))
            print(green(phex))
            print(cyan('len(phex)'), len(str(phex)))
            print('')
            print('')
            pubKeysFound.append(phex)

        for pubkey in pubkeys:

            print(green('for pubkey in pubkeys:'))
            print(green('************ pubkey ************'))
            print(blue('repr(pubkey)'))
            print(repr(pubkey))
            print(cyan('len(pubkey)'), len(str(pubkey)))
            print('')
            if not isinstance(pubkey, PublicKey):
                raise Exception("Pubkeys must be array of 'PublicKey'")

            k = pubkey.unCompressed()[2:]
            print(green('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'))
            print(yellow('k'))
            print(k)
            print(cyan('len(k)'), len(str(k)))
            print(yellow('pubKeysFound'))
            print(pubKeysFound)
            print(cyan('len(pubKeysFound[0])'), len(pubKeysFound[0]))
            print('')
            print(green('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'))

            if k not in pubKeysFound and repr(pubkey) not in pubKeysFound:
                print(
                    blue('if k not in pubKeysFound and repr(pubkey) ' +
                         'not in pubKeysFound:'))
                k = PublicKey(PublicKey(k).compressed())
                f = format(k, 'BTS')  # chain_params["prefix"]) # 'BTS'
                print('')
                print(red('FIXME'))
                raise Exception("Signature for %s missing!" % f)

        return pubKeysFound

    def sign(self, wifkeys, chain="BTS"):
        print('Signed_Transaction.sign')
        """
        Sign the transaction with the provided private keys.
        """
        self.deriveDigest(chain)

        # Get Unique private keys
        self.privkeys = []
        [self.privkeys.append(item)
         for item in wifkeys if item not in self.privkeys]

        # Sign the message with every private key given!
        sigs = []
        for wif in self.privkeys:
            signature = sign_message(self.message, wif)
            sigs.append(Signature(signature))

        self.data["signatures"] = Array(sigs)
        return self

class Limit_order_create(GrapheneObject):  # bitsharesbase/operations.py

    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('seller', ObjectId(kwargs["seller"], "account")),
                ('amount_to_sell', Asset(kwargs["amount_to_sell"])),
                ('min_to_receive', Asset(kwargs["min_to_receive"])),
                ('expiration', PointInTime(kwargs["expiration"])),
                ('fill_or_kill', Uint8(kwargs["fill_or_kill"])),
                ('extensions', Array([])),
            ]))

class Limit_order_cancel(GrapheneObject):  # bitsharesbase/operations.py

    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('fee_paying_account', ObjectId(
                    kwargs["fee_paying_account"], "account")),
                ('order', ObjectId(kwargs["order"], "limit_order")),
                ('extensions', Array([])),
            ]))

def verify_message(message, signature, hashfn=sha256):

    # graphenebase/ecdsa.py stripped of non-secp256k1 methods
    print(red('verify_message...return phex'))
    # require message and signature to be bytes
    if not isinstance(message, bytes):
        message = bytes(message, "utf-8")
    if not isinstance(signature, bytes):
        signature = bytes(signature, "utf-8")

    digest = hashfn(message).digest()
    sig = signature[1:]
    # recover parameter only
    recoverParameter = bytearray(signature)[0] - 4 - 27
    # "bitwise or"; each bit of the output is 0
    # if the corresponding bit of x AND of y is 0, otherwise it's 1
    ALL_FLAGS = (secp256k1_lib.SECP256K1_CONTEXT_VERIFY |
                 secp256k1_lib.SECP256K1_CONTEXT_SIGN)
    # ecdsa.PublicKey with additional functions to serialize
    # in uncompressed and compressed formats
    pub = secp256k1_PublicKey(flags=ALL_FLAGS)
    # recover raw signature
    sig = pub.ecdsa_recoverable_deserialize(sig, recoverParameter)
    # recover public key
    verifyPub = secp256k1_PublicKey(pub.ecdsa_recover(message, sig))
    # convert recoverable sig to normal sig
    normalSig = verifyPub.ecdsa_recoverable_convert(sig)
    # verify
    verifyPub.ecdsa_verify(message, normalSig)
    phex = verifyPub.serialize(compressed=True)

    return phex

def isArgsThisClass(self, args): # graphenebase/objects.py
    # if there is only one argument and its type name is
    # the same as the type name of self
    ret = (len(args) == 1 and
            type(args[0]).__name__ == type(self).__name__)
    return ret

' PRIMARY TRANSACTION BACKBONE '

def build_transaction(order):
    # this performs incoming limit order api conversion
    # from human terms to graphene terms

    # humans speak:
    "account name, asset name, order number"
    "decimal amounts, rounded is just fine"
    "buy/sell/cancel"
    "amount of assets"
    "price in currency"

    # graphene speaks:
    "1.2.x, 1.3.x, 1.7.x"
    "only in integers"
    "create/cancel"
    "min_to_receive/10^receiving_precision"
    "amount_to_sell/10^selling_precision"

    # build_transaction speaks:
    "list of buy/sell/cancel human terms edicts any order in"
    "validated data request"
    "autoscale amounts if out of budget"
    "autoscale amounts if spending last bitshare"
    "bundled cancel/buy/sell transactions out; cancel first"
    "prevent inadvertent huge number of orders"

    global account_id, account_name, currency_id, asset_id
    global currency_precision, asset_precision
    # first we will perform some checks on incoming data format
    if not isinstance(order['edicts'], list):
        raise ValueError('order parameter must be list: %s' % order['edicts'])
    if not isinstance(order['nodes'], list):
        raise ValueError('order parameter must be list: %s' % order['nodes'])
    if not isinstance(order['header'], dict):
        raise ValueError('order parameter must be list: %s' % order['header'])
    # the location of the decimal place must be provided by order
    currency_precision = int(order['header']['currency_precision'])
    asset_precision = int(order['header']['asset_precision'])
    # validate a.b.c identifiers of account id and asset ids
    currency_id = str(order['header']['currency_id']) 
    asset_id = str(order['header']['asset_id'])
    account_id = str(order['header']['account_id'])
    account_name = str(order['header']['account_name'])
    for i in [account_id, currency_id, asset_id]:
        try:
            a,b,c = i.split('.')
            int(a) == 1
            int(b) in [2,3]
            int(c) == float(c)
        except:
            raise ValueError('invalid object id %s' % i)
    # fetch block data via websocket request
    block = rpc_block_number()
    ref_block_num = block["head_block_number"] & 0xFFFF
    ref_block_prefix = unpack_from(
        "<I",
        unhexlify(block["head_block_id"]),
        4)[0]
    #print('block number:', block['head_block_number'], ref_block_num)
    #print('block id    :', block['head_block_id'], ref_block_prefix)
    # fetch fee via websocket request
    fees = rpc_fees()
    # establish transaction expiration
    tx_expiration = to_iso_date(int(time() + 120))
    # initialize tx_operations list
    tx_operations = []
    # sort incoming edicts by type:
    buy_edicts = []
    sell_edicts = []
    cancel_edicts = []
    for edict in order['edicts']:
        if edict['op'] == 'cancel':
            print(yellow(str(edict)))
            cancel_edicts.append(edict)
        elif edict['op'] == 'buy':
            print(yellow(str(edict)))
            buy_edicts.append(edict)
        elif edict['op'] == 'sell':
            print(yellow(str(edict)))
            sell_edicts.append(edict)
    #print('early edicts')
    #edicts = cancel_edicts + buy_edicts + sell_edicts
    #pprint(edicts)
    # append incoming cancel edicts to graphene type tx_operations
    for edict in cancel_edicts:
        if '1.7.X' in edict['ids']: # the "cancel all" signal
            # for cancel all op, we collect all open orders in 1 market
            edict['ids'] = rpc_open_orders()
        for order_id in edict['ids']:
            # confirm it is good 1.7.x format:
            order_id = str(order_id)
            a,b,c = order_id.split('.', 2)
            assert (int(a) == 1)
            assert (int(b) == 7)
            assert (int(c) == float(c) > 0)
            # create cancel fee ordered dictionary
            fee = OrderedDict([
                              ('amount', fees['cancel']),
                              ('asset_id', '1.3.0')
                              ])
            # create ordered operation dicitonary for this edict
            operation = [2, # two means "Limit_order_cancel"
                OrderedDict([
                    ('fee', fee),
                    ('fee_paying_account', account_id),
                    ('order', order_id),
                    ('extensions', [])
            ])]
            # append the dict to the transaction operations list
            tx_operations.append(operation)
    #print('after cancel edicts')
    #edicts = cancel_edicts + buy_edicts + sell_edicts
    #pprint(edicts)
    if AUTOSCALE or BTS_FEES:
        satoshi = 0.00000001
        six_sig = 0.999999
        currency, assets, bitshares = rpc_balances()
        # scale order size to funds on hand
        if AUTOSCALE and len(buy_edicts+sell_edicts) :
            # autoscale buy edicts
            currency_value = 0
            # calculate total value of each amount in the order
            for i in range(len(buy_edicts)):
                currency_value += (buy_edicts[i]['amount'] *
                                    buy_edicts[i]['price'])
            # scale the order amounts to means
            scale = six_sig*currency/(currency_value+satoshi)
            if scale < 1:
                print(yellow('ALERT: scaling buy edicts to means: %.3f' % scale))
                for i in range(len(buy_edicts)):
                    buy_edicts[i]['amount'] *= scale
            # autoscale sell edicts
            asset_total = 0
            # calculate total amount in the order
            for i in range(len(sell_edicts)):
                asset_total += sell_edicts[i]['amount']
            scale = six_sig*assets/(asset_total+satoshi)
            # scale the order amounts to means
            if scale < 1:
                print(yellow('ALERT: scaling sell edicts to means: %.3f' % scale))
                for i in range(len(sell_edicts)):
                    sell_edicts[i]['amount'] *= scale
        #print('after autoscale edicts')
        #edicts = cancel_edicts + buy_edicts + sell_edicts
        #pprint(edicts)
        # always save our last 2 Bitshares for fees !!!
        if BTS_FEES and (len(buy_edicts+sell_edicts) 
                and ('1.3.0' in [asset_id, currency_id])):
            #print(bitshares, 'BTS balance')
            # when BTS is the currency don't spend the last 2
            if currency_id == '1.3.0':
                bts_value = 0
                # calculate total bts value of each amount in the order
                for i in range(len(buy_edicts)):
                    bts_value += (buy_edicts[i]['amount'] *
                                  buy_edicts[i]['price'])
                # scale the order amounts to save last two bitshares
                scale = six_sig*max(0,(bitshares-2.01))/(bts_value+satoshi)
                if scale < 1:
                    print(yellow('ALERT: scaling buy edicts for fees: %.4f' % scale))
                    for i in range(len(buy_edicts)):
                        buy_edicts[i]['amount'] *= scale
            # when BTS is the asset don't sell the last 2
            if asset_id == '1.3.0':
                bts_total = 0
                # calculate total of each bts amount in the order
                for i in range(len(sell_edicts)):
                    bts_total += sell_edicts[i]['amount']
                scale = six_sig*max(0,(bitshares-2.01))/(bts_total+satoshi)
                # scale the order amounts to save last two bitshares
                if scale < 1:
                    print(yellow('ALERT: scaling sell edicts for fees: %.4f' % scale))
                    for i in range(len(sell_edicts)):
                        sell_edicts[i]['amount'] *= scale
    #print('after bts fee edicts')
    #edicts = cancel_edicts + buy_edicts + sell_edicts
    #pprint(edicts)
    # after scaling recombine buy and sell 
    create_edicts = buy_edicts+sell_edicts
    # remove dust edicts
    if DUST:
        ce = []
        dust = DUST*100000/10**asset_precision
        for i in range(len(create_edicts)):
            if create_edicts[i]['amount'] > dust:
                ce.append(create_edicts[i])
            else:
                print(red('WARN: removing dust threshold %s order from edicts' % dust), create_edicts[i])
        create_edicts = ce[:] # copy as new list
        del ce
    #print('after bts fee edicts')
    #edicts = cancel_edicts + buy_edicts + sell_edicts
    #pprint(edicts)
    # port incoming create edicts to Limit_order_create objects
    for i in range(len(create_edicts)):
        price = decimal(create_edicts[i]['price'])
        amount = decimal(create_edicts[i]['amount'])
        op_exp = int(create_edicts[i]['expiration'])
        # convert zero expiration flag to "really far in future"
        if op_exp == 0:
            op_exp = END_OF_TIME
        op_expiration = to_iso_date(op_exp)
        # we'll use ordered dicts and put items in api specific order
        min_to_receive = OrderedDict({})
        amount_to_sell = OrderedDict({})
        # derive min_to_receive & amount_to_sell from price & amount
        # means SELLING currency RECEIVING assets
        if create_edicts[i]['op'] == 'buy':
            min_to_receive['amount'] = int(amount *
                                           10 ** asset_precision)
            min_to_receive['asset_id'] = asset_id

            amount_to_sell['amount'] = int(amount * price *
                                           10 ** currency_precision)
            amount_to_sell['asset_id'] = currency_id
        # means SELLING assets RECEIVING currency
        if create_edicts[i]['op'] == 'sell':
            min_to_receive['amount'] = int(amount * price *
                                           10 ** currency_precision)
            min_to_receive['asset_id'] = currency_id

            amount_to_sell['amount'] = int(amount *
                                           10 ** asset_precision)
            amount_to_sell['asset_id'] = asset_id
        # Limit_order_create fee ordered dictionary
        fee = OrderedDict([
                          ('amount', fees['create']),
                          ('asset_id', '1.3.0')
                          ])
        # create ordered dicitonary from each buy/sell operation
        operation = [1,
            OrderedDict([
                ('fee', fee),  # OrderedDict
                ('seller', account_id),  # "a.b.c"
                ('amount_to_sell', amount_to_sell),  # OrderedDict
                ('min_to_receive', min_to_receive),  # OrderedDict
                ('expiration', op_expiration),  # ISO8601
                ('fill_or_kill', KILL_OR_FILL),  # bool
                ('extensions', [])  # always empty list for our purpose
        ])]
        tx_operations.append(operation)

    # prevent inadvertent huge number of orders
    tx_operations = tx_operations[:LIMIT]
    # the tx is just a regular dictionary we will convert to json later
    # the operations themselves are still an OrderedDict

    tx = {'ref_block_num': ref_block_num,
          'ref_block_prefix': ref_block_prefix,
          'expiration': tx_expiration,
          'operations': tx_operations,
          'signatures': [],
          'extensions': []
          }

    return tx

def serialize_transaction(tx):

    if tx['operations'] == []:
        return tx, b""

    # gist.github.com/xeroc/9bda11add796b603d83eb4b41d38532b
    print(blue('serialize_transaction'))
    print(yellow('IF WE DO EVERYTHING RIGHT:'))
    print(green('rpc_tx_hex = manual_tx_hex'))
    # RPC call for ordered dicts which are dumped by the query
    print(yellow('get RPC tx hex...'))
    rpc_tx_hex = rpc_get_transaction_hex_without_sig(tx)
    print(yellow('build manual tx hex...'))
    buf = b"" # create an empty byte string buffer
    # add block number, prefix, and tx expiration to the buffer
    buf += pack("<H", tx["ref_block_num"]) # 2 byte int
    buf += pack("<I", tx["ref_block_prefix"]) # 4 byte int
    buf += pack("<I", from_iso_date(tx['expiration'])) # 4 byte int
    # add length of operations list to buffer
    buf += bytes(varint(len(tx["operations"])))
    # add the operations list to the buffer in graphene type fashion
    for op in tx["operations"]:
        # print(op[0])  # Int (1=create, 2=cancel)
        # print(op[1])  # OrderedDict of operations
        buf += varint(op[0])
        if op[0] == 1:
            buf += bytes(Limit_order_create(op[1]))
        if op[0] == 2:
            buf += bytes(Limit_order_cancel(op[1]))
    # add legth of (empty) extensions list to buffer
    buf += bytes(varint(len(tx["extensions"]))) # effectively varint(0)
    # this the final manual transaction hex, which should match rpc
    manual_tx_hex = hexlify(buf)
    print(red('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'))
    print('   rpc_tx_hex:  ', rpc_tx_hex)
    print('manual_tx_hex:  ', manual_tx_hex)
    print(red('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'))
    print(yellow('assert (rpc_tx_hex == manual_tx_hex)'))
    assert(rpc_tx_hex == manual_tx_hex), "Serialization Failed"
    print(green('Serialization Success'))
    # prepend the chain ID to the buffer to create final serialized msg
    message = unhexlify(ID) + buf
    return tx, message

def sign_transaction(tx, message):

    # graphenebase/ecdsa.py
    # tools.ietf.org/html/rfc6979
    # @xeroc/steem-transaction-signing-in-a-nutshell
    # @dantheman/steem-and-bitshares-cryptographic-security-update

    # deterministic signatures retain the cryptographic 
    # security features associated with digital signatures
    # but can be more easily implemented
    # since they do not need high-quality randomness

    # 1 in 4 signatures are randomly canonical; "normal form"
    # using the other three causes vulnerability to maleability attacks
    # as a metaphor; "require reduced fractions in simplest terms"
    def canonical(sig):  
        sig = bytearray(sig)
        # 0x80 hex = 10000000 binary = 128 integer
        ret = (not (int(sig[0]) & 0x80) and
               not (sig[0] == 0 and not (int(sig[1]) & 0x80)) and
               not (int(sig[32]) & 0x80) and
               not (sig[32] == 0 and not (int(sig[33]) & 0x80)))
        print(green('canonical'), cyan(str(ret)))
        print(sig)
        return ret # true/false
    # create fixed length representation of arbitrary length data
    # this will thoroughly obfuscate and compress the transaction
    # signing large data is computationally expensive and time consuming
    # the hash of the data is a relatively small
    # signing hash is more efficient than signing serialization
    digest = sha256(message).digest()
    print(digest)
    '''
    ECDSA
    eliptical curve digital signature algorithm
    this is where the real hocus pocus lies
    all of the ordering, typing, serializing, and digesting
    culminates with the message meeting the wif 
    '''
    # 8 bit string representation of private key
    p = bytes(PrivateKey(wif))
    # create some arbitrary data used by the nonce generation
    ndata = secp256k1_ffi.new("const int *ndata")
    ndata[0] = 0 # it adds "\0x00", then "\0x00\0x00", etc..
    while 1: # repeat process until deterministic and cannonical  
        ndata[0] += 1 # increment the arbitrary nonce
        # obtain compiled/binary private key from the WIF
        privkey = secp256k1_PrivateKey(p, raw=True)
        print(red(str(privkey)))
        print(privkey)
        # create a new recoverable 65 byte ECDSA signature
        sig = secp256k1_ffi.new(
            'secp256k1_ecdsa_recoverable_signature *')
        # parse a compact ECDSA signature (64 bytes + recovery id)
        # returns: 1 = deterministic; 0 = not deterministic
        deterministic = (
            secp256k1_lib.secp256k1_ecdsa_sign_recoverable(
                privkey.ctx, # initialized context object
                sig, # array where signature is held
                digest, # 32-byte message hash being signed
                privkey.private_key, # 32-byte secret key
                secp256k1_ffi.NULL, # default nonce function
                ndata # incrementing nonce data
        ))
        if not deterministic:
            print('not deterministic, try again...')
            continue 
        # we derive the recovery paramter
        # which simplifies the verification of the signature
        # it links the signature to a single unique public key
        # without this parameter, the back-end would need to test
        # for multiple public keys instead of just one
        signature, i = privkey.ecdsa_recoverable_serialize(sig)
        # we ensure that the signature is canonical; simplest form
        if canonical(signature):
            # add 4 and 27 to stay compatible with other protocols
            i += 4   # compressed
            i += 27  # compact
            # and have now obtained our signature
            break
    # having derived a valid canonical signature
    # we format it in its hexadecimal representation
    # and add it our transactions signatures
    # note that we do not only add the signature
    # but also the recover parameter
    # this kind of signature is then called "compact signature"
    signature = hexlify(
        pack("<B", i) + signature
    ).decode("ascii")
    tx["signatures"].append(signature)
    print(blue('tx["signatures"].append(signature)'))
    print(signature)
    print('')

    return tx 

def verify_transaction(tx):
    # gist.github.com/xeroc/9bda11add796b603d83eb4b41d38532b
    # once you have derived your new tx including the signatures
    # verify your transaction and it's signature 
    print(blue('verify_transaction'))
    print(blue('tx2 = Signed_Transaction(**tx)'))
    tx2 = Signed_Transaction(**tx)
    print(tx2)

    print(blue('tx2.deriveDigest("BTS")'))
    tx2.deriveDigest("BTS")

    print(blue('pubkeys = [PrivateKey(wif).pubkey]'))
    pubkeys = [PrivateKey(wif).pubkey]
    print(pubkeys)

    print(blue('tx2.verify(pubkeys, "BTS")'))
    tx2.verify(pubkeys, "BTS")

    return tx

' THE BROKER METHOD'

def broker(order):

    'broker(order) --> execute(signal, order)'
    # insistent timed multiprocess wrapper for authorized ops
    # covers all incoming buy/sell/cancel authenticated requests
    # if command does not execute in time: terminate and respawn
    # serves to force disconnect websockets if hung
    "up to ATTEMPTS chances; each PROCESS_TIMEOUT long: else abort"
    # signal is switched to 0 after execution to end the process

    global_constants()
    global_variables()
    control_panel()

    signal = Value('i', 1)
    i = 0
    while signal.value and (i < ATTEMPTS):
        i += 1
        print('')
        print('manualSIGNING authentication attempt:', i, ctime())
        child = Process(target=execute, args=(signal, order))
        child.daemon = False
        child.start()
        if JOIN: # means main script will not continue till child done
            child.join(PROCESS_TIMEOUT)
        print('')

def execute(signal, order):
    global nodes, account_id, account_name, wif


    start = time()
    if not DEV: # disable printing with DEV=False
        blockPrint()
    nodes = order['nodes']
    account_id = order['header']['account_id']
    account_name = order['header']['account_name']
    wif = order['header']['wif']
    wss_handshake()
    if not DEV:
        enablePrint()
    try:
        tx = build_transaction(order)
    except Exception as e:
        trace(e)
    if len(tx['operations']): # if there are any orders
        if not DEV: # disable printing with DEV=False
            blockPrint()
        # perform ecdsa on serialized transaction
        tx, message = serialize_transaction(tx)
        signed_tx = sign_transaction(tx, message)
        signed_tx = verify_transaction(signed_tx)
        if not DEV:
            enablePrint()
        broadcasted_tx = rpc_broadcast_transaction(signed_tx)
    else:
        print(red('manualSIGNING rejected your order'), order['edicts'])
    print('manualSIGNING process elapsed: %.3f sec' %
            (time() - start))
    print('')
    signal.value = 0

def prototype_order():

    '''
    # included for example only!
    # in production use this method with Bitshares_Trustless_Client()
    # creates an auto formatted empty prototype order in json format
    # you will need to add your ['edicts'] key

    proto = {}
    metaNODE = Bitshares_Trustless_Client()
    proto['op'] = ''
    proto['nodes'] = metaNODE['whitelist']
    proto['header'] = {}
    proto['header']['wif'] = WIF # use python getpass() at login 
    proto['header']['asset_id'] = metaNODE['asset_id']
    proto['header']['currency_id'] = metaNODE['currency_id']
    proto['header']['asset_precision'] = metaNODE['asset_precision']
    proto['header']['currency_precision'] = metaNODE['currency_precision']
    proto['header']['account_id'] = metaNODE['account_id']
    proto['header']['account_name'] = metaNODE['account_name']
    del metaNODE
    return json_dumps(proto)
    '''

' IN SCRIPT DEMONSTRATION '

def log_in():

    global wif, account_name, account_id
    global order, order1, order2, order3, nodes

    print("\033c") # clear terminal
    # bitshares ascii logo encoded and compressed
    b = b'x\x9c\xad\xd4M\n\xc4 \x0c\x05\xe0}O1P\x12B\x10\xbc\x82\xf7?\xd5\xf8\xaf\x83F\xe3\xe0[t\xf9\xf5%\xda>\x9f\x1c\xf7\x7f\x9e\xb9\x01\x17\x0cc\xec\x05\xe3@Y\x18\xc6(\'Z\x1a\xca.\x1bC\xa5l\r\x85\xa20\xb6\x8a\xca\xd8,W0\xec\x05\xc3\xdf\xd4_\xe3\r\x11(q\x16\xec\x95l\x04\x06\x0f\x0c\xc3\xddD\x9dq\xd2#\xa4NT\x0c/\x10\xd1{b\xd4\x89\x92\x91\x84\x11\xd9\x9d-\x87.\xe4\x1cB\x15|\xe0\xc8\x88\x13\xa5\xbc\xd4\xa21\x8e"\x18\xdc\xd2\x0e\xd3\xb6\xa0\xc6h\xa3\xd4\xde\xd0\x19\x9a\x1e\xd8\xddr\x0e\xcf\xf8n\xe0Y\rq\x1fP:p\x92\xf2\xdbaB,v\xda\x84j\xc4.\x03\xb1>\x97\xee{\x99oSa\x00\x0f\xc6\x84\xd8\xdf\x0f\xb4e\xa7$\xfdE\xae\xde\xb1/\x1d\xfc\x96\x8a'
    print(cyan(decompress(b).decode()))
    print(green('                                       y**2 = x**3 + 7'))
    print('************************************************************')
    print('')
    print(green(' manualSIGNING - BUY/SELL/CANCEL OPS v%.8f alpha' % VERSION))
    print('')
    print('************************************************************')
    print('')
    print('             given a buy/sell/cancel order and wif:')
    print('                  convert to graphene terms')
    print('                  serialize the transaction')
    print('                       perform ECDSA')
    print('                  broadcast to a public node')
    print('               use only standard python modules')
    print('              spell the rest out here concisely')
    print('')
    print('           if you input name and wif this script will:')
    print('')
    print(red('          BUY 10 BTS with OPEN.BTC at 0.00000100'))
    print('')
    print(green("              WITHOUT IMPORTING PYBITSHARES "))
    print('')
    print('enter account name (press ENTER for demo)')
    print('')
    account_name = input('account name: ')
    print('')
    print('lookup account_id...')
    print('')
    if account_name == '':
        account_name = 'fd'  # some random acct
        print('using mock account for demo: %s' % account_name)
    nodes = order1['nodes']
    # create a websocket connection
    wss_handshake()
    # convert account name to id via rpc request
    account_id = rpc_account_id()
    print(account_id)
    print('')
    # input wallet import format key for authentication
    wif = getpass(prompt='enter wif (press ENTER for demo): ')
    if not wif:
        # some random wif
        wif = "5JLw5dgQAx6rhZEgNN5C2ds1V47RweGshynFSWFbaMohsYsBvE8"
        print('using sample wallet import format (wif)')
        print(wif)
        print('')
        print(green('BEGIN DEMO'))
        print('')
    # add wif, account_id, and account_name to sample order headers
    order1['header']['wif'] = wif
    order1['header']['account_id'] = account_id
    order1['header']['account_name'] = account_name
    order2['header']['wif'] = wif
    order2['header']['account_id'] = account_id
    order2['header']['account_name'] = account_name
    order3['header']['wif'] = wif
    order3['header']['account_id'] = account_id
    order3['header']['account_name'] = account_name
    print(' 1:buy, 2:sell, 3:cancel ')
    select = 0
    while select not in [1,2,3]:
        select = int(input('1, 2, or 3? '))
    if select == 1:
        order = order1
    if select == 2:
        order = order2
    if select == 3:
        order = order3

def demo():

    # this is the backbone of events for the demo
    '''
    receive order
    build graphene transaction
    serialize transaction
    sign transaction
    verify transaction
    broadcast transaction
    '''

    try:
        print(purple('======================================'))
        print(purple('receive order                         '))
        print(purple('======================================'))
        pprint(order)
        print('')
    except Exception as e:
        trace(e)

    try:
        print(purple('======================================'))
        print(purple('build graphene transaction from order '))
        print(purple('======================================'))
        tx = build_transaction(order)
        pprint(tx)
        print('')
    except Exception as e:
        trace(e)
    if len(tx['operations']):
        try:
            print(purple('======================================'))
            print(purple('serialize transaction bytes string    '))
            print(purple('======================================'))
            tx, message = serialize_transaction(tx)
            pprint(tx)
            print('')
        except Exception as e:
            trace(e)

        try:
            print(purple('======================================'))
            print(purple('sign transaction with wif             '))
            print(purple('======================================'))
            signed_tx = sign_transaction(tx, message)
            pprint(signed_tx)
            print('')
        except Exception as e:
            trace(e)

        try:
            print(purple('======================================'))
            print(purple('verify the signature on transaction   '))
            print(purple('======================================'))
            signed_tx = verify_transaction(signed_tx)
            pprint(signed_tx)
            print('')
        except Exception as e:
            trace(e)

        try:
            print(purple('======================================'))
            print(purple('broadcast transaction                 '))
            print(purple('======================================'))
            broadcasted_tx = rpc_broadcast_transaction(signed_tx)
            pprint(broadcasted_tx)
            print('')
        except Exception as e:
            trace(e)
    else:
        print('no operations to broadcast')

    try:
        ws.close()
        print(purple('connection terminated'))
    except Exception as e:
        trace(e)
    print('')
    print('END')

def main():

    sample_orders() 
    global_constants()
    global_variables()
    control_panel()
    log_in()
    demo()

if __name__ == "__main__":

    main()

