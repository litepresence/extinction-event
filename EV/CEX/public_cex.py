"""
Normalized Last, Book, Candles

Binance, Poloniex, Bitfinex, Bittrex, Coinbase, Kraken

litepresence 2019
"""
# STANDARD MODULES
# ======================================================================
import os
import time
from pprint import pprint
from json import dumps as json_dumps
from json import loads as json_loads
from multiprocessing import Process, Value
from datetime import datetime
from calendar import timegm
from math import ceil
import traceback

# THIRD PARTY MODULES
# ======================================================================
import numpy as np
import requests

# GLOBAL USER DEFINED CONSTANTS
# ======================================================================
TIMEOUT = 30
ATTEMPTS = 10
PATH = str(os.path.dirname(os.path.abspath(__file__))) + "/"
# READ ME
# ======================================================================
def read_me():
    """
    MODULE USAGE

    from public_cex import price, klines, depth

    print(get_price(exchange, symbol))
    print(get_book(exchange, symbol, depth))
    print(get_candles(exchange, symbol, interval, start, end))

    ABOUT

    Only supports top ranked exchanges with real volume over $10m daily
    unified API inputs 
    normalized return as dict of numpys 
    pep8 / pylint
    procedural Python - no class objects
    external requests multiprocess wrapped
    architecture sorted by call type
    human readable interprocess communication via *.txt
    easy to compare exchange parameters
    
    EXCHANGE RANKINGS
    
    https://www.sec.gov/comments/sr-nysearca-2019-01/srnysearca201901-5164833-183434.pdf    
    
    https://www.coingecko.com/en/exchanges
    https://www.cryptocompare.com/exchanges
    https://www.bti.live/exchanges/
    https://bitcoinexchangeguide.com/bitcoin-exchanges-in-the-united-states/
    https://coin.market/exchanges
    https://cryptorank.io/exchanges    
    
    ADDITIONAL EXCHANGES
    
    Exchange addition PR's considered on case by case basis.
    $10m minimum daily - legitimate - volume
    """
    print(read_me.__doc__)


def api_docs():
    """
    API DOCS

    https://bittrex.github.io/api/v1-1
    https://github.com/thebotguys/golang-bittrex-api/
        wiki/Bittrex-API-Reference-(Unofficial)

    https://docs.bitfinex.com/reference

    https://docs.pro.coinbase.com/

    https://docs.poloniex.com/#introduction

    https://binance-docs.github.io/apidocs/spot/en/#change-log

    https://www.kraken.com/features/api
    https://github.com/veox/python3-krakenex
    https://support.kraken.com/hc/en-us/categories/360000080686-API    
    """
    print(api_docs.__doc__)


# TEXT PIPE
# ======================================================================
def race_write(doc="", text=""):
    """
    Bulletproof Write to File Operation for Text Pipe IPC
    """
    text = str(text)
    i = 0
    while True:
        try:
            time.sleep(0.05 * i ** 2)
            i += 1
            with open("pipe/" + doc, "w+") as handle:
                handle.write(text)
                handle.close()
                break
        except Exception as error:
            msg = str(type(error).__name__) + str(error.args)
            msg += " race_write()"
            print(msg)
            try:
                handle.close()
            except:
                pass
            continue
        finally:
            try:
                handle.close()
            except:
                pass


def race_read_json(doc=""):
    """
    Bulletproof Read JSON from File Operation for Text Pipe IPC
    """
    i = 0
    while True:
        try:
            time.sleep(0.05 * i ** 2)
            i += 1
            with open("pipe/" + doc, "r") as handle:
                data = json_loads(handle.read())
                handle.close()
                return data
        except Exception as error:
            msg = str(type(error).__name__) + str(error.args)
            msg += " race_read_json()"
            print(msg)
            try:
                handle.close()
            except:
                pass
            continue
        finally:
            try:
                handle.close()
            except:
                pass


# FORMATING
# ======================================================================
def from_iso_date(date):
    """
    ISO to UNIX conversion
    """
    return int(timegm(time.strptime(str(date), "%Y-%m-%dT%H:%M:%S")))


def to_iso_date(unix):
    """
    iso8601 datetime given unix epoch
    """
    return datetime.utcfromtimestamp(int(unix)).isoformat()


