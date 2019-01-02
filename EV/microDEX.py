
' microDEX '

# Lightweight UI for Bitshares Decentralized Exchange

' litepresence 2019 '

def WTFPL_v0_March_1765():
    if any([stamps, licenses, taxation, regulation, fiat, etat]):
        try:
            print('no thank you')
        except:
            return [tar, feathers]

# Standard Python Modules
import os
import sys
import zlib
import time
import json
import requests
import traceback
import numpy as np
from tkinter import *
from getpass import getpass
from decimal import Decimal as decimal
from ast import literal_eval as literal
from random import random, shuffle, randint

# Bitshares Modules
try:
    from bitshares import BitShares
    from bitshares.market import Market
    from bitshares.account import Account
    from bitshares.blockchain import Blockchain
except Exception as e:
    print(str(e.args))
    print('for installation please visit:')
    print('https://github.com/litepresence/extinction-event/blob/master/README.md')

DEV = False  # additional feedback
COLOR = True  # black and white only in terminal
SLOW_PING = 1.25  # switch nodes if laggy

'''
# Development tool for namespace object size
try:
    from pympler import asizeof

    sizes = []
    for name, obj in locals().items():
        if name != 'asizeof':
            sizes.append((name, (asizeof.asizeof(obj) / 1024)))
    race_write(doc='sizes.txt', text=str(sizes))
except:
    pass
'''

# set default currency pair
BitCURRENCY = 'OPEN.BTC'
BitASSET = 'BTS'
BitPAIR = BitASSET + ':' + BitCURRENCY
PASS_PHRASE = ''
BEGIN = int(time.time())
VERSION = 'v0.00000021-DEL'
SATOSHI = 0.00000001
ANTISAT = expiration = 1/SATOSHI

# mainnet ID
ID = '4018d7844c78f6a6c41c6a552b898022310fc5dec06da467ee7905a8dad512c8'

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

def colors():

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

def elapsed(text=''):
    if DEV:
        global stopwatch
        now = time.time()
        e = now - stopwatch
        stopwatch = now
        print(('%.4f' % e), text)

def msg_(e):  # traceback message
    return (str(type(e).__name__) + str(e.args) + str(e) +
            str(traceback.format_exc()) + str(sys.exc_info()))

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
                if metaNODE == {}:
                    raise ValueError('metaNODE is blank')
                break
        except Exception as e:
            msg = str(
                time.ctime(
                ) + ' ' + type(
                    e).__name__) + ' ' + str(
                e.args)
            race_condition = ['Unterminated', "Expecting"]
            if any([x in str(e.args) for x in race_condition]):
                print('metaNODE = Bitshares_Trustless_Client() RACE READ')
            elif 'metaNODE is blank' in str(e.args):
                continue
            else:
                print('metaNODE = Bitshares_Trustless_Client() ' + msg)
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

def race_read(doc=''):  # Concurrent Read from File Operation

    opened = 0
    while not opened:
        try:
            with open(doc, 'r') as f:
                # ret = json.loads(f.read())
                ret = literal(f.read())
                opened = 1
        except Exception as e:
            msg = (time.ctime() + str(type(e).__name__) + str(e.args))
            print('race_read ' + msg)
            time.sleep(0.1)
            pass
    return ret

def race_append(doc='', text=''):  # Concurrent Append to File Operation

    text = '\n' + str(time.ctime()) + ' ' + str(text) + '\n'
    opened = 0
    while not opened:
        try:
            with open(doc, 'a+') as f:

                f.write(str(text))
                opened = 1
        except Exception as e:
                msg = (time.ctime() + str(type(e).__name__) + str(e.args))
                print('race_append' + msg)
                time.sleep(0.1)
                pass

def race_write(doc='', text=''):  # Concurrent Write to File Operation

    if not isinstance(text, str):
        text = str(text)

    i = 0
    while True:
        time.sleep(0.05 * i ** 2)
        i += 1
        try:
            with open(doc, 'w+') as f:
                f.write(text)
                f.close()
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

