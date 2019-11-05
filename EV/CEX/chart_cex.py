"""
Plots Historic Candles, Volume, and Depth of Market 

Makes calls to 6 exchanges simultaneously

deomonstrates functionality of public_cex.py

https://i.imgur.com/evwcUYa.png
"""

# STANDARD MODULES
# ======================================================================
from pprint import pprint
from multiprocessing import Process

# THIRD PARTY MODULES
# ======================================================================
from pylab import *
import numpy as np

# EXTINCTION EVENT MODULES
# ======================================================================
from public_cex import get_price, get_book, get_candles


def plot_format(axis):
    """
    Edit colors and title bar, etc.
    """
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
    axis.title.set_color("0.9")


def zoom_to_data(axis):
    """
    change axis limits of plot to show all data
    """
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
    return ymax, ymin, xmax, xmin



def log_y_labels(axis, form):
    """
    Logarithmic scale the Y axis
    """
    axis.set_yscale("log")
    satoshi_format = matplotlib.ticker.FormatStrFormatter(form)
    # axis.yaxis.set_major_formatter(satoshi_format)
    axis.yaxis.set_minor_formatter(satoshi_format)
    ymax, ymin, _, _ = zoom_to_data(axis)
    set_sub_formatter = []
    for coeff in [10, 12, 16, 22, 35]:
        for power in range(-8, 8):
            set_sub_formatter.append(coeff * 10 ** power)
    labels = []
    for label in set_sub_formatter:
        if ymin < label < ymax:
            labels.append(label)
    axis.set_yticks(labels)


def demo(exchange, symbol):
    """
    Print demo of last price, orderbook, and candles
    Formatted to extinctionEVENT standards
    """
    print("\n***", exchange.upper(), "PRICE ***")
    price = get_price(exchange, symbol)
    # pprint(price)

    print("\n***", exchange.upper(), "BOOK ***")
    depth = 50
    book = get_book(exchange, symbol, depth)

    if price > book["askp"][0]:
        price = book["askp"][0]

    if price < book["bidp"][0]:
        price = book["bidp"][0]

    # pprint(book)
    # kline request parameters
    interval = 86400
    # None / None will return latest ten candles
    start = None  # or unix epoch seconds
    end = None  # or unix epoch seconds

    print("\n***", exchange.upper(), "CANDLES ***")
    now = int(time.time())
    depth = 600
    start = now - interval * depth
    end = now
    candles = get_candles(exchange, symbol, interval, start, end)
    # pprint(candles)

    bid_cum_v = np.cumsum(book["bidv"])
    ask_cum_v = np.cumsum(book["askv"])
    bid_v0 = np.zeros(len(bid_cum_v))
    ask_v0 = np.zeros(len(ask_cum_v))
    candles_0 = np.zeros(len(candles["unix"]))

    f, axarr = plt.subplots(3, 1, figsize=(5, 25))
    f.canvas.set_window_title((exchange.upper() + " " + symbol))

    f.set_facecolor((0, 0, 0))

    axarr[0].set_ylabel("CANDLES")

    axarr[0].plot(candles["unix"], candles["open"], color="white")
    axarr[0].plot(candles["unix"], candles["close"], color="yellow")
    axarr[0].plot(candles["unix"], candles["high"], color="green")
    axarr[0].plot(candles["unix"], candles["low"], color="red")

    axarr[0].plot(
        (candles["unix"][-1], candles["unix"][-len(candles["unix"])]),
        (price, price),
        color="yellow",
    )
    axarr[0].text(
        candles["unix"][-len(candles["unix"])],
        price,
        ("  %.8f" % price),
        horizontalalignment="left",
        verticalalignment="bottom",
        color="yellow",
        # alpha=0.3,
        size=13,
        weight="extra bold",
    )

    log_y_labels(axarr[0], "%.8f")
    plot_format(axarr[0])

    axarr[1].set_ylabel("VOLUME")
    axarr[1].plot(candles["unix"], candles["volume"], "magenta", alpha=0.75)
    axarr[1].fill_between(
        candles["unix"], candles_0, candles["volume"], color="magenta", alpha=0.25
    )

    plot_format(axarr[1])

    # axarry1twin.yaxis.tick_left()

    max_volume = max(max(ask_cum_v), max(bid_cum_v))
    axarr[2].set_ylabel("{} {} BOOK".format(exchange.upper(), symbol))
    axarr[2].plot(book["bidp"], bid_cum_v, color="green")
    axarr[2].plot(book["askp"], ask_cum_v, color="red")

    axarr[2].fill_between(book["askp"], ask_v0, ask_cum_v, color="red", alpha=0.15)
    axarr[2].fill_between(book["bidp"], bid_v0, bid_cum_v, color="green", alpha=0.15)
    axarr[2].fill_between(book["bidp"], ask_v0, book["bidv"], color="lime")
    axarr[2].fill_between(book["askp"], bid_v0, book["askv"], color="tomato")
    axarr[2].plot((price, price), (0, (0.9 * max_volume)), color="yellow")
    axarr[2].text(
        price,
        0.975 * max_volume,
        ("%.8f" % price),
        horizontalalignment="center",
        color="yellow",
        # alpha=0.3,
        size=13,
        weight="extra bold",
    )
    axarr[2].text(
        price,
        0.95 * max_volume,
        (("%.8f" % book["bidp"][0]).replace(".", "").lstrip("0") + "  "),
        horizontalalignment="right",
        color="green",
        size=10,
        weight="extra bold",
    )
    axarr[2].text(
        price,
        0.95 * max_volume,
        ("  " + ("%.8f" % book["askp"][0]).replace(".", "").lstrip("0")),
        horizontalalignment="left",
        color="red",
        size=10,
        weight="extra bold",
    )

    plot_format(axarr[2])
    # axarr[2].set_xscale("log")
    form = str("%.8f".replace(".", "").lstrip("0"))
    form = matplotlib.ticker.FormatStrFormatter(form)
    axarr[2].xaxis.set_major_formatter(form)
    axarr[2].xaxis.set_minor_formatter(form)
    tight_layout()
    show()


def main():
    """
    Primary Demonstration Events
    """
    print("\033c", __doc__)
    symbol = "XLM:BTC"
    exchanges = ["bittrex", "bitfinex", "binance", "poloniex", "coinbase", "kraken"]
    print("\n", symbol, "\n")
    print("fetching PRICE, BOOK, and CANDLES from:\n\n", exchanges)
    child = {}
    for exchange in exchanges:
        print("\n==================\n", exchange.upper(), "API\n==================")
        child[exchange] = Process(target=demo, args=(exchange, symbol))
        child[exchange].daemon = False
        child[exchange].start()
    print("\n\n\nProcesses initialized !!!\n\n\n")


if __name__ == "__main__":
    main()
