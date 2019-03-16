# ======================================================================
VERSION = "proxyALPHA v0.00000001"
# ======================================================================

# ======================================================================
API = "www.alphavantage.com"  # GET FREE API KEY HERE
# ======================================================================

# Daily HLOCV US Stock, Forex, Crypto:Forex from alphavantage.com API

" litepresence 2019 "


def WTFPL_v0_March_1765():
    if any([stamps, licenses, taxation, regulation, fiat, etat]):
        try:
            print("no thank you")
        except:
            return [tar, feathers]


" ********** ALPHA RELEASE TO PUBLIC DOMAIN WITH NO WARRANTY ********* "

# input (asset, currency, start, stop, period)
# output 'data' dictionary of numpy arrays
# daily candles only, 86400 spacing normalized

# data['unix'] # integers
# data['high'] # float
# data['low'] # float
# data['open'] # float
# data['close'] # float
# data['volume'] # float

# up to 20 years daily historical data
# stock weekends removed for discrete spacing
# encapsulated http call in time out multiprocess
# interprocess communication via txt; returns numpy arrays

# to learn more about available data visit these links
crypto_list = "https://www.alphavantage.co/digital_currency_list"
fiat_list = "https://www.alphavantage.co/physical_currency_list"

import time
import requests
import numpy as np
from pprint import pprint
from json import dumps as json_dumps
from json import loads as json_loads
from multiprocessing import Process, Value

FULL = True
ATTEMPTS = 3
TIMEOUT = 60


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


def from_iso_date(date):  # returns unix epoch given YYYY-MM-DD
    return int(time.mktime(time.strptime(str(date), "%Y-%m-%d")))


def to_list_of_dicts_stocks(ret):
    data = []
    # change from dict of dicts to list of dicts;
    # rename keys, add unix
    for k, v in ret.items():
        v["unix"] = from_iso_date(k)
        v["open"] = v.pop("1. open")
        v["high"] = v.pop("2. high")
        v["low"] = v.pop("3. low")
        v["close"] = v.pop("4. close")
        v["volume"] = v.pop("6. volume")
        v["split"] = v.pop("8. split coefficient")
        data.append(v)
    # sort list of dicts by value of key unix
    return sorted(data, key=lambda k: k["unix"])


def to_list_of_dicts_forex(ret):
    data = []
    # change from dict of dicts to list of dicts;
    # rename keys, add unix
    for k, v in ret.items():
        v["unix"] = from_iso_date(k)
        v["open"] = v.pop("1. open")
        v["high"] = v.pop("2. high")
        v["low"] = v.pop("3. low")
        v["close"] = v.pop("4. close")
        v["volume"] = 1
        data.append(v)
    # sort list of dicts by value of key unix
    return sorted(data, key=lambda k: k["unix"])


def to_list_of_dicts_crypto(ret, currency):
    data = []
    # change from dict of dicts to list of dicts;
    # rename keys, add unix
    for k, v in ret.items():
        v["unix"] = from_iso_date(k)
        v["open"] = v.pop("1a. open (%s)" % currency)
        v["high"] = v.pop("2a. high (%s)" % currency)
        v["low"] = v.pop("3a. low (%s)" % currency)
        v["close"] = v.pop("4a. close (%s)" % currency)
        v["volume"] = v.pop("5. volume")
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


def remove_weekends(data):

    # remove weekends for backtesting discrete time
    depth = len(data["unix"])
    end = max(data["unix"])
    begin = end - depth * 86400
    data["unix"] = [u for u in range(begin, end, 86400)]
    return data


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


def stocks(signal, asset, currency, start, stop, period):

    days = int((stop - start) / float(period))
    # make api call for data
    if KEY == "":
        raise ValueError("YOU MUST GET API KEY FROM alphavantage.com")
    if period != 86400:
        raise ValueError("Daily Candles Only")
    outputsize = "compact"
    if FULL:
        outputsize = "full"
    uri = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "outputsize": outputsize,
        "symbol": asset,
        "apikey": KEY,
    }
    ret = requests.get(uri, params=params, timeout=(6, 30)).json()
    ret = ret["Time Series (Daily)"]
    # post process to extinctionEVENT format
    data = to_list_of_dicts_stocks(ret)
    data = to_dict_of_lists(data)
    data = remove_weekends(data)
    data = window(start, stop, data)
    # inter process communication via txt
    race_write("proxy.txt", json_dumps(data))
    signal.value = 1


