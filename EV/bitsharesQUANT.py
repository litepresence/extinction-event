"""
Algorithmic Trading and Backtesting Platform
litepresence 2019
************ ALPHA RELEASE TO PUBLIC DOMAIN WITH NO WARRANTY ***********
"""
import sys
import time
import warnings
import traceback
from calendar import timegm
from getpass import getpass
from datetime import datetime
from json import loads as json_loads
from ast import literal_eval as literal
from random import sample, choice
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import requests

# litepresence/extinction-event utilities
from proxyDEX import proxyDEX
from proxyCEX import proxyCEX
from synthDATA import synthDATA
from proxyALPHA import proxySTX, proxyFOX, proxyCRY
from metaNODE import Bitshares_Trustless_Client
from manualSIGNING import broker, prototype_order


# ======================================================================
VERSION = "Bitshares QUANT v0.00000002 pre-alpha"
# ======================================================================


def log_in(mode):
    """
    User Input for Wallet Import Format (WIF) Private Key
    """
    mode["wif"] = ""
    if mode["id"] in [3, 6]:
        print("DO NOT ENTER PASSWORD WITHOUT READING, UNDERSTANDING,")
        print("AND TAKING PERSONAL RESPONSIBILITY FOR THE CODE")
        print("")
        print("welcome back %s" % mode["account_name"])
        print("")
        authenticated = False
        while not authenticated:
            try:
                mode["wif"] = getpass(prompt="               WIF: ")
                print("\033[F              WIF: " + "********************************")
                print("")
                print("AUTHENTICATING to DEX wallet...")
                try:
                    authenticated = authenticate(mode)
                except Exception as error:
                    print(trace(error))
                if authenticated:
                    print("")
                    print(("*****************"))
                    print(("**AUTHENTICATED**") + (" YOUR WALLET IS UNLOCKED"))
                    print(("*****************"))
                else:
                    mode["wif"] = ""
                    print(("WIF does not match account name"))
            except Exception as error:
                print(error.args)
    return mode


def authenticate(mode):
    """
    Matches Private Key to Account Name via Public Key
    Calls manualSIGNING.py with broker(order) method
    """
    edicts = [{"op": "login"}]
    order = json_loads(prototype_order())
    order["header"]["wif"] = mode["wif"]
    order["edicts"] = edicts
    authenticated = broker(order)
    return authenticated


def cancel_all(mode):
    """
    Cancels all outstanding orders
    Calls manualSIGNING.py with broker(order) method
    """
    edicts = [{"op": "cancel", "ids": ["1.7.X"]}]
    order = json_loads(prototype_order())
    order["header"]["wif"] = mode["wif"]
    order["edicts"] = edicts
    if not mode["paper"]:
        broker(order)
    else:
        print(order)


def place_order(edicts, mode):
    """
    Places BUY and SELL orders given a list of edicts
    Calls manualSIGNING.py with broker(order) method
    """
    order = json_loads(prototype_order())
    order["header"]["wif"] = mode["wif"]
    order["edicts"] = edicts
    live_chart_edicts(edicts)
    if not mode["paper"]:
        broker(order)
    else:
        print(order)


def fee_maintainer(mode):
    """
    If holding less than 0.5 BTS, then buy 1.5 BTS
    Gathers balances via metaNODE.txt
    Calls manualSIGNING.py with broker(order) method
    Pays with market currency, unless BTS: Then pay with assets
    """
    metaNODE = Bitshares_Trustless_Client()
    nodes = metaNODE["whitelist"]
    precision = metaNODE["currency_precision"]
    account_name = metaNODE["account_name"]
    account_id = metaNODE["account_id"]
    bts = metaNODE["bts_balance"]
    cid = metaNODE["currency_id"]
    if metaNODE["currency"] == "BTS":
        cid = metaNODE["asset_id"]
        precision = metaNODE["asset_precision"]
    del metaNODE
    print("BTS Balance: %.2f" % bts)
    if bts < 0.5:
        order = {
            "edicts": [{"op": "buy", "amount": 1.5, "price": 99999, "expiration": 0}],
            "header": {
                "asset_id": "1.3.0",
                "currency_id": cid,
                "asset_precision": 5,
                "currency_precision": precision,
                "account_id": account_id,
                "account_name": account_name,
                "wif": mode["wif"],
            },
            "nodes": nodes,
        }
        if not mode["paper"]:
            broker(order)
        else:
            print(order)


def race_read(doc=""):
    """
    Concurrent Read from File Operation
    """
    i = 0
    while True:
        try:
            time.sleep(0.05 * i ** 2)
            i += 1
            with open(doc, "r") as handle:
                ret = handle.read()
                handle.close()
                try:
                    ret = literal(ret)
                except:
                    pass
                try:
                    ret = ret.split("]")[0] + "]"
                    ret = literal(ret)
                except:
                    pass
                try:
                    ret = ret.split("}")[0] + "}"
                    ret = literal(ret)
                except:
                    if "{" in ret:
                        ret = {}
                    else:
                        ret = []
                break
        except Exception as error:
            msg = str(type(error).__name__) + str(error.args)
            msg += " race_read()"
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
    return ret


