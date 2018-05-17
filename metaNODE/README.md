metaNODE = Bitshares_Trustless_Client()
========================

There were two ways to get data from Bitshares blockchain:

1) private node that uses lots of RAM, prefers its own machine, and is technical to tend
2) public node that is difficult to stay connected to and may provide rogue data

I've created a 3rd path; connect to several random nodes in the public network... ask them each for latest market data; then move on to other node nodes.  Finally, perform statistical analysis on the combined feeds and maintain a streaming curated output file; the metaNODE.  



[ANN] metaNODE
===============

	Alex M - clockwork, [19.04.18 11:29]
	Its intriguing definitely

	Marko Paasila, [19.04.18 11:38]
	Much additional value from a small program

	Permie, [25.04.18 02:38]
	Wow nice work man!

	Digital Lucife®, [12.05.18 23:45]
	Almighty

	Stefan Schießl, [14.05.18 23:44]
	Very cool




Bitshares is a protocol that allows many wonderful things, among them: 

Algo trading cryptocurrency by bot script on decentralized exchange

Until now, the public nodes connected to by traders were rated based on trust earned on telegram message boards.  Today that changes; connecting to a public Bitshares node can now be trustless. 

https://github.com/litepresence/extinction-event/tree/master/metaNODE

	litepresence 

	May 2018


The Challenge:
===========

When we deal with a centralized exchange, there is a single server running a single software.  
Although the websites are prone to ddos; the API's we tie our bots to are often rock solid reliable. The closing price is the closing price; it can be counted on. The profit incentive, for the exchange to keep API data reliable and timely, is huge.

When we deal with decentralized exchange, there is a network of usually well meaning, 
but often-enough errant, private parties who offer public blockchain API nodes, with thin profit incentive.  These providers may or may not have updated to the latest bleeding edge version of the core Bitshares software.  Their internet connection, hardware implementation, or configuration might be weak or flawed for whatever reason. 

Further complicating matters, there is group-think tendency amongst users of these API's towards crowding in long-trusted “word of mouth” whitelisted nodes, while ignoring otherwise good working nodes.   This leaves some nodes in the network overwhelmed while others in the network, who consume considerable resources, are relatively unused.

There also exist the potential for a node to purposefully deceive with inaccurate market prices or slow responses to manipulate markets.  This individual could deliver good data for months… then suddenly send all connected bots erroneous price feeds. 

	Then normalization issues:      1.21 = '1.21'  

To botscript this is an error; but something as simple as float is not equal to string can arise between a public node updating versions of the Bitshares core; and the result is your bot crashes. 

	Zero price is another problem.         price = 0

To botscript zero is the price, even though to human eye its obviously an error to be ignored until the next data request.  For whatever reason, these little glitches are part of the nature of dealing with the DEX.  On some nodes, for whatever reason, you get zero price sometimes in last, order book, or history.

When you ask five people the price of a local service and four say about $100 and the fifth says $2, I think we all agree the fifth is crazy.  But what happens when you only trust one friend and he suddenly goes crazy or stops talking to you? 

These are the problems we face when depending upon a single less than reliable public node.  The process of connecting to a public node is prone to brittleness / rogue data.   A node you connected to 5 minutes ago may be gone or wrong now.  Its not easy to tie in to to a random public DEX node - plug play and walk away - as it is to flagship CEX API. For this reason it becomes advisable to sample statistically.  However, maintaining statistically curated data within the framework of botscript becomes messy fast; clutters the script; and is prone to exceptions and runaway processes.

Of course the alternative to using a public node for trading is to run a personal node.  This requires lots of RAM, a specific OS, and preferably a stand alone machine.  Not to mention, some technical know how to maintain and launch the private node.  Time and resources that could be better spent, from the perspective of a bot trader, attempting to deploy algo on other less technically difficult markets. 
The Mission:

Provide only critical, curated, verified data to botscript.  The data should be acquired from a mesh of multiple low latency public nodes.  All incoming data should be statistically validated. 

This must occur while keeping resource dependencies; ram/cpu/web-traffic as minimal as possible.  By spec metaNODE should be able to operate with 99.99 uptime; ie. no memory leaks and a week or more at a time without interruption.  metaNODE should supply 99.99 clean data from the Bishares DEX to bots to prevent flash trading on bad feeds.  metaNODE should strive for 1/10th the RAM resources of a traditional private node by shifting resource focus from RAM intensive to ssd hard drive read/write intensive.   

In doing so it should provide high resolution data, for a single account, in one market.   metaNODE should provide API for 5 feeds: last 100 market history, book, open orders, market balances, top hot tested “whitelist” nodes.   

To streamline requests and eliminate any connectivity issues, metaNODE will not depend on pybitshares and will make direct requests to the public nodes via websocket-client.  



The Methods:
==============

	cache()
The first thing metaNODE does is make several calls to determine key blockchain information used later in our script. Given an account name, what is the account ID?  Given an asset symbol, what is its asset ID? When we have an asset quantity as integer where do we put the decimal place?  In the metaNODE tradition, this data is collected from multiple nodes and then statistically rendered.

	inquire()
