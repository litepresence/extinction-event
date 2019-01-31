
#=======================================================================
VERSION = 'Bitshares latencyTEST 0.00000010'
#=======================================================================

# Bitshares Public Node Location Utility

' litepresence 2019 '

def WTFPL_v0_March_1765():
    if any([stamps, licenses, taxation, regulation, fiat, etat]):
        try:
            print('no thank you')
        except:
            return [tar, feathers]

' ********** ALPHA RELEASE TO PUBLIC DOMAIN WITH NO WARRANTY ********* '

' features '
# no pybitshares dependencies
# Writes unique domains to file nodes.txt; which is used by metaNODE.py
# Uploads list and other latency data to jsonbin.io
# Includes Geolocation Data from ip-api.com
# Creates map from geolocation data and uploads to vgy.me
# New control panel
# Map base image auto downloads from imgur

' maintained live at '
# api.jsonbin.io/b/5c06e4f71deea01014bd4261/latest#Bitshares_Latency

# standard modules
from multiprocessing import Process, Value, Array
from json import loads as json_loads
from json import dumps as json_dumps
from datetime import datetime
from calendar import timegm
from time import strptime
import traceback
import time
import sys
import os

# you may need to install
print('pip3 install websocket-client')
print('pip3 install matplotlib')
print('pip3 install requests')
print('pip3 install numpy')
from websocket import create_connection as wss  # handshake to node
import matplotlib.cbook as cbook
import matplotlib.pyplot as plt
import numpy as np
import requests
print("\033c")  # clear screen if they are all installed

#
''' USER CONTROL PANEL '''
#
# bitshares main net id
ID = '4018d7844c78f6a6c41c6a552b898022310fc5dec06da467ee7905a8dad512c8'
BLIP = 0.05  # pause between race read conditions
JSONBIN = True  # set to true to share your latency test
IPAPI = True  # set to true to add geolocation data
PLOT = True  # set to true to plot
UPLOAD = True  # set true to upload final image to hosting service
SEEDS = False  # test seed nodes?
TIMEOUT = 3  # Websocket Timeout
PINGS = 9999  # Crop validated list prior to use
CROP = 9999  # Crop final unique list
NOPRINT = False  # Reduced terminal printing
WRITE = True  # Write nodes.txt with unique list
INCLUDE = True  # Include this private node list in global_lists()
EXCLUDE = True  # Exclude these known bad nodes in global_lists()
MASTER = False  # Check only Bitshares UI Master List
ONLY = False  # Test just nodes in only list
LOOP = True  # Repeat latency test indefinitely
UNIVERSE = True  # Check all in known universe in global_lists()
TESTNET = False  # False to skip testnet nodes
TRACE_DETAIL = False  # websocket.enableTrace
BIN = 'see jsonbin() definition to for sample bin creation script'
KEY = 'get your api keys after signup at jsonbin.io'



if TRACE_DETAIL:
    websocket.enableTrace(True)

def race_write(doc='', text=''):  # Concurrent Write to File Operation

    text = str(text)
    i = 0
    while True:
        time.sleep(BLIP * i ** 2)
        i += 1
        try:
            with open(doc, 'w+') as f:
                f.write(text)
                f.close()
                break
        except Exception as e:
            msg = str(type(e).__name__) + str(e.args)
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