def race_write(doc="", text=""):
    """
    Concurrent Write to File Operation
    """
    text = str(text)
    i = 0
    while True:
        try:
            time.sleep(0.05 * i ** 2)
            i += 1
            with open(doc, "w+") as handle:
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


def race_append(doc="", text=""):
    """
    Concurrent Append to File Operation
    """
    text = "\n" + str(time.ctime()) + " " + str(text) + "\n"
    i = 0
    while True:
        time.sleep(0.05 * i ** 2)
        i += 1
        if i > 10:
            break
        try:
            with open(doc, "a+") as handle:
                handle.write(text)
                handle.close()
                break
        except Exception as error:
            msg = str(type(error).__name__) + str(error.args)
            msg += " race_append()"
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


def watchdog():
    """
    Allows duplex keep alive communication to metaNODE
    """
    identity = 0  # metaNODE:1, botscript:0
    max_latency = 60
    warn = " !!!!! WARNING: the other app is not responding !!!!!"
    while True:
        try:
            try:
                with open("watchdog.txt", "r") as handle:
                    ret = handle.read()
                    handle.close()
                ret = literal(ret)
                response = int(ret[identity])
                now = int(time.time())
                latency = now - response
                if identity == 0:
                    msg = str([response, now])
                if identity == 1:
                    msg = str([now, response])
                with open("watchdog.txt", "w+") as handle:
                    handle.write(msg)
                    handle.close()
                msg = str(latency)
                if latency > max_latency:
                    msg += warn
                return msg
            except Exception as error:
                msg = str(type(error).__name__) + str(error.args)
                print(msg)
                now = int(time.time())
                with open("watchdog.txt", "w+") as handle:
                    handle.write(str([now, now]))
                    handle.close()
                    break
        except Exception as error:
            msg = str(type(error).__name__) + str(error.args)
            print(msg)
            try:
                handle.close()
            except:
                pass
        finally:
            try:
                handle.close()
            except:
                pass


def test_buy(order, portfolio, storage, info, tune, mode):
    """
    Execute a backtest BUY operation
    Updates Holdings, Plots, and Logs
    """
    storage["trades"] += 1
    now = info["current_time"]
    storage["buys"][0].append(info["current_time"])
    storage["buys"][1].append(order["price"])
    portfolio["assets"] = portfolio["currency"] / order["price"]
    storage["holding"] = True
    if mode["id"]:
        print(
            (
                "[%s] %s BUY %s %.2f %s at %.8f value %.2f %s"
                % (
                    time.ctime(now),
                    storage["trades"],
                    order["call"],
                    portfolio["assets"],
                    tune["asset"],
                    order["price"],
                    portfolio["currency"],
                    tune["currency"],
                )
            )
        )
        plt.plot(
            info["current_time"],
            (order["price"]),
            markersize=10,
            marker="^",
            color="lime",
            label="buy",
        )
        try:
            sell_price = float(storage["sells"][1][-1])
            sell_time = int(storage["sells"][0][-1])
            if order["price"] > sell_price:
                plt.plot(
                    (sell_time, now),
                    (sell_price, order["price"]),
                    color="coral",
                    label="loss",
                    lw=2,
                )
            else:
                plt.plot(
                    (sell_time, now),
                    (sell_price, order["price"]),
                    color="lime",
                    label="win",
                    lw=2,
                )
        except:
            pass
    portfolio["currency"] = 0


def test_sell(order, portfolio, storage, info, tune, mode):
    """
    Execute a backtest SELL operation
    Updates Holdings, Plots, and Logs
    """
    storage["trades"] += 1
    now = info["current_time"]
    storage["sells"][0].append(info["current_time"])
    storage["sells"][1].append(order["price"])
    portfolio["currency"] = portfolio["assets"] * order["price"]
    storage["holding"] = False
    if mode["id"]:
        print(
            (
                "[%s] %s SELL %s %.2f %s at %.8f value %.2f %s"
                % (
                    time.ctime(now),
                    storage["trades"],
                    order["call"],
                    portfolio["assets"],
                    tune["asset"],
                    order["price"],
                    portfolio["currency"],
                    tune["currency"],
                )
            )
        )
        plt.plot(
            info["current_time"],
            (order["price"]),
            markersize=10,
            marker="v",
            color="coral",
            label="sell",
        )
        try:
            buy_price = float(storage["buys"][1][-1])
            buy_time = int(storage["buys"][0][-1])
            if order["price"] > buy_price:
                plt.plot(
                    (buy_time, now),
                    (buy_price, order["price"]),
                    color="lime",
                    label="win",
                    lw=2,
                )
            else:
                plt.plot(
                    (buy_time, now),
                    (buy_price, order["price"]),
                    color="coral",
                    label="loss",
                    lw=2,
                )
        except:
            pass
    portfolio["assets"] = 0


