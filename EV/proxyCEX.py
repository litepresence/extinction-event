# ======================================================================
VERSION = "proxyCEX v0.00000001"
# ======================================================================

# ======================================================================
API = "www.cryptocompare.com"  # GET FREE API KEY HERE
# ======================================================================

# Daily HLOCV 3000+ Altcoin:Altcoin Candle Data from cryptocompare.com

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
# daily candles only, 86400

# data['unix'] # integers
# data['high'] # float
# data['low'] # float
# data['open'] # float
# data['close'] # float
# data['volume'] # float

# up to 2000 candles of daily historical data
# synthesizes altcoin1/altcoin2 and altcoin/fiat data
# encapsulated http call in time out multiprocess
# interprocess communication via txt; returns numpy arrays
# normalize data arrays: high never more than 2x; low no less than 0.5x

from multiprocessing import Process, Value  # encapsulate processes
from json import dumps as json_dumps  # serialize object to string
from json import loads as json_loads  # deserialize string to object
import numpy as np
import requests
import time

SYNTHESIS = 4
ATTEMPTS = 3
TIMEOUT = 60

# to learn more about available data visit these links
altcoin_list = "https://www.cryptocompare.com/coins/list/USD/1"


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


def synthesize(signal, asset, currency, start, stop, period):

    # before sending request on to cryptocompare
    # allow for altcoin/altcoin pairs
    # (asset1/BTC) / (asset2/BTC)

    # this synthetic process can introduce abberations in dataset
    # SYNTHESIS in tune_install allows for reconstruction control

    # cryptocompare returns dictionary with
    # {"time","close","high","low","open","volumefrom","volumeto"}

    if currency == "BTC":
        data = cryptocompare(asset, currency, start, stop, period)

    elif (currency in ["USD", "CNY"]) and (asset == "BTC"):
        data = cryptocompare(asset, currency, start, stop, period)

    else:

        dataset1 = cryptocompare("BTC", asset, start, stop, period)
        dataset2 = cryptocompare("BTC", currency, start, stop, period)
        minlen = min(len(dataset1), len(dataset2))
        dataset1 = (dataset1)[-minlen:]
        dataset2 = (dataset2)[-minlen:]
        dataset3 = []

        for i in range(len(dataset1)):

            d1_h = dataset1[i]["high"]
            d2_h = dataset2[i]["high"]
            d1_l = dataset1[i]["low"]
            d2_l = dataset2[i]["low"]
            d1_o = dataset1[i]["open"]
            d2_o = dataset2[i]["open"]
            d1_c = dataset1[i]["close"]
            d2_c = dataset2[i]["close"]
            time = dataset1[i]["time"]
            _close = d1_c / d2_c
            _open = d1_o / d2_o

            # various high/low synthesis SYNTHESISs can be entertained

            # most simply
            if SYNTHESIS == 0:
                _high = d1_h / d2_c
                _low = d1_l / d2_c
            # most unrealistic profitable
            if SYNTHESIS == 1:
                _high = d1_h / d2_l
                _low = d1_l / d2_h
            # most conservative least profitable
            if SYNTHESIS == 2:
                _high = d1_h / d2_h
                _low = d1_l / d2_l
            # halfway between 1 and 2
            if SYNTHESIS == 3:
                _high = ((d1_h + d1_c) / 2) / ((d2_l + d2_c) / 2)
                _low = ((d1_l + d1_c) / 2) / ((d2_h + d2_c) / 2)
            # most thoughtful / likely
            if SYNTHESIS == 4:
                _high = (d1_h / d2_c) / 2 + (d1_c / d2_l) / 2
                _low = (d1_l / d2_c) / 2 + (d1_c / d2_h) / 2

            _low = min(_high, _low, _open, _close)
            _high = max(_high, _low, _open, _close)

            volumefrom = dataset1[i]["volumefrom"]
            volumeto = dataset1[i]["volumeto"]
            candle = {
                "time": time,
                "close": _close,
                "high": _high,
                "low": _low,
                "open": _open,
                "volumefrom": volumefrom,
                "volumeto": volumeto,
            }
            dataset3.append(candle)
        data = dataset3
    reformat(signal, data)


