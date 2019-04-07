"""
metaNODE = Bitshares_Trustless_Client()

Trustless Public Node Statistical Curation Utility

******** WTFPL ALPHA RELEASE TO PUBLIC DOMAIN WITH NO WARRANTY *********

litepresence 2019
"""

# 99.99% uptime
# no rogue data, no stale data
# no hung processes, no runaway processes
# maintains whitelist of validated tested nodes for buy/sell/cancel ops
# no pybitshares dependencies
# metaNODE is a dict of account and market conditions for one DEX pair
# stored in json format in file metaNODE.txt
# it can be storage['access']ed by ANY script in ANY language
# this statistically curated data is updated every few seconds
# you can tail any of these live updated texts:
# metaNODE.txt
# metaNODElog.txt
# whitelist.txt
# blacklist.txt
# nodes.txt
# account_history.txt
# to access metaNODE data from any python scirpt:
# metaNODE = Bitshares_Trustless_Client()
# access time with SSD is about 0.0003 seconds

# STANDARD PYTHON MODULES
from time import time, sleep, ctime, strptime
from random import random, shuffle, choice
from multiprocessing import Process, Value
from json import loads as json_load
from json import dumps as json_dump
from traceback import format_exc
from datetime import datetime
from statistics import mode
from calendar import timegm
from sys import stdout
from os import popen

# MODULES WHICH MAY REQUIRE INSTALLATION
from requests import get as requests_get
from psutil import Process as psutil_Process
from websocket import create_connection as wss
from websocket import enableTrace


# ======================================================================
VERSION = "Bitshares metaNODE 0.00000020"
# ======================================================================
DEV = False
COLOR = True
MAVENS = 7  # 7
TIMEOUT = 100  # 100
PROCESSES = 20  # 20
MIN_NODES = 15  # 15
BOOK_DEPTH = 30  # 30
THRESH_PAUSE = 4  # 4
UTILIZATIONS = 30  # 30
HISTORY_DEPTH = 30  # 30
LATENCY_REPEAT = 900  # 900
LATENCY_TIMEOUT = 5  # 5
BIFURCATION_PAUSE = 2  # 2
# ======================================================================
ID = "4018d7844c78f6a6c41c6a552b898022310fc5dec06da467ee7905a8dad512c8"
# ======================================================================


# GLOBAL USER DEFINED WHITELIST
# ======================================================================
def public_nodes():
    """
    Static list of RPC nodes
    """
    # SEEN LIVE SINCE 181127
    return [
        "wss://altcap.io_count/wss",
        "wss://api-ru.bts.blckchnd.com/ws",
        "wss://api.bitshares.bhuz.info/wss",
        "wss://api.bitsharesdex.com/ws",
        "wss://api.bts.ai/ws",
        "wss://api.bts.blckchnd.com/wss",
        "wss://api.bts.mobi/wss",
        "wss://api.bts.network/wss",
        "wss://api.btsgo.net/ws",
        "wss://api.btsxchng.com/wss",
        "wss://api.dex.trading/ws",
        "wss://api.fr.bitsharesdex.com/ws",
        "wss://api.open-asset.tech/wss",
        "wss://atlanta.bitshares.apasia.tech/wss",
        "wss://australia.bitshares.apasia.tech/ws",
        "wss://b.mrx.im/wss",
        "wss://bit.btsabc.org/wss",
        "wss://bitshares.crypto.fans/wss",
        "wss://bitshares.cyberit.io_count/ws",
        "wss://bitshares.dacplay.org/wss",
        "wss://bitshares.dacplay.org:8089/wss",
        "wss://bitshares.openledger.info/wss",
        "wss://blockzms.xyz/ws",
        "wss://bts-api.lafona.net/ws",
        "wss://bts-seoul.clockwork.gr/ws",
        "wss://bts.liuye.tech:4443/wss",
        "wss://bts.open.icowallet.net/ws",
        "wss://bts.proxyhosts.info/wss",
        "wss://btsfullnode.bangzi.info/ws",
        "wss://btsws.roelandp.nl/ws",
        "wss://chicago.bitshares.apasia.tech/ws",
        "wss://citadel.li/node/wss",
        "wss://crazybit.online/wss",
        "wss://dallas.bitshares.apasia.tech/wss",
        "wss://dex.iobanker.com:9090/wss",
        "wss://dex.rnglab.org/ws",
        "wss://dexnode.net/ws",
        "wss://england.bitshares.apasia.tech/ws",
        "wss://eu-central-1.bts.crypto-bridge.org/wss",
        "wss://eu.nodes.bitshares.ws/ws",
        "wss://eu.openledger.info/ws",
        "wss://france.bitshares.apasia.tech/ws",
        "wss://frankfurt8.daostreet.com/wss",
        "wss://japan.bitshares.apasia.tech/wss",
        "wss://kc-us-dex.xeldal.com/ws",
        "wss://kimziv.com/ws",
        "wss://la.dexnode.net/ws",
        "wss://miami.bitshares.apasia.tech/ws",
        "wss://na.openledger.info/ws",
        "wss://ncali5.daostreet.com/wss",
        "wss://netherlands.bitshares.apasia.tech/ws",
        "wss://new-york.bitshares.apasia.tech/ws",
        "wss://node.bitshares.eu/ws",
        "wss://node.market.rudex.org/wss",
        "wss://nohistory.proxyhosts.info/wss",
        "wss://openledger.hk/wss",
        "wss://paris7.daostreet.com/wss",
        "wss://relinked.com/wss",
        "wss://scali10.daostreet.com/wss",
        "wss://seattle.bitshares.apasia.tech/wss",
        "wss://sg.nodes.bitshares.ws/ws",
        "wss://singapore.bitshares.apasia.tech/ws",
        "wss://status200.bitshares.apasia.tech/wss",
        "wss://us-east-1.bts.crypto-bridge.org/ws",
        "wss://us-la.bitshares.apasia.tech/ws",
        "wss://us-ny.bitshares.apasia.tech/ws",
        "wss://us.nodes.bitshares.ws/wss",
        "wss://valley.bitshares.apasia.tech/ws",
        "wss://ws.gdex.io_count/ws",
        "wss://ws.gdex.top/wss",
        "wss://ws.hellobts.com/wss",
        "wss://ws.winex.pro/wss",
    ]


# INTER PROCESS COMMUNICATION VIA TEXT
# ======================================================================
def Bitshares_Trustless_Client():
    """
    Include this definition in your script to storage['access'] metaNODE.txt
    Deploy your bot script in the same folder as metaNODE.py
    """
    while True:
        try:
            with open("metaNODE.txt", "r") as handle:
                ret = handle.read()  # .replace("'",'"')
                handle.close()
                metaNODE = json_load(ret)
                break
        except Exception as error:
            msg = trace(error)
            race_condition = ["Unterminated", "Expecting"]
            if any([x in str(error.args) for x in race_condition]):
                print("metaNODE = Bitshares_Trustless_Client() RACE READ")
            elif "metaNODE is blank" in str(error.args):
                continue
            else:
                print("metaNODE = Bitshares_Trustless_Client() " + msg)
            try:
                handle.close()
            except BaseException:
                pass
        finally:
            try:
                handle.close()
            except BaseException:
                pass
    return metaNODE


