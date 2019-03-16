# ======================================================================
VERSION = "Bitshares extinctionEVENT v0.00000014"
# ======================================================================

# Algorithmic Trading and Backtesting Platform

" litepresence 2019 "


def WTFPL_v0_March_1765():
    if any([stamps, licenses, taxation, regulation, fiat, etat]):
        try:
            print("no thank you")
        except:
            return [tar, feathers]


" ********** ALPHA RELEASE TO PUBLIC DOMAIN WITH NO WARRANTY ********* "


# standard python modules
import os
import sys
import time
import math
import requests
import warnings
import traceback
from calendar import timegm
from getpass import getpass
from datetime import datetime
from json import loads as json_loads
from json import dumps as json_dumps
from ast import literal_eval as literal  # race read and watchdog
from random import random, randint, sample, choice

# dependencies
import matplotlib
import numpy as np
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import matplotlib.dates as mdates

# litepresence/extinction-event utilities
from proxyDEX import proxyDEX
from proxyCEX import proxyCEX
from proxyALPHA import proxySTX, proxyFOX, proxyCRY
from metaNODE import Bitshares_Trustless_Client
from manualSIGNING import broker, prototype_order

# Google Agorism
SATOSHI = 0.00000001
ANTISAT = 1 / SATOSHI
# BitShares Chain Identifier
ID = "4018d7844c78f6a6c41c6a552b898022310fc5dec06da467ee7905a8dad512c8"


def banner():
    """

    Bitshares DEX for live trading and backtesting
    Cryptocompare and AlphaVantage API's for backtesting

    - Play simple effective 4 state 50 day cross

        - uses live 4h arrays to generate moving averages
        - ma1xma2 is about 17x50 day simple moving average cross
        - cross plus +/- threshold changes state logic from bull to bear
        - Bull Logic
            buy 17 day support
            sell 17 day x ~1.5 selloff
        - Bear logic
            sell 17 day resistance
            buy 17 day x ~0.75 despair

    - Dynamic stoploss upon market shift
    - Approximately 7-20 day trade frequency depending upon pair
    - Announces machine state on plot
    - Iceberg entry and exit
    - Scalp ops updated every 10 minutes
    - Bot runs local
    - Backtest Engine included for optimizing thresholds
    - Maintains storage from backtest to live session

    h/t @ cryptocompare.com w/ 2000+ altcoin pairs of market data
    h/t to crew at BitsharesDEV telegram
    """


# USER CONTROLS
# ======================================================================


def tune_install():  # Basic User Controls

    global CURRENCY, ASSET, MA1, MA2, CANDLE_SOURCE, GRAVITAS
    global SELLOFF, SUPPORT, RESISTANCE, DESPAIR
    global MIN_CROSS, MAX_CROSS, BULL_STOP, BEAR_STOP

    # ==================================================================
    "GRAVITAS"
    # ==================================================================
    # though an algorithm is "perfectly tuned" to old data
    # inadequate volume at extremes can occur in the more mature market
    # override tune_install() thresholds conservatively by 0.01 = 1%
    # applies to despair, resistance, support, selloff
    GRAVITAS = 0.00  # use 0.00 for backtesting
    # 0.00-0.05 for final testing and when live
    # ==================================================================
    "DATA SOURCE EXAMPLE"
    # ==================================================================
    SOURCE = 1  # choose data source

    if SOURCE == 1:
        # bitshares dex           smart contracts (backtest and LIVE)
        CANDLE_SOURCE = "DEX"
        CURRENCY = "OPEN.BTC"
        ASSET = "BTS"

    if SOURCE == 2:
        # cryptocompare.com       crypto:crypto (backtesting only)
        CANDLE_SOURCE = "CEX"
        CURRENCY = "BTC"
        ASSET = "BTS"

    if SOURCE == 3:
        # alphavantage.com        fiat:fiat (backtesting only)
        CANDLE_SOURCE = "FOX"
        CURRENCY = "USD"
        ASSET = "CNY"

    if SOURCE == 4:
        # alphavantage.com        crypto:fiat (backtesting only)
        CANDLE_SOURCE = "CRY"
        CURRENCY = "USD"
        ASSET = "BTC"

    if SOURCE == 5:
        # alphavantage.com        USstocks:USD (backtesting only)
        CANDLE_SOURCE = "STX"
        CURRENCY = "USD"
        ASSET = "QURE"

    # ==================================================================
    "STATE MACHINE TUNE EXAMPLE"
    # ==================================================================
    # ma1 is the raw signal line
    # ma2 is the long moving average
    # alpha signal of state machine is the moving average crossover
    MA1 = 10  # about 5 to 25 (min 3 for accurate daily backtesting)
    MA2 = 50  # about 30 to 70 (max 75 for accurate live warmup)
    # min and max cross describe ma1 offset and thickness respectively
    # they are coeffs of ma1 (signal line) upon crossing ma2
    # the full thickness of the signal must pass through ma2
    # to switch alpha market state from bull to bear; vise versa
    MIN_CROSS = 1  # about 0.9 to -1.1
    MAX_CROSS = 1.05  # greater than 1, usually no more than 1.2
    # bull and bear stop are offsets of ma2
    # they increase aggressiveness of support/resistance
    # usually only near the moving average crossover
    # support is max(signal, ma2*bullstop)
    # resistance is min(signal, ma2*bearstop)
    BULL_STOP = 1  # about 0.9 to -1.1
    BEAR_STOP = 1  # about 0.9 to -1.1
    # selloff and support are bull market coeffs of ma1
    # resistance and despair are bear market coeffs of ma1
    # these create the outer buy/sell boundaries of active market
    # the bull market is shaded green; the bear market red
    # the inactive "extinct" market is plotted in purple
    SELLOFF = 1.5  # about 1.5 - 2.5
    SUPPORT = 1.1  # about 0.8 - 1.2
    RESISTANCE = 0.9  # about 0.8 - 1.2
    DESPAIR = 0.7  # about 0.6 - 0.8
    # all ten thresholds allow float inputs; ie 1.0254
    # these are the "synapses" of a "neural network"
    # you can make adjustments; tune them by repeatedly backtesting
    # and using gross ROI "gradient ascent" as the "cost function"
    # this process is called "back propagation"
    # you could automate it, I have.  but do not get too lost in that...
    # the algorithm can be profitably tuned for ANY currency pair
    # the ideal values for each are close to defaults
    # a good tune can be manually achieved in about 50 backtests
    # a perfect tune; "the solution" can be found in about 50,000 tests
    # the perfect solution will evolve slowly over time
    # this is to say a tune will become stale after 12-18 months
    # feed forward optimization is periodically retuning to a window
    # eg.: 365 days of the latest data retuned quarterly
    # though a bit tedious, this can certainly be achieved manually

    " ELITIST BRED QUANTUM PARTICLE SWARM OPTIMIZATION "
    " WITH CYCLICAL SIMULATED ANNEALING AND CONTINUAL SUMMIT EROSION "
    # if you like I'll invoke the sorceress for you
    # it takes time, intuitive experience, and burns cpus very hard
    ' 1 pair "perfect" tuned to any 365 day dataset is: '
    # 5000 BTS - dex most pairs
    # 6000 BTS - dex bts:fiat or btc:fiat
    # 7000 BTS - dex bts:btc
    # 8000 BTS - cryptocompare crypto:btc
    # 9000 BTS - cryptocompare crypto:fiat or crypto:crypto
    # 20000 BTS - alphavantage stocks and FX
    # 10% deposit, 24hrs I show results, then u settle, then u get tune
    # telegram @litepresence
    " prices per github extinctionEVENT.py at time of request "




def control_panel():  # Advanced User Controls

    global DAYS, END, START_ASSETS, START_CURRENCY, BULL_MARKET
    global MAX_ASSETS, MAX_CURRENCY, MIN_AMOUNT
    global SCALP, SCALP_PIECES, SCALP_FUND, SCALP_FUND_QTY, SCALP_ZONE
    global MIN_MARGIN, MA3, MA4
    global TICK, TICK_TIMING, TICK_MINIMUM
    global ANIMATE, CURRENCY_STOP, WARMUP
    global LIVE_PLOT_DEPTH, LIVE_PLOT_PROJECTION
    global DEPTH, APY, DPT, ROI, END

    # ==================================================================
    "BACKTEST"
    # ==================================================================
    DAYS = 720  # backtest depth in days
    END = "2100-01-01"  # "YYYY-MM-DD"; set '2100-01-01' for latest
    START_ASSETS = 0  # backtest initial asset holdings
    START_CURRENCY = 1  # backtest initial currency holdings
    BULL_MARKET = True  # initial backtest market state (True is "BULL")
    ANIMATE = False  # resource intensive backtest / better plotting
    CURRENCY_STOP = False  # shift to currency on last tick of backtest
    # ==================================================================
    "LIVE"
    # ==================================================================
    # live tick size in seconds
    TICK = 600
    TICK_TIMING = 51  # number of seconds past the minute to tick
    TICK_MINIMUM = 300  # must be less than tick
    WARMUP = 90  # depth of backtest prior to live session
    # live window #FIXME plot_text() needs to shift with projections
    LIVE_PLOT_DEPTH = 86400  # 86400 = 1 day
    LIVE_PLOT_PROJECTION = 86400
    # max percent may invest in:
    # 100 = "all in" ; 10 = "10 percent in"
    # to let bot do its thing with full bank use 100, 100
    MAX_ASSETS = 100
    MAX_CURRENCY = 100
    # ==================================================================
    "SCALPING"
    # ==================================================================
    SCALP = True  # False to disable scalping
    # scalp thresholds
    SCALP_PIECES = 2  # number of pieces to break up scalp orders
    SCALP_FUND = 0.5  # 0.10 = 10% of holdings reserved for scalping
    SCALP_FUND_QTY = 0.5  # 0.10 = 10% of scalp fund on books per tick
    SCALP_ZONE = 0.8  # 0.80 = scalp middle 80% of market only; max 1
    MIN_MARGIN = 0.007  # about 0.005 - 0.015
    # scalp "center" moving average mesh period in days
    MA3 = 0.200  # about 0.200 to 0.600
    MA4 = 0.066  # about 0.166
    # minimum order size in asset terms
    MIN_AMOUNT = 10
    # ==================================================================
    "CONSTANTS - DO NOT CHANGE"
    # ==================================================================
    # CANDLES of depth prior to info['begin'] to get data
    DEPTH = int(max(MA1, MA2) * (86400 / CANDLE) + 10)
    APY = DPT = ROI = 1.0
    END = int(min(time.time(), from_iso_date(END)))
    if MODE == 3:
        print(("BOT MAY SPEND:     ", MAX_ASSETS, "PERCENT CURRENCY"))
        print(("BOT MAY LIQUIDATE: ", MAX_CURRENCY, "PERCENT ASSETS"))


# CHOOSE TRADING MODE AND ENTER WIF
# ======================================================================
def select_mode():  # Bitshares Keys

    global wif, PAIR
    global MODE, USERNAME
    global LIVE, CANDLE, PAPER, DEPTH, BACKTEST, SALES, OPTIMIZE
    global DAYS, BLIP, END, OPTIMIZATIONS, DPT, ROI, APY, ORDER_TEST

    if CANDLE_SOURCE == "DEX":
        PAIR = ASSET + ":" + CURRENCY
    if CANDLE_SOURCE in ["CEX", "STX", "FOX", "CRY"]:
        PAIR = "%s_%s" % (CURRENCY, ASSET)

    MODE = 999
    print("0:OPTIMIZE 1:BACKTEST 2:PAPER 3:LIVE 4:SALES 6:ORDER_TEST")
    while MODE not in [0, 1, 2, 3, 4, 6]:
        MODE = int(input("TRADING MODE: "))
    print("")
    if MODE == 6:
        print("WARNING TESTING LIVE WITH FUNDS:")
        print("This mode will repeatedly buy/sell/cancel")
        print("0.1 assets on 20% spread.")
        print("Monitor with microDEX.py")
        print("")
        time.sleep(10)

    if MODE not in [0, 1, 4]:
        metaNODE = Bitshares_Trustless_Client()
        asset = metaNODE["asset"]
        currency = metaNODE["currency"]
        USERNAME = metaNODE["account_name"]
        del metaNODE
        pair = asset + ":" + currency
        if pair != PAIR:
            raise ValueError("metaNODE PAIR != tune_install() PAIR")

    BLIP = 0.0005  # a small amount of time
    CANDLE = 86400
    # 0        1          2       3      4       6
    OPTIMIZE = BACKTEST = PAPER = LIVE = SALES = ORDER_TEST = False
    if MODE == 0:
        OPTIMIZE = True
    if MODE == 1:
        BACKTEST = True
        OPTIMIZATIONS = 0
    if MODE == 2:
        PAPER = True
        MAX_ASSETS = 0
        MAX_CURRENCY = 0
    if MODE == 6:
        ORDER_TEST = True
        MAX_ASSETS = 0
        MAX_CURRENCY = 0
    if MODE in [2, 3, 6]:
        LIVE = True
        CANDLE = 14400
        OPTIMIZATIONS = 0
    if MODE == 4:
        BACKTEST = True
        SALES = True
        OPTIMIZATIONS = 0
    wif = ""
    if MODE in [3, 6]:
        log_in()