def reconnect():

    global account, market, nodes, chain, pings
    try:
        history_text.delete("1.0", "end")
        history_text.insert(END, '\n\n CONNECTING...')
        master.update()
    except:
        pass
    print(cyan(time.ctime() + ' CONNECTING...'))
    start = time.time()

    # create fresh websocket connection
    connected = 0
    while not connected:
        # fetch fresh nodes list from subprocess and shuffle it
        metaNODE = Bitshares_Trustless_Client()
        nds = metaNODE['whitelist']
        del metaNODE
        if isinstance(nds, list):
            nodes = nds
        shuffle(nodes)
        node = nodes[0]
        print(green(node))
        pings = [0]
        try:
            account = Account(USERNAME,
                              bitshares_instance=BitShares(nodes,
                                                           num_retries=2))
            market = Market(BitPAIR,
                            bitshares_instance=BitShares(nodes,
                                                         num_retries=2),
                            mode='head')
            chain = Blockchain(
                bitshares_instance=BitShares(nodes, num_retries=2), mode='head')
            if chain.get_network()['chain_id'] != ID:
                raise ValueError('Not Mainnet Chain')
            connected = 1
        except Exception as e:
            try:
                history_text.insert(END, '\n\n RECONNECTING...')
                master.update()
            except:
                pass
            msg = (time.ctime() + str(type(e).__name__) + str(e.args))
            print('RECONNECTING ' + msg)
            pass
    try:
        market.bitshares.wallet.unlock(PASS_PHRASE)
    except:
        # print('YOUR WALLET IS LOCKED')
        pass
    print('CONNECTION ELAPSED: ', ('%.1f' % (time.time() - start)))