def symbol_syntax(exchange, symbol):
    """
    translate ticker symbol to each exchange's local syntax
    """
    asset, currency = symbol.upper().split(":")
    # ticker symbol colloquialisms
    if exchange == "kraken":
        if asset == "BTC":
            asset = "XBT"
        if currency == "BTC":
            currency = "XBT"
    if exchange == "poloniex":
        if asset == "XLM":
            asset = "STR"
        if currency == "USD":
            currency = "USDT"
    if exchange == "binance":
        if currency == "USD":
            currency = "USDT"
    symbols = {
        "bittrex": (currency + "-" + asset),
        "bitfinex": (asset + currency),
        "binance": (asset + currency),
        "poloniex": (currency + "_" + asset),
        "coinbase": (asset + "-" + currency),
        "kraken": (asset.lower() + currency.lower()),
    }
    symbol = symbols[exchange]
    return symbol


def trace(error):
    """
    Stack Trace Message Formatting
    """
    msg = str(type(error).__name__) + str(error.args) + str(traceback.format_exc())
    return msg


# SUBPROCESS REMOTE PROCEDURE CALL
# ======================================================================
def request(exchange, instance, signal, method, params=None):
    """
    GET remote procedure call to public exchange API
    """
    urls = {
        "coinbase": "https://api.pro.coinbase.com",
        "bittrex": "https://bittrex.com",
        "bitfinex": "https://api-pub.bitfinex.com",
        "kraken": "https://api.kraken.com",
        "poloniex": "https://www.poloniex.com",
        "binance": "https://api.binance.com",
    }
    url = urls[exchange]
    print(exchange, method, url, params)
    resp = requests.get((url + method), params)
    data = resp.json()
    if isinstance(data, dict):
        print("dict", data.keys())
    elif isinstance(data, list):
        print("list", len(data))
    else:
        print(data)
    print("len request data", len(data))
    doc = instance + "_{}_public.txt".format(exchange)
    race_write(doc, json_dumps(data))
    signal.value = 1


def process_request(exchange, path, params):
    """
    Multiprocessing Durability Wrapper for External Requests
    """
    begin = time.time()
    signal = Value("i", 0)
    i = 0
    instance = str(int(time.time()))
    while (i < ATTEMPTS) and not signal.value:
        i += 1
        print("")
        print("{} PUBLIC attempt:".format(exchange), i, time.ctime())
        child = Process(target=request, args=(exchange, instance, signal, path, params))
        child.daemon = False
        child.start()
        child.join(TIMEOUT)
        child.terminate()
        time.sleep(3)
    doc = instance + "_{}_public.txt".format(exchange)
    data = race_read_json(doc)
    path = PATH + "pipe/"
    if os.path.isfile(path + doc):
        os.remove(path + doc)
    # convert dict values from lists to numpy arrays
    print("{} PUBLIC elapsed:".format(exchange), ("%.2f" % (time.time() - begin)))
    print("")
    return data


# METHODS
# ======================================================================
def get_price(exchange, symbol):
    """
    Last Price as float
    """
    symbol = symbol_syntax(exchange, symbol)
    method = {
        "bittrex": "/api/v1.1/public/getticker",
        "bitfinex": "/v2/ticker/t{}".format(symbol),
        "binance": "/api/v1/ticker/allPrices",
        "poloniex": "/public",
        "coinbase": "/products/{}/ticker".format(symbol),
        "kraken": "/0/public/Ticker",
    }
    params = {
        "bittrex": {"market": symbol},
        "bitfinex": {"market": symbol},
        "binance": {},
        "poloniex": {"command": "returnTicker"},
        "coinbase": {"market": symbol},
        "kraken": {"pair": [symbol]},
    }
    method = method[exchange]
    params = params[exchange]
    while 1:

        try:
            data = process_request(exchange, method, params)
            if exchange == "bittrex":
                last = float(data["result"]["Last"])
            elif exchange == "bitfinex":
                last = float(data[6])
            elif exchange == "binance":
                data = {d["symbol"]: float(d["price"]) for d in data}
                last = data[symbol]
            elif exchange == "poloniex":
                last = float(data[symbol]["last"])
            elif exchange == "coinbase":
                last = float(data["price"])
            elif exchange == "kraken":
                data = data["result"]
                data = data[list(data)[0]]
                last = float(data["c"][0])
        except Exception as error:
            print(trace(error))
        break

    return last