def race_append(doc="", text=""):
    """
    Concurrent Append to File Operation
    """
    iteration = 0
    while True:
        sleep(0.0001 * iteration ** 2)
        iteration += 1
        try:
            if iteration > 10:
                break
            with open(doc, "a+") as handle:
                handle.write(text)
                handle.close()
                break
        except Exception as error:
            print(trace(error))
            try:
                handle.close()
            except BaseException:
                pass
        finally:
            try:
                handle.close()
            except BaseException:
                pass


def race_write(doc="", text=""):
    """
    Concurrent Write to File Operation
    """
    if not isinstance(text, str):
        text = str(text)
    iteration = 0
    while True:
        sleep(0.0001 * iteration ** 2)
        iteration += 1
        try:
            with open(doc, "w+") as handle:
                handle.write(text)
                handle.close()
                break
        except Exception as error:
            print(trace(error))
            try:
                handle.close()
            except BaseException:
                pass
        finally:
            try:
                handle.close()
            except BaseException:
                pass


def race_read(doc=""):
    """
    Concurrent Read from File Operation
    """
    iteration = 0
    while True:
        sleep(0.0001 * iteration ** 2)
        iteration += 1
        try:
            with open(doc, "r") as handle:
                ret = handle.read().replace("'", '"')
                handle.close()
                try:
                    # ret = json_load(ret)
                    ret = json_load(ret)
                except BaseException:
                    try:
                        ret = ret.split("]")[0] + "]"
                        # ret = json_load(ret)
                        ret = json_load(ret)
                    except BaseException:
                        try:
                            ret = ret.split("}")[0] + "}"
                            # ret = ljson_load(ret)
                            ret = json_load(ret)
                        except BaseException:
                            print("race_read() failed %s" % str(ret))
                            if "{" in ret:
                                ret = {}
                            else:
                                ret = []
                break
        except FileNotFoundError:
            ret = []
        except Exception as error:
            if DEV:
                print(trace(error))
            try:
                handle.close()
            except BaseException:
                pass
        finally:
            try:
                handle.close()
            except BaseException:
                pass
    return ret


def watchdog():
    """
    Duplex keep alive communication to botscript
    """
    identity = 1  # metaNODE:1, botscript:0
    max_latency = 600
    while True:
        try:
            try:
                with open("watchdog.txt", "r") as handle:
                    ret = handle.read()
                    handle.close()
                ret = json_load(ret)
                response = int(ret[identity])
                now = int(time())
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
                    msg += " !!!!! WARNING: app is not responding !!!!!"
                return msg
            except Exception as error:
                print(trace(error))
                now = int(time())
                with open("watchdog.txt", "w+") as handle:
                    handle.write(str([now, now]))
                    handle.close()
                    break  # exit while loop
        except Exception as error:
            print(trace(error))
            try:
                handle.close()
            except BaseException:
                pass
        finally:
            try:
                handle.close()
            except BaseException:
                pass


# WEBSOCKET SEND AND RECEIVE
# ======================================================================
def wss_handshake(storage, node):
    """
    Create a websocket handshake
    """
    start = time()
    handshake_max = min(9.999, 10 * storage["mean_ping"])
    rpc = wss(node, timeout=handshake_max)
    handshake_latency = min(9.999, (time() - start))
    if 0 > handshake_latency > handshake_max:
        raise ValueError("slow handshake", handshake_latency)
    sleep(2)
    return rpc, handshake_latency, handshake_max


def wss_query(rpc, params):
    """
    Send and receive websocket requests
    """
    query = json_dump({"method": "call", "params": params, "jsonrpc": "2.0", "id": 1})
    rpc.send(query)
    ret = json_load(rpc.recv())
    try:
        return ret["result"]  # if there is result key take it
    except BaseException:
        return ret


# REMOTE PROCEDURE CALLS TO PUBLIC API DATABASE
# ======================================================================
def rpc_account_balances(rpc, cache, asset_ids, asset_precisions):
    """
    Gather account balances for current market and BTS balance
    """
    if "1.3.0" not in asset_ids:
        asset_ids.append("1.3.0")
        asset_precisions.append(5)
    ret = wss_query(
        rpc,
        ["database", "get_named_account_balances", [cache["account_name"], asset_ids]],
    )
    balances = {}
    for _, asset_id in enumerate(asset_ids):
        balances[asset_id] = 0
    for item, asset_id in enumerate(asset_ids):
        for _, balance in enumerate(ret):
            if balance["asset_id"] == asset_id:
                balances[asset_id] += (
                    float(balance["amount"]) / 10 ** asset_precisions[item]
                )
    return balances


def rpc_market_history(rpc, cache, now, then, depth=100):
    """
    Get recent recent transaction in this market
    """
    trade_history = wss_query(
        rpc,
        [
            "database",
            "get_trade_history",
            [cache["currency"], cache["asset"], now, then, depth],
        ],
    )
    history = []
    for _, value in enumerate(trade_history):
        unix = int(from_iso_date(value["date"]))
        price = precision(value["price"], 16)
        if float(price) == 0:
            raise ValueError("zero price in history")
        amount = precision(value["amount"], cache["asset_precision"])
        history.append([unix, price, amount])
    if not history:
        raise ValueError("no history")
    return history


def rpc_lookup_asset_symbols(rpc, cache):
    """
    Given asset names return asset ids and precisions
    """
    ret = wss_query(
        rpc, ["database", "lookup_asset_symbols", [[cache["asset"], cache["currency"]]]]
    )
    asset_id = ret[0]["id"]
    asset_precision = ret[0]["precision"]
    currency_id = ret[1]["id"]
    currency_precision = ret[1]["precision"]
    return asset_id, asset_precision, currency_id, currency_precision


def rpc_block_latency(rpc, storage):
    """
    Confirm the data contained on this node is not stale
    """
    dgp = wss_query(rpc, ["database", "get_dynamic_global_properties", []])
    blocktime = from_iso_date(dgp["time"])
    block_latency = min(9.999, (time() - blocktime))
    block_max = min(9.999, (3 + 3 * storage["mean_ping"]))
    if 0 > block_latency > block_max:
        raise ValueError("stale blocktime", block_latency)
    return block_latency, block_max, int(blocktime)


