
' microDEX '

# Low latency UI for Bitshares Decentralized Exchange

' litepresence 2018 '

def WTFPL_v0_March_1765():
    if any([stamps, licenses, taxation, regulation, fiat, etat]):
        try:
            print('no thank you')
        except:
            return [tar, feathers]

import os
import sys
import time
import json
import warnings
import requests
import datetime
import traceback
tz = time.timezone
import numpy as np
from tkinter import *
from getpass import getpass
from datetime import datetime
import matplotlib.ticker as tkr
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from random import random, shuffle
from decimal import Decimal as decimal
from ast import literal_eval as literal
from multiprocessing import Process, Value, Array
# warnings.simplefilter(action='ignore', category=FutureWarning)

# Google Agorism
from bitshares import BitShares
from bitshares.market import Market
from bitshares.account import Account
from bitshares.blockchain import Blockchain
# bitshares.org/technology/industrial-performance-and-scalability/

PAUSE = 0.5
COLOR = True

def version():

    global VERSION

    VERSION = 'v0.00000016'

    sys.stdout.write(
        '\x1b]2;' +
        'Bitshares microDEX' +
        '\x07')  # terminal #title

def Bitshares_Trustless_Client():  # Your access to the metaNODE
    # Include this definition in your script to access metaNODE.txt
    # Deploy your bot script in the same folder as metaNODE.py
    i = 0
    while True:
        time.sleep(0.05 * i ** 2)
        i += 1
        try:
            with open('metaNODE.txt', 'r') as f:
                ret = f.read()  # .replace("'",'"')
                f.close()
                metaNODE = json.loads(ret)
                break
        except Exception as e:
            msg = str(type(e).__name__) + str(e.args)
            if DEV:
                msg += str(traceback.format_exc())
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
    return metaNODE

def red(text):
    return ('\033[91m' + text + '\033[0m') if COLOR else text

def green(text):
    return ('\033[92m' + text + '\033[0m') if COLOR else text

def yellow(text):
    return ('\033[93m' + text + '\033[0m') if COLOR else text

def blue(text):
    return ('\033[94m' + text + '\033[0m') if COLOR else text

def purple(text):
    return ('\033[95m' + text + '\033[0m') if COLOR else text

def cyan(text):
    return ('\033[96m' + text + '\033[0m') if COLOR else text

def constants():

    global BitCURRENCY, BitASSET, BitPAIR
    global ID, SATOSHI, ANTISAT, nodes

    # default market
    BitCURRENCY = 'OPEN.BTC'
    BitASSET = 'BTS'
    BitPAIR = BitASSET + ':' + BitCURRENCY
    # mainnet ID
    ID = '4018d7844c78f6a6c41c6a552b898022310fc5dec06da467ee7905a8dad512c8'
    SATOSHI = 0.00000001
    ANTISAT = 1 / SATOSHI
    # seed nodes for first use; auto updates thereafter

    nodes = race_read(doc='nodes.txt')

def msg_(e):  # traceback message
    return (str(type(e).__name__) + str(e.args) + str(e) +
            str(traceback.format_exc()) + str(sys.exc_info()))

def race_write(doc='', text=''):  # Concurrent Write to File Operation

    opened = 0
    while not opened:
        try:
            with open(doc, 'w+') as f:
                f.write(str(text))
                opened = 1
        except Exception as e:
                msg = msg_(e)
                race_append(doc='microDEX_log.txt', text=msg)
                pass

def race_append(doc='', text=''):  # Concurrent Append to File Operation

    text = '\n' + str(time.ctime()) + ' ' + str(text) + '\n'
    opened = 0
    while not opened:
        try:
            with open(doc, 'a+') as f:

                f.write(str(text))
                opened = 1
        except Exception as e:
                msg = msg_(e)
                race_append(doc='microDEX_log.txt', text=msg)
                pass

def race_read(doc=''):  # Concurrent Read from File Operation

    opened = 0
    while not opened:
        try:
            with open(doc, 'r') as f:
                #ret = json.loads(f.read())
                ret = literal(f.read())
                opened = 1
        except Exception as e:
            msg = msg_(e)
            race_append(doc='microDEX_log.txt', text=msg)
            pass
    return ret

def zprint(z):  # prints 10X to flash orderbook
    OFFSET = '                                                      '
    z = '\n\n' + OFFSET + str(z)
    for i in range(10):
        time.sleep(0.03)
        print("\033c")
        for i in range(50):
            print(z)

def reconnect(BitPAIR, USERNAME, PASS_PHRASE):

    # create fresh websocket connection
    connected = 0
    while not connected:
        # fetch fresh nodes list from subprocess and shuffle it
        nds = race_read('nodes.txt')
        if isinstance(nds, list):
            nodes = nds
        shuffle(nodes)
        node = nodes[0]
        try:
            account = Account(USERNAME,
                              bitshares_instance=BitShares(node,
                                                           num_retries=0))
            market = Market(BitPAIR,
                            bitshares_instance=BitShares(node,
                                                         num_retries=0),
                            mode='head')
            chain = Blockchain(
                bitshares_instance=BitShares(node, num_retries=0), mode='head')
            if chain.get_network()['chain_id'] != ID:
                raise ValueError('Not Mainnet Chain')
            connected = 1
        except:
            pass
    try:
        market.bitshares.wallet.unlock(PASS_PHRASE)
    except:
        pass
    return account, market, nodes, chain

