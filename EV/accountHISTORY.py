
' accountHISTORY '

# Bitshares Historical Account Balance Visualization Tool

' litepresence 2018 '

# Whenever your metaNODE.py restarts
# it appends currency_max and asset_max
# to accountHISTORY.txt text file, along with unix timestamp
# Every hour it appends another snapshot
# When you want to read the text file json
# you run python script accountHISTORY.py and you get visualization


def WTFPL_v0_March_1765():
    if any([stamps, licenses, taxation, regulation, fiat, etat]):
        try:
            print('no thank you')
        except:
            return [tar, feathers]

import sys
import time
import json
import warnings
from datetime import datetime
from tkinter import *
import matplotlib.ticker as tkr
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

sys.stdout.write(
    '\x1b]2;' +
    'Bitshares accountHISTORY' +
    '\x07')  # terminal #title


def cyan(text):  # colorize with escape sequence
    return ('\033[96m' + text + '\033[0m')


def json_read(doc=''):  # Concurrent Read from File Operation

    opened = 0
    while not opened:
        try:
            with open(doc, 'r') as f:
                ret = f.read().splitlines()
                ret = list(ret)
                # print(ret)
                ret = [json.loads(str(r).replace("'", '"')) for r in ret]
                for r in ret:
                    print(r)
                opened = 1

        except Exception as e:

            time.sleep(0.1)
            pass

    return ret


def plt_format():

    warnings.filterwarnings("ignore", category=cbook.mplDeprecation)
    ax = plt.gca()
    ax.patch.set_facecolor('0.1')
    ax.yaxis.tick_right()
    ax.spines['bottom'].set_color('0.5')
    ax.spines['top'].set_color(None)
    ax.spines['right'].set_color('0.5')
    ax.spines['left'].set_color(None)
    ax.tick_params(axis='x', colors='0.7', which='both')
    ax.tick_params(axis='y', colors='0.7', which='both')
    ax.yaxis.label.set_color('0.9')
    ax.xaxis.label.set_color('0.9')
    plt.minorticks_on
    plt.grid(b=True, which='major', color='0.2', linestyle='-')
    plt.grid(b=True, which='minor', color='0.2', linestyle='-')
    ax.yaxis.set_major_formatter(tkr.ScalarFormatter())
    ax.yaxis.set_minor_formatter(tkr.ScalarFormatter())
    ax.yaxis.set_major_formatter(tkr.FormatStrFormatter("%.8f"))
    ax.yaxis.set_minor_formatter(tkr.FormatStrFormatter("%.2f"))
    plt.autoscale(enable=True, axis='y')
    plt.tight_layout()
    plt.gcf().autofmt_xdate(rotation=30)
    plt.gcf().canvas.set_window_title('microDEX DOM')

    def timestamp(x, pos):
        return (datetime.fromtimestamp(x)).strftime('%m/%d %H:%M')
    ax.xaxis.set_major_formatter(tkr.FuncFormatter(timestamp))
    plt.gcf().autofmt_xdate(rotation=30)
    plt.gcf().canvas.set_window_title('accountHISTORY - Bitshares')


def draw_chart():

    grid = plt.GridSpec(3, 2)
    plt.subplot(grid[0, 0:])
    plt.title(('price ' + asset + ':' + currency), color='r')
    plt.plot(unix, price, 'go-')
    plt_format()

    plt.subplot(grid[1, 0])
    plt.title(('maximum ' + currency), color='r')
    plt.plot(unix, currency_max, 'ro-')
    plt_format()

    plt.subplot(grid[1, 1])
    plt.title(('maximum ' + asset), color='b')
    plt.plot(unix, asset_max, 'bo-')
    plt_format()

    plt.subplot(grid[2, 0])
    plt.title('percent invested', color='g')
    plt.plot(unix, invested, 'go-')
    plt_format()

    plt.subplot(grid[2, 1])
    plt.title('RETURN ON INVESTMENT', color='g')
    plt.plot(unix, currency_roi, 'ro-')
    plt.plot(unix, asset_roi, 'bo-')
    plt.plot(unix, gross_roi, 'go-')
    plt_format()
    plt.show()