def test_seeds():  # ping and geolocate seed nodes

    if SEEDS:
        # scrape list of seed nodes from github:
        url = ('https://raw.githubusercontent.com/bitshares/' +
               'bitshares-core/master/libraries/app/application.cpp')

        # my ISP is currently blocking github
        uri = 'https://www.textise.net/showText.aspx?strURL=https%253A//'
        url = uri + ('raw.githubusercontent.com/bitshares/bitshares-core/' +
                     'master/libraries/app/application.cpp')
        # so I hack quick hole in their bullshit...

        req = requests.get(url).text
        ret = req.replace(
            " ",
            "").replace(",",
                        "").split('seeds={')[1].split('}')[0]
        del req
        ret = ret.split('//')
        ret = [i for i in ret if '"' in i]
        ret = [i.split('"')[1] for i in ret]
        ret = [i.split(':')[0] for i in ret]

        seeds = []
        print('pinging and geolocating seed nodes...')
        print('')
        for i in ret:

            cmd = 'ping -c 1 ' + i
            a = os.popen(cmd).read()
            try:
                ping = int(a.split('time=')[1].split(' ms')[0])
            except:
                ping = 0
            geolocate = 'http://ip-api.com/json/'
            ip = i

            # some ips are not recognized by ip-api.com; substitute ipinfo.info
            # manually:
            if ip == 'seeds.bitshares.eu':
                ip = '45.76.70.247'
            geolocate += ip

            req = requests.get(geolocate, headers={})
            ret = json_loads(req.text)
            del req
            entriesToRemove = (
                'isp',
                'regionName',
                'org',
                'countryCode',
                'timezone',
                'region',
                'as',
                'status',
                'zip')
            for k in entriesToRemove:
                ret.pop(k, None)
            ret['ip'] = ret.pop('query')
            ret = (i, ping, ret)
            print(ret)
            seeds.append(ret)
        del ret

        print('')
        from pympler import asizeof
        sizes = []
        local = dict(locals())
        for name, obj in local.items():
            if name != 'asizeof':
                sizes.append((('%.2f' % (asizeof.asizeof(obj) / 1024)), name))
        print('')
        print(sizes)
        for s in sizes:
            print(s)
        race_write(doc='sizes.txt', text=str(sizes))

        return seeds
    else:
        return []

def jsonbin(no_suffix, unique, speed, geo, urls, image_url, seeds):

    # upload data from latency test to jsonbin.io
    # you will need to need to create an api key to use this feature

    url = 'https://api.jsonbin.io/b/'
    '''
    # run this commmented subscript to create a new jsonbin

    headers = {'Content-Type': 'application/json',
        'secret-key':key,
        'private':'false'}

    data = {"UNIX": str(int(time.time()))}

    req = requests.post(uri, json=data, headers=headers)
    ret = req.text
    data = json_loads(ret)
    print (data)
    print(data['id'])
    '''
    url = url + BIN

    headers = {'Content-Type': 'application/json',
               'secret-key': KEY,
               'private': 'false'}

    data = {
        "MISSION": "Bitshares Public Node Latency Testing",
        "LOCATION": "USA EAST",
        "UNIVERSE": str(no_suffix),
        "OWNER": 'litepresence',
        "COUNT": (str(len(unique)) + '/' + str(len(no_suffix))),
        "LIVE": str(unique),
        "PING": str(speed),
        "UNIX": str(int(time.time())),
        "UTC": str(time.strftime("%a, %d %b %Y %H:%M:%S",
                                 time.gmtime())),
        "URLS": str(urls),
        "GEO": str(geo),
        "SEEDS": str(seeds),
        "MAP_URL": str(image_url),
        "SOURCE_CODE": (
            "https://github.com/litepresence/extinction-event/blob/" +
            "MASTER/EV/bitshares-latency.py")
    }

    del geo
    del image_url
    del seeds
    del speed
    del no_suffix
    del unique
    del urls
    data["DICT_KEYS"] = str(list(data.keys()))
    req = requests.put(url, json=data, headers=headers)
    del data
    print('reading jsonbin...')
    url += '/latest'
    print(url)
    req = requests.get(url, headers=headers)
    del url
    del headers
    print(req.text)
    del req

def clean(raw):  # remove parenthesis and commas from strings
    return ((str(raw).replace('"', " "))
            .replace("'", " ")).replace(',', ' ')

def parse(cleaned):  # return list of words beginning with wss
    return [t for t in cleaned.split() if t.startswith('wss')]

def validate(parsed):  # remove suffixes for each domain
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

def suffix(v):  # add suffixes for each domain

    wss = [(i + '/wss') for i in v]
    ws = [(i + '/ws') for i in v]
    v = v + wss + ws
    return sorted(v)