def backtest_candles(start, stop, candle, mode, storage, tune):
    """
    For backtest daily candles, return slice of storage['max_data']
    For intraday make RPC to public BitShares Node
    """
    if candle == 86400:
        unix = storage["max_data"]["unix"]
        items = len(unix)
        stop = items - int(max(unix - mode["end"]) / 86400.0)
        start = max(0, (stop - storage["days"] - tune["max_period"] - 1))
        data = {k: v[start:stop] for k, v in storage["max_data"].items()}
    else:
        data = proxyDEX(tune["asset"], tune["currency"], start, stop, candle)
    return data


def slice_candles(now, data, candle, depth):
    """
    Window backtest_candles() data to test each candle
    """
    data_out = {}
    unix = data["unix"]
    for i in range(len(unix)):
        if (now <= unix[i]) and (unix[i] < (now + candle)):
            temp_high = []
            temp_low = []
            temp_open = []
            temp_close = []
            for j in range(depth):
                try:
                    temp_high.append(data["high"][i - j])
                    temp_low.append(data["low"][i - j])
                    temp_open.append(data["open"][i - j])
                    temp_close.append(data["close"][i - j])
                except:
                    pass
            data_out["high"] = np.array(temp_high[::-1])
            data_out["low"] = np.array(temp_low[::-1])
            data_out["open"] = np.array(temp_open[::-1])
            data_out["close"] = np.array(temp_close[::-1])
    return data_out


def live_candles(tune, candle, depth):
    """
    Current HLOCV arrays from Bitshares RPC to a given depth
    """
    now = int(time.time())
    data = proxyDEX(
        tune["asset"], tune["currency"], (now - (depth + 10) * candle), now, candle
    )
    data["unix"] = data["unix"][-depth:]
    data["high"] = data["high"][-depth:]
    data["low"] = data["low"][-depth:]
    data["open"] = data["open"][-depth:]
    data["close"] = data["close"][-depth:]
    data["volume"] = data["volume"][-depth:]
    return data


def live_initialize(mode, control, storage):
    """
    Reset global dictionaries in preparation for real-time session
    Set timing offset past the whole minute
    """
    print("~====== BEGIN LIVE SESSION =====================~")
    info = {}
    data = {}
    portfolio = {}
    edicts = []
    storage["trades"] = 0
    storage["previous_v"] = 0.00000001
    storage["holding_ticks"] = 0
    info["live"] = True
    info["tick"] = 0
    info["hour"] = 0
    info["day"] = 0
    info["end"] = None
    info["current_time"] = info["begin"] = int(time.time())
    if mode["id"] == 3:
        seconds_past = time.time() % 60
        offset = control["tick_timing"] - seconds_past
        if offset < 0:
            offset += 60
        print("")
        print(
            time.ctime(),
            "setting tick offset to",
            control["tick_timing"],
            "sleeping for",
            ("%.1f" % offset),
            "seconds",
        )
        time.sleep(offset)
    return storage, portfolio, info, data, edicts


def set_timing(control, info):
    """
    Ensures appropriate number of ticks per day
    """
    plt.pause(0.01)
    print("set_timing()")
    now = time.time()
    # time elapsed since live_initialize(tune, mode, storage, control, info, portfolio)
    elapsed = now - info["begin"]
    # ticks that should have occurred
    ticks = int(elapsed / control["tick"]) + 1
    # ticks that should have, less ticks that actually did occur
    tick_drift = ticks - info["tick"]
    # duration of the latest tick
    drift = info["tick"] * control["tick"] - elapsed
    wait = min(drift, control["tick"])
    print(
        "wait: %.2f, drift: %.2f, tick: %s, tick drift %s"
        % (wait, drift, info["tick"], tick_drift)
    )
    wait -= 10
    if wait > 0:
        plt.pause(wait)
    seconds_past = time.time() % 60
    offset = control["tick_timing"] - seconds_past
    if offset < 0:
        offset += 60
    plt.pause(offset)


def live_data(tune, storage, portfolio, data):
    """
    Gather live data from metaNODE and proxyDEX
    """
    plt.pause(0.01)
    print("live_data()")
    metaNODE = Bitshares_Trustless_Client()
    last = storage["last"] = float(metaNODE["last"])
    book = storage["book"] = metaNODE["book"]
    portfolio["currency"] = float(metaNODE["currency_balance"])
    portfolio["assets"] = float(metaNODE["asset_balance"])
    del metaNODE
    # orderbook and last price
    sbids = [("%.8f" % i) for i in book["bidp"][:3]]
    sbids = sbids[::-1]
    sasks = [("%.8f" % i) for i in book["askp"][:3]]
    # populate 4h and 5m candles to size needed for moving averages
    # tune['ma1'], tune['ma2'], MA3, MA4 are daily moving average periods
    depth_4h = 10 + tune["max_period"] * 6  # 6*4h = 24 hours
    depth_5m = 300
    data["14400"] = live_candles(tune, 14400, depth_4h)
    data["300"] = live_candles(tune, 300, depth_5m)
    # print top of book
    print(
        it("green", sbids), "< BIDS <", it("yellow", last), "> ASKS >", it("red", sasks)
    )
    return portfolio, data, storage


