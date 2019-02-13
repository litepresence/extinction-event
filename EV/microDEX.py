
# ======================================================================
VERSION = 'microDEX - Bitshares Minimalist UI 0.00000026'
# ======================================================================
# Lightweight BUY/SELL/CANCEL UI for Bitshares Decentralized Exchange

' litepresence 2019 '


def WTFPL_v0_March_1765():
    if any([stamps, licenses, taxation, regulation, fiat, etat]):
        try:
            print('no thank you')
        except:
            return [tar, feathers]

' ********** ALPHA RELEASE TO PUBLIC DOMAIN WITH NO WARRANTY ********* '

# Standard Modules
import os
import sys
import time
import requests
import traceback
import numpy as np
import tkinter as tk
from getpass import getpass
from multiprocessing import Process
from json import dumps as json_dumps
from json import loads as json_loads
from decimal import Decimal as decimal
from sys import platform, version_info
from random import choice
from pprint import pprint
# litepresence/extinction-event modules
from manualSIGNING import broker, prototype_order

# CONTROLS
# ======================================================================
DEV = True  # additional feedback in terminal log
COLOR = True  # black and white only in terminal
UI_REFRESH = 0.100  # seconds between ui button animation
# CONSTANTS
# ======================================================================
BEGIN = int(time.time())
SATOSHI = decimal(0.00000001)
SIXSIG = decimal(0.999999)
ANTISAT = 1 / SATOSHI
# bitshares mainnet chain ID
ID = '4018d7844c78f6a6c41c6a552b898022310fc5dec06da467ee7905a8dad512c8'

# AUTHENTICATED DEX ACTIONS
# ======================================================================


def buy(price, amount):

    confirm.destroy()
    account_state()
    edicts = [{'op': 'buy',
               'price': price,
               'amount': amount,
               'expiration': 0}]
    place_order(edicts)


def sell(price, amount):

    confirm.destroy()
    account_state()
    edicts = [{'op': 'sell',
               'price': price,
               'amount': amount,
               'expiration': 0}]
    place_order(edicts)


def cancel():

    confirm.destroy()
    account_state()
    edicts = [{'op': 'cancel', 'ids': ['1.7.X']}]
    place_order(edicts)


def log_in():

    global authenticated
    edicts = [{'op': 'login'}]
    order = json_loads(prototype_order())
    order['header']['wif'] = wif
    order['edicts'] = edicts
    authenticated = broker(order)


def place_order(edicts):

    order = json_loads(prototype_order())
    order['header']['wif'] = wif
    order['edicts'] = edicts
    process(order)


def process(order):

    # concurrent process wrapper for broker threading
    # broker itself is a timeout joined process
    process = Process(target=broker, args=(order,))
    process.daemon = False
    process.start()


# LOGO, COLOR, AND PRINTING
# ======================================================================


def trace(e):

    return (str(type(e).__name__) + str(e.args) + str(e) +
            str(traceback.format_exc()) + str(sys.exc_info()))


def it(style, text):

    # color printing in terminal
    emphasis = {'red': 91,
                'green': 92,
                'yellow': 93,
                'blue': 94,
                'purple': 95,
                'cyan': 96}
    return (('\033[%sm' % emphasis[style]) + str(text) + '\033[0m')


def colors():

    # tk widget colors
    global red1, red2, blue1, blue2, yellow1, yellow2, green1, green2
    global gray1, gray2, gray3
    red1 = '#ff5858'
    red2 = '#820000'
    blue1 = '#77c5ec'
    blue2 = '#247fab'
    yellow1 = '#dcd900'
    yellow2 = '#989200'
    green1 = '#00d905'
    green2 = '#026500'
    gray1 = '#C0C0C0'
    gray2 = '#3f3f3f'
    gray3 = '#262626'


def ascii_logo(design):

    # ascii artwork stored in pastebins
    urls = {'bitshares': 'https://pastebin.com/raw/xDJkyBrS',
            'microdex': 'https://pastebin.com/raw/3DYAUqQR',
            'extinction-event': 'https://pastebin.com/raw/5YuEHcC4',
            'metanode': 'https://pastebin.com/raw/VALMtPjL',
            'version': 'https://raw.githubusercontent.com/litepresence' +
                        '/extinction-event/master/EV/microDEX.py'}
    try:
        return (requests.get(urls[design], timeout=(6, 30))).text
    except:
        return ''


