"""
Simple Moving Average Cross Strategy for bitshareQUANT Platform
litepresence 2019
************ ALPHA RELEASE TO PUBLIC DOMAIN WITH NO WARRANTY ***********
"""
import time
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

# litepresence/extinction-event utilities
from metaNODE import Bitshares_Trustless_Client
from bitsharesQUANT import log_in, cancel_all, test_stop, race_write
from bitsharesQUANT import place_order, fee_maintainer, watchdog
from bitsharesQUANT import plot_format
from bitsharesQUANT import float_period, trace, logo, test_plot
from bitsharesQUANT import slice_candles, announce_version, adjust_mode
from bitsharesQUANT import live_initialize, live_data, draw_live_chart
from bitsharesQUANT import holdings, set_timing, dictionaries
from bitsharesQUANT import zoom_to_data, test_rechart_orders, initialize
from bitsharesQUANT import hourly, daily, test_buy, test_sell, live_plot
from bitsharesQUANT import select_mode, print_tune, draw_test_chart
from bitsharesQUANT import test_initialize

# ======================================================================
VERSION = "Bitshares smaCROSS v0.00000002 pre-alpha"
# ======================================================================

# USER CONTROLS
# ======================================================================
def tune_install():
    """
    User input for data source and state machine tuning
    """
    tune = {}
    # ==================================================================
    # DATA SOURCE EXAMPLES
    # ==================================================================
    source = 6  # user input choose data source
    if source == 1:
        # bitshares RPC           smart contracts BACKTEST and LIVE
        tune["data_source"] = "DEX"
        tune["currency"] = "OPEN.BTC"
        tune["asset"] = "BTS"
    # ALL OTHER SOURCES ARE DAILY CANDLES, BACKTEST ONLY:
    if source == 2:
        # cryptocompare.com       crypto:crypto
        tune["data_source"] = "CEX"
        tune["currency"] = "BTC"
        tune["asset"] = "BTS"
    if source == 3:
        # alphavantage.com        fiat:fiat
        tune["data_source"] = "FOX"
        tune["currency"] = "USD"
        tune["asset"] = "CNY"
    if source == 4:
        # alphavantage.com        crypto:fiat
        tune["data_source"] = "CRY"
        tune["currency"] = "USD"
        tune["asset"] = "BTC"
    if source == 5:
        # alphavantage.com        USstocks:USD
        tune["data_source"] = "STX"
        tune["currency"] = "USD"
        tune["asset"] = "QURE"
    if source == 6:
        # Synthetic Data          Harmonic Brownian Walk
        tune["data_source"] = "SYN"
        tune["currency"] = "SYNTHETIC"
        tune["asset"] = "DATA"
    # ==================================================================
    # SIMPLE MOVING AVERAGE CROSS STATE MACHINE TUNE EXAMPLE
    # ==================================================================
    # ma1 is the raw signal line
    # ma2 is the long moving average
    # alpha signal of state machine is the moving average crossover
    tune["ma1"] = 10  # about 5 to 25 (min 3 for daily backtesting)
    tune["ma2"] = 50  # about 30 to 70 (max 75 for accurate live warmup)
    # min and max cross describe ma1 offset and thickness respectively
    # they are coeffs of ma1 (signal line) upon crossing ma2
    # the full thickness of the signal must pass through ma2
    # to switch alpha market state from bull to bear; vise versa
    tune["min_cross"] = 1  # about 0.9 to -1.1
    tune["max_cross"] = 1.05  # greater than 1, usually no more than 1.2
    # every strategy must specify pair and max indicator period + 1
    tune["max_period"] = 1 + int(max(tune["ma1"], tune["ma2"]))
    # the asset/currency pair is always specified like this:
    if tune["data_source"] == "DEX":
        tune["pair"] = tune["asset"] + ":" + tune["currency"]
    else:
        tune["pair"] = "%s_%s" % (tune["currency"], tune["asset"])
    return tune


def scalp_tune_install():
    """
    User settings for scalp operations
    """
    scalp_tune = {}
    return scalp_tune


