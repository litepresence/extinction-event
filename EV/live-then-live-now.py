'litepresence2018'

compare three lists

# LIVE THEN
# MAX LIVE SINCE 181127
a = ['wss://status200.bitshares.apasia.tech/wss', 'wss://us-east-1.bts.crypto-bridge.org/ws', 'wss://us-ny.bitshares.apasia.tech/ws', 'wss://api.bts.network', 'wss://new-york.bitshares.apasia.tech/ws', 'wss://blockzms.xyz/wss', 'wss://api.bts.mobi/ws', 'wss://chicago.bitshares.apasia.tech/ws', 'wss://bts-api.lafona.net/wss', 'wss://btsfullnode.bangzi.info/ws', 'wss://dallas.bitshares.apasia.tech/ws', 'wss://na.openledger.info/ws', 'wss://api.bitsharesdex.com', 'wss://relinked.com/ws', 'wss://atlanta.bitshares.apasia.tech/wss', 'wss://api.bitshares.bhuz.info', 'wss://kc-us-dex.xeldal.com/wss', 'wss://la.dexnode.net/wss', 'wss://dexnode.net/wss', 'wss://altcap.io/wss', 'wss://dex.rnglab.org/wss', 'wss://node.bitshares.eu/wss', 'wss://netherlands.bitshares.apasia.tech/wss', 'wss://api.bts.blckchnd.com', 'wss://api.fr.bitsharesdex.com/wss', 'wss://us-la.bitshares.apasia.tech/ws', 'wss://eu.nodes.bitshares.ws/wss', 'wss://bitshares.openledger.info/wss', 'wss://bts.proxyhosts.info/wss', 'wss://eu.openledger.info/wss', 'wss://node.market.rudex.org/wss', 'wss://us.nodes.bitshares.ws/wss', 'wss://eu-central-1.bts.crypto-bridge.org/wss', 'wss://api.dex.trading/wss', 'wss://btsws.roelandp.nl/ws', 'wss://england.bitshares.apasia.tech/ws', 'wss://seattle.bitshares.apasia.tech/wss', 'wss://api-ru.bts.blckchnd.com/wss', 'wss://ws.gdex.io/wss', 'wss://b.mrx.im/ws', 'wss://ws.hellobts.com/wss', 'wss://api.btsxchng.com/ws', 'wss://bts-seoul.clockwork.gr/wss', 'wss://openledger.hk/wss', 'wss://bitshares.cyberit.io', 'wss://australia.bitshares.apasia.tech/wss', 'wss://api.bts.ai/wss', 'wss://ws.gdex.top/wss', 'wss://bts.liuye.tech:4443/ws', 'wss://bitshares.dacplay.org:8089', 'wss://bts.open.icowallet.net/ws', 'wss://bit.btsabc.org/wss', 'wss://sg.nodes.bitshares.ws/wss', 'wss://nohistory.proxyhosts.info/wss', 'wss://bitshares.dacplay.org/ws', 'wss://api.btsgo.net/ws', 'wss://kimziv.com/ws', 'wss://crazybit.online']

