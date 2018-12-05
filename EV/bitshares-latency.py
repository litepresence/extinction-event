# Python3
#
# Returns list of live tested nodes sorted by latency
# Prints list to file

# Includes Geolocation Data from ip-api.com

# Uploads list to jsonbin.io
'''maintained live at https://api.jsonbin.io/b/5c06e4f71deea01014bd4261/latest#Bitshares_Latency'''



# (BTS) litepresence1

'''
license: WTFPL
'''

from multiprocessing import Process, Value, Array
from bitshares.blockchain import Blockchain
from bitshares import BitShares
from datetime import datetime
import requests
import json
import time
import sys
import os

# terminal header
sys.stdout.write('\x1b]2;' + 'Bitshares Latency' + '\x07')

# bitshares main net id
ID = '4018d7844c78f6a6c41c6a552b898022310fc5dec06da467ee7905a8dad512c8'

BIN = 'get your bin id by creating a new bin with commented script above'
KEY = 'get your api keys after signup at jsonbin.io'

# set to true to share your latency test
JSONBIN = True
# set to true to add geolocation data 
IPAPI = True

def jsonbin(no_suffix, unique, speed, geo, urls):


    uri = 'https://api.jsonbin.io/b/'
    '''
    # run this commmented subscript to create a new jsonbin

    headers = {'Content-Type': 'application/json', 
        'secret-key':key,
        'private':'false'}

    data = {"UNIX": str(int(time.time()))}

    req = requests.post(uri, json=data, headers=headers)
    ret = req.text
    data = json.loads(ret)
    print (data)
    print(data['id'])
    '''
    url = uri + BIN

    headers = {'Content-Type': 'application/json', 
        'secret-key':KEY,
        'private':'false'}

    data = {
        "MISSION": "Bitshares Public Node Latency Testing",
        "LOCATION": "USA EAST",
        "UNIVERSE": str(no_suffix), 
        "OWNER": 'litepresence',
        "COUNT": ( str(len(unique)) + '/' + str(len(no_suffix)) ),
        "LIVE": str(unique), 
        "PING": str(speed),
        "UNIX": str(int(time.time())),
        "UTC":  str(time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())),
        "URLS": str(urls),
        "GEO": str(geo),
        "SOURCE_CODE": "https://github.com/litepresence/extinction-event/blob/master/EV/bitshares-latency.py"
        }

    data["DICT_KEYS"] = str(list(data.keys()))

    req = requests.put(url, json=data, headers=headers)

    print('updating jsonbin...')
    print(req.text)
    print('reading jsonbin...')
    url += '/latest'
    print(url)
    req = requests.get(url, headers=headers)
    print(req.text)