def control_panel():
    """
    User input for backtest and live session parameters
    """
    control = {}
    # ==================================================================
    # BACKTEST
    # ==================================================================
    control["days"] = 720  # backtest depth in days
    control["end"] = "2100-01-01"  # "YYYY-MM-DD"; set '2100-01-01' for latest
    control["start_assets"] = 0  # backtest initial asset holdings
    control["start_currency"] = 1  # backtest initial currency holdings
    control["bull_market"] = True  # initial backtest market state (True is "BULL")
    # ==================================================================
    # LIVE
    # ==================================================================
    # live tick size in seconds
    control["tick"] = 600
    control["tick_timing"] = 51  # number of seconds past the minute to tick
    control["tick_minimum"] = 300  # must be less than tick
    control["warmup"] = 90  # depth of backtest prior to live session
    # max percent may invest in:
    # 100 = "all in" ; 10 = "10 percent in"
    # to let bot do its thing with full bank use 100, 100
    control["max_assets"] = 100
    control["max_currency"] = 100
    # minimum order size in asset terms
    control["min_amount"] = 10
    return control


# LIVE
# ======================================================================


def live(mode, control, storage, tune):
    """
    Primary live event loop
    """
    logo()
    print(VERSION)
    storage, portfolio, info, data, edicts = live_initialize(mode, control, storage)
    previous_order_value = 0
    attempt = 0
    msg = ""
    while True:
        plt.pause(1)  # prevent inadvertent attack on API's
        if info["tick"] > 0:
            set_timing(control, info)
        info["current_time"] = now = int(time.time())
        print("")
        print("%s %s" % (tune["pair"], time.ctime()))
        print("")
        # DEBUG mode['live'] SESSION
        debug = 0
        if debug:
            print("$$$$$$$$$$$$$$$$$$")
            print("WARN: DEBUG - RUNTIME: %s" % (info["current_time"] - info["begin"]))
            print("$$$$$$$$$$$$$$$$$$")
            print("")
            print("WATCHDOG LATENCY:", watchdog())
            portfolio, data, storage = live_data(tune, storage, portfolio, data)
            storage, portfolio = indicators(data, tune, storage, portfolio, mode, info)
            polynomial_regression(storage, tune, info)
            state_machine(storage, info, tune, control, portfolio, mode)
            hourly(info)
            daily(storage, info)
            cancel_all(mode)
            edicts = []
            storage, scalp_edicts = scalp(storage)
            edicts += scalp_edicts
            storage, trade_edicts = trade(storage, mode, portfolio, info, tune, control)
            place_order(edicts, mode)
            draw_live_state(info, data, tune, storage, mode)
            draw_live_chart(info, data, storage)
            plot_format(info, storage)
            live_plot(info)
            draw_text(storage, info, mode, tune)
            plt.pause(10)
            info["tick"] += 1
        else:
            try:
                plt.pause(0.05)
                print("")
                print("RUNTIME: %s" % (info["current_time"] - info["begin"]))
                print("")
                print("WATCHDOG LATENCY:", watchdog())
                print("")
                # RAISE ALARM
                if attempt > 2:
                    time_msg = datetime.fromtimestamp(now).strftime("%H:%M")
                    print(("%s FAIL @@@@@@@ ATTEMPT: %s %s" % (msg, attempt, time_msg)))
                # GATHER AND POST PROCESS DATA
                start = time.time()
                print("elapsed: %.3f" % (time.time() - start))
                start = time.time()
                try:
                    plt.pause(0.05)
                    portfolio, data, storage = live_data(tune, storage, portfolio, data)
                    print("live_data()", data.keys())
                except Exception as error:
                    msg += trace(error) + "live_data() "
                    attempt += 1
                    continue
                print("elapsed: %.3f" % (time.time() - start))
                start = time.time()
                try:
                    plt.pause(0.05)
                    storage, portfolio = indicators(
                        data, tune, storage, portfolio, mode, info
                    )
                    print("indicators()", data.keys())
                except Exception as error:
                    msg += trace(error) + "indicators() "
                    attempt += 1
                    continue
                print("elapsed: %.3f" % (time.time() - start))
                start = time.time()
                try:
                    plt.pause(0.05)
                    polynomial_regression(storage, tune, info)
                except Exception as error:
                    msg += trace(error) + "polynomial_regression() "
                    attempt += 1
                    continue
                print("elapsed: %.3f" % (time.time() - start))
                start = time.time()
                try:
                    plt.pause(0.05)
                    state_machine(storage, info, tune, control, portfolio, mode)
                except Exception as error:
                    msg += trace(error) + "state_machine() "
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
                        hourly(info)
                        info["hour"] += 1
                    except Exception as error:
                        msg += trace(error) + "hourly() "
                        attempt += 1
                        continue
                print("elapsed: %.3f" % (time.time() - start))
                start = time.time()
                check_day = runtime / 86400.0
                if check_day > info["day"]:
                    try:
                        daily(storage, info)
                        info["day"] += 1
                    except Exception as error:
                        msg += trace(error) + "daily() "
                        attempt += 1
                        continue
                print("elapsed: %.3f" % (time.time() - start))
                start = time.time()
                metaNODE = Bitshares_Trustless_Client()
                order_value = metaNODE["sell_orders"] + metaNODE["buy_orders"]
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
                        cancel_all(mode)
                        plt.pause(3)  # allow acct balance to update
                    print("elapsed: %.3f" % (time.time() - start))
                    start = time.time()
                    # MAINTAIN 1 BITSHARE FOR FEES
                    plt.pause(0.05)
                    try:
                        fee_maintainer(mode)
                    except Exception as error:
                        msg += trace(error) + "fee_maintainer() "
                        attempt += 1
                        continue
                    print("elapsed: %.3f" % (time.time() - start))
                    start = time.time()
                edicts = []  # reset edict list prior to scalp/trade ops
                # SCALP OPS
                plt.pause(0.01)
                try:
                    storage, scalp_edicts = scalp(storage)
                    edicts += scalp_edicts
                except Exception as error:
                    msg += trace(error) + "scalp() "
                    attempt += 1
                    continue
                print("elapsed: %.3f" % (time.time() - start))
                start = time.time()
                # TRADE OPS
                plt.pause(0.01)
                try:
                    storage, trade_edicts = trade(
                        storage, mode, portfolio, info, tune, control
                    )
                    edicts += trade_edicts
                except Exception as error:
                    msg += trace(error) + "trade() "
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
                    place_order(edicts, mode)
                    print("elapsed: %.3f" % (time.time() - start))
                    start = time.time()
                plt.pause(5)
                metaNODE = Bitshares_Trustless_Client()
                previous_order_value = metaNODE["sell_orders"] + metaNODE["buy_orders"]
                del metaNODE
                # PLOT
                try:
                    draw_live_state(info, data, tune, storage, mode)
                    draw_live_chart(info, data, storage)
                except Exception as error:
                    msg += trace(error) + "live_chart() "
                    attempt += 1
                    continue
                print("elapsed: %.3f" % (time.time() - start))
                start = time.time()
                try:
                    plot_format(info, storage)
                except Exception as error:
                    msg += trace(error) + "plot_format() "
                    attempt += 1
                    continue
                print("elapsed: %.3f" % (time.time() - start))
                start = time.time()
                try:
                    live_plot(info)
                    draw_text(storage, info, mode, tune)
                except Exception as error:
                    msg += trace(error) + "live_plot() + draw_text() "
                    attempt += 1
                    continue
                print("elapsed: %.3f" % (time.time() - start))
                start = time.time()
                # mode['end'] PRIMARY control['tick']
                plt.pause(0.05)
                msg = ""
                print("tick", info["tick"])
                info["tick"] += 1
                attempt = 0
            except Exception as error:
                trace(error)
                continue