def rpc_lookup_accounts(rpc, cache):
    """
    Given account name return A.B.C account id
    """
    ret = wss_query(rpc, ["database", "lookup_accounts", [cache["account_name"], 1]])
    return ret[0][1]


def rpc_ping_latency(rpc, storage):
    """
    Confirm we have fast connection to a node on the correct chain
    """
    start = time()
    chain_id = wss_query(rpc, ["database", "get_chain_id", []])
    ping_latency = min(9.999, (time() - start))
    ping_max = min(2, 2 * storage["mean_ping"])
    if chain_id != ID:
        raise ValueError("chain_id != ID")
    if 0 > ping_latency > ping_max:
        raise ValueError("slow ping", ping_latency)
    return ping_latency, ping_max


def rpc_book(rpc, cache, depth=3):
    """
    Remote procedure call orderbook bids and asks
    """
    order_book = wss_query(
        rpc, ["database", "get_order_book", [cache["currency"], cache["asset"], depth]]
    )
    askp = []
    bidp = []
    askv = []
    bidv = []
    for i in range(len(order_book["asks"])):
        price = precision(order_book["asks"][i]["price"], 16)
        if float(price) == 0:
            raise ValueError("zero price in asks")
        volume = precision(order_book["asks"][i]["quote"], cache["asset_precision"])
        askp.append(price)
        askv.append(volume)
    for i in range(len(order_book["bids"])):
        price = precision(order_book["bids"][i]["price"], 16)
        if float(price) == 0:
            raise ValueError("zero price in bids")
        volume = precision(order_book["bids"][i]["quote"], cache["asset_precision"])
        bidp.append(price)
        bidv.append(volume)
    if float(bidp[0]) >= float(askp[0]):
        raise ValueError("mismatched orderbook")
    return askp, bidp, askv, bidv


def rpc_open_orders(rpc, cache):
    """
    Remote procedure call for open orders returns price as fraction,
    with unreferenced decimal point locations on both amounts,
    also reference by A.B.C instead of ticker symbol
    Gather data and post process to human readable from graphene
    """
    ret = wss_query(
        rpc, ["database", "get_full_accounts", [[cache["account_name"]], False]]
    )
    try:
        limit_orders = ret[0][1]["limit_orders"]
    except BaseException:
        limit_orders = []
    orders = []
    for order in limit_orders:
        base_id = order["sell_price"]["base"]["asset_id"]
        quote_id = order["sell_price"]["quote"]["asset_id"]
        if (base_id in [cache["currency_id"], cache["asset_id"]]) and (
            quote_id in [cache["currency_id"], cache["asset_id"]]
        ):
            amount = float(order["for_sale"])
            base_amount = float(order["sell_price"]["base"]["amount"])
            quote_amount = float(order["sell_price"]["quote"]["amount"])
            if base_id == cache["currency_id"]:
                base_precision = cache["currency_precision"]
                quote_precision = cache["asset_precision"]
            else:
                base_precision = cache["asset_precision"]
                quote_precision = cache["currency_precision"]
            base_amount /= 10 ** base_precision
            quote_amount /= 10 ** quote_precision
            if base_id == cache["asset_id"]:
                order_type = "sell"
                price = quote_amount / base_amount
                amount = amount / 10 ** base_precision
            else:
                order_type = "buy"
                price = base_amount / quote_amount
                amount = (amount / 10 ** base_precision) / price
            orders.append(
                {
                    "orderNumber": order["id"],
                    "orderType": order_type,
                    "market": cache["pair"],
                    "amount": precision(amount, cache["asset_precision"]),
                    "price": precision(price, 16),
                }
            )
    return sorted(orders, key=lambda k: k["price"])


def rpc_last(rpc, cache):
    """
    Get the latest ticker price
    """
    ticker = wss_query(
        rpc, ["database", "get_ticker", [cache["currency"], cache["asset"], False]]
    )
    last = precision(ticker["latest"], 16)
    if float(last) == 0:
        raise ValueError("zero price last")
    return last


