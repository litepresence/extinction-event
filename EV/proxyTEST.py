# ======================================================================
VERSION = "proxyTEST v0.00000001"
# ======================================================================

# Plots Data Retrieved by proxyCEX, proxyDEX, proxyMIX, and proxyALPHA

" litepresence 2019 "


def WTFPL_v0_March_1765():
    if any([stamps, licenses, taxation, regulation, fiat, etat]):
        try:
            print("no thank you")
        except:
            return [tar, feathers]


" ********** ALPHA RELEASE TO PUBLIC DOMAIN WITH NO WARRANTY ********* "

# standard python modules
from datetime import datetime
from pprint import pprint
import time
import sys

# will require installation
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# litepresence/extinction-event
from proxyALPHA import proxyFOX, proxySTX, proxyCRY
from proxyCEX import proxyCEX
from proxyDEX import proxyDEX
from proxyMIX import proxyMIX

API = 6

if API == 1:
    source = "DEX"  # bitshares public rpc nodes
    asset = "BTS"  # Bitshares
    currency = "OPEN.BTC"  # Open Ledger Bitcoin
if API == 2:
    source = "CEX"  # www.cryptocompare.com altcoin:altcoin
    asset = "BTS"  # Bitshares
    currency = "ETH"  # Ethereum
if API == 3:
    source = "STX"  # www.alphavantage.com stocks:usd
    asset = "AAPL"  # Apple, Inc. US Stock
    currency = "USD"  # US Dollar
if API == 4:
    source = "FOX"  # www.alphavantage.com forex
    asset = "THB"  # Thai Baht
    currency = "USD"  # US Dollar
if API == 5:
    source = "CRY"  # www.alphavantage.com crypto:fiat
    asset = "BTC"  # Bitcoin
    currency = "KRW"  # South Korean Won
if API == 6:
    source = "MIX"  # www.nomics.com crypto markets
    exchange = "binance"  # exchange specific markets
    asset = "ETH"  # Binance Ethereum
    currency = "BTC"  # Binance Bitcoin

candles = 600
period = 86400

now = int(time.time())
start = now - candles * period
stop = now


def format_plot():
    def timestamp(x, pos):

        return (datetime.fromtimestamp(x)).strftime("%Y-%m-%d %H:%M")
        # return (datetime.fromtimestamp(x)).strftime('%m/%d %H:%M')

    def zoom_to_data():

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
        # todo, this definition can be optimized to use less resource
        return ymax, ymin, xmax, xmin

    # format colors
    fig.patch.set_facecolor("black")
    ax.patch.set_facecolor("0.1")
    ax.spines["bottom"].set_color("0.5")
    ax.spines["top"].set_color(None)
    ax.spines["right"].set_color("0.5")
    ax.spines["left"].set_color(None)
    ax.tick_params(axis="x", colors="0.7", which="both")
    ax.tick_params(axis="y", colors="0.7", which="both")
    ax.yaxis.label.set_color("0.9")
    ax.xaxis.label.set_color("0.9")
    fig.canvas.set_window_title(title)

    # format x axis labels
    # ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    # ax.yaxis.set_minor_formatter(matplotlib.ticker.ScalarFormatter())
    ax.xaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(timestamp)
    )
    plt.gcf().autofmt_xdate(rotation=30)

    # format y axis labels
    plt.yscale("log")
    ax.yaxis.tick_right()
    ymax, ymin, xmax, xmin = zoom_to_data()
    set_sub_formatter = []
    sub_ticks = [10, 11, 12, 14, 16, 18, 22, 25, 35, 45]
    sub_ticks = [8, 16, 32, 64]
    sub_range = [-8, 8]
    for i in sub_ticks:
        for j in range(sub_range[0], sub_range[1]):
            set_sub_formatter.append(i * 10 ** j)
    k = []
    for l in set_sub_formatter:
        if ymin < l < ymax:
            k.append(l)
    ax.set_yticks(k)
    ax.yaxis.set_major_formatter(
        matplotlib.ticker.FormatStrFormatter("%.8f")
    )
    ax.yaxis.set_minor_formatter(
        matplotlib.ticker.FormatStrFormatter("%.8f")
    )
    plt.tight_layout()


def to_iso_date(unix):  # returns iso8601 datetime given unix epoch
    return datetime.utcfromtimestamp(int(unix)).isoformat()


def plot(data):

    x = data["unix"]
    plt.plot(x, data["high"], color="lime", alpha=0.3)
    plt.plot(x, data["low"], color="red", alpha=0.3)
    plt.plot(x, data["open"], color="yellow", alpha=0.3)
    plt.plot(x, data["close"], color="yellow", alpha=0.3)


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


def report(data):

    print("test")

    end = max(data["unix"])

    pprint(data)
    print("")
    print([k for k, v in data.items()])
    print("depth", len(data["unix"]))
    print("period", data["unix"][1] - data["unix"][0])
    print("end unix  ", end)
    print("end local ", time.ctime(end))
    print("end utc   ", to_iso_date(end))


def main():

    global fig, ax, title

    title = "proxyTEST" + str([source, asset, currency])
    sys.stdout.write("\x1b]2;" + title + "\x07")
    print("\033c")

    if source == "CEX":
        data = proxyCEX(asset, currency, start, stop, period)
    if source == "DEX":
        data = proxyDEX(asset, currency, start, stop, period)
    if source == "STX":
        data = proxySTX(asset, currency, start, stop, period)
    if source == "FOX":
        data = proxyFOX(asset, currency, start, stop, period)
    if source == "CRY":
        data = proxyCRY(asset, currency, start, stop, period)
    if source == "MIX":
        data = proxyMIX(exchange, asset, currency, start, stop, period)

    MA1 = float_sma(data["close"], 30)
    MA1x = data["unix"][-len(MA1) :]
    MA2 = float_sma(data["close"], 60)
    MA2x = data["unix"][-len(MA2) :]
    MA3 = float_sma(data["close"], 90)
    MA3x = data["unix"][-len(MA3) :]

    fig = plt.figure()
    ax = plt.axes()
    report(data)
    plot(data)

    plt.plot(MA1x, MA1, color="white")
    plt.plot(MA2x, MA2, color="aqua")
    plt.plot(MA3x, MA3, color="magenta")

    format_plot()
    plt.show()


if __name__ == "__main__":

    main()