def log_in():

    global wif

    print("DO NOT ENTER PASSWORD WITHOUT READING, UNDERSTANDING,")
    print("AND TAKING PERSONAL RESPONSIBILITY FOR THE CODE")
    print("")
    print("welcome back %s" % USERNAME)
    print("")
    authenticated = False
    while not authenticated:
        try:
            wif = getpass(prompt="               wif: ")
            print(
                "\033[F              wif: "
                + "********************************"
            )
            print("")
            print("AUTHENTICATING to DEX wallet...")
            try:
                authenticated = authenticate()
            except Exception as e:
                print(trace(e))
            if authenticated:
                print("")
                print(("*****************"))
                print(
                    ("**AUTHENTICATED**") + (" YOUR WALLET IS UNLOCKED")
                )
                print(("*****************"))
            else:
                wif = ""
                print(("wif DOES NOT MATCH USERNAME"))
        except Exception as e:
            print(e.args)
            pass


# BITSHARES DEX TRADING API
# ======================================================================


def authenticate():

    global edicts
    edicts = [{"op": "login"}]
    order = json_loads(prototype_order())
    order["header"]["wif"] = wif
    order["edicts"] = edicts
    if not PAPER:
        authenticated = broker(order)
    else:
        print("PAPER - skipping auth")
        authenticated = True
    edicts = []
    return authenticated


def cancel_all():

    global edicts
    edicts = [{"op": "cancel", "ids": ["1.7.X"]}]
    order = json_loads(prototype_order())
    order["header"]["wif"] = wif
    order["edicts"] = edicts
    if not PAPER:
        broker(order)
    else:
        print(order)
    edicts = []


def place_order():

    global edicts
    order = json_loads(prototype_order())
    order["header"]["wif"] = wif
    order["edicts"] = edicts
    if not PAPER:
        broker(order)
    else:
        print(order)
    edicts = []


def fee_maintainer():

    # if holding less than 0.5 BTS, then buy 1.5 BTS
    metaNODE = Bitshares_Trustless_Client()
    nodes = metaNODE["whitelist"]
    precision = metaNODE["currency_precision"]
    account_name = metaNODE["account_name"]
    account_id = metaNODE["account_id"]
    bts = metaNODE["bts_balance"]
    # pay with market currency, unless bts then pay with assets
    cid = metaNODE["currency_id"]
    if metaNODE["currency"] == "BTS":
        cid = metaNODE["asset_id"]
        precision = metaNODE["asset_precision"]
    # if low on fee funds create custom order to buy some BTS
    del metaNODE
    print("fee_maintainer() BTS: %.2f" % bts)
    if bts < 0.5:
        order = {
            "edicts": [
                {
                    "op": "buy",
                    "amount": 1.5,
                    "price": 99999,
                    "expiration": 0,
                }
            ],
            "header": {
                "asset_id": "1.3.0",
                "currency_id": cid,
                "asset_precision": 5,
                "currency_precision": precision,
                "account_id": account_id,
                "account_name": account_name,
                "wif": wif,
            },
            "nodes": nodes,
        }
        if not PAPER:
            broker(order)
        else:
            print(order)


# TEXT PIPE
# ======================================================================


def race_read(doc=""):  # Concurrent Read from File Operation

    i = 0
    while True:
        try:
            time.sleep(0.05 * i ** 2)
            i += 1
            with open(doc, "r") as f:
                ret = f.read()
                f.close()
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
        except Exception as e:
            msg = str(type(e).__name__) + str(e.args)
            msg += " race_read()"
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
    return ret


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


def race_append(doc="", text=""):  # Concurrent Append to File Operation

    text = "\n" + str(time.ctime()) + " " + str(text) + "\n"
    i = 0
    while True:
        time.sleep(0.05 * i ** 2)
        i += 1
        if i > 10:
            break
        try:
            with open(doc, "a+") as f:
                f.write(text)
                f.close()
                break
        except Exception as e:
            msg = str(type(e).__name__) + str(e.args)
            msg += " race_append()"
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


def watchdog():

    identity = 0  # metaNODE:1, botscript:0
    max_latency = 60
    warn = " !!!!! WARNING: the other app is not responding !!!!!"

    while True:
        try:
            try:
                with open("watchdog.txt", "r") as f:
                    ret = f.read()
                    f.close()

                ret = literal(ret)
                response = int(ret[identity])
                now = int(time.time())
                latency = now - response

                if identity == 0:
                    msg = str([response, now])
                if identity == 1:
                    msg = str([now, response])

                with open("watchdog.txt", "w+") as f:
                    f.write(msg)
                    f.close()

                msg = str(latency)
                if latency > max_latency:
                    msg += warn
                return msg

            except Exception as e:
                msg = str(type(e).__name__) + str(e.args)
                print(msg)
                now = int(time.time())
                with open("watchdog.txt", "w+") as f:
                    f.write(str([now, now]))
                    f.close()
                    break  # exit while loop
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


# CANDLE DATA
# ======================================================================


def backtest_candles(start, stop, candle):  # HLOCV arrays

    if candle == 86400:
        items = len(max_data["unix"])
        stop = items - int(max(max_data["unix"] - END) / 86400.0)
        start = max(0, (stop - DAYS - int(max(MA1, MA2)) - 1))

        data = {k: v[start:stop] for k, v in max_data.items()}
        print(max(max_data["unix"]), time.time(), END)
        print("items", items)
        print("start", start, "stop", stop)
        # print('max', max_data)
        print("data", data)
    else:
        data = proxyDEX(ASSET, CURRENCY, start, stop, candle)

    return data


def slice_candles(now, data):  # Window backtest arrays

    # window backtest_candles() data to test each candle
    d = {}
    for i in range(len(data["unix"])):
        if now <= data["unix"][i] < (now + CANDLE):
            h = []
            l = []
            o = []
            c = []
            for j in range(DEPTH):
                try:
                    h.append(data["high"][i - j])
                    l.append(data["low"][i - j])
                    o.append(data["open"][i - j])
                    c.append(data["close"][i - j])
                except:
                    print("append failed")
                    pass
            d["high"] = np.array(h[::-1])
            d["low"] = np.array(l[::-1])
            d["open"] = np.array(o[::-1])
            d["close"] = np.array(c[::-1])
    return d


def live_candles(candle, depth):  # Current HLOCV arrays

    # gather latest from Bitshares RPC to a given depth
    now = int(time.time())
    data = proxyDEX(
        ASSET, CURRENCY, (now - (depth + 10) * candle), now, candle
    )
    data["unix"] = data["unix"][-depth:]
    data["high"] = data["high"][-depth:]
    data["low"] = data["low"][-depth:]
    data["open"] = data["open"][-depth:]
    data["close"] = data["close"][-depth:]
    data["volume"] = data["volume"][-depth:]

    return data


# LIVE
# ======================================================================


def live_initialize():  # Begin live session

    global storage, portfolio, info, data, edicts
    logo()
    print(VERSION)
    print("~====== BEGIN LIVE SESSION =====================~")
    # clear global dictionaries except for "storage"
    info = {}
    data = {}
    portfolio = {}
    edicts = []
    # initialize storage
    storage["trades"] = 0
    storage["previous_v"] = SATOSHI
    storage["holding_ticks"] = 0
    info["live"] = True
    info["tick"] = 0
    info["hour"] = 0
    info["day"] = 0
    info["end"] = None
    info["current_time"] = info["begin"] = int(time.time())
    # set initial timing offset
    if MODE == 3:
        seconds_past = time.time() % 60
        offset = TICK_TIMING - seconds_past
        if offset < 0:
            offset += 60
        print("")
        print(
            time.ctime(),
            "setting tick offset to",
            TICK_TIMING,
            "sleeping for",
            ("%.1f" % offset),
            "seconds",
        )
        time.sleep(offset)


def live():  # Primary live event loop

    global storage
    global info

    live_initialize()

    previous_order_value = 0
    attempt = 0
    msg = ""
    while True:
        plt.pause(1)  # prevent inadvertent attack on API's
        if info["tick"] > 0:
            set_timing(TICK)
        info["current_time"] = now = int(time.time())
        print("")
        print(
            (
                "______________________________ %s %s"
                % (PAIR, time.ctime())
            )
        )
        print("")

        # DEBUG LIVE SESSION
        debug = 0
        if debug:
            print("$$$$$$$$$$$$$$$$$$")
            print(
                "WARN: DEBUG - RUNTIME: %s"
                % (info["current_time"] - info["begin"])
            )
            print("$$$$$$$$$$$$$$$$$$")
            print("")
            print("WATCHDOG LATENCY:", watchdog())
            live_data()
            indicators()
            polynomial_regression()
            state_machine()
            hourly()
            daily()
            cancel_all()
            scalp()
            trade()
            place_order()
            live_chart()
            plot_format()
            live_plot()
            plt.pause(10)
            info["tick"] += 1

        else:
            try:
                plt.pause(0.05)
                print("")
                print(
                    "RUNTIME: %s"
                    % (info["current_time"] - info["begin"])
                )
                print("")
                print("WATCHDOG LATENCY:", watchdog())
                print("")
                # RAISE ALARM
                if attempt > 2:
                    time_msg = datetime.fromtimestamp(now).strftime(
                        "%H:%M"
                    )
                    print(
                        (
                            "%s FAIL @@@@@@@ ATTEMPT: %s %s"
                            % (msg, attempt, time_msg)
                        )
                    )
                # GATHER AND POST PROCESS DATA
                start = time.time()
                print("elapsed: %.3f" % (time.time() - start))
                start = time.time()
                try:
                    plt.pause(0.05)
                    live_data()
                except Exception as e:
                    msg += trace(e) + "live_data() "
                    attempt += 1
                    continue
                print("elapsed: %.3f" % (time.time() - start))
                start = time.time()
                try:
                    plt.pause(0.05)
                    indicators()
                except Exception as e:
                    msg += trace(e) + "indicators() "
                    attempt += 1
                    continue
                print("elapsed: %.3f" % (time.time() - start))
                start = time.time()
                try:
                    plt.pause(0.05)
                    polynomial_regression()
                except Exception as e:
                    msg += trace(e) + "polynomial_regression() "
                    attempt += 1
                    continue
                print("elapsed: %.3f" % (time.time() - start))
                start = time.time()
                try:
                    plt.pause(0.05)
                    state_machine()
                except Exception as e:
                    msg += trace(e) + "state_machine() "
                    attempt += 1
                    continue
                print("elapsed: %.3f" % (time.time() - start))
                start = time.time()
                # LOWER FREQENCY EVENTS
                plt.pause(0.05)
                runtime = info["current_time"] - info["begin"]
                check_hour = runtime / 3600.0
                if check_hour > info["hour"]:

                    try:
                        hourly()
                        info["hour"] += 1
                    except Exception as e:
                        msg += trace(e) + "hourly() "
                        attempt += 1
                        continue
                print("elapsed: %.3f" % (time.time() - start))
                start = time.time()
                check_day = runtime / 86400.0
                if check_day > info["day"]:
                    try:
                        daily()
                        info["day"] += 1
                    except Exception as e:
                        msg += trace(e) + "daily() "
                        attempt += 1
                        continue
                print("elapsed: %.3f" % (time.time() - start))
                start = time.time()

                metaNODE = Bitshares_Trustless_Client()
                order_value = (
                    metaNODE["sell_orders"] + metaNODE["buy_orders"]
                )
                for order in metaNODE["orders"]:
                    print(order)
                del metaNODE

                # if no orders are on books
                # or any orders have been touched since last tick
                # or every 10 ticks at least
                if (
                    (order_value < previous_order_value)
                    or (order_value == 0)
                    or (info["tick"] % 10 == 0)
                ):

                    # CANCEL ALL OUTSTANDING ORDERS IN THIS MARKET
                    if order_value > 0:
                        cancel_all()
                        plt.pause(3)  # allow acct balance to update

                    print("elapsed: %.3f" % (time.time() - start))
                    start = time.time()

                    # MAINTAIN 1 BITSHARE FOR FEES
                    plt.pause(0.05)
                    try:
                        fee_maintainer()
                    except Exception as e:
                        msg += trace(e) + "fee_maintainer() "
                        attempt += 1
                        continue
                    print("elapsed: %.3f" % (time.time() - start))
                    start = time.time()

                # SCALP OPS
                plt.pause(0.01)
                try:
                    scalp()
                except Exception as e:
                    msg += trace(e) + "scalp() "
                    attempt += 1
                    continue
                print("elapsed: %.3f" % (time.time() - start))
                start = time.time()

                # TRADE OPS
                plt.pause(0.01)
                try:
                    trade()
                except Exception as e:
                    msg += trace(e) + "trade() "
                    attempt += 1
                    continue
                print("elapsed: %.3f" % (time.time() - start))
                start = time.time()

                # EXECUTE
                if (
                    (order_value < previous_order_value)
                    or (order_value == 0)
                    or (info["tick"] % 10 == 0)
                ):
                    order = json_loads(prototype_order())
                    order["header"]["wif"] = wif
                    order["edicts"] = edicts
                    if not PAPER:
                        broker(order)
                    else:
                        print(order)
                    print("elapsed: %.3f" % (time.time() - start))
                    start = time.time()

                plt.pause(5)
                metaNODE = Bitshares_Trustless_Client()
                previous_order_value = (
                    metaNODE["sell_orders"] + metaNODE["buy_orders"]
                )
                del metaNODE

                # PLOT
                try:
                    live_chart()
                except Exception as e:
                    msg += trace(e) + "live_chart() "
                    attempt += 1
                    continue
                print("elapsed: %.3f" % (time.time() - start))
                start = time.time()
                try:
                    plot_format()
                except Exception as e:
                    msg += trace(e) + "plot_format() "
                    attempt += 1
                    continue
                print("elapsed: %.3f" % (time.time() - start))
                start = time.time()
                try:
                    live_plot()
                except Exception as e:
                    msg += trace(e) + "live_plot() "
                    attempt += 1
                    continue
                print("elapsed: %.3f" % (time.time() - start))
                start = time.time()

                # END PRIMARY TICK
                plt.pause(0.05)
                msg = ""
                print("tick", info["tick"])
                info["tick"] += 1
                attempt = 0
            except Exception as e:
                trace(e)
                continue