# STATISTICAL DATA CURATION
# ======================================================================
def thresh(storage, process, epoch, pid, cache):
    """
    Make calls for data, shake out any errors
    There are 20 threshing process running in parallel
    They are each periodically terminated and respawned
    """
    handshake_bs = []
    ping_bs = []
    block_bs = []
    reject_bs = []
    storage["access"] = 0
    storage["data_latency"] = 0
    while True:
        storage["mean_ping"] = 0.5
        try:
            nodes = get_nodes()
            static_nodes = public_nodes()
            shuffle(nodes)
            node = nodes[0]
            storage["bw_depth"] = max(int(len(nodes) / 6), 1)
            # CHECK BLACK AND WHITE LISTS
            black = race_read(doc="blacklist.txt")[-storage["bw_depth"] :]
            white = race_read(doc="whitelist.txt")[-storage["bw_depth"] :]
            try:
                start = time()
                metaNODE = Bitshares_Trustless_Client()
                storage["access"] = time() - start
                ping = storage["mean_ping"] = metaNODE["ping"]
                blacklist = metaNODE["blacklist"][-storage["bw_depth"] :]
                whitelist = metaNODE["whitelist"][-storage["bw_depth"] :]
                blocktime = metaNODE["blocktime"]
                storage["data_latency"] = time() - blocktime
                del metaNODE
                if len(blacklist) > len(black):
                    black = blacklist
                    race_write("blacklist.txt", json_dump(black))
                if len(whitelist) > len(white):
                    white = whitelist
                    race_write("whitelist.txt", json_dump(white))
            except BaseException:
                pass
            if node in black:
                raise ValueError("blacklisted")
            if node in white:
                raise ValueError("whitelisted")
            # connect to websocket
            rpc, handshake_latency, handshake_max = wss_handshake(storage, node)
            # use each node several times
            utilizations = UTILIZATIONS
            if (time() - cache["begin"]) < 100:
                utilizations = 1
            for util in range(utilizations):
                sleep(THRESH_PAUSE)
                # Database calls w/ data validations
                ping_latency, ping_max = rpc_ping_latency(rpc, storage)
                block_latency, block_max, blocktime = rpc_block_latency(rpc, storage)
                set_timing = "                  " + "speed/max/ratio/cause/rate"
                if handshake_max == 5:
                    set_timing = "                  " + it(
                        "red", "RESOLVING MEAN NETWORK SPEED"
                    )
                # timing analysis for development
                ping_r = ping_latency / ping_max
                block_r = block_latency / block_max
                handshake_r = handshake_latency / handshake_max
                ping_b = int(bool(int(ping_r)))
                block_b = int(bool(int(block_r)))
                handshake_b = int(bool(int(handshake_r)))
                reject_b = int(bool(ping_b + block_b + handshake_b))
                ping_bs.append(ping_b)
                block_bs.append(block_b)
                reject_bs.append(reject_b)
                handshake_bs.append(handshake_b)
                ping_bs = ping_bs[-100:]
                block_bs = block_bs[-100:]
                reject_bs = reject_bs[-100:]
                handshake_bs = handshake_bs[-100:]
                ping_p = sum(ping_bs) / len(ping_bs)
                block_p = sum(block_bs) / len(block_bs)
                reject_p = sum(reject_bs) / len(reject_bs)
                handshake_p = sum(handshake_bs) / len(handshake_bs)
                ping_b = str(ping_b).ljust(7)
                block_b = str(block_b).ljust(7)
                handshake_b = str(handshake_b).ljust(7)
                reject = "".ljust(7)
                if reject_b:
                    reject = it("red", "X".ljust(7))
                optimizing = it("red", "OPTIMIZING".ljust(7))
                if (time() - cache["begin"]) > 200:
                    optimizing = "".ljust(7)
                # last, history, orderbook, balances, orders
                last = float(rpc_last(rpc, cache))
                now = to_iso_date(time())
                then = to_iso_date(time() - 3 * 86400)
                history = rpc_market_history(rpc, cache, now, then, depth=HISTORY_DEPTH)
                askp, bidp, askv, bidv = rpc_book(rpc, cache, depth=BOOK_DEPTH)
                ids = [cache["asset_id"], cache["currency_id"]]
                precisions = [cache["asset_precision"], cache["currency_precision"]]
                balances = rpc_account_balances(
                    rpc, cache, asset_ids=ids, asset_precisions=precisions
                )
                bts_balance = float(balances["1.3.0"])
                asset_balance = float(balances[cache["asset_id"]])
                currency_balance = float(balances[cache["currency_id"]])
                orders = rpc_open_orders(rpc, cache)
                # CPU, RAM, io_count data REQUIRES MODULE INSTALL
                try:
                    proc = psutil_Process()
                    descriptors = proc.num_fds()
                    usage = (
                        "grep 'cpu ' /proc/stat | awk "
                        + "'{usage=($2+$4)*100/($2+$4+$5)}"
                        + " END {print usage }' "
                    )
                    cpu = "%.3f" % (float(popen(usage).readline()))
                    ram = "%.3f" % (100 * float(proc.memory_percent()))
                    io_count = list(proc.io_counters())[:2]
                except Exception as error:
                    if DEV:
                        print(trace(error))
                watchdog_latency = watchdog()
                metaNODE = Bitshares_Trustless_Client()
                buy_orders = 0
                currency_holding = 0
                currency_max = 0
                sell_orders = 0
                asset_holding = 0
                asset_max = 0
                invested = 0
                divested = 0
                ping = 0.5
                keys = ["bifurcating the metaNODE...."]
                m_orders = orders
                m_history = history
                m_last = last
                m_askp = askp
                m_bidp = bidp
                m_askv = askv
                m_bidv = bidv
                m_bts_balance = bts_balance
                m_asset_balance = asset_balance
                m_currency_balance = currency_balance
                try:
                    buy_orders = metaNODE["buy_orders"]
                    currency_holding = metaNODE["currency_holding"]
                    currency_max = metaNODE["currency_max"]
                    sell_orders = metaNODE["sell_orders"]
                    asset_holding = metaNODE["asset_holding"]
                    asset_max = metaNODE["asset_max"]
                    invested = metaNODE["invested"]
                    divested = metaNODE["divested"]
                    keys = metaNODE["keys"]
                    ping = storage["mean_ping"] = metaNODE["ping"]
                    m_orders = metaNODE["orders"]
                    m_history = metaNODE["history"]
                    m_last = metaNODE["last"]
                    m_askp = metaNODE["book"]["askp"]
                    m_bidp = metaNODE["book"]["bidp"]
                    m_askv = metaNODE["book"]["askv"]
                    m_bidv = metaNODE["book"]["bidv"]
                    m_bts_balance = metaNODE["bts_balance"]
                    m_asset_balance = metaNODE["asset_balance"]
                    m_currency_balance = metaNODE["currency_balance"]
                except BaseException:
                    pass
                del metaNODE
                runtime = int(time()) - cache["begin"]
                # storage['bw_depth'] = max(int(len(nodes) / 6), 1)
                if (len(white) < storage["bw_depth"]) or (
                    len(black) < storage["bw_depth"]
                ):
                    alert = it("red", "    BUILDING BLACK AND WHITE LISTS")
                else:
                    alert = ""
                if nodes == static_nodes:
                    alert += " ::WARN:: USING STATIC NODE LIST"
                # in the event data passes all tests, then:
                # print, winnow the node, and nascent trend the maven
                print_market(storage, cache)
                print(keys)
                print("")
                print("runtime:epoch:pid", runtime, epoch, pid)
                try:
                    print("fds:processes    ", descriptors, process, "of", PROCESSES)
                except BaseException:
                    print("processes    ", process, "of", PROCESSES)
                try:
                    print("cpu:ram:io_count ", cpu, ram, io_count)
                except BaseException:
                    pass
                print("utilization:node ", str(util + 1).ljust(3), node)
                print(
                    "total:white:black",
                    len(static_nodes),
                    len(nodes),
                    len(white),
                    len(black),
                    alert,
                )
                print(set_timing)
                print(
                    "block latency    ",
                    "%.2f %.1f %.1f %s %.2f"
                    % (block_latency, block_max, block_r, block_b, block_p),
                )
                print(
                    "handshake        ",
                    "%.2f %.1f %.1f %s %.2f"
                    % (
                        handshake_latency,
                        handshake_max,
                        handshake_r,
                        handshake_b,
                        handshake_p,
                    ),
                )
                print(
                    "ping             ",
                    "%.2f %.1f %.1f %s %.2f"
                    % (ping_latency, ping_max, ping_r, ping_b, ping_p),
                )
                print(
                    "mean ping        ",
                    (it("yellow", ("%.3f" % ping))),
                    "       %s %.2f" % (reject, reject_p),
                    optimizing,
                )
                print(
                    "                 ",
                    [
                        x.rjust(16, " ")
                        for x in [
                            "name",
                            "balance",
                            "orders",
                            "holding",
                            "max",
                            "percent",
                        ]
                    ],
                )
                print(
                    "currency         ",
                    it(
                        "cyan",
                        [
                            str(x).rjust(16, " ")
                            for x in [
                                cache["currency"],
                                m_currency_balance,
                                buy_orders,
                                currency_holding,
                                currency_max,
                                divested,
                            ]
                        ],
                    ),
                )
                print(
                    "assets           ",
                    it(
                        "cyan",
                        [
                            str(x).rjust(16, " ")
                            for x in [
                                cache["asset"],
                                m_asset_balance,
                                sell_orders,
                                asset_holding,
                                asset_max,
                                invested,
                            ]
                        ],
                    ),
                )
                print("bitshares        ", m_bts_balance, "BTS")
                print("")
                print(
                    "history      ",
                    it("yellow", ("%.16f" % m_last)),
                    "LAST with depth",
                    len(m_history),
                )
                for item in range(3):
                    print(it("blue", m_history[item]))
                print("")
                print("asks depth       ", len(m_askp))
                for item in range(3):
                    print(it("red", precision(m_askp[item], 16)), m_askv[item])
                print("bids depth       ", len(m_bidp))
                for item in range(3):
                    print(it("green", precision(m_bidp[item], 16)), m_bidv[item])
                print("")
                print("open orders      ", len(m_orders))
                for order in m_orders:
                    print(it("yellow", order))
                print("")
                print("watchdog latency:", watchdog_latency)
                print("")
                # send the maven dictionary to nascent_trend()
                # Must be JSON type
                # 'STRING', 'INT', 'FLOAT', '{DICT}', or '[LIST]'
                maven = {}
                maven["ping"] = (19 * storage["mean_ping"] + ping_latency) / 20  # FLOAT
                maven["bidv"] = bidv  # LIST of precision() STRINGS
                maven["askv"] = askv  # LIST of precision() STRINGS
                maven["bidp"] = bidp  # LIST of precision() STRINGS
                maven["askp"] = askp  # LIST of precision() STRINGS
                maven["bts_balance"] = bts_balance  # FLOAT
                maven["currency_balance"] = currency_balance  # FLOAT
                maven["asset_balance"] = asset_balance  # FLOAT
                maven["market_history"] = history  # LIST OF LISTS
                maven["orders"] = orders  # LIST
                maven["last"] = last  # precision() STRING
                maven["whitelist"] = white  # LIST
                maven["blacklist"] = black  # LIST
                maven["blocktime"] = blocktime  # INT
                nascent_trend(maven)
                # winnow this node to the whitelist
                winnow(storage, "whitelist", node)
                # clear namespace
                del maven
                del bidv
                del askv
                del bidp
                del askp
                del bts_balance
                del currency_balance
                del asset_balance
                del history
                del orders
                del last
                del io_count
                del alert
                del currency_max
                del balances
                del buy_orders
                del ram
                del sell_orders
                del cpu
                del asset_max
                del keys
                del watchdog_latency
                del asset_holding
                del divested
                del now
                del invested
                del runtime
                del currency_holding
                del descriptors
                del proc
            try:
                sleep(0.0001)
                rpc.close()
            except Exception as error:
                if DEV:
                    print(trace(error))
            continue
        except Exception as error:
            try:
                if DEV:
                    print(trace(error))
                sleep(0.0001)
                rpc.close()
            except BaseException:
                pass
            try:
                msg = trace(error) + node
                if (
                    ("ValueError" not in msg)
                    and ("StatisticsError" not in msg)
                    and ("result" not in msg)
                    and ("timeout" not in msg)
                    and ("SSL" not in msg)
                ):
                    if (
                        ("WebSocketTimeoutException" not in msg)
                        and ("WebSocketBadStatusException" not in msg)
                        and ("WebSocketAddressException" not in msg)
                        and ("ConnectionResetError" not in msg)
                        and ("ConnectionRefusedError" not in msg)
                    ):
                        msg += "\n" + str(format_exc())
                if DEV:  # or ((time() - cache["begin"]) > 60):
                    print(msg)
                if "listed" not in msg:
                    race_append(doc="metaNODElog.txt", text=msg)
                winnow(storage, "blacklist", node)
                del msg
            except BaseException:
                pass
            continue


