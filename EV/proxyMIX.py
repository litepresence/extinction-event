# ======================================================================
VERSION = "proxyMIX v0.00000001"
# ======================================================================

# ======================================================================
API = "www.nomics.com"  # GET FREE API KEY HERE
# ======================================================================

# Daily HLOCV Crypto Exchange Specific Candles from nomics.com

" litepresence 2019 "


def WTFPL_v0_March_1765():
    if any([stamps, licenses, taxation, regulation, fiat, etat]):
        try:
            print("no thank you")
        except:
            return [tar, feathers]


" ********** ALPHA RELEASE TO PUBLIC DOMAIN WITH NO WARRANTY ********* "


# input (exchange, asset, currency, start, stop, period) *note exchange
# output 'data' dictionary of numpy arrays
# daily candles only, 86400

# data['unix'] # integers
# data['high'] # float
# data['low'] # float
# data['open'] # float
# data['close'] # float
# data['volume'] # float

# get candles to data origin
# exact data as reported by each exchange
# encapsulated websocket call in time out multiprocess
# interprocess communication via txt; returns numpy arrays

import time
import requests
import numpy as np
from pprint import pprint
from calendar import timegm
from datetime import datetime
from json import dumps as json_dumps
from json import loads as json_loads
from multiprocessing import Process, Value

ATTEMPTS = 3
TIMEOUT = 60

# to learn more about available data visit these links
market_list = "https://api.nomics.com/v1/markets?key=YOUR-API-KEY"
exchange_list = "https://nomics.com/exchanges"


def race_write(doc="", text=""):  # Concurrent Write to File Operation

    text = str(text)
    i = 0
    while True:
        try:
            time.sleep(0.05 * i ** 2)
            i += 1
            with open(doc, "w+") as f:
                f.write(text)
                f.close()
                break
        except Exception as e:
            msg = str(type(e).__name__) + str(e.args)
            msg += " race_write()"
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


def race_read_json(doc=""):

    i = 0
    while True:
        try:
            time.sleep(0.05 * i ** 2)
            i += 1
            with open(doc, "r") as f:
                data = json_loads(f.read())
                f.close()
                return data
        except Exception as e:
            msg = str(type(e).__name__) + str(e.args)
            msg += " race_read_json()"
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


def to_iso_date(unix):  # returns iso8601 datetime given unix epoch
    return datetime.utcfromtimestamp(int(unix)).isoformat()


def from_iso_date(date):  # returns unix epoch given iso8601 datetime
    return int(timegm(time.strptime(str(date), "%Y-%m-%dT%H:%M:%SZ")))


def to_list_of_dicts(ret):
    data = []
    # change from dict of dicts to list of dicts;
    # rename keys, add unix
    for i in range(len(ret)):
        v = {}
        v["unix"] = from_iso_date(ret[i]["timestamp"])
        v["open"] = ret[i]["open"]
        v["high"] = ret[i]["high"]
        v["low"] = ret[i]["low"]
        v["close"] = ret[i]["close"]
        v["volume"] = ret[i]["volume"]
        data.append(v)
    # sort list of dicts by value of key unix
    return sorted(data, key=lambda k: k["unix"])


def to_dict_of_lists(data):
    # switch from list of dicts <-> to dict of lists
    d = {}
    d["unix"] = []
    d["high"] = []
    d["low"] = []
    d["open"] = []
    d["close"] = []
    d["volume"] = []
    try_split = True
    for i in range(len(data)):  # days):
        if try_split:
            try:
                split = float(data[i]["split"])
            except:
                split = 1
                try_split = False
        else:
            split = 1
        d["unix"].append(int(data[i]["unix"]))
        d["high"].append(float(data[i]["high"]) * split)
        d["low"].append(float(data[i]["low"]) * split)
        d["open"].append(float(data[i]["open"]) * split)
        d["close"].append(float(data[i]["close"]) * split)
        d["volume"].append(float(data[i]["volume"]) * split)
    return d


def window(start, stop, data):

    # limit data to window requested
    d = {}
    d["unix"] = []
    d["high"] = []
    d["low"] = []
    d["open"] = []
    d["close"] = []
    d["volume"] = []
    for i in range(len(data["unix"])):
        if start <= data["unix"][i] <= stop:
            d["unix"].append(int(data["unix"][i]))
            d["high"].append(float(data["high"][i]))
            d["low"].append(float(data["low"][i]))
            d["open"].append(float(data["open"][i]))
            d["close"].append(float(data["close"][i]))
            d["volume"].append(float(data["volume"][i]))
    return d


def crypto(signal, exchange, asset, currency, start, stop, period):

    market = asset + currency

    days = int((stop - start) / float(period))
    # make api call for data
    if KEY == "":
        raise ValueError("YOU MUST GET API KEY FROM nomics.com")
    if period != 86400:
        raise ValueError("Daily Candles Only")

    uri = "https://api.nomics.com/v1/exchange_candles"
    params = {
        "key": KEY,
        "interval": "1d",
        "exchange": exchange,
        "market": market,
        "start": to_iso_date(start),
        "end": to_iso_date(stop),
    }
    ret = requests.get(uri, params=params, timeout=(6, 30)).json()

    print(ret)
    # post process to extinctionEVENT format
    data = to_list_of_dicts(ret)
    data = to_dict_of_lists(data)
    data = window(start, stop, data)
    # inter process communication via txt
    race_write("proxy.txt", json_dumps(data))
    signal.value = 1


def proxyMIX(exchange, asset, currency, start, stop, candle=86400):

    global KEY

    KEY = race_read_json(doc="apiKEYS.py")["nomics"]

    begin = time.time()
    start = int(start)
    stop = int(stop)
    period = int(candle)
    depth = int((stop - start) / 86400.0)

    print(
        (
            "API Nomics %s %s %s %ss %se CANDLE %s DAYS %s"
            % (exchange, asset, currency, start, stop, period, depth)
        )
    )

    signal = Value("i", 0)
    i = 0
    while (i < ATTEMPTS) and not signal.value:
        i += 1
        print("")
        print("proxyALPHA attempt:", i, time.ctime())
        child = Process(
            target=crypto,
            args=(
                signal,
                exchange,
                asset,
                currency,
                start,
                stop,
                period,
            ),
        )
        child.daemon = False
        child.start()
        child.join(TIMEOUT)
        child.terminate()

    # read text file written by child; in worst case return stale
    data = race_read_json("proxy.txt")
    race_write("proxy.txt", "")
    # convert dict values from lists to numpy arrays
    print("proxyDEX elapsed:", ("%.2f" % (time.time() - begin)))
    return {k: np.array(v) for k, v in data.items()}