def hourly(info):
    """
    Repeat this process every hour
    """
    print(("hour: %s" % info["hour"]))


def daily(storage, info):
    """
    Repeat this process every day
    """
    if info["tick"] > 0:
        logo()  # clear terminal to prevent overflow
    now = int(time.time())
    ma2 = storage["ma2poly"][-1]
    print(("day: %s" % info["day"]))
    plt.plot(now, ma2, markersize=20, marker=".", color="white", label="daily")


def holdings(storage, info, data, portfolio):
    """
    Calculate starting portfolio and recurring updates
    """
    info["holdings"] = info.get("holdings", False)
    if not info["holdings"]:
        close = data["close"][-storage["days"]]
    else:
        close = storage["close"][-1]
    storage["max_assets"] = portfolio["assets"] + (portfolio["currency"] / close)
    storage["max_currency"] = portfolio["currency"] + (portfolio["assets"] * close)
    if not info["holdings"]:
        storage["begin_max_assets"] = storage["max_assets"]
        storage["begin_max_currency"] = storage["max_currency"]
        storage["start_price"] = close
    info["holdings"] = True
    return storage, info


def test_rechart_orders(storage):
    """
    Set buy/sell markers on top
    """
    for i in range(len(storage["sells"][0])):
        plt.plot(
            storage["sells"][0][i],
            (storage["sells"][1][i]),
            markersize=10,
            marker="v",
            color="coral",
            label="sell",
        )
    for i in range(len(storage["buys"][0])):
        plt.plot(
            storage["buys"][0][i],
            (storage["buys"][1][i]),
            markersize=10,
            marker="^",
            color="lime",
            label="buy",
        )


def test_stop(storage, portfolio, info, data, tune):
    """
    Display results of backtest session
    """
    assets = portfolio["assets"]
    currency = portfolio["currency"]
    close = storage["close"][-1]
    end_max_assets = assets + (currency / close)
    end_max_currency = currency + (assets * close)
    roi_assets = end_max_assets / storage["begin_max_assets"]
    roi_currency = end_max_currency / storage["begin_max_currency"]
    storage["roi_currency"] = roi_currency
    storage["roi_assets"] = roi_assets
    storage["roi_gross"] = (roi_currency * roi_assets) ** (1 / 2.0)
    days = (info["end"] - info["begin"]) / 86400.0
    frequency = (0.00000001 + storage["trades"]) / days
    storage["dpt"] = 1.0 / frequency
    print("==========================================================")
    print("START DATE........: %s" % time.ctime(info["begin"]))
    print("END DATE..........: %s" % time.ctime(info["end"]))
    print("DAYS..............: %.1f" % days)
    print("TICKS.............: %s" % info["tick"])
    print("HOLDING TICKS.....: %s" % storage["holding_ticks"])
    print("HOLDING RATIO.....: %.3f" % (storage["holding_ticks"] / info["tick"]))
    print("TRADES............: %s" % storage["trades"])
    print("DAYS PER TRADE....: %.1f" % storage["dpt"])
    print("START PRICE.......: %.8f " % data["close"][-storage["days"]])
    print("END PRICE.........: %.8f" % close)
    print("START MAX ASSETS..: %s %s" % (storage["begin_max_assets"], tune["asset"]))
    print("END MAX ASSETS....: %s %s" % (end_max_assets, tune["asset"]))
    print(("ROI ASSETS........: %.2fX" % roi_assets))
    print(
        "START MAX CURRENCY: %s %s" % (storage["begin_max_currency"], tune["currency"])
    )
    print("END MAX CURRENCY..: %s %s" % (end_max_currency, tune["currency"]))
    print("ROI CURRENCY......: %.2fX" % roi_currency)
    print("==========================================================")
    print("~===END BACKTEST=========================================~")


def live_chart_edicts(edicts):
    """
    plot all orders in edicts; a list of dicts
    op key of each dict is "buy" or "sell"
    """
    now = int(time.time())
    for edict in edicts:
        print("edict", edict)
        if edict["op"] == "buy":
            plt.plot(now, edict["price"], color="lime", marker="^", markersize=10)
        if edict["op"] == "sell":
            plt.plot(now, edict["price"], color="coral", marker="v", markersize=10)


def zoom_to_data():
    """
    change axis limits of plot to show all data
    """
    axis = plt.gca()
    ydata = []  # all y values on plot
    xdata = []  # all x values on plot
    for axis_line in range(len(axis.get_lines())):
        line = axis.get_lines()[axis_line]
        ydata.append((line.get_ydata()).tolist())
        xdata.append((line.get_xdata()).tolist())
    ydata = [item for sublist in ydata for item in sublist]
    ymin, ymax = np.min(ydata), np.max(ydata)
    axis.set_ylim([0.95 * ymin, 1.05 * ymax])
    xdata = [item for sublist in xdata for item in sublist]
    xmin, xmax = np.min(xdata), np.max(xdata)
    axis.set_xlim([xmin, xmax])
    plt.pause(0.01)
    return ymax, ymin, xmax, xmin


