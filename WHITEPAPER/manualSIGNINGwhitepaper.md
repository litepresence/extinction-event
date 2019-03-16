
manualSIGNING.py - Bitshares Limit Order Transaction Signing

litepresence2019

I'm about to break down some crypto hocus pocus, so focus!

:D 

First of all... Why?  Doesn't Pybitshares do this?

Indeed it does and it works well: in auditing and development on the DEX, I have personally executed hundreds of thousands of Bitshares DEX buy/sell/cancel operations through pybitshares. The package is tried and true. I'm humbled, impressed, I see what they (well @xeroc mostly) did there... wow: The DEX works and Pybitshares works it.   Pybitshares is capable of doing just about EVERYTHING on the bitshares blockchain.  You can create accounts, propose workers, vote, and perform a myriad of other blockchain functions; some of which I've yet to even explore.  

This broad ability comes at a price:  Pybitshares is 2MB; 60,000 lines of python divided into several folders, each containing dozens of *.py scripts.  At runtime it will depend upon a wallet within a SQL database created by the uptick utility.  The package is often updated, with a back log of feature requests and issues - to be expected - with do-all software of this sort. It is by no means a lightweight utility; it is not something you can read from top to bottom and have any sense of - or unfortunately have inherent faith in - how it all works; it is overwhelming at first glance.

Pybitshares uses several layers of abstraction with each action you request of it.  A simple limit order request passes through many python scripts, classes, and definitions prior to broadcast; you will need many document tabs open to follow it all.  You will need to go from tab to tab and back twice more.  Complicating things Pybitshares shares architecture with several other graphene chains.  To maintain cross chain compatibility, this also ads many layers of abstractions. Pybitshares offers custom passphrase compatibility in place of wif keys and allows multiparty lists of wif keys.  Finally, it maintains a persistent websocket connection... each of these features ads yet more abstraction.  

There is nothing "wrong" with this process; especially not for a simple action like making a single vote or even a more obscure action like creating an asset.  Further, realistically, to do everything pybitshares does - to be "reference" software - for every chain it serves, you NEED this type of architecture.   

However, when performing thousands of - specific and repetitive - actions, on only BTS chain, during the course of algo trading you do begin to question... what if there was some unseen flaw in one of these 60,000 lines of code that I missed?  What is all this sorcery between my request and its broadcast?  What if some unseen floating point math error causes microloss^1000? Nobody ever saw it because it was in that one file, in that one folder, that nobody looks at... and nobody expected me to place 100k orders this month to expose the vulnerability.  Do I really need to be using a swiss army knife to cut my algo trading steak dinner?  

I have set out to produce a single script, just 50KB; 1500 lines of code, you can read over a cup of coffee.  

It authenticates ONLY Bitshares DEX buy/sell/cancel.  I will be using the established; albeit stripped down, condensed, and merged methods set forth by pybitshares to do so.  The end goal is to provide to you a method:

>
> from manualSIGNING import broker
>
> broker(order) # broadcast signed buy/sell/cancel transaction to the network
>

now DEX "wallet" is 50KB script instead of 2 MB software
========++++++++========================================
buy/sell/cancel have their independence from pybitshares


THE BACKBONE OF EVENTS

0) place orders in human terms
1) establish a dex connection
2) convert orders to graphene terms
3) serialize the transaction 
4) validate the serialization
5) sign the serialzed message with a wif using ECDSA
6) validate the signed transaction
7) broadcased the validated transaction to the network

COMPLETED OBJECTIVES

'import only standard python objects'
'gather needed pybitshares objects: copy, paste, and cite' 
'strip pybitshares objects of unused methods'
'restack classes and definitions chronologically'
'allow orders to be placed in human terms'
'build tx in graphene terms'
'serialize tx'
'validate serialization via get_transaction_hex_without_sig()'
'sign tx with ECDSA'
'validate signed tx'
'broadcast tx to rpc node'
'allow this script to be imported as module; broker(order)'
'allow list of buy/sell operations'
'allow list cancel operations'
'allow cancel all'
'heavy line-by-line commentary'

REMAINING PYBITSHARES DEPENDENCIES

none! 

PLACE ORDERS IN HUMAN TERMS