def nodes(timeout=20, pings=999999, crop=99, noprint=False, write=False,
          include=False, exclude=False, master=False):

    # timeout : seconds to ping until abort per node
    # pings   : number of good nodes to find until satisfied (0 none, 999 all)
    # noprint : disables printing, only returns list of good nodes
    # master  : check only nodes listed in bitshares/ui/master
    # crop    : return only best nodes
    # write   : maintains an output file nodes.txt with list of best nodes

    # include and exclude custom nodes
    included, excluded = [], []
    if include:
        included = ['api.bts.mobi', 'status200.bitshares.apasia.tech']

    if exclude:
        excluded = []

    # web scraping methods
    def clean(raw):
        return ((str(raw).replace('"', " "))
                .replace("'", " ")).replace(',', ' ')

    def parse(cleaned):
        return [t for t in cleaned.split() if t.startswith('wss')]


    def validate(parsed):
        v = parsed
        for i in range(len(v)):
            if v[i].endswith('/'):
                v[i] = v[i][:-1]
        for i in range(len(v)):
            if v[i].endswith('/ws'):
                v[i] = v[i][:-3]
        for i in range(len(v)):
            if v[i].endswith('/wss'):
                v[i] = v[i][:-4]
        return sorted(list(set(v)))

    def suffix(v):

        wss = [(i + '/wss') for i in v]
        ws = [(i + '/ws') for i in v]
        v = v + wss + ws
        return sorted(v)

    # ping the blockchain and return latency
            
    def ping(n, num, arr):

        try:
            start = time.time()
            chain = Blockchain(
                bitshares_instance=BitShares(n, num_retries=0), mode='head')

            # print(n,chain.rpc.chain_params["chain_id"])
            ping_latency = time.time() - start
            current_block = chain.get_current_block_num()
            blocktimestamp = abs(
                chain.block_timestamp(current_block))  # + utc_offset)
            block_latency = time.time() - blocktimestamp
            # print (blocktimestamp)
            # print (time.time())
            # print (block_latency)
            # print (ping_latency)
            # print (time.ctime())
            # print (utc_offset)
            # print (chain.get_network())
            if chain.get_network()['chain_id'] != ID:
                num.value = 333333
            elif block_latency < (ping_latency + 4):
                num.value = ping_latency
            else:
                num.value = 111111
        except:
            num.value = 222222
            pass

    # Disable / Enable printing
    def blockPrint():
        if noprint:
            sys.stdout = open(os.devnull, 'w')

    def enablePrint():
        if noprint:
            sys.stdout = sys.__stdout__

    # gather list of nodes from github
    blockPrint()
    begin = time.time()
    utc_offset = (datetime.fromtimestamp(begin) -
                  datetime.utcfromtimestamp(begin)).total_seconds()
    print ('=====================================')
    print(('found %s nodes stored in script' % len(included)))
    urls = []
    # scrape from github
    git = 'https://raw.githubusercontent.com'
    url = git + '/bitshares/bitshares-ui/master/app/api/apiConfig.js'
    urls.append(url)
    if not master:
        url = git + '/bitshares/bitshares-ui/staging/app/api/apiConfig.js'
        urls.append(url)
        url = git + '/CryptoBridge/cryptobridge-ui/'
        url += 'e5214ad63a41bd6de1333fd98d717b37e1a52f77/app/api/apiConfig.js'
        urls.append(url)
        url = git + '/litepresence/extinction-event/master/bitshares-nodes.py'
        urls.append(url)

    # include manually entered sites for Bitshares nodes
    validated = [] + included

    for u in urls:
        attempts = 3
        while attempts > 0:
            try:
                raw = requests.get(u).text
                v = validate(parse(clean(raw)))
                print(('found %s nodes at %s' % (len(v), u[:65])))
                validated += v
                attempts = 0
            except:
                print(('failed to connect to %s' % u))
                attempts -= 1
                pass

    # remove known bad nodes from test
    if len(excluded):
        excluded = sorted(excluded)
        print(('remove %s known bad nodes' % len(excluded)))
        validated = [i for i in validated if i not in excluded]

    #manual timeout and validated list for quick custom test
    if 0:
        timeout = 30
    if 0:
        validated = ['wss://b.mrx.im', 'wss://b.mrx.im/ws', 'wss://b.mrx.im/wss']
    if 0:
        validated = validated[-3:]

    # final sanitization
    validated = sorted(list(set(validate(parse(clean(validated))))))

    # test triplicate; add /ws and /wss suffixes to all validated websockets
    no_suffix = validated
    validated = suffix(validated)

    # attempt to contact each websocket
    print ('=====================================')
    print(('found %s total nodes' % len(no_suffix)))
    print ('=====================================')
    print (no_suffix)
    pinging = min(pings, len(validated))
    if pinging:
        print ('=====================================')
        enablePrint()
        print(('%s pinging %s nodes; timeout %s sec; est %.1f minutes' % (
            time.ctime(), pinging, timeout, timeout * len(validated) / 60.0)))
        blockPrint()
        print ('=====================================')
        pinged, timed, down, stale, expired, testnet = [], [], [], [], [], []
        i = 0
        for n in validated:
            if len(pinged) < pinging:
                i +=1
                # use multiprocessing module to enforce timeout
                num = Value('d', 999999)
                arr = Array('i', list(range(0)))
                p = Process(target=ping, args=(n, num, arr))
                p.start()
                p.join(timeout)
                if p.is_alive() or (num.value > timeout):
                    p.terminate()
                    p.join()
                    if num.value == 111111:  # head block is stale
                        stale.append(n)
                    elif num.value == 222222:  # connect failed
                        down.append(n)
                    elif num.value == 333333:  # connect failed
                        testnet.append(n)
                    elif num.value == 999999:  # timeout reached
                        expired.append(n)
                else:
                    pinged.append(n)        # connect success
                    timed.append(num.value)  # connect success time
                print(('ping:', ('%.2f' % num.value), n))

        # sort websockets by latency
        pinged = [x for _, x in sorted(zip(timed, pinged))]
        timed = sorted(timed)
        unknown = sorted(
            list(set(validated).difference(
                pinged + down + stale + expired + testnet)))

        unique = []
        speed = []
        geo = []
        for i in range(len(pinged)):
            geolocate = 'http://ip-api.com/json/'
            if pinged[i].strip('/ws') not in [j.strip('/ws') for j in unique]:
                unique.append(pinged[i])
                speed.append((pinged[i],int(timed[i]*1000)/1000.0))  
                time.sleep(1) 
                if IPAPI:
                    print('geolocating...')
                    ip = (validate([pinged[i]])[0])[6:]  
                    geolocate += ip
                    print(geolocate)               
                    req = requests.get(geolocate, headers={})
                    ret = json.loads(req.text)
                    entriesToRemove =    ('isp','regionName','org','countryCode','timezone','region','as','status','zip')
                    for k in entriesToRemove:
                        ret.pop(k, None)
                    ret['ip'] = ret.pop('query')
                    print (ret)
                    geo.append((pinged[i],ret))


        # report outcome
        print('')
        print((len(pinged), 'of', len(validated),
               'nodes are active with latency less than', timeout))
        print('')
        print(('fastest node', pinged[0], 'with latency', ('%.2f' % timed[0])))
        if len(excluded):
            for i in range(len(excluded)):
                print(((i+1), 'EXCLUDED', excluded[i]))
        if len(unknown):
            for i in range(len(unknown)):
                print(((i+1), 'UNTESTED', unknown[i]))
        if len(testnet):
            for i in range(len(testnet)):
                print(((i+1), 'TESTNET', testnet[i]))
        if len(expired):
            for i in range(len(expired)):
                print(((i+1), 'TIMEOUT', expired[i]))
        if len(stale):
            for i in range(len(stale)):
                print(((i+1), 'STALE', stale[i]))
        if len(down):
            for i in range(len(down)):
                print(((i+1),'DOWN', down[i]))
        if len(pinged):
            for i in range(len(pinged)):
                print(((i+1), 'GOOD PING', '%.2f' % timed[i], pinged[i]))
        if len(unique):
            for i in range(len(unique)):
                print(((i+1), 'UNIQUE:', unique[i]))
        print('UNIQUE LIST:')
        print(unique)
        ret = pinged[:crop]
    else:
        ret = validated[:crop]

    print ('')
    enablePrint()
    elapsed = time.time()-begin
    print ('elapsed:', ('%.1f' % elapsed), 
            'fastest:', ('%.3f' % timed[0]), ret[0])

    print (ret)

    if write and (len(ret) == crop):
        opened = 0
        while not opened:
            try:
                with open('nodes.txt', 'w+') as file:
                    file.write(str(ret))

                opened = 1
            except:
                pass

    if JSONBIN: jsonbin(no_suffix, unique, speed, geo, urls)

    return (ret)

def loop():

    while 1:
        try:
            nodes(timeout=10, pings=999, crop=999, noprint=False, write=True,
                include=True, exclude=False, master=False)
            time.sleep(900)

        # no matter what happens just keep verifying book
        except Exception as e:
            print (type(e).__name__, e.args, e)
            pass


def update():

    print('Acquiring low latency connection to Bitshares DEX'+
            ', this may take a few minutes...')
    updated = 0
    try:
        while not updated:
            nodes(timeout=6, pings=999, crop=999, noprint=False, write=True,
                include=False, exclude=False, master=False)
            updated = 1

    # not satisfied until verified once
    except Exception as e:
        print (type(e).__name__, e.args, e)
        pass


if __name__ == '__main__':


        loop()