def get_book(exchange, symbol, depth=10):
    """
    Depth of Market format:

    {"bidv": [], "bidp": [], "askp": [], "askv": []}
    """

    if depth > 50:
        depth = 50
    symbol = symbol_syntax(exchange, symbol)
    method = {
        "bittrex": "/api/v1.1/public/getorderbook",
        "bitfinex": "/v2/book/t{}/P0".format(symbol),
        "binance": "/api/v1/depth",
        "poloniex": "/public",
        "coinbase": "/products/{}/book".format(symbol),
        "kraken": "/0/public/Depth",
    }
    params = {
        "bittrex": {"market": symbol, "type": "both"},
        "bitfinex": {"len": 100},
        "binance": {"symbol": symbol},
        "poloniex": {"command": "returnOrderBook", "currencyPair": symbol},
        "coinbase": {"level": 2},
        "kraken": {"pair": symbol, "count": "50"},
    }
    method = method[exchange]
    params = params[exchange]

    while 1:
        try:
            data = process_request(exchange, method, params)
            if exchange == "kraken":
                data = data["result"]
                data = data[list(data)[0]]
            if exchange == "bittrex":
                data = data["result"]

            # convert books to unified format
            book = {"bidv": [], "bidp": [], "askp": [], "askv": []}
            if exchange in ["binance", "poloniex", "coinbase", "kraken"]:
                # {"bids" [[,],[,],[,]], "asks": [[,],[,],[,]]}
                for i in range(len(data["bids"])):
                    book["bidv"].append(float(data["bids"][i][1]))
                    book["bidp"].append(float(data["bids"][i][0]))
                for i in range(len(data["asks"])):
                    book["askv"].append(float(data["asks"][i][1]))
                    book["askp"].append(float(data["asks"][i][0]))
            elif exchange == "bittrex":
                # {"bids": [{Quantity:, "Rate"},...,],
                #  "asks": [{Quantity:, "Rate"},...,]}
                for _, item in enumerate(data["buy"]):
                    book["bidv"].append(float(item["Quantity"]))
                    book["bidp"].append(float(item["Rate"]))
                for _, item in enumerate(data["sell"]):
                    book["askv"].append(float(item["Quantity"]))
                    book["askp"].append(float(item["Rate"]))
            elif exchange == "bitfinex":
                # [[,,],[,,],[,,]] # bids negative volume
                for _, item in enumerate(data):
                    if item[2] > 0:
                        book["bidv"].append(float(item[2]))
                        book["bidp"].append(float(item[0]))
                    else:
                        book["askv"].append(-float(item[2]))
                        book["askp"].append(float(item[0]))
                # book = {k:v[::-1] for k, v in book.items()}

            # normalize lowest ask and highest bid to [0] position
            book["bidv"] = [v for p, v in sorted(zip(book["bidp"], book["bidv"]))]
            book["askv"] = [v for p, v in sorted(zip(book["askp"], book["askv"]))]
            book["bidp"] = sorted(book["bidp"])
            book["askp"] = sorted(book["askp"])
            book["bidv"] = book["bidv"][::-1]
            book["bidp"] = book["bidp"][::-1]
            # standardize book depth
            book["bidv"] = book["bidv"][:depth]
            book["bidp"] = book["bidp"][:depth]
            book["askv"] = book["askv"][:depth]
            book["askp"] = book["askp"][:depth]

            book = {k: np.array(v) for k, v in book.items()}

            print("total bids:", len(book["bidp"]))
            print("total asks:", len(book["askp"]))
        except Exception as error:
            print(trace(error))
        break

    return book