def trace_detail(node):

    print('====================')
    print(node)
    print('====================')
    try:
        handshake_latency, ws = dex_handshake(node)
        print('handshake', ('%.3f' % handshake_latency))
        print('')
        print('ws', ws)
        print('')
    except:
        print('websocket handshake failed')
        pass
    try:
        ping_latency = dex_ping_latency(ws)
        print('chain id ping', ('%.3f' % ping_latency))
        print('')
    except:
        print('websocket chain id request failed')
        pass
    try:
        close = ws.close()
        print('closing...', close)
    except:
        print('ws.close() failed')
    print('====================')

def from_iso_date(iso):
    # returns unix epoch given iso8601 datetime
    ISO8601 = '%Y-%m-%dT%H:%M:%S%Z'
    unix = int(timegm(strptime((iso + "UTC"), ISO8601)))
    return unix

def wss_handshake(node):

    global ws
    ws = wss(node, timeout=TIMEOUT)

def wss_query(params):

    query = json_dumps({"method": "call",
                        "params": params,
                        "jsonrpc": "2.0",
                        "id": 1})
    ws.send(query)
    ret = json_loads(ws.recv())
    try:
        ret = ret['result']  # if there is result key take it
    except:
        pass
    return ret

def rpc_get_dynamic_global_properties():
    ret = wss_query(["database",
                     "get_dynamic_global_properties",
                     []])
    return ret['head_block_number']

def rpc_get_chain_properties():
    ret = wss_query(["database",
                     "get_chain_properties",
                     []])
    return ret['chain_id']

def rpc_get_block(block):
    ret = wss_query(["database",
                     "get_block",
                     [block]])
    return from_iso_date(ret['timestamp'])

def ping(n, num, arr):  # ping the blockchain and return latency

    try:
        if TRACE_DETAIL:
            trace_detail(n)

        start = time.time()
        wss_handshake(n)
        ping_latency = time.time() - start

        block = rpc_get_dynamic_global_properties()
        chain = rpc_get_chain_properties()
        blocktimestamp = rpc_get_block(block)
        block_latency = time.time() - blocktimestamp
 
        if chain != ID:
            num.value = 333333
        elif block_latency < (ping_latency + 4):
            num.value = ping_latency
        else:
            num.value = 111111
        
    except Exception as e:
        print(str(type(e).__name__) + ' '  + str(e.args))
        num.value = 222222
        
def blockPrint():  # temporarily disable printing
    if NOPRINT:
        sys.stdout = open(os.devnull, 'w')

def enablePrint():  # re-enable printing
    if NOPRINT:
        sys.stdout = sys.__stdout__