def set_timing(tick_size):  # Limits live tick interval (seconds)

    plt.pause(0.01)
    print("set_timing()")
    now = time.time()
    # time elapsed since live_initialize()
    elapsed = now - info["begin"]
    # ticks that should have occurred
    ticks = int(elapsed / tick_size) + 1
    # ticks that should have, less ticks that actually did occur
    tick_drift = ticks - info["tick"]
    # duration of the latest tick
    drift = info["tick"] * tick_size - elapsed
    wait = min(drift, tick_size)
    print(
        (
            "wait: %.2f, drift: %.2f, tick: %s, tick drift %s"
            % (wait, drift, info["tick"], tick_drift)
        )
    )
    wait -= 10
    if wait > 0:
        plt.pause(wait)
    seconds_past = time.time() % 60
    offset = TICK_TIMING - seconds_past
    if offset < 0:
        offset += 60
    plt.pause(offset)


def live_data():  # Gather live data from metaNODE and proxyDEX

    global portfolio
    global data
    global storage

    plt.pause(0.01)
    print("live_data()")
    "*************************************"
    metaNODE = Bitshares_Trustless_Client()
    "*************************************"
    print("metaNODE()")
    orders = metaNODE["orders"]
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
    # MA1, MA2, MA3, MA4 are daily moving average periods
    depth_4h = int(max(MA1, MA2) * 1.05 * 6)  # 6*4h = 24 hours
    depth_5m = int(max(MA3, MA4) * 1.05 * 288)  # 288*5m = 24 hours
    data["14400"] = live_candles(candle=14400, depth=depth_4h)
    data["300"] = live_candles(candle=300, depth=depth_5m)
    # print top of book
    print(
        it("green", sbids),
        "< BIDS <",
        it("yellow", last),
        "> ASKS >",
        it("red", sasks),
    )


def scalp():  # Initiate secondary order placement

    global storage, edicts

    # localize data
    now = int(time.time())
    # from metaNODE
    "*************************************"
    metaNODE = Bitshares_Trustless_Client()
    "*************************************"
    currency = portfolio["currency"] = metaNODE["currency_balance"]
    assets = portfolio["assets"] = metaNODE["asset_balance"]
    last = storage["last"] = metaNODE["last"]
    invested = metaNODE["invested"]
    divested = metaNODE["divested"]
    max_assets = metaNODE["asset_max"]
    max_currency = metaNODE["currency_max"]
    book = metaNODE["book"]
    nodes = metaNODE["whitelist"]
    del metaNODE

    ask_p = book["askp"][0]
    ask_v = book["askv"][0]
    bid_p = book["bidp"][0]
    bid_v = book["bidv"][0]
    ask_p2 = book["askp"][1]
    bid_p2 = book["bidp"][1]

    # from indicators()
    mid_market = storage["mid_market"]
    buying = storage["buying"]
    selling = storage["selling"]
    high = storage["high"]
    low = storage["low"]
    ma3 = storage["ma3"][-1]
    ma4 = storage["ma4"][-1]

    # plot zoom in
    now = time.time()
    past = now - LIVE_PLOT_DEPTH
    ax = plt.gca()
    ax.set_ylim([0.90 * last, 1.1 * last])
    ax.set_xlim([past, now])
    plot_text()
    plt.pause(0.01)

    # from state_machine()
    bull_market = storage["bull_market"]

    # means to buy and percent invested
    means = storage["means"] = currency / last  # assets can afford
    storage["max_assets"] = max_assets
    storage["asset_ratio"] = invested
    storage["max_currency"] = max_currency
    # define scalp support and resistance
    scalp_resistance = max(high, ma3, ma4)
    scalp_support = min(low, ma3, ma4)
    # expand scalp ops to dex just inside market bid/ask
    scalp_resistance = max(scalp_resistance, 0.999999999 * ask_p)
    scalp_support = min(scalp_support, 1.000000001 * bid_p)
    # adjust scalp margins if too thin
    scalp_margin = (scalp_resistance - scalp_support) / scalp_support
    if scalp_margin < MIN_MARGIN:
        midscalp = (scalp_resistance + scalp_support) / 2
        scalp_resistance = (1 + MIN_MARGIN / 2) * midscalp
        scalp_support = (1 - MIN_MARGIN / 2) * midscalp
    # limit scalp ops to a middle subset of the alpha channel
    market_spread = selling - buying
    no_scalping_zone = market_spread * ((1 - SCALP_ZONE) / 2)
    max_scalp_buy = selling - no_scalping_zone
    min_scalp_sell = buying + no_scalping_zone
    # go all in / all out if outside of the alpha channel
    if scalp_support < buying:
        scalp_support = buying
    if scalp_resistance > selling:
        scalp_resistance = selling
    # rattle the volatility on top and bottom of the alpha channel
    if scalp_support > max_scalp_buy:
        scalp_support = max_scalp_buy
        scalp_resistance = selling
    if scalp_resistance < min_scalp_sell:
        scalp_resistance = min_scalp_sell
        scalp_support = buying
    # assure support under resistance
    if scalp_support > scalp_resistance:
        print("skip scalp, calculation error")
        raise
    # store scalp thresholds globally
    storage["scalp_resistance"] = scalp_resistance
    storage["scalp_support"] = scalp_support
    # scale scalp orders to alpha market state and SCALP FUND
    holding = storage["holding"]
    if holding:  # from primary trade() function
        max_holding = 1
        min_holding = 1 - SCALP_FUND
    else:
        max_holding = SCALP_FUND
        min_holding = 0

    buy_qty = max(0, max_assets * (max_holding - invested / 100))
    sell_qty = max(0, max_assets * (invested / 100 - min_holding))

    # print('b s qty', buy_qty, sell_qty)

    buy_qty = min(buy_qty, max_assets * SCALP_FUND)
    sell_qty = min(sell_qty, max_assets * SCALP_FUND)

    # print('b s qty', buy_qty, sell_qty)

    buy_qty *= SCALP_FUND_QTY
    sell_qty *= SCALP_FUND_QTY

    # print('b s qty', buy_qty, sell_qty)

    # break up scalp orders into smaller pieces
    pieces = SCALP_PIECES
    pie = []
    for i in range(pieces):
        pie.append(random())
    total = sum(pie)
    for i in range(pieces):
        pie[i] = pie[i] / total
    # initialize starting max holdings and start price
    if info["tick"] == 0:
        storage["begin_max_assets"] = max_assets
        storage["begin_max_currency"] = max_currency
        storage["start_price"] = last

    # return on investment vs buy/hold vs sell/wait
    roi_assets = max_assets / storage["begin_max_assets"]
    roi_currency = max_currency / storage["begin_max_currency"]
    roi_gross = roi_assets * roi_currency
    buy_hold = last / storage["start_price"]
    sell_wait = 1 / buy_hold

    if SCALP:
        print("")
        print("begin scalp() ops")
        print("")
        print("assets        ", satoshi_str(assets))
        print("currency      ", satoshi_str(currency))
        print("invested      ", ("%.3f" % invested))
        print("means         ", satoshi_str(means))
        print("max assets    ", satoshi_str(max_assets))
        print("max currency  ", satoshi_str(max_currency))
        print(
            "start assets  ", satoshi_str(storage["begin_max_assets"])
        )
        print(
            "start currency", satoshi_str(storage["begin_max_currency"])
        )
        print("start price   ", satoshi_str(storage["start_price"]))
        print("roi gross     ", ("%.4f" % roi_gross))
        print("roi assets    ", ("%.4f" % roi_assets))
        print("roi currency  ", ("%.4f" % roi_currency))
        print("buy_hold      ", ("%.4f" % buy_hold))
        print("sell_wait     ", ("%.4f" % sell_wait))
        print("holding       ", holding)
        print("max_holding   ", max_holding)
        print("min holding   ", min_holding)
        print("buy qty       ", buy_qty)
        print("sell_qty      ", sell_qty)
        print("scalp s       ", satoshi_str(scalp_support))
        print("scalp r       ", satoshi_str(scalp_resistance))
        print("pieces        ", pieces, pie)
        print("")

        # SCALP BUY
        for i in range(pieces):
            qty = buy_qty * pie[i]
            print("bqty", qty)
            scalp = scalp_support - i * 2 * random() * SATOSHI
            try:
                if qty > MIN_AMOUNT:
                    print(
                        "scalp buy",
                        satoshi_str(qty),
                        "at",
                        satoshi_str(scalp),
                    )

                    edicts.append(
                        {
                            "op": "buy",
                            "price": scalp,
                            "amount": qty,
                            "expiration": 0,
                        }
                    )
            except:
                pass

        # SCALP SELL
        for i in range(pieces):
            qty = sell_qty * pie[i]
            print("sqty", qty)
            scalp = scalp_resistance + i * 2 * random() * SATOSHI
            try:

                if qty > MIN_AMOUNT:
                    print(
                        "scalp sell",
                        satoshi_str(qty),
                        "at",
                        satoshi_str(scalp),
                    )
                    edicts.append(
                        {
                            "op": "sell",
                            "price": scalp,
                            "amount": qty,
                            "expiration": 0,
                        }
                    )
            except:
                pass

    ymax, ymin, xmax, xmin = zoom_out_live()
    # Print trade pair and time
    time_LOCAL = datetime.fromtimestamp(int(time.time())).strftime(
        "%H:%M:%S"
    )
    time_UTC = datetime.fromtimestamp(
        int(time.time()) + 18000
    ).strftime("%H:%M:%S")
    print(("%.2f %s %.2f %s" % (currency, CURRENCY, assets, ASSET)))
    print(
        (
            "%s UTC                                             %s"
            % (time_UTC, time_LOCAL)
        )
    )
    print(
        ("(buying: %.8f selling %.8f)" % (buying, selling))
        + (
            "(scalp buy %.8f, scalp sell %.8f)"
            % (scalp_support, scalp_resistance)
        )
    )


