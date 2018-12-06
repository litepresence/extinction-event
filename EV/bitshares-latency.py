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
# set to true to plot
PLOT = True
# set true to upload final image to hosting service
UPLOAD = True

def jsonbin(no_suffix, unique, speed, geo, urls, image_url):


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
        "MAP_URL": str(image_url),
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
        excluded = [
            'wss://bit.btzadazdsabc.org',
            'wss://bitazdazdshares.openledger.info', 
            'wss://bitshaazdzares.openledger.info',
            'wss://bitshasdares.dacplay.org:8089',
            'wss://bitsqsdqsdhares.openledger.info',
            'wss://secuasdre.freedomledger.com',
            'wss://testnet.bitshares.eu/wqsdsqs', 
            ] # known typos found in webscraping methods, etc.


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
    # Bitshares Master
    url = git + '/bitshares/bitshares-ui/master/app/api/apiConfig.js'
    urls.append(url)
    
    if not master:
        
        gits = [
            '/bitshares/bitshares-ui/staging/app/api/apiConfig.js',
            '/CryptoBridge/cryptobridge-ui/e5214ad63a41bd6de1333fd98d717b37e1a52f77/app/api/apiConfig.js',
            '/litepresence/extinction-event/master/bitshares-nodes.py',
            '/blckchnd/rudex-ui/rudex/app/api/apiConfig.js',
            '/jhtitor/citadel/92c561a23aee20189c3827e231643f6d54ed55c1/bitsharesqt/bootstrap.py',
            '/BitSharesEurope/wallet.bitshares.eu/c618759e450ed645629421d6e6d063d0623652b1/app/api/apiConfig.js',
            '/dexgate/dexgate-ui/b16c117df1aa13348925ca99caf12f27947ccfbc/app/api/apiConfig.js',
            '/tpkeeper/btswallet_web/master/app/api/apiConfig.js',
            '/crexonline/crex/00fec97b4305d9105b19d723bccf93085bf55a12/app/api/apiConfig.js',
            '/InfraexDev/BTSExchange/a9de1845ceed16270e1d22752cf0a0e98841f4bd/app/api/apiConfig.js',
            '/myneworder/crex-ui/eb3f77ddb81b415c83c817c8aa980abf79ac8bb5/app/api/apiConfig.js',
            '/hamzoni/zcom-ui/aed6c10417e40f9b9467a891c48aba1d64a5dc18/app/api/apiConfig.js',
            '/mhowardweb/blockchain-connector/5c99251cfcb780a04f9bb06150d76a6423a7c871/vuex-bitshares/config.js',
            '/TKFORKED/hx-ui/6e5282ace6e4845a4cf3db99b9688ba6b2de6c80/app/api/apiConfig.js',
            '/MCLXI/cb/d3842a05f052276cc0d48e5d1ece4fd4b0977dcd/app/api/apiConfig.js',
            '/blag-potok/blgtk/c5192cedf09f9f298cf8d7d59de89cebc1f71f8c/index.html',
            '/Open-Asset/Bitshares_nodes/d375fa830699131a9e334cb689a5d70578f4db4f/Bitshares%20Public%20Nodes%20Open-Assets',
            '/zcom-project/zcomjs-ws/94dd0763c4ea0866dfffcaba568ac5f970c7d38a/test/Manager.js',
            '/AAAChain/w3ajs-ws/479b7c562fe216156edc2d38b3e22297428ea30b/test/Manager.js',
            '/LocalCoinIS/localcoinjs-ws/00870ec1471b69014b8076e84ba76ef8bd16f7b5/test/Manager.js',
            '/Cloud-eer/cloud-ws/17f95488b444bf5ff693cd16701bad9fd4902d8b/test/Manager.js',
            '/denkhaus/bitshares/f73c254c7b94b36174cd0597c68b1c6c5ecb982e/api/tester.go',
            '/BTS-CM/Bitshares-HUG-REST-API/a39b3d09e65a118ad551dc0834ef9199ec618a14/hug_script.py',
            '/dbxone/dbxui/4a39f849d203f28d8e27a78b5b70c4ae5b6e3f5a/app/api/apiConfig.js',
            '/oooautoclub/autounite-js/51c04acd6b795ad9801b2241a01ca890ec8a535e/app/api/apiConfig.js',
            '/alldex/alldex-ui/61323a668783aa3609eb1e77b92348f5cffcba01/app/api/apiConfig.js',
            '/jwaiswa7/bit_shares_exknox/046a514a31d10dba38c0ea37f3dbd14b64abecad/app/api/apiConfig.js',
            '/theserranos/bitsharesAPINode/3a9a49cc566246e95a71b49389fe1eebffcfce81/config.js',
            ]
        for g in gits:
            url = git + g
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

    ########################################################
    ########################################################
    #manual timeout and validated list for quick custom test
    if 0:
        timeout = 30
    if 0:
        validated = ['wss://b.mrx.im', 'wss://b.mrx.im/ws', 'wss://b.mrx.im/wss']
    if 0:
        validated = validated[-5:]
    ########################################################
    ########################################################

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
                    ip = (validate([pinged[i]])[0])[6:]  #strip wws://, /wss, /ws, and / 
                    ip = ip.split(":")[0]
                    # ip-api has trouble with these; parsed manually at ipinfo.info:
                    if (ip == 'freedom.bts123.cc'):
                        ip = '121.42.8.104'
                    if (ip == 'ws.gdex.top'):
                        ip = '106.15.82.97' 
                    if (ip == 'bitshares.dacplay.org'):
                        ip = '120.55.181.181'
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

    if PLOT:

        print('plotting...')
        import matplotlib.pyplot as plt
        import matplotlib.cbook as cbook
        import numpy as np
        imageFile = cbook.get_sample_data('/home/oracle/extinction-event/LIVE/map2.png')
        img = plt.imread(imageFile)
        fig, ax = plt.subplots(figsize=(9,18))
        plt.xticks(np.arange(-180,180,30))
        plt.yticks(np.arange(-90,90,30))
        ax.imshow(img, extent=[-180, 180, -90, 90])
        fig.tight_layout()

        plt.pause(0.1)

        xs = []
        ys = []
        for i in range(len(geo)):
            try:
                x = float(geo[i][1]['lon'])
                y = float(geo[i][1]['lat'])
                xs.append(x)
                ys.append(y)
                l = geo[i][0]
                try:
                    s = float(speed[i][1])
                    m = 10*5/s              
                except:
                    m = 10
                    pass
                print(x,y,l,s,m)
                plt.plot([x],[y],'ro', markersize=m,alpha=0.2)

            except:
                print('skipping', geo[i])
                pass
        plt.plot(xs,ys,'yo', markersize=4)




        plt.savefig('/home/oracle/extinction-event/LIVE/nodemap.png', dpi=100)

    if UPLOAD:

        image_url = ''
        try:
            url = 'https://vgy.me/upload'
            files = {'file': open('nodemap.png', 'rb')}
            r = requests.post(url, files=files)
            image_url = json.loads(r.text)['image']
        except:
            print('vgy failed')
            pass
        print (image_url)

    if JSONBIN: jsonbin(no_suffix, unique, speed, geo, urls, image_url)

    if PLOT:
        for i in range(9000):
            plt.pause(0.1)
    else: 
        time.sleep(900)

    

    return (ret)

def loop():

    while 1:
        try:
            nodes(timeout=6, pings=999, crop=999, noprint=False, write=True,
                include=True, exclude=True, master=False)
            

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
                include=False, exclude=False, master=True)
            updated = 1

    # not satisfied until verified once
    except Exception as e:
        print (type(e).__name__, e.args, e)
        pass


if __name__ == '__main__':


        loop()
