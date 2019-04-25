"""
usage 1)

from bitsharesNODES import Nodes
print(Nodes.apasia())

usage 2) 

ran as a script it prints new `Nodes` class with sorted node lists

apasia
universe
excluded
since_181127
recent
short_list
github
"""


class Nodes:
    """
    Various lists of bitshares public RPC nodes
    """
    def apasia():
        """
        32 nodes hosted by the apasia infrastructure worker
        """
        return [
            "wss://api.open-asset.tech",
            "wss://atlanta.bitshares.apasia.tech",
            "wss://australia.bitshares.apasia.tech",
            "wss://bitshares.apasia.tech",
            "wss://bitshares.nu",
            "wss://canada6.daostreet.com",
            "wss://chicago.bitshares.apasia.tech",
            "wss://croatia.bitshares.apasia.tech",
            "wss://dallas.bitshares.apasia.tech",
            "wss://england.bitshares.apasia.tech",
            "wss://france.bitshares.apasia.tech",
            "wss://frankfurt8.daostreet.com",
            "wss://japan.bitshares.apasia.tech",
            "wss://miami.bitshares.apasia.tech",
            "wss://ncali5.daostreet.com",
            "wss://netherlands.bitshares.apasia.tech",
            "wss://new-york.bitshares.apasia.tech",
            "wss://ohio4.daostreet.com",
            "wss://oregon2.daostreet.com",
            "wss://paris7.daostreet.com",
            "wss://scali10.daostreet.com",
            "wss://seattle.bitshares.apasia.tech",
            "wss://seoul9.daostreet.com",
            "wss://singapore.bitshares.apasia.tech",
            "wss://slovenia.bitshares.apasia.tech",
            "wss://status200.bitshares.apasia.tech",
            "wss://testnet-eu.bitshares.apasia.tech",
            "wss://testnet.bitshares.apasia.tech",
            "wss://us-la.bitshares.apasia.tech",
            "wss://us-ny.bitshares.apasia.tech",
            "wss://valley.bitshares.apasia.tech",
            "wss://virginia3.daostreet.com",
        ]

    def universe():
        """
        123 nodes known to have existed at ANY point in time
        """
        return [
            "wss://altcap.io",
            "wss://ap-northeast-1.bts.crypto-bridge.org",
            "wss://ap-northeast-2.bts.crypto-bridge.org",
            "wss://ap-south-1.bts.crypto-bridge.org",
            "wss://ap-southeast-1.bts.crypto-bridge.org",
            "wss://ap-southeast-2.bts.crypto-bridge.org",
            "wss://api-ru.bts.blckchnd.com",
            "wss://api.bitshares.bhuz.info",
            "wss://api.bitsharesdex.com",
            "wss://api.bts.ai",
            "wss://api.bts.blckchnd.com",
            "wss://api.bts.mobi",
            "wss://api.bts.network",
            "wss://api.btsgo.net",
            "wss://api.btsxchng.com",
            "wss://api.dex.trading",
            "wss://api.fr.bitsharesdex.com",
            "wss://api.open-asset.tech",
            "wss://atlanta.bitshares.apasia.tech",
            "wss://australia.bitshares.apasia.tech",
            "wss://b.mrx.im",
            "wss://bit.btsabc.org",
            "wss://bitshares-api.wancloud.io",
            "wss://bitshares.apasia.tech",
            "wss://bitshares.bts123.cc:15138",
            "wss://bitshares.crypto.fans",
            "wss://bitshares.cyberit.io",
            "wss://bitshares.dacplay.org",
            "wss://bitshares.dacplay.org:8089",
            "wss://bitshares.neocrypto.io",
            "wss://bitshares.nu",
            "wss://bitshares.openledger.info",
            "wss://bitshares.testnet.crypto-bridge.org",
            "wss://blockzms.xyz",
            "wss://bts-api.lafona.net",
            "wss://bts-seoul.clockwork.gr",
            "wss://bts.ai.la",
            "wss://bts.liuye.tech:4443",
            "wss://bts.open.icowallet.net",
            "wss://bts.proxyhosts.info",
            "wss://bts.to0l.cn:4443",
            "wss://bts.transwiser.com",
            "wss://btsfullnode.bangzi.info",
            "wss://btsws.roelandp.nl",
            "wss://btsza.co.za:8091",
            "wss://ca-central-1.bts.crypto-bridge.org",
            "wss://canada6.daostreet.com",
            "wss://capetown.bitshares.africa",
            "wss://chicago.bitshares.apasia.tech",
            "wss://citadel.li/node",
            "wss://crazybit.online",
            "wss://croatia.bitshares.apasia.tech",
            "wss://dallas.bitshares.apasia.tech",
            "wss://de.bts.dcn.cx",
            "wss://dele-puppy.com",
            "wss://dex.iobanker.com:9090",
            "wss://dex.rnglab.org",
            "wss://dexnode.net",
            "wss://england.bitshares.apasia.tech",
            "wss://eu-central-1.bts.crypto-bridge.org",
            "wss://eu-west-1.bts.crypto-bridge.org",
            "wss://eu-west-2.bts.crypto-bridge.org",
            "wss://eu-west-3.bts.crypto-bridge.org",
            "wss://eu.nodes.bitshares.works",
            "wss://eu.nodes.bitshares.ws",
            "wss://eu.openledger.info",
            "wss://fi.bts.dcn.cx",
            "wss://france.bitshares.apasia.tech",
            "wss://frankfurt8.daostreet.com",
            "wss://freedom.bts123.cc:15138",
            "wss://japan.bitshares.apasia.tech",
            "wss://kc-us-dex.xeldal.com",
            "wss://kimziv.com",
            "wss://la.dexnode.net",
            "wss://miami.bitshares.apasia.tech",
            "wss://na.openledger.info",
            "wss://ncali5.daostreet.com",
            "wss://netherlands.bitshares.apasia.tech",
            "wss://new-york.bitshares.apasia.tech",
            "wss://node.bitshares.eu",
            "wss://node.btscharts.com",
            "wss://node.market.rudex.org",
            "wss://node.testnet.bitshares.eu",
            "wss://nohistory.proxyhosts.info",
            "wss://ohio4.daostreet.com",
            "wss://openledger.hk",
            "wss://oregon2.daostreet.com",
            "wss://paris7.daostreet.com",
            "wss://relinked.com",
            "wss://sa-east-1.bts.crypto-bridge.org",
            "wss://scali10.daostreet.com",
            "wss://seattle.bitshares.apasia.tech",
            "wss://secure.freedomledger.com",
            "wss://seoul9.daostreet.com",
            "wss://sg.nodes.bitshares.works",
            "wss://sg.nodes.bitshares.ws",
            "wss://singapore.bitshares.apasia.tech",
            "wss://slovenia.bitshares.apasia.tech",
            "wss://status200.bitshares.apasia.tech",
            "wss://testnet-eu.bitshares.apasia.tech",
            "wss://testnet-node.dynx.io",
            "wss://testnet.bitshares.apasia.tech",
            "wss://testnet.bitshares.eu",
            "wss://testnet.bts.dcn.cx",
            "wss://testnet.dex.trading",
            "wss://testnet.nodes.bitshares.ws",
            "wss://this.uptick.rocks",
            "wss://us-east-1.bts.crypto-bridge.org",
            "wss://us-la.bitshares.apasia.tech",
            "wss://us-ny.bitshares.apasia.tech",
            "wss://us-west-1.bts.crypto-bridge.org",
            "wss://us.nodes.bitshares.works",
            "wss://us.nodes.bitshares.ws",
            "wss://valen-tin.fr:8090",
            "wss://valley.bitshares.apasia.tech",
            "wss://virginia3.daostreet.com",
            "wss://ws.aunite.com",
            "wss://ws.gdex.io",
            "wss://ws.gdex.top",
            "wss://ws.hellobts.com",
            "wss://ws.winex.pro",
            "wss://wss.ioex.top",
            "wss://za.bitshares.africa",
        ]

    def excluded():
        """
        8 node mispellings and other errant data
        """
        return [
            "wss://bit.btzadazdsabc.org",
            "wss://bitazdazdshares.openledger.info",
            "wss://bitshaazdzares.openledger.info",
            "wss://bitshasdares.dacplay.org:8089",
            "wss://bitsqsdqsdhares.openledger.info",
            "wss://fake.automatic-selection.com",
            "wss://secuasdre.freedomledger.com",
            "wss://testnet.bitshares.eu/wqsdsqs",
        ]

    def since_181127():
        """
        72 nodes seen since bitshares core update 181127
        """
        return [
            "wss://altcap.io",
            "wss://api-ru.bts.blckchnd.com",
            "wss://api.bitshares.bhuz.info",
            "wss://api.bitsharesdex.com",
            "wss://api.bts.ai",
            "wss://api.bts.blckchnd.com",
            "wss://api.bts.mobi",
            "wss://api.bts.network",
            "wss://api.btsgo.net",
            "wss://api.btsxchng.com",
            "wss://api.dex.trading",
            "wss://api.fr.bitsharesdex.com",
            "wss://api.open-asset.tech",
            "wss://atlanta.bitshares.apasia.tech",
            "wss://australia.bitshares.apasia.tech",
            "wss://b.mrx.im",
            "wss://bit.btsabc.org",
            "wss://bitshares.crypto.fans",
            "wss://bitshares.cyberit.io",
            "wss://bitshares.dacplay.org",
            "wss://bitshares.dacplay.org:8089",
            "wss://bitshares.openledger.info",
            "wss://blockzms.xyz",
            "wss://bts-api.lafona.net",
            "wss://bts-seoul.clockwork.gr",
            "wss://bts.liuye.tech:4443",
            "wss://bts.open.icowallet.net",
            "wss://bts.proxyhosts.info",
            "wss://btsfullnode.bangzi.info",
            "wss://btsws.roelandp.nl",
            "wss://chicago.bitshares.apasia.tech",
            "wss://citadel.li/node",
            "wss://crazybit.online",
            "wss://dallas.bitshares.apasia.tech",
            "wss://dex.iobanker.com:9090",
            "wss://dex.rnglab.org",
            "wss://dexnode.net",
            "wss://england.bitshares.apasia.tech",
            "wss://eu-central-1.bts.crypto-bridge.org",
            "wss://eu.nodes.bitshares.ws",
            "wss://eu.openledger.info",
            "wss://france.bitshares.apasia.tech",
            "wss://frankfurt8.daostreet.com",
            "wss://japan.bitshares.apasia.tech",
            "wss://kc-us-dex.xeldal.com",
            "wss://kimziv.com",
            "wss://la.dexnode.net",
            "wss://miami.bitshares.apasia.tech",
            "wss://na.openledger.info",
            "wss://ncali5.daostreet.com",
            "wss://netherlands.bitshares.apasia.tech",
            "wss://new-york.bitshares.apasia.tech",
            "wss://node.bitshares.eu",
            "wss://node.market.rudex.org",
            "wss://nohistory.proxyhosts.info",
            "wss://openledger.hk",
            "wss://paris7.daostreet.com",
            "wss://relinked.com",
            "wss://scali10.daostreet.com",
            "wss://seattle.bitshares.apasia.tech",
            "wss://sg.nodes.bitshares.ws",
            "wss://singapore.bitshares.apasia.tech",
            "wss://status200.bitshares.apasia.tech",
            "wss://us-east-1.bts.crypto-bridge.org",
            "wss://us-la.bitshares.apasia.tech",
            "wss://us-ny.bitshares.apasia.tech",
            "wss://us.nodes.bitshares.ws",
            "wss://valley.bitshares.apasia.tech",
            "wss://ws.gdex.io",
            "wss://ws.gdex.top",
            "wss://ws.hellobts.com",
            "wss://ws.winex.pro",
        ]

    def recent():
        """
        35 nodes seen in past few  months 
        this list includes known working suffixes
        """
        return [
            "wss://altcap.io",
            "wss://ap-northeast-1.bts.crypto-bridge.org/wss",
            "wss://ap-southeast-1.bts.crypto-bridge.org/wss",
            "wss://ap-southeast-2.bts.crypto-bridge.org",
            "wss://ap-southeast-3.bts.crypto-bridge.org/ws",
            "wss://api.bitsharesdex.com/wss",
            "wss://api.bts.ai/ws",
            "wss://api.bts.mobi/wss",
            "wss://api.bts.network/ws",
            "wss://api.dex.trading",
            "wss://api.fr.bitsharesdex.com/ws",
            "wss://b.mrx.im/wss",
            "wss://bitshares.cyberit.io/ws",
            "wss://bitshares.openledger.info/wss",
            "wss://bts-api.lafona.net/wss",
            "wss://bts-seoul.clockwork.gr/wss",
            "wss://bts.liuye.tech:4443/ws",
            "wss://btsfullnode.bangzi.info/ws",
            "wss://btsws.roelandp.nl/wss",
            "wss://dex.iobanker.com:9090/ws",
            "wss://dexnode.net/ws",
            "wss://eu-central-1.bts.crypto-bridge.org/ws",
            "wss://eu.nodes.bitshares.ws/ws",
            "wss://freedom.bts123.cc:15138/wss",
            "wss://kc-us-dex.xeldal.com/wss",
            "wss://kimziv.com/ws",
            "wss://na.openledger.info/wss",
            "wss://node.bitshares.eu/wss",
            "wss://nohistory.proxyhosts.info/wss",
            "wss://openledger.hk/wss",
            "wss://sg.nodes.bitshares.ws/wss",
            "wss://us-west-2.bts.crypto-bridge.org/ws",
            "wss://us.nodes.bitshares.ws",
            "wss://ws.gdex.io/wss",
            "wss://ws.gdex.top/ws",
        ]

    def short_list():
        """
        1 nodes in user defined short list for quick testing
        """
        return [
            "wss://kc-us-dex.xeldal.com/wss",
        ]

    def github():
        """
        24 github locations known to host lists of nodes
        """
        return [
            "/AAAChain/w3ajs-ws/479b7c562fe216156edc2d38b3e22297428ea30b/test/Manager.js",
            "/BTS-CM/Bitshares-HUG-REST-API/c13ee4ae322240b17c60e42bb5c45e188fdf8d6d/work_in_progress/get_all_balances.py",
            "/BitSharesEurope/wallet.bitshares.eu/c618759e450ed645629421d6e6d063d0623652b1/app/api/apiConfig.js",
            "/Cloud-eer/cloud-ws/17f95488b444bf5ff693cd16701bad9fd4902d8b/test/Manager.js",
            "/CryptoBridge/cryptobridge-ui/e5214ad63a41bd6de1333fd98d717b37e1a52f77/app/api/apiConfig.js",
            "/InfraexDev/BTSExchange/a9de1845ceed16270e1d22752cf0a0e98841f4bd/app/api/apiConfig.js",
            "/LocalCoinIS/localcoinjs-ws/00870ec1471b69014b8076e84ba76ef8bd16f7b5/test/Manager.js",
            "/MCLXI/cb/d3842a05f052276cc0d48e5d1ece4fd4b0977dcd/app/api/apiConfig.js",
            "/bitshares/bitshares-ui/develop/app/api/apiConfig.js",
            "/bitshares/bitshares-ui/staging/app/api/apiConfig.js",
            "/blckchnd/rudex-ui/rudex/app/api/apiConfig.js",
            "/crexonline/crex/00fec97b4305d9105b19d723bccf93085bf55a12/app/api/apiConfig.js",
            "/dbxone/dbxui/4a39f849d203f28d8e27a78b5b70c4ae5b6e3f5a/app/api/apiConfig.js",
            "/denkhaus/bitshares/f73c254c7b94b36174cd0597c68b1c6c5ecb982e/api/tester.go",
            "/dexgate/dexgate-ui/b16c117df1aa13348925ca99caf12f27947ccfbc/app/api/apiConfig.js",
            "/hamzoni/zcom-ui/aed6c10417e40f9b9467a891c48aba1d64a5dc18/app/api/apiConfig.js",
            "/jhtitor/citadel/92c561a23aee20189c3827e231643f6d54ed55c1/bitsharesqt/bootstrap.py",
            "/jwaiswa7/bit_shares_exknox/046a514a31d10dba38c0ea37f3dbd14b64abecad/app/api/apiConfig.js",
            "/litepresence/extinction-event/master/EV/bitsharesNODES.py",
            "/mhowardweb/blockchain-connector/5c99251cfcb780a04f9bb06150d76a6423a7c871/vuex-bitshares/config.js",
            "/myneworder/crex-ui/eb3f77ddb81b415c83c817c8aa980abf79ac8bb5/app/api/apiConfig.js",
            "/oooautoclub/autounite-js/51c04acd6b795ad9801b2241a01ca890ec8a535e/app/api/apiConfig.js",
            "/theserranos/bitsharesAPINode/3a9a49cc566246e95a71b49389fe1eebffcfce81/config.js",
            "/zcom-project/zcomjs-ws/94dd0763c4ea0866dfffcaba568ac5f970c7d38a/test/Manager.js",
        ]