def plot_format(info, storage):
    """
    set plot colors and attributes
    """

    warnings.filterwarnings("ignore", category=cbook.mplDeprecation)
    axis = plt.gca()

    axis.patch.set_facecolor("0.1")
    axis.yaxis.tick_right()
    axis.spines["bottom"].set_color("0.5")
    axis.spines["top"].set_color(None)
    axis.spines["right"].set_color("0.5")
    axis.spines["left"].set_color(None)
    axis.tick_params(axis="x", colors="0.7", which="both")
    axis.tick_params(axis="y", colors="0.7", which="both")
    axis.yaxis.label.set_color("0.9")
    axis.xaxis.label.set_color("0.9")
    # plt.minorticks_on
    plt.grid(b=True, which="major", color="0.2", linestyle="-")
    plt.grid(b=True, which="minor", color="0.2", linestyle="-")
    if (info["live"] is False) and (info["tick"] > 1):
        plt.ylabel("LOGARITHMIC PRICE SCALE")
        plt.yscale("log")
    if info["live"] is True:
        plt.ylabel("MARKET PRICE")
    satoshi_format = matplotlib.ticker.FormatStrFormatter("%.8f")
    axis.yaxis.set_major_formatter(satoshi_format)
    axis.yaxis.set_minor_formatter(satoshi_format)
    axis.title.set_color("darkorchid")

    # custom x axis label spacing
    stepsize = 86400
    if info["live"]:
        stepsize = 7200
    else:
        if storage["days"] > 20:
            stepsize = 864000
        if storage["days"] > 100:
            stepsize = 2592000
        if storage["days"] > 1000:
            stepsize = 25920000
    start, end = axis.get_xlim()
    axis.xaxis.set_ticks(np.arange((end - end % 3600), start, -stepsize))

    def iso(x, pos):
        """
        format x axis labels with ISO style timestamps
        """
        if not info["live"]:
            iso_format = "%Y-%m-%d"
        else:
            iso_format = "%m/%d %H:%M"
        return (datetime.fromtimestamp(x)).strftime(iso_format)

    axis.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(iso))

    # custom log scale y axis label spacing
    if info["tick"] > 1:
        ymax, ymin, xmax, xmin = zoom_to_data()
        if info["live"] is False:
            # add sub minor ticks
            set_sub_formatter = []
            sub_ticks = [10, 11, 12, 14, 16, 18, 22, 25, 35, 45]
            sub_range = [-8, 8]
            for coeff in sub_ticks:
                for power in range(sub_range[0], sub_range[1]):
                    set_sub_formatter.append(coeff * 10 ** power)
            labels = []
            for label in set_sub_formatter:
                if ymin < label < ymax:
                    labels.append(label)
            axis.set_yticks(labels)
    # live y axis tick spacing
    if info["live"]:
        start, end = axis.get_ylim()
        stepsize = abs(start - end) / 25
        axis.yaxis.set_ticks(np.arange(end, start, -stepsize))
    plt.tight_layout()
    # bitshares_vector_logo()
    axis.yaxis.tick_right()
    axis.xaxis.tick_bottom()
    plt.gcf().autofmt_xdate(rotation=30)

    if info["live"]:
        plt.pause(0.001)


def trace(error):  
    """
    Stack trace report upon exception
    """
    print(error.args)
    return (
        "========================================================"
        + "\n\n"
        + str(time.ctime())
        + " "
        + str(type(error).__name__)
        + "\n\n"
        + str(error.args)
        + "\n\n"
        + str(traceback.format_exc())
        + "\n\n"
    )


def announce_version(version):
    """
    Set Terminal Window Label and Announce Version
    """
    sys.stdout.write("\x1b]2;" + version + "\x07")
    print("")
    print(version)
    print("")


def logo():
    """
    flaming Extintion Event logo
    """

    def download_text(key):
        """
        ascii artwork stored in pastebin
        """
        urls = {"extinction-event": "https://pastebin.com/raw/5YuEHcC4"}
        try:
            return (requests.get(urls[key], timeout=(6, 30))).text
        except:
            return ""

    def r_y():
        """
        random flame color effect
        """
        return choice(["red", "yellow"])

    ev_logo = download_text("extinction-event")
    a = r"""            *.   ~          %             `     ,        """
    b = r"""      *.()      *`()      *~()    @      *,()      *.()  """
    c = r"""    *()/     *()/\     *()/\%   % @       *()/\     *()/ """
    d = r""" ()/_ ()/\_ ()/_ ()/_ ()/_ ()/_ ()()() ()(@@)_ ()()()()()"""
    for i in range(20):
        print("\033c")
        print("     " + " ".join([it(r_y(), i) for i in sample(a, 27)]))
        print("     " + " ".join([it(r_y(), i) for i in sample(a, 27)]))
        print("     " + " ".join([it(r_y(), i) for i in sample(a, 27)]))
        print("     " + " ".join([it(r_y(), i) for i in sample(b, 27)]))
        print("    " + " ".join([it(r_y(), i) for i in sample(c, 28)]))
        print("   " + " ".join([it(r_y(), i) for i in sample(c, 29)]))
        print("    " + " ".join([it(r_y(), i) for i in sample(d, 28)]))
        print("     " + " ".join([it(r_y(), i) for i in sample(d, 27)]))
        print(it("yellow", ev_logo))
        print("")
        time.sleep(0.1)