# UI MASTER LIST
b = ['wss://ap-northeast-1.bts.crypto-bridge.org', 'wss://ap-southeast-1.bts.crypto-bridge.org', 'wss://ap-southeast-2.bts.crypto-bridge.org', 'wss://api-ru.bts.blckchnd.com', 'wss://api.bitshares.bhuz.info', 'wss://api.bitsharesdex.com', 'wss://api.bts.ai', 'wss://api.bts.blckchnd.com', 'wss://api.bts.mobi', 'wss://api.bts.network', 'wss://api.btsgo.net', 'wss://api.btsxchng.com', 'wss://api.dex.trading', 'wss://api.fr.bitsharesdex.com', 'wss://api.open-asset.tech', 'wss://atlanta.bitshares.apasia.tech', 'wss://australia.bitshares.apasia.tech', 'wss://bit.btsabc.org', 'wss://bitshares.bts123.cc:15138', 'wss://bitshares.crypto.fans', 'wss://bitshares.cyberit.io', 'wss://bitshares.nu', 'wss://bitshares.openledger.info', 'wss://blockzms.xyz', 'wss://bts-api.lafona.net', 'wss://bts-seoul.clockwork.gr', 'wss://bts.liuye.tech:4443', 'wss://bts.open.icowallet.net', 'wss://bts.proxyhosts.info', 'wss://btsfullnode.bangzi.info', 'wss://btsws.roelandp.nl', 'wss://canada6.daostreet.com', 'wss://chicago.bitshares.apasia.tech', 'wss://citadel.li/node', 'wss://crazybit.online', 'wss://dallas.bitshares.apasia.tech', 'wss://de.bts.dcn.cx', 'wss://dex.rnglab.org', 'wss://dexnode.net', 'wss://england.bitshares.apasia.tech', 'wss://eu-central-1.bts.crypto-bridge.org', 'wss://eu-west-1.bts.crypto-bridge.org', 'wss://eu-west-2.bts.crypto-bridge.org', 'wss://eu.nodes.bitshares.ws', 'wss://fake.automatic-selection.com', 'wss://fi.bts.dcn.cx', 'wss://france.bitshares.apasia.tech', 'wss://freedom.bts123.cc:15138', 'wss://japan.bitshares.apasia.tech', 'wss://kc-us-dex.xeldal.com', 'wss://kimziv.com', 'wss://la.dexnode.net', 'wss://miami.bitshares.apasia.tech', 'wss://na.openledger.info', 'wss://netherlands.bitshares.apasia.tech', 'wss://new-york.bitshares.apasia.tech', 'wss://node.btscharts.com', 'wss://node.market.rudex.org', 'wss://node.testnet.bitshares.eu', 'wss://openledger.hk', 'wss://seattle.bitshares.apasia.tech', 'wss://sg.nodes.bitshares.ws', 'wss://status200.bitshares.apasia.tech', 'wss://testnet-eu.bitshares.apasia.tech', 'wss://testnet.bitshares.apasia.tech', 'wss://testnet.bts.dcn.cx', 'wss://testnet.dex.trading', 'wss://testnet.nodes.bitshares.ws', 'wss://us-east-1.bts.crypto-bridge.org', 'wss://us-la.bitshares.apasia.tech', 'wss://us-west-1.bts.crypto-bridge.org', 'wss://us.nodes.bitshares.ws', 'wss://valley.bitshares.apasia.tech', 'wss://ws.gdex.top', 'wss://ws.hellobts.com', 'wss://ws.winex.pro']

# LIVE NOW
c = ['wss://new-york.bitshares.apasia.tech/wss', 'wss://bts-api.lafona.net/ws', 'wss://node.bitshares.eu/wss', 'wss://netherlands.bitshares.apasia.tech/ws', 'wss://node.market.rudex.org/ws', 'wss://paris7.daostreet.com/ws', 'wss://us.nodes.bitshares.ws/ws', 'wss://dex.rnglab.org/ws', 'wss://eu.nodes.bitshares.ws/ws', 'wss://blockzms.xyz/wss', 'wss://btsfullnode.bangzi.info/wss', 'wss://api.dex.trading/wss', 'wss://seattle.bitshares.apasia.tech/ws', 'wss://api.bts.mobi', 'wss://us-ny.bitshares.apasia.tech/ws', 'wss://atlanta.bitshares.apasia.tech/wss', 'wss://scali10.daostreet.com/ws', 'wss://bts.proxyhosts.info/wss', 'wss://bitshares.openledger.info/ws', 'wss://england.bitshares.apasia.tech/ws', 'wss://eu-central-1.bts.crypto-bridge.org', 'wss://dallas.bitshares.apasia.tech/wss', 'wss://eu.openledger.info/ws', 'wss://us-east-1.bts.crypto-bridge.org', 'wss://api.bitshares.bhuz.info', 'wss://na.openledger.info/ws', 'wss://us-la.bitshares.apasia.tech/ws', 'wss://bit.btsabc.org/wss', 'wss://france.bitshares.apasia.tech/wss', 'wss://bitshares.cyberit.io', 'wss://api.bts.blckchnd.com/wss', 'wss://la.dexnode.net/ws', 'wss://openledger.hk/ws', 'wss://frankfurt8.daostreet.com/ws', 'wss://valley.bitshares.apasia.tech/wss', 'wss://bts.liuye.tech:4443/ws', 'wss://ws.hellobts.com/ws', 'wss://b.mrx.im/ws', 'wss://nohistory.proxyhosts.info/wss', 'wss://singapore.bitshares.apasia.tech/wss', 'wss://ws.gdex.io/wss', 'wss://ncali5.daostreet.com/ws']

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

a = validate(a)
b = validate(b)
c = validate(c)

print('MAX LIVE SINCE 181127')
print('a', len(a), a)
print('')
print('UI MASTER')
print('b', len(b), b)
print('')
print('LIVE NOW')
print('c', len(c), c)
print('')


print('LIVE THEN NOT LIVE NOW')
print([i for i in a if i not in c])
print('')
print('LIVE NOW NOT IN UI MASTER')
print([i for i in a if i not in b])
print('')
print('UI MASTER BUT NOT LIVE')
print([i for i in b if i not in a])
print('')
print('LIVE SINCE THEN AND IN UI MASTER')
d = [i for i in a if i in b]
print(d)
print('')
print('LIVE SINCE THEN AND UI MASTER BUT NOT LIVE NOW')
e = [i for i in d if i not in c]
print(e)