def get_cache(storage, cache, nodes):
    """
    Acquire and store account id; asset ids, and asset precisions
    This is called once prior to spawning additional processes
    """
    storage["bw_depth"] = 10

    def wwc(cache):
        """
        Winnowing Websocket Connections...
        """
        print("\033c")
        cache = logo(cache)
        print("")
        print(ctime(), "\n")
        print(wwc.__doc__, "\n")

    account_ids, asset_ids, currency_ids = [], [], []
    asset_precisions, currency_precisions = [], []
    # trustless of multiple nodes
    while True:
        try:
            wwc(cache)
            black = race_read(doc="blacklist.txt")
            white = race_read(doc="whitelist.txt")
            # switch nodes
            nodes = get_nodes()
            shuffle(nodes)
            node = nodes[0]
            print(node)
            if node in black:
                raise ValueError("blacklisted")
            if node in white:
                raise ValueError("whitelisted")
            # reconnect and make calls
            rpc, _, _ = wss_handshake(storage, node)
            account_id = rpc_lookup_accounts(rpc, cache)
            (
                asset_id,
                asset_precision,
                currency_id,
                currency_precision,
            ) = rpc_lookup_asset_symbols(rpc, cache)
            # prepare for statistical mode of cache items
            asset_ids.append(asset_id)
            account_ids.append(account_id)
            currency_ids.append(currency_id)
            asset_precisions.append(asset_precision)
            currency_precisions.append(currency_precision)
            # mode of cache
            if len(asset_ids) > 4:
                try:
                    cache["begin"] = int(time())
                    cache["asset_id"] = mode(asset_ids)
                    cache["account_id"] = mode(account_ids)
                    cache["currency_id"] = mode(currency_ids)
                    cache["asset_precision"] = mode(asset_precisions)
                    cache["currency_precision"] = mode(currency_precisions)
                    enableTrace(False)
                    print_market(storage, cache)
                    winnow(storage, "whitelist", node)
                    break
                except BaseException:
                    winnow(storage, "blacklist", node)
                    continue
        except Exception as error:
            print(trace(error))
            continue
    return storage, cache


def winnow(storage, list_type, node):
    """
    Seperate good nodes from bad
    """
    if list_type == "blacklist":
        black = race_read(doc="blacklist.txt")
        if isinstance(black, list):
            if node in black:
                black.remove(node)
            black.append(node)
            black = black[-storage["bw_depth"] :]
            race_write(doc="blacklist.txt", text=black)
        else:
            race_write(doc="blacklist.txt", text=[node])
    if list_type == "whitelist":
        white = race_read(doc="whitelist.txt")
        if isinstance(white, list):
            if node in white:
                white.remove(node)
            white.append(node)
            white = white[-storage["bw_depth"] :]
            race_write(doc="whitelist.txt", text=white)
        else:
            race_write(doc="whitelist.txt", text=[node])
    try:
        del white
        del black
        del node
    except BaseException:
        pass


