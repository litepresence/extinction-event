"""
Normalized Buy, Sell, Cancel, Open Orders, Balances

Binance, Poloniex, Bitfinex, Bittrex, Coinbase, Kraken

litepresence.com 2019
"""

#NOTE: THIS WAS WRITTEN FROM API DOCS WITHOUT LIVE TESTING    
#NOTE: set DETAIL and SANDBOX to False for live trading
#NOTE: toolkit rounds to limit error handling and may be off by dust amount

raise NotImplementedError("WARNING: PRE ALPHA - NOT LIVE TESTED")

# STANDARD MODULES
import os
import time
import hmac
import hashlib
from pprint import pprint
from json import dumps as json_dumps 
from base64 import b64decode, b64encode
from multiprocessing import Process, Value

# THIRD PARTY MODULES
from urllib.parse import urlencode
import requests

# EXTINCTION EVENT MODULES
from public_cex import race_write, race_read_json
from public_cex import symbol_syntax

# GLOBAL USER DEFINED CONSTANTS
TIMEOUT = 30
ATTEMPTS = 10
PATH = str(os.path.dirname(os.path.abspath(__file__))) + "/"
DETAIL = False
SANDBOX = False

def about():
    
    # USAGE:    
    # 
    # from private_cex import get_orders, get_balances, post_order, cancel
    #
    # get_orders(api)          # your open orders in market
    # get_balances(api)        # your asset and currency balances in market
    # cancel(api)              # cancel all in market
    # cancel(api, order_ids)   # cancel string or list of strings
    # post_order(api, side, quantity, price)    # "buy" and "sell"
    #
    
    """
    "api" is a dictionary that travels through the script gathering k:v
    ending with a properly formatted authenticated https request
    the script is organized first by remote procedure; then by exchange
    all external requests are multiprocess wrapped for durability
    open order and balances are normalized when returned
    cancel and post orders are returned raw
    
    USER PROVIDES:
    
    api['key']          # public key from exchange
    api['secret']       # private key from exchange
    api['passphrase']   # some exchanges also provide passphrase else ""
    api['exchange']     # name of exchange; ie "binance"
    api['symbol']       # market pair symbol in format BTC:USD
    
    SCRIPT BUILDS request(api, params) SPECIFIC:
    
    api['nonce']        # time.time() at beginning of request
    api['url']          # https://...xyz.com
    api['endpoint']     # path/to/server/resource
    api['method']       # GET, POST, or DELETE
    api['params']       # dict with request specific parameters
    api['data']         # str with request specific parameters
    api['headers']      # contains authentication signature
    
    REFERENCE:
    
    https://bittrex.github.io/api/v1-1
    https://github.com/ericsomdahl/python-bittrex/blob/master/bittrex
    https://github.com/veox/python3-krakenex/blob/master/krakenex
    https://docs.bitfinex.com/docs/rest-auth
    https://github.com/scottjbarr/bitfinex/blob/develop/bitfinex/client.py
    https://github.com/bitfinexcom/bitfinex-api-py  
    
    KNOWN BUGS:
    
    No error handling    
    Only Coinbase is live tested with funds
    """
    
    print(about.__doc__)


def lookup_url(api):
    """
    add url key to api dict given exchange
    """
    if SANDBOX:
        urls = {
            # get keys at https://public.sandbox.pro.coinbase.com/
            "coinbase": "https://api-public.sandbox.pro.coinbase.com",
            "poloniex": "WARN_NO_SANDBOX",
            "binance": "WARN_NO_SANDBOX",
            "bitfinex": "WARN_NO_SANDBOX",
            "kraken": "WARN_NO_SANDBOX",
            "bittrex": "WARN_NO_SANDBOX",
        }
    else:
        urls = {
            "coinbase": "https://api.pro.coinbase.com",
            "poloniex": "https://www.poloniex.com",
            "binance": "https://api.binance.com",
            "bitfinex": "https://api.bitfinex.com",
            "kraken": "https://api.kraken.com",
            "bittrex": "https://api.bittrex.com",
        }
    api["url"] = urls[api["exchange"]]
    return api