def clear_terminal():

    print("\033c")


def terminal_title():

    sys.stdout.write(
        '\x1b]2;' +
        VERSION +
        '\x07')


def download_img(url, filename):

    ret = requests.get(url, timeout=(6, 30))
    with open(filename, 'wb') as f:
        for chunk in ret.iter_content(4096):
            f.write(chunk)


def account_state():

    print(' ASSETS: ' + (ap % asset_balance).rjust(12, ' ') +
          '         CURRENCY: ' +
          (cp % currency_balance).rjust(12, ' ') +
          '                BITSHARES: %.2f' % bts_balance)
    print(' ORDERS: ' +
         (ap % sell_orders).rjust(12, ' ') +
          '                   ' +
         (cp % buy_orders).rjust(12, ' ') +
          '                     LAST: %.16f' % last)
    print('  TOTAL: ' +
         (ap % asset_total).rjust(12, ' ') +
          ' ' + (str(invested) + ' %').ljust(7, ' ') +
          '           ' +
         (cp % currency_total).rjust(12, ' ') +
          ' ' + str(divested).ljust(5, ' ') +
          '               TIME: %s' % time.ctime())
    print('    MAX: ' +
         (ap % asset_value).rjust(12, ' ') + ' ' +
          asset.ljust(10, ' ') +
          '        ' +
         (cp % currency_value).rjust(12, ' ') + ' ' +
          currency.ljust(10, ' '))


# TEXT PIPE
# ======================================================================


def Bitshares_Trustless_Client():

    for i in range(5):
        try:
            with open('metaNODE.txt', 'r') as f:
                ret = f.read()  # .replace("'",'"')
                f.close()
                metaNODE = json_loads(ret)
                return metaNODE
        except Exception as e:
            msg = str(
                time.ctime(
                ) + ' ' + type(
                    e).__name__) + ' ' + str(
                e.args)
            race_condition = ['Unterminated', "Expecting"]
            if any([x in str(e.args) for x in race_condition]):
                continue  # print('metaNODE RACE READ')
            elif 'metaNODE is blank' in str(e.args):
                continue
            else:
                print('metaNODE ' + msg)
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


def race_append(doc='', text=''):

    # Concurrent Append to File Operation
    text = '\n' + str(time.ctime()) + ' ' + str(text) + '\n'
    for i in range(10):
        try:
            with open(doc, 'a+') as f:
                f.write(str(text))
                return
        except Exception as e:
                msg = (time.ctime() + str(type(e).__name__) +
                       str(e.args))
                print('race_append' + msg)
                continue


def race_write(doc='', text=''):

    # Concurrent Write to File Operation
    text = str(text)
    for i in range(10):
        try:
            with open(doc, 'w+') as f:
                f.write(text)
                f.close()
                return
        except Exception as e:
            msg = str(type(e).__name__) + str(e.args)
            if DEV:
                msg += str(traceback.format_exc())
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

def race_read(doc=''):  # Concurrent Read from File Operation

    for i in range(3) :
        try:
            with open(doc, 'r') as f:
                return f.read()
        except Exception as e:
            msg = (time.ctime() + str(type(e).__name__) + str(e.args))
            print('race_read ' + msg)
    raise

# WELCOME
# ======================================================================


def initialize():

    global update_id

    update_id = 0
    race_write(doc='microDEX_log.txt', text=time.ctime())
    colors()
    terminal_title()
    clear_terminal()
    print('')
    print('   initializing microDEX...')
    bitshares_logo = it('cyan', ascii_logo('bitshares'))
    clear_terminal()
    print(bitshares_logo)
    print('')
    print(it('blue', ascii_logo('microdex')))
    print(it('blue', '''
    ===================================================================
          '''))
    print(it('cyan', '              ' + VERSION))
    print(it('blue', '''
    ===================================================================
          '''))
    print(it('cyan', 'CHECKING version number...'))
    print('')
    check_version()
    print(it('cyan', 'GATHERING curated DEX data from the metaNODE...'))
    time.sleep(0.2)
    try:
        cache()
        print('')
        print(it('yellow', '      metaNODE = Bitshares_Trustless_Client()'))
    except:
        raise ValueError('metaNODE was not found')
    print('')
    time.sleep(0.2)
    print(it('cyan', 'CHOOSING whitelisted public API...'))
    time.sleep(0.2)
    print('')
    print('      ' + it('green', nodes[0]))
    print('')
    print(it('cyan', 'CONNECTING to DEX account...'))
    time.sleep(0.2)
    print('')
    print('      Welcome Back: ',
          it('green', account_name), it('blue', str(account_id)))
    print('')
    print(it('cyan', 'CONNECTING to DEX market...'))
    time.sleep(0.2)
    print('')
    print('   You are Trading: ', it('green', pair))
    print('')
    sign_in()
    time.sleep(0.3)
    print(it('cyan', 'LAUNCHING microDEX user interface...'))
    print(it('blue', '''
    ===================================================================
          '''))
    print(it('cyan', '           ' + time.ctime()))
    print(it('blue', '''
    ===================================================================
          '''))
    print('')