print("\033c")  # clear screen and logo
import zlib
b = b'x\x9c\xad\xd4M\n\xc4 \x0c\x05\xe0}O1P\x12B\x10\xbc\x82\xf7?\xd5\xf8\xaf\x83F\xe3\xe0[t\xf9\xf5%\xda>\x9f\x1c\xf7\x7f\x9e\xb9\x01\x17\x0cc\xec\x05\xe3@Y\x18\xc6(\'Z\x1a\xca.\x1bC\xa5l\r\x85\xa20\xb6\x8a\xca\xd8,W0\xec\x05\xc3\xdf\xd4_\xe3\r\x11(q\x16\xec\x95l\x04\x06\x0f\x0c\xc3\xddD\x9dq\xd2#\xa4NT\x0c/\x10\xd1{b\xd4\x89\x92\x91\x84\x11\xd9\x9d-\x87.\xe4\x1cB\x15|\xe0\xc8\x88\x13\xa5\xbc\xd4\xa21\x8e"\x18\xdc\xd2\x0e\xd3\xb6\xa0\xc6h\xa3\xd4\xde\xd0\x19\x9a\x1e\xd8\xddr\x0e\xcf\xf8n\xe0Y\rq\x1fP:p\x92\xf2\xdbaB,v\xda\x84j\xc4.\x03\xb1>\x97\xee{\x99oSa\x00\x0f\xc6\x84\xd8\xdf\x0f\xb4e\xa7$\xfdE\xae\xde\xb1/\x1d\xfc\x96\x8a'
print(cyan(zlib.decompress(b).decode()))

print('')
print('reading your account history...')
print('')
time.sleep(1)


doc = json_read(doc='account_history.txt')
for i in range(4):
    print('')
print('plotting...')
for i in range(4):
    print('')
time.sleep(1)


def data_set():

    global currency, asset, currency_max, asset_max
    global unix, invested, price, begin, end
    global currency_roi, asset_roi, gross_roi

    start = 0
    stop = 9999999999999999999
    try:
        start = float(BEGIN.get())
        stop = float(END.get())
        var.set('')
        if start > stop:
            var.set('BEGIN must be less than END')
            raise ValueError('BEGIN must be less than END')
    except Exception as e:
        if not 'name' in str(e.args[0]):
            print(e.args[0])
        start = 0
        stop = 9999999999999999999
        pass

    currency = doc[0]['comment']['currency']
    asset = doc[0]['comment']['asset']
    currency_max = []
    asset_max = []
    unix = []
    invested = []

    for i in range(len(doc)):

        if ((doc[i]['comment']['unix'] > start) and
                (doc[i]['comment']['unix'] < stop)):

            currency_max.append(doc[i]['comment']['currency_max'])
            asset_max.append(doc[i]['comment']['asset_max'])
            unix.append(doc[i]['comment']['unix'])
            invested.append(doc[i]['comment']['invested'])

    begin = min(unix)
    end = max(unix)

    currency_roi = [r / currency_max[0] for r in currency_max]

    # for r in asset_max:

    asset_roi = [r / asset_max[0] for r in asset_max]

    gross_roi = []
    price = []
    for i in range(len(asset_max)):
        gross_roi.append((currency_roi[i] * asset_roi[i]) ** (1 / 2.0))
        price.append(currency_max[i] / asset_max[i])


def refresh():
    data_set()
    draw_chart()

data_set()

fig = plt.figure()
fig.patch.set_facecolor('0.15')
interface = Tk()
f1 = Frame()
f1.pack()
f2 = Frame()
f2.pack()
f3 = Frame()
f3.pack()
BEGIN = Scale(f1,
              from_=begin,
              to=end,
              resolution=1,
              orient=HORIZONTAL,
              length=300)

Label(f1, text='BEGIN').pack(side=LEFT)
BEGIN.set(begin)
BEGIN.pack(side=LEFT)

END = Scale(f2,
            from_=begin,
            to=end,
            resolution=1,
            orient=HORIZONTAL,
            length=300)

Label(f2, text='    END').pack(side=LEFT)
END.set(end)
END.pack(side=LEFT)

Button(f3, text='UPDATE CHART', command=refresh).pack(side=LEFT)
var = StringVar()
var.set('')
Label(f3, textvariable=var).pack(side=LEFT)

interface.after(1, refresh)

interface.title('microDEX plot updater')
interface.geometry("0x0+0+0")
interface.lift()
interface.call('wm', 'attributes', '.', '-topmost', True)
interface.mainloop()