def scalp(storage):
    """
    Scalping Strategy and Execution
    """
    # localize data
    now = int(time.time())
    metaNODE = Bitshares_Trustless_Client()
    currency = metaNODE["currency_balance"]
    assets = metaNODE["asset_balance"]
    last = metaNODE["last"]
    max_currency = metaNODE["currency_max"]
    max_assets = metaNODE["asset_max"]
    invested = metaNODE["invested"]
    divested = metaNODE["divested"]
    nodes = metaNODE["whitelist"]
    book = metaNODE["book"]
    del metaNODE
    # extract orderbook
    ask_p = book["askp"][0]
    ask_v = book["askv"][0]
    bid_p = book["bidp"][0]
    bid_v = book["bidv"][0]
    ask_p2 = book["askp"][1]
    bid_p2 = book["bidp"][1]
    # high low and primary market state from storage
    bull_market = storage["bull_market"]
    high = storage["high"]
    low = storage["low"]
    # given the above objects (or more that you create)
    # your scalping strategy goes here:
    edicts = []
    # if condition:
    #     edict = {
    #         'op':'buy',
    #         'amount':1.0,
    #         'price':150.5,
    #         'expiration:0
    #     }
    #     edicts.append(edict)
    return storage, edicts


def trade(storage, mode, portfolio, info, tune, control):
    """
    Primary Order Execution
    """
    # localize storage data
    buying = storage["buying"]
    selling = storage["selling"]
    edicts = []
    if info["live"]:  # localize additional data for live session
        # load metaNODE data
        metaNODE = Bitshares_Trustless_Client()
        currency = metaNODE["currency_balance"]
        assets = metaNODE["asset_balance"]
        last = metaNODE["last"]
        book = metaNODE["book"]
        ask_p = book["askp"][0]
        bid_p = book["bidp"][0]
        invested = metaNODE["invested"]
        divested = metaNODE["divested"]
        max_assets = metaNODE["asset_max"]
        del metaNODE
        # localize stored indicators
        high = storage["high"]
        low = storage["low"]
        # plot zoom in to trade decision
        mesh_max = max(storage["long_average"], storage["signal_line"])
        mesh_min = min(storage["long_average"], storage["signal_line"])
        now = time.time()
        past = now - 86400
        future = now + 86400
        axis = plt.gca()
        axis.set_ylim([0.93 * mesh_min, 1.07 * mesh_max])
        axis.set_xlim([past, future])
        draw_text(storage, info, mode, tune)
        plt.pause(0.01)
        print(("assets %.1f, max assets %.1f" % (assets, max_assets)))
        pieces = 10.0  # order size
        # this is the trigger to the live state machine
        if high > selling:
            storage["holding"] = False
        if low < buying:
            storage["holding"] = True
        # primary order placement routine
        qty = max_assets / pieces
        if last > 0.90 * selling:
            print("")
            print("APPROACHING SELL POINT")
            if assets > 0.1:
                if divested < mode["max_currency"]:
                    selling_r = max(selling, (last + ask_p) / 2)
                    try:
                        if qty > control["min_amount"]:
                            # iceberg
                            print(
                                (
                                    "SELLING",
                                    tune["pair"],
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
                else:
                    print("MAX DIVESTED")
            else:
                print("NO ASSETS")
        qty = max_assets / pieces
        if last < 1.20 * buying:
            print("")
            print("APPROACHING BUY POINT")
            if currency > 0.1:
                if invested < mode["max_assets"]:
                    buying_r = min(buying, (last + bid_p) / 2)
                    try:
                        if qty > control["min_amount"]:
                            print(
                                (
                                    "BUYING",
                                    tune["pair"],
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
                else:
                    print("MAX INVESTED")
            else:
                print("NO CURRENCY")
        zoom_to_data()
        draw_text(storage, info, mode, tune)

    else:
        order = {}
        # test trade
        if portfolio["currency"] > 0:
            if storage["low"][-1] < buying:
                buying_r = min(storage["high"][-1], buying)
                order["call"] = "BUY"
                order["price"] = buying
                test_buy(order, portfolio, storage, info, tune, mode)
        elif portfolio["assets"] > 0:
            if storage["high"][-1] > selling:
                selling_r = max(storage["low"][-1], selling)
                order["call"] = "SELL"
                order["price"] = selling
                test_sell(order, portfolio, storage, info, tune, mode)
    # we can keep track of the ratio of ticks invested/divested
    if storage["holding"]:
        storage["holding_ticks"] += 1
    return storage, edicts


# BACKTEST
# ======================================================================


def backtest(storage, info, data, portfolio, mode, tune, control):
    """
    Primary backtest event loop; the "cost function"
    """
    storage["days"] = int(
        len(data["unix"]) / float(86400 / mode["candle"])
        - max(tune["ma1"], tune["ma2"])
        - 1
    )
    info["current_time"] = info["begin"]
    info["end"] = max(data["unix"])
    while True:
        if info["current_time"] < info["end"]:
            try:
                data_slice = slice_candles(
                    info["current_time"], data, mode["candle"], mode["depth"]
                )
                storage["high"] = data_slice["high"]
                storage["low"] = data_slice["low"]
                storage["open"] = data_slice["open"]
                storage["close"] = data_slice["close"]
                storage, info = holdings(storage, info, data, portfolio)
                storage, portfolio = indicators(
                    data, tune, storage, portfolio, mode, info
                )
                state_machine(storage, info, tune, control, portfolio, mode)
                trade(storage, mode, portfolio, info, tune, control)
                if mode["live"] or mode["backtest"]:
                    draw_test_state(mode, info, storage)
                    draw_test_chart(info, storage)
                    if info["tick"] % 100 == 0:
                        if not mode["optimize"]:
                            pass
            except Exception as error:
                print(
                    "WARN: backtest data unavailable",
                    time.ctime(info["current_time"]),
                    trace(error),
                )
            info["current_time"] += mode["candle"]
            info["tick"] += 1
            if mode["live"] and (info["tick"] % 50 == 0):
                draw_text(storage, info, mode, tune)
                plt.pause(0.0001)
        else:
            if mode["live"] or mode["backtest"]:
                test_stop(storage, portfolio, info, data, tune)
                test_rechart_orders(storage)
                test_plot(info, mode)
                draw_text(storage, info, mode, tune)
                if mode["backtest"]:
                    try:
                        plt.autoscale(enable=True, axis="y")
                    except:
                        print("autoscale failed")
                    plt.ioff()
                try:
                    plot_format(info, storage)
                except:
                    pass
                plt.pause(0.0001)
            break
    return storage, info


# PLOT
# ======================================================================
def draw_test_state(mode, info, storage):
    """
    Add objects to backtest chart
    """
    try:
        state = {}
        state["now"] = info["current_time"]
        state["ma1"] = state["ma1poly"] = storage["ma1"][-1]
        state["ma2"] = state["ma2poly"] = storage["ma2"][-1]
        if info["live"]:
            state["ma1poly"] = storage["ma1poly"][-1]
            state["ma2poly"] = storage["ma2poly"][-1]
        state["max_cross"] = storage["max_cross"]
        state["min_cross"] = storage["min_cross"]
        state["buying"] = storage["buying"]
        state["selling"] = storage["selling"]
        draw_state_machine(state, mode, info, storage)
    except Exception as error:
        print(error.args)


def draw_live_state_zero(info, data, tune, storage, mode):
    """
    initializes last 24 hours of indicator state machine
    """
    now = info["current_time"]
    ma1_period = tune["ma1"] * 86400 / 14400.0
    ma2_period = tune["ma2"] * 86400 / 14400.0
    ma1_arr = float_period(data["14400"]["close"], ma1_period)
    ma2_arr = float_period(data["14400"]["close"], ma2_period)
    unix = data["14400"]["unix"]
    for item in range(-1, -10, -1):
        for offset in range(0, 14400, 600):
            try:
                state = {}
                state["now"] = unix[item] + offset
                state["ma1"] = state["ma1poly"] = ma1_arr[item]
                state["ma2"] = state["ma2poly"] = ma2_arr[item]
                state["min_cross"] = tune["min_cross"] * state["ma1"]
                state["max_cross"] = tune["max_cross"] * state["min_cross"]
                state["buying"] = state["max_cross"]
                state["selling"] = state["min_cross"]
                draw_state_machine(state, mode, info, storage)
            except Exception as error:
                print(trace(error))


def draw_live_state(info, data, tune, storage, mode):
    """
    appends real time indicator state machine to chart
    """
    if info["tick"] == 0:
        draw_live_state_zero(info, data, tune, storage, mode)
    # localize low frequency indicators
    state = {}
    state["now"] = info["current_time"]
    state["ma1"] = storage["ma1"][-1]
    state["ma2"] = storage["ma2"][-1]
    state["ma1poly"] = storage["ma1poly"][-1]
    state["ma2poly"] = storage["ma2poly"][-1]
    state["buying"] = storage["buying"]
    state["selling"] = storage["selling"]
    state["max_cross"] = storage["max_cross"]
    state["min_cross"] = storage["min_cross"]
    # plot state machine
    draw_state_machine(state, mode, info, storage)


def draw_state_machine(state, mode, info, storage):
    """
    Plots primary trade indications
    """
    # localize indicators
    now = state["now"]
    ma1 = state["ma1"]
    ma2 = state["ma2"]
    ma2poly = state["ma2poly"]
    buying = state["buying"]
    selling = state["selling"]
    max_cross = state["max_cross"]
    min_cross = state["min_cross"]
    # set state machine line size in backtest and live modes
    markersize_1 = 0.5
    markersize_2 = 3
    markersize_3 = 3
    if mode["live"] or mode["paper"]:
        markersize_1 = 1
        markersize_2 = 4
        markersize_3 = 8
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
        markersize=markersize_3,
        marker=".",
        color="aqua",
        label="long",
    )
    # plot width of signal line
    if storage["bull_market"]:
        plt.plot(
            now,
            max_cross,
            markersize=markersize_2,
            marker=".",
            color="cornsilk",
            label="max_cross",
        )
        plt.plot(
            now,
            min_cross,
            markersize=markersize_1,
            marker=".",
            color="cornsilk",
            label="min_cross",
        )
    else:
        plt.plot(
            now,
            max_cross,
            markersize=markersize_1,
            marker=".",
            color="cornsilk",
            label="max_cross",
        )
        plt.plot(
            now,
            min_cross,
            markersize=markersize_2,
            marker=".",
            color="cornsilk",
            label="min_cross",
        )
    # shade between signal lines
    plt.plot(
        (now, now), (max_cross, min_cross), color="cornsilk", label="cross", alpha=0.15
    )
    # plot buying and selling to display market state
    if storage["bull_market"]:
        plt.plot(now, buying, color="lime")
    else:
        plt.plot(now, selling, color="tomato")


def draw_text(storage, info, mode, tune):
    """
    Display dynamic text regarding current market conditions
    """
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

    def scale(axis, alpha):
        """
        Text placement per plot boundaries
        """
        if axis == "x":
            locus = alpha * (pltxlim1 - pltxlim0) + pltxlim0
        elif axis == "y":
            locus = alpha * (pltylim1 - pltylim0) + pltylim0
        return locus

    # BITSHARES EXTINCTION EVENT in aqua
    textx = scale("x", 0.1)
    texty = scale("y", 0.75)
    storage["text"].append(
        plt.text(
            textx,
            texty,
            "BitSharesQUANT",
            color="aqua",
            alpha=0.3,
            size=35,
            weight="extra bold",
        )
    )
    textx = scale("x", 0.1)
    texty = scale("y", 0.7)
    storage["text"].append(
        plt.text(
            textx,
            texty,
            "SIMPLE MOVING AVERAGE CROSS",
            color="aqua",
            alpha=0.3,
            size=18,
            weight="extra bold",
        )
    )
    # market tune['pair'], LAST price, and mode['id'] in dark orange
    textx = scale("x", 0.75)
    texty = scale("y", 0.75)
    pair = tune["pair"]
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
    if mode["id"] == 1:
        text = "mode['backtest']"
    if mode["id"] == 2:
        text = "mode['paper']"
    if mode["id"] == 3:
        text = "mode['live']"
    if mode["id"] == 4:
        text = "mode['sales']"
    if mode["id"] == 6:
        text = "TEST ORDERS"
    if mode["id"] in [2, 3, 6]:
        if not info["live"]:
            text = "INITIALIZING"
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
        # magenta triangle marker for last price on far right
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
    y_value = 0.95
    texty = scale("y", y_value)
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
    if info["live"]:
        y_value *= 0.97
        texty = scale("y", y_value)
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
        y_value *= 0.97
        texty = scale("y", y_value)
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
        y_value *= 0.97
        texty = scale("y", y_value)
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
        y_value *= 0.97
        texty = scale("y", y_value)
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
    y_value *= 0.97
    texty = scale("y", y_value)
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
    y_value *= 0.97
    texty = scale("y", y_value)
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
    return storage


# DATA
# ======================================================================
def indicators(data, tune, storage, portfolio, mode, info):
    """
    Post process data with technical indicators
    """
    ma1_period = tune["ma1"] * 86400.0 / mode["candle"]
    ma2_period = tune["ma2"] * 86400.0 / mode["candle"]
    if not info["live"]:
        # alpha moving averages
        storage["ma1"] = float_period(storage["close"], ma1_period)
        storage["ma2"] = float_period(storage["close"], ma2_period)
    if info["live"]:
        print("indicators()")
        # alpha moving averages
        storage["ma1"] = float_period(data["14400"]["close"], ma1_period)
        storage["ma2"] = float_period(data["14400"]["close"], ma2_period)
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
        portfolio["percent_divested"] = 100 - portfolio["percent_invested"]
        # recent volume ratio for plotting marker size
        depth = 100
        volume = data["300"]["volume"][-1]
        if data["300"]["volume"][-1] == data["300"]["volume"][-2]:
            volume = 0
        m_v = (depth * volume) / sum(data["300"]["volume"][-depth:])
        storage["m_volume"] = 1 if m_v < 1 else 5 if m_v > 5 else m_v
    return storage, portfolio


def polynomial_regression(storage, tune, info):
    """
    Live aggregated indicator smoothing
    """
    print("polynomial_regression()")
    # live indictors return stepwise due to 10m tick with 4h candle
    # in ma1 or ma2 live this wiggle can induce buy/sell/buy signal
    # state_machine() will use ma1poly and ma2poly data instead
    # this definition will gather plotted moving average data
    # then reprocess that data "smoothed" with regression
    # in effect removing candle aggregation artifacts
    # we'll also add some forward projections for visual purposes
    # - sideways (green/red based on slope of linear)
    # - linear regression
    # - x^2 regression
    # - prediction cone per difference between linear and X^2
    axis = plt.gca()
    # on the first live tick we'll just use the float_period()
    storage["ma1poly"] = storage["ma1"]
    storage["ma2poly"] = storage["ma2"]
    # all objects plotted by this definition
    # are removed and replotted anew every 5 minutes
    # except ma1poly_shadow and ma2poly_shadow which persist to 'now'
    labels = ["ma2poly", "ma1poly", "ma2linear", "ma1linear"]
    shadows = ["ma2poly_shadow", "ma1poly_shadow"]
    for line in axis.lines:
        if (str(line.get_label()) in labels) or (
            (line.get_xdata()[0] < time.time()) and (str(line.get_label()) in shadows)
        ):
            line.remove()
            del line
    # remove fill_between type
    fills = ["ma1cone", "ma2cone", "ma1sideways", "ma2sideways"]
    for collection in axis.collections:
        if str(collection.get_label()) in fills:
            collection.remove()
            del collection
    # sideways and cone projects will be offset per market cross
    offset = tune["min_cross"]
    if storage["bull_market"]:
        offset *= tune["max_cross"]
    # create unix timestamps 24 hours into past and future: last_24h next_24h
    now = time.time()
    stop = now
    start = stop - 86400
    last_24h = np.linspace(start, stop, num=13)
    start = now
    stop = start + 86400
    next_24h = np.linspace(start, stop, num=13)
    # gather x and y coordinates for plots labeled ma1 and ma2
    ma1x = []
    ma1y = []
    ma2x = []
    ma2y = []
    for line in axis.lines:
        if str(line.get_label()) == "ma1":
            ma1x = ma1x + list(line.get_xdata())
            ma1y = ma1y + list(line.get_ydata())
        if str(line.get_label()) == "ma2":
            ma2x = ma2x + list(line.get_xdata())
            ma2y = ma2y + list(line.get_ydata())
    # linear regression of both ma1 and ma2
    # this will be used to plot cone of probability
    ma1linear = np.polyfit(ma1x, ma1y, 1)  # X^1 degree polynomial
    ma1linear_y_ = np.polyval(ma1linear, next_24h)  # projection
    ma1linear_y_ *= offset
    ma2linear = np.polyfit(ma2x, ma2y, 1)
    ma2linear_y_ = np.polyval(ma2linear, next_24h)
    # polynomial regression of latest 24 hours of ma1 and ma2 data
    # state_machine(s) will use "smoothed" ma1poly and ma2poly data
    # regression will also be plotted 24 hours into the future
    # tip of ma1poly and ma2poly prediction remains on the chart
    ma1poly = np.polyfit(ma1x, ma1y, 2)  # X^2 degree polynomial
    ma1poly_y = np.polyval(ma1poly, last_24h)  # regression
    ma1poly_y_ = np.polyval(ma1poly, next_24h)  # projection
    ma2poly = np.polyfit(ma2x, ma2y, 2)
    ma2poly_y = np.polyval(ma2poly, last_24h)
    ma2poly_y_ = np.polyval(ma2poly, next_24h)
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
        next_24h,
        ma1sideways,
        ma1linear_y_,
        color=ma1color,
        label="ma1sideways",
        alpha=0.5,
    )
    plt.fill_between(
        next_24h,
        ma2sideways,
        ma2linear_y_,
        color=ma2color,
        label="ma2sideways",
        alpha=0.5,
    )
    # plot cone of probability
    plt.fill_between(
        next_24h, ma1cone1, ma1cone2, color="yellow", label="ma1cone", alpha=0.5
    )
    plt.fill_between(
        next_24h, ma2cone1, ma2cone2, color="yellow", label="ma2cone", alpha=0.5
    )
    # plot poly regressions
    plt.plot(
        last_24h, ma1poly_y, markersize=1, marker=".", color="cornsilk", label="ma1poly"
    )
    plt.plot(
        last_24h, ma2poly_y, markersize=1, marker=".", color="aqua", label="ma2poly"
    )
    # plot poly projections
    plt.plot(
        next_24h,
        ma1poly_y_,
        markersize=1,
        marker=".",
        color="cornsilk",
        label="ma1poly",
    )
    plt.plot(
        next_24h, ma2poly_y_, markersize=1, marker=".", color="aqua", label="ma2poly"
    )
    # plot magenta dot on tip of poly projection; leave on chart
    plt.plot(
        next_24h[-1],
        ma1poly_y_[-1],
        markersize=1,
        marker=".",
        color="magenta",
        label="ma1poly_shadow",
    )
    plt.plot(
        next_24h[-1],
        ma2poly_y_[-1],
        markersize=1,
        marker=".",
        color="magenta",
        label="ma2poly_shadow",
    )
    # plot linear projections
    plt.plot(
        next_24h,
        ma1linear_y_,
        markersize=1,
        marker=".",
        color="cornsilk",
        label="ma1linear",
    )
    plt.plot(
        next_24h,
        ma2linear_y_,
        markersize=1,
        marker=".",
        color="aqua",
        label="ma2linear",
    )
    return storage


def state_machine(storage, info, tune, control, portfolio, mode):
    """
    Finite State Machine Primary Logic Tree
    """
    # localize primary indicators
    ma1 = storage["ma1"][-1]
    ma2 = storage["ma2"][-1]
    if info["live"]:
        # when live use polynomial regressions for aggregate smoothing
        print("state_machine()")
        ma1 = storage["ma1poly"][-1]
        ma2 = storage["ma2poly"][-1]
    # require a width of tune['ma1'] to completely cross tune['ma2']
    min_cross = storage["min_cross"] = tune["min_cross"] * ma1
    max_cross = storage["max_cross"] = tune["max_cross"] * min_cross
    # set alpha market state per tune['ma1'] and tune['ma2'] crossing
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
    # initialize backtest per control['bull_market']
    order = {}
    if (info["live"] is False) and (info["tick"] == 0):
        close = storage["close"][-1]
        storage["selling"] = storage["buying"] = order["price"] = close
        storage["bull_market"] = control["bull_market"]
        if control["bull_market"]:
            if control["start_currency"] > 0:
                order["call"] = "BUY"
                test_buy(order, portfolio, storage, info, tune, mode)
        else:
            if control["start_assets"] > 0:
                order["call"] = "SELL"
                test_sell(order, portfolio, storage, info, tune, mode)
    # set beta state
    # bull market => buy ma1
    # bear market => sell ma1
    if storage["bull_market"]:
        storage["buying"] = ma1
        storage["selling"] = 10 ** 10
    else:
        storage["buying"] = 0
        storage["selling"] = ma1


def optimizer():
    """
    Please support my worker
    """
    raise ValueError("litepresence needs funding")


# PRIMARY PROCESS
# ======================================================================
def main():
    """
    Primary process handler
    """
    race_write(doc="EV_log.txt", text=time.ctime())
    logo()
    announce_version(VERSION)
    tune = tune_install()
    mode = select_mode(tune)
    mode = log_in(mode)
    info, storage, portfolio = dictionaries()
    control = control_panel()
    mode = adjust_mode(tune, mode, control)
    initialize(tune, mode, storage, control)
    storage, portfolio, info, data = test_initialize(
        tune, mode, storage, control, info, portfolio
    )
    if (mode["id"] in [2, 3, 6]) or mode["backtest"]:
        backtest(storage, info, data, portfolio, mode, tune, control)
    print_tune(tune, storage)
    if mode["id"] in [2, 3, 6]:
        live(mode, control, storage, tune)
    elif mode["optimize"]:
        optimizer()
    else:
        plt.show()


if __name__ == "__main__":
    main()
# ======================================================================
# EXTINCTION EVENT
# ======================================================================
#
# THE DESTROYER,
# litepresence - 2019
#