def forex(signal, asset, currency, start, stop, period):

    days = int((stop - start) / float(period))
    # make api call for data
    if KEY == "":
        raise ValueError("YOU MUST GET API KEY FROM alphavantage.com")
    if period != 86400:
        raise ValueError("Daily Candles Only")
    outputsize = "compact"
    if FULL:
        outputsize = "full"
    uri = "https://www.alphavantage.co/query"
    params = {
        "function": "FX_DAILY",
        "outputsize": outputsize,
        "from_symbol": currency,
        "to_symbol": asset,
        "apikey": KEY,
    }
    ret = requests.get(uri, params=params, timeout=(6, 30)).json()

    ret = ret["Time Series FX (Daily)"]
    # post process to extinctionEVENT format
    data = to_list_of_dicts_forex(ret)
    data = to_dict_of_lists(data)
    data = remove_weekends(data)
    data = window(start, stop, data)
    # inter process communication via txt
    race_write("proxy.txt", json_dumps(data))
    signal.value = 1


def crypto(signal, asset, currency, start, stop, period):

    days = int((stop - start) / float(period))
    # make api call for data
    if KEY == "":
        raise ValueError("YOU MUST GET API KEY FROM alphavantage.com")
    if period != 86400:
        raise ValueError("Daily Candles Only")
    outputsize = "compact"
    if FULL:
        outputsize = "full"
    uri = "https://www.alphavantage.co/query"
    params = {
        "function": "DIGITAL_CURRENCY_DAILY",
        "outputsize": outputsize,
        "market": currency,
        "symbol": asset,
        "apikey": KEY,
    }
    ret = requests.get(uri, params=params, timeout=(6, 30)).json()

    print(ret)
    ret = ret["Time Series (Digital Currency Daily)"]

    # post process to extinctionEVENT format
    data = to_list_of_dicts_crypto(ret, currency)
    data = to_dict_of_lists(data)
    data = remove_weekends(data)
    data = window(start, stop, data)
    # inter process communication via txt
    race_write("proxy.txt", json_dumps(data))
    signal.value = 1


def proxySTX(asset, currency, start, stop, candle=86400):

    global KEY

    KEY = race_read_json(doc="apiKEYS.py")["alphavantage"]

    begin = time.time()
    start = int(start)
    stop = int(stop)
    period = int(candle)
    depth = int((stop - start) / 86400.0)

    print(
        (
            "API AlphaVantage Stocks %s %s %ss %se CANDLE %s DAYS %s"
            % (asset, currency, start, stop, period, depth)
        )
    )

    signal = Value("i", 0)
    i = 0
    while (i < ATTEMPTS) and not signal.value:
        i += 1
        print("")
        print("proxyALPHA attempt:", i, time.ctime())
        child = Process(
            target=stocks,
            args=(signal, asset, currency, start, stop, period),
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


def proxyFOX(asset, currency, start, stop, candle=86400):

    global KEY

    KEY = race_read_json(doc="apiKEYS.py")["alphavantage"]

    begin = time.time()
    start = int(start)
    stop = int(stop)
    period = int(candle)
    depth = int((stop - start) / 86400.0)

    print(
        (
            "API AlphaVantage Forex %s %s %ss %se CANDLE %s DAYS %s"
            % (asset, currency, start, stop, period, depth)
        )
    )

    signal = Value("i", 0)
    i = 0
    while (i < ATTEMPTS) and not signal.value:
        i += 1
        print("")
        print("proxyALPHA attempt:", i, time.ctime())
        child = Process(
            target=forex,
            args=(signal, asset, currency, start, stop, period),
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


def proxyCRY(asset, currency, start, stop, candle=86400):

    global KEY

    KEY = race_read_json(doc="apiKEYS.py")["alphavantage"]

    begin = time.time()
    start = int(start)
    stop = int(stop)
    period = int(candle)
    depth = int((stop - start) / 86400.0)

    print(
        (
            "API AlphaVantage Crypto %s %s %ss %se CANDLE %s DAYS %s"
            % (asset, currency, start, stop, period, depth)
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
            args=(signal, asset, currency, start, stop, period),
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