def global_lists():

    '''
    # pretty print a list in order
    j = validate(j)
    for i in j:
        print("'" + i +"',")
    '''

    global included, excluded, only, gits, universe

    only = ['wss://status200.bitshares.apasia.tech/ws']

    included = [  # seen since core 181127
        'wss://altcap.io',
        'wss://api-ru.bts.blckchnd.com',
        'wss://api.bitshares.bhuz.info',
        'wss://api.bitsharesdex.com',
        'wss://api.bts.ai',
        'wss://api.bts.blckchnd.com',
        'wss://api.bts.mobi',
        'wss://api.bts.network',
        'wss://api.btsgo.net',
        'wss://api.btsxchng.com',
        'wss://api.dex.trading',
        'wss://api.fr.bitsharesdex.com',
        'wss://api.open-asset.tech',
        'wss://atlanta.bitshares.apasia.tech',
        'wss://australia.bitshares.apasia.tech',
        'wss://b.mrx.im',
        'wss://bit.btsabc.org',
        'wss://bitshares.crypto.fans',
        'wss://bitshares.cyberit.io',
        'wss://bitshares.dacplay.org',
        'wss://bitshares.dacplay.org:8089',
        'wss://bitshares.openledger.info',
        'wss://blockzms.xyz',
        'wss://bts-api.lafona.net',
        'wss://bts-seoul.clockwork.gr',
        'wss://bts.liuye.tech:4443',
        'wss://bts.open.icowallet.net',
        'wss://bts.proxyhosts.info',
        'wss://btsfullnode.bangzi.info',
        'wss://btsws.roelandp.nl',
        'wss://chicago.bitshares.apasia.tech',
        'wss://citadel.li/node',
        'wss://crazybit.online',
        'wss://dallas.bitshares.apasia.tech',
        'wss://dex.iobanker.com:9090',
        'wss://dex.rnglab.org',
        'wss://dexnode.net',
        'wss://england.bitshares.apasia.tech',
        'wss://eu-central-1.bts.crypto-bridge.org',
        'wss://eu.nodes.bitshares.ws',
        'wss://eu.openledger.info',
        'wss://france.bitshares.apasia.tech',
        'wss://frankfurt8.daostreet.com',
        'wss://japan.bitshares.apasia.tech',
        'wss://kc-us-dex.xeldal.com',
        'wss://kimziv.com',
        'wss://la.dexnode.net',
        'wss://miami.bitshares.apasia.tech',
        'wss://na.openledger.info',
        'wss://ncali5.daostreet.com',
        'wss://netherlands.bitshares.apasia.tech',
        'wss://new-york.bitshares.apasia.tech',
        'wss://node.bitshares.eu',
        'wss://node.market.rudex.org',
        'wss://nohistory.proxyhosts.info',
        'wss://openledger.hk',
        'wss://paris7.daostreet.com',
        'wss://relinked.com',
        'wss://scali10.daostreet.com',
        'wss://seattle.bitshares.apasia.tech',
        'wss://sg.nodes.bitshares.ws',
        'wss://singapore.bitshares.apasia.tech',
        'wss://status200.bitshares.apasia.tech',
        'wss://us-east-1.bts.crypto-bridge.org',
        'wss://us-la.bitshares.apasia.tech',
        'wss://us-ny.bitshares.apasia.tech',
        'wss://us.nodes.bitshares.ws',
        'wss://valley.bitshares.apasia.tech',
        'wss://ws.gdex.io',
        'wss://ws.gdex.top',
        'wss://ws.hellobts.com',
        'wss://ws.winex.pro',
    ]

    excluded = [  # known typos found in webscraping methods, etc.
        'wss://bit.btzadazdsabc.org',
        'wss://bitazdazdshares.openledger.info',
        'wss://bitshaazdzares.openledger.info',
        'wss://bitshasdares.dacplay.org:8089',
        'wss://bitsqsdqsdhares.openledger.info',
        'wss://secuasdre.freedomledger.com',
        'wss://testnet.bitshares.eu/wqsdsqs',
        'wss://fake.automatic-selection.com',
    ]

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
    ]  # github locations known to list Bitshares public API's

    universe = ['wss://altcap.io',
                'wss://ap-northeast-1.bts.crypto-bridge.org',
                'wss://ap-northeast-2.bts.crypto-bridge.org',
                'wss://ap-south-1.bts.crypto-bridge.org',
                'wss://ap-southeast-1.bts.crypto-bridge.org',
                'wss://ap-southeast-2.bts.crypto-bridge.org',
                'wss://api-ru.bts.blckchnd.com',
                'wss://api.bitshares.bhuz.info',
                'wss://api.bitsharesdex.com',
                'wss://api.bts.ai',
                'wss://api.bts.blckchnd.com',
                'wss://api.bts.mobi',
                'wss://api.bts.network',
                'wss://api.btsgo.net',
                'wss://api.btsxchng.com',
                'wss://api.dex.trading',
                'wss://api.fr.bitsharesdex.com',
                'wss://api.open-asset.tech',
                'wss://atlanta.bitshares.apasia.tech',
                'wss://australia.bitshares.apasia.tech',
                'wss://b.mrx.im',
                'wss://bit.btsabc.org',
                'wss://bitshares-api.wancloud.io',
                'wss://bitshares.apasia.tech',
                'wss://bitshares.bts123.cc:15138',
                'wss://bitshares.crypto.fans',
                'wss://bitshares.cyberit.io',
                'wss://bitshares.dacplay.org',
                'wss://bitshares.dacplay.org:8089',
                'wss://bitshares.neocrypto.io',
                'wss://bitshares.nu',
                'wss://bitshares.openledger.info',
                'wss://bitshares.testnet.crypto-bridge.org',
                'wss://blockzms.xyz',
                'wss://bts-api.lafona.net',
                'wss://bts-seoul.clockwork.gr', 'wss://bts.ai.la',
                'wss://bts.liuye.tech:4443', 'wss://bts.open.icowallet.net',
                'wss://bts.proxyhosts.info', 'wss://bts.to0l.cn:4443',
                'wss://bts.transwiser.com', 'wss://btsfullnode.bangzi.info',
                'wss://btsws.roelandp.nl', 'wss://btsza.co.za:8091',
                'wss://ca-central-1.bts.crypto-bridge.org',
                'wss://canada6.daostreet.com', 'wss://capetown.bitshares.africa',
                'wss://chicago.bitshares.apasia.tech', 'wss://citadel.li/node',
                'wss://crazybit.online', 'wss://croatia.bitshares.apasia.tech',
                'wss://dallas.bitshares.apasia.tech', 'wss://de.bts.dcn.cx',
                'wss://dele-puppy.com', 'wss://dex.iobanker.com:9090',
                'wss://dex.rnglab.org', 'wss://dexnode.net',
                'wss://england.bitshares.apasia.tech',
                'wss://eu-central-1.bts.crypto-bridge.org',
                'wss://eu-west-1.bts.crypto-bridge.org',
                'wss://eu-west-2.bts.crypto-bridge.org',
                'wss://eu-west-3.bts.crypto-bridge.org',
                'wss://eu.nodes.bitshares.works', 'wss://eu.nodes.bitshares.ws',
                'wss://eu.openledger.info', 'wss://fi.bts.dcn.cx',
                'wss://france.bitshares.apasia.tech', 'wss://frankfurt8.daostreet.com',
                'wss://freedom.bts123.cc:15138', 'wss://japan.bitshares.apasia.tech',
                'wss://kc-us-dex.xeldal.com', 'wss://kimziv.com',
                'wss://la.dexnode.net', 'wss://miami.bitshares.apasia.tech',
                'wss://na.openledger.info', 'wss://ncali5.daostreet.com',
                'wss://netherlands.bitshares.apasia.tech',
                'wss://new-york.bitshares.apasia.tech',
                'wss://node.bitshares.eu', 'wss://node.btscharts.com',
                'wss://node.market.rudex.org', 'wss://node.testnet.bitshares.eu',
                'wss://nohistory.proxyhosts.info', 'wss://ohio4.daostreet.com',
                'wss://openledger.hk', 'wss://oregon2.daostreet.com',
                'wss://paris7.daostreet.com', 'wss://relinked.com',
                'wss://sa-east-1.bts.crypto-bridge.org',
                'wss://scali10.daostreet.com', 'wss://seattle.bitshares.apasia.tech',
                'wss://secure.freedomledger.com', 'wss://seoul9.daostreet.com',
                'wss://sg.nodes.bitshares.works', 'wss://sg.nodes.bitshares.ws',
                'wss://singapore.bitshares.apasia.tech',
                'wss://slovenia.bitshares.apasia.tech',
                'wss://status200.bitshares.apasia.tech',
                'wss://testnet-eu.bitshares.apasia.tech',
                'wss://testnet.bitshares.apasia.tech',
                'wss://testnet.bitshares.eu', 'wss://testnet.bts.dcn.cx',
                'wss://testnet.dex.trading', 'wss://testnet.nodes.bitshares.ws',
                'wss://this.uptick.rocks', 'wss://us-east-1.bts.crypto-bridge.org',
                'wss://us-la.bitshares.apasia.tech',
                'wss://us-ny.bitshares.apasia.tech',
                'wss://us-west-1.bts.crypto-bridge.org',
                'wss://us.nodes.bitshares.works', 'wss://us.nodes.bitshares.ws',
                'wss://valen-tin.fr:8090', 'wss://valley.bitshares.apasia.tech',
                'wss://virginia3.daostreet.com', 'wss://ws.aunite.com',
                'wss://ws.gdex.io', 'wss://ws.gdex.top', 'wss://ws.hellobts.com',
                'wss://ws.winex.pro', 'wss://wss.ioex.top',
                'wss://za.bitshares.africa'
                ]  # All historical node locations