def check_version():
    # check github for latest microDEX version
    latest_version = ascii_logo('version')
    latest = latest_version.split(maxsplit=21)[:20]
    for j in latest:
        try:
            latest = float("".join(i for i in j if i in "0123456789."))
            break
        except:
            pass
    current = float("".join(i for i in VERSION if i in "0123456789."))
    if latest > current:
        print(it('red', '      WARN: NEW VERSION AVAILABLE!'))
        print(it('yellow',
                 '      github/litepresence/extinction-event/EV'))
        choice = ''
        while choice.lower() not in ['y', 'n']:
            choice = input('      Y/N UPGRADE?  ')
        if choice == 'y':
            # backup and overwrite microDEX.py
            current_version = race_read('metaNODE.py')
            backup = 'microDEX' + ('%.8f' % current) + '.py'
            race_write(backup, current_version)
            race_write('microDEX.py', latest_version)
            sys.exit('microDEX version updated please RESTART')
    else:
        print('      This is the latest microDEX version.')
    print('')
    print(it('cyan', 'AFFIRMING system for compatibility...'))
    # confirm python 3 and linux OS
    if 'linux' not in platform:
        raise Exception('not a linux box, format drive and try again...')
    if version_info[0] < 3:
        raise Exception("% is DED, long live Python 3.4+" % version_info[0])
    print('')
    print('      found python', version_info[0], 'running on', platform)
    print('')
    time.sleep(0.2)


def cache():

    global asset, currency, asset_precision, currency_precision
    global pair, ap, cp, account_name, account_id, nodes
    metaNODE = Bitshares_Trustless_Client()
    currency_precision = metaNODE['currency_precision']
    asset_precision = metaNODE['asset_precision']
    account_name = metaNODE['account_name']
    account_id = metaNODE['account_id']
    currency = metaNODE['currency']
    nodes = metaNODE['whitelist']
    asset = metaNODE['asset']
    del metaNODE
    # create dynamic format styles: "%.4f" etc. based on "precision"
    ap = '%.' + str(int(asset_precision / 2.0)) + 'f'
    cp = '%.' + str(int(currency_precision / 2.0)) + 'f'
    pair = asset + ':' + currency


def sign_in():
    global authenticated, wif
    print(it('yellow',
             ' Enter WIF below to AUTHENTICATE or press ENTER to skip'))
    print(it('red',
             ' YOU SHOULD UNDERSTAND THE SCRIPT BEFORE AUTHENTICATING'))
    print('')
    authenticated = False
    while not authenticated:
        try:
            wif = getpass(prompt='               wif: ')
            print("\033[F              wif: " + it('green',
                  '********************************'))
            if wif:
                print('')
                print(it('cyan', 'AUTHENTICATING to DEX wallet...'))
                try:
                    log_in()
                except Exception as e:
                    print(trace(e))
                    pass
                if authenticated:
                    print('')
                    print(it('red', '*****************'))
                    print(it('red', '**AUTHENTICATED**') +
                          it('yellow', ' YOUR WALLET IS UNLOCKED'))
                    print(it('red', '*****************'))
                    break
                else:
                    print(it('yellow', 'WIF does NOT match account'))
            else:
                print('')
                print(it('yellow', 'SKIP AUTH - WALLET LOCKED'))
                break
        except Exception as e:
            print(trace(e))
            pass

# TKINTER GUI
# ======================================================================