def signed_request(api, signal):
    """
    Remote procedure call for authenticated exchange operations
    api         : dict with keys for building external request
    signal      : multiprocessing completion relay
    """
    api = lookup_url(api)
    api["data"] = ""
    if api["exchange"] == "coinbase":
        api["data"] = json_dumps(api["params"]) if api["params"] else ""
        api["params"] = None
        message = (
            str(api["nonce"]) + api["method"] + api["endpoint"] + api["data"]
        ).encode("ascii")
        secret = b64decode(api["secret"])
        signature = hmac.new(secret, message, hashlib.sha256).digest()
        signature = b64encode(signature).decode("utf-8")
        api["headers"] = {
            "Content-Type": "Application/JSON",
            "CB-ACCESS-SIGN": signature,
            "CB-ACCESS-TIMESTAMP": str(api["nonce"]),
            "CB-ACCESS-KEY": api["key"],
            "CB-ACCESS-PASSPHRASE": api["passphrase"],
        }
    elif api["exchange"] == "poloniex":
        api["params"]["nonce"] = int(api["nonce"] * 1000)
        message = urlencode(api["params"]).encode("utf-8")
        secret = api["secret"].encode("utf-8")
        signature = hmac.new(secret, message, hashlib.sha512).hexdigest()
        api["headers"] = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Key": api["key"],
            "Sign": signature,
        }
    elif api["exchange"] == "binance":
        api["params"]["timestamp"] = int(api["nonce"] * 1000)
        api["params"]["signature"] = signature
        message = urlencode(api["params"].items()).encode("utf-8")
        secret = bytes(api["secret"].encode("utf-8"))
        signature = hmac.new(secret, message, hashlib.sha256).hexdigest()
        api["headers"] = {"X-MBX-APIKEY": api["key"]}
    elif api["exchange"] == "bittrex":
        api["params"]["apikey"] = api["key"]
        api["params"]["nonce"] = int(api["nonce"] * 1000)
        message = api["url"] + api["endpoint"] + urlencode(api["params"])
        message = bytearray(message, "ascii")
        secret = bytearray(api["secret"], "ascii")
        signature = hmac.new(secret, message, hashlib.sha512).hexdigest()
        api["headers"] = {}
    elif api["exchange"] == "kraken":
        api["data"] = api["params"][:]
        api["params"] = {}
        data["nonce"] = int(1000 * api["nonce"])
        api["endpoint"] = "/2.1.0/private/" + api["endpoint"]
        message = (str(data["nonce"]) + urlencode(data)).encode("ascii")
        message = api["endpoint"].encode("ascii") + hashlib.sha256(message).digest()
        secret = b64decode(api["secret"])
        signature = b64encode(hmac.new(secret, message, hashlib.sha512).digest())
        api["headers"] = {
            "User-Agent": "krakenex/2.1.0",
            "API-Key": api["key"],
            "API-Sign": signature,
        }
    elif api["exchange"] == "bitfinex":
        nonce = str(int(api["nonce"] * 1000))
        api["endpoint"] = path = "v2/auth/r/orders"
        api["data"] = json.dumps(api["params"])
        api["params"] = {}
        message = ("/api/" + api["endpoint"] + nonce + api["data"]).encode("utf8")
        secret = api["secret"].encode("utf8")
        signature = hmac.new(secret, message, hashlib.sha384).hexdigest()
        api["headers"] = {
            "bfx-nonce": nonce,
            "bfx-apikey": api["key"],
            "bfx-signature": signature,
            "content-type": "application/json",
        }
        
    #I can do this to tag the work?  hmm?  maybe...
    api['headers']['User-Agent'] = "extinctionEVENT litepresence.com"  
    
    url = api["url"] + api["endpoint"]
    ret = requests.request(
        method=api["method"],
        url=url,
        data=api["data"],
        params=api["params"],
        headers=api["headers"],
    )
    response = ret.json()
    if DETAIL:
        pprint(api)
        print("ret           ", ret)
        print("ret json      ", response)
        print("ret method    ", ret.request.method)
        print("ret url       ", ret.request.url)
        print("ret endpoint  ", ret.request.path_url)
        print("ret body      ", ret.request.body)
        print("ret headers   ", ret.request.headers)
    doc = str(int(api["nonce"])) + "_{}_private.txt".format(api["exchange"])
    race_write(doc, json_dumps(response))
    # signal multiprocessing handler to terminate
    signal.value = 1