def get_candles(exchange, symbol, interval=86400, start=None, end=None):
    """
    input and output normalized requests for candle data
    returns a dict with numpy array values for the following keys
    ["high", "low", "open", "close", "volume", "unix"]
    """

    def paginate_candles(exchange, symbol, interval, start, end):
        """
        paginate requests per maximum request size per exchage
        collate responses crudely with one interval overlap               
        """

        max_candles = {
            "bittrex": 1000,  # 1000
            "bitfinex": 2000,  # 5000
            "binance": 500,  # 1000
            "poloniex": 2000,
            "coinbase": 300,  # 300
            "kraken": 200,  # 200
        }

        """
        # USE FOR EDGE MATCHING DEV
        max_candles = {
            "bittrex": 100, 
            "bitfinex": 100,  
            "binance": 100, 
            "poloniex": 100,
            "coinbase": 100,
            "kraken": 100,  
        }
        """

        # fetch the max candles at this exchange
        max_candles = max_candles[exchange] - 5 
        # define the maximum exchange window in seconds
        window = int(max_candles * interval)
        # determine number of candles we require
        depth = int(ceil((end - deep_begin) / float(interval)))
        # determine number of calls required to get those candles
        calls = int(max(ceil(depth / float(max_candles)), 1))
        # pagination and crude collation
        stop = end
        if calls > 1:
            data = []
            for call in range(calls, 0, -1):

                # one interval wide on each end
                end = stop - (call - 1) * window + 2*interval
                start = stop - call * window - 2*interval

                print("call", call, "/", calls, start, end)
                datum = candles(exchange, symbol, interval, start, end)
                time.sleep(1)
                data += datum
        # single request
        else:
            data = candles(exchange, symbol, interval, deep_begin, end)

        return data

    def no_duplicates(data):
        """
        ensure no duplicates - pagination overlap at edges
        """
        dup_free = []
        timestamps = []
        for index, item in enumerate(data):
            if item["unix"] not in timestamps:
                timestamps.append(item["unix"])
                dup_free.append(item)

        return dup_free

    def sort_by_unix(data):

        data = sorted(data, key=lambda k: k["unix"])

        return data

    def interpolate_previous(data, start, end, interval):

        start = int(start)
        end = int(end)
        interval = int(interval)

        ip_unix = [t for t in range(min(data["unix"]), max(data["unix"]), interval)]

        v = []
        h = []
        l = []
        o = []
        c = []
        for _, candle in enumerate(ip_unix):
            for idx, _ in enumerate(data["unix"]):

                match = False
                diff = candle - data["unix"][idx]

                if 0 <= diff < interval:
                    match = True
                    v.append(data["volume"][idx])
                    h.append(data["high"][idx])
                    l.append(data["low"][idx])
                    o.append(data["open"][idx])
                    c.append(data["close"][idx])
                    break

            if not match:
                if candle == start:
                    close = data["close"][0]
                else:
                    close = c[-1]
                v.append(0)
                h.append(close)
                l.append(close)
                o.append(close)
                c.append(close)
        d2 = {}
        d2["high"] = h
        d2["low"] = l
        d2["open"] = o
        d2["close"] = c
        d2["volume"] = v
        d2["unix"] = ip_unix

        for k,v in d2.items():
            print(len(v), k)


        return d2

    def window_data(data, start, end):
        """
        # use this to window data if still in list of dict form
        d2 = []        
        for index, item in enumerate(data):
            if start < item["unix"] < end:
                d2.append(item)
        """
        d2 = {"high": [], "low": [], "open": [], "close": [], "volume": [], "unix":[]}

        for idx, item in enumerate(data["unix"]):
            if start < item <= end:
                d2["high"].append(data["high"][idx])
                d2["low"].append(data["low"][idx])
                d2["open"].append(data["open"][idx])
                d2["close"].append(data["close"][idx])
                d2["volume"].append(data["volume"][idx])
                d2["unix"].append(data["unix"][idx])

        return d2

    def left_strip(data):
        
        d2 = {"high": [], "low": [], "open": [], "close": [], "volume": [], "unix":[]}
        begin = False
        
        for idx, item in enumerate(data['volume']):  
            if item or begin:
                begin = True
                d2["high"].append(data["high"][idx])
                d2["low"].append(data["low"][idx])
                d2["open"].append(data["open"][idx])
                d2["close"].append(data["close"][idx])
                d2["volume"].append(data["volume"][idx])
                d2["unix"].append(data["unix"][idx])
        
        return d2

    def reformat(data):
        """
        switch from list-of-dicts to dict-of-lists
        """
        list_format = {}
        list_format["unix"] = []
        list_format["high"] = []
        list_format["low"] = []
        list_format["open"] = []
        list_format["close"] = []
        list_format["volume"] = []
        for _, item in enumerate(data):
            list_format["unix"].append(item["unix"])
            list_format["high"].append(item["high"])
            list_format["low"].append(item["low"])
            list_format["open"].append(item["open"])
            list_format["close"].append(item["close"])
            list_format["volume"].append(item["volume"])

        return list_format

    def normalize(data):
        """
        ensure high is high and low is low
        filter extreme candatales at 0.5X to 2X the candatale average
        ensure open and close are within high and low
        """

        for i, _ in enumerate(data["close"]):

            data["high"][i] = max(
                data["high"][i], data["low"][i], data["open"][i], data["close"][i]
            )
            data["low"][i] = min(
                data["high"][i], data["low"][i], data["open"][i], data["close"][i]
            )
            ocl = (data["open"][i] + data["close"][i] + data["low"][i]) / 3
            och = (data["open"][i] + data["close"][i] + data["high"][i]) / 3
            data["high"][i] = min(data["high"][i], 2 * ocl)
            data["low"][i] = max(data["low"][i], och / 2)
            data["open"][i] = min(data["open"][i], data["high"][i])
            data["open"][i] = max(data["open"][i], data["low"][i])
            data["close"][i] = min(data["close"][i], data["high"][i])
            data["close"][i] = max(data["close"][i], data["low"][i])

        return data

    symbol = symbol_syntax(exchange, symbol)
    if end is None:
        # to current
        end = int(time.time())
    if start is None:
        # default 10 candles
        start = end - 10 * interval
    # allow for timestamp up to one minute in future.
    end = end + 60

    # request 3 candles deeper than needed
    deep_begin = start - 3 * interval

    print("\nstart:", to_iso_date(start), "end:", to_iso_date(end))
    
    while True:
    
        try:
            # collect external data in pages if need be
            data = paginate_candles(exchange, symbol, interval, deep_begin, end)
            print(len(data), "edge match - paginated with overlap and collated")
            data = no_duplicates(data)
            print(len(data), "edge match - no duplicates by unix")
            data = sort_by_unix(data)
            print(len(data), "edge match - sort by unix")
            data = reformat(data)
            print(len(data["unix"]), "rotation; reformated to dict of lists")
            data = interpolate_previous(data, deep_begin, end, interval)
            print(len(data["unix"]), len(data["close"]), "missing buckets to candles interpolated as previous close")
            data = window_data(data, start, end)
            print(len(data["unix"]), "windowed to intial start / end request")
            data = left_strip(data)
            print(len(data["unix"]), "stripped of empty pre market candles")
            data = normalize(data)
            print({k: len(v) for k, v in data.items()})
            print("normalized as valid: high is highest, no extremes, etc.")
            data = {k: np.array(v) for k, v in data.items()}
            print("final conversion to dict of numpy arrays:\n")
            print("total items", len(data), "/", len(data["unix"]), "keys", data.keys(), "type", type(data["unix"]))
            print("\n\nRETURNING", exchange.upper(), symbol, "CANDLE DATA\n\n")
            
            return data

        except Exception as error:
            msg = trace(error)
            print(msg, data)
            continue