def tk_master():

    global master, wif_entry
    global header_text, bid_text, ask_text
    global history_text, orders_text, account_text
    global buy_price, buy_amount, sell_price, sell_amount
    global lock_label

    master = tk.Tk()
    master['bg'] = '#262626'
    master.title(VERSION)
    header_text = tk.Text(
        master,
        height=5,
        width=90,
        fg=blue1,
        bg=gray3,
        wrap=tk.NONE)
    header_text.insert(tk.END, '')
    header_text.grid(row=0, column=0, columnspan=4)
    bid_text = tk.Text(
        master,
        height=30,
        width=45,
        fg=green1,
        bg=gray3,
        wrap=tk.NONE)
    bid_text.insert(tk.END, '')
    bid_text.grid(row=1, column=0, columnspan=2)
    bid_text.tag_configure("right", justify="right")
    bid_text.tag_configure("left", justify="left")
    ask_text = tk.Text(
        master,
        height=30,
        width=45,
        fg=red1,
        bg=gray3,
        wrap=tk.NONE)
    ask_text.insert(tk.END, '')
    ask_text.grid(row=1, column=2, columnspan=2)
    orders_text = tk.Text(
        master,
        height=11,
        width=45,
        fg=yellow1,
        bg=gray3,
        wrap=tk.NONE)
    orders_text.insert(tk.END, '')
    orders_text.grid(row=2, column=0, columnspan=2)
    history_text = tk.Text(
        master,
        height=11,
        width=45,
        fg=gray1,
        bg=gray3, wrap=tk.NONE)
    history_text.insert(tk.END, '')
    history_text.grid(row=2, column=2, columnspan=2)
    account_text = tk.Text(
        master,
        height=4,
        width=90,
        fg=blue1,
        bg=gray3,
        wrap=tk.NONE)
    account_text.insert(tk.END, '')
    account_text.grid(row=3, columnspan=4)
    tk.Label(
        master,
        text="PRICE:",
        fg=gray1,
        bg=gray3).grid(
        row=4,
        column=0,
        sticky=tk.E)
    tk.Label(
        master,
        text="AMOUNT:",
        fg=gray1,
        bg=gray3).grid(
        row=5,
        column=0,
        sticky=tk.E)
    tk.Label(
        master,
        text="PRICE:",
        fg=gray1,
        bg=gray3).grid(
        row=4,
        column=2,
        sticky=tk.E)
    tk.Label(
        master,
        text="AMOUNT:",
        fg=gray1,
        bg=gray3).grid(
        row=5,
        column=2,
        sticky=tk.E)
    tk.Label(
        master,
        text="litepresence2019",
        fg=gray2,
        bg=gray3).grid(
        row=9,
        column=3,
        sticky=tk.SE)
    lock_label = tk.StringVar()
    lock_label.set('')
    tk.Label(
        master,
        textvariable=lock_label,
        fg=yellow1,
        bg=gray3).grid(
        row=8,
        column=2,
        sticky=tk.W)
    tk.Label(master,
             text=("   *ORDERS TAKE A FEW SECONDS TO APPEAR; " +
                   "CLICK ONCE, THEN CONFIRM*"),
             fg='#C0C0C0', bg='#262626'
             ).grid(row=9, column=0, columnspan=4, sticky=tk.W)
    try:
        try:
            photo = tk.PhotoImage(file="bitshares_logo.gif")
        except:
            download_img(
                'https://i.imgur.com/fvCE86Z.gif',
                'bitshares_logo.gif')
            photo = tk.PhotoImage(file="bitshares_logo.gif")
        label = tk.Label(image=photo)
        label.image = photo
        label.grid(row=0, column=3, sticky=tk.E)
    except:
        pass
    buy_price = tk.Entry(master, fg=gray1, bg=gray2)
    buy_amount = tk.Entry(master, fg=gray1, bg=gray2)
    sell_price = tk.Entry(master, fg=gray1, bg=gray2)
    sell_amount = tk.Entry(master, fg=gray1, bg=gray2)
    wif_entry = tk.Entry(master, fg=gray1, bg=gray2)
    buy_price.grid(row=4, column=1)
    buy_amount.grid(row=5, column=1)
    sell_price.grid(row=4, column=3)
    sell_amount.grid(row=5, column=3)
    wif_entry.grid(row=8, column=1)
    tk.Button(
        master,
        text='BUY',
        command=tk_buy,
        fg=gray1,
        bg=gray3,
        activebackground=green2,
        highlightbackground=green1).grid(
        row=7,
        column=1,
        pady=4)
    tk.Button(
        master,
        text='SELL',
        command=tk_sell,
        fg=gray1,
        bg=gray3,
        activebackground=red2,
        highlightbackground=red1).grid(
        row=7,
        column=3,
        pady=4)
    tk.Button(
        master,
        text='CANCEL ALL',
        command=tk_cancel,
        fg=gray1,
        bg=gray3,
        activebackground=yellow2,
        highlightbackground=yellow1).grid(
        row=7,
        column=0,
        sticky=tk.E,
        pady=4)
    tk.Button(
        master,
        text='LOCK/UNLOCK',
        command=tk_authenticate,
        fg=gray1,
        bg=gray3,
        activebackground=blue2,
        highlightbackground=blue1).grid(
        row=8,
        column=0,
        sticky=tk.E,
        pady=4)
    master.geometry('+9999+9999')
    master.after(0, tk_animate)
    master.mainloop()