To get this cache data we establish a standard method for contacting a public node and switching nodes if the contact fails using the reliable websocket-client package. 

	spawn()
After we have ID numbers and other cached data we can move on to collecting live market data from multiple nodes.  We would like to check many nodes concurrently, so we'll be using the multiprocessing module.  Sometimes these instances become hung for whatever reason, so we'll kill them off and re-spawn them continually in a timely, yet somewhat random manner.  

	thresh()
Each of our spawned processes will begin searching for value errors in all the data we wish to collect, namely: last price, market history, account balances, and the order book.  There are many common categories of errors that can quickly be discerned and the node's data disregarded.  From thresh, if no errors are found the data is sent off to nascent_trend(), and either way it is winnowed into a whitelist (if good data) or blacklist (if rogue). Once connected to a node it will go through several thresh cycles before moving on to the next node, or the process is killed by spawn. 

	winnow()
Maintains two text documents in a dynamic manner concurrently by multiple processes; whitelist.txt and blacklist.txt.  If the node made it through the threshing process unscathed, its address is written to the whitelist ; if not blacklist.    

	nascent_trend()
When a node address is whitelisted, its collected data is then called a maven and is sent on to the nascent trend definition which maintains maven.txt.   Mavens are the 7 most recent datasets from nodes that passed the threshing process.  A maven is a trusted expert, who seeks to pass timely and relevant knowledge. 

	race_write()
Race is a condition where multiple processes attempt to read or write to a file concurrently and cause exception error.  This circumstance creates some issues which must be handled by the programmer.  `race_write() race_read(), race_append(), `and `Bitshares_Trustless_Client()` definitions all handle file access without clashing. 

	bifurcation()
Mavens are trusted experts, but that doesn't mean they're correct.  The statistical mode (most common) of the mavens' datasets is sought.  If there is no mode with all 7 mavens; the mode of 6 or 5 most recent are also considered.   When a mode is found, metaNODE.txt is written with the most common data amongst the mavens.  This subprocess is attempted every second; 99% of the time a mode is found. 

Usage:
===============

In the beginning of your script you'd declare:

	use_metaNODE=True  

`metaNODE.py` is a stand alone script that runs in the terminal and creates `metaNODE.txt` 

`metaNODE.txt` holds the metaNODE dictionary of curated market data.  

On each tick of your bot you would simply call:

	metaNODE = Bitshares_Trustless_Client()

This will perform a “race read” operation on metaNODE.txt, see:  https://pastebin.com/BX7khLDG

In subsequent calls when you gather data like the latest ticker: 

	if use_metaNODE: 
		last = metaNODE['last'] 
		# get data from curated dictionary now in RAM
	else: 
		last = Market.Ticker()['lastest'] 
		# get data with pybitshares websocket call

This means instead of making a websocket call to a potentially rogue node for last price, you are reading a curated text document on your local machine maintained by `metaNODE.py`.
metaNODE uses websocket-client which is already installed on any machine with pybitshares.  metaNODE has no additional module requisites and does not natively depend on pybitshares, which means any bugs in the do-everything pybitshares reference software cannot cause complications to the feeds provided by the lightweight `metaNODE.py`.  

At this time, buy/sell/cancel operations would still be performed by pybitshares.    However, additionally, where your bot currently has a single public node specified to do business with, you would be advised to check with 

	metaNODE['whitelisted'] 
	
prior to making a buy/sell/cancel request with pybitshares. From here forward it would be making that request on a node that has recently been pre-qualified in a trust-less manner, rather than one naively cherry picked; potentially days earlier.

`metaNODE.py` would be running in the same folder as your botscript and would perform all of the wss operations for gathering market data including last price, market history, order book, account balances. The data would be returned in this format:  https://pastebin.com/LE19ex3p 

Additional calls would fit in the framework with a few lines of code.  For example, I intend to add open order id's when core pull request 849/463 is complete later this month. see: 

https://github.com/bitshares/bitshares-core/pull/849

Likewise, the metaNODE framework could be adapted to other custom blockchain feeds.

Common Exceptions:
===============

Connection Related Errors:
----------------
WebSocketBadStatusException('Handshake status 502 Bad Gateway',)
WebSocketTimeoutException('The read operation timed out',)
ConnectionResetError(104, 'Connection reset by peer')
timeout('_ssl.c:584: The handshake operation timed out',)
WebSocketAddressException(gaierror(-2, 'Name or service not known'),)
WebSocketBadStatusException('Handshake status 404 Not Found',)
ConnectionRefusedError(111, 'Connection refused')
timeout('timed out',)

API returns any empty dictionary or an error
----------------
KeyError('result',)

Latency and testnet related errors:
----------------
ValueError('chain_id != MAINNET')
ValueError('ping_elapsed', 1.5726029872894287) # fails if >1
ValueError('handshake_elapsed', 7.850483179092407) # fails if >4
ValueError('blocktime is stale', 7697593.410705566) # fails if >6

Occasionally data gathered cannot be statistically analyzed:
----------------
ValueError('min() arg is an empty sequence',)
StatisticsError('no unique mode; found 2 equally common values',)