def it(style, text):
    """
    colored text in terminal
    """
    emphasis = {
        "red": 91,
        "green": 92,
        "yellow": 93,
        "blue": 94,
        "purple": 95,
        "cyan": 96,
    }
    return ("\033[%sm" % emphasis[style]) + str(text) + "\033[0m"


def clock():
    """
    current 24 hour clock, local time, formatted HH:MM:SS
    """
    return str(time.ctime())[11:19]


def satoshi(number):
    """
    float prices rounded to satoshi
    """
    return float("%.8f" % float(number))


def satoshi_str(number):
    """
    string prices rounded to satoshi
    """
    return "%.8f" % float(number)


def dictionaries():
    """
    primary dictionaries used in global space
    """
    info = {}  # tick data
    storage = {}  # candle data
    portfolio = {}  # account balance data
    return info, storage, portfolio


def from_iso_date(date):
    """
    used for mode['end'] point of backtest ISO to UNIX conversion
    """
    return int(timegm(time.strptime(str(date), "%Y-%m-%d")))


def moving_average(array, period):
    """
    numpy array moving average
    """
    csum = np.cumsum(array, dtype=float)
    csum[period:] = csum[period:] - csum[:-period]
    return csum[period - 1 :] / period


def float_period(array, period):
    # float_period(function, array, period):
    """
    floating point period indications
    the weighted average of the integer periods n and n+1
    above/below desired float period
    weighted towards the n period
    """
    if period == int(period):
        indicator = moving_average(array, int(period))
    else:
        floor_period = int(period)
        ceil_period = int(floor_period + 1)
        floor_ratio = ceil_period - period
        ceil_ratio = 1.0 - floor_ratio
        floor = moving_average(array, floor_period)
        ceil = moving_average(array, ceil_period)
        depth = min(len(floor), len(ceil))
        floor = floor[-depth:]
        ceil = ceil[-depth:]
        indicator = (floor_ratio * floor) + (ceil_ratio * ceil)
    return indicator


def draw_live_chart_zero(data):
    """
    initializes last 24 hours of 10 minute candles
    """
    high = data["300"]["high"]
    low = data["300"]["low"]
    close = data["300"]["close"]
    unix = data["300"]["unix"]
    for i in range(len(unix)):
        now = unix[i]
        plt.plot((now, now), (high[i], low[i]), color="magenta", label="high/low")
        if high[i] > close[i]:
            plt.plot(
                now, high[i], markersize=4, marker=".", color="magenta", label="high"
            )
        if low[i] < close[i]:
            plt.plot(
                now, low[i], markersize=4, marker=".", color="magenta", label="low"
            )
        plt.plot(now, close[i], markersize=4, marker=".", color="yellow", label="close")


def draw_live_chart(info, data, storage):
    """
    Append real time 10 minute candles
    """
    if info["tick"] == 0:
        draw_live_chart_zero(data)
    # localize high frequency indicators
    now = int(time.time())
    low = storage["low"]
    high = storage["high"]
    last = storage["last"]
    book = storage["book"]
    ask = book["askp"][0]
    bid = book["bidp"][0]
    m_volume = storage["m_volume"]
    # plot high and low
    plt.plot((now, now), (high, low), color="m", label="high/low")
    if high > last:
        plt.plot(now, high, markersize=4, marker=".", color="magenta", label="high")
    if low < last:
        plt.plot(now, low, markersize=4, marker=".", color="magenta", label="low")
    # plot top of orderbook
    plt.plot(now, ask, markersize=3, marker=".", color="teal", label="ask")
    plt.plot(now, bid, markersize=3, marker=".", color="teal", label="bid")
    # plot last price
    plt.plot(
        now, last, markersize=(4 * m_volume), marker=".", color="yellow", label="last"
    )
    plt.pause(0.001)


def draw_test_chart(info, storage):
    """
    Plot high low and close on backtest
    """
    try:
        now = info["current_time"]
        close = storage["close"]
        high = storage["high"]
        low = storage["low"]
        # plot candles
        plt.plot(
            (now, now),
            ((high[-1]), (low[-1])),
            color="magenta",
            alpha=0.5,
            label="high_low",
        )
        plt.plot(
            now, (close[-1]), markersize=4, marker=".", color="yellow", label="close"
        )
    except Exception as error:
        print(error.args)