def candles(exchange, symbol, interval, start, end):
    """
    single page of candle data
    """
    limit = int(float(end - start) / interval) + 1
    intervals = {
        "bittrex": {
            60: "oneMin",
            300: "fiveMin",
            1800: "thirtyMin",
            3600: "hour",
            86400: "day",
        },
        "bitfinex": {
            60: "1m",
            300: "5m",
            900: "15m",
            1800: "30m",
            3600: "1h",
            10800: "3h",
            21600: "6h",
            43200: "12h",
            86400: "1D",
            604800: "7D",
            1209600: "14D",
            2419200: "1M",
        },
        "binance": {
            60: "1m",
            180: "3m",
            300: "5m",
            900: "15m",
            1800: "30m",
            3600: "1h",
            14400: "4h",
            21600: "6h",
            28800: "8h",
            43200: "12h",
            86400: "1d",
            604800: "1w",
            2419200: "1M",
        },
        "poloniex": {
            300: 300,
            900: 900,
            1800: 1800,
            7200: 7200,
            14400: 14000,
            86400: 86400,
        },
        "coinbase": {
            60: 60,
            300: 300,
            900: 900,
            3600: 3600,
            21600: 21600,
            86400: 86400,
        },
        "kraken": {
            60: 1,
            300: 5,
            900: 15,
            1800: 30,
            3600: 60,
            14400: 240,
            86400: 1440,
            604800: 10080,
            2419200: 21600,
        },
    }

    try:
        bitfinex_hist = "".join(
            [i for i in intervals["bitfinex"][interval] if not i.isdigit()]
        )
        interval = intervals[exchange][interval]
    except Exception as error:
        trace(error)
        print("Invalid interval for this exchange")
        print(exchange, symbol, interval)
        pprint(intervals)

    method = {
        "bittrex": "/api/v2.0/pub/market/GetTicks",
        "bitfinex": "/v2/candles/trade:1{}:t{}/hist".format(bitfinex_hist, symbol),
        "binance": "/api/v1/klines",
        "poloniex": "/public",
        "coinbase": "/products/{}/candles".format(symbol),
        "kraken": "/0/public/OHLC",
    }
    params = {
        "bittrex": {"marketName": symbol, "tickInterval": interval},
        "bitfinex": {"granularity": interval, "limit": limit},
        "binance": {"symbol": symbol, "interval": interval},
        "poloniex": {
            "command": "returnChartData",
            "currencyPair": symbol,
            "period": interval,
        },
        "coinbase": {"granularity": interval},
        "kraken": {"pair": symbol, "interval": interval},
    }
    windows = {
        "bittrex": {},  # {"_": 1000 * start},
        "bitfinex": {"start": 1000 * start, "end": 1000 * end},
        "binance": {"startTime": 1000 * start, "endTime": 1000 * end},
        "poloniex": {"start": start, "end": end},
        "coinbase": {"start": to_iso_date(start), "end": to_iso_date(end)},
        "kraken": {"since": start},
    }
    method = method[exchange]
    params = params[exchange]
    params.update(windows[exchange])

    while 1:

        try:
            data = process_request(exchange, method, params)
            if exchange == "bittrex":
                data = data["result"]
                data = [
                    {
                        "open": float(d["O"]),
                        "high": float(d["H"]),
                        "low": float(d["L"]),
                        "close": float(d["C"]),
                        "volume": float(d["V"]),
                        "unix": from_iso_date(d["T"]),
                    }
                    for d in data
                    if start < from_iso_date(d["T"]) <= end
                ]

            elif exchange == "bitfinex":
                data = [
                    {
                        "unix": int(float(d[0]) / 1000.0),
                        "open": float(d[1]),
                        "close": float(d[2]),
                        "high": float(d[3]),
                        "low": float(d[4]),
                        "volume": float(d[5]),
                    }
                    for d in data
                    if start <= int(float(d[0]) / 1000.0) <= end
                ]
            elif exchange == "binance":
                data = [
                    {
                        "open": float(d[1]),
                        "high": float(d[2]),
                        "low": float(d[3]),
                        "close": float(d[4]),
                        "volume": float(d[5]),
                        "unix": int(int(d[6]) / 1000.0),
                    }
                    for d in data
                ]
            elif exchange == "poloniex":
                data = [
                    {
                        "open": float(d["open"]),
                        "high": float(d["high"]),
                        "low": float(d["low"]),
                        "close": float(d["close"]),
                        "volume": float(d["quoteVolume"]),
                        "unix": int(d["date"]),
                    }
                    for d in data
                ]
            elif exchange == "coinbase":
                data = [
                    {
                        "unix": int(d[0]),
                        "low": float(d[1]),
                        "high": float(d[2]),
                        "open": float(d[3]),
                        "close": float(d[4]),
                        "volume": float(d[5]),
                    }
                    for d in data
                ]
            elif exchange == "kraken":
                data = data["result"]
                data = data[list(data)[0]]
                data = [
                    {
                        "unix": int(d[0]),
                        "open": float(d[1]),
                        "high": float(d[2]),
                        "low": float(d[3]),
                        "close": float(d[4]),
                        # vwap d[5]
                        "volume": float(d[6]),
                    }
                    for d in data
                ]
        except Exception as error:
            print(trace(error))
        break

    return data