def bifurcation(storage, cache):
    """
    Given 7 dictionaries of data (mavens) find the most common
    Send good (statistical mode) data to metaNODE
    """
    while True:
        try:
            sleep(BIFURCATION_PAUSE)  # take a deep breath
            # initialize the metaNODE dictionary
            metaNODE = {}
            # initialize lists to sort data from each maven by key
            bidp = []
            askp = []
            bidv = []
            askv = []
            bts_balance = []
            currency_balance = []
            asset_balance = []
            history = []
            last = []
            whitelist = []
            blacklist = []
            blocktime = []
            orders = []
            pings = []
            # gather list of maven opinions from the nascent_trend()
            mavens = race_read(doc="mavens.txt")
            # sort maven data for statistical mode analysis by key
            len_m = len(mavens)
            for i in range(len_m):
                maven = mavens[i]
                bts_balance.append(maven["bts_balance"])
                currency_balance.append(maven["currency_balance"])
                asset_balance.append(maven["asset_balance"])
                last.append(maven["last"])
                blocktime.append(maven["blocktime"])
                whitelist.append(maven["whitelist"])
                blacklist.append(maven["blacklist"])
                pings.append(maven["ping"])
                # stringify lists for statistical mode of json text
                bidp.append(json_dump(maven["bidp"]))
                askp.append(json_dump(maven["askp"]))
                bidv.append(json_dump(maven["bidv"]))
                askv.append(json_dump(maven["askv"]))
                history.append(json_dump(maven["market_history"]))
                orders.append(json_dump(maven["orders"]))
            # the mean ping of the mavens is passed to the metaNODE
            ping = int(1000 * sum(pings) / (len(pings) + 0.00000001)) / 1000.0
            ping = min(1, ping)
            # find the youngest bitshares blocktime in our dataset
            try:
                blocktime = max(blocktime)
            except BaseException:
                print("validating the nascent trend...")
                continue
            # get the mode of the mavens for each metric
            # allow 1 or 2 less than total & most recent for mode
            # accept "no mode" statistics error as possibility
            try:
                bts_balance = mode(bts_balance)
            except BaseException:
                try:
                    bts_balance = mode(bts_balance[-(len_m - 1) :])
                except BaseException:
                    bts_balance = mode(bts_balance[-(len_m - 2) :])
            try:
                currency_balance = mode(currency_balance)
            except BaseException:
                try:
                    currency_balance = mode(currency_balance[-(len_m - 1) :])
                except BaseException:
                    currency_balance = mode(currency_balance[-(len_m - 2) :])
            try:
                asset_balance = mode(asset_balance)
            except BaseException:
                try:
                    asset_balance = mode(asset_balance[-(len_m - 1) :])
                except BaseException:
                    asset_balance = mode(asset_balance[-(len_m - 2) :])
            try:
                last = mode(last)
            except BaseException:
                try:
                    last = mode(last[-(len_m - 1) :])
                except BaseException:
                    last = mode(last[-(len_m - 2) :])
            try:
                bidp = mode(bidp)
            except BaseException:
                try:
                    bidp = mode(bidp[-(len_m - 1) :])
                except BaseException:
                    bidp = mode(bidp[-(len_m - 2) :])
            try:
                askp = mode(askp)
            except BaseException:
                try:
                    askp = mode(askp[-(len_m - 1) :])
                except BaseException:
                    askp = mode(askp[-(len_m - 2) :])
            try:
                bidv = mode(bidv)
            except BaseException:
                try:
                    bidv = mode(bidv[-(len_m - 1) :])
                except BaseException:
                    bidv = mode(bidv[-(len_m - 2) :])
            try:
                askv = mode(askv)
            except BaseException:
                try:
                    askv = mode(askv[-(len_m - 1) :])
                except BaseException:
                    askv = mode(askv[-(len_m - 2) :])
            try:
                history = mode(history)
            except BaseException:
                try:
                    history = mode(history[-(len_m - 1) :])
                except BaseException:
                    history = mode(history[-(len_m - 2) :])
            try:
                orders = mode(orders)
            except BaseException:
                try:
                    orders = mode(orders[-(len_m - 1) :])
                except BaseException:
                    orders = mode(orders[-(len_m - 2) :])
            # convert statistical mode string back to python object
            history = json_load(history)
            orders = json_load(orders)
            bidp = json_load(bidp)
            askp = json_load(askp)
            bidv = json_load(bidv)
            askv = json_load(askv)
            # attempt a full whitelist and blacklist
            white_l = []
            for i in whitelist:
                white_l += i
            whitelist = list(set(white_l))[-storage["bw_depth"] :]
            black_l = []
            for i in blacklist:
                black_l += i
            blacklist = list(set(black_l))[-storage["bw_depth"] :]
            # rebuild orderbook as 4 key dict with lists of floats
            bidp = [float(i) for i in bidp]
            bidv = [float(i) for i in bidv]
            askp = [float(i) for i in askp]
            askv = [float(i) for i in askv]
            book = {"bidp": bidp, "bidv": bidv, "askp": askp, "askv": askv}
            # calculate total outstanding orders
            buy_orders = 0
            sell_orders = 0
            for order in orders:
                if order["orderType"] == "buy":
                    buy_orders += float(order["amount"]) * float(order["price"])
                if order["orderType"] == "sell":
                    sell_orders += float(order["amount"])
            buy_orders = float(precision(buy_orders, cache["currency_precision"]))
            sell_orders = float(precision(sell_orders, cache["asset_precision"]))
            # provide some metadata regarding account balances
            currency_holding = float(currency_balance) + float(buy_orders)
            asset_holding = float(asset_balance) + float(sell_orders)
            currency_max = currency_holding + asset_holding * float(last)
            asset_max = currency_max / float(last)
            invested = 100 * asset_holding / (0.00000000001 + asset_max)
            divested = 100 - invested
            currency_holding = float(
                precision(currency_holding, cache["currency_precision"])
            )
            asset_holding = float(precision(asset_holding, cache["asset_precision"]))
            currency_max = float(precision(currency_max, cache["currency_precision"]))
            asset_max = float(precision(asset_max, cache["asset_precision"]))
            invested = float(precision(invested, 1))
            divested = float(precision(divested, 1))
            # if you made it this far without statistics error
            # truncate and rewrite the metaNODE with curated data
            # Must be JSON type
            # 'STRING', 'INT', 'FLOAT', '{DICT}', or '[LIST]'
            metaNODE["ping"] = ping  # FLOAT about 0.500
            metaNODE["book"] = book  # DICTIONARY
            metaNODE["bts_balance"] = float(bts_balance)  # FLOAT
            metaNODE["currency_balance"] = float(currency_balance)  # FLOAT
            metaNODE["asset_balance"] = float(asset_balance)  # FLOAT
            metaNODE["history"] = history  # LIST
            metaNODE["orders"] = orders  # LIST
            metaNODE["last"] = float(last)  # FLOAT
            metaNODE["whitelist"] = whitelist  # LIST
            metaNODE["blacklist"] = blacklist  # LIST
            metaNODE["blocktime"] = int(blocktime)  # INT
            metaNODE["account_name"] = cache["account_name"]  # STRING
            metaNODE["account_id"] = cache["account_id"]  # STRING A.B.C
            metaNODE["asset"] = cache["asset"]  # STRING SYMBOL
            metaNODE["asset_id"] = cache["asset_id"]  # STRING A.B.C
            metaNODE["asset_precision"] = int(cache["asset_precision"])  # INT
            metaNODE["currency"] = cache["currency"]  # STRING SYMBOL
            metaNODE["currency_id"] = cache["currency_id"]  # STRING A.B.C
            metaNODE["pair"] = cache["pair"]  # STRING A:B
            metaNODE["currency_precision"] = int(cache["currency_precision"])
            metaNODE["buy_orders"] = float(buy_orders)  # FLOAT
            metaNODE["sell_orders"] = float(sell_orders)  # FLOAT
            metaNODE["currency_holding"] = currency_holding  # FLOAT
            metaNODE["asset_holding"] = asset_holding  # FLOAT
            metaNODE["currency_max"] = currency_max  # FLOAT
            metaNODE["asset_max"] = asset_max  # FLOAT
            metaNODE["invested"] = invested  # FLOAT 0 to 1
            metaNODE["divested"] = divested  # FLOAT 0 to 1
            # add index to metaNODE
            metaNODE["keys"] = list(metaNODE.keys())
            # solitary process with write storage['access'] to metaNODE.txt
            metaNODE = json_dump(metaNODE)
            race_write(doc="metaNODE.txt", text=metaNODE)
            print("metaNODE.txt updated")
            # clear namespace
            del metaNODE
            del mavens
            del maven
            del bidp
            del askp
            del bidv
            del askv
            del bts_balance
            del currency_balance
            del asset_balance
            del history
            del last
            del whitelist
            del blacklist
            del blocktime
            del orders
            del len_m
            del currency_max
            del book
            del black_l
            del white_l
            del currency_holding
            del asset_max
            del divested
            del invested
            del buy_orders
            del asset_holding
            del sell_orders
        except Exception as error:  # wait a second and try again
            # common msg is "no mode statistics error"
            if DEV:
                msg = trace(error)
                print(msg)
                race_append(doc="metaNODElog.txt", text=msg)
            continue  # from top of while loop NOT pass through error


