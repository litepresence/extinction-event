# Python3
#
# Returns list of live tested nodes sorted by latency
#
# (BTS) litepresence1

def nodes(timeout=5, pings=999, noprint=True, custom=True):  # Public Nodes List

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

    include, exclude = [],[]
    if custom:
        include = ['wss://relinked.com/ws']
        exclude = ['wss://valen-tin.fr:8090/ws', 
            'wss://japan.bitshares.apasia.tech/ws',
            'wss://us-ny.bitshares.apasia.tech/ws',
            'wss://bitshares.apasia.tech/ws',
            'wss://altcap.io/ws',
            'wss://btsza.co.za:8091/ws',
            'wss://dex.rnglab.org', 
            ]

    # web scraping methods
    def clean(raw):
        return ((raw.replace('"'," ")).replace("'"," ")).replace(',',' ')
    def parse(cleaned):
        return [ t for t in cleaned.split() if t.startswith('wss') ]
    def validate(parsed):
        return [i for i in parsed if (('test' not in i) and ('fake' not in i))]
    #ping the blockchain and return latency
    def ping(n,num,arr):
        start = time.time()
        try:
            chain = Blockchain(bitshares_instance=BitShares(n))
            t = time.time() - abs(datetime.strptime( (chain.info())['time'], 
                "%Y-%m-%dT%H:%M:%S").timestamp()+utc_offset)
            if t < 4:
                num.value = time.time() - start
            else:
                num.value = 111111 #head block is stale
        except:
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
    print(('found %s nodes stored in script' % len(include))) 
    urls = []
    # scrape from github
    git = 'https://raw.githubusercontent.com'
    url = git+'/bitshares/bitshares-ui/staging/app/api/apiConfig.js'
    urls.append(url)
    url = git+'/bitshares/bitshares-ui/master/app/api/apiConfig.js'
    urls.append(url)
    url = git+'/CryptoBridge/cryptobridge-ui/'
    url += 'e5214ad63a41bd6de1333fd98d717b37e1a52f77/app/api/apiConfig.js'
    urls.append(url)
    # use pastebin as failsafe backup
    url = 'https://pastebin.com'
    url += '/raw/YCsHRwgS'
    urls.append(url)

    # searched selected sites for Bitshares nodes
    validated = []+include
    for u in urls:
        try:
            raw = requests.get(u).text
            v = validate(parse(clean(raw)))
            print(('found %s nodes at %s' % (len(v),u[:65])))
            validated += v
        except:
            print(('failed to connect to %s' % u)) 
            pass
    if len(exclude):
        exclude = sorted(exclude)
        print ('remove %s bad nodes' % len(exclude))
        validated = [i for i in validated if i not in exclude]
    validated = sorted(list(set(validated)))


    print ('=====================================')
    print(('found %s total nodes - no duplicates' % len(validated)))
    print ('=====================================')
    print (validated)
    pinging = min(pings, len(validated))
    
    if pinging: # attempt to contact each websocket
        print ('=====================================')
        enablePrint()
        print ('%s searching %s nodes; timeout %s sec; est %.1f minutes' % (
            time.ctime(),pinging,timeout,timeout*len(validated)/60.0))
        blockPrint()
        print ('=====================================')
        pinged, timed, down, stale = [], [], [], []
        # use multiprocessing module to enforce timeout
        for n in validated:
            if len(pinged) < pinging:
                num = Value('d', 999999)
                arr = Array('i', list(range(0)))
                p = Process(target=ping, args=(n, num, arr))
                p.start()
                p.join(timeout)
                if p.is_alive() or (num.value>timeout):
                    p.terminate()
                    p.join()
                    if num.value == 111111:
                        stale.append(n)
                    else:
                        down.append(n)
                else:
                    pinged.append(n)
                    timed.append(num.value)
                print(('ping:', ('%.2f'% num.value), n))
        # sort websockets by latency 
        pinged = [x for _,x in sorted(zip(timed,pinged))]
        timed = sorted(timed)
        unknown = sorted(list(set(validated).difference(pinged+down+stale)))
        print('')
        print((len(pinged) ,'of', len(validated), 
            'nodes are active with latency less than', timeout))
        print(('fastest node', pinged[0], 'with latency', ('%.2f'%timed[0])))

        if len(exclude):
            print('')
            print ('EXCLUDED nodes:')
            print('')
            for i in range(len(exclude)):
                print(('XXXX', exclude[i]))
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
        if len(pinged):
            print ('')
            print ('UP nodes:')
            print ('')
            for i in range(len(pinged)):
                print((('%.2f'%timed[i]), pinged[i]))

        ret = pinged
    else:
        ret = validated
   
    print ('')
    print (ret)
    print ('')
    enablePrint()
    print(('elapsed', ('%.2f' %(time.time()-begin))))
    return ret
    
nodes(timeout=5, pings=999, noprint=False, custom=False)