def thresh():

    global previous_unique, only, included, excluded, gits
    try:
        print('')
        print('previous unique list')
        print(previous_unique)
        print('')
    except:
        pass

    global_lists()
    seeds = test_seeds()

    # INCLUDE and EXCLUDE custom nodes
    if not INCLUDE:
        included = []

    if not EXCLUDE:
        excluded = []

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

    # my ISP is currently blocking github so...
    git = 'https://www.textise.net/showText.aspx?strURL=https%253A//raw.githubusercontent.com'

    # Bitshares Master
    url = git + '/bitshares/bitshares-ui/master/app/api/apiConfig.js'
    urls.append(url)

    if MASTER:
        gits = []
    else:
        for g in gits:
            url = git + g
            urls.append(url)
    del gits

    # INCLUDE manually entered sites for Bitshares nodes
    validated = [] + included


    if UNIVERSE:
        validated = universe
        print('Testing the known universe...')
    else:
        if not ONLY:
            if MASTER:
                print('searching github Bitshares UI master for nodes...')
            else:
                print('scraping github for Bitshares nodes...')

            for u in urls:
                attempts = 3
                while attempts > 0:
                    try:
                        raw = requests.get(u).text
                        v = validate(parse(clean(raw)))
                        del raw
                        u = u.replace(git, '')
                        u = "/".join(u.split("/", 3)[:3])
                        print(('found %s nodes at %s' % (len(v), u)))
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

    if ONLY and len(only):
        validated = only


    if not TESTNET:
        print('skipping known testnet nodes')
        validated = [i for i in validated if 'test' not in i]

    # final sanitization
    validated = sorted(list(set(validate(parse(clean(validated))))))

    # test triplicate; add /ws and /wss suffixes to all validated websockets
    no_suffix = validated
    validated = suffix(validated)

    validated = validated[:PINGS]
    # attempt to contact each websocket
    print ('=====================================')
    print(('found %s total nodes' % len(no_suffix)))
    print ('=====================================')
    print (no_suffix)
    pinging = min(PINGS, len(validated))
    if pinging:
        print ('=====================================')
        enablePrint()
        print(('%s pinging %s nodes; TIMEOUT %s sec; est %.1f minutes' % (
            time.ctime(), pinging, TIMEOUT, TIMEOUT * len(validated) / 120.0)))
        blockPrint()
        print ('=====================================')
        pinged, timed, down = [], [], []
        stale, expired, testnet = [], [], []
        i = 0
        for n in validated:
            if len(pinged) < pinging:
                i += 1
                # use multiprocessing module to enforce TIMEOUT
                num = Value('d', 999999)
                arr = Array('i', list(range(0)))
                p = Process(target=ping, args=(n, num, arr))
                p.start()
                p.join(TIMEOUT)
                if p.is_alive() or (num.value > TIMEOUT):
                    p.terminate()
                    p.join()
                    if num.value == 111111:  # head block is stale
                        stale.append(n)
                    elif num.value == 222222:  # connect failed
                        down.append(n)
                    elif num.value == 333333:  # connect failed
                        testnet.append(n)
                    elif num.value == 999999:  # TIMEOUT reached
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
                speed.append((pinged[i], int(timed[i] * 1000) / 1000.0))
                time.sleep(1)
                if IPAPI:
                    print('geolocating...')
                    ip = (validate([pinged[i]])[0])[
                        6:]  # strip wws://, /wss, /ws, and /
                    ip = ip.split(":")[0]
                    ip = ip.split("/")[0]
                    # ip-api.com has trouble with these
                    # parsed manually at ipinfo.info instead
                    if (ip == 'freedom.bts123.cc'):
                        ip = '121.42.8.104'
                    if (ip == 'ws.gdex.top'):
                        ip = '106.15.82.97'
                    if (ip == 'bitshares.dacplay.org'):
                        ip = '120.55.181.181'
                    if (ip == 'crazybit.online'):
                        ip = '39.108.95.236'
                    if (ip == 'citadel.li'):
                        ip = '37.228.129.75'
                    if (ip == 'bts.liuye.tech'):
                        ip =  '27.195.68.51'

                    geolocate += ip
                    print(geolocate)
                    req = requests.get(geolocate, headers={})
                    ret = json_loads(req.text)
                    entriesToRemove = (
                        'isp',
                        'regionName',
                        'org',
                        'countryCode',
                        'timezone',
                        'region',
                        'as',
                        'status',
                        'zip')
                    for k in entriesToRemove:
                        ret.pop(k, None)
                    ret['ip'] = ret.pop('query')
                    print (ret)
                    geo.append((pinged[i], ret))


        speeds = []
        for i in range(len(speed)):
            speeds.append(speed[i][1])
        mean_speed = sum(speeds)/len(speeds)

        # report outcome
        print('')
        print((len(pinged), 'of', len(validated),
               'nodes are active with latency less than', TIMEOUT))
        print('')
        print(('fastest node', pinged[0],
               'with latency', ('%.2f' % timed[0])))
        print('mean latency', mean_speed)
        if len(excluded):
            for i in range(len(excluded)):
                print(((i + 1), 'EXCLUDED', excluded[i]))
        if len(unknown):
            for i in range(len(unknown)):
                print(((i + 1), 'UNTESTED', unknown[i]))
        if len(testnet):
            for i in range(len(testnet)):
                print(((i + 1), 'TESTNET', testnet[i]))
        if len(expired):
            for i in range(len(expired)):
                print(((i + 1), 'TIMEOUT', expired[i]))
        if len(stale):
            for i in range(len(stale)):
                print(((i + 1), 'STALE', stale[i]))
        if len(down):
            for i in range(len(down)):
                print(((i + 1), 'DOWN', down[i]))
        if len(pinged):
            for i in range(len(pinged)):
                print(((i + 1), 'GOOD PING', '%.2f' %
                       timed[i], pinged[i]))
        if len(unique):
            for i in range(len(unique)):
                print(((i + 1), 'UNIQUE:', unique[i]))
        print('UNIQUE LIST:')
        print(unique)

    del excluded
    del unknown
    del testnet
    del expired
    del stale
    del down
    del pinged

    print ('')
    enablePrint()
    elapsed = time.time() - begin
    print ('elapsed:', ('%.1f' % elapsed),
           'fastest:', ('%.3f' % timed[0]), unique[0])

    if WRITE:
        race_write(doc='nodes.txt', text=str(unique))

    del timed

    if PLOT:
        try:
            plt.close()
        except:
            pass
        print('plotting...')
      
        def download_img(imageUrl, localFileName):
            while 1:
                r = requests.get(imageUrl, stream=True)
                if r.status_code == 200:
                    with open(localFileName, 'wb') as f:
                        for chunk in r.iter_content(1024):
                            f.write(chunk)
                    break
        path = os.path.dirname(os.path.abspath(__file__))
        im = '/basemap.png'
        path = path+im
        print(path)
        try:
            basemap = cbook.get_sample_data(path)
        except:
            url = 'https://i.imgur.com/yIVogZH.png'
            download_img(url,'basemap.png')
            basemap = cbook.get_sample_data(path)

        img = plt.imread(basemap)

        fig, ax = plt.subplots(figsize=(12, 24))
        plt.xticks([])
        plt.yticks([])
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
                    s = float(speed[i][1])/mean_speed
                    m = 20 / s
                except:
                    m = 10
                    pass
                print(x, y, l, s, m)
                plt.plot([x], [y], 'mo', markersize=m, alpha=0.25)

            except:
                print('skipping', geo[i])
                pass
        plt.plot(xs, ys, 'wo', markersize=4, alpha=0.25)
        del x
        del y
        del xs
        del ys

    # PLOT SEED NODES
    if SEEDS:
        xs = []
        ys = []
        for i in range(len(seeds)):
            if float(seeds[i][1]) > 0:
                try:
                    x = float(seeds[i][2]['lon'])
                    y = float(seeds[i][2]['lat'])
                    xs.append(x)
                    ys.append(y)
                except:
                    print('skipping', seeds[i])
                    pass
        plt.plot(xs, ys, 'yo', markersize=4, alpha=1.0)
        utc = str(
            time.strftime("%a, %d %b %Y %H:%M:%S",
                          time.gmtime())) + ' UTC'

        plt.text(0, -60, utc, alpha=0.5, color='w', size=15)

        location = '/home/oracle/extinction-event/EV/nodemap.png'

        plt.savefig(location,
                    dpi=100,
                    bbox_inches='tight',
                    pad_inches=0)

        # SAVE HISTORY
        if 1:
            location = '/home/oracle/extinction-event/EV/HISTORY/nodemap_' + \
                str(int(time.time())) + '.png'

            plt.savefig(location,
                        dpi=100,
                        bbox_inches='tight',
                        pad_inches=0)

    if UPLOAD:

        image_url = ''
        try:
            url = 'https://vgy.me/upload'
            files = {'file': open('nodemap.png', 'rb')}
            r = requests.post(url, files=files)
            del files
            image_url = json_loads(r.text)['image']
        except:
            print('vgy failed')
            pass
        print (image_url)

    if JSONBIN:
        jsonbin(no_suffix, unique, speed, geo, urls, image_url, seeds)

    del no_suffix
    del speed
    del geo
    del urls
    del image_url
    del seeds

    try:
        print('')
        print('live now, not live last round')
        print([i for i in unique if i not in previous_unique])
        print('live last round, not live now')
        print([i for i in previous_unique if i not in unique])

    except:
        pass

    previous_unique = unique[:]
    del unique