def trade():  # Initiate primary order placement

    global storage, edicts

    # localize storage data
    buying = storage["buying"]
    selling = storage["selling"]
    mid_market = storage["mid_market"]
    bull_market = storage["bull_market"]

    if info["live"]:  # localize additional data for live session

        # load metaNODE data
        "*************************************"
        metaNODE = Bitshares_Trustless_Client()
        "*************************************"
        currency = metaNODE["currency_balance"]
        assets = metaNODE["asset_balance"]
        last = metaNODE["last"]
        book = metaNODE["book"]
        ask_p = book["askp"][0]
        bid_p = book["bidp"][0]
        invested = metaNODE["invested"]
        divested = metaNODE["divested"]
        max_assets = metaNODE["asset_max"]
        max_currency = metaNODE["currency_max"]
        nodes = metaNODE["whitelist"]
        del metaNODE

        high = storage["high"]
        low = storage["low"]

        # plot zoom in to trade decision
        mesh_max = max(storage["long_average"], storage["signal_line"])
        mesh_min = min(storage["long_average"], storage["signal_line"])
        now = time.time()
        past = now - LIVE_PLOT_DEPTH
        future = now + LIVE_PLOT_PROJECTION
        ax = plt.gca()
        ax.set_ylim([0.93 * mesh_min, 1.07 * mesh_max])
        ax.set_xlim([past, future])
        plot_text()
        plt.pause(0.01)

        print(("assets %.1f, max assets %.1f" % (assets, max_assets)))
        pieces = 10.0  # order size

        if ORDER_TEST:
            edicts.append({"op": "cancel", "ids": ["1.7.X"]})

            edicts.append(
                {
                    "op": "buy",
                    "price": 0.8 * last,
                    "amount": 0.0001 / last,
                    "expiration": 0,
                }
            )

            edicts.append(
                {
                    "op": "sell",
                    "price": 1.2 * last,
                    "amount": 0.0001 / last,
                    "expiration": 0,
                }
            )

        if high > selling:
            storage["holding"] = False
        if low < buying:
            storage["holding"] = True

        qty = max_assets / pieces
        if (last > 0.90 * selling) and not ORDER_TEST:
            print("")
            print("APPROACHING SELL POINT")
            if assets > 0.1:
                if divested < MAX_CURRENCY:
                    selling_r = max(selling, (last + ask_p) / 2)
                    try:
                        if qty > MIN_AMOUNT:
                            # iceberg
                            print(
                                (
                                    "SELLING",
                                    PAIR,
                                    "RATE",
                                    ("%.8f" % selling_r),
                                    "AMOUNT",
                                    ("%.1f" % qty),
                                )
                            )

                            edicts.append(
                                {
                                    "op": "sell",
                                    "price": selling_r,
                                    "amount": qty,
                                    "expiration": 0,
                                }
                            )

                        # iceberg front limit
                        selling_r *= 1.0 - 0.015 * random()
                        qty /= randint(69, 99)
                        if (qty > MIN_AMOUNT) and (random() > 0.5):
                            print(
                                (
                                    "SELLING MINI",
                                    PAIR,
                                    "RATE",
                                    ("%.8f" % selling_r),
                                    "AMOUNT",
                                    ("%.1f" % qty),
                                )
                            )

                            edicts.append(
                                {
                                    "op": "sell",
                                    "price": selling_r,
                                    "amount": qty,
                                    "expiration": 0,
                                }
                            )
                    except:
                        print("SELL FAILED")
                        pass
                else:
                    print("MAX DIVESTED")
            else:
                print("NO ASSETS")

        qty = max_assets / pieces
        if (last < 1.20 * buying) and not ORDER_TEST:
            print("")
            print("APPROACHING BUY POINT")
            if currency > 0.1:
                if invested < MAX_ASSETS:
                    buying_r = min(buying, (last + bid_p) / 2)
                    try:
                        if qty > MIN_AMOUNT:
                            print(
                                (
                                    "BUYING",
                                    PAIR,
                                    "RATE",
                                    ("%.8f" % buying_r),
                                    "AMOUNT",
                                    ("%.1f" % qty),
                                )
                            )

                            edicts.append(
                                {
                                    "op": "buy",
                                    "price": buying_r,
                                    "amount": qty,
                                    "expiration": 0,
                                }
                            )

                        buying_r *= 1.0 + 0.015 * random()
                        qty /= randint(69, 99)
                        if (qty > MIN_AMOUNT) and (random() > 0.5):
                            print(
                                (
                                    "BUYING MINI",
                                    PAIR,
                                    "RATE",
                                    ("%.8f" % buying_r),
                                    "AMOUNT",
                                    ("%.1f" % qty),
                                )
                            )

                            edicts.append(
                                {
                                    "op": "buy",
                                    "price": buying_r,
                                    "amount": qty,
                                    "expiration": 0,
                                }
                            )
                    except:
                        print("buy FAIL")
                        pass
                else:
                    print("MAX INVESTED")
            else:
                print("NO CURRENCY")

        ymax, ymin, xmax, xmin = zoom_out_live()

    else:
        # test trade
        if portfolio["currency"] > 0:
            if storage["low"][-1] < buying:
                buying_r = min(storage["high"][-1], buying)
                test_buy(buying_r)

        elif portfolio["assets"] > 0:
            if storage["high"][-1] > selling:
                selling_r = max(storage["low"][-1], selling)
                test_sell(selling_r)

    if storage["holding"]:
        storage["holding_ticks"] += 1


def hourly():  # Do this every hour
    print(("hour: %s" % info["hour"]))


def daily():  # Do this every day

    if info["tick"] > 0:
        logo()  # clear terminal to prevent overflow
    now = int(time.time())
    ma2 = storage["ma2poly"][-1]
    print(("day: %s" % info["day"]))
    plt.plot(
        now,
        ma2,
        markersize=20,
        marker=".",
        color="white",
        label="daily",
    )


# BACKTEST
# ======================================================================


def initialize():  # Open plot, set backtest days

    global DAYS, edicts, max_data

    if LIVE:
        cancel_all()
        print("checking with metaNODE watchdog before live session...")
        watchdog()
    if MODE == 0:
        print("~=== OPTIMIZING 1D CANDLES =================~")
    if MODE == 1:
        print("~=== BEGIN BACKTEST 1D CANDLES =============~")
    if MODE == 2:
        print("~=== WARMING UP PAPER SESSION 4H CANDLES ===~")
    if MODE == 3:
        print("")
        print("")
        print("NOTE: ALPHA RELEASE TO PUBLIC DOMAIN WITH NO WARRANTY")
        print("")
        print("")
        print("~=== WARMING UP LIVE MACHINE 4H CANDLES ====~")
    if MODE == 4:
        print("~=== BEGIN SALES BACKTEST 1D CANDLES =======~")
    if MODE in [2, 3]:
        print("This will take a few minutes...")
    if MODE == 6:
        print("~=== BEGIN LIVE BUY/SELL/CANCEL TEST =======~")

    now = int(time.time())
    days = 100000
    if LIVE or PAPER or ORDER_TEST:
        days = WARMUP
    else:
        if CANDLE_SOURCE == "DEX":
            days = 1000
            max_data = proxyDEX(
                ASSET, CURRENCY, (now - 86400 * 1000), now, 86400
            )
        if CANDLE_SOURCE == "CEX":
            max_data = proxyCEX(ASSET, CURRENCY, 1390000000, now, 86400)
            days = len(max_data["unix"])
            # filter glitches in early datasets
            if ASSET == "BTS":
                days -= 250
                if CURRENCY == "BITCNY":
                    days -= 200
            elif ASSET == "DASH":
                days -= 360
            elif ASSET == "NXT":
                days -= 300
            else:
                days -= 100
        if CANDLE_SOURCE == "STX":
            max_data = proxySTX(ASSET, CURRENCY, 0, now, 86400)
        if CANDLE_SOURCE == "FOX":
            max_data = proxyFOX(ASSET, CURRENCY, 0, now, 86400)
        if CANDLE_SOURCE == "CRY":
            max_data = proxyCRY(ASSET, CURRENCY, 0, now, 86400)
    days = days - DEPTH * (86400 / CANDLE)
    DAYS = int(min(days, DAYS))

    if LIVE or BACKTEST:
        plt.ion()
        fig = plt.figure()
        fig.patch.set_facecolor("0.15")
        fig.canvas.set_window_title(VERSION)


def holdings():  # Calculate starting portfolio

    info["holdings"] = info.get("holdings", False)
    if not info["holdings"]:
        close = data["close"][-DAYS]
    else:
        close = storage["close"][-1]
    storage["max_assets"] = portfolio["assets"] + (
        portfolio["currency"] / close
    )
    storage["max_currency"] = portfolio["currency"] + (
        portfolio["assets"] * close
    )
    if not info["holdings"]:
        storage["begin_max_assets"] = storage["max_assets"]
        storage["begin_max_currency"] = storage["max_currency"]
        storage["start_price"] = close
    info["holdings"] = True


def test_initialize():  # Begin backtest session

    now = int(time.time())

    global storage
    global portfolio
    global info
    global data
    # initialize storage
    storage["trades"] = 0
    storage["buys"] = [[], []]
    storage["sells"] = [[], []]
    storage["holding"] = True
    storage["holding_ticks"] = 0
    storage["bull_market"] = BULL_MARKET
    # initialize portfolio balances
    portfolio["assets"] = float(START_ASSETS)
    portfolio["currency"] = float(START_CURRENCY)
    # initialize info dictionary objects
    info["end"] = int(min(now, END))
    info["begin"] = info["end"] - DAYS * 86400
    if LIVE or PAPER or ORDER_TEST:
        info["end"] = now
        info["begin"] = int(info["end"] - 86400 * WARMUP)
    info["origin"] = int(
        info["begin"] - max(MA1, MA2) * 86400 - 2 * CANDLE
    )
    info["current_time"] = info["begin"]
    info["live"] = False
    info["tick"] = 0

    print(info["origin"], time.ctime(info["origin"]), "origin")
    print(info["begin"], time.ctime(info["begin"]), "begin")
    print(info["end"], time.ctime(info["end"]), "end")

    print(
        (
            "Dataset.....: %s DAYS"
            % int((now - info["origin"]) / 86400.0)
        )
    )
    print(
        ("Backtesting.: %s DAYS" % int((now - info["begin"]) / 86400.0))
    )

    # check for compatible interval
    if CANDLE not in [14400, 86400]:
        print(("Tick Interval must be in [14400, 86400]"))
        raise stop()

    # gather complete data set for backtest
    if LIVE or BACKTEST:
        data = backtest_candles(info["origin"], now, CANDLE)
        # print PAIR CANDLE ORIGIN and BEGIN
        print("")
        print(("PAIR......: %s" % PAIR))
        print("")
        print(("CANDLE....: %s" % CANDLE))
        print(
            (
                "ORIGIN....: %s %s"
                % (info["origin"], time.ctime(info["origin"]))
            )
        )
        print(
            (
                "BEGIN.....: %s %s"
                % (info["begin"], time.ctime(info["begin"]))
            )
        )
        plot_format()


def backtest():  # Primary backtest event loop; the cost function

    global DAYS
    global storage

    DAYS = int(
        len(data["unix"]) / float(86400 / CANDLE) - max(MA1, MA2) - 1
    )
    info["current_time"] = info["begin"]
    info["end"] = max(data["unix"])
    while True:
        if info["current_time"] < info["end"]:

            try:
                data_slice = slice_candles(info["current_time"], data)
                storage["high"] = data_slice["high"]
                storage["low"] = data_slice["low"]
                storage["open"] = data_slice["open"]
                storage["close"] = data_slice["close"]
                holdings()
                indicators()
                state_machine()
                trade()
                if LIVE or BACKTEST:
                    test_chart()
                    if info["tick"] % 100 == 0:
                        if not OPTIMIZE:
                            plt.pause(0.0001)
            except:
                print(
                    "WARN: backtest data unavailable",
                    time.ctime(info["current_time"]),
                )

            info["current_time"] += CANDLE
            info["tick"] += 1
            if LIVE and (info["tick"] % 50 == 0):
                plot_text()
                plt.pause(0.0001)

        else:
            test_stop()
            if LIVE or BACKTEST:
                test_plot()
                plt.pause(0.0001)
                if BACKTEST:
                    plt.ioff()
                try:
                    plot_format()
                except:
                    pass
                plt.pause(0.0001)
            break


def test_buy(price):  # Execute a backtest buy

    storage["trades"] += 1
    now = time.ctime(info["current_time"])
    storage["buys"][0].append(info["current_time"])
    storage["buys"][1].append(price)
    portfolio["assets"] = portfolio["currency"] / price
    storage["holding"] = True
    if LIVE or BACKTEST:
        plot_text()
        if storage["bull_market"] is True:
            call = "BULL SUPPORT"
        else:
            call = "BEAR DESPAIR"
        print(
            (
                "[%s] %s BUY %s %.2f %s at %.8f value %.2f %s"
                % (
                    now,
                    storage["trades"],
                    call,
                    portfolio["assets"],
                    ASSET,
                    price,
                    portfolio["currency"],
                    CURRENCY,
                )
            )
        )

        plt.plot(
            info["current_time"],
            (price),
            markersize=10,
            marker="^",
            color="lime",
            label="buy",
        )
    portfolio["currency"] = 0
    if LIVE:
        plt.pause(0.0001)
        watchdog()


def test_sell(price):  # Execute a backtest sell

    storage["trades"] += 1
    now = info["current_time"]
    storage["sells"][0].append(info["current_time"])
    storage["sells"][1].append(price)
    portfolio["currency"] = portfolio["assets"] * price
    storage["holding"] = False
    if LIVE or BACKTEST:
        plot_text()
        plt.plot(
            info["current_time"],
            (price),
            markersize=10,
            marker="v",
            color="coral",
            label="sell",
        )
        if storage["bull_market"] is True:
            call = "BULL OVERBOUGHT"
        else:
            call = "BEAR RESISTANCE"
        if storage["buys"][1][-1]:
            buy_price = storage["buys"][1][-1]
            buy_time = storage["buys"][0][-1]
            if price > buy_price:
                plt.plot(
                    (buy_time, now),
                    (buy_price, price),
                    color="lime",
                    label="win",
                    lw=2,
                )
            else:
                plt.plot(
                    (buy_time, now),
                    (buy_price, price),
                    color="coral",
                    label="loss",
                    lw=2,
                )

        print(
            (
                "[%s] %s SELL %s %.2f %s at %.8f value %.2f %s"
                % (
                    time.ctime(now),
                    storage["trades"],
                    call,
                    portfolio["assets"],
                    ASSET,
                    price,
                    portfolio["currency"],
                    CURRENCY,
                )
            )
        )
    portfolio["assets"] = 0
    if LIVE:
        plt.pause(0.0001)
        watchdog()


