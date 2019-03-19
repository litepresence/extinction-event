# ======================================================================
VERSION = "proxyDEX v0.00000002"
# ======================================================================

# ======================================================================
API = "BitShares Public API Nodes"
# ======================================================================

# HLOCV Smart Contract Candle Data from BitShares DEX Public Nodes

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
# 86400, 14400, 300 second candle sizes

# data['unix'] # discretely spaced integers
# data['high'] # linearly interpolated float
# data['low'] # linearly interpolated float
# data['open'] # linearly interpolated float
# data['close'] # linearly interpolated float
# data['volume'] # float

# get up to 1000 candles
# provide statistical mean data from several nodes in network
# encapsulated websocket call in time out multiprocess
# interprocess communication via txt; returns numpy arrays
# normalized, discrete, interpolated data arrays

from websocket import create_connection as wss  # handshake to node
from multiprocessing import Process, Value  # encapsulate processes
from json import dumps as json_dumps
from json import loads as json_loads
from operator import itemgetter
from collections import Counter
from datetime import datetime
from calendar import timegm
from random import shuffle
from pprint import pprint
import numpy as np
import traceback
import time

ATTEMPTS = 30
TIMEOUT = 480

# to learn more about available data visit these links
dex_asset_list = "http://cryptofresh.com/assets"


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


def public_nodes():
    # live since core 181127 and known to have market history
    return [
        "wss://altcap.io/wss",
        "wss://api-ru.bts.blckchnd.com/ws",
        "wss://api.bitshares.bhuz.info/wss",
        "wss://api.bitsharesdex.com/ws",
        "wss://api.bts.ai/ws",
        "wss://api.bts.blckchnd.com/wss",
        "wss://api.bts.mobi/wss",
        "wss://api.bts.network/wss",
        "wss://api.btsgo.net/ws",
        "wss://api.btsxchng.com/wss",
        "wss://api.dex.trading/ws",
        "wss://api.fr.bitsharesdex.com/ws",
        "wss://api.open-asset.tech/wss",
        "wss://atlanta.bitshares.apasia.tech/wss",
        "wss://australia.bitshares.apasia.tech/ws",
        "wss://bit.btsabc.org/wss",
        "wss://bitshares.crypto.fans/wss",
        "wss://bitshares.cyberit.io/ws",
        "wss://bitshares.dacplay.org/wss",
        "wss://bitshares.dacplay.org:8089/wss",
        "wss://bitshares.openledger.info/wss",
        "wss://blockzms.xyz/ws",
        "wss://bts-api.lafona.net/ws",
        "wss://bts-seoul.clockwork.gr/ws",
        "wss://bts.liuye.tech:4443/wss",
        "wss://bts.open.icowallet.net/ws",
        "wss://bts.proxyhosts.info/wss",
        "wss://btsfullnode.bangzi.info/ws",
        "wss://btsws.roelandp.nl/ws",
        "wss://chicago.bitshares.apasia.tech/ws",
        "wss://citadel.li/node/wss",
        "wss://crazybit.online/wss",
        "wss://dallas.bitshares.apasia.tech/wss",
        "wss://dex.iobanker.com:9090/wss",
        "wss://dex.rnglab.org/ws",
        "wss://dexnode.net/ws",
        "wss://england.bitshares.apasia.tech/ws",
        "wss://eu-central-1.bts.crypto-bridge.org/wss",
        "wss://eu.nodes.bitshares.ws/ws",
        "wss://eu.openledger.info/ws",
        "wss://france.bitshares.apasia.tech/ws",
        "wss://frankfurt8.daostreet.com/wss",
        "wss://japan.bitshares.apasia.tech/wss",
        "wss://kc-us-dex.xeldal.com/ws",
        "wss://kimziv.com/ws",
        "wss://la.dexnode.net/ws",
        "wss://miami.bitshares.apasia.tech/ws",
        "wss://na.openledger.info/ws",
        "wss://ncali5.daostreet.com/wss",
        "wss://netherlands.bitshares.apasia.tech/ws",
        "wss://new-york.bitshares.apasia.tech/ws",
        "wss://node.bitshares.eu/ws",
        "wss://node.market.rudex.org/wss",
        "wss://openledger.hk/wss",
        "wss://paris7.daostreet.com/wss",
        "wss://relinked.com/wss",
        "wss://scali10.daostreet.com/wss",
        "wss://seattle.bitshares.apasia.tech/wss",
        "wss://sg.nodes.bitshares.ws/ws",
        "wss://singapore.bitshares.apasia.tech/ws",
        "wss://status200.bitshares.apasia.tech/wss",
        "wss://us-east-1.bts.crypto-bridge.org/ws",
        "wss://us-la.bitshares.apasia.tech/ws",
        "wss://us-ny.bitshares.apasia.tech/ws",
        "wss://us.nodes.bitshares.ws/wss",
        "wss://valley.bitshares.apasia.tech/ws",
        "wss://ws.gdex.io/ws",
        "wss://ws.gdex.top/wss",
        "wss://ws.hellobts.com/wss",
        "wss://ws.winex.pro/wss",
    ]