# DEMONSTRATION
# ======================================================================
def demo(exchange, symbol):
    """
    Print demo of last price, orderbook, and candles
    Formatted to extinctionEVENT standards
    """
    print("\n***", exchange.upper(), "PRICE ***")
    pprint(get_price(exchange, symbol))
    print("\n***", exchange.upper(), "BOOK ***")
    depth = 50
    pprint(get_book(exchange, symbol, depth))
    # kline request parameters
    interval = 86400
    # None / None will return latest ten candles
    start = None  # or unix epoch seconds
    end = None  # or unix epoch seconds
    print("\n***", exchange.upper(), "CANDLES ***")

    now = int(time.time())
    depth = 100
    start = now - interval * depth
    end = now
    pprint(get_candles(exchange, symbol, interval, start, end))


def main():
    """
    Primary Demonstration Events
    """
    print("\033c", __doc__)
    read_me()
    api_docs()
    symbol = "BTC:USD"
    exchanges = ["bittrex", "bitfinex", "binance", "poloniex", "coinbase", "kraken"]
    print("\n", symbol, "\n")
    print("fetching PRICE, BOOK, and CANDLES from:\n\n", exchanges)
    for exchange in exchanges:
        print("\n==================\n", exchange.upper(), "API\n==================")
        demo(exchange, symbol)


if __name__ == "__main__":
    main()