order = {   'op': 'buy',
            'wif': '',
            'nodes':    [
                        'wss://chicago.bitshares.apasia.tech/wss',
                        'wss://new-york.bitshares.apasia.tech/ws',
                        ],
            'params':   [
                        {'amount'       : 10.0,
                        'price'         : 0.00000100,
                        'expiration'    : 0},
                        ],
            'header':   { 
                        'asset_id'          : '1.3.x',
                        'currency_id'       : '1.3.x',
                        'asset_precision'   : 5,
                        'currency_precision': 8,
                        'account_id'        : '1.2.x',
                        'account_name'      : '',
                        } }

The new `broker(order)` method requires that you create an order in the format of a dictionary with 5 keys: 

['op', 'wif', 'nodes', 'params', 'header']

'op' 

can be one of ['buy', 'sell', 'cancel']

'wif' 

is your wallet import format key that can be obtained from the Bitshares reference UI.

'nodes' 

is a list of nodes which you have whitelisted in some manner to use for trading; they should be known to be responsive and on the correct chain identifier.  I provide an additional utility to do this in automated fashion which I call latencyTEST.py. latencyTEST, in a loop which updates each hour, writes a list of whitelisted nodes to nodes.txt.  It would then be up to the developer to read and feed into each new order the updated list.  Alternatively, you could also use a static/manual whitelist with each order or devise your own method of dynamically whitelisting. 

'params' 

is a list of operations, in the case of buy and sell orders, each operation is a dictionary with 3 keys:

['amount', 'price', 'expiration']
    
'amount' and 'price' 

are expressed in decimal terms as you would at any centralized exchange.  We are speaking here of "buying assets" in prices denominated in "currency".  Example would be buying BTC assets in USD currency for $4000.   

In the case of 'cancel' orders you will still need to provide a list of 'params' but each element will be a order id instead of a dictionary.  For our puposes, it should be noted that the a.b.c system identifies accounts as 1.2.X, assets as 1.3.X, and orders as 1.7.X.  

You can cancel as many orders as you like in one transaction.  As an example if you wished to cancel 4 orders you would pass to params:

['1.7.3486981','1.7.3486982','1.7.3486983','1.7.3486984']

manualSIGNING 'cancel' also allows for a "cancel all" orders, on one account, in one market, in the following 3 part format:

['1.7.X', '1.3.0', '1.3.861']

This tells the script to cancel all '1.7.X', in the bitshares '1.3.0' vs open.btc '1.3.861' market. 

'expiration' 

is an integer of seconds since the unix epoch; Jan 1, 1970.  This is the time format returned by time.time().  You can use (time.time() + 86400) and it will cancel the order 86400 seconds in the future; one day.  You also have the option to set expiration to int(0), this will flag manualSIGNING to resolve the expiration to 75 years in the future.

'header'

will require a bit of legwork on the developers behalf, which I demonstate in the sample script manualSIGNINGexample.py.  Essentially, you will need to request some information from a public api node and cache this information when you initialize your script.  Every order your botscript places will require the same header and there is no reason to have manualSIGNING repeat this header creation process at every request as it will only slow things down.

For a buy or sell order you will need to provide a dictionary with the following keys:

'header':   { 
            'asset_id'          : '1.3.x',
            'currency_id'       : '1.3.x',
            'asset_precision'   : 5,
            'currency_precision': 8,
            'account_id'        : '1.2.x',
            'account_name'      : '',
            } }

On the graphene backend, to save space on the blockchain, there are no decimal places in any of the amounts or prices.   Everything is stored as integer and we use a cached "precision" to locate the decimal place such that:

human_amount_of_asset = graphene_amount_of_asset / (10 ^ graphene_precision_for_that_asset)

Every asset on the DEX has a precision, always an integer and usually between 3 and 10; for example: bitshares is 5, bitcoin is 8.  So if I want to buy 6 bitshares, in graphene terms this is 600000 / 10^5 bitshares; amount 600000 with precision 5

Every asset ticker symbol and account name on the dex also has a unique identity in a.b.c format. You will obviously know the account name you wish to use and the - human terms - asset and curreny ticker symbols. From those you can derive the "header" by making the following requests to a public node using the wss_query() method as shown in manualSIGNINGexample.py.