def latency_test(storage):
    """
    In loop, latency test the static list to produce nodes.txt
    Qualify round 1 = good chain id, 1000ms ping, 5000ms handshake
    All three ending suffixes are tested for each static list domain
    Only one of each suffix is allowed to pass
    latency() itself is a is a multiprocess child of spawn
    All tests done by latency() are multiprocess timeout wrapped
    """

    def test(node, signal, storage):
        """
        < 5 second hanshake
        < 1 second ping AND good chain id
        < 4.5 second blocktime
        """
        try:
            rpc, _, _ = wss_handshake(storage, node)
            rpc_ping_latency(rpc, storage)
            rpc_block_latency(rpc, storage)
            signal.value = 1  # if no exceptions pipe true response
        except BaseException:
            signal.value = 0

    def validate(unique):
        """
        remove suffixes for each domain, then remove duplicates
        """
        for item, unique_item in enumerate(unique):
            if unique_item.endswith("/"):
                unique[item] = unique_item[:-1]
        for item, unique_item in enumerate(unique):
            if unique_item.endswith("/ws"):
                unique[item] = unique_item[:-3]
        for item, unique_item in enumerate(unique):
            if unique_item.endswith("/wss"):
                unique[item] = unique_item[:-4]
        return sorted(list(set(unique)))

    def suffix(no_suffix):
        """
        add suffixes of each type for each validated domain
        """
        wss_suffix = [(i + "/wss") for i in no_suffix]
        ws_suffix = [(i + "/ws") for i in no_suffix]
        suffixed = no_suffix + wss_suffix + ws_suffix
        return sorted(suffixed)

    static_nodes = public_nodes()
    while True:
        start = time()
        whitelist = []
        blacklist = []
        suffixed_nodes = suffix(validate(static_nodes))
        for node in suffixed_nodes:
            # do not retest whitelisted domains with another suffix
            if validate([node])[0] not in validate(whitelist):
                # wrap test in timed multiprocess
                signal = Value("d", 0)
                t_process = Process(target=test, args=(node, signal, storage))
                t_process.daemon = False
                t_process.start()
                t_process.join(LATENCY_TIMEOUT)
                # kill hung process and blacklist the node
                if t_process.is_alive():
                    t_process.join()
                    t_process.terminate()
                    blacklist.append(node)
                # bad chain id, ping, handshake, or blocktime
                elif signal.value == 0:
                    blacklist.append(node)
                # good chain id, ping, handshake, and blocktime
                elif signal.value == 1:
                    # if domain is not already in list
                    whitelist.append(node)
        # nodes.txt is used as metaNODE's primary universe
        race_write("nodes.txt", json_dump(whitelist))
        race_write("blacklist2.txt", json_dump(blacklist))
        # repeat latency testing periodically per LATENCY_REPEAT
        sleep(max(0, (LATENCY_REPEAT - (time() - start))))


def spawn(storage, cache):
    """
    Multiprocessing handler spawns all parallel processes
    """
    # initialize one latency testing process
    l_process = Process(target=latency_test, args=(storage,))
    l_process.daemon = False
    l_process.start()
    # initialize one bifurcation process
    b_process = Process(target=bifurcation, args=(storage, cache))
    b_process.daemon = False
    b_process.start()
    # initialize one portfolio history log
    h_process = Process(target=log_account_history)
    h_process.daemon = False
    h_process.start()
    # initialize multiple threshing processes
    epoch = 0
    proc_id = 0
    multinode = {}
    for proc in range(PROCESSES):
        proc_id += 1
        multinode[str(proc)] = Process(
            target=thresh, args=(storage, proc, epoch, proc_id, cache)
        )
        multinode[str(proc)].daemon = False
        multinode[str(proc)].start()
        sleep(0.01)
    # kill and respawn threshing processes periodically for durability
    # even if anything gets hung metaNODE always moves on
    # a = process of PROCESSES; b = respawn epoch; c = process id
    # every time a process is respawned it gets new process id
    while True:
        epoch += 1
        race_write(doc="metaNODElog.txt", text="")
        for proc in range(PROCESSES):
            proc_id += 1
            sleep(TIMEOUT / 2 + TIMEOUT * random())
            try:
                multinode[str(proc)].terminate()
            except Exception as error:
                msg = trace(error)
                print("terminate() WARNING", msg)
                race_append(doc="metaNODElog.txt", text=msg)
            try:
                multinode[str(proc)] = Process(
                    target=thresh, args=(storage, proc, epoch, proc_id, cache)
                )
                multinode[str(proc)].daemon = False
                multinode[str(proc)].start()
            except Exception as error:
                msg = trace(error)
                print("process() WARNING", msg)
                race_append(doc="metaNODElog.txt", text=msg)