# PLOT
# ======================================================================


def draw_state_machine(  # Plots primary trade indications
    now,
    selloff,
    support,
    resistance,
    despair,
    buying,
    selling,
    min_cross,
    max_cross,
    bull_market,
    ma1,
    ma2,
    ma1poly,
    ma2poly,
):
    # do not plot state machine for sales backtests
    if not SALES:
        # shade active market red or green
        # shade extinct market purple
        if bull_market:
            plt.plot(
                (now, now),
                (selloff, support),
                color="lime",
                label="state",
                alpha=0.15,
            )
            plt.plot(
                (now, now),
                (resistance, despair),
                color="darkorchid",
                label="state",
                alpha=0.15,
            )
        else:
            plt.plot(
                (now, now),
                (resistance, despair),
                color="red",
                label="state",
                alpha=0.15,
            )
            plt.plot(
                (now, now),
                (selloff, support),
                color="darkorchid",
                label="state",
                alpha=0.15,
            )
        # set state machine line size in backtest and live modes
        m1 = 0.5
        m2 = 1.5
        m3 = 3
        m4 = 3
        m5 = 3
        if LIVE or PAPER or ORDER_TEST:
            m1 = 1
            m2 = 3
            m3 = 4
            m4 = 1
            m5 = 8
            # the labels for ma1 and ma2 are CRITICAL for live warmup
            # DO NOT reassign outside of draw_state_machine()
            # they will be used in polynomial_regression()
            # however we'll plot them very small and transparent
            plt.plot(
                now,
                ma1,
                markersize=0.01,
                marker=".",
                color="black",
                label="ma1",
                alpha=0.01,
            )
            plt.plot(
                now,
                ma2,
                markersize=0.01,
                marker=".",
                color="black",
                label="ma2",
                alpha=0.01,
            )
        # in backtests we plot ma2, when live ma2poly as long
        long_average = ma2
        if info["live"]:
            long_average = ma2poly
        plt.plot(
            now,
            long_average,
            markersize=m5,
            marker=".",
            color="aqua",
            label="long",
        )
        # plot extinct market extremes purple
        plt.plot(
            now,
            selloff,
            markersize=m2,
            marker=".",
            color="darkorchid",
            label="selloff",
        )
        plt.plot(
            now,
            support,
            markersize=m2,
            marker=".",
            color="darkorchid",
            label="support",
        )
        plt.plot(
            now,
            despair,
            markersize=m2,
            marker=".",
            color="darkorchid",
            label="despair",
        )
        plt.plot(
            now,
            resistance,
            markersize=m2,
            marker=".",
            color="darkorchid",
            label="resistance",
        )
        # plot width of signal line
        if storage["bull_market"]:
            plt.plot(
                now,
                max_cross,
                markersize=m3,
                marker=".",
                color="cornsilk",
                label="max_cross",
            )
            plt.plot(
                now,
                min_cross,
                markersize=m1,
                marker=".",
                color="cornsilk",
                label="min_cross",
            )
        else:
            plt.plot(
                now,
                max_cross,
                markersize=m1,
                marker=".",
                color="cornsilk",
                label="max_cross",
            )
            plt.plot(
                now,
                min_cross,
                markersize=m3,
                marker=".",
                color="cornsilk",
                label="min_cross",
            )
        # shade between bull and bear signal lines
        plt.plot(
            (now, now),
            (max_cross, min_cross),
            color="cornsilk",
            label="cross",
            alpha=0.15,
        )
        # plot active market extremes in red and green extra bold
        plt.plot(
            now,
            buying,
            markersize=m5,
            marker=".",
            color="green",
            label="buying",
        )
        plt.plot(
            now,
            selling,
            markersize=m5,
            marker=".",
            color="red",
            label="selling",
        )


def test_rechart_orders():  # Set buy/sell markers on top

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
    plot_text()
    plt.pause(0.01)


def test_chart():  # Add objects to backtest plot

    try:
        # localize data
        now = info["current_time"]
        ma1 = ma1poly = storage["ma1"][-1]
        ma2 = ma2poly = storage["ma2"][-1]
        if info["live"]:
            ma1poly = storage["ma1poly"][-1]
            ma2poly = storage["ma2poly"][-1]
        close = storage["close"]
        high = storage["high"]
        low = storage["low"]
        selloff = storage["selloff"]
        despair = storage["despair"]
        resistance = storage["resistance"]
        support = storage["support"]
        max_cross = storage["max_cross"]
        min_cross = storage["min_cross"]
        bull_market = storage["bull_market"]
        buying = storage["buying"]
        selling = storage["selling"]

        draw_state_machine(  # Plots primary trade indications
            now,
            selloff,
            support,
            resistance,
            despair,
            buying,
            selling,
            min_cross,
            max_cross,
            bull_market,
            ma1,
            ma2,
            ma1poly,
            ma2poly,
        )

        # plot candles
        plt.plot(
            (now, now),
            ((high[-1]), (low[-1])),
            color="m",
            label="high_low",
            alpha=0.5,
        )
        plt.plot(
            now,
            (close[-1]),
            markersize=4,
            marker=".",
            color="y",
            label="close",
        )

        if info["live"]:
            plt.pause(0.01)
    except:
        pass


def live_chart_zero():

    # localize indicators
    now = info["current_time"]
    bull_market = storage["bull_market"]
    selloff = storage["selloff"]
    despair = storage["despair"]
    # draw vertical line at beginning of live session
    plt.plot(
        (now, now),
        (selloff, despair),
        color="white",
        label="vertical start",
        lw=5,
        alpha=0.2,
    )
    # clone the backtest in higher resolution for last 24hrs
    ma1_period = MA1 * 86400 / 14400.0
    ma2_period = MA2 * 86400 / 14400.0
    ma1_arr = float_sma(data["14400"]["close"], ma1_period)
    ma2_arr = float_sma(data["14400"]["close"], ma2_period)
    unix = data["14400"]["unix"]
    # backtest state machine clone; 24 hours high resolution
    for i in range(-1, -10, -1):
        for z in range(0, 14400, 600):
            try:
                now = unix[i] + z
                ma1 = ma1poly = ma1_arr[i]
                ma2 = ma2poly = ma2_arr[i]
                min_cross = MIN_CROSS * ma1
                max_cross = MAX_CROSS * min_cross
                bull_stop = BULL_STOP * ma2
                bear_stop = BEAR_STOP * ma2
                selloff = SELLOFF * ma1
                despair = DESPAIR * ma1
                support = max((SUPPORT * ma1), bull_stop)
                resistance = min((RESISTANCE * ma1), bear_stop)
                selloff *= 1 - GRAVITAS
                resistance *= 1 - GRAVITAS
                support *= 1 + GRAVITAS
                despair *= 1 + GRAVITAS
                if bull_market:
                    selling = selloff
                    buying = support
                else:
                    buying = despair
                    selling = resistance
                # plot state machine
                draw_state_machine(
                    now,
                    selloff,
                    support,
                    resistance,
                    despair,
                    buying,
                    selling,
                    min_cross,
                    max_cross,
                    bull_market,
                    ma1,
                    ma2,
                    ma1poly,
                    ma2poly,
                )
            except Exception as e:
                print(trace(e))
                pass
    # plot latest five minute data
    now = int(time.time())
    d = backtest_candles((now - LIVE_PLOT_DEPTH), now, 300)
    high = d["high"]
    low = d["low"]
    close = d["close"]
    unix = d["unix"]
    for i in range(len(unix)):
        now = unix[i]
        plt.plot(
            (now, now),
            (high[i], low[i]),
            color="magenta",
            label="high/low",
        )
        if high[i] > close[i]:
            plt.plot(
                now,
                high[i],
                markersize=4,
                marker=".",
                color="magenta",
                label="high",
            )
        if low[i] < close[i]:
            plt.plot(
                now,
                low[i],
                markersize=4,
                marker=".",
                color="magenta",
                label="low",
            )
        plt.plot(
            now,
            close[i],
            markersize=4,
            marker=".",
            color="yellow",
            label="close",
        )
    plt.pause(0.001)
    plot_format()


def live_chart():  # Add objects to live plot

    if info["tick"] == 0:
        live_chart_zero()
    # localize low frequency indicators
    now = info["current_time"]
    ma1 = storage["ma1"][-1]
    ma2 = storage["ma2"][-1]
    ma1poly = storage["ma1poly"][-1]
    ma2poly = storage["ma2poly"][-1]
    selloff = storage["selloff"]
    despair = storage["despair"]
    support = storage["support"]
    resistance = storage["resistance"]
    buying = storage["buying"]
    selling = storage["selling"]
    max_cross = storage["max_cross"]
    min_cross = storage["min_cross"]
    bull_market = storage["bull_market"]
    # plot state machine
    draw_state_machine(
        now,
        selloff,
        support,
        resistance,
        despair,
        buying,
        selling,
        min_cross,
        max_cross,
        bull_market,
        ma1,
        ma2,
        ma1poly,
        ma2poly,
    )
    # localize high frequency indicators
    low = storage["low"]
    high = storage["high"]
    last = storage["last"]
    book = storage["book"]
    ask = book["askp"][0]
    bid = book["bidp"][0]
    ma3 = storage["ma3"][-1]
    ma4 = storage["ma4"][-1]
    m_volume = storage["m_volume"]
    scalp_support = storage["scalp_support"]
    scalp_resistance = storage["scalp_resistance"]
    # plot scalp thresholds
    plt.plot(
        now,
        scalp_resistance,
        markersize=4,
        marker=".",
        color="tomato",
        label="scalp_resistance",
    )
    plt.plot(
        now,
        scalp_support,
        markersize=4,
        marker=".",
        color="palegreen",
        label="scalp_support",
    )
    # plot high and low
    plt.plot((now, now), (high, low), color="m", label="high/low")
    if high > last:
        plt.plot(
            now,
            high,
            markersize=4,
            marker=".",
            color="magenta",
            label="high",
        )
    if low < last:
        plt.plot(
            now,
            low,
            markersize=4,
            marker=".",
            color="magenta",
            label="low",
        )
    # plot top of orderbook
    plt.plot(
        now, ask, markersize=3, marker=".", color="teal", label="ask"
    )
    plt.plot(
        now, bid, markersize=3, marker=".", color="teal", label="bid"
    )
    # plot last price
    plt.plot(
        now,
        last,
        markersize=(4 * m_volume),
        marker=".",
        color="yellow",
        label="last",
    )

    plt.pause(0.001)


def zoom_out_live():

    ax = plt.gca()
    # plot zoom out to state machine
    yd = []  # matrix of y values from all lines on plot
    xd = []  # matrix of x values from all lines on plot
    for n in range(len(ax.get_lines())):
        line = ax.get_lines()[n]
        yd.append((line.get_ydata()).tolist())
        xd.append((line.get_xdata()).tolist())
    yd = [item for sublist in yd for item in sublist]
    ymin, ymax = np.min(yd), np.max(yd)
    ax.set_ylim([0.95 * ymin, 1.05 * ymax])
    xd = [item for sublist in xd for item in sublist]
    xmin, xmax = np.min(xd), np.max(xd)
    ax.set_xlim([xmin, xmax])
    plot_text()
    plt.pause(0.01)
    # todo, this definition can be optimized to use less resource
    return ymax, ymin, xmax, xmin


def plot_format():

    # Set plot colors and attributes
    warnings.filterwarnings("ignore", category=cbook.mplDeprecation)
    ax = plt.gca()
    ax.patch.set_facecolor("0.1")
    ax.yaxis.tick_right()
    ax.spines["bottom"].set_color("0.5")
    ax.spines["top"].set_color(None)
    ax.spines["right"].set_color("0.5")
    ax.spines["left"].set_color(None)
    ax.tick_params(axis="x", colors="0.7", which="both")
    ax.tick_params(axis="y", colors="0.7", which="both")
    ax.yaxis.label.set_color("0.9")
    ax.xaxis.label.set_color("0.9")
    plt.minorticks_on
    plt.grid(b=True, which="major", color="0.2", linestyle="-")
    plt.grid(b=True, which="minor", color="0.2", linestyle="-")
    if (info["live"] is False) and (info["tick"] > 1):
        plt.ylabel("LOGARITHMIC PRICE SCALE")
        plt.yscale("log")
    if info["live"] is True:
        plt.ylabel("MARKET PRICE")
    """
    scalar_format = matplotlib.ticker.ScalarFormatter()
    ax.yaxis.set_major_formatter(scalar_format)
    ax.yaxis.set_minor_formatter(scalar_format)
    """
    satoshi_format = matplotlib.ticker.FormatStrFormatter("%.8f")
    ax.yaxis.set_major_formatter(satoshi_format)
    ax.yaxis.set_minor_formatter(satoshi_format)
    ax.title.set_color("darkorchid")
    # custom x axis label spacing
    stepsize = 86400
    if info["live"]:
        stepsize = 7200
    else:
        if DAYS > 20:
            stepsize = 864000
        if DAYS > 100:
            stepsize = 2592000
        if DAYS > 1000:
            stepsize = 25920000
    start, end = ax.get_xlim()
    ax.xaxis.set_ticks(np.arange((end - end % 3600), start, -stepsize))
    # format x axis labels with ISO style timestamps

    def iso(x, pos):
        if not info["live"]:
            return (datetime.fromtimestamp(x)).strftime("%Y-%m-%d")
        else:
            return (datetime.fromtimestamp(x)).strftime("%m/%d %H:%M")

    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(iso))
    plt.gcf().autofmt_xdate(rotation=30)
    # custom log scale y axis label spacing
    if info["tick"] > 1:
        ymax, ymin, xmax, xmin = zoom_out_live()
        if info["live"] is False:
            # add sub minor ticks
            set_sub_formatter = []
            sub_ticks = [10, 11, 12, 14, 16, 18, 22, 25, 35, 45]
            sub_range = [-8, 8]
            for i in sub_ticks:
                for j in range(sub_range[0], sub_range[1]):
                    set_sub_formatter.append(i * 10 ** j)
            k = []
            for l in set_sub_formatter:
                if ymin < l < ymax:
                    k.append(l)
            ax.set_yticks(k)
    # live y axis tick spacing
    if info["live"]:
        start, end = ax.get_ylim()
        stepsize = abs(start - end) / 25
        ax.yaxis.set_ticks(np.arange(end, start, -stepsize))
    plt.tight_layout()
    if info["live"]:
        plt.pause(0.001)