def loop():  # repeat latency test indefinitely

    print('')

    while True:
        #print("\033c")
        # Encoded Compressed Bitshares ASCII Logo
        import zlib
        b = b'x\x9c\xad\xd4M\n\xc4 \x0c\x05\xe0}O1P\x12B\x10\xbc\x82\xf7?\xd5\xf8\xaf\x83F\xe3\xe0[t\xf9\xf5%\xda>\x9f\x1c\xf7\x7f\x9e\xb9\x01\x17\x0cc\xec\x05\xe3@Y\x18\xc6(\'Z\x1a\xca.\x1bC\xa5l\r\x85\xa20\xb6\x8a\xca\xd8,W0\xec\x05\xc3\xdf\xd4_\xe3\r\x11(q\x16\xec\x95l\x04\x06\x0f\x0c\xc3\xddD\x9dq\xd2#\xa4NT\x0c/\x10\xd1{b\xd4\x89\x92\x91\x84\x11\xd9\x9d-\x87.\xe4\x1cB\x15|\xe0\xc8\x88\x13\xa5\xbc\xd4\xa21\x8e"\x18\xdc\xd2\x0e\xd3\xb6\xa0\xc6h\xa3\xd4\xde\xd0\x19\x9a\x1e\xd8\xddr\x0e\xcf\xf8n\xe0Y\rq\x1fP:p\x92\xf2\xdbaB,v\xda\x84j\xc4.\x03\xb1>\x97\xee{\x99oSa\x00\x0f\xc6\x84\xd8\xdf\x0f\xb4e\xa7$\xfdE\xae\xde\xb1/\x1d\xfc\x96\x8a'
        print(zlib.decompress(b).decode())
        del b
        start = time.time()
        try:
            thresh()

            print('elapsed: ', (time.time() - start))

            if PLOT:
                plt.pause(7200)
            else:
                time.sleep(7200)
        # no matter what happens just keep verifying book
        except Exception as e:
            print (type(e).__name__, e.args, e)
            time.sleep(1)
            pass

def update():  # run one latency test

    print('Acquiring low latency connection to Bitshares DEX' +
          ', this may take a few minutes...')
    updated = 0
    try:
        while not updated:
            thresh()
            updated = 1

    # not satisfied until verified once
    except Exception as e:
        print (type(e).__name__, e.args, e)
        pass

def main():

    # terminal header
    sys.stdout.write('\x1b]2;' + 'Bitshares latencyTEST' + '\x07')
    if LOOP:
        loop()
    else:
        update()

if __name__ == '__main__':

    main()