def tk_animate():

    global update_id, last, node_scroll, read_times
    global asset_total, currency_total, asset_value, currency_value
    global buy_orders, sell_orders, invested, divested
    global asset_balance, currency_balance, bts_balance
    global blocktime, last, orders, history, book, latency, slast
    global buy_orders, sell_orders, invested, divested, ping
    global asset_total, currency_total, asset_value, currency_value
    global sbidp, saskp, sbidv, saskv
    global cbidp, caskp, cbidv, caskv
    global last_refresh, ui_refreshes, pings, latencies, ui_delta
    global lock_label

    if update_id == 0:
        node_scroll = ''
        last_refresh = time.time()
        ui_refreshes = []
        pings = []
        latencies = []
        read_times = []
        ui_delta = 0

    # keep moving average of UI_REFRESH timing
    now = time.time()
    ui_refreshes.append(now - last_refresh)
    ui_refreshes = ui_refreshes[-20:]
    ui_refresh = sum(ui_refreshes) / len(ui_refreshes)
    last_refresh = now

    while True:
        try:
            # open metaNODE and note how long it took
            start = time.time()
            metaNODE = Bitshares_Trustless_Client()
            read_times.append(time.time() - start)
            read_times = read_times[-40:]
            read_time = sum(read_times) / len(read_times)
            # localize metaNODE data
            whitelist = metaNODE['whitelist']
            blocktime = metaNODE['blocktime']
            last = metaNODE['last']
            orders = metaNODE['orders']
            currency_balance = metaNODE['currency_balance']
            asset_balance = metaNODE['asset_balance']
            bts_balance = metaNODE['bts_balance']
            history = metaNODE['history']
            book = metaNODE['book']
            buy_orders = metaNODE['buy_orders']
            sell_orders = metaNODE['sell_orders']
            invested = metaNODE['invested']
            divested = metaNODE['divested']
            ping = metaNODE['ping']
            pings.append(ping)
            pings = pings[-20:]
            ping = sum(pings) / len(pings)
            # metaNODE dict is large, best to delete object when done
            del metaNODE
            # build scrolling whitelisted websocket display
            while len(node_scroll) < 100:
                node_scroll += ('   ' + choice(
                    whitelist).replace(
                    'wss://',
                    '').replace('/wss',
                                '').replace('/ws',
                                            '').split('/')[0].split(':')[0])
                words = node_scroll.split()
                node_scroll = (
                    "   ".join(sorted(set(words), key=words.index)))
            node_scroll = node_scroll[1:]
            # limit size of orders object to keys needed
            for i in range(len(orders)):
                orders[i] = {k: v for k, v in orders[
                    i].items() if k in ['price', 'orderType', 'amount']}
            asset_total = (asset_balance + sell_orders)
            currency_total = (currency_balance + buy_orders)
            asset_value = asset_total + currency_total / last
            currency_value = asset_value * last
            # limit history depth
            history = history[:10]
            slast = '%.16f' % last
            latency = time.time() - blocktime + time.timezone
            latencies.append(latency)
            latencies = latencies[-20:]
            latency = sum(latencies) / len(latencies)
            # stringified volume
            sbidp = [(' %.16f ' % i).rjust(20, ' ') for i in book['bidp']]
            saskp = [(' %.16f ' % i).ljust(20, ' ') for i in book['askp']]
            sbidv = [(' %.2f ' % i).rjust(12, ' ') for i in book['bidv']]
            saskv = [(' %.2f ' % i).rjust(12, ' ') for i in book['askv']]
            # stringified cumulative volume
            cbidv = list(np.cumsum(book['bidv']))
            caskv = list(np.cumsum(book['askv']))
            cbidv = [(' %.2f ' % i).rjust(12, ' ') for i in cbidv]
            caskv = [(' %.2f ' % i).rjust(12, ' ') for i in caskv]
            depth = 30
            sbidp = sbidp[:depth]
            saskp = saskp[:depth]
            sbidv = sbidv[:depth]
            saskv = saskv[:depth]
            cbidv = cbidv[:depth]
            caskv = caskv[:depth]
            del book  # eliminate book after data extraction
            runtime = str(int(time.time()) - BEGIN)
            break
        except Exception as e:
            continue
    # rebuild tkinter text fields with updated data
    header_text.delete("1.0", "end")
    header_text.insert(tk.END, (
        ('        ' + time.ctime() +
                      ('                LAST %s' % slast) +
         '\n\n')
    ))
    header_text.insert(tk.END, (node_scroll[:90] + '\n\n'))
    header_text.insert(tk.END, (
        ('       UI %.4f' % ui_refresh) +
        ('    PING %.3f' % ping) +
        ('    READ %.5f' % read_time) +
        ('    DATA %s' % ('%.1f' % latency).ljust(4)) +
        ('   RUN %s' % runtime)
    ))
    bid_text.delete("1.0", "end")
    ask_text.delete("1.0", "end")
    for i in range(len(saskp)):
        ask_text.insert(tk.END, (saskp[i] + saskv[i] + caskv[i] + '\n'))
        bid_text.insert(
            tk.END,
            (cbidv[i] + sbidv[i] + sbidp[i] + '\n'),
            'right')
    history_text.delete("1.0", "end")
    history_text.insert(
        tk.END,
        (' ' + str(int(time.time())) + ' LAST TRADE ' +
         str(int(time.time() - history[0][0] + time.timezone)) + '\n'))
    for i in range(len(history)):
        history_text.insert(
            tk.END,
            (' ' + str(history[i][0]) + ' ' +
             str(history[i][1]) + ' ' +
             str(history[i][2]) + ' ' + '\n'))
    orders_text.delete("1.0", "end")
    if len(orders):
        orders_text.insert(tk.END, ' OPEN ORDERS IN ' + pair + '\n')
        for i in range(len(orders)):
            orders_text.insert(
                tk.END,
                (' ' + str(orders[i]['price']) + ' ' +
                 str(orders[i]['orderType']).ljust(4, ' ') + ' ' +
                 str(orders[i]['amount']) + '\n'))
    else:
        orders_text.insert(tk.END, ('\n NO OPEN ORDERS IN ' + pair))
    account_text.delete("1.0", "end")
    account_text.insert(tk.END, ' ASSETS: ' +
                        (ap % asset_balance).rjust(12, ' ') +
                        '         CURRENCY: ' +
                        (cp % currency_balance).rjust(12, ' ') +
                        '                BITSHARES: ' +
                        ('%.2f' % bts_balance) + '\n')
    account_text.insert(tk.END, ' ORDERS: ' +
                       (ap % sell_orders).rjust(12, ' ') +
                        '                   ' +
                       (cp % buy_orders).rjust(12, ' ') + '\n')
    account_text.insert(tk.END, '  TOTAL: ' +
                       (ap % asset_total).rjust(12, ' ') +
                        ' ' + (str(invested) + ' %').ljust(7, ' ') +
                        '           ' +
                       (cp % currency_total).rjust(12, ' ') +
                        ' ' + str(divested).ljust(5, ' ') + ' %\n')
    account_text.insert(tk.END, '    MAX: ' +
                       (ap % asset_value).rjust(12, ' ') + ' ' +
                        asset.ljust(10, ' ') +
                        '        ' +
                       (cp % currency_value).rjust(12, ' ') + ' ' +
                        currency.ljust(10, ' '))
    # destroy and recreate lock label

    lock_label.set('WALLET LOCKED')
    if authenticated:
        lock_label.set('AUTHENTICATED')

    # update id increment
    if update_id == 0:
        account_state()
        print(it('cyan', '\n          ctrl+shft+\\ to EXIT microDEX \n'))
    update_id += 1
    # set perfect UI_REFRESH timing
    if float('%.4f' % ui_refresh) < (UI_REFRESH):
        ui_delta += 0.000005
    if float('%.4f' % ui_refresh) > (UI_REFRESH):
        ui_delta -= 0.000005
    pause = int(1000 *
                min(UI_REFRESH, (
                    max(0.001, (
                        2 * UI_REFRESH - ui_refresh + ui_delta)))))
    master.after(pause, tk_animate)