def process_request(api):
    """
    Multiprocessing Durability Wrapper for External Requests
    interprocess communication via durable text pipe
    """
    begin = time.time()
    # multiprocessing completion signal
    signal = Value("i", 0)
    # several iterations of external requests until satisfied with response
    i = 0
    while (i < ATTEMPTS) and not signal.value:
        # multiprocessing text file name nonce
        api["nonce"] = time.time()
        i += 1
        print("")
        print("{} {} PRIVATE attempt:".format(api["exchange"],api["symbol"]), i, time.ctime(), int(time.time()))
        child = Process(target=signed_request, args=(api, signal))
        child.daemon = False
        child.start()
        child.join(TIMEOUT)
        child.terminate()
        time.sleep(i ** 2)
    # the doc was created by the subprocess; read and destroy it
    doc = str(int(api["nonce"])) + "_{}_private.txt".format(api["exchange"])
    data = race_read_json(doc)
    path = PATH + "pipe/"
    if os.path.isfile(path + doc):
        os.remove(path + doc)
    print(
        "{} {} PRIVATE elapsed:".format(api["exchange"],api["symbol"]), ("%.2f" % (time.time() - begin))
    )
    print("")
    return data


def get_balances(api):
    """
    Normalized external requests for balances in market
    """
    if DETAIL:
        print(get_balances.__doc__, api["symbol"])
    else:
        print('\nGet Balances', api["symbol"])
    asset, currency = api["symbol"].split(":")
    balances = {"asset": asset, "currency": currency}
    
    
    
    
    # format remote procedure call to exchange api standards
    if api["exchange"] == "coinbase":
        api["endpoint"] = "/accounts/"
        api["params"] = {}
        api["method"] = "GET"
    elif api["exchange"] == "poloniex":
        api["endpoint"] = "/tradingApi"
        api["params"] = {"command": "returnCompleteBalances"}
        api["method"] = "POST"
    elif api["exchange"] == "binance":
        api["endpoint"] = "/api/v3/account"
        api["params"] = {}
        api["method"] = "GET"
    elif api["exchange"] == "bittrex":
        api["endpoint"] = "/api/v1.1/account/getbalances"
        api["params"] = {}
        api["method"] = "GET"
    elif api["exchange"] == "kraken":
        api["endpoint"] = "/0/private/Balance"
        api["params"] = {}
        api["method"] = "GET"
    elif api["exchange"] == "bitfinex":
        api["endpoint"] = "/auth/r/wallets"
        api["params"] = {}
        api["method"] = "POST"
    # make external call
    ret = process_request(api)
    # format json response to extinctionEVENT standard dictionary
    if api["exchange"] == "coinbase":
        # [{'currency': 'BTC', 'balance': '0.0', 'available': '0.0', 'hold': '0.0',
        # 'id': 'abc', 'profile_id': 'xyz', 'trading_enabled': True},...]
        asset_account = [i for i in ret if i["currency"] == asset][0]
        currency_account = [i for i in ret if i["currency"] == currency][0]
        balances = {
            "asset_total": float(asset_account["balance"]),
            "asset_free": float(asset_account["available"]),
            "asset_tied": float(asset_account["hold"]),
            "currency_total": float(currency_account["balance"]),
            "currency_free": float(currency_account["available"]),
            "currency_tied": float(currency_account["hold"]),
        }
    elif api["exchange"] == "poloniex":
        # {'BTC': { available: '0.0',  onOrders: '0.0', btcValue: '0.0' },...}
        balances = {
            "asset_free": float(ret[asset]["available"]),
            "asset_tied": float(ret[asset]["onOrders"]),
            "currency_free": float(ret[currency]["available"]),
            "currency_tied": float(ret[currency]["onOrders"]),
        }
        balances["asset_total"] = balances["currency_free"] + balances["currency_tied"]
        balances["currency_total"] = balances["asset_free"] + balances["asset_tied"]
    elif api["exchange"] == "binance":
        # {"balances": [{"asset": "BTC", "free": "0.0", "locked": "0.0" },...]}
        ret = ret["balances"]
        asset_account = [i for i in ret if i["asset"] == asset][0]
        currency_account = [i for i in ret if i["asset"] == currency][0]
        balances = {
            "asset_free": float(ret[asset]["free"]),
            "asset_tied": float(ret[asset]["locked"]),
            "currency_free": float(ret[currency]["free"]),
            "currency_tied": float(ret[currency]["locked"]),
        }
        balances["asset_total"] = balances["currency_free"] + balances["currency_tied"]
        balances["currency_total"] = balances["asset_free"] + balances["asset_tied"]
    elif api["exchange"] == "bittrex":
        # "result": [{"Currency": "BTC","Balance": 0.0, "Available": 0.0},...]}
        ret = ret["result"]
        asset_account = [i for i in ret if i["currency"] == asset][0]
        currency_account = [i for i in ret if i["currency"] == currency][0]
        ask = float(asset_account["Balance"]) - float(asset_account["Available"])
        bid = float(currency_account["Balance"]) - float(currency_account["Available"])
        balances = {
            "asset_total": float(asset_account["Balance"]),
            "asset_free": float(asset_account["Available"]),
            "asset_tied": ask,
            "currency_total": float(currency_account["balance"]),
            "currency_free": float(currency_account["available"]),
            "currency_tied": bid,
        }

    elif api["exchange"] == "kraken":
        # kraken has a deeply nested balances dictionary
        ret = ret["accounts"]["cash"]["balances"]
        balances = {
            "asset_total": ret[asset.lower()],
            "currency_total": ret[currency.lower()],
            
        }
        # and once you get there it lacks "free" balances
        # {"accounts":{"cash":{"balances":{"xbt":0,...}}}}
        # we fix this with a 2nd call to open orders 
        api["params"] = {}
        api["endpoint"] = "/0/private/OpenOrders"
        api["method"] = "GET"
        ret = get_orders(api)
        kraken_ask_sum = ret["ask_sum"]
        # bid sum will need to derived in currency terms
        kraken_bid_sum = 0
        for i in ret['bids']:
            kraken_bid_sum += (i["price"]*i["current_qty"])  
        kraken_bid_sum *= 1.000001 # account for available conservatively        
        kraken_ask_sum = min(kraken_ask_sum, balances['asset_total'])
        kraken_bid_sum = min(kraken_bid_sum, balances['currency_total'])        
        balances["asset_tied"] = kraken_ask_sum,
        balances["currency_tied"] = kraken_bid_sum,
        balances["asset_free"] = balances["asset_total"] - kraken_ask_sum
        balances["currency_free"] = balances["currency_total"] - kraken_bid_sum

    elif api["exchange"] == "bitfinex":
        # bitfinex uses a unique list of lists format that must be indexed
        # [[WALLET_TYPE, CURRENCY, BALANCE, UNSETTLED_INTEREST, BALANCE_AVAILABLE],...]
        asset_account = [i for i in ret if i[1] == asset][0]
        currency_account = [i for i in ret if i[1] == currency][0]
        ask = float(asset_account[2]) - float(asset_account[4])
        bid = float(currency_account[2]) - float(currency_account[4])
        balances = {
            "asset_total": float(asset_account[2]),
            "asset_free": float(asset_account[4]),
            "asset_tied": ask,
            "currency_total": float(currency_account[2]),
            "currency_free": float(currency_account[4]),
            "currency_tied": bid,
        }
    return balances