rpc_lookup_accounts(account_name) # returns account id in 1.7.X format
rpc_lookup_asset_symbols(asset, currency) # returns both asset's ids (1.3.X) and precisions as integers

Here we concluded what you will need to provide to manifest an order, the remainder will be handled by manualSIGNING.py

If you are a bot trader looking to buy/sell/cancel on the dex, take a peak at manualSIGNINGexample.py and put manualSIGNING.py in the same folder as your botscript:

>
> from manualSIGNING import broker
>
> broker(order)
>

DONE

>>> manualSIGNING has broadcast your order



...but if you would like to take greater responsibility for all code between your algo and the blockchain, read on...


ESTABLISH A DEX CONNECTION

Pybitshares creates a persistent websocket connection to a single node and uses a secondary thread ping to stay connected. It accomplishes this with the websocket-client module.  We will be using the same module but taking an alternative; more lightweight approach.  For each request, manualSIGNING will create a new websocket connection, we'll use it for our order and terminated thereafter.  

Our incoming order already gives us a list of whitelisted nodes to attempt to use; this list can be dynamically generated by our botscript.  Given that list:

wss_handshake() 

will attempt to create a websocket handshake in less than 3 seconds, else switch nodes and wait a bit and try again.   Once it has created the websocket connection we will name it "ws" and push it to the global space to be used by our RPC calls.  If the process continually fails our "wait a bit" will increase exponentially.

wss_query() 

then serves as a template to make various remote procedure call request in json format; that is... dictionaries using only double quotes; with our websocket connected, all requests hereafter should take hundreds of milliseconds or less.

the dictionary format of the query is:

query = json_dumps({"method": "call",
                    "params": params,
                    "jsonrpc": "2.0",
                    "id": info['id']})

"method" and "jsonrpc" will always be the same; "call" and "2.0" repsectively

"id" can simply be a constant, it is just a marker for you to keep track of your own requests.  As a convenience, manualSIGNING will increment by one after each request, but this function is not strictly necessary.

What is important is the "params" field, the format of which is always a list of three items:

["location", "object", []]

For database requests we'll use "database" as the location, then one of the "database" type rpc requests as the "object", for example:

wss_query(["database", "get_dynamic_global_properties", []])

Would pass an (empty) list as params in order to fetch such "dynamic_global_properties" from the "database" as the block number.  For other requests we will need to add arguments to our empty list.

Later, for transactions, we use use "network broadcast" as location and "broadcast_transaction" as the "object".  The list in this final request will contain our signed transaction.  Otherwise, however, all other requests we make will be made to the "database" location.

With our websocket established we can now convert our order to graphene terms:


CONVERT ORDER TO GRAPHENE TERMS AND PREPARE FOR SERIALIZATION

A single graphene Limit_order_cancel operation is a list with two items:

operation = [2, 
            OrderedDict([
                        ('fee',                 fee),
                        ('fee_paying_account',  account_id),
                        ('order',               order_id),
                        ('extensions',          [])
                        ])
            ]

The first item; number 2, signifies that this is a "Limit_order_cancel" operation

The second item; the ordered dictionary, provides the information required to cancel one order.  It is crucial that this dictionary be ordered as it will later be serialized into the transaction - in order.  

'fee_paying_account' is simply your account_id which we cached earlier

'fee' will be fetched with an RPC request:

rpc_get_required_fees(op, account_id)

Don't get too lost in "omg I have to pay to cancel order":  +/- it costs about $100 to be a lifetime Bitshares member and cancelling 10,000 orders is a $1 thereafter; peanuts.  Cancellation fees are 1/10 of creation fees and creation fees are only paid when and if an order actually transacts on the blockchain before being cancelled/expiring.

'seller' 

is the same "account_id" we cached earlier

'extensions'

In the case buy/sell/cancel 'extensions' MUST be present but will ALWAYS be an empty list; []

Both "buy" AND "sell" will be handled by the graphene "Limit_order_create" operation which takes the following ORDERED format:

operation = [1, 
            OrderedDict([
                ('fee', fee),  # OrderedDict
                ('seller', account_id),  # "a.b.c"
                ('amount_to_sell', amount_to_sell),  # OrderedDict
                ('min_to_receive', min_to_receive),  # OrderedDict
                ('expiration', op_expiration),  # ISO8601
                ('fill_or_kill', False),  # always False for our purpose
                ('extensions', [])  # always empty list for our purpose
            ])]

First, we see the 2, for "Limit_order_cancel"; has been replaced by a 1, for "Limit_order_create".

Then, you will note that no price is specified and no mention of whether it is a buy or sell operation.  It is up to the developer here to convert the three humans-terms vectors of "buy/sell" "price" and "amount" to graphene terms of "min_to_recieve" "amount_to_sell".   

some things to note here:

It is important to use the decimal class when dealing with these conversion for increased precision. 

human terms "buy asset with currency" in graphene terms means SELLING currency RECEIVING assets
human terms "sell assets for currency" in graphene terms means means SELLING assets RECEIVING currency

example:

human terms "buying" bitcoin (BTC) asset for $1000 (USD) currency 

    means "SELLING AMOUNT OF USD" while asserting "MINIMUM BTC TO RECEIVE" in graphene terms

human terms "selling" bitcoin (BTC) asset for $1000 (USD) currency at a centralized exchange

    means "SELLING AMOUNT OF BTC" while asserting "MINIMUM USD TO RECEIVE" in graphene terms

Note again we are always SELLING one thing and RECEIVING something else in return.  We never "buy" on the backend and we never speak in prices, just amounts...    

"amounts" in graphene terms must be integers without their "precision"

the fee, amount_to_sell, and min_to_receive values are themselves ORDERED dictionaries in the following format:

('amount_to_sell', OrderedDict([('amount', 999), ('asset_id', '1.3.861')]))
('min_to_receive', OrderedDict([('amount', 1000000), ('asset_id', '1.3.0')]))

in human terms, this means buy 10 bitshares with open.btc at 100 satoshi; 0.00000100

likewise a fee appears like this:

('fee', OrderedDict([('amount', 578), ('asset_id', '1.3.0')]))

divided by the asset precision of 1.3.0; bitshares; (5) this is 

578/10^5 = 0.00578 BTS; 

This leaves the "kill_or_fill" element of the  "Limit_order_create" operation.  For simplicity sake, manualSIGNING does not expose this option to auto cancel an order if it does not fill immediately.  The value defaults to False.

The last element of building the transaction is to add the operations to the transaction itself.

The transaction always takes the form of a dictionary, but it need not be an ordered dictionary as we will handle its order manually when serializing the transaction later.  This is the format of the dictionary.

    tx = {'ref_block_num'       : ref_block_num,
          'ref_block_prefix'    : ref_block_prefix,
          'expiration'          : tx_expiration,
          'operations'          : tx_operations,
          'signatures'          : [],
          'extensions'          : []
          }

For our limit order purposes extension is ALWAYS an empty list; [].  For the time being, signatures is also an empty list; [] - a place holder because we have yet to sign this transaction.

Reference block number and prefix will need to be fetched from the chain with a websocket call, and then manipulated prior to insertion thus:

dgp = rpc_get_dynamic_global_properties()

    ref_block_num       = dgp["head_block_number"] & 0xFFFF
    ref_block_prefix    = unpack_from("<I", unhexlify(dgp["head_block_id"]), 4)[0]

the tx_expiration will be added here as ISO8601 time format; ie '2019-01-21T19:03:25'

tx_expiration is always just 2 minutes into the future:

    to_iso_time(time.time()+120)

Finally we add our tx_operation to the tx as a list; [] containing each of the operations we just created in the previous step; so a list [of two element lists].  The 2 elements being first integers ((1 or 2) for (create or cancel)) then ordered operation dictionaries. 

Although graphene can process operations of multiple types in a single transaction, to keep things simple manualSIGNING will only create lists of buy dicts, list of sell dicts, or lists of cancel a.b.c's. If you wish to broadcast only one operation, it needs to be contained as the single element of a list.  


A QUICK DISCUSSION OF PYTHON MAGIC METHODS

Serializing the transaction is a matter of converting the data contained therein into bytes, and doing so in both a very specific order, and a very specific manner for each datum so represented.  We serialize it on this side in order, it gets deserialized on the other side in order and we are able to communicate effectively.