def tk_authenticate():

    # unlock wallet from gui
    global wif_entry, wif, authenticated
    wif = str(wif_entry.get())
    wif_entry.delete(0, tk.END)
    print(it('blue', 'LOCK/UNLOCK WALLET'))
    authenticated = False
    if wif:
        try:
            log_in()
        except:
            pass
    if authenticated:
        print(it('red', '*****************'))
        print(it('red', '**AUTHENTICATED**'))
        print(it('red', '*****************'))
    else:
        wif = ''
        print(it('yellow', 'WALLET IS LOCKED'))


def tk_buy():

    global confirm
    print(it('green', '*** BUY ***'))
    metaNODE = Bitshares_Trustless_Client()
    currency = metaNODE['currency']
    asset = metaNODE['asset']
    currency_balance = decimal(metaNODE['currency_balance'])
    del metaNODE
    # interact with tkinter
    confirm = tk.Tk()
    if authenticated:
        #
        # gather the price and amount from tkinter gui
        price = buy_price.get()
        amount = buy_amount.get()
        try:
            if price == '':
                raise ValueError('No Price Specified')
            if amount == '':
                raise ValueError('No Amount Specified')
            # convert pricing to ultra precision decimal
            price = decimal(price)
            # convert amounts to decimal; should already be
            amount = decimal(amount)
            # do not spend your last bitshare
            if currency == 'BTS':
                currency_balance -= 2
            # limit buy amount to means given currency in hand and price
            means = SIXSIG * currency_balance / decimal(price)
            if amount > means:
                amount = means
            #
            sprice = str(price)[:16]
            samount = str(amount)[:16]
            sorder = str(
                'CONFIRM BUY ' +
                samount +
                ' ' +
                asset +
                ' @ ' +
                sprice)
            if amount > 0:
                confirm.title(sorder)
                print(it('yellow', 'CONFIRM BUY?'))
                tk.Button(
                    confirm,
                    text='CONFIRM BUY',
                    command=lambda: buy(price, amount)).grid(
                    row=1,
                    column=0,
                    pady=8)
                tk.Button(
                    confirm,
                    text='INVALIDATE',
                    command=lambda: tk_invalidate(confirm)).grid(
                    row=2,
                    column=0,
                    pady=8)
            else:
                confirm.title('NO CURRENCY TO BUY')
                print(it('yellow', 'NO CURRENCY TO BUY'))
                tk.Button(
                    confirm,
                    text='OK',
                    command=confirm.destroy).grid(
                    row=2,
                    column=0,
                    pady=8)
        except Exception as e:
            msg = str(type(e).__name__) + str(e.args)
            print(msg)
            if str(type(e).__name__) == 'NumRetriesReached()':
                confirm.title('LOST CONNECTION, TRY AGAIN')
                print(it('yellow', 'LOST CONNECTION, TRY AGAIN'))
            else:
                confirm.title('INVALID BUY ORDER')
                print(it('yellow', 'INVALID BUY ORDER'))
            tk.Button(
                confirm,
                text='OK',
                command=confirm.destroy).grid(
                row=2,
                column=0,
                pady=8)
        confirm.geometry('500x100+800+175')
        confirm.lift()
        confirm.call('wm', 'attributes', '.', '-topmost', True)
    else:
        confirm.title('YOUR WALLET IS LOCKED')
        print(it('yellow', 'YOUR WALLET IS LOCKED'))
        tk.Button(
            confirm,
            text='OK',
            command=confirm.destroy).grid(
            row=2,
            column=0,
            pady=8)
    confirm.geometry('500x100+800+175')
    confirm.lift()
    confirm.call('wm', 'attributes', '.', '-topmost', True)