def get_orders(api):
    """
    Normalized external requests for open orders in one market
    {'asset_total': 0.0, 'asset_free': 0.0, 'asset_tied': 0.0, 
    'currency_total': 0.0, 'currency_free': 0.0, 'currency_tied': 0.0}

    """
    if DETAIL:
        print(get_orders.__doc__, api["symbol"])
    else:
        print('\nGet Orders', api["symbol"])
    # format remote procedure call to exchange api standards
    symbol = symbol_syntax(api["exchange"], api["symbol"])
    if api["exchange"] == "poloniex":
        api["params"] = {"command": "returnOpenOrders", "currencyPair": api["symbol"]}
        api["endpoint"] = "/tradingApi"
        api["method"] = "POST"
    elif api["exchange"] == "binance":
        api["params"] = {"symbol": api["symbol"]}
        api["endpoint"] = "/api/v3/openOrders"
        api["method"] = "GET"
    elif api["exchange"] == "bittrex":
        api["params"] = {"market": api["symbol"]}
        api["endpoint"] = "/market/getopenorders"
        api["method"] = "GET"
    elif api["exchange"] == "kraken":
        api["params"] = {}
        api["endpoint"] = "/0/private/OpenOrders"
        api["method"] = "GET"
    elif api["exchange"] == "bitfinex":
        api["params"] = {}
        api["endpoint"] = "/v1/orders"
        api["method"] = "GET"
    elif api["exchange"] == "coinbase":
        api["endpoint"] = "/orders"
        api["params"] = {"product_id": api["symbol"]}
        api["method"] = "GET"

    # make external call
    ret = process_request(api)
    # format response to extinctionEVENT standards
    bids = []
    asks = []
    bid_sum = 0
    ask_sum = 0
    # bittrex nests the response in a results key
    if api["exchange"] == "bittrex":
        ret = ret["result"]
    # normalize all our open orders in this market
    for order in ret:
        normalized_order = {}
        # coinbase/kraken/binance do not provide current quantity  
        if api["exchange"] in ["coinbase", "binance", "kraken"]:
            if api["exchange"] == "coinbase":
                    order_type = order["side"]
                    normalized_order = {
                        "price": float(order["price"]),
                        "order_id": str(order["id"]),
                        "start_qty": float(order["size"]),
                        "executed_qty": float(order["filled_size"]),
                    }
            elif api["exchange"] == "binance":
                    order_type = order["side"]
                    normalized_order = {
                        "price": float(order["price"]),
                        "order_id": str(order["orderId"]),
                        "start_qty": float(order["origQty"]),
                        "executed_qty": float(order["executedQty"]),
                    }
           
            elif api["exchange"] == "kraken":
                # kraken nests the data mostly in "descr"
                order_type = order["descr"]["type"]
                # it also does not pre sort orders by symbol
                if order["descr"]["pair"] == symbol:
                    normalized_order = {
                        "price": float(order["descr"]["price"]),
                        "order_id": str(order["refid"]),
                        "start_qty": float(order["descr"]["volume"]),
                        "executed_qty": float(order["descr"]["vol_exec"]),
                    }
            if normalized_order:
                normalized_order["current_qty"] = (
                    normalized_order["start_qty"] - normalized_order["executed_qty"]
                )
        # poloniex/bitfinex/bittrex do not provide executed quantity
        if api["exchange"] in ["coinbase", "binance", "kraken"]:
            if api["exchange"] == "poloniex":
                order_type = order["type"]
                normalized_order = {
                    "price": float(order["rate"]),
                    "order_id": str(order["orderNumber"]),
                    "start_qty": float(order["startingAmount"]),
                    "current_qty": float(order["amount"]),
                }
            elif api["exchange"] == "bittrex":
                order_type = order["OrderType"]
                normalized_order = {
                    "price": float(order["Price"]),
                    "order_id": str(order["OrderUuid"]),
                    "start_qty": float(order["Quantity"]),
                    "current_qty": float(order["QuantityRemaining"]),
                }
            elif api["exchange"] == "bitfinex":
                # see bitfinex docs for list indexing
                normalized_order = {
                    "price": float(order[16]),
                    "order_id": str(order[0]),
                    "start_qty": float(order[7]),
                    "current_qty": float(order[6]),
                }
            normalized_order["executed_qty"] = (
                normalized_order["start_qty"] - normalized_order["current_qty"]
            )
            # bitfinex uses negative values to denote sell
            order_type = "buy"
            if normalized_order["start_qty"] < 0:
                order_type = "sell"
                normalized_order["start_qty"] *= 1
                normalized_order["current_qty"] *= 1
                normalized_order["executed_qty"] *= 1

        if normalized_order: # in case of kraken there may not be one
            order_type = order_type.lower()
            if order_type == "buy":
                bids.append(normalized_order)
                bid_sum += normalized_order["current_qty"]
            elif order_type == "sell":
                asks.append(normalized_order)
                ask_sum += normalized_order["current_qty"]

    orders = {"bids": bids, "asks": asks, "bid_sum": bid_sum, "ask_sum": ask_sum}
    return orders