def nascent_trend(maven):
    """
    Append data from recently polled node to vetted list of dictionaries
    """
    mavens = race_read(doc="mavens.txt")
    if isinstance(mavens, list):
        mavens.append(maven)
        mavens = mavens[-MAVENS:]
        race_write(doc="mavens.txt", text=json_dump(mavens))
    else:
        race_write(doc="mavens.txt", text=json_dump([maven]))
    del mavens


# HELPER FUNCTIONS
# ======================================================================
def print_market(storage, cache):
    """
    metaNODE header containing with cached values
    """
    print("\033c")
    cache = logo(cache)
    print("")
    print(
        ctime(),
        it("yellow", ("%.5f" % storage["access"])),
        "read",
        it("yellow", ("%.1f" % storage["data_latency"])),
        "data",
    )
    print("==================================================")
    print("account   ", cache["account_name"], cache["account_id"])
    print(
        "currency  ",
        cache["currency"],
        cache["currency_id"],
        cache["currency_precision"],
    )
    print("asset     ", cache["asset"], cache["asset_id"], cache["asset_precision"])
    print("==================================================")
    print("")


def remove_chars(string, chars):
    """
    Return string without given characters
    """
    return "".join([c for c in string if c not in set(chars)])


def precision(number, places):
    """
    String representation of float to n decimal places
    """
    return ("%." + str(places) + "f") % float(number)


def log_account_history():
    """
    Logs snapshot of account balance to file periodically
    """
    while True:
        sleep(3)
        metaNODE = Bitshares_Trustless_Client()
        if metaNODE:
            try:
                keys = ["currency", "asset", "currency_max", "asset_max", "invested"]
                snapshot = {k: metaNODE[k] for k in keys}
                snapshot["unix"] = int(time())
                race_append(doc="account_history.txt", text=json_dump(snapshot))
                sleep(3600)
            except Exception as error:
                msg = trace(error)
                if DEV:
                    print(msg)
                race_append(doc="metaNODElog.txt", text=msg)
                sleep(30)


def from_iso_date(date):
    """
    Unix epoch given iso8601 datetime
    """
    return int(timegm(strptime(str(date), "%Y-%m-%dT%H:%M:%S")))


def to_iso_date(unix):
    """
    iso8601 datetime given unix epoch
    """
    return datetime.utcfromtimestamp(int(unix)).isoformat()


def ascii_logo(design):
    """
    Gather ascii artwork stored externally at pastebin.com
    """
    urls = {
        "bitshares": "https://pastebin.com/raw/xDJkyBrS",
        "microdex": "https://pastebin.com/raw/3DYAUqQR",
        "extinction-event": "https://pastebin.com/raw/5YuEHcC4",
        "metanode": "https://pastebin.com/raw/VALMtPjL",
    }
    try:
        return (requests_get(urls[design], timeout=(6, 30))).text
    except BaseException:
        return ""


def it(style, text):
    """
    Color printing in terminal
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


def welcome(cache):
    """
    Announce version and print logo, log current local time
    """
    print("\033c")
    race_write(doc="metaNODElog.txt", text=str(ctime()))
    cache = logo(cache)
    return cache


def version(cache):
    """
    Get version number from VERSION name
    Label terminal window
    """
    cache["version_number"] = "".join(item for item in VERSION if item in "0123456789.")
    stdout.write("\x1b]2;" + "Bitshares metaNODE" + "\x07")  # terminal title bar
    return cache


def sign_in(cache):
    """
    Input Account and Market, or press Enter for demo
    """
    print(
        """
        (BTS) litepresence1
        Resistance and Disobedience in Economic Activity
        is the Most Moral Human Action Possible
        -SEK3
        """
    )
    print("")
    print(sign_in.__doc__)
    print("")
    cache["account_name"] = input("account name: ").strip('"').strip("'")
    print("")
    cache["currency"] = input("    currency: ").strip('"').strip("'").upper()
    print("")
    cache["asset"] = input("       asset: ").strip('"').strip("'").upper()
    print("")
    if cache["account_name"] == "":
        cache["account_name"] = "abc123"
    if cache["currency"] == "":
        cache["currency"] = "OPEN.BTC"
    if cache["asset"] == "":
        cache["asset"] = "BTS"
    cache["pair"] = cache["asset"] + ":" + cache["currency"]
    return cache


def trace(error):
    """
    Stack trace upon exception
    """
    msg = str(type(error).__name__) + str(error.args)
    if DEV:
        msg += str(format_exc()) + " " + ctime()
    return msg


def initialize():
    """
    Clear text IPC channels
    Initialize storage and cache
    """
    storage = {}
    storage["data_latency"] = 0
    storage["access"] = 0
    storage["mean_ping"] = 0.5
    now = int(time())
    cache = {"begin": now}
    if DEV:
        enableTrace(True)
    race_write(doc="blacklist.txt", text=json_dump([]))
    race_write(doc="whitelist.txt", text=json_dump([]))
    race_write(doc="metaNODElog.txt", text=json_dump(""))
    race_write(doc="metaNODE.txt", text=json_dump({}))
    race_write(doc="mavens.txt", text=json_dump([]))
    race_write(doc="watchdog.txt", text=json_dump([now, now]))
    race_write(doc="nodes.txt", text=json_dump(public_nodes()))
    return storage, cache


def get_nodes():
    """
    Dynamic list if long enough else static list
    """
    nodes = race_read(doc="nodes.txt")
    if len(nodes) < MIN_NODES:
        nodes = public_nodes()
    return nodes


def logo(cache):
    """
    Print animated ascii artwork
    """

    def hexy():
        """
        Generate random hexadecimal string
        """
        alpha = "abcdef1234567890"
        beta = ""
        for _ in range(17):
            beta = str(beta + r"\x" + choice(alpha) + choice(alpha))
        return beta

    hex1, hex2, hex3, hex4 = hexy(), hexy(), hexy(), hexy()
    if "metanode_logo" not in cache.keys():
        cache["metanode_logo"] = ascii_logo("metanode")
    print(it("blue", hex1))
    print(it("blue", hex2))
    print(it("cyan", cache["metanode_logo"]))
    print(
        "                                                          "
        + cache["version_number"]
    )
    print(it("blue", hex3))
    print(it("blue", hex4))
    if DEV:
        msg = ""
        for _ in range(17):
            msg += "DEV "
        print(it("red", msg))
    return cache


def main():
    """
    Primary event backbone
    """
    storage, cache = initialize()
    cache = version(cache)
    cache = welcome(cache)
    cache = sign_in(cache)
    storage, cache = get_cache(storage, cache, get_nodes())
    spawn(storage, cache)


if __name__ == "__main__":
    main()