struct is a standard python package

    from struct import pack, unpack

"performs conversions between Python values and C structs represented as Python strings. This can be used in handling binary data[.] It uses Format Strings as compact descriptions of the layout of the C structs and the intended conversion to/from Python values." 

https://docs.python.org/2/library/struct.html 

Keep that tidbit in mind while I introduce you to python's "dunder" / "magic" methods which will be used extensively in this section.  These methods are a little abstract and under documented, 

so to elucidate: 

bytes() is a "built in" function like str(), int(), list().  It returns byte strings like: b'\x00\x00\x00'.  The "graphenebase types" methods will redefine the type of byte string returned by the "built in" bytes() in global space, but only when bytes() is called on an object that has passed through a class with a "magic" __bytes__ method. This is done to efficiently pack C structs of different data types; signed vs unsigned integers, 8 bit vs 64 bit data size, etc.  These methods will be used to serialize the OrderDicts of various elements we prepared in the previous step. 

All of this data type classing prior to serialization is done as a matter of efficiently encoding data onto the blockchain while taking up as little space as possible. 

For our puposes, with limit order create and cancel, graphenebase  __str__() methods have been mostly removed from their respective class functions.  Most classes now contain just __init__ and __bytes__.  Looking forward, with only a single method beyond init; this point to the notion that - for limit orders - we could remove yet another layer of abstraction by converting these magic classes to more simplistic definitions.  That exercise is for another day.

Lastly, the following graphenebase methods have been merged for clarity:

    # Set() has been merged into Array()
    # Bool() has been merged into Uint8()
    # Varint32() has been merged into both Id() and Array()

Consider the following "magic method" example:

    # this would have no effect on the way bytes() normally behaves
    class normal():
        def __init__(self, d):
            self.data = int(d)
        def __bytes__(self):

            return bytes(self.data)  # "regular bytes of self data"

    # this redifines bytes() in global to pack unsigned 8 bit integers
    # but only in the case of bytes(Uint8(x))
    class Uint8():
        def __init__(self, d):
            self.data = int(d)
        def __bytes__(self):

            return pack("<B", self.data) # here were using struct to pack the data as "little endian unsigned char bytes"

    # this is a less abstract definition method to accomplish the same task without the "magic" notation.
    def bytes_Uint8(data):
        return pack("<B", int(data))

    # apply each of these methods to x=3 to show what happens
    x = 3
    print(bytes(x))
    print(bytes(normal(x)))
    print(bytes(Uint8(x)))
    print(bytes_Uint8(x))
    '''
    # >>>
    # b'\x00\x00\x00'
    # b'\x00\x00\x00'
    # b'\x03'
    # b'\x03'
    '''

SERIALIZE THE TRANSACTION

There are two ways to serialize the transaction and the outcomes should be the same.  You can do so manually and you can do so via RPC allowing the graphene backend to serialize for you.  By doing both and insisting upon the results being the same we can ensure the transaction is serialized correctly.  

Nonetheless, the RPC method is easy so lets get it out of the way:

rpc_tx_hex = rpc_get_transaction_hex_without_sig(tx)

done.

Pause for a second and reflect here.  If we could get the api to serialize this transaction for us.... and we did not have to provide it in ordered dictionary form...and we did not have to perform conversion to various bytes of cstruct types:  Why did we just do all that work?  Academic curiosity?   We could just call it done here.  So... to venture down that rabbit hole I forked this script and stopped right there and lo and behold I was able to cut out 700 some lines of seralizing and typing and even verifying too because what is to verify if we just have the server do it for us? Right? Nothing.  All is good.  Yeah!  Well... actually NO.  I had that itchy feeling that I was doing the crypto dirty... so off to telegram BitsharesDEV to have a peer chit chat:

    litepresence 
        Q  does relying on server side serialization expose vulnerability 
        to an unwanted order transaction or can this method be trusted as "gold standard" 
        because as fallback you'll still be specifying the order again during broadcast in the json?

    clockwork 
        say you want to transfer 10 bts to account X
        a malicious api node could provide a serialisation that transfers 10000 BTS to account Y instead

    litepresence 
        then u sign it 
        yikes! definately disregard... this is NOT the way you should not do things!