def post_order(api, side, quantity, price):
    """
    POST Normalized Limit Order
    """
    
    def precision(num, places):
        """
        return an amount rounded down to given precision
        """
        return int(num * 10 ** places) / float(10 ** places)

    print(post_order.__doc__, side.upper(), quantity, api['symbol'], "at", "%.8f"%price)
    price = precision(float(price), 8)
    # six sigma of requested quantity to account for rounding issues
    if int(quantity) != quantity:
        quantity = 0.999999 * float(quantity)
    # each exchange has its own precision standards available by api call
    # to save call; hard coded max precision by assets > $25 price Nov 2019
    # FIXME: may need case by case basis
    asset, currency = api['symbol'].split(":")
    if asset == "BTC":
        quantity = precision(quantity, 3)
        price = precision(price, 2)
    elif asset in ["MKR", "BCH", "ETH", "BSV", "DASH", "XMR", "LTC", "ZEC"]:
        quantity = precision(quantity, 1)
    else:
        quantity = int(quantity)
    if DETAIL:
        print("adjusted", quantity, api['symbol'], "at", price)
    # format remote procedure call to exchange api standards
    symbol = symbol_syntax(api["exchange"], api['symbol'])
    if api["exchange"] == "coinbase":
        api["params"] = {
            "product_id": symbol,
            "side": side.lower(),
            "price": price,
            "size": quantity,
            "type": "limit",
        }
        api["endpoint"] = "/orders"
        api["method"] = "POST"
    elif api["exchange"] == "poloniex":
        api["params"] = {
            "command": side.lower(),
            "currencyPair": symbol,
            # requires explicit string formatting
            "amount": str(quantity), 
            "rate": "%.8f" % price,
        }
        api["endpoint"] = "/tradingApi"
        api["method"] = "POST"
    elif api["exchange"] == "binance":
        api["params"] = {
            "symbol": symbol,
            "side": side.lower(),
            "quantity": quantity,
            "type": "LIMIT",
            "price": price,
            "timeInForce": "GTC",
        }
        api["endpoint"] = "/api/v3/order"
        api["method"] = "POST"
    elif api["exchange"] == "bittrex":
        api["method"] = "GET"
        if side == "buy":
            api["endpoint"] = "/market/buylimit"
        if side == "sell":
            api["endpoint"] = "/market/selllimit"
        api["params"] = {
            "market": symbol,
            "quanity": quantity,
            "rate": price,
            "timeInForce": "GTC",
        }
    elif api["exchange"] == "kraken":
        api["params"] = {
            "pair": symbol,
            "type": side,
            "orderType": "limit",
            "price": price,
            "volume": quanity,
        }
        api["endpoint"] = "0/private/AddOrder"
        api["method"] = "POST"
    elif api["exchange"] == "bitfinex":
        api["params"] = {
            "type": "LIMIT",
            "symbol": symbol,
            "price": price,
            "amount": quantity,
        }
        if side == "sell":  # negative amount indicates sell
            api["params"]["amount"] *= 1
        api["endpoint"] = "/v2/auth/w/order/submit"
        api["method"] = "POST"
    # make external POST order call
    ret = process_request(api)
    return ret