When metaNODE attempts to contact a node known to recently give bad data
----------------
ValueError('blacklisted')
When metaNODE attempts to contact a node with more than one process
----------------
ValueError('whitelisted')

Some common errors validated from price feeds:
----------------
ValueError('zero price last')
ValueError('zero price in history')
ValueError('zero price in bids')
ValueError('mismatched orderbook')

In each of these instances, metaNODE shifts to another node, gathers new data, and attempts to analyze again without getting hung.  If your goal was to monitor several public nodes as a provider you might wish to include additional stack trace to the output log. 



Results:
================
metaNODE has now been running 5 straight days without interruption and is using less than ½ GB of RAM. RAM usage remained unchanged, network history fell into a steady pattern, and cpu usage remained tightly clustered around 15% on each core.  This, indicates the framework is very stable and could run for a long time; ie. no RAM leaks, no hung instances, and no burned up cpu cores... even though we're moving tons of pertinent data, from many untrusted websocket sources, writing concurrently; and doing so relentlessly and fast. 

	MetaNODElog.txt 

maintains a list of the various errors encountered in the data.  The three most common errors relate to connectivity time; handshake time, ping time, and blocktime latency.   These calls are made first so that any issues with connectivity cause a switching of nodes, before any additional effort is wasted making calls for market data.  Another common error is zero price values either in last, orderbook, or history.   Also from time to time we see that the highest bid is greater than the lowest ask.  In these instances we also move onto another node.  

It does not seem like well trusted nodes are any more or less likely to have occasional issues.  In reporting some of the issues to the telegram Node Admin channel as they arise, I find the node administrator just needs to restart, make some small change, or is having trouble with their hosting service.  It is far more common that rogue data is due to errant operation than malicious intent. 

Among mean/median/mode,  the mode statistic is the most resistant to outlier data, it is also the correct statistic to apply to “nominal data” that is, we can convert the whole orderbook to a string, and in one query ask which of these seven orderbooks are the same?  It is through the use of the mode statistic that we arrive at what the “truth” of the market condition is.  What are “most” of the nodes that we've validated as mavens saying?    

Of the 90 known nodes, about 60 are giving good data at any given time and about half of those have ping latency less than one second to my location.  The remainder are often on testnets, temporarily down, or for some other reason not configured correctly.  Of the 60 good nodes, when there is a difference of opinion it is often just a matter of rounding; or floating point vs decimal math.  From time to time in history there are some strange outliers; 10% or more from truth, but often the volume related to these is what amounts to “dust” and the data rarely makes it through the bifurcation process. 

The primary advantages of metaNODE vs publicNODE is trustless data curation and uptime.  The primary advantages of metaNODE vs privateNODE is RAM resources consumed and technical overhead to launch and maintain.  


Deploy:
=====================
The only non-python-native module you may need is websocket-client.  If you have installed pybitshares, its setup process automatically installed websocket-client for you. 

Simply launch metaNODE.py from the same folder as your botscript, you'll be asked to input your account name and the symbol of the asset and currency for the market you'd like to curate.

metaNODE does everything else.

    From your botscript, include the Bitshares_Trustless_Client() definition, then each tick do this:

        metaNODE = Bitshares_Trustless_Client()

    metaNODE is now a python dictionary with these curated public node Bitshares DEX feeds:

metaNODE['last']   
          float; latest price
metaNODE['bids']  
          list of (price,amount) tuples; [0][0]=highest bid price
metaNODE['asks'] 
          list of (price,amount) tuples; [0][0]=lowest ask price
metaNODE['history']
          list of (unix,price,amount) tuples; [0][0]=last trade time
metaNODE['currency']
          float; quantity of currency
metaNODE['assets']  
          float; quantity of assets
metaNODE['whitelist']
          list; [0]=most recently whitelisted node
metaNODE['blacklist'] 
          list; [0]=most recently blacklisted node
metaNODE['blocktime'] 
          oldest blockchain time in metaNODE maven data


to watch data feed, in second terminal type:

	>>> tail -f metaNODE.txt'

to watch error report, in third terminal type:

	>>> tail -f metaNODElog.txt'

Controls
===============

Presets as live tested:

    WHITE = 20
    BLACK = 30
    TIMEOUT = 300
    PROCESSES = 20
    MAVENS = 7
    BOOK_DEPTH = 10
    HISTORY_DEPTH = 50
    PAUSE = 2
    BLIP = 0.05

WHITE is the number of whitelisted nodes you'd like to retain for buy/sell/cancel operations
BLACK is the number of nodes you suspect you'd prefer to ignore
TIMEOUT is the rough lifespan of each threshing process launched by spawn
PROCESSES is the maximum number of concurrent websocket connections you'll maintained
MAVENS is the depth of the maven data you'll consider for statistical mode
BOOK DEPTH relate to how many items deep each side of the orderbook is
HISTORY DEPTH relates to number of items in market order history
PAUSE is how much time each threshing process remains silent before making wss requests again
BLIP is a brief moment of pause to prevent clashing or overwhelmed processes