So back to our due diligence...

The manual method is a bit more involved, but not altogether that complicated when you break it down.  Step one is serialize the block number, prefix, and tx_expiration:

    buf = b'' # begin by declaring buffer to be an empty byte string

    buf += pack("<H", tx["ref_block_num"])                  # <H little endian 2 byte short unsigned int
    buf += pack("<I", tx["ref_block_prefix"])               # <I little endian 4 byte unsigned int
    buf += pack("<I", from_iso_date(tx['expiration']))      # <I little endian 4 byte unsigned int

The from_iso_date function converts ISO8601 time back to unix time. 

Next we'll add length of operations list to buffer, for this we'll use a method called "varint"; it allows for very small byte strings to describe most numbers efficiently, but also allows for numbers of unlimited size,  In most cases the length of our operations list is very small... so no need to waste space on the blockhain 64 byte numbers... but occassionally a user might like to send out a large number of operations, maybe an "airdrop".  "varint" handles this edge case for us while retaining data size efficiency for the common case:

    buf += bytes(varint(len(tx["operations"])))

The next step is to add each individual operation to the buffer in graphene fashion:
    
Remember every operation is a list of two items, an integer and a dictionary.   For each operation, in the operations list, of the transaction, we'll serialize the leading number as a varint(); (1=create, 2=cancel); referencing this as op[0]

        buf += varint(op[0])

And then depending on whether it is a create or cancel operation we'll format each element of the ordered dictionary correctly using the "magic bytes" methods described earlier:

        if op[0] == 1:
            buf += bytes(Limit_order_create(op[1])) # magic/dunder bytes of a CREATE OrderedDict
        if op[0] == 2:
            buf += bytes(Limit_order_cancel(op[1])) # magic/dunder bytes of a CANCEL OrderedDict

Limit_order_create and Limit_order_cancel are templates which instruct the bytes method how to serialize each contained element

Finally, we will add the length of the empty extension list to the buffer also using the varint method as used for the operation list size:

    buf += bytes(varint(len(tx["extensions"]))) # effectively varint(0) "extensions" is always empty list for limit orders.

We now have the final manual transaction hex and this should match the transaction hex we obtained first via rpc request to public node.

    assert(rpc_tx_hex == manual_tx_hex)

After we are sure the rpc_tx_hex matches the manual_tx_hex we add the Bitshares chain ID to the buffer, it is a globally declared constant.

    message = unhexlify(ID) + buf

This message; the serialized transaction will then be joined with a wif in the signing process

ELIPTICAL CURVE DIGITAL SIGNATURE ALGORITHM (ECDSA)

This is where the real hocus pocus of crypto lies.  All of the ordering, typing, serializing, and digesting culminates with the message meeting the wif to create a signature.

Eliptical curve digital signature agorithm produces a deterministic signature which retains the cryptographic security features associated with other digital signatures but can be more easily implemented in any environment since they do not need high-quality randomness.

To perform the signature we will need borrow some modules from two well maintained cryptographic python repositories

    import ecdsa        # this is the number theory behind the calculations of private keys
    import secp256k1    # efficient parameters for ecdsa curve, namely: y^2 = x^3 +7

While I generally prefer not to use custom modules, these two are monitored by the broader cryptography community and have changed little since they were first introduced.  I do encourage you to look them over after pip3 install.  Like pybitshares, each package performs more than we need of it and could be cropped down to our specific use case. However, that would be another undertaking, in itself, for another time.  So for now... we'll use the modules in good faith.  

This said, let me describe - short and skinny, 250 words or less (slightly bullshit back of napkin version I admit) - what is happening here because it is noteworthy, often neglected and actually quite simple.

We have the "elipitcal" curve Y^2 = X^3 +7; reflected over the x axis as to form a sideways U shape, we call this curve secp256k1

Its very special with a fundamental property that any line that intersects at least two points must also intersect a third except for vertical and tangent lines.  

We begin at an origin point on the curve, our transaction. We pick a random number, our private key.

We perform an algorithm method whereby we iterate from point to point on the curve, with pre defined geometric rules.  The rules involve paths alternately traveling tangent to the curve to the next intersection, then vertically to the next intersection, for our randomly selected NUMBER of iterations; the PRIVATE key, from our initial point, we get our end point on the curve: the PUBLIC key.