def wss_handshake(node):
    global ws
    ws = wss(node, timeout=5)


def wss_send(params):
    query = json_dumps(
        {"method": "call", "params": params, "jsonrpc": "2.0", "id": 1}
    )
    ws.send(query)


def wss_receive():
    ret = json_loads(ws.recv())
    try:
        return ret["result"]  # if there is result key take it
    except:
        return ret


def rpc_market_history(currency_id, asset_id, period, start, stop):
    ret = wss_send(
        [
            "history",
            "get_market_history",
            [
                currency_id,
                asset_id,
                period,
                to_iso_date(start),
                to_iso_date(stop),
            ],
        ]
    )


def rpc_lookup_asset_symbols(asset, currency):
    ret = wss_send(
        ["database", "lookup_asset_symbols", [[asset, currency]]]
    )


def from_iso_date(date):  # returns unix epoch given iso8601 datetime
    return int(timegm(time.strptime(str(date), "%Y-%m-%dT%H:%M:%S")))


def to_iso_date(unix):  # returns iso8601 datetime given unix epoch
    return datetime.utcfromtimestamp(int(unix)).isoformat()


def parse_market_history(g_history, period):

    cp = currency_precision  # quote
    ap = asset_precision  # base

    history = []
    for i in range(len(g_history)):
        h = (float(int(g_history[i]["high_quote"])) / 10 ** cp) / (
            float(int(g_history[i]["high_base"])) / 10 ** ap
        )
        l = (float(int(g_history[i]["low_quote"])) / 10 ** cp) / (
            float(int(g_history[i]["low_base"])) / 10 ** ap
        )
        o = (float(int(g_history[i]["open_quote"])) / 10 ** cp) / (
            float(int(g_history[i]["open_base"])) / 10 ** ap
        )
        c = (float(int(g_history[i]["close_quote"])) / 10 ** cp) / (
            float(int(g_history[i]["close_base"])) / 10 ** ap
        )
        cv = float(int(g_history[i]["quote_volume"])) / 10 ** cp
        av = float(int(g_history[i]["base_volume"])) / 10 ** ap
        vwap = cv / av
        u = int(from_iso_date(g_history[i]["key"]["open"]) + period)
        history.append(
            {
                "high": h,
                "low": l,
                "open": o,
                "close": c,
                "vwap": vwap,
                "currency_v": cv,
                "asset_v": av,
                "unix": u,
            }
        )
    return history


def interpolate_previous(data, start, stop, period):

    start = int(start)
    stop = int(stop)
    period = int(period)

    x = [t for t in range(start, stop, period)]
    xp = data["unix"]
    v = []
    h = []
    l = []
    o = []
    c = []
    for i in x:
        for j in range(len(xp)):
            match = False
            diff = i - xp[j]
            if (0 <= diff) and (diff < period):
                v.append(data["volume"][j])
                h.append(data["high"][j])
                l.append(data["low"][j])
                o.append(data["open"][j])
                c.append(data["close"][j])
                match = True
        if not match:
            if i == start:
                close = data["close"][0]
            else:
                close = c[-1]
            v.append(0)
            h.append(close)
            l.append(close)
            o.append(close)
            c.append(close)
    data["high"] = h
    data["low"] = l
    data["open"] = o
    data["close"] = c
    data["volume"] = v
    data["unix"] = x

    return data


def reformat(data):
    # switch from list of dicts <-> to dict of lists
    d = {}
    d["unix"] = []
    d["high"] = []
    d["low"] = []
    d["open"] = []
    d["close"] = []
    d["volume"] = []
    for i in range(len(data)):
        d["unix"].append(data[i]["unix"])
        d["high"].append(data[i]["high"])
        d["low"].append(data[i]["low"])
        d["open"].append(data[i]["open"])
        d["close"].append(data[i]["close"])
        d["volume"].append(data[i]["currency_v"])
    return d


