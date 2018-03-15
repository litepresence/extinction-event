# Python3
#
# Returns list of live tested nodes sorted by latency
#
# (BTS) litepresence1


def nodes(timeout=5, pings=999999, 
        noprint=False, include=False, exclude=False, suffix=False):

    # timeout is seconds to ping until abort per websocket
    # pings is number of websockets to ping  until skip (0 none, 999 all)

    from multiprocessing import Process, Value, Array
    from bitshares.blockchain import Blockchain
    from bitshares import BitShares
    from datetime import datetime
    import requests
    import time
    import sys
    import os

    # include and exclude custom nodes
    included, excluded = [], []
    if include:
        included = []

    if exclude:
        excluded = []

    # web scraping methods
    def clean(raw):
        return ((str(raw).replace('"', " "))
                .replace("'", " ")).replace(',', ' ')

    def parse(cleaned):
        return [t for t in cleaned.split() if t.startswith('wss')]

    def validate(parsed):
        v = [i for i in parsed if (('test' not in i) and ('fake' not in i))]
        for i in range(len(v)):
            if v[i].endswith('/'):
                v[i] = v[i][:-1]
        for i in range(len(v)):
            if v[i].endswith('/ws'):
                v[i] = v[i][:-3]
        for i in range(len(v)):
            if v[i].endswith('/wss'):
                v[i] = v[i][:-4]
        x_for = ['wss://relinked.com',
                 'wss://bitshares.crypto.fans',
                 'wss://this.uptick.rocks']
        if suffix:
            wss = [(i+'/wss') for i in v]
            ws = [(i+'/ws') for i in v]
            v = v+wss+ws
        else:
            for i in range(len(v)):
                if v[i] in x_for:
                    v[i] += '/ws'
                else:
                    v[i] += '/wss'
        return v

    # ping the blockchain and return latency
    def ping(n, num, arr):
        try:
            start = time.time()
            chain = Blockchain(
                bitshares_instance=BitShares(
                    n,
                    num_retries=0),
                mode='head')
            ping_latency = time.time() - start
            current_block = chain.get_current_block_num()
            blocktimestamp = abs(
                chain.block_timestamp(
                    current_block) +
                utc_offset)
            block_latency = time.time() - blocktimestamp
            if block_latency < (ping_latency + 4):
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

    blockPrint()
    begin = time.time()
    utc_offset = (datetime.fromtimestamp(begin) -
                  datetime.utcfromtimestamp(begin)).total_seconds()
    print ('=====================================')
    print(('found %s nodes stored in script' % len(included)))
    urls = []
    # scrape from github
    git = 'https://raw.githubusercontent.com'
    url = git + '/bitshares/bitshares-ui/staging/app/api/apiConfig.js'
    urls.append(url)
    url = git + '/bitshares/bitshares-ui/master/app/api/apiConfig.js'
    urls.append(url)
    url = git + '/CryptoBridge/cryptobridge-ui/'
    url += 'e5214ad63a41bd6de1333fd98d717b37e1a52f77/app/api/apiConfig.js'
    urls.append(url)
    url = git + '/litepresence/extinction-event/master/bitshares-nodes.py'
    urls.append(url)

    # searched selected sites for Bitshares nodes
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
                attempts += 1
                pass

    if len(excluded):
        excluded = sorted(excluded)
        print(('remove %s known bad nodes' % len(excluded)))
        validated = [i for i in validated if i not in excluded]

    validated = sorted(list(set(validate(parse(clean(validated))))))

    print ('=====================================')
    print(('found %s total nodes - no duplicates' % len(validated)))
    print ('=====================================')
    print (validated)
    pinging = min(pings, len(validated))

    if pinging:  # attempt to contact each websocket
        print ('=====================================')
        enablePrint()
        print(('%s searching for %s nodes; timeout %s sec; est %.1f minutes' % (
            time.ctime(), pinging, timeout, timeout * len(validated) / 60.0)))
        blockPrint()
        print ('=====================================')
        pinged, timed, down, stale, expired = [], [], [], [], []
        # use multiprocessing module to enforce timeout
        for n in validated:
            if len(pinged) < pinging:
                num = Value('d', 999999)
                arr = Array('i', list(range(0)))
                p = Process(target=ping, args=(n, num, arr))
                p.start()
                p.join(timeout)
                if p.is_alive() or (num.value > timeout):
                    p.terminate()
                    p.join()
                    if num.value == 111111: # head block is stale
                        stale.append(n)
                    if num.value == 222222: # websocket connect failed
                        down.append(n)
                    if num.value == 999999: # timeout reached
                        expired.append(n)
                else:
                    pinged.append(n)        # websocket connect success
                    timed.append(num.value) # websocket connect time
                print(('ping:', ('%.2f' % num.value), n))
        # sort websockets by latency
        pinged = [x for _, x in sorted(zip(timed, pinged))]
        timed = sorted(timed)
        unknown = sorted(
            list(set(validated).difference(pinged + down + stale + expired)))
        print('')
        print((len(pinged), 'of', len(validated),
               'nodes are active with latency less than', timeout))
        print(('fastest node', pinged[0], 'with latency', ('%.2f' % timed[0])))

        if len(excluded):
            print('')
            print ('EXCLUDED nodes:')
            print('')
            for i in range(len(excluded)):
                print(('XXXX', excluded[i]))
        if len(unknown):
            print('')
            print ('UNTESTED nodes:')
            print('')
            for i in range(len(unknown)):
                print(('????', unknown[i]))
        if len(down):
            print('')
            print ('DOWN nodes:')
            print('')
            for i in range(len(down)):
                print(('DOWN', down[i]))
        if len(stale):
            print('')
            print ('STALE nodes:')
            print('')
            for i in range(len(stale)):
                print(('SSSS', stale[i]))
        if len(expired):
            print('')
            print ('TIMEOUT nodes:')
            print('')
            for i in range(len(expired)):
                print(('TTTT', expired[i]))
        if len(pinged):
            print ('')
            print ('UP nodes:')
            print ('')
            for i in range(len(pinged)):
                print((('%.2f' % timed[i]), pinged[i]))

        ret = pinged
    else:
        ret = validated

    print ('')
    print (ret)
    print ('')
    enablePrint()
    print(('elapsed', ('%.2f' % (time.time() - begin))))
    return ret

nodes()