def tk_sell():

    global confirm
    print(it('red', '*** SELL ***'))
    metaNODE = Bitshares_Trustless_Client()
    bts_balance = decimal(metaNODE['bts_balance'])
    asset_balance = decimal(metaNODE['asset_balance'])
    asset = metaNODE['asset']
    del metaNODE
    # interact with tkinter confirm sell widget
    confirm = tk.Tk()
    if authenticated:
        price = sell_price.get()
        amount = sell_amount.get()
        # retain the last bitshare
        try:
            if price == '':
                raise ValueError('No Price Specified')
            if amount == '':
                raise ValueError('No Amount Specified')
            if asset == 'BTS':
                asset_balance -= 2
            price = decimal(price)
            amount = decimal(amount)
            if amount > (SIXSIG * asset_balance):
                amount = SIXSIG * asset_balance
            sprice = str(price)[:16]
            samount = str(amount)[:16]
            sorder = str(
                'CONFIRM SELL ' +
                samount +
                ' ' +
                asset +
                ' @ ' +
                sprice)
            if amount > 0:
                confirm.title(sorder)
                print(it('yellow', 'CONFIRM SELL?'))
                tk.Button(
                    confirm,
                    text='CONFIRM SELL',
                    command=lambda: sell(price, amount)).grid(
                    row=1,
                    column=0,
                    pady=8)
                tk.Button(
                    confirm,
                    text='INVALIDATE',
                    command=lambda: tk_invalidate(confirm)).grid(
                    row=2,
                    column=0,
                    pady=8)
            else:
                confirm.title('NO ASSETS TO SELL')
                print(it('yellow', 'NO ASSETS TO SELL'))
                tk.Button(
                    confirm,
                    text='OK',
                    command=confirm.destroy).grid(
                    row=2,
                    column=0,
                    pady=8)
        except Exception as e:
            msg = str(type(e).__name__) + str(e.args)
            print(msg)
            if str(type(e).__name__) == 'NumRetriesReached()':
                confirm.title('LOST CONNECTION, TRY AGAIN')
                print(it('yellow', 'LOST CONNECTION, TRY AGAIN'))
            confirm.title('INVALID SELL ORDER')
            print(it('yellow', 'INVALID SELL ORDER'))
            tk.Button(
                confirm,
                text='OK',
                command=confirm.destroy).grid(
                row=2,
                column=0,
                pady=8)
    else:
        confirm.title('YOUR WALLET IS LOCKED')
        print(it('yellow', 'YOUR WALLET IS LOCKED'))
        tk.Button(
            confirm,
            text='OK',
            command=confirm.destroy).grid(
            row=2,
            column=0,
            pady=8)
    confirm.geometry('500x100+800+175')
    confirm.lift()
    confirm.call('wm', 'attributes', '.', '-topmost', True)