def plot_text():  # Display market condition on plot

    # clear text
    storage["text"] = storage.get("text", [])
    for text in storage["text"]:
        try:
            text.remove()
        except:
            pass
    # determine current boundaries of plot
    pltxlim0 = float(plt.xlim()[0])
    pltxlim1 = float(plt.xlim()[1])
    pltylim0 = float(plt.ylim()[0])
    pltylim1 = float(plt.ylim()[1])
    # allow text placement per plot boundaries

    def scale(axis, alpha):
        if axis == "x":
            return alpha * (pltxlim1 - pltxlim0) + pltxlim0
        elif axis == "y":
            return alpha * (pltylim1 - pltylim0) + pltylim0

    # BITSHARES EXTINCTION EVENT in aqua
    textx = scale("x", 0.1)
    texty = scale("y", 0.7)
    if storage["bull_market"]:
        texty = scale("y", 0.1)
    storage["text"].append(
        plt.text(
            textx,
            texty,
            "EXTINCTION EVENT",
            color="aqua",
            alpha=0.3,
            size=25,
            weight="extra bold",
        )
    )
    textx = scale("x", 0.1)
    texty = scale("y", 0.75)
    if storage["bull_market"]:
        texty = scale("y", 0.15)
    storage["text"].append(
        plt.text(
            textx,
            texty,
            "BitShares",
            color="aqua",
            alpha=0.3,
            size=35,
            weight="extra bold",
        )
    )
    # LAST, PAIR, MODE, DIVERGENCE in dark orange
    textx = scale("x", 0.75)
    texty = scale("y", 0.75)
    pair = PAIR
    storage["text"].append(
        plt.text(
            textx,
            texty,
            pair,
            horizontalalignment="center",
            color="darkorange",
            alpha=0.50,
            size=15,
            weight="extra bold",
        )
    )
    if info["live"]:
        textx = scale("x", 0.75)
        texty = scale("y", 0.65)
        text = " LAST: %.8f\n" % storage["last"]
        storage["text"].append(
            plt.text(
                textx,
                texty,
                text,
                horizontalalignment="center",
                color="darkorange",
                alpha=0.50,
                size=15,
                weight="extra bold",
            )
        )
    textx = scale("x", 0.75)
    texty = scale("y", 0.1)
    text = ""

    if MODE == 1:
        text = "BACKTEST"
    if MODE == 2:
        text = "PAPER"
    if MODE == 3:
        text = "LIVE"
    if MODE == 4:
        text = "SALES"
    if MODE == 6:
        text = "TEST ORDERS"
    if MODE in [2, 3, 6]:
        if not info["live"]:
            text = "INITIALING"

    storage["text"].append(
        plt.text(
            textx,
            texty,
            text,
            horizontalalignment="center",
            color="darkorange",
            alpha=0.50,
            size=30,
            weight="extra bold",
        )
    )
    if info["live"]:
        # display divergence and days to next crossing
        divergence_text = (" Divergence %.8f\n" % storage["mesh"]) + (
            " Next Cross %.2f Days" % storage["next_cross"]
        )
        textx = scale("x", 0.75)
        texty = scale("y", 0.55)
        text = divergence_text
        storage["text"].append(
            plt.text(
                textx,
                texty,
                text,
                horizontalalignment="center",
                color="darkorange",
                size=10,
            )
        )
    # dynamic state machine text
    if info["live"]:
        high = storage["high"]
        low = storage["low"]
    else:
        high = storage["high"][-1]
        low = storage["low"][-1]
    # bull market labels
    if storage["bull_market"]:
        textx = scale("x", 0.1)
        texty = scale("y", 0.7)
        storage["text"].append(
            plt.text(
                textx,
                texty,
                "BULL MARKET",
                color="lime",
                alpha=0.3,
                size=30,
                weight="extra bold",
            )
        )
        textx = scale("x", 0.125)
        texty = scale("y", 0.65)
        if low < storage["buying"]:
            storage["text"].append(
                plt.text(
                    textx,
                    texty,
                    "BUY SUPPORT",
                    color="lime",
                    alpha=0.5,
                    size=20,
                    weight="extra bold",
                )
            )
        elif high > storage["selling"]:
            storage["text"].append(
                plt.text(
                    textx,
                    texty,
                    "SELL OVERBOUGHT",
                    color="red",
                    alpha=0.5,
                    size=20,
                    weight="extra bold",
                )
            )
    # bear market labels
    else:
        textx = scale("x", 0.1)
        texty = scale("y", 0.1)
        storage["text"].append(
            plt.text(
                textx,
                texty,
                "BEAR MARKET",
                color="red",
                alpha=0.3,
                size=30,
                weight="extra bold",
            )
        )
        textx = scale("x", 0.125)
        texty = scale("y", 0.05)
        if low < storage["buying"]:
            storage["text"].append(
                plt.text(
                    textx,
                    texty,
                    "BUY DESPAIR",
                    color="lime",
                    alpha=0.5,
                    size=20,
                    weight="extra bold",
                )
            )
        elif high > storage["selling"]:
            storage["text"].append(
                plt.text(
                    textx,
                    texty,
                    "SELL RESISTANCE",
                    color="red",
                    alpha=0.5,
                    size=20,
                    weight="extra bold",
                )
            )

    if info["live"]:
        # label selloff, support, resistance, and  despair
        # use dynamic text showing values
        textx = scale("x", 0.52)
        selloff_c = "darkorchid"
        support_c = "darkorchid"
        resistance_c = "red"
        despair_c = "green"
        if storage["bull_market"]:
            selloff_c = "red"
            support_c = "green"
            resistance_c = "darkorchid"
            despair_c = "darkorchid"
        texty = storage["selloff"]
        text = "BULL SELLOFF"
        storage["text"].append(
            plt.text(
                textx,
                texty,
                text,
                weight="extra bold",
                size=12,
                color=selloff_c,
                verticalalignment="center",
            )
        )
        texty = storage["support"]
        text = "BULL SUPPORT"
        storage["text"].append(
            plt.text(
                textx,
                texty,
                text,
                weight="extra bold",
                size=12,
                color=support_c,
                verticalalignment="center",
            )
        )
        texty = storage["resistance"]
        text = "BEAR RESISTANCE"
        storage["text"].append(
            plt.text(
                textx,
                texty,
                text,
                weight="extra bold",
                size=12,
                color=resistance_c,
                verticalalignment="center",
            )
        )
        texty = storage["despair"]
        text = "BEAR DESPAIR"
        storage["text"].append(
            plt.text(
                textx,
                texty,
                text,
                weight="extra bold",
                size=12,
                color=despair_c,
                verticalalignment="center",
            )
        )
        """
        texty = storage['ma1poly'][-1]
        text = 'RAW SIGNAL (MA1)' % storage['ma1poly'][-1]
        storage['text'].append(
            plt.text(textx, texty, text,
                     color='gray', verticalalignment='center', size=8))
        """
        # label long and signal lines; include slope and concavity
        textx = scale("x", 0.75)
        long_text = "LONG (MA2)\n"
        long_text += "%.8f f(x)\n%.8f f`(x)\n%.8f f``(x)" % (
            storage["ma2poly"][-1],
            storage["ma2_slope"],
            storage["ma2_concavity"],
        )
        signal_text = "SIGNAL (MA1*offset)\n"
        signal_text += "%.8f f(x)\n%.8f f`(x)\n%.8f f``(x)" % (
            storage["signal_line"],
            storage["ma1_slope"],
            storage["ma1_concavity"],
        )
        texty = storage["long_average"]
        if storage["bull_market"]:
            texty *= 0.95
        else:
            texty *= 1.05
        text = long_text
        storage["text"].append(
            plt.text(
                textx,
                texty,
                text,
                horizontalalignment="center",
                color="aqua",
                verticalalignment="center",
                size=8,
            )
        )
        texty = storage["signal_line"]
        if storage["bull_market"]:
            texty *= 1.05
        else:
            texty *= 0.95
        text = signal_text
        storage["text"].append(
            plt.text(
                textx,
                texty,
                text,
                horizontalalignment="center",
                color="cornsilk",
                verticalalignment="center",
                size=8,
            )
        )
        # triangle marker for last price on far right
        textx = scale("x", 1.0)
        texty = storage["last"]
        storage["text"].append(
            plt.text(
                textx,
                texty,
                "> ",
                horizontalalignment="right",
                color="magenta",
                verticalalignment="center",
                size=40,
            )
        )
        # custom legend on upper right; \u2588 is a solid square
        textx = scale("x", 1.0)
        y = 0.95
        texty = scale("y", y)
        storage["text"].append(
            plt.text(
                textx,
                texty,
                "EXTINCT EVENT \u2588 ",
                horizontalalignment="right",
                color="darkorchid",
                size=8,
            )
        )
        y *= 0.97
        texty = scale("y", y)
        storage["text"].append(
            plt.text(
                textx,
                texty,
                "HIGH & LOW \u2588 ",
                horizontalalignment="right",
                color="magenta",
                size=8,
            )
        )
        y *= 0.97
        texty = scale("y", y)
        storage["text"].append(
            plt.text(
                textx,
                texty,
                "BID & ASK \u2588 ",
                horizontalalignment="right",
                color="teal",
                size=8,
            )
        )
        y *= 0.97
        texty = scale("y", y)
        storage["text"].append(
            plt.text(
                textx,
                texty,
                ("PRIMARY SELL %.8f \u2588 " % storage["selling"]),
                horizontalalignment="right",
                color="red",
                size=8,
            )
        )
        y *= 0.97
        texty = scale("y", y)
        storage["text"].append(
            plt.text(
                textx,
                texty,
                (
                    "SCALP SELL %.8f \u2588 "
                    % storage["scalp_resistance"]
                ),
                horizontalalignment="right",
                color="tomato",
                size=8,
            )
        )
        y *= 0.97
        texty = scale("y", y)
        storage["text"].append(
            plt.text(
                textx,
                texty,
                ("LAST %.8f \u2588 " % storage["last"]),
                horizontalalignment="right",
                color="yellow",
                size=8,
            )
        )
        y *= 0.97
        texty = scale("y", y)
        storage["text"].append(
            plt.text(
                textx,
                texty,
                ("SCALP BUY %.8f \u2588 " % storage["scalp_support"]),
                horizontalalignment="right",
                color="palegreen",
                size=8,
            )
        )
        y *= 0.97
        texty = scale("y", y)
        storage["text"].append(
            plt.text(
                textx,
                texty,
                ("PRIMARY BUY %.8f \u2588 " % storage["buying"]),
                horizontalalignment="right",
                color="lime",
                size=8,
            )
        )
        y *= 0.97
        texty = scale("y", y)
        storage["text"].append(
            plt.text(
                textx,
                texty,
                "LONG AVERAGE \u2588 ",
                horizontalalignment="right",
                color="aqua",
                size=8,
            )
        )
        y *= 0.97
        texty = scale("y", y)
        storage["text"].append(
            plt.text(
                textx,
                texty,
                "SIGNAL LINE \u2588 ",
                horizontalalignment="right",
                color="cornsilk",
                size=8,
            )
        )
    plt.tight_layout()
    if info["live"]:
        plt.pause(0.001)


