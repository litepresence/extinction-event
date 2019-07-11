"""
4 State Moving Average Cross Strategy for bitshareQUANT Platform
litepresence 2019
************ ALPHA RELEASE TO PUBLIC DOMAIN WITH NO WARRANTY ***********
"""
import time
from random import random, randint
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
from bitsharesQUANT import test_initialize, satoshi_str


# ======================================================================
VERSION = "Bitshares extinctionEVENT v0.00000017"
# ======================================================================
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
    - scalp_tune['enable'] ops updated every 10 minutes
    - Bot runs local
    - Backtest Engine included for optimizing thresholds
    - Maintains storage from backtest to live session
    h/t @ cryptocompare.com nomics.com and alphavantage.com for data
    h/t to crew at BitsharesDEV telegram
    """


# USER CONTROLS
# ======================================================================
def tune_install():
    """
    User input for data source and state machine tuning
    """
    tune = {}
    # ==================================================================
    "DATA source EXAMPLE"
    # ==================================================================
    source = 1  # choose data source
    if source == 1:
        # bitshares dex           smart contracts (backtest and mode['live'])
        tune["data_source"] = "DEX"
        tune["currency"] = "OPEN.BTC"
        tune["asset"] = "BTS"
    if source == 2:
        # cryptocompare.com       crypto:crypto (backtesting only)
        tune["data_source"] = "CEX"
        tune["currency"] = "BTC"
        tune["asset"] = "BTS"
    if source == 3:
        # alphavantage.com        fiat:fiat (backtesting only)
        tune["data_source"] = "FOX"
        tune["currency"] = "USD"
        tune["asset"] = "CNY"
    if source == 4:
        # alphavantage.com        crypto:fiat (backtesting only)
        tune["data_source"] = "CRY"
        tune["currency"] = "USD"
        tune["asset"] = "BTC"
    if source == 5:
        # alphavantage.com        USstocks:USD (backtesting only)
        tune["data_source"] = "STX"
        tune["currency"] = "USD"
        tune["asset"] = "QURE"
    if source == 6:
        tune["data_source"] = "SYN"
        tune["currency"] = "SYNTHETIC"
        tune["asset"] = "DATA"
    # ==================================================================
    "EXTINCTION EVENT STATE MACHINE TUNE EXAMPLE"
    # ==================================================================
    # ma1 is the raw signal line
    # ma2 is the long moving average
    # alpha signal of state machine is the moving average crossover
    tune["ma1"] = 10  # about 5 to 25 (min 3 for daily backtesting)
    tune["ma2"] = 50  # about 30 to 70 (max 75 for live warmup)
    # min and max cross describe ma1 offset and thickness respectively
    # they are coeffs of ma1 (signal line) upon crossing ma2
    # the full thickness of the signal must pass through ma2
    # to switch alpha market state from bull to bear; vise versa
    tune["min_cross"] = 1  # about 0.9 to -1.1
    tune["max_cross"] = 1.05  # greater than 1, usually no more than 1.2
    # bull and bear stop are offsets of ma2
    # they increase aggressiveness of support/resistance
    # usually only near the moving average crossover
    # support is max(signal, ma2*bullstop)
    # resistance is min(signal, ma2*bearstop)
    tune["bull_stop"] = 1  # about 0.9 to -1.1
    tune["bear_stop"] = 1  # about 0.9 to -1.1
    # selloff and support are bull market coeffs of ma1
    # resistance and despair are bear market coeffs of ma1
    # these create the outer buy/sell boundaries of active market
    # the bull market is shaded green; the bear market red
    # the inactive "extinct" market is plotted in purple
    tune["selloff"] = 1.5  # about 1.5 - 2.5
    tune["support"] = 1.1  # about 0.8 - 1.2
    tune["resistance"] = 0.9  # about 0.8 - 1.2
    tune["despair"] = 0.7  # about 0.6 - 0.8
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
    # though an algorithm is "perfectly tuned" to old data
    # inadequate volume at extremes can occur in the more mature market
    # override tune_install() thresholds conservatively by 0.01 = 1%
    # applies to despair, resistance, support, selloff
    tune["gravitas"] = 0.00  # use 0.00 for backtesting
    # 0.00-0.05 for final testing and when live
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
    # wanna see something pretty cool?
    # run a 1000 day backtest on this:
    """
    tune['data_source'] = "CEX"
    tune['currency'] = "BTC"
    tune['asset'] = "EMC2"
    tune['ma1'] = 6.034
    tune['ma2'] = 17.002
    tune['selloff'] = 1.9214
    tune['support'] = 0.9861
    tune['resistance'] = 1.0159
    tune['despair'] = 0.8363
    tune['min_cross'] = 0.9522
    tune['max_cross'] = 1.0301
    tune['bull_stop'] = 1.0127
    tune['bear_stop'] = 1.0122
    """

    # every strategy must specify pair and max indicator period
    tune["max_period"] = 1 + int(max(tune["ma1"], tune["ma2"]))
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
    scalp_tune["enable"] = True  # False to disable scalping
    # scalp_tune['enable'] thresholds
    scalp_tune["pieces"] = 2  # number of pieces to break up scalp_tune['enable'] orders
    scalp_tune["fund"] = 0.5  # 0.10 = 10% of holdings reserved for scalping
    scalp_tune[
        "quantity"
    ] = 0.5  # 0.10 = 10% of scalp_tune['enable'] fund on books per tick
    scalp_tune[
        "zone"
    ] = 0.8  # 0.80 = scalp_tune['enable'] middle 80% of market only; max 1
    scalp_tune["margin"] = 0.007  # about 0.005 - 0.015
    # scalp_tune['enable'] "center" moving average mesh period in days
    scalp_tune["ma3"] = 0.200  # about 0.200 to 0.600
    scalp_tune["ma4"] = 0.066  # about 0.166
    return scalp_tune


def control_panel():
    """
    User input for backtest and live session parameters
    """
    control = {}
    # ==================================================================
    # BACKTEST
    # ==================================================================
    control["days"] = 90  # backtest depth in days
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
def live(mode, control, storage, tune, scalp_tune):
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
        print("\n%s %s" % (tune["pair"], time.ctime()), "\n")
        if mode["live_debug"]:
            print("$$$$$$$$$$$$$$$$$$")
            print("WARN: DEBUG - RUNTIME: %s" % (info["current_time"] - info["begin"]))
            print("$$$$$$$$$$$$$$$$$$\n")
            print("WATCHDOG LATENCY:", watchdog())
            portfolio, data, storage = live_data(tune, storage, portfolio, data)
            storage, portfolio = indicators(
                data, tune, storage, portfolio, mode, info, scalp_tune
            )
            polynomial_regression(storage, tune, info)
            state_machine(storage, info, tune, control, portfolio, mode)
            hourly(info)
            daily(storage, info)
            cancel_all(mode)
            edicts = []
            storage, scalp_edicts = scalp(storage, info, scalp_tune, control, tune)
            edicts += scalp_edicts
            storage, trade_edicts = trade(storage, mode, portfolio, info, tune, control)
            edicts += trade_edicts
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
                print("\nRUNTIME: %s" % (info["current_time"] - info["begin"]))
                print("\nWATCHDOG LATENCY:", watchdog(), "\n")
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
                        data, tune, storage, portfolio, mode, info, scalp_tune
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
                    storage, scalp_edicts = scalp(
                        storage, info, scalp_tune, control, tune
                    )
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


def scalp(storage, info, scalp_tune, control, tune):
    """
    Scalping Strategy and Execution
    """
    now = int(time.time())
    # from metaNODE
    now = int(time.time())
    metaNODE = Bitshares_Trustless_Client()
    currency = metaNODE["currency_balance"]
    assets = metaNODE["asset_balance"]
    last = metaNODE["last"]
    max_currency = metaNODE["currency_max"]
    max_assets = metaNODE["asset_max"]
    invested = metaNODE["invested"]
    book = metaNODE["book"]
    del metaNODE
    ask_p = book["askp"][0]
    bid_p = book["bidp"][0]
    # from indicators(data, tune, storage, portfolio, mode,info)
    buying = storage["buying"]
    selling = storage["selling"]
    high = storage["high"]
    low = storage["low"]
    ma3 = storage["ma3"][-1]
    ma4 = storage["ma4"][-1]
    # plot zoom in
    now = time.time()
    past = now - 86400
    axis = plt.gca()
    axis.set_ylim([0.90 * last, 1.1 * last])
    axis.set_xlim([past, now])
    # means to buy and percent invested
    means = storage["means"] = currency / last  # assets can afford
    storage["max_assets"] = max_assets
    storage["asset_ratio"] = invested
    storage["max_currency"] = max_currency
    # define scalp_tune['enable'] support and resistance
    scalp_resistance = max(high, ma3, ma4)
    scalp_support = min(low, ma3, ma4)
    # expand scalp_tune['enable'] ops to dex just inside market bid/ask
    scalp_resistance = max(scalp_resistance, 0.999999999 * ask_p)
    scalp_support = min(scalp_support, 1.000000001 * bid_p)
    # adjust scalp_tune['enable'] margins if too thin
    scalp_margin = (scalp_resistance - scalp_support) / scalp_support
    if scalp_margin < scalp_tune["margin"]:
        midscalp = (scalp_resistance + scalp_support) / 2
        scalp_resistance = (1 + scalp_tune["margin"] / 2) * midscalp
        scalp_support = (1 - scalp_tune["margin"] / 2) * midscalp
    storage["scalp_shadow"] = (scalp_support, scalp_resistance)
    # limit scalp_tune['enable'] ops to a middle subset of the alpha channel
    market_spread = selling - buying
    no_scalping_zone = market_spread * ((1 - scalp_tune["zone"]) / 2)
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
        raise ValueError("scalp calculation error")
    # store scalp_tune['enable'] thresholds globally
    storage["scalp_resistance"] = scalp_resistance
    storage["scalp_support"] = scalp_support
    # scale orders to alpha market state and scalp_tune['fund']
    holding = storage["holding"]
    if holding:  # from primary trade() function
        max_holding = 1
        min_holding = 1 - scalp_tune["fund"]
    else:
        max_holding = scalp_tune["fund"]
        min_holding = 0
    buy_qty = max(0, max_assets * (max_holding - invested / 100))
    sell_qty = max(0, max_assets * (invested / 100 - min_holding))
    buy_qty = min(buy_qty, max_assets * scalp_tune["fund"])
    sell_qty = min(sell_qty, max_assets * scalp_tune["fund"])
    buy_qty *= scalp_tune["quantity"]
    sell_qty *= scalp_tune["quantity"]
    # break up scalp_tune['enable'] orders into smaller pieces
    pieces = scalp_tune["pieces"]
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
    edicts = []
    if scalp_tune["enable"]:
        print("")
        print("begin scalp_tune['enable']() ops")
        print("")
        print("assets        ", satoshi_str(assets))
        print("currency      ", satoshi_str(currency))
        print("invested      ", ("%.3f" % invested))
        print("means         ", satoshi_str(means))
        print("max assets    ", satoshi_str(max_assets))
        print("max currency  ", satoshi_str(max_currency))
        print("start assets  ", satoshi_str(storage["begin_max_assets"]))
        print("start currency", satoshi_str(storage["begin_max_currency"]))
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
        print("scalp support ", satoshi_str(scalp_support))
        print("scalp resist  ", satoshi_str(scalp_resistance))
        print("pieces        ", pieces, pie)
        print("")
        # scalp_tune['enable'] BUY
        for i in range(pieces):
            qty = buy_qty * pie[i]
            print("bqty", qty)
            scalp_tune["enable"] = scalp_support - i * 2 * random() * 10 ** -10
            try:
                if qty > control["min_amount"]:
                    print(
                        "scalp buy",
                        satoshi_str(qty),
                        "at",
                        satoshi_str(scalp_tune["enable"]),
                    )
                    edicts.append(
                        {
                            "op": "buy",
                            "price": scalp_tune["enable"],
                            "amount": qty,
                            "expiration": 0,
                        }
                    )
            except:
                pass
        # scalp_tune['enable'] SELL
        for i in range(pieces):
            qty = sell_qty * pie[i]
            print("sqty", qty)
            scalp_tune["enable"] = scalp_resistance + i * 2 * random() * 10 ** -10
            try:
                if qty > control["min_amount"]:
                    print(
                        "scalp sell",
                        satoshi_str(qty),
                        "at",
                        satoshi_str(scalp_tune["enable"]),
                    )
                    edicts.append(
                        {
                            "op": "sell",
                            "price": scalp_tune["enable"],
                            "amount": qty,
                            "expiration": 0,
                        }
                    )
            except:
                pass
    # Print trade pair and time
    time_local = datetime.fromtimestamp(int(time.time())).strftime("%H:%M:%S")
    time_utc = datetime.fromtimestamp(int(time.time()) + 18000).strftime("%H:%M:%S")
    print(("%.2f %s %.2f %s" % (currency, tune["currency"], assets, tune["asset"])))
    print(
        (
            "%s UTC                                             %s"
            % (time_utc, time_local)
        )
    )
    print(
        ("(buying: %.8f selling %.8f)" % (buying, selling))
        + ("(scalp buy %.8f, scalp sell %.8f)" % (scalp_support, scalp_resistance))
    )
    return storage, edicts


def trade(storage, mode, portfolio, info, tune, control):
    """
    Primary Order Execution
    """
    edicts = []
    buying = storage["buying"]
    selling = storage["selling"]
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
        if mode["live_test"]:
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
        if (last > 0.90 * selling) and not mode["live_test"]:
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
                        # iceberg front limit
                        selling_r *= 1.0 - 0.015 * random()
                        qty /= randint(69, 99)
                        if (qty > control["min_amount"]) and (random() > 0.5):
                            print(
                                (
                                    "SELLING MINI",
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
        if (last < 1.20 * buying) and not mode["live_test"]:
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
                        buying_r *= 1.0 + 0.015 * random()
                        qty /= randint(69, 99)
                        if (qty > control["min_amount"]) and (random() > 0.5):
                            print(
                                (
                                    "BUYING MINI",
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
        # test trade
        order = {}
        if portfolio["currency"] > 0:
            if storage["low"][-1] < buying:
                buying_r = min(storage["high"][-1], buying)
                order["price"] = buying
                if storage["bull_market"] is True:
                    order["call"] = "BULL SUPPORT"
                else:
                    order["call"] = "BEAR DESPAIR"
                test_buy(order, portfolio, storage, info, tune, mode)
        elif portfolio["assets"] > 0:
            if storage["high"][-1] > selling:
                selling_r = max(storage["low"][-1], selling)
                order["price"] = selling
                if storage["bull_market"] is True:
                    order["call"] = "BULL OVERBOUGHT"
                else:
                    order["call"] = "BEAR RESISTANCE"
                test_sell(order, portfolio, storage, info, tune, mode)
    if storage["holding"]:
        storage["holding_ticks"] += 1
    return storage, edicts


# BACKTEST
# ======================================================================
def backtest(storage, info, data, portfolio, mode, tune, control, scalp_tune):
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
                    data, tune, storage, portfolio, mode, info, scalp_tune
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
def draw_state_machine(state, mode, info, storage):
    """
    Plots primary trade indications
    """
    now = state["now"]
    selloff = state["selloff"]
    support = state["support"]
    despair = state["despair"]
    resistance = state["resistance"]
    ma1 = state["ma1"]
    ma2 = state["ma2"]
    ma2poly = state["ma2poly"]
    buying = state["buying"]
    selling = state["selling"]
    max_cross = state["max_cross"]
    min_cross = state["min_cross"]
    # do not plot state machine for sales backtests
    if not mode["sales"]:
        # shade active market red or green
        # shade extinct market purple
        if storage["bull_market"]:
            plt.plot(
                (now, now), (selloff, support), color="lime", label="state", alpha=0.15
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
        # set state machine marker size in backtest and live modes
        markersize_1 = 0.5
        markersize_2 = 1.5
        markersize_3 = 3
        markersize_4 = 3
        if mode["live"] or mode["paper"] or mode["live_test"]:
            markersize_1 = 1
            markersize_2 = 3
            markersize_3 = 4
            markersize_4 = 8
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
            markersize=markersize_4,
            marker=".",
            color="aqua",
            label="long",
        )
        # plot extinct market extremes purple
        plt.plot(
            now,
            selloff,
            markersize=markersize_2,
            marker=".",
            color="darkorchid",
            label="selloff",
        )
        plt.plot(
            now,
            support,
            markersize=markersize_2,
            marker=".",
            color="darkorchid",
            label="support",
        )
        plt.plot(
            now,
            despair,
            markersize=markersize_2,
            marker=".",
            color="darkorchid",
            label="despair",
        )
        plt.plot(
            now,
            resistance,
            markersize=markersize_2,
            marker=".",
            color="darkorchid",
            label="resistance",
        )
        # plot width of signal line
        if storage["bull_market"]:
            plt.plot(
                now,
                max_cross,
                markersize=markersize_3,
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
                markersize=markersize_3,
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
            markersize=markersize_4,
            marker=".",
            color="green",
            label="buying",
        )
        plt.plot(
            now,
            selling,
            markersize=markersize_4,
            marker=".",
            color="red",
            label="selling",
        )


def draw_test_state(mode, info, storage):
    """
    Add objects to backtest chart
    """
    try:
        # localize data
        state = {}
        state["now"] = info["current_time"]
        state["ma1"] = state["ma1poly"] = storage["ma1"][-1]
        state["ma2"] = state["ma2poly"] = storage["ma2"][-1]
        if info["live"]:
            state["ma1poly"] = storage["ma1poly"][-1]
            state["ma2poly"] = storage["ma2poly"][-1]
        state["selloff"] = storage["selloff"]
        state["despair"] = storage["despair"]
        state["resistance"] = storage["resistance"]
        state["support"] = storage["support"]
        state["max_cross"] = storage["max_cross"]
        state["min_cross"] = storage["min_cross"]
        state["bull_market"] = storage["bull_market"]
        state["buying"] = storage["buying"]
        state["selling"] = storage["selling"]
        draw_state_machine(state, mode, info, storage)
    except:
        pass


def draw_live_state_zero(info, data, tune, storage, mode):
    """
    initializes last 24 hours of indicator state machine
    """
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
    ma1_period = tune["ma1"] * 86400 / 14400.0
    ma2_period = tune["ma2"] * 86400 / 14400.0
    ma1_arr = float_period(data["14400"]["close"], ma1_period)
    ma2_arr = float_period(data["14400"]["close"], ma2_period)
    unix = data["14400"]["unix"]
    # backtest state machine clone; 24 hours high resolution
    for item in range(-1, -10, -1):
        for offset in range(0, 14400, 600):
            try:
                state = {}
                state["now"] = unix[item] + offset
                state["ma1"] = state["ma1poly"] = ma1_arr[item]
                state["ma2"] = state["ma2poly"] = ma2_arr[item]
                state["min_cross"] = tune["min_cross"] * state["ma1"]
                state["max_cross"] = tune["max_cross"] * state["min_cross"]
                state["bull_stop"] = tune["bull_stop"] * state["ma2"]
                state["bear_stop"] = tune["bear_stop"] * state["ma2"]
                state["selloff"] = tune["selloff"] * state["ma1"]
                state["despair"] = tune["despair"] * state["ma1"]
                state["support"] = max(
                    (tune["support"] * state["ma1"]), state["bull_stop"]
                )
                state["resistance"] = min(
                    (tune["resistance"] * state["ma1"]), state["bear_stop"]
                )
                state["selloff"] *= 1 - tune["gravitas"]
                state["resistance"] *= 1 - tune["gravitas"]
                state["support"] *= 1 + tune["gravitas"]
                state["despair"] *= 1 + tune["gravitas"]
                if bull_market:
                    state["selling"] = state["selloff"]
                    state["buying"] = state["support"]
                else:
                    state["buying"] = state["despair"]
                    state["selling"] = state["resistance"]
                # plot state machine
                draw_state_machine(state, mode, info, storage)
            except Exception as error:
                print(trace(error))
    plt.pause(0.001)
    plot_format(info, storage)


def draw_live_state(info, data, tune, storage, mode):
    """
    appends real time indicator state machine to chart
    """
    if info["tick"] == 0:
        draw_live_state_zero(info, data, tune, storage, mode)
    # localize low frequency indicators
    state = {}
    now = state["now"] = info["current_time"]
    state["ma1"] = storage["ma1"][-1]
    state["ma2"] = storage["ma2"][-1]
    state["ma1poly"] = storage["ma1poly"][-1]
    state["ma2poly"] = storage["ma2poly"][-1]
    state["selloff"] = storage["selloff"]
    state["despair"] = storage["despair"]
    state["support"] = storage["support"]
    state["resistance"] = storage["resistance"]
    state["buying"] = storage["buying"]
    state["selling"] = storage["selling"]
    state["max_cross"] = storage["max_cross"]
    state["min_cross"] = storage["min_cross"]
    # plot state machine
    draw_state_machine(state, mode, info, storage)
    # localize high frequency indicators
    shadow = storage["scalp_shadow"]
    scalp_support = storage["scalp_support"]
    scalp_resistance = storage["scalp_resistance"]
    # plot ma3 and ma4 scalping mesh
    plt.plot((now, now), shadow, color="black", label="scalp_shadow")
    # plot scalp_tune['enable'] thresholds
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


def draw_text(storage, info, mode, tune):
    """
    Display dynamic text regarding current market conditions
    """
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

    # to later test if high/low are outside buying/selling
    if info["live"]:
        high = storage["high"]
        low = storage["low"]
    else:
        high = storage["high"][-1]
        low = storage["low"][-1]

    # BitSharesQUANT & EXTINCTION EVENT in aqua
    textx = scale("x", 0.25)
    texty = scale("y", 0.7)
    if storage["bull_market"]:
        texty = scale("y", 0.1)
    storage["text"].append(
        plt.text(
            textx,
            texty,
            "EXTINCTION EVENT",
            horizontalalignment="center",
            color="aqua",
            alpha=0.3,
            size=20,
            weight="extra bold",
        )
    )
    texty = scale("y", 0.75)
    if storage["bull_market"]:
        texty = scale("y", 0.15)
    storage["text"].append(
        plt.text(
            textx,
            texty,
            "BitSharesQUANT",
            horizontalalignment="center",
            color="aqua",
            alpha=0.3,
            size=30,
            weight="extra bold",
        )
    )
    # bull market labels in green
    if storage["bull_market"]:
        texty = scale("y", 0.7)
        storage["text"].append(
            plt.text(
                textx,
                texty,
                "BULL MARKET",
                horizontalalignment="center",
                color="lime",
                alpha=0.3,
                size=30,
                weight="extra bold",
            )
        )
        texty = scale("y", 0.65)
        if low < storage["buying"]:
            storage["text"].append(
                plt.text(
                    textx,
                    texty,
                    "BUY SUPPORT",
                    horizontalalignment="center",
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
                    horizontalalignment="center",
                    color="red",
                    alpha=0.5,
                    size=20,
                    weight="extra bold",
                )
            )
    # bear market labels in red
    else:
        texty = scale("y", 0.1)
        storage["text"].append(
            plt.text(
                textx,
                texty,
                "BEAR MARKET",
                horizontalalignment="center",
                color="red",
                alpha=0.3,
                size=30,
                weight="extra bold",
            )
        )
        texty = scale("y", 0.05)
        if low < storage["buying"]:
            storage["text"].append(
                plt.text(
                    textx,
                    texty,
                    "BUY DESPAIR",
                    horizontalalignment="center",
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
                    horizontalalignment="center",
                    color="red",
                    alpha=0.5,
                    size=20,
                    weight="extra bold",
                )
            )
    # LAST, PAIR, MODE, DIVERGENCE in orange
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
    texty = scale("y", 0.1)
    text = ""
    if mode["id"] == 1:
        text = "BACKTEST"
    if mode["id"] == 2:
        text = "PAPER"
    if mode["id"] == 3:
        text = "LIVE"
    if mode["id"] == 4:
        text = "SALES"
    if mode["id"] == 5:
        text = "LIVE DEBUG"
    if mode["id"] == 6:
        text = "LIVE TEST"
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
        # display divergence and days to next crossing
        divergence_text = (" Divergence %.8f\n" % storage["mesh"]) + (
            " Next Cross %.2f Days" % storage["next_cross"]
        )
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
    if info["live"]:
        # label selloff, support, resistance, and  despair
        # use dynamic text height
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
        # triangle marker for last price at y-scale on far right
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
                "EXTINCT EVENT \u2588 ",
                horizontalalignment="right",
                color="darkorchid",
                size=8,
            )
        )
        y_value *= 0.97
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
                ("SCALP SELL %.8f \u2588 " % storage["scalp_resistance"]),
                horizontalalignment="right",
                color="tomato",
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
                ("SCALP BUY %.8f \u2588 " % storage["scalp_support"]),
                horizontalalignment="right",
                color="palegreen",
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


# ALGORITHM
# ======================================================================
def indicators(data, tune, storage, portfolio, mode, info, scalp_tune):
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
        # scalp_tune['enable'] moving averages
        storage["ma3"] = float_period(data["300"]["close"], 288 * scalp_tune["ma3"])
        storage["ma4"] = float_period(data["300"]["close"], 288 * scalp_tune["ma4"])
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
        # recent volume ratio for plotting
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
    # float_period() returns stepwise due to 10m tick with 4h candle
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
    # create unix timestamps 24 hours into past and future: _x x_
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
    # state_machine() will use "smoothed" ma1poly and ma2poly data
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


def state_machine(storage, info, tune, control, portfolio, mode):
    """
    Finite State Machine Primary Logic Tree
    """

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
    # establish beta thresholds
    storage["selloff"] = ma1 * tune["selloff"]
    storage["support"] = ma1 * tune["support"]
    storage["despair"] = ma1 * tune["despair"]
    storage["resistance"] = ma1 * tune["resistance"]
    # adjust support & resistance stoploss near tune['ma1']/tune['ma2'] crossing
    storage["support"] = max(storage["support"], ma2 * tune["bull_stop"])
    storage["resistance"] = min(storage["resistance"], ma2 * tune["bear_stop"])
    # adjust beta thresholds conservatively per tune['gravitas']
    storage["selloff"] *= 1 - tune["gravitas"]
    storage["support"] *= 1 + tune["gravitas"]
    storage["despair"] *= 1 + tune["gravitas"]
    storage["resistance"] *= 1 - tune["gravitas"]
    # initialize backtest per control['bull_market']
    if (info["live"] is False) and (info["tick"] == 0):
        order = {}
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
        ma1_concavity = storage["ma1_concavity"] = (ma1[-1] - ma1[-5]) - (
            ma1[-5] - ma1[-10]
        )
        ma2_concavity = storage["ma2_concavity"] = (ma2[-1] - ma2[-5]) - (
            ma2[-5] - ma2[-10]
        )
        ma1_ = storage["ma1poly"][-10]
        ma2_ = storage["ma2poly"][-10]
        min_cross_ = tune["min_cross"] * ma1_
        max_cross_ = tune["max_cross"] * min_cross_
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
        # on the first live tick we do not have scalp_tune['enable'] values
        # substitute buying and selling for initial plot labels
        storage["scalp_resistance"] = storage.get(
            "scalp_resistance", storage["selling"]
        )
        storage["scalp_support"] = storage.get("scalp_support", storage["buying"])
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
        print("long average: ", ma2, "slope:", ma2_slope, "concavity:", ma2_concavity)
        print("signal line: ", signal, "slope:", ma1_slope, "concavity:", ma1_concavity)
        print("divergence:   ", mesh)
        print("")


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
    scalp_tune = scalp_tune_install()
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
        backtest(storage, info, data, portfolio, mode, tune, control, scalp_tune)
    print_tune(tune, storage)
    if mode["id"] in [2, 3, 6]:
        live(mode, control, storage, tune, scalp_tune)
    elif mode["optimize"]:
        optimizer()
    else:
        plt.show()


if __name__ == "__main__":
    main()
# ======================================================================
# EXTINCTION EVENT - CEX MUST DIE
# ======================================================================
#
# THE DESTROYER,
# litepresence - 2019
#