def tk_cancel():

    global confirm
    print(it('blue', '*** CANCEL ***'))
    metaNODE = Bitshares_Trustless_Client()
    orders = metaNODE['orders']
    del metaNODE
    # interact with tkinter
    confirm = tk.Tk()
    if len(orders):
        if authenticated:
            if len(orders) > 1:
                title = str(len(orders)) + ' ORDERS TO CANCEL'
            else:
                title = str(len(orders)) + ' ORDER TO CANCEL'
            confirm.title(title)
            print(it('yellow', 'CONFIRM?'))
            tk.Button(
                confirm,
                text='CONFIRM CANCEL ALL',
                command=cancel).grid(  # lambda: cancel(market)).grid(
                row=1,
                column=0,
                pady=8)
            tk.Button(
                confirm,
                text='INVALIDATE',
                command=lambda: tk_invalidate(confirm)).grid(
                row=2,
                column=0,
                pady=8)
            confirm.geometry('500x100+800+175')
            confirm.lift()
            confirm.call('wm', 'attributes', '.', '-topmost', True)
        else:
            confirm.title('YOUR WALLET IS LOCKED')
            print(it('yellow', 'YOUR WALLET IS LOCKED'))
            tk.Button(
                confirm,
                text='OK',
                command=confirm.destroy).grid(
                row=2,
                column=0,
                pady=8)
    else:
        confirm.title('NO OUTSTANDING ORDERS')
        print(it('yellow', 'NO OUTSTANDING ORDERS'))
        tk.Button(
            confirm,
            text='OK',
            command=confirm.destroy).grid(
            row=2,
            column=0,
            pady=8)
    confirm.geometry('500x100+800+175')
    confirm.lift()
    confirm.call('wm', 'attributes', '.', '-topmost', True)


def tk_invalidate(confirm):

    confirm.destroy()
    print(it('blue', 'MANUALLY INVALIDATED'))

# MAIN
# ======================================================================


def main():

    initialize()
    tk_master()


if __name__ == "__main__":

    main()