What is magic about this is that given any two points on the curve its impossible to calculate the number of iterations to get from A to B.  But given point A and the number of iterations, (the private key) you can always, with very little effort, arrive again at point B (the public key); this the "one way cryptographic trap door"

for 250 words+ discussion see:
https://ebrary.net/7940/education/moving_around_line
https://onekosmos.com/blog/the-elliptic-curve-digital-signature-algorithm/
https://www.instructables.com/id/Understanding-how-ECDSA-protects-your-data/
https://blog.cloudflare.com/a-relatively-easy-to-understand-primer-on-elliptic-curve-cryptography/


THE SIGNING

Now lets use the ecdsa and secp256k1 modules to perform this fancy iterative calculation to begin the actual signing:

The first step in signing the transaction is to perform a hash function on the incoming serialized message.  Hash functions create a fixed length representation of otherwise arbitrary length data.  This hash "digest" can later be reversed to retrieve the original data.  The hash of the data is a relatively small, so signing hash is more efficient than signing serialization.  We will use sha256 for this purpose.

    digest = sha256(message).digest()

The process of signing with ECDSA requires a loop which creates a new signature and passes it through two criteria:  Is it deterministic?  Is it canonical?

1 in 4 ECDSA signatures are randomly canonical; "normal form", using the other three causes vulnerability to maleability attacks.  As a metaphor; we will "require reduced fractions in simplest terms".  The test of whether a potential signature (sig) a canonical signature is:

(not (int(sig[0]) & 0x80) and
 not (sig[0] == 0 and not (int(sig[1]) & 0x80)) and
 not (int(sig[32]) & 0x80) and
 not (sig[32] == 0 and not (int(sig[33]) & 0x80)))

I'll leave that to the reader to either have faith or delve into the meaning of the byte code themselves, lest I digress...

Before we start the loop we will need to initialize a "nonce" this is some arbitrary data that we will incrment over each loop cycle to ensure that each pass initializes slightly differently in the search for a deterministic and canonical signature.   

    ndata = secp256k1_ffi.new("const int *ndata")
    ndata[0] = 0 # it adds "\0x00", then "\0x00\0x00", etc..

The next step is to get an 8 bit string representation of private key:

    p = bytes(PrivateKey(wif))

Now we begin our loop

    increment our nonce
    create a new privkey seeded with the wif byte string
    create a new signature from the private key
    given the privkey, digest, nonce, and curve: 
        determine if it is recoverable; deterministic
        check if it is canonical; simple form
    if not repeat loop

    if so, generate a recovery parameter and move on

The signature and recovery parameter are 65 bytes; 64+1.  Now that we have our canonical deterministic signature we will hexlify it and its binary recovery parameter (i) and add it to our transaction:


signature = hexlify(
    pack("<B", i) + signature
).decode("ascii")

tx["signatures"].append(signature)

With the signature added to the transaction we will now verify that it is indeed a legit signature:

VERIFY TRANSACTION


Our tx is still just a normal dictionary with an added signature.  The first thing we'll do is classify the tx as a "Signed_Transaction" this will apply the TYPES "magic/dunder" templates to each element of the dictionary to prepare it for processing as struct bytes.

    tx2 = Signed_Transaction(**tx)
  
The second step is to derive the digest; the sha256(message) from the transaction, this will modify tx2 in place.

    tx2.deriveDigest("BTS")

Next will then pass the wif through the PrivateKey class and apply the pubkey method to it:

    pubkeys = [PrivateKey(wif).pubkey]

Lastly, we confirm that the signature on the tx matches the public key it is supposed to:

    tx2.verify(pubkeys, "BTS")

The only remaining step now is to broadcast the transaction to the network.

FINALLY BROADCAST TRANSACTION

Until now, everything we just discussed was handled by manualSIGNING just a few of seconds...

Using the still open websocket we'll make a final query, in the same format as all other queries:

wss_query(["network_broadcast", "broadcast_transaction", [tx]])

Now your signed transaction has been uploaded to the blockchain.

DONE

>>> manualSIGNING has broadcast your order