def book():  # updates orderbook data

    account, market, nodes, chain = reconnect(BitPAIR, USERNAME, PASS_PHRASE)
    node = nodes[0]
    begin = time.time()

    while True:
        try:
            time.sleep(PAUSE)
            metaNODE = Bitshares_Trustless_Client()

            start = time.time()
            chain.get_network()['chain_id']
            ping = time.time() - start
            if ping > 2:
                raise ValueError('SLOW PING')
            # localize metaNODE data
            node = metaNODE['whitelist'][0]
            blocktime = metaNODE['blocktime']
            last = metaNODE['last']
            orders = metaNODE['orders']
            currency_balance = metaNODE['currency_balance']
            asset_balance = metaNODE['asset_balance']
            bts_balance = metaNODE['bts_balance']
            currency = metaNODE['currency']
            asset = metaNODE['asset']
            history = metaNODE['history']
            book = metaNODE['book']
            buy_orders = metaNODE['buy_orders']
            sell_orders = metaNODE['sell_orders']

            asset_total = (asset_balance + sell_orders)
            currency_total = (currency_balance + buy_orders)
            asset_value = asset_total + currency_total / last
            currency_value = asset_value * last

            # format data
            history = history[:10]

            # for i in range(len(history)):
            # history[0][0] = history[0][0] - time.timezone

            slast = '%.16f' % last
            latency = '%.3f' % (time.time() - blocktime + time.timezone)
            sbidp = [('%.16f' % i) for i in book['bidp']]
            saskp = [('%.16f' % i) for i in book['askp']]
            sbidv = [('%.2f' % i).rjust(12, ' ') for i in book['bidv']]
            saskv = [('%.2f' % i).rjust(12, ' ') for i in book['askv']]
            cbidv = list(np.cumsum(book['bidv']))
            caskv = list(np.cumsum(book['askv']))
            cbidv = [('%.2f' % i).rjust(12, ' ') for i in cbidv]
            caskv = [('%.2f' % i).rjust(12, ' ') for i in caskv]

            depth = 30
            sbidp = sbidp[:depth]
            saskp = saskp[:depth]
            sbidv = sbidv[:depth]
            saskv = saskv[:depth]
            cbidv = cbidv[:depth]
            caskv = caskv[:depth]

            # display orderbooks
            print("\033c")
            print(cyan(time.ctime()),
                  blue('    microDEX - Bishares Minimalist UI    '),
                  'RUN TIME', cyan(str(int(time.time()) - BEGIN)),
                  '     ', blue(VERSION))
            # for k, v in metaNODE.items():
            #    print(k)
            print('')
            print('                        PING', cyan('%.3f' % ping),
                  '   ', 'BLOCK LATENCY', cyan(latency), '   ', purple(node))
            print('')
            print(
                yellow('                        LAST'),
                yellow(slast[:10] + ',' + slast[10:]),
                '   ',
                yellow(BitPAIR))
            print('')
            print('            ', purple(sbidv[0]), '  ',
                  purple((sbidp[0])[:10] + ',' + (sbidp[0])[10:]),
                  '   ',
                  purple((saskp[0])[:10] + ',' + (saskp[0])[10:]),
                  purple(saskv[0]))
            print('                                           ',
                  'BIDS',
                  '   ',
                  'ASKS')
            for i in range(1, len(sbidp)):
                print(
                    green(cbidv[i]), green(sbidv[i]), '  ',
                    green((sbidp[i])[:10] + ',' + (sbidp[i])[10:]),
                    '   ',
                    red((saskp[i])[:10] + ',' + (saskp[i])[10:]),
                    red(saskv[i]), red(caskv[i]))
            print('')

            # display orders, holdings, and market history
            for o in orders:
                print (yellow(str(o)))
            if len(orders) == 0:
                print (
                    yellow('                                  NO OPEN ORDERS'))

            print('')
            print (
                blue(
                    ' ASSETS: '), ('%.4f' %
                                   asset_balance).rjust(12, ' '), '          ',
                blue(
                    '  CURRENCY: '), ('%.4f' %
                                      currency_balance).rjust(12, ' '),
                blue('             BITSHARES: '), bts_balance)
            print(blue(' ORDERS: '), ('%.4f' % sell_orders).rjust(12, ' '),
                  '                       ', ('%.4f' % buy_orders).rjust(12, ' '))
            print(
                blue('  TOTAL: '), purple(('%.4f' %
                (asset_total)).rjust(12, ' ')),
                '                       ',
                purple(('%.4f' % (currency_total)).rjust(12, ' ')))
            print(
                blue('    MAX: '),
                green(('%.4f' % (asset_value)).rjust(12, ' ')),
                yellow(asset.ljust(10, ' ')), '            ',
                green(('%.4f' % (currency_value)).rjust(12, ' ')),
                yellow(currency.ljust(10, ' ')))
            print('')
            now = int(time.time())
            print(
                cyan(str(now)),
                yellow('MARKET HISTORY - LAST TRADE '),
                cyan(str(now - (history[0][0] - tz))))  # , stale, 'since last trade')
            for transaction in history:
                print ((transaction[0] - tz), transaction[1], transaction[2])

            print('')
            print(blue('ctrl+shift+\ will EXIT to terminal'))
            print('')

        except Exception as e:
            msg = msg_(e)
            msg += (' BOOK FAILED, RECONNECTING ' + str(node))
            race_append(doc='microDEX_log.txt', text=msg)
            account, market, nodes, chain = reconnect(
                BitPAIR, USERNAME, PASS_PHRASE)
            pass