def test_plot():  # Display backtest plot

    begin = info["begin"]
    end = info["end"]
    while (end - begin) > LIVE_PLOT_DEPTH:
        # PLOT FORMAT
        try:
            ax = plt.gca()
            # Window Plot
            left, right = ax.set_xlim(left=begin - 50, right=end + 50)
            # Prevent Memory Leak Outside Plot Window
            for l in ax.get_lines():
                xval = l.get_xdata()[0]
                if xval < begin:
                    l.remove()
            if LIVE:
                begin = begin + 0.3 * (end - begin)
            else:
                begin = end
            plt.tight_layout()
            plt.pause(0.0001)
        except:
            print("animated test plot failed")
    plot_text()
    plot_format()

    if BACKTEST:
        try:
            plt.autoscale(enable=True, axis="y")
            plt.pause(0.0001)

        except:
            print("static test plot failed")


def live_plot():  # Display live plot

    now = int(time.time())
    ax = plt.gca()
    # Window Plot
    ax.set_xlim([(now - LIVE_PLOT_DEPTH), (now + LIVE_PLOT_PROJECTION)])
    # Prevent Memory Leak Outside Plot Window; remove unnecessary data
    for line in ax.get_lines():
        xval = line.get_xdata()[0]
        if xval < (ax.get_xlim()[0]):
            line.remove()
            del line
        if info["tick"] == 0:
            if xval > time.time():
                line.remove()
                del line
    plot_text()
    plt.tight_layout()
    plt.pause(0.0001)


# DIAGNOSTICS AND PRINTING
# ======================================================================


def test_stop():  # Display results of backtest session

    # localize
    assets = portfolio["assets"]
    currency = portfolio["currency"]
    close = storage["close"][-1]
    # move to currency
    if BACKTEST and (assets > 0.1) and CURRENCY_STOP:
        print("stop() EXIT TO CURRENCY")
        test_sell(price=close)
    # calculate return on investment
    end_max_assets = assets + (currency / close)
    end_max_currency = currency + (assets * close)
    roi_assets = end_max_assets / storage["begin_max_assets"]
    roi_currency = end_max_currency / storage["begin_max_currency"]
    storage["roi_currency"] = roi_currency
    storage["roi_assets"] = roi_assets
    storage["roi_gross"] = (roi_currency * roi_assets) ** (1 / 2.0)
    days = (info["end"] - info["begin"]) / 86400.0
    frequency = (SATOSHI + storage["trades"]) / days
    storage["dpt"] = 1.0 / frequency

    # A = P*(1+(r/n))**(n*t)
    P = storage["begin_max_currency"]
    t = DAYS / 365.0
    A = end_max_currency
    n = 1.0
    r = n * ((A / P) ** (1 / (n * t)) - 1)
    storage["apy_currency"] = r

    if LIVE or BACKTEST:

        print(
            "=========================================================="
        )
        print(("START DATE........: %s" % time.ctime(info["begin"])))
        print(("END DATE..........: %s" % time.ctime(info["end"])))
        print(("DAYS..............: %.1f" % days))
        print(("TICKS.............: %s" % info["tick"]))
        print(("HOLDING TICKS.....: %s" % storage["holding_ticks"]))
        print(
            (
                "HOLDING RATIO.....: %.3f"
                % (storage["holding_ticks"] / info["tick"])
            )
        )
        print(("TRADES............: %s" % storage["trades"]))
        print(("DAYS PER TRADE....: %.1f" % storage["dpt"]))

        print(("START PRICE.......: %.8f " % data["close"][-DAYS]))
        print(("END PRICE.........: %.8f" % close))
        print(
            (
                "START PORTFOLIO...: %.1f %s %.1f %s"
                % (START_CURRENCY, CURRENCY, START_ASSETS, ASSET)
            )
        )
        print(
            (
                "START MAX ASSETS..: %s %s"
                % (storage["begin_max_assets"], ASSET)
            )
        )
        print(("END MAX ASSETS....: %s %s" % (end_max_assets, ASSET)))
        print(("ROI ASSETS........: %.2fX" % roi_assets))
        print(
            (
                "START MAX CURRENCY: %s %s"
                % (storage["begin_max_currency"], CURRENCY)
            )
        )
        print(
            ("END MAX CURRENCY..: %s %s" % (end_max_currency, CURRENCY))
        )
        print(("ROI CURRENCY......: %.2fX" % roi_currency))
        # print(('APY CURRENCY......: %.2f' % storage['apy_currency']))
        print(
            "=========================================================="
        )
        print(VERSION)
        print("~===END BACKTEST=========================~")
        test_rechart_orders()


def print_tune():  # Display input thresholds

    storage["roi_currency"] = storage.get("roi_currency", ROI)
    storage["roi_assets"] = storage.get("roi_assets", ROI)
    storage["roi_gross"] = storage.get("roi_gross", ROI)
    storage["dpt"] = storage.get("dpt", DPT)
    storage["trades"] = storage.get("trades", 0)

    frequency = (SATOSHI + storage["trades"]) / DAYS

    z = "="

    print("#######################################")
    print("# %s" % time.ctime())
    print("#######################################")   
    print(("# DAYS          : %s" % DAYS))
    print(("# DPT           : %.1f" % storage["dpt"]))
    print(("# ROI CURRENCY  : %.2fX" % storage["roi_currency"]))
    print(("# ROI ASSETS    : %.2fX" % storage["roi_assets"]))
    print(("# ROI GROSS     : %.2fX" % storage["roi_gross"]))
    print(("# TUNE DATE     : %s" % time.ctime()))
    print("#######################################")    
    print(('CANDLE_SOURCE  = "%s"' % CANDLE_SOURCE))
    print(('CURRENCY       = "%s"' % CURRENCY))
    print(('ASSET          = "%s"' % ASSET))
    print(("MA1            %s %.3f" % (z, MA1)))
    print(("MA2            %s %.3f" % (z, MA2)))
    print(("SELLOFF        %s %.4f" % (z, SELLOFF)))
    print(("SUPPORT        %s %.4f" % (z, SUPPORT)))
    print(("RESISTANCE     %s %.4f" % (z, RESISTANCE)))
    print(("DESPAIR        %s %.4f" % (z, DESPAIR)))
    print(("MIN_CROSS      %s %.4f" % (z, MIN_CROSS)))
    print(("MAX_CROSS      %s %.4f" % (z, MAX_CROSS)))
    print(("BULL_STOP      %s %.4f" % (z, BULL_STOP)))
    print(("BEAR_STOP      %s %.4f" % (z, BEAR_STOP)))



def trace(e):  # traceback message
    print(
        "                                                  "
        + "               !@#$%^&*(){}[]{}()*&^%$#@!"
    )
    print("@litepresence on telegram for faster development")
    print("")
    return (
        "========================================================"
        + "\n\n"
        + str(time.ctime())
        + " "
        + str(type(e).__name__)
        + "\n\n"
        + str(e.args)
        + "\n\n"
        + str(traceback.format_exc())
        + "\n\n"
    )


def diagnostics(level=[]):

    try:
        import psutil  # REQUIRES MODULE INSTALL

        proc = psutil.Process()

        if 1 in level:
            num_open_files = proc.num_fds()
            print("")
            print("file descriptors:", num_open_files)
            print("connections:", len(proc.connections()))
        if 2 in level:
            import psutil

            proc = psutil.Process()
            n = 1
            open_files = proc.open_files()
            for i in range(len(open_files)):
                if "ttf" not in str(open_files[i]):
                    print(n, str(open_files[i]).split("/")[-1])
                    n += 1
            print(proc.io_counters())
            connections = proc.connections()
            for i in range(len(connections)):
                print(i, connections[i])
            print("")
            processes = psutil.process_iter()
            for i in range(len(processes)):
                print(i, processes[i])
            print("")
    except Exception as e:
        msg = str(type(e).__name__) + str(e.args) + "psutil"
        print(msg)

    if 3 in level:
        fds = {}
        base = "/proc/self/fd"
        for num in os.listdir(base):
            try:
                fds[int(num)] = os.readlink(os.path.join(base, num))
            except:
                pass
        print(fds)
    print("")


def version():

    print(
        "Python3 and Linux Required; your system: Python",
        sys.version.split(" ")[0],
        "-",
        sys.platform,
        "OS",
    )
    sys.stdout.write("\x1b]2;" + "Bitshares extinctionEVENT" + "\x07")
    print("")
    print(VERSION)
    print("")


def logo():
    def download_text(key):
        # ascii artwork stored in pastebin
        urls = {"extinction-event": "https://pastebin.com/raw/5YuEHcC4"}
        try:
            return (requests.get(urls[key], timeout=(6, 30))).text
        except:
            return ""

    def ry():
        return choice(["red", "yellow"])

    ev = download_text("extinction-event")
    a = r"""            *.   ~          %             `     ,        """
    b = r"""      *.()      *`()      *~()    @      *,()      *.()  """
    c = r"""    *()/     *()/\     *()/\%   % @       *()/\     *()/ """
    d = r""" ()/_ ()/\_ ()/_ ()/_ ()/_ ()/_ ()()() ()(@@)_ ()()()()()"""
    for i in range(20):
        print("\033c")
        print("     " + " ".join([it(ry(), i) for i in sample(a, 27)]))
        print("     " + " ".join([it(ry(), i) for i in sample(a, 27)]))
        print("     " + " ".join([it(ry(), i) for i in sample(a, 27)]))
        print("     " + " ".join([it(ry(), i) for i in sample(b, 27)]))
        print("    " + " ".join([it(ry(), i) for i in sample(c, 28)]))
        print("   " + " ".join([it(ry(), i) for i in sample(c, 29)]))
        print("    " + " ".join([it(ry(), i) for i in sample(d, 28)]))
        print("     " + " ".join([it(ry(), i) for i in sample(d, 27)]))
        print(it("yellow", ev))
        print("")
        time.sleep(0.1)


# DATA FORMATTING
# ======================================================================


def it(style, text):
    # colored text in terminal
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
    # current 24 hour clock formatted HH:MM:SS
    return str(time.ctime())[11:19]


def satoshi(n):
    # prices rounded to satoshi
    return float("%.8f" % float(n))


def satoshi_str(n):
    # string prices rounded to satoshi
    return "%.8f" % float(n)


def dictionaries():
    # primary dictionaries used in global space
    global info, storage, portfolio, book
    info = {}  # tick data
    book = {}  # bid / ask data
    storage = {}  # candle data
    portfolio = {}  # account balance data


def from_iso_date(date):
    # used for END point of backtest ISO to UNIX conversion
    return int(timegm(time.strptime(str(date), "%Y-%m-%d")))


# ALGORITHM
# ======================================================================


def float_sma(array, period):  # floating point period moving average
    def moving_average(array, period):  # numpy array moving average
        csum = np.cumsum(array, dtype=float)
        csum[period:] = csum[period:] - csum[:-period]
        return csum[period - 1 :] / period

    if period == int(period):
        return moving_average(array, int(period))
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
        ma = (floor_ratio * floor) + (ceil_ratio * ceil)
        return ma


def indicators():  # Post process data

    global storage
    global book

    ma1_period = MA1 * 86400.0 / CANDLE
    ma2_period = MA2 * 86400.0 / CANDLE

    if not info["live"]:
        # alpha moving averages
        storage["ma1"] = float_sma(storage["close"], ma1_period)
        storage["ma2"] = float_sma(storage["close"], ma2_period)

    if info["live"]:
        print("indicators()")
        # alpha moving averages
        ma1 = storage["ma1"] = float_sma(
            data["14400"]["close"], ma1_period
        )
        ma2 = storage["ma2"] = float_sma(
            data["14400"]["close"], ma2_period
        )

        # scalp moving averages
        storage["ma3"] = float_sma(data["300"]["close"], 288 * MA3)
        storage["ma4"] = float_sma(data["300"]["close"], 288 * MA4)

        # 20 minute high and low
        storage["high"] = max(data["300"]["high"][-4:])
        storage["low"] = min(data["300"]["low"][-4:])
        storage["high"] = max(storage["high"], storage["last"])
        storage["low"] = min(storage["low"], storage["last"])

        # means to buy and percent invested
        assets = portfolio["assets"]
        currency = portfolio["currency"]
        means = storage["means"] = currency / storage["last"]
        max_assets = storage["max_assets"] = assets + means
        storage["max_currency"] = max_assets * storage["last"]

        storage["asset_ratio"] = assets / max_assets
        portfolio["percent_invested"] = 100 * storage["asset_ratio"]
        portfolio["percent_divested"] = (
            100 - portfolio["percent_invested"]
        )

        # recent volume ratio for plotting
        depth = 100
        v = data["300"]["volume"][-1]
        if data["300"]["volume"][-1] == data["300"]["volume"][-2]:
            v = 0
        mv = (depth * v) / sum(data["300"]["volume"][-depth:])
        storage["m_volume"] = 1 if mv < 1 else 5 if mv > 5 else mv