def test_plot(info, mode):
    """
    Set backtest plot limits, remove data out of window
    """
    begin = info["begin"]
    end = info["end"]
    while (end - begin) > 86400:
        # PLOT FORMAT
        try:
            axis = plt.gca()
            # Window Plot
            axis.set_xlim(left=begin - 50, right=end + 50)
            # Prevent Memory Leak Outside Plot Window
            for line in axis.get_lines():
                xval = line.get_xdata()[0]
                if int(xval) < begin:
                    line.remove()
            if mode["live"]:
                begin = begin + 0.3 * (end - begin)
            else:
                begin = end
            plt.tight_layout()
        except Exception as error:
            print("animated test plot failed", error.args)


def live_plot(info):
    """
    Set live plot limits, remove data out of window
    """
    now = int(time.time())
    axis = plt.gca()
    axis.set_xlim([(now - 86400), (now + 86400)])
    # Prevent Memory Leak Outside Plot Window; remove unnecessary data
    for line in axis.get_lines():
        xval = line.get_xdata()[0]
        if xval < (axis.get_xlim()[0]):
            line.remove()
            del line
        if info["tick"] == 0:
            if xval > time.time():
                line.remove()
                del line
    plt.tight_layout()
    plt.pause(0.0001)


def select_mode(tune):
    """
    Primary user input for live / backtest, etc.
    """
    mode = {}
    mode["id"] = 999
    print(
        "0:OPTIMIZE 1:BACKTEST 2:PAPER" + " 3:LIVE 4:SALES 5:LIVE DEBUG 6:LIVE TEST \n"
    )
    while mode["id"] not in [0, 1, 2, 3, 4, 5, 6]:
        mode["id"] = int(input("CHOSE TRADING MODE: "))
    print("")
    if mode["id"] == 6:
        print("WARNING TESTING LIVE WITH FUNDS:")
        print("This mode will repeatedly buy/sell/cancel")
        print("0.1 assets on 20% spread.")
        print("Monitor with microDEX.py \n")
        time.sleep(10)
    if mode["id"] in [2, 3, 5, 6]:
        metaNODE = Bitshares_Trustless_Client()
        asset = metaNODE["asset"]
        currency = metaNODE["currency"]
        mode["account_name"] = metaNODE["account_name"]
        del metaNODE
        pair = asset + ":" + currency
        if pair != tune["pair"]:
            raise ValueError("tune['pair'] != metaNODE['pair']")
    mode["optimize"] = False
    mode["backtest"] = False
    mode["paper"] = False
    mode["live"] = False
    mode["sales"] = False
    mode["live_debug"] = False
    mode["live_test"] = False
    if mode["id"] == 0:
        mode["optimize"] = True
    if mode["id"] == 1:
        mode["backtest"] = True
    if mode["id"] == 2:
        mode["live"] = True
        mode["paper"] = True
    if mode["id"] == 3:
        mode["live"] = True
    if mode["id"] == 4:
        mode["backtest"] = True
        mode["sales"] = True
    if mode["id"] == 6:
        mode["live"] = True
        mode["paper"] = True
        mode["live_debug"] = True
    if mode["id"] == 6:
        mode["live"] = True
        mode["live_test"] = True
    mode["candle"] = 86400
    if mode["live"]:
        mode["candle"] = 14400
    return mode


def print_tune(tune, storage):
    """
    Display storage and tune dictionaries
    """
    storage["roi_currency"] = storage.get("roi_currency", 1)
    storage["roi_assets"] = storage.get("roi_assets", 1)
    storage["roi_gross"] = storage.get("roi_gross", 1)
    storage["dpt"] = storage.get("dpt", 1)
    storage["trades"] = storage.get("trades", 0)
    print("#######################################")
    print("# %s" % time.ctime())
    print("#######################################")
    print("# DAYS          : %s" % storage["days"])
    print("# DPT           : %.1f" % storage["dpt"])
    print("# ROI CURRENCY  : %.2fX" % storage["roi_currency"])
    print("# ROI ASSETS    : %.2fX" % storage["roi_assets"])
    print("# ROI GROSS     : %.2fX" % storage["roi_gross"])
    print("# TUNE DATE     : %s" % time.ctime())
    print("#######################################")
    for key, value in tune.items():
        print(('tune["' + str(key) + '"]').ljust(20), "=", value)


def adjust_mode(tune, mode, control):
    """
    Adjust depth of arrays to max period
    Set max assets and currency to zero in paper mode
    Limit end of backtest to current time
    """
    mode["depth"] = int(tune["max_period"] * (86400 / mode["candle"]) + 10)
    mode["end"] = int(min(time.time(), from_iso_date(control["end"])))
    mode["max_assets"] = control["max_assets"]
    mode["max_currency"] = control["max_currency"]
    if mode["id"] == 2:
        mode["max_assets"] = 0
        mode["max_currency"] = 0
    if mode["id"] == 3:
        print(("BOT MAY SPEND:     ", mode["max_assets"], "PERCENT ASSETS"))
        print(("BOT MAY LIQUIDATE: ", mode["max_currency"], "PERCENT CURRENCY"))
    return mode