def cancel(api, order_ids=None):
    """
    DELETE all orders by api["symbol"] (or) by symbol and order_id:
    """
    if DETAIL:
        print(cancel.__doc__, "symbol", api['symbol'], "order_ids", order_ids)
    if order_ids is None:
        order_ids = [] # must be a list
    # format remote procedure call to exchange api standards
    symbol = symbol_syntax(api["exchange"], api['symbol'])
    if not order_ids:
        print("Cancel All")
    else:
        print("Cancel Order Ids:", order_ids)
    # Coinbase and Poloniex offer both Cancel All and Cancel One
    if api["exchange"] in ["coinbase", "poloniex"]:
        if order_ids: 
            # Cancel a list of orders
            ret = []
            for order_id in order_ids:
                print("Cancel Order", order_id)
                if api["exchange"] == "coinbase":                
                    api["endpoint"] = "/orders/" + str(order_id)
                    api["params"] = {}
                    api["method"] = "DELETE"
                elif api["exchange"] == "poloniex":                
                    api["endpoint"] = "/tradingApi"
                    api["params"] = {"command": "cancelOrder", "orderNumber": int(order_id)}
                    api["method"] = "POST"  
                    response = process_request(api)
                    ret.append({"order_id": order_id, "response": response})
        else: 
            # Cancel All
            if api["exchange"] == "coinbase":    
                api["endpoint"] = "/orders"
                api["params"] = {"product_id": symbol}
                api["method"] = "DELETE"            
            elif api["exchange"] == "poloniex":    
                api["endpoint"] = "/tradingApi"
                api["params"] = {"command": "cancelAllOrders", "currencyPair": symbol}
                api["method"] = "POST"
            ret = process_request(api)
        
    # Handle cases where "Cancel All" in one market is not supported
    elif api["exchange"] in ["kraken", "binance", "bittrex", "Bitfinex"]:
        if (api["exchange"] == "bitfinex") and not api["symbol"]:
            print("WARN: Cancel All in ALL MARKETS")
            api["endpoint"] = "/v2/auth/w/order/cancel/multi"
            api["params"] = {}
            api["method"] = "POST"
            ret = process_request(api)
        else:
            # If we have an order_ids list we'll use it, else make one
            if not order_ids:
                print("Open Orders call to suppport Cancel All")
                orders = get_orders(api)
                order_ids = []
                for order in orders["asks"]:
                    order_ids.append(order["order_id"])
                for order in orders["bids"]:
                    order_ids.append(order["order_id"]) 
            ret = []
            for order_id in order_ids:
                print("Cancel Order", order_id)
                if api['exchange'] == "bitfinex":
                    api["endpoint"] = "/v2/auth/w/order/cancel"
                    api["params"] = {"id": order_id}
                    api["method"] = ""
                elif api["exchange"] == "binance":
                    api["endpoint"] = "/api/v3/order"
                    api["params"] = {"symbol": symbol, "orderId": order_id}
                    api["method"] = "DELETE"
                elif api["exchange"] == "bittrex": 
                    api["endpoint"] = "/api/v1.1/market/cancel"
                    api["params"] = {"uuid": order_id}
                    api["method"] = "GET"
                elif api["exchange"] == "kraken":
                    api["endpoint"] = "/0/private/CancelOrder"
                    api["params"] = {"txid": order_id}
                    api["method"] = "POST"
                response = process_request(api)
                ret.append(response) 

    return ret


def demo():
    """
    Open Orders and Account Balances Demonstration
    """
    # get sandbox keys at https://public.sandbox.pro.coinbase.com/
    api = {
        "symbol": "XLM:BTC",
        "exchange": "coinbase",
        "key": "test",
        "secret": "test",
        "passphrase": "test",
    }
    

    api["symbol"] = "XRP:BTC"
    
    
    print(api["symbol"])    
    print(cancel(api))
    print(get_orders(api))  
    print(get_balances(api))
    print(post_order(api, side="buy", quantity=2, price=0.00003250))
    print(get_orders(api))
    print(get_balances(api))


if __name__ == "__main__":
    print("\033c")
    demo()