def dex_buy():

    def buy(price, amount):
        confirm.destroy()
        print('CONFIRMED')
        attempt = 1

        while attempt:
            try:
                msg = market.buy(price, amount, expiration)

                msg = (' BUY ' + str(amount) + ' of ' + str(BitPAIR) +
                       ' @ ' + str(price) + '\n' + str(msg))
                print (msg)
                attempt = 0
            except Exception as e:
                msg = msg_(e)
                race_append(doc='microDEX_log.txt', text=msg)
                msg += (str(attempt) + ' ' + ' BUY FAILED, RECONNECTING '
                        + str(nodes[0]) + ' ' + str(price) + ' ' + str(amount))
                print(' BUY FAILED, RECONNECTING ', msg)
                race_append(doc='microDEX_log.txt', text=msg)
                reconnect()
                attempt += 1
                if attempt > 10:
                    print('BUY ABORTED')
                    return
                pass
        race_append(doc='microDEX_log.txt', text=msg)

    print(green('*** BUY ***'))
    metaNODE = Bitshares_Trustless_Client()
    currency = metaNODE['currency']
    currency_balance = metaNODE['currency_balance']
    del metaNODE
    # interact with tkinter
    confirm = Tk()
    if market.bitshares.wallet.unlocked():
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
            # convert amounts to float; should already be
            amount = float(amount)
            # do not spend your last bitshare
            if currency == 'BTS':
                currency_balance = currency_balance - 1
            # limit buy amount to means given currency in hand and price
            means = 0.998 * currency_balance / float(price)
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
                print(yellow('CONFIRM BUY?'))
                Button(
                    confirm,
                    text='CONFIRM BUY',
                    command=lambda: buy(price, amount)).grid(
                    row=1,
                    column=0,
                    pady=8)
                Button(
                    confirm,
                    text='INVALIDATE',
                    command=lambda: invalidate(confirm)).grid(
                    row=2,
                    column=0,
                    pady=8)
            else:
                confirm.title('NO CURRENCY TO BUY')
                print(yellow('NO CURRENCY TO BUY'))
                Button(
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
                print(yellow('LOST CONNECTION, TRY AGAIN'))
                reconnect()
            else:
                confirm.title('INVALID BUY ORDER')
                print(yellow('INVALID BUY ORDER'))
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
        print(yellow('YOUR WALLET IS LOCKED'))
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

    def sell(price, amount):
        confirm.destroy()
        print('CONFIRMED')
        attempt = 1
        while attempt:
            try:
                msg = market.sell(price, amount, expiration)
                msg = (' SELL ' + str(amount) + ' of ' + str(BitPAIR) +
                       ' @ ' + str(price) + '\n' + str(msg))
                print (msg)
                attempt = 0
            except Exception as e:
                msg = msg_(e)
                race_append(doc='microDEX_log.txt', text=msg)
                msg += (str(attempt) + ' ' + ' SELL FAILED, RECONNECTING '
                        + str(nodes[0]) + ' ' + str(price) + ' ' + str(amount))
                print(' SELL FAILED, RECONNECTING ', msg)
                race_append(doc='microDEX_log.txt', text=msg)
                reconnect()
                attempt += 1
                if attempt > 10:
                    print('SELL ABORTED')
                    return
                pass
        race_append(doc='microDEX_log.txt', text=msg)

    print(red('*** SELL ***'))

    metaNODE = Bitshares_Trustless_Client()
    bts_balance = metaNODE['bts_balance']
    asset_balance = metaNODE['asset_balance']
    asset = metaNODE['asset']
    del metaNODE

    # interact with tkinter confirm sell widget
    confirm = Tk()
    if market.bitshares.wallet.unlocked():
        price = sell_price.get()
        amount = sell_amount.get()
        # retain the last bitshare
        try:
            if price == '':
                raise ValueError('No Price Specified')
            if amount == '':
                raise ValueError('No Amount Specified')
            if asset == 'BTS':
                if float(amount) > (bts_balance - 1):
                    amount = (bts_balance - 1)
            price = decimal(price)
            amount = float(amount)
            if amount > (0.998 * asset_balance):
                amount = 0.998 * asset_balance
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
                print(yellow('CONFIRM SELL?'))
                Button(
                    confirm,
                    text='CONFIRM SELL',
                    command=lambda: sell(price, amount)).grid(
                    row=1,
                    column=0,
                    pady=8)
                Button(
                    confirm,
                    text='INVALIDATE',
                    command=lambda: invalidate(confirm)).grid(
                    row=2,
                    column=0,
                    pady=8)
            else:
                confirm.title('NO ASSETS TO SELL')
                print(yellow('NO ASSETS TO SELL'))
                Button(
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
                print(yellow('LOST CONNECTION, TRY AGAIN'))
                reconnect()
            confirm.title('INVALID SELL ORDER')
            print(yellow('INVALID SELL ORDER'))

            Button(
                confirm,
                text='OK',
                command=confirm.destroy).grid(
                row=2,
                column=0,
                pady=8)
    else:
        confirm.title('YOUR WALLET IS LOCKED')
        print(yellow('YOUR WALLET IS LOCKED'))
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

    print(blue('*** CANCEL ***'))
    # attempt cancel all 10X or until satisfied
    metaNODE = Bitshares_Trustless_Client()
    orders = metaNODE['orders']
    del metaNODE

    def cancel(market):
        confirm.destroy()
        print('CONFIRMED')
        attempt = 1
        metaNODE = Bitshares_Trustless_Client()
        orders = metaNODE['orders']
        del metaNODE

        o = orders[:]
        while len(o):
            order_list = []
            for order in orders:
                order_list.append(order['orderNumber'])
            try:
                msg = market.cancel(order_list)
                msg = (' CANCEL ' + str(order_list) + ' of ' +
                       str(BitPAIR) + '\n' + str(msg))
                print (msg)

            except Exception as e:
                msg = msg_(e)
                race_append(doc='microDEX_log.txt', text=msg)
                msg += (' CANCEL FAILED, RECONNECTING ' + str(nodes[0]))
                print(' CANCEL FAILED, RECONNECTING ')
                race_append(doc='microDEX_log.txt', text=msg)
                reconnect()
                pass
            o = market.accountopenorders()
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
            print(yellow('CONFIRM?'))
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
                command=lambda: invalidate(confirm)).grid(
                row=2,
                column=0,
                pady=8)
            confirm.geometry('500x100+800+175')
            confirm.lift()
            confirm.call('wm', 'attributes', '.', '-topmost', True)
        else:
            confirm.title('YOUR WALLET IS LOCKED')
            print(yellow('YOUR WALLET IS LOCKED'))
            Button(
                confirm,
                text='OK',
                command=confirm.destroy).grid(
                row=2,
                column=0,
                pady=8)
    else:
        confirm.title('NO OUTSTANDING ORDERS')
        print(yellow('NO OUTSTANDING ORDERS'))
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
    global lock, PASS_PHRASE
    PASS_PHRASE = str(login.get())
    login.delete(0, END)
    print(blue('LOCK/UNLOCK WALLET'))
    try:
        market.bitshares.wallet.unlock(PASS_PHRASE)
        lock.set('AUTHENTICATED')
        print(red('*****************'))
        print(red('**AUTHENTICATED**'))
        print(red('*****************'))
    except Exception as e:
        print(type(e).__name__)
        market.bitshares.wallet.lock()
        lock.set('WALLET IS UNLOCKED')
        print(yellow('WALLET LOCKED'))
        pass

def update():

    global ping, update_id, pings
    elapsed('begin')
    complete = 0
    if update_id % 8 == 0:
        while not complete:
            try:
                trade_node = nodes[0].replace(
                    'wss://',
                    '').replace('/wss',
                                '').replace('/ws',
                                            '')
                if update_id % 80 == 0:
                    start = time.time()
                    chain.get_network()['chain_id']
                    chain_id = chain.get_network()['chain_id']
                    if chain_id != ID:
                        raise ValueError('INVALID CHAIN: ' + chain_id)
                    ping = time.time() - start
                pings.append(ping)
                depth = 6
                pings = pings[-depth:]
                ping = sum(pings) / len(pings)
                if ping > SLOW_PING:
                    raise ValueError('SLOW PING: %.3f' % ping)
                if len(pings) == (depth - 1):
                    print('PING: %.3f' % (ping * depth / (depth - 1)))
                elapsed('ping')
                metaNODE = Bitshares_Trustless_Client()
                elapsed('metaNODE')
                # localize metaNODE data
                data_node = metaNODE['whitelist'][0].replace(
                    'wss://',
                    '').replace('/wss',
                                '').replace('/ws',
                                            '')
                blocktime = metaNODE['blocktime']
                last = metaNODE['last']
                orders = metaNODE['orders']
                currency_balance = metaNODE['currency_balance']
                asset_balance = metaNODE['asset_balance']
                currency_precision = metaNODE['currency_precision']
                asset_precision = metaNODE['asset_precision']
                bts_balance = metaNODE['bts_balance']
                currency = metaNODE['currency']
                asset = metaNODE['asset']
                history = metaNODE['history']
                book = metaNODE['book']
                buy_orders = metaNODE['buy_orders']
                sell_orders = metaNODE['sell_orders']
                invested = metaNODE['invested']
                divested = metaNODE['divested']
                # metaNODE dict is large, best to delete object when done
                del metaNODE

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
                latency = '%.3f' % (time.time() - blocktime + time.timezone)
                sbidp = [(' %.16f ' % i).rjust(20, ' ') for i in book['bidp']]
                saskp = [(' %.16f ' % i).ljust(20, ' ') for i in book['askp']]
                sbidv = [(' %.2f ' % i).rjust(12, ' ') for i in book['bidv']]
                saskv = [(' %.2f ' % i).rjust(12, ' ') for i in book['askv']]
                cbidv = list(np.cumsum(book['bidv']))
                caskv = list(np.cumsum(book['askv']))
                cbidv = [(' %.2f ' % i).rjust(12, ' ') for i in cbidv]
                caskv = [(' %.2f ' % i).rjust(12, ' ') for i in caskv]
                del book  # eliminate book after data extraction

                depth = 30
                sbidp = sbidp[:depth]
                saskp = saskp[:depth]
                sbidv = sbidv[:depth]
                saskv = saskv[:depth]
                cbidv = cbidv[:depth]
                caskv = caskv[:depth]
                complete = 1
                elapsed('format data')
            except Exception as e:
                print(e)
                reconnect()
                elapsed('reconnect')
                continue

        header_text.delete("1.0", "end")
        header_text.insert(
            END,
            ('     ' + time.ctime() + '    microDEX - Bishares Minimalist UI\n\n'))
        header_text.insert(
            END, ('               MEAN PING ' + ('%.3f' %
                                                 ping) + '  ' + trade_node + '\n'))
        header_text.insert(
            END,
            ('            DATA LATENCY ' + latency + '  ' + data_node + '\n'))
        header_text.insert(
            END,
            ('                    LAST ' + slast + '     ' +
             BitPAIR + '   RUNTIME ' + str(int(time.time()) - BEGIN)))
        elapsed('header')

        bid_text.delete("1.0", "end")
        ask_text.delete("1.0", "end")
        for i in range(len(saskp)):
            # askp = ['%.8f' % j for j in book['askp']]
            ask_text.insert(END, (saskp[i] + saskv[i] + caskv[i] + '\n'))
            bid_text.insert(
                END,
                (cbidv[i] + sbidv[i] + sbidp[i] + '\n'),
                'right')
        elapsed('book')

        history_text.delete("1.0", "end")
        history_text.insert(
            END,
            (' ' + str(int(time.time())) + ' LAST TRADE ' +
             str(int(time.time() - history[0][0] + time.timezone)) + '\n'))
        for i in range(len(history)):
            history_text.insert(
                END,
                (' ' + str(history[i][0]) + ' ' +
                 str(history[i][1]) + ' ' +
                 str(history[i][2]) + ' ' + '\n'))
        elapsed('history')

        orders_text.delete("1.0", "end")
        if len(orders):
            orders_text.insert(END, ' OPEN ORDERS\n')
            for i in range(len(orders)):
                orders_text.insert(
                    END,
                    (' ' + str(orders[i]['price']) + ' ' +
                     str(orders[i]['orderType']).ljust(4, ' ') + ' ' +
                     str(orders[i]['amount']) + '\n'))
        else:
            orders_text.insert(END, '\n NO OPEN ORDERS')
        elapsed('orders')

        # create dynamic format styles: "%.4f" etc.
        ap = '%.' + str(int(asset_precision / 2.0)) + 'f'
        cp = '%.' + str(int(currency_precision / 2.0)) + 'f'

        account_text.delete("1.0", "end")
        account_text.insert(END, ' ASSETS: ' + (ap % asset_balance).rjust(12, ' ') +
                            '         CURRENCY: ' + (cp % currency_balance).rjust(12, ' ') +
                            '                BITSHARES: ' + ('%.2f' % bts_balance) + '\n')

        account_text.insert(END, ' ORDERS: ' +
                           (ap % sell_orders).rjust(12, ' ') +
                            '                   ' +
                           (cp % buy_orders).rjust(12, ' ') + '\n')

        account_text.insert(END, '  TOTAL: ' +
                           (ap % asset_total).rjust(12, ' ') +
                            ' ' + (str(invested) + ' %').ljust(7, ' ') +
                            '           ' +
                           (cp % currency_total).rjust(12, ' ') +
                            ' ' + str(divested).ljust(4, ' ') + ' %\n')

        account_text.insert(END, '    MAX: ' +
                           (ap % asset_value).rjust(12, ' ') + ' ' +
                            asset.ljust(10, ' ') +
                            '        ' +
                           (cp % currency_value).rjust(12, ' ') + ' ' +
                            currency.ljust(10, ' '))
        master.update()
        elapsed('account')

        lock = StringVar()
        lock.set('AUTHENTICATED')
        lock_color = red1
        if market.bitshares.wallet.locked():
            lock.set('WALLET LOCKED')
            lock_color = blue1
        Label(
            master,
            textvariable=lock,
            fg=lock_color,
            bg=gray3).grid(
            row=8,
            column=2,
            sticky=W)
        master.update()
        elapsed('locked')
    update_id += 1

    master.after(100, update)

def invalidate(confirm):
    confirm.destroy()
    print(blue('MANUALLY INVALIDATED'))

def switch():

    print(blue('MANUALLY SWITCHING NODES...'))
    reconnect()

def main():

    global stopwatch, USERNAME, BitPAIR, PASS_PHRASE
    global master, lock
    global header_text, bid_text, ask_text, history_text, orders_text
    global update_id, ping, pings, account_text
    global account, market, nodes, chain
    global buy_price, buy_amount, sell_price, sell_amount, login

    colors()

    race_write(doc='microDEX_log.txt', text=time.ctime())
    stopwatch = time.time()

    print("\033c")
    sys.stdout.write(
        '\x1b]2;' +
        'Bitshares microDEX' +
        '\x07')  # terminal #title
    # Encoded Compressed Bitshares ASCII Logo
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
    time.sleep(0.3)
    print(cyan('GATHERING live curated DEX data from the metaNODE...'))
    time.sleep(0.3)
    try:
        metaNODE = Bitshares_Trustless_Client()
        nodes = metaNODE['whitelist']
        account_name = metaNODE['account_name']
        asset = metaNODE['asset']
        currency = metaNODE['currency']
        del metaNODE
        print('')
        print('      metaNODE = Bitshares_Trustless_Client()')
    except:
        raise ValueError('metaNODE not found')
    print('')
    time.sleep(0.3)
    print(cyan('CHOOSING whitelisted public API...'))
    time.sleep(0.3)
    print('')
    print('      ' + green(nodes[0]))
    print('')
    print(cyan('CONNECTING to DEX account...'))
    print('')

    valid = 0
    while not valid:
        try:
            USERNAME = account_name
            account = Account(
                USERNAME,
                bitshares_instance=BitShares(
                    nodes,
                    num_retries=5))
            valid = 1
        except Exception as e:
            print (type(e).__name__, 'try again...')
            pass
    print('      Welcome Back: ', green(USERNAME), blue(str(account)))
    print('')
    print(cyan('CONNECTING to DEX market...'))
    valid = 0
    while not valid:
        try:
            BitPAIR = asset + ':' + currency
            BitASSET = BitPAIR.split(':')[0]
            BitCURRENCY = BitPAIR.split(':')[1]
            market = Market(
                BitPAIR,
                bitshares_instance=BitShares(
                    nodes,
                    num_retries=5),
                mode='head')
            valid = 1
        except Exception as e:
            print (type(e).__name__, 'try again...')
            pass
    print('')
    print('   You are Trading: ', green(BitPAIR))
    print('')
    print(yellow(
        'Enter PASS PHRASE below to AUTHENTICATE or press ENTER to skip'))
    print(red(' YOU SHOULD UNDERSTAND THE SCRIPT BEFORE ENTERING PASS PHRASE'))

    print('')
    valid = 0
    default = ''
    while not valid:
        try:
            PASS_PHRASE = getpass(prompt='       PASS PHRASE: ') or default
            print(
                "\033[F       PASS PHRASE: " + green(
                    '********************************'))
            if PASS_PHRASE != '':
                print('')
                print(cyan('AUTHENTICATING to DEX wallet...'))
                market.bitshares.wallet.unlock(PASS_PHRASE)
                print('')
                print(red('*****************'))
                print(red('**AUTHENTICATED**') +
                      yellow(' YOUR WALLET IS UNLOCKED'))
                print(red('*****************'))
                valid = 1
            else:
                print('')
                print(yellow('SKIP AUTHENTICATION - YOUR WALLET IS LOCKED'))
                valid = 1
        except Exception as e:
            print (type(e).__name__, 'try again...')
            pass
    time.sleep(0.3)
    print('')
    print(
        cyan('VALIDATING mainnet DEX chain...'))
    print('')
    chain = Blockchain(
        bitshares_instance=BitShares(nodes, num_retries=5), mode='head')
    chain_id = chain.get_network()['chain_id']
    if chain_id != ID:
        print(cyan('INVALID CHAIN reconnecting...'))
        reconnect()
    print(' BITSHARES MAINNET: ', blue(chain_id))
    print('')
    time.sleep(0.3)
    print(cyan('LAUNCHING microDEX user interface...'))

    master = Tk()
    # master.geometry("650x950")
    master['bg'] = '#262626'
    master.title('microDEX - Bitshares Minimalist UI')

    elapsed('master')
    lock = StringVar()
    lock.set('AUTHENTICATED')
    if market.bitshares.wallet.locked():
        lock.set('WALLET LOCKED')
    elapsed('lock')

    header_text = Text(master, height=5, width=90, fg=blue2, bg=gray3)
    header_text.insert(END, '')
    header_text.grid(row=0, column=0, columnspan=4)

    bid_text = Text(master, height=30, width=45, fg=green1, bg=gray3)
    bid_text.insert(END, '')
    bid_text.grid(row=1, column=0, columnspan=2)
    bid_text.tag_configure("right", justify="right")
    bid_text.tag_configure("left", justify="left")

    ask_text = Text(master, height=30, width=45, fg=red1, bg=gray3)
    ask_text.insert(END, '')
    ask_text.grid(row=1, column=2, columnspan=2)

    orders_text = Text(master, height=11, width=45, fg=yellow1, bg=gray3)
    orders_text.insert(END, '')
    orders_text.grid(row=2, column=0, columnspan=2)

    history_text = Text(
        master,
        height=11,
        width=45,
        fg=gray1,
        bg=gray3)
    history_text.insert(END, '')
    history_text.grid(row=2, column=2, columnspan=2)

    account_text = Text(master, height=4, width=90, fg=blue1, bg=gray3)
    account_text.insert(END, '')
    account_text.grid(row=3, columnspan=4)

    elapsed('wireframe')

    Label(
        master,
        text="PRICE:",
        fg=gray1,
        bg=gray3).grid(
        row=4,
        column=0,
        sticky=E)
    Label(
        master,
        text="AMOUNT:",
        fg=gray1,
        bg=gray3).grid(
        row=5,
        column=0,
        sticky=E)
    Label(
        master,
        text="PRICE:",
        fg=gray1,
        bg=gray3).grid(
        row=4,
        column=2,
        sticky=E)
    Label(
        master,
        text="AMOUNT:",
        fg=gray1,
        bg=gray3).grid(
        row=5,
        column=2,
        sticky=E)
    Label(
        master,
        text="litepresence2018",
        fg=gray2,
        bg=gray3).grid(
        row=9,
        column=3,
        sticky=SE)
    Label(master, text=
          "   *ORDERS TAKE A FEW SECONDS TO APPEAR; CLICK ONCE, THEN CONFIRM*", fg='#C0C0C0', bg='#262626'
          ).grid(row=9, column=0, columnspan=4, sticky=W)

    try:
        # add bitshares logo to gui via imgur
        def downloadImage(imageUrl, localFileName):
            response = requests.get(imageUrl)
            with open(localFileName, 'wb') as fo:
                for chunk in response.iter_content(4096):
                    fo.write(chunk)
        try:
            photo = PhotoImage(file="bitshares_logo.gif")
        except:
            downloadImage(
                'https://i.imgur.com/fvCE86Z.gif',
                'bitshares_logo.gif')
            photo = PhotoImage(file="bitshares_logo.gif")
        label = Label(image=photo)
        label.image = photo
        label.grid(row=0, column=3, sticky=E)

    except:
        pass

    buy_price = Entry(master, fg=gray1, bg=gray2)
    buy_amount = Entry(master, fg=gray1, bg=gray2)
    sell_price = Entry(master, fg=gray1, bg=gray2)
    sell_amount = Entry(master, fg=gray1, bg=gray2)
    login = Entry(master, fg=gray1, bg=gray2)

    buy_price.grid(row=4, column=1)
    buy_amount.grid(row=5, column=1)
    sell_price.grid(row=4, column=3)
    sell_amount.grid(row=5, column=3)
    login.grid(row=8, column=1)
    elapsed('entry')

    Button(
        master,
        text='BUY',
        command=dex_buy, fg=gray1, bg=gray3, activebackground=green2, highlightbackground=green1).grid(
        row=7,
        column=1,
        # sticky=E,
        pady=4)
    Button(
        master,
        text='SELL',
        command=dex_sell, fg=gray1, bg=gray3, activebackground=red2, highlightbackground=red1).grid(
        row=7,
        column=3,
        # sticky=E,
        pady=4)
    Button(
        master,
        text='CANCEL ALL',
        command=dex_cancel, fg=gray1, bg=gray3, activebackground=yellow2, highlightbackground=yellow1).grid(
        row=7,
        column=0,
        sticky=E,
        pady=4)
    Button(
        master,
        text='LOCK/UNLOCK',
        command=dex_auth_gui, fg=gray1, bg=gray3, activebackground=blue2, highlightbackground=blue1).grid(
        row=8,
        column=0,
        sticky=E,
        pady=4)
    elapsed('button')
    Button(
        master,
        text='SWITCH NODE',
        command=switch, fg=gray1, bg=gray3, activebackground=blue2, highlightbackground=blue1).grid(
        row=8,
        column=3,
        sticky=E,
        pady=4)
    elapsed('button')

    update_id = 0
    ping = 0
    pings = [0]
    print(blue('''
    ===================================================================
          '''))
    print(cyan('           ' + time.ctime()))
    print(blue('''
    ===================================================================
          '''))
    print('')

    master.geometry('+9999+9999')
    master.after(1, update)
    master.mainloop()

if __name__ == "__main__":

    main()