def initialize(tune, mode, storage, control):
    """
    Gather backtest data, adjust test days, create plot figure
    """
    # Open plot, set backtest days
    if mode["live"]:
        cancel_all(mode)
        print("checking with metaNODE watchdog before live session...")
        watchdog()
    if mode["id"] == 0:
        print("~=== OPTIMIZING 1D CANDLES =================~")
    if mode["id"] == 1:
        print("~=== BEGIN BACKTEST 1D CANDLES =============~")
    if mode["id"] == 2:
        print("~=== WARMING UP PAPER SESSION 4H CANDLES ===~")
    if mode["id"] in [3, 5, 6]:
        print("")
        print("")
        print("NOTE: ALPHA RELEASE TO PUBLIC DOMAIN WITH NO WARRANTY")
        print("")
        print("")
        print("~=== WARMING UP LIVE MACHINE 4H CANDLES ====~")
    if mode["id"] in [2, 3]:
        print("This will take a few minutes...")
    now = int(time.time())
    days = 100000
    storage["max_data"] = {}
    if mode["live"] or mode["paper"]:
        days = control["warmup"]
    else:
        if tune["data_source"] == "DEX":
            days = 1000
            storage["max_data"] = proxyDEX(
                tune["asset"], tune["currency"], (now - 86400 * 1000), now, 86400
            )
        if tune["data_source"] == "CEX":
            storage["max_data"] = proxyCEX(
                tune["asset"], tune["currency"], 1390000000, now, 86400
            )
            days = len(storage["max_data"]["unix"])
            # filter glitches in early datasets
            if tune["asset"] == "BTS":
                days -= 250
                if tune["currency"] == "BITCNY":
                    days -= 200
            elif tune["asset"] == "DASH":
                days -= 360
            elif tune["asset"] == "NXT":
                days -= 300
            else:
                days -= 100
        if tune["data_source"] == "STX":
            storage["max_data"] = proxySTX(
                tune["asset"], tune["currency"], 0, now, 86400
            )
        if tune["data_source"] == "FOX":
            storage["max_data"] = proxyFOX(
                tune["asset"], tune["currency"], 0, now, 86400
            )
        if tune["data_source"] == "CRY":
            storage["max_data"] = proxyCRY(
                tune["asset"], tune["currency"], 0, now, 86400
            )
        if tune["data_source"] == "SYN":
            storage["max_data"] = synthDATA()
    days = days - mode["depth"] * (86400 / mode["candle"])
    storage["days"] = int(min(days, control["days"]))
    if mode["live"] or mode["backtest"]:
        plt.ion()
        fig = plt.figure()
        fig.patch.set_facecolor("0.15")
        fig.canvas.set_window_title("BitShares QUANT")

    return storage


def test_initialize(tune, mode, storage, control, info, portfolio):
    """
    Set initial info, storage, and portfolio values
    """

    # Begin backtest session
    now = int(time.time())
    # initialize storage
    storage["trades"] = 0
    storage["buys"] = [[], []]
    storage["sells"] = [[], []]
    storage["holding"] = True
    storage["holding_ticks"] = 0
    storage["bull_market"] = control["bull_market"]
    # initialize portfolio balances
    portfolio["assets"] = float(control["start_assets"])
    portfolio["currency"] = float(control["start_currency"])
    # initialize info dictionary objects
    info["end"] = int(min(now, mode["end"]))
    info["begin"] = info["end"] - storage["days"] * 86400
    if mode["live"] or mode["paper"]:
        info["end"] = now
        info["begin"] = int(info["end"] - 86400 * control["warmup"])
    info["origin"] = int(
        info["begin"] - tune["max_period"] * 86400 - 2 * mode["candle"]
    )
    info["current_time"] = info["begin"]
    info["live"] = False
    info["tick"] = 0
    dataset_days = int((now - info["begin"]) / 86400.0)
    backtest_days = int((now - info["origin"]) / 86400.0)
    print(info["origin"], time.ctime(info["origin"]), "origin")
    print(info["begin"], time.ctime(info["begin"]), "begin")
    print(info["end"], time.ctime(info["end"]), "end")
    print("Dataset.....: %s DAYS" % dataset_days)
    print("Backtesting.: %s DAYS" % backtest_days)
    # check for compatible interval
    if mode["candle"] not in [14400, 86400]:
        raise ValueError("Tick Interval must be in [14400, 86400]")
    # gather complete data set for backtest
    if mode["live"] or mode["backtest"]:
        data = backtest_candles(
            info["origin"], now, mode["candle"], mode, storage, tune
        )
        # print pair candle orgin and begin
        print("")
        print("PAIR......: %s" % tune["pair"])
        print("")
        print("CANDLE....: %s" % mode["candle"])
        print("ORIGIN....: %s %s" % (info["origin"], time.ctime(info["origin"])))
        print("BEGIN.....: %s %s" % (info["begin"], time.ctime(info["begin"])))
        plot_format(info, storage)

    return storage, portfolio, info, data


# ======================================================================
# EXTINCTION EVENT
# ======================================================================
#
# THE DESTROYER,
# litepresence - 2019
#