def dex_buy():

    # update wallet unlock to low latency node
    zprint('BUY')
    account, market, nodes, chain = reconnect(BitPAIR, USERNAME, PASS_PHRASE)
    # attempt buy 10X or until satisfied

    def buy(price, amount, market):
        confirm.destroy()
        zprint('CONFIRMED')
        attempt = 1
        while attempt:
            try:
                msg = market.buy(price, amount)
                msg = (' BUY ' + str(amount) + ' of ' + str(BitPAIR) +
                       ' @ ' + str(price) + '\n' + str(msg))
                print (msg)
                attempt = 0
            except Exception as e:
                msg = msg_(e)
                race_append(doc='microDEX_log.txt', text=msg)
                msg += (+ str(attempt) + ' ' + ' BUY FAILED, RECONNECTING '
                        + str(nodes[0]) + ' ' + str(price) + ' ' + str(amount))
                zprint(' BUY FAILED, RECONNECTING ')
                race_append(doc='microDEX_log.txt', text=msg)
                account, market, nodes, chain = reconnect(
                    BitPAIR, USERNAME, PASS_PHRASE)
                attempt += 1
                if attempt > 10:
                    zprint('BUY ABORTED')
                    return
                pass
        race_append(doc='microDEX_log.txt', text=msg)

    # interact with tkinter
    confirm = Tk()
    if market.bitshares.wallet.unlocked():

        #
        # gather the price and amount from tkinter gui
        price = buy_price.get()
        amount = buy_amount.get()
        # if no price was specified, market buy 10% over last
        if price == '':
            price = 1.1 * float(market.ticker()['latest'])
        # if no amount is specified, attempt near infinity
        if amount == '':
            amount = ANTISAT
        try:
            # convert pricing to ultra precision decimal
            price = decimal(price)
            # convert amounts to float; should already be
            amount = float(amount)
            # consider how much buying power we actually hold
            currency = float(account.balance(BitCURRENCY))
            # limit buy amount to means given currency in hand and price
            means = 0.998 * currency / float(price)
            if amount > means:
                amount = means
            #
            sprice = str(price)[:16]
            samount = str(amount)[:16]
            sorder = str(
                'CONFIRM BUY ' +
                samount +
                ' ' +
                BitASSET +
                ' @ ' +
                sprice)
            if amount > 0:
                confirm.title(sorder)
                Button(
                    confirm,
                    text='CONFIRM BUY',
                    command=lambda: buy(price, amount, market)).grid(
                    row=1,
                    column=0,
                    pady=8)
                Button(
                    confirm,
                    text='INVALIDATE',
                    command=confirm.destroy).grid(
                    row=2,
                    column=0,
                    pady=8)
            else:
                confirm.title('NO CURRENCY TO BUY')
                Button(
                    confirm,
                    text='OK',
                    command=confirm.destroy).grid(
                    row=2,
                    column=0,
                    pady=8)
        except:
            confirm.title('INVALID BUY ORDER')
            Button(
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
        Button(
            confirm,
            text='OK',
            command=confirm.destroy).grid(
            row=2,
            column=0,
            pady=8)
    confirm.geometry('500x100+800+175')
    confirm.lift()
    confirm.call('wm', 'attributes', '.', '-topmost', True)

def dex_sell():

    # update wallet unlock to low latency node
    zprint('SELL')
    account, market, nodes, chain = reconnect(
        BitPAIR, USERNAME, PASS_PHRASE)
    # attempt to sell 10X or until satisfied

    def sell(price, amount, market):
        confirm.destroy()
        zprint('CONFIRMED')
        attempt = 1
        while attempt:
            try:
                msg = market.sell(price, amount)
                msg = (' SELL ' + str(amount) + ' of ' + str(BitPAIR) +
                       ' @ ' + str(price) + '\n' + str(msg))
                print (msg)
                attempt = 0
            except Exception as e:
                msg = msg_(e)
                race_append(doc='microDEX_log.txt', text=msg)
                msg += (+ str(attempt) + ' ' + ' SELL FAILED, RECONNECTING '
                        + str(nodes[0]) + ' ' + str(price) + ' ' + str(amount))
                zprint(' SELL FAILED, RECONNECTING ')
                race_append(doc='microDEX_log.txt', text=msg)
                account, market, nodes, chain = reconnect(
                    BitPAIR, USERNAME, PASS_PHRASE)
                attempt += 1
                if attempt > 10:
                    zprint('SELL ABORTED')
                    return
                pass
        race_append(doc='microDEX_log.txt', text=msg)

    # interact with tkinter
    confirm = Tk()
    if market.bitshares.wallet.unlocked():
        price = sell_price.get()
        amount = sell_amount.get()
        if price == '':
            price = 0.9 * float(market.ticker()['latest'])
        if amount == '':
            amount = ANTISAT
        try:
            price = decimal(price)
            amount = float(amount)
            assets = float(account.balance(BitASSET))
            if amount > (0.998 * assets):
                amount = 0.998 * assets
            sprice = str(price)[:16]
            samount = str(amount)[:16]
            sorder = str(
                'CONFIRM SELL ' +
                samount +
                ' ' +
                BitASSET +
                ' @ ' +
                sprice)

            if amount > 0:
                confirm.title(sorder)
                Button(
                    confirm,
                    text='CONFIRM SELL',
                    command=lambda: sell(price, amount, market)).grid(
                    row=1,
                    column=0,
                    pady=8)
                Button(
                    confirm,
                    text='INVALIDATE',
                    command=confirm.destroy).grid(
                    row=2,
                    column=0,
                    pady=8)
            else:
                confirm.title('NO ASSETS TO SELL')
                Button(
                    confirm,
                    text='OK',
                    command=confirm.destroy).grid(
                    row=2,
                    column=0,
                    pady=8)
        except:
            confirm.title('INVALID SELL ORDER')
            Button(
                confirm,
                text='OK',
                command=confirm.destroy).grid(
                row=2,
                column=0,
                pady=8)
    else:
        confirm.title('YOUR WALLET IS LOCKED')
        Button(
            confirm,
            text='OK',
            command=confirm.destroy).grid(
            row=2,
            column=0,
            pady=8)
    confirm.geometry('500x100+800+175')
    confirm.lift()
    confirm.call('wm', 'attributes', '.', '-topmost', True)

def dex_cancel():

    # update wallet unlock to low latency node
    zprint('CANCEL')
    account, market, nodes, chain = reconnect(BitPAIR, USERNAME, PASS_PHRASE)
    orders = market.accountopenorders()
    # attempt cancel all 10X or until satisfied

    def cancel(market):
        confirm.destroy()
        zprint('CONFIRMED')
        attempt = 1
        order_list = []
        for order in orders:
            order_list.append(order['id'])
        while attempt:
            try:
                msg = market.cancel(order_list)
                msg = (' CANCEL ' + str(order_list) + ' of ' +
                       str(BitPAIR) + '\n' + str(msg))
                print (msg)
                attempt = 0
            except Exception as e:
                msg = msg_(e)
                race_append(doc='microDEX_log.txt', text=msg)
                msg += (+ str(attempt) + ' ' + ' CANCEL FAILED, RECONNECTING '
                        + str(nodes[0]) + ' ' + str(price) + ' ' + str(amount))
                zprint(' CANCEL FAILED, RECONNECTING ')
                race_append(doc='microDEX_log.txt', text=msg)
                account, market, nodes, chain = reconnect(
                    BitPAIR, USERNAME, PASS_PHRASE)
                attempt += 1
                if attempt > 10:
                    zprint('CANCEL ABORTED')
                    return
                pass
        race_append(doc='microDEX_log.txt', text=msg)

    # interact with tkinter
    confirm = Tk()
    if len(orders):
        if market.bitshares.wallet.unlocked():
            if len(orders) > 1:
                title = str(len(orders)) + ' ORDERS TO CANCEL'
            else:
                title = str(len(orders)) + ' ORDER TO CANCEL'
            confirm.title(title)
            Button(
                confirm,
                text='CONFIRM CANCEL ALL',
                command=lambda: cancel(market)).grid(
                row=1,
                column=0,
                pady=8)
            Button(
                confirm,
                text='INVALIDATE',
                command=confirm.destroy).grid(
                row=2,
                column=0,
                pady=8)
            confirm.geometry('500x100+800+175')
            confirm.lift()
            confirm.call('wm', 'attributes', '.', '-topmost', True)
        else:
            confirm.title('YOUR WALLET IS LOCKED')
            Button(
                confirm,
                text='OK',
                command=confirm.destroy).grid(
                row=2,
                column=0,
                pady=8)
    else:
        confirm.title('NO OUTSTANDING ORDERS')
        Button(
            confirm,
            text='OK',
            command=confirm.destroy).grid(
            row=2,
            column=0,
            pady=8)
    confirm.geometry('500x100+800+175')
    confirm.lift()
    confirm.call('wm', 'attributes', '.', '-topmost', True)

def dex_auth_gui():

    # unlock wallet from gui
    global PASS_PHRASE
    PASS_PHRASE = str(login.get())
    login.delete(0, END)
    account, market, nodes, chain = reconnect(BitPAIR, USERNAME, PASS_PHRASE)
    try:
        market.bitshares.wallet.unlock(PASS_PHRASE)
        lock.set('UNLOCKED')
        zprint('AUTHENTICATED')
    except Exception as e:
        if PASS_PHRASE != '':
            zprint(type(e).__name__)
        market.bitshares.wallet.lock()
        lock.set('LOCKED')
        zprint('WALLET LOCKED')
        pass

def float_sma(array, period):

    def moving_average(array, period):  # numpy array moving average
        csum = np.cumsum(array, dtype=float)
        csum[period:] = csum[period:] - csum[:-period]
        return csum[period - 1:] / period

    if period == int(period):  # simple moving average
        return moving_average(array, int(period))
    else:  # simple moving average w/ decimal period
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

def chartdata(pair, start, stop, period):  # Public API cryptocompare

    #{"time","close","high","low","open","volumefrom","volumeto"}
    # docs at https://www.cryptocompare.com/api/
    if period in [60, 300, 900, 1800, 3600, 7200, 14400, 43200, 86400]:

        uri = 'https://min-api.cryptocompare.com/data/'
        if period <= 1800:
            uri += 'histominute'
            aggregate = period / 60.0
        if 3600 <= period <= 43200:
            uri += 'histohour'
            aggregate = period / 3600.0
        if period >= 86400:
            uri += 'histoday'
            aggregate = period / 86400.0
        aggregate = int(aggregate)
        pair_split = pair.split('_')
        fsym = pair_split[1]
        tsym = pair_split[0]
        toTs = int(stop)
        limit = int((stop - start) / float(period))
        if limit > 2000:
            limit = 2000
        params = {'fsym': fsym, 'tsym': tsym, 'limit': 2000,
                  'aggregate': aggregate, 'toTs': toTs}
        ret = requests.get(uri, params=params).json()
        d = ret['Data']
        clean_d = clean_d1 = [i for i in d if i['close'] > 0]

        if (period == 7200) and ((stop - start) / 7200.0 > 1000):
            toTs -= period * len(clean_d)
            params = {'fsym': fsym, 'tsym': tsym, 'limit': 2000,
                      'aggregate': aggregate, 'toTs': toTs}
            ret = requests.get(uri, params=params).json()
            d = ret['Data']
            clean_d2 = [i for i in d if i['close'] > 0]
            clean_d = clean_d2 + clean_d1
            clean_d = [i for i in clean_d if i['time'] > start]

        return clean_d

    else:
        print('invalid period')
        return None

def live_candles(pair, candle, depth):  # Current HLOCV arrays

    # gather latest data to a given depth
    now = int(time.time())
    raw = chartdata(pair, (now - (depth + 10) * candle), now, candle)
    d = {}
    d['unix'] = []
    d['high'] = []
    d['low'] = []
    d['open'] = []
    d['close'] = []
    d['volume'] = []
    for i in range(len(raw)):
        d['unix'].append(raw[i]['time'])
        d['high'].append(raw[i]['high'])
        d['low'].append(raw[i]['low'])
        d['open'].append(raw[i]['open'])
        d['close'].append(raw[i]['close'])
        d['volume'].append(raw[i]['volumefrom'])
    # filter absurd wicks
    for i in range(len(d['unix'])):
        if d['high'][i] > 3 * d['close'][i]:
                d['high'][i] = 3 * d['close'][i]
        if d['low'][i] < 0.4 * d['close'][i]:
                d['low'][i] = 0.4 * d['close'][i]
    d['unix'] = np.array(d['unix'][-depth:])
    d['high'] = np.array(d['high'][-depth:])
    d['low'] = np.array(d['low'][-depth:])
    d['open'] = np.array(d['open'][-depth:])
    d['close'] = np.array(d['close'][-depth:])
    d['volume'] = np.array(d['volume'][-depth:])
    return d

def plot_format(log):

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
    if log == 1:
        plt.ylabel('LOGARITHMIC PRICE SCALE')
        plt.yscale('log')
    ax.yaxis.set_major_formatter(tkr.ScalarFormatter())
    ax.yaxis.set_minor_formatter(tkr.ScalarFormatter())
    ax.yaxis.set_major_formatter(tkr.FormatStrFormatter("%.8f"))
    ax.yaxis.set_minor_formatter(tkr.FormatStrFormatter("%.8f"))
    plt.autoscale(enable=True, axis='y')
    plt.tight_layout()
    if log == 1:
        # manifest 'logarithmic autoscale'
        yd = []  # matrix of y values from all lines on plot
        xd = []  # matrix of x values from all lines on plot
        for n in range(len(plt.gca().get_lines())):
            line = plt.gca().get_lines()[n]
            yd.append((line.get_ydata()).tolist())
            xd.append((line.get_xdata()).tolist())
        yd = [item for sublist in yd for item in sublist]
        ymin, ymax = np.min(yd), np.max(yd)
        ax.set_ylim([0.95 * ymin, 1.05 * ymax])
        xd = [item for sublist in xd for item in sublist]
        xmin, xmax = np.min(xd), np.max(xd)
        ax.set_xlim([xmin, xmax])
        # add sub minor ticks on log scale
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

    # Format X axis
    def timestamp(x, pos):
        return (datetime.fromtimestamp(x)).strftime('%m/%d %H:%M')
    ax.xaxis.set_major_formatter(tkr.FuncFormatter(timestamp))
    plt.gcf().autofmt_xdate(rotation=30)
    plt.gcf().canvas.set_window_title('microDEX CHART')

def dom_format():

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
    ax.yaxis.set_major_formatter(tkr.FormatStrFormatter("%.0f"))
    ax.yaxis.set_minor_formatter(tkr.FormatStrFormatter("%.0f"))
    plt.autoscale(enable=True, axis='y')
    plt.tight_layout()
    plt.gcf().autofmt_xdate(rotation=30)
    plt.gcf().canvas.set_window_title('microDEX DOM')

def dom():

    fig = plt.figure()
    while True:
        try:
            # gather data from the metaNODE
            metaNODE = Bitshares_Trustless_Client()
            # localize variables
            book = metaNODE['book']
            orders = metaNODE['orders']
            history = metaNODE['history']
            # orders comes to us from metaNODE sorted by price
            # sort orders prices/volumes by bid/ask
            obidp = []
            oaskp = []
            obidv = []
            oaskv = []
            for order in orders:
                if order['orderType'] == 'buy':
                    obidp.append(float(order['price']))
                    obidv.append(float(order['amount']))
                if order['orderType'] == 'sell':
                    oaskp.append(float(order['price']))
                    oaskv.append(float(order['amount']))
            # we need to reverse bids before cumsum
            obidp = obidp[::-1]
            obidv = obidv[::-1]
            # normal open order volume
            sum_ov = sum(obidv + oaskv)
            len_ov = len(obidv + oaskv)
            oav = sum_ov / len_ov if len_ov else 1
            # average of my open order volume
            onbidv = [30 * i / oav for i in obidv]
            onaskv = [30 * i / oav for i in oaskv]
            # cumulative open order volume
            ocbidv = list(np.cumsum(obidv))
            ocaskv = list(np.cumsum(oaskv))
            # quick list of zeros size of our cumulative order volume
            obid0 = [0 for i in ocbidv]
            oask0 = [0 for i in ocaskv]
            # market bid ask price and volume lists
            bidp = book['bidp']
            askp = book['askp']
            bidv = book['bidv']
            askv = book['askv']
            # cumulative volume
            cbidv = list(np.cumsum(bidv))
            caskv = list(np.cumsum(askv))
            # limit the orderbook depth
            depth = 30
            bidp = bidp[:depth]
            askp = askp[:depth]
            bidv = bidv[:depth]
            askv = askv[:depth]
            cbidv = cbidv[:depth]
            caskv = caskv[:depth]
            # quick list of zeros size of cumulative volume
            bid0 = [0 for i in cbidv]
            ask0 = [0 for i in caskv]
            # normalize recent trade history time and volue to fit dom
            trade_price = []
            trade_volume = []
            for trade in history:
                trade_price.append(float(trade[1]))
                trade_volume.append(float(trade[2]))
            # normalize trade time to scale of y axis
            max_cv = max(cbidv + caskv)
            sig_max_cv = float('%s' % float('%.1g' % max_cv))
            trade_time = np.linspace(0, -max_cv, num=len(trade_price))
            # normalize trade volume to use as marker size
            stv = sum(trade_volume)
            ltv = len(trade_volume)
            atv = stv / ltv
            n_trade_volume = [i / atv for i in trade_volume]
            # clear plot then add items
            plt.cla()
            # plot depth of market
            plt.plot(bidp, cbidv,
                     markersize=1, marker='.', color='lime')
            plt.plot(askp, caskv,
                     markersize=1, marker='.', color='red')
            # shade depth of market
            plt.fill_between(bidp, cbidv, bid0,
                             facecolor='green', interpolate=True, alpha=0.2)
            plt.fill_between(askp, caskv, ask0,
                             facecolor='red', interpolate=True, alpha=0.2)
            # plot depth of market
            plt.plot(obidp, ocbidv,
                     markersize=1, marker='.', color='orange')
            plt.plot(oaskp, ocaskv,
                     markersize=1, marker='.', color='orange')
            # shade depth of market
            plt.fill_between(obidp, ocbidv, obid0,
                             facecolor='orange', interpolate=True, alpha=0.2)
            plt.fill_between(oaskp, ocaskv, oask0,
                             facecolor='orange', interpolate=True, alpha=0.2)
            # scatter plot orders on cumulative volume line with normalized
            # marker size
            plt.scatter(
                obidp,
                ocbidv,
                s=onbidv,
                marker='o',
                color='yellow',
                alpha=0.5)
            plt.scatter(
                oaskp,
                ocaskv,
                s=onaskv,
                marker='o',
                color='yellow',
                alpha=0.5)
            # plot recent trade history
            plt.plot(trade_price, trade_time,
                     markersize=1, marker='.', color='magenta')
            for i in range(len(trade_price)):
                # plot recent trade history volume
                plt.plot([trade_price[i]], [trade_time[i]],
                         markersize=(3 * n_trade_volume[i]), marker='.', color='yellow', alpha = 0.5)
            # format the chart
            fig.patch.set_facecolor('0.15')
            plt.yticks(np.linspace(0, sig_max_cv, 11))
            dom_format()
            # repeat process every second
            plt.pause(2)
        except Exception as e:
            msg = msg_(e)
            race_append(doc='microDEX_log.txt', text=msg)
            time.sleep(10)
            pass

def charts():

    try:
        def draw_chart():
            try:
                ASSET = BitASSET.replace('OPEN.', '')
                CURRENCY = BitCURRENCY.replace('OPEN.', '')
                PAIR = ('%s_%s' % (CURRENCY, ASSET))
                ret = live_candles(PAIR, 300, 1000)
                cex_5m_x = ret['unix']
                cex_5m_close = ret['close']
                cex_5m_high = ret['high']
                cex_5m_low = ret['low']
                cex_5m_x = [(i + 150) for i in cex_5m_x]
                ret = live_candles(PAIR, 7200, 2000)
                cex_2h_x = ret['unix']
                cex_2h_close = ret['close']
                cex_2h_high = ret['high']
                cex_2h_low = ret['low']
                cex_2h_x = [(i + 3600) for i in cex_2h_x]
                ret = live_candles(PAIR, 86400, 1000)
                cex_d_x = ret['unix']
                cex_d_close = ret['close']
                cex_d_high = ret['high']
                cex_d_low = ret['low']
                crop = len(cex_d_x) - 90
                cex_d_x = cex_d_x[-crop:]
                cex_d_close = cex_d_close[-crop:]
                cex_d_high = cex_d_high[-crop:]
                cex_d_low = cex_d_low[-crop:]
                cex_d_x = [(i + 43400) for i in cex_d_x]
                ma1_d_period = float(MA1.get())
                ma2_d_period = float(MA2.get())
                ma1_2h_period = 12.0 * ma1_d_period
                ma2_2h_period = 12.0 * ma2_d_period

                selloff_ = float(SELLOFF.get())
                support_ = float(SUPPORT.get())
                resistance_ = float(RESISTANCE.get())
                despair_ = float(DESPAIR.get())
                cross_ = float(CROSS.get())

                ma1_2h = float_sma(cex_2h_close, ma1_2h_period)
                ma2_2h = float_sma(cex_2h_close, ma2_2h_period)
                min_len = min(len(ma1_2h), len(ma2_2h))
                ma1_2h = ma1_2h[-min_len:]
                ma2_2h = ma2_2h[-min_len:]
                ma_x_2h = cex_2h_x[-min_len:]
                ma2_2h = cross_ * ma2_2h

                if min(ma1_d_period, ma2_d_period) > 2:

                    ma1_d = float_sma(cex_d_close, ma1_d_period)
                    ma2_d = float_sma(cex_d_close, ma2_d_period)
                    min_len = min(len(ma1_d), len(ma2_d))

                    ma1_d = ma1_d[-min_len:]
                    ma2_d = ma2_d[-min_len:]
                    ma_x_d = cex_d_x = cex_d_x[-min_len:]
                    cex_d_high = cex_d_high[-min_len:]
                    cex_d_low = cex_d_low[-min_len:]
                    cex_d_close = cex_d_close[-min_len:]

                    ma_x_d = np.array(ma_x_d)
                    ma1_d = np.array(ma1_d)
                    ma2_d = np.array(ma2_d)
                    cex_d_high = np.array(cex_d_high)
                    cex_d_low = np.array(cex_d_low)

                    ma_x_d = ma_x_d + 86400
                    ma2_d = ma2_d * cross_
                    selloff = ma2_d * selloff_
                    support = ma2_d * support_
                    resistance = ma2_d * resistance_
                    despair = ma2_d * despair_

                metaNODE = Bitshares_Trustless_Client()
                history = metaNODE['history']
                dex_x, dex_y = [], []
                for trade in history:
                        dex_x.append(float(trade[0]))
                        dex_y.append(float(trade[1]))

                plt.cla()
                ax = plt.gca()
                log = int((scale.var).get())
                '''
                for l in ax.get_lines():
                        l.remove()
                '''
                fig.patch.set_facecolor('0.15')

                plt.plot(cex_5m_x, cex_5m_high,
                         markersize=1, marker='.', color='magenta')
                plt.plot(cex_5m_x, cex_5m_low,
                         markersize=1, marker='.', color='magenta')
                plt.plot(cex_5m_x, cex_5m_close,
                         markersize=1, marker='.', color='yellow')
                plt.plot(cex_2h_x, cex_2h_high,
                         markersize=1, marker='.', color='magenta')
                plt.plot(cex_2h_x, cex_2h_low,
                         markersize=1, marker='.', color='magenta')
                plt.plot(cex_2h_x, cex_2h_close,
                         markersize=1, marker='.', color='yellow')
                plt.plot(cex_d_x, cex_d_high,
                         markersize=1, marker='.', color='magenta')
                plt.plot(cex_d_x, cex_d_low,
                         markersize=1, marker='.', color='magenta')
                plt.plot(cex_d_x, cex_d_close,
                         markersize=1, marker='.', color='yellow')

                if ma1_d_period > 3:
                    plt.plot(ma_x_d, ma1_d,
                             markersize=1, marker='.', color='purple')
                else:
                    plt.plot(ma_x_2h, ma1_2h,
                             markersize=1, marker='.', color='purple')

                if ma2_d_period > 3:
                    plt.plot(ma_x_d, ma2_d,
                             markersize=1, marker='.', color='aqua')
                else:
                    plt.plot(ma_x_2h, ma2_2h,
                             markersize=1, marker='.', color='aqua')

                if ma2_d_period > 3:
                    plt.fill_between(
                        ma_x_d, support, selloff, where=(ma2_d > ma1_d),
                        facecolor='green', interpolate=True, alpha = 0.2)
                    plt.fill_between(
                        ma_x_d, resistance, despair, where=(ma2_d < ma1_d),
                        facecolor='red', interpolate=True, alpha = 0.2)

                plt.plot(dex_x, dex_y, markersize=6, marker='.', color='white')
                plot_format(log)
                interface.after(300000, draw_chart)  # refresh in milliseconds
                plt.show()
                print("\033c")
            except Exception as e:
                msg = msg_(e)
                race_append(doc='microDEX_log.txt', text=msg)
                pass

        # Create User interface for plot
        fig = plt.figure()
        interface = Tk()
        f1 = Frame()
        f2 = Frame()
        f3 = Frame()
        f4 = Frame()
        f1.pack()
        f2.pack()
        f3.pack()
        f4.pack()

        MA1 = Scale(f1,
                    from_=0.2,
                    to=100,
                    resolution=0.01,
                    orient=HORIZONTAL,
                    length=300)
        MA2 = Scale(f1,
                    from_=0.2,
                    to=100,
                    resolution=0.01,
                    orient=HORIZONTAL,
                    length=300)

        SELLOFF = Scale(f2,
                        from_=0.333,
                        to=3,
                        resolution=0.01,
                        orient=HORIZONTAL,
                        length=200)
        SUPPORT = Scale(f3,
                        from_=0.333,
                        to=3,
                        resolution=0.01,
                        orient=HORIZONTAL,
                        length=200)
        RESISTANCE = Scale(f2,
                           from_=0.333,
                           to=3,
                           resolution=0.01,
                           orient=HORIZONTAL,
                           length=200)
        DESPAIR = Scale(f3,
                        from_=0.333,
                        to=3,
                        resolution=0.01,
                        orient=HORIZONTAL,
                        length=200)
        CROSS = Scale(f1,
                      from_=0.333,
                      to=3,
                      resolution=0.01,
                      orient=HORIZONTAL,
                      length=200)
        v = IntVar()
        scale = Checkbutton(f2, text="LOG SCALE", variable=v)
        scale.var = v

        MA1.set(50)
        MA2.set(10)
        SELLOFF.set(2)
        SUPPORT.set(1.25)
        RESISTANCE.set(0.9)
        DESPAIR.set(0.5)
        CROSS.set(1)
        Label(f1, text='LONG AVERAGE').pack(side=LEFT)
        MA1.pack(side=LEFT)
        Label(f1, text='SIGNAL LINE').pack(side=LEFT)
        MA2.pack(side=LEFT)
        Label(f1, text='CROSS').pack(side=LEFT)
        CROSS.pack(side=LEFT)

        Label(f2, text='SELLOFF').pack(side=LEFT)
        SELLOFF.pack(side=LEFT)
        Label(f2, text='RESISTANCE').pack(side=LEFT)
        RESISTANCE.pack(side=LEFT)
        scale.pack(side=LEFT)

        Label(f3, text='      SUPPORT').pack(side=LEFT)
        SUPPORT.pack(side=LEFT)
        Label(f3, text='      DESPAIR').pack(side=LEFT)
        DESPAIR.pack(side=LEFT)
        Button(f3, text='UPDATE CHART', command=draw_chart).pack(side=LEFT)

        interface.after(1, draw_chart)
        interface.title('microDEX plot updater')
        interface.geometry("0x0+0+0")
        interface.lift()
        interface.call('wm', 'attributes', '.', '-topmost', True)
        interface.mainloop()

    except Exception as e:
        msg = msg_(e)
        race_append(doc='microDEX_log.txt', text=msg)
        pass

def main():

    global USERNAME, BitPAIR, BitASSET, BitCURRENCY, BEGIN
    global account, market, PASS_PHRASE
    global login, buy_price, buy_amount, sell_price, sell_amount, lock

    version()
    constants()

    race_write(doc='microDEX_log.txt', text='')
    msg = 'BEGIN SESSION ' + str(VERSION)
    race_append(doc='microDEX_log.txt', text=msg)

    # sign in - username/market/password
    print("\033c")

    # Encoded Compressed Bitshares ASCII Logo
    import zlib
    b = b'x\x9c\xad\xd4M\n\xc4 \x0c\x05\xe0}O1P\x12B\x10\xbc\x82\xf7?\xd5\xf8\xaf\x83F\xe3\xe0[t\xf9\xf5%\xda>\x9f\x1c\xf7\x7f\x9e\xb9\x01\x17\x0cc\xec\x05\xe3@Y\x18\xc6(\'Z\x1a\xca.\x1bC\xa5l\r\x85\xa20\xb6\x8a\xca\xd8,W0\xec\x05\xc3\xdf\xd4_\xe3\r\x11(q\x16\xec\x95l\x04\x06\x0f\x0c\xc3\xddD\x9dq\xd2#\xa4NT\x0c/\x10\xd1{b\xd4\x89\x92\x91\x84\x11\xd9\x9d-\x87.\xe4\x1cB\x15|\xe0\xc8\x88\x13\xa5\xbc\xd4\xa21\x8e"\x18\xdc\xd2\x0e\xd3\xb6\xa0\xc6h\xa3\xd4\xde\xd0\x19\x9a\x1e\xd8\xddr\x0e\xcf\xf8n\xe0Y\rq\x1fP:p\x92\xf2\xdbaB,v\xda\x84j\xc4.\x03\xb1>\x97\xee{\x99oSa\x00\x0f\xc6\x84\xd8\xdf\x0f\xb4e\xa7$\xfdE\xae\xde\xb1/\x1d\xfc\x96\x8a'
    print(cyan(zlib.decompress(b).decode()))

    print(blue('''
                                       ______   ________  ____  ____
                                      (_   _ `.(_   __  |(_  _)(_  _)
       __  __  ____  ___  ____   ___    | | `. \ | |_ \_|  \ \__/ /
      (  \/  )(_  _)/ __)(  _ \ / _ \   | |  | | |  _) _    ) __ (
       )    (  _||_( (__  )   /( (_) ) _| |_.' /_| |__/ | _/ /  \ \_
      (_/\/\_)(____)\___)(_)\_) \___/ (______.'(________|(____)(____)
    ===================================================================
          '''))
    print(cyan('           Bitshares Minimalist UI ' + VERSION))
    print(blue('''
    ===================================================================
          '''))
    print('')
    print('')

    valid = 0
    while not valid:
        try:
            USERNAME = input('           Account: ')
            account = Account(
                USERNAME,
                bitshares_instance=BitShares(
                    nodes,
                    num_retries=10))
            valid = 1
        except Exception as e:
            print (type(e).__name__, 'try again...')
            pass
    print('')
    print('      Welcome Back: ', account)
    print('')
    print(' Default market is: ', red(BitPAIR))
    print('')
    print(
        yellow('Input new Bitshares DEX market below or press ENTER to skip'))
    print('e.g.: BTS:CNY, BTS:OPEN.BTC, OPEN.LTC:OPEN.BTC, OPEN.BTC:USD')
    print('')
    valid = 0
    default = BitPAIR
    while not valid:
        try:
            BitPAIR = input('  Change market to: ') or default
            BitASSET = BitPAIR.split(':')[0]
            BitCURRENCY = BitPAIR.split(':')[1]
            market = Market(
                BitPAIR,
                bitshares_instance=BitShares(
                    nodes,
                    num_retries=0),
                mode='head')
            valid = 1
        except Exception as e:
            print (type(e).__name__, 'try again...')
            pass
    print('')
    print(yellow(
        'Enter PASS PHRASE below to unlock your wallet or press ENTER to skip'))
    print('')
    valid = 0
    default = ''
    while not valid:
        try:
            PASS_PHRASE = getpass(prompt='       Pass Phrase: ') or default
            if PASS_PHRASE != '':
                market.bitshares.wallet.unlock(PASS_PHRASE)
                print('')
                print(yellow('AUTHENTICATED - YOUR WALLET IS UNLOCKED'))
                valid = 1
            else:
                print('')
                print('SKIP AUTHENTICATION - YOUR WALLET IS LOCKED')
                valid = 1
        except Exception as e:
            print (type(e).__name__, 'try again...')
            pass
    print('')
    print(
        blue('Connecting to the Bitshares Distributed Exchange, please wait...'))
    print('')

    # begin several concurrent background processes of launch_book()
    BEGIN = int(time.time())

    # begin orderbooks
    b = Process(target=book)
    b.daemon = False
    b.start()

    # begin live charts
    try:
        c = Process(target=charts)
        c.daemon = True
        c.start()
    except:
        print('WARN: plotting only available for crypto altcoins')

    # begin live charts
    try:
        d = Process(target=dom)
        d.daemon = True
        d.start()
    except:
        print('WARN: plotting only available for crypto altcoins')

    time.sleep(5)

    print("\033c")
    print('')
    print('')
    print('')
    print(yellow('initializing microDEX...'))

    # tkinter primary busybox
    master = Tk()
    lock = StringVar()
    lock.set('UNLOCKED')
    if market.bitshares.wallet.locked():
        lock.set('LOCKED')
    master.title(VERSION)
    Label(master, text="PRICE:").grid(row=0, column=0, sticky=E)
    Label(master, text="AMOUNT:").grid(row=1, column=0, sticky=E)
    Label(master, text="PRICE:").grid(row=0, column=2, sticky=E)
    Label(master, text="AMOUNT:").grid(row=1, column=2, sticky=E)
    Label(master, textvariable=lock).grid(row=6, column=2, sticky=W)
    Label(master, text=
          "   *ORDERS TAKE A FEW SECONDS TO APPEAR; CLICK ONCE, THEN CONFIRM*"
          ).grid(row=7, column=0, columnspan=4, sticky=W)
    buy_price = Entry(master)
    buy_amount = Entry(master)
    sell_price = Entry(master)
    sell_amount = Entry(master)
    login = Entry(master)
    buy_price.grid(row=0, column=1)
    buy_amount.grid(row=1, column=1)
    sell_price.grid(row=0, column=3)
    sell_amount.grid(row=1, column=3)
    login.grid(row=6, column=1)
    Button(
        master,
        text='BUY',
        command=dex_buy).grid(
        row=3,
        column=1,
        sticky=W,
        pady=4)
    Button(
        master,
        text='SELL',
        command=dex_sell).grid(
        row=3,
        column=3,
        sticky=W,
        pady=4)
    Button(
        master,
        text='CANCEL ALL',
        command=dex_cancel).grid(
        row=5,
        column=0,
        sticky=E,
        pady=4)
    Button(
        master,
        text='LOCK/UNLOCK',
        command=dex_auth_gui).grid(
        row=6,
        column=0,
        sticky=E,
        pady=4)
    master.geometry('+550+700')
    master.lift()
    master.call('wm', 'attributes', '.', '-topmost', True)
    mainloop()

if __name__ == "__main__":

    main()