def cryptocompare(asset, currency, start, stop, period):

    # make api call with requests module
    # {"time","close","high","low","open","volumefrom","volumeto"}
    # docs at https://www.cryptocompare.com/api/
    if KEY == "":
        raise ValueError("YOU MUST GET API KEY FROM cryptocompare.com")
    if period != 86400:
        raise ValueError("Daily Candles Only")

    while True:
        try:
            uri = "https://min-api.cryptocompare.com/data/histoday"
            # prepare parameters per required format
            fsym = asset
            tsym = currency
            toTs = int(stop)
            candles = int((stop - start) / float(period))
            limit = 10 + candles
            calls = 1 + int(limit / 2000.0)
            print("calls", calls)
            limit = min(limit, 2000)
            window = 2000 * 86400
            data = []
            now = int(time.time())
            # make multiple calls for needed depth
            for i in range((calls - 1), -1, -1):
                toTs = now - i * window
                params = {
                    "fsym": fsym,
                    "tsym": tsym,
                    "limit": limit,
                    "aggregate": 1,
                    "toTs": toTs,
                }
                print("params", params)
                headers = {"Apikey": KEY}
                ret = requests.get(
                    uri, params=params, headers=headers, timeout=(6, 30)
                ).json()
                d = ret["Data"]
                d = [i for i in d if i["close"] > 0]
                data += d
            data = data[-candles:]
            if data:
                return data

        except Exception as e:
            msg = trace(e)
            print(msg, "chartdata() failed; try again...")
            continue


def reformat(signal, data):

    d = {}
    d["unix"] = []
    d["high"] = []
    d["low"] = []
    d["open"] = []
    d["close"] = []
    d["volume"] = []
    # switch from list of candles to dictionary of lists
    for i in range(len(data)):
        d["unix"].append(data[i]["time"])
        d["high"].append(data[i]["high"])
        d["low"].append(data[i]["low"])
        d["open"].append(data[i]["open"])
        d["close"].append(data[i]["close"])
        d["volume"].append(data[i]["volumefrom"])

    normalize(signal, d)


def normalize(signal, d):

    # normalize high and low data
    for i in range(len(d["close"])):
        h = max(d["high"][i], d["low"][i], d["open"][i], d["close"][i])
        l = min(d["high"][i], d["low"][i], d["open"][i], d["close"][i])
        d["high"][i] = h
        d["low"][i] = l
        d["high"][i] = min(d["high"][i], (d["open"][i] + d["close"][i]))
        d["open"][i] = min(d["open"][i], (d["open"][i] + d["close"][i]))
        d["close"][i] = min(
            d["close"][i], (d["open"][i] + d["close"][i])
        )
        d["low"][i] = max(
            d["low"][i], (d["open"][i] + d["close"][i]) / 4
        )
        d["open"][i] = max(
            d["open"][i], (d["open"][i] + d["close"][i]) / 4
        )
        d["close"][i] = max(
            d["close"][i], (d["open"][i] + d["close"][i]) / 4
        )

    race_write("proxy.txt", json_dumps(d))
    signal.value = 1
    return


def trace(e):  # traceback message

    msg = str(type(e).__name__) + str(e.args)
    return msg


def proxyCEX(asset, currency, start, stop, period):

    global KEY

    KEY = race_read_json(doc="apiKEYS.py")["cryptocompare"]

    begin = time.time()
    start = int(start)
    stop = int(stop)
    period = int(period)

    print(
        (
            "API cryptocompare %s %s %ss %se CANDLE %s DAYS %s"
            % (
                asset,
                currency,
                start,
                stop,
                period,
                int((stop - start) / 86400.0),
            )
        )
    )

    signal = Value("i", 0)
    i = 0
    while (i < ATTEMPTS) and not signal.value:
        i += 1
        print("")
        print("proxyCEX attempt:", i, time.ctime())
        child = Process(
            target=synthesize,
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