def polynomial_regression():

    print("polynomial_regression()")
    # float_sma() returns stepwise due to 10m tick with 4h candle
    # in ma1 or ma2 live this wiggle can induce buy/sell/buy signal
    # state_machine() will use ma1poly and ma2poly data instead
    # this definition will gather plotted moving average data
    # then reprocess that data "smoothed" with X^2 regression
    # in effect removing candle aggregation artifacts
    # we'll also add some forward projections for visual purposes
    # sideways (green/red based on slope of linear)
    # linear regression
    # x^2 regression
    # prediction cone per difference between linear and X^2

    global storage
    ax = plt.gca()

    # on the first live tick we'll just use the float_sma()
    storage["ma1poly"] = storage["ma1"]
    storage["ma2poly"] = storage["ma2"]

    # all objects plotted by this definition
    # are removed and replotted anew every 5 minutes
    # except ma1poly_shadow and ma2poly_shadow which persist to 'now'
    labels = ["ma2poly", "ma1poly", "ma2linear", "ma1linear"]
    shadows = ["ma2poly_shadow", "ma1poly_shadow"]
    for line in ax.lines:
        if (str(line.get_label()) in labels) or (
            (line.get_xdata()[0] < time.time())
            and (str(line.get_label()) in shadows)
        ):
            line.remove()
            del line

    # remove fill_between type
    fills = ["ma1cone", "ma2cone", "ma1sideways", "ma2sideways"]
    for collection in ax.collections:
        if str(collection.get_label()) in fills:
            collection.remove()
            del collection

    # sideways and cone projects will be offset per market cross
    offset = MIN_CROSS
    if storage["bull_market"]:
        offset *= MAX_CROSS

    # create unix timestamps 24 hours into past and future: _x x_
    now = time.time()
    stop = now
    start = stop - 86400
    _x = np.linspace(start, stop, num=13)
    start = now
    stop = start + LIVE_PLOT_PROJECTION
    x_ = np.linspace(start, stop, num=13)

    # gather x and y coordinates for plots labeled ma1 and ma2
    ma1x = []
    ma1y = []
    ma2x = []
    ma2y = []
    for line in ax.lines:
        if str(line.get_label()) == "ma1":
            ma1x = ma1x + list(line.get_xdata())
            ma1y = ma1y + list(line.get_ydata())
        if str(line.get_label()) == "ma2":
            ma2x = ma2x + list(line.get_xdata())
            ma2y = ma2y + list(line.get_ydata())

    # linear regression of both ma1 and ma2
    # this will be used to plot cone of probability
    ma1linear = np.polyfit(ma1x, ma1y, 1)  # X^1 degree polynomial
    ma1linear_y_ = np.polyval(ma1linear, x_)  # projection
    ma1linear_y_ *= offset
    ma2linear = np.polyfit(ma2x, ma2y, 1)
    ma2linear_y_ = np.polyval(ma2linear, x_)

    # polynomial regression of latest 24 hours of ma1 and ma2 data
    # state_machine() will use "smoothed" ma1poly and ma2poly data
    # regression will also be plotted 24 hours into the future
    # tip of ma1poly and ma2poly prediction remains on the chart
    ma1poly = np.polyfit(ma1x, ma1y, 2)  # X^2 degree polynomial
    ma1poly_y = np.polyval(ma1poly, _x)  # regression
    ma1poly_y_ = np.polyval(ma1poly, x_)  # projection
    ma2poly = np.polyfit(ma2x, ma2y, 2)
    ma2poly_y = np.polyval(ma2poly, _x)
    ma2poly_y_ = np.polyval(ma2poly, x_)

    # CRITICAL:
    # post first tick we'll use poly regressions of moving averages
    # AFTER passing a COPY of ma1poly_y to storage,
    # we'll offset it for plotting the signal line projections
    if info["tick"] > 0:
        storage["ma1poly"] = np.array(ma1poly_y, copy=True)
        storage["ma2poly"] = np.array(ma2poly_y, copy=True)
    ma1poly_y *= offset
    ma1poly_y_ *= offset

    # offset the linear projections to begin at same point as poly
    ma1linear_y_ += ma1poly_y_[-13] - ma1linear_y_[-13]
    ma2linear_y_ += ma2poly_y_[-13] - ma2linear_y_[-13]

    # sideways projections will be colored based linear slope
    ma1sideways = np.ones(13) * ma1linear_y_[-13]
    ma2sideways = np.ones(13) * ma2linear_y_[-13]
    ma1color = "red"
    ma2color = "red"
    if ma1linear_y_[-1] > ma1linear_y_[-2]:
        ma1color = "lime"
    if ma2linear_y_[-1] > ma2linear_y_[-2]:
        ma2color = "lime"

    # calculate cone of probability for long average
    ma2cone2 = ma2linear_y_ - 0.5 * (ma2poly_y_ - ma2linear_y_)
    ma2cone1 = ma2linear_y_ + 4 * (ma2poly_y_ - ma2linear_y_)

    # calculate cone of probability for signal line
    ma1cone1 = ma1linear_y_ - 0.5 * (ma1poly_y_ - ma1linear_y_)
    ma1cone2 = ma1linear_y_ + 4 * (ma1poly_y_ - ma1linear_y_)

    # PLOT PROJECTIONS
    plt.pause(0.0001)
    # plot sideways
    plt.fill_between(
        x_,
        ma1sideways,
        ma1linear_y_,
        color=ma1color,
        label="ma1sideways",
        alpha=0.5,
    )
    plt.fill_between(
        x_,
        ma2sideways,
        ma2linear_y_,
        color=ma2color,
        label="ma2sideways",
        alpha=0.5,
    )

    # plot cone of probability
    plt.fill_between(
        x_,
        ma1cone1,
        ma1cone2,
        color="yellow",
        label="ma1cone",
        alpha=0.5,
    )
    plt.fill_between(
        x_,
        ma2cone1,
        ma2cone2,
        color="yellow",
        label="ma2cone",
        alpha=0.5,
    )

    # plot poly regressions
    plt.plot(
        _x,
        ma1poly_y,
        markersize=1,
        marker=".",
        color="cornsilk",
        label="ma1poly",
    )
    plt.plot(
        _x,
        ma2poly_y,
        markersize=1,
        marker=".",
        color="aqua",
        label="ma2poly",
    )
    # plot poly projections
    plt.plot(
        x_,
        ma1poly_y_,
        markersize=1,
        marker=".",
        color="cornsilk",
        label="ma1poly",
    )
    plt.plot(
        x_,
        ma2poly_y_,
        markersize=1,
        marker=".",
        color="aqua",
        label="ma2poly",
    )

    # plot magenta dot on tip of poly projection; leave on chart
    plt.plot(
        x_[-1],
        ma1poly_y_[-1],
        markersize=1,
        marker=".",
        color="magenta",
        label="ma1poly_shadow",
    )
    plt.plot(
        x_[-1],
        ma2poly_y_[-1],
        markersize=1,
        marker=".",
        color="magenta",
        label="ma2poly_shadow",
    )

    # plot linear projections
    plt.plot(
        x_,
        ma1linear_y_,
        markersize=1,
        marker=".",
        color="cornsilk",
        label="ma1linear",
    )
    plt.plot(
        x_,
        ma2linear_y_,
        markersize=1,
        marker=".",
        color="aqua",
        label="ma2linear",
    )


def state_machine():  # Alpha and beta market finite state

    # localize primary indicators
    ma1 = storage["ma1"][-1]
    ma2 = storage["ma2"][-1]
    if info["live"]:
        # when live use polynomial regressions for aggregate smoothing
        print("state_machine()")
        ma1 = storage["ma1poly"][-1]
        ma2 = storage["ma2poly"][-1]

    # require a width of MA1 to completely cross MA2
    min_cross = storage["min_cross"] = MIN_CROSS * ma1
    max_cross = storage["max_cross"] = MAX_CROSS * min_cross

    # set alpha market state per MA1 and MA2 crossing
    if storage["bull_market"] is False:
        if min_cross > ma2:
            storage["bull_market"] = True
    if storage["bull_market"] is True:
        if max_cross < ma2:
            storage["bull_market"] = False

    # final long average and signal line
    storage["long_average"] = ma2
    storage["signal_line"] = min_cross
    if storage["bull_market"]:
        storage["signal_line"] = max_cross

    # establish beta thresholds
    storage["selloff"] = ma1 * SELLOFF
    storage["support"] = ma1 * SUPPORT
    storage["despair"] = ma1 * DESPAIR
    storage["resistance"] = ma1 * RESISTANCE

    # adjust support & resistance stoploss near MA1/MA2 crossing
    storage["support"] = max(storage["support"], ma2 * BULL_STOP)
    storage["resistance"] = min(storage["resistance"], ma2 * BEAR_STOP)

    # adjust beta thresholds conservatively per GRAVITAS
    storage["selloff"] *= 1 - GRAVITAS
    storage["support"] *= 1 + GRAVITAS
    storage["despair"] *= 1 + GRAVITAS
    storage["resistance"] *= 1 - GRAVITAS

    # initialize backtest per BULL_MARKET
    if (info["live"] is False) and (info["tick"] == 0):
        close = storage["close"][-1]
        storage["selling"] = storage["buying"] = close
        storage["bull_market"] = BULL_MARKET
        if BULL_MARKET:
            if START_CURRENCY > 0:
                test_buy(close)
        else:
            if START_ASSETS > 0:
                test_sell(close)

    # set beta state
    # bull market => sell selloff & buy support
    # bear market => sell resistance & buy despair
    if storage["bull_market"]:
        storage["buying"] = storage["support"]
        storage["selling"] = storage["selloff"]
    else:
        storage["buying"] = storage["despair"]
        storage["selling"] = storage["resistance"]
    storage["mid_market"] = (storage["buying"] + storage["selling"]) / 2

    # calculate slope, concavity, and divergence
    # this section is for charting/printing ONLY
    # does not effect trade decisions
    if info["live"]:
        ma1 = storage["ma1poly"]
        ma2 = storage["ma2poly"]
        ma1_slope = storage["ma1_slope"] = ma1[-1] - ma1[-10]
        ma2_slope = storage["ma2_slope"] = ma2[-1] - ma2[-10]
        ma1_concavity = storage["ma1_concavity"] = (
            ma1[-1] - ma1[-5]
        ) - (ma1[-5] - ma1[-10])
        ma2_concavity = storage["ma2_concavity"] = (
            ma2[-1] - ma2[-5]
        ) - (ma2[-5] - ma2[-10])
        ma1_ = storage["ma1poly"][-10]
        ma2_ = storage["ma2poly"][-10]
        min_cross_ = MIN_CROSS * ma1_
        max_cross_ = MAX_CROSS * min_cross_
        signal = min_cross
        signal_ = min_cross_
        if storage["bull_market"]:
            signal = max_cross
            signal_ = max_cross_
        # current spread between ma2 and signal line
        mesh = abs(ma2[-1] - signal)
        # spread 24 hours ago
        mesh_ = abs(ma2_ - signal_)
        # approximate number of days till next crossing
        next_cross = mesh / (mesh_ - mesh)
        # when mesh is > mesh_ next cross will be negative
        if next_cross < 0:
            if storage["bull_market"]:
                next_cross = 777
            else:
                next_cross = 666
        # store to global space
        storage["mesh"] = mesh
        storage["next_cross"] = next_cross
        # on the first live tick we do not have scalp values
        # substitute buying and selling for initial plot labels
        storage["scalp_resistance"] = storage.get(
            "scalp_resistance", storage["selling"]
        )
        storage["scalp_support"] = storage.get(
            "scalp_support", storage["buying"]
        )
        # print next crossing insights
        ma2 = "%.8f" % ma2[-1]
        ma2_slope = "%.8f" % ma2_slope
        ma2_concavity = "%.8f" % ma2_concavity
        signal = "%.8f" % signal
        ma1_slope = "%.8f" % ma1_slope
        ma1_concavity = "%.8f" % ma1_concavity
        mesh = "%.8f" % mesh
        next_cross = "%.2f" % next_cross
        print("days to next crossing:", next_cross)
        print(
            "long average: ",
            ma2,
            "slope:",
            ma2_slope,
            "concavity:",
            ma2_concavity,
        )
        print(
            "signal line: ",
            signal,
            "slope:",
            ma1_slope,
            "concavity:",
            ma1_concavity,
        )
        print("divergence:   ", mesh)
        print("")


def sorceress_visendakona():

    raise ValueError("The World Is Not Yet Ready For Seidr")


# PRIMARY PROCESS
# ======================================================================

if __name__ == "__main__":

    data = {}
    race_write(doc="EV_log.txt", text=time.ctime())
    banner()
    logo()
    version()
    tune_install()
    select_mode()
    optimize = False
    control_panel()
    dictionaries()
    initialize()
    test_initialize()
    if (MODE in [2, 3, 6]) or BACKTEST:
        backtest()
    print_tune()
    if BACKTEST:
        while True:  # refresh backtest hourly
            for i in range(7200):
                plt.pause(0.5)
            logo()
            plt.close()
            data = {}
            control_panel()
            dictionaries()
            initialize()
            test_initialize()
            backtest()
            print_tune()

    if MODE in [2, 3, 6]:
        live()

    if OPTIMIZE:
        sorceress_visendakona()

# ======================================================================
""" EXTINCTION EVENT """
# ======================================================================
#
# THE DESTROYER,
# litepresence - 2019
#