def normalize(d):

    for i in range(len(d["close"])):
        # normalize high and low data
        high = max(
            d["high"][i], d["low"][i], d["open"][i], d["close"][i]
        )
        low = min(
            d["high"][i], d["low"][i], d["open"][i], d["close"][i]
        )
        d["high"][i] = high
        d["low"][i] = low
        # filter extreme candles at 0.5X to 2X the open/close average
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

    return d


def truncate(d, depth):
    # truncate to depth requested
    d["unix"] = d["unix"][-depth:]
    d["high"] = d["high"][-depth:]
    d["low"] = d["low"][-depth:]
    d["open"] = d["open"][-depth:]
    d["close"] = d["close"][-depth:]
    d["volume"] = d["volume"][-depth:]
    return d


def dexdata(signal, asset, currency, start, stop, period, depth):

    global asset_id, asset_precision, currency_id, currency_precision

    if period not in [300, 14400, 86400]:
        raise ValueError("invalid period")

    window = int(period * 200)
    calls = min(5, (1 + int((stop - start) / float(window))))

    print("window", window, "calls", calls)
    # fetch node list and shuffle in place
    nodes = public_nodes()
    shuffle(nodes)
    # mavens will hold potential datasets
    mavens = []
    while True:
        try:
            # rotate nodes list
            nodes.append(nodes.pop(0))
            node = nodes[0]
            wss_handshake(node)
            # gather id and precision for asset and currency
            rpc_lookup_asset_symbols(asset, currency)
            ret = wss_receive()
            asset_id = ret[0]["id"]
            asset_precision = ret[0]["precision"]
            currency_id = ret[1]["id"]
            currency_precision = ret[1]["precision"]
            # make multiple calls for full dataset
            now = int(time.time()) + 1
            for i in range((calls - 1), -1, -1):
                g_start = now - (i + 1) * window
                g_stop = now - i * window
                print("   ", i, period, window, g_start, g_stop)
                rpc_market_history(
                    currency_id, asset_id, period, g_start, g_stop
                )
            data = []
            for i in range((calls - 1), -1, -1):
                ret = wss_receive()
                data += ret
            # convert from graphene to human readable candles
            data = parse_market_history(data, period)
            # resort by unix timestamp if any irregularities
            data = sorted(data, key=lambda k: k["unix"])
            # call multiple nodes until 3 duplicates are found
            if data:
                mavens.append(json_dumps(data))
            max_count = Counter(mavens).most_common(1)[0][1]
            print(max_count, node)
            if max_count == 3:
                break
        except Exception as e:
            trace(e)
            continue

    # switch from list of dicts <-> to dict of lists
    data = reformat(data)
    # ensure high is high, low is low, and extreme values are filtered
    data = normalize(data)
    # interpolate to fill in buckets with no price action
    data = interpolate_previous(data, start, stop, period)
    # limit lists to depth
    data = truncate(data, depth)
    # write data to file
    race_write("proxy.txt", json_dumps(data))
    # switch multiprocessing signal and end function
    signal.value = 1
    return


def trace(e):  # traceback message

    return (
        str(type(e).__name__)
        + str(e.args)
        + str(traceback.format_exc())
    )


def proxyDEX(asset, currency, start, stop, period):

    begin = time.time()
    start = int(start)
    period = int(period)
    # if ending point is in future adjust to now
    stop = min(int(stop), int(time.time()))
    # if request is more than 1000 candles adjust starting point
    depth = int((stop - start) / float(period))
    if depth > 1000:
        start = int(stop - (period * 1000))
        depth = 1000
    days = (stop - start) / 86400.0

    print(
        "RPC %s %s %ss %se CANDLE %s DAYS %.1f DEPTH %s"
        % (asset, currency, start, stop, period, days, depth)
    )
    if depth < 1:
        raise ValueError("no depth")

    # make several attempts to contact websocket
    # use text file interprocess communication
    signal = Value("i", 0)
    i = 0
    while (i < ATTEMPTS) and not signal.value:
        i += 1
        print("")
        print("proxyDEX attempt:", i, time.ctime())
        child = Process(
            target=dexdata,
            args=(signal, asset, currency, start, stop, period, depth),
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