def main():
    """
    Prints a new class function with sorted lists
    """
    print("\033c")
    print("class Nodes:")
    print('    """')
    print("    Various lists of bitshares public RPC nodes")
    print('    """')
    print("    def apasia():")
    print('        """')
    print(
        "        %s nodes hosted by the apasia infrastructure worker"
        % len(Nodes.apasia())
    )
    print('        """')
    print("        return [")
    nodes = [('            "' + node + '",') for node in sorted(Nodes.apasia())]
    for node in nodes:
        print(node)
    print("        ]\n\n    def universe():")
    print('        """')
    print(
        "        %s nodes known to have existed at ANY point in time"
        % len(Nodes.universe())
    )
    print('        """')
    print("        return [")
    nodes = [('            "' + node + '",') for node in sorted(Nodes.universe())]
    for node in nodes:
        print(node)
    print("        ]\n\n    def excluded():")
    print('        """')
    print("        %s node mispellings and other errant data" % len(Nodes.excluded()))
    print('        """')
    print("        return [")
    nodes = [('            "' + node + '",') for node in sorted(Nodes.excluded())]
    for node in nodes:
        print(node)
    print("        ]\n\n    def since_181127():")
    print('        """')
    print(
        "        %s nodes seen since bitshares core update 181127"
        % len(Nodes.since_181127())
    )
    print('        """')
    print("        return [")
    nodes = [('            "' + node + '",') for node in sorted(Nodes.since_181127())]
    for node in nodes:
        print(node)
    print("        ]\n\n    def recent():")
    print('        """')
    print("        %s nodes seen in past few  months " % len(Nodes.recent()))
    print("        this list includes known working suffixes")
    print('        """')
    print("        return [")
    nodes = [('            "' + node + '",') for node in sorted(Nodes.recent())]
    for node in nodes:
        print(node)
    print("        ]\n\n    def short_list():")
    print('        """')
    print(
        "        %s nodes in user defined short list for quick testing"
        % len(Nodes.short_list())
    )
    print('        """')
    print("        return [")
    nodes = [('            "' + node + '",') for node in sorted(Nodes.short_list())]
    for node in nodes:
        print(node)
    print("        ]\n\n    def github():")
    print('        """')
    print(
        "        %s github locations known to host lists of nodes" % len(Nodes.github())
    )
    print('        """')
    print("        return [")
    nodes = [('            "' + node + '",') for node in sorted(Nodes.github())]
    for node in nodes:
        print(node)
    print("        ]")


if __name__ == "__main__":

    main()
