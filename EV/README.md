Extinction Event
====================
I have developed a suite of tools for the bitshares distributed exchange (DEX).  
They are all open source and free to use, license:

`WTFPL v0 ca. 1765`

`if any([taxes,licenses]):`
`    return (tar, feathers)`

**see 'Installation' in parent folder README.md to begin trading**


metaNODE.py
----------------------------

metaNODE is a client side mesh network tool I developed for interacting with Bitshares Public DEX Nodes in a trustless manner. The tool scans the bitshares network for latest orderbook and account data and then statistically verifies that data vs other nodes in the public network. metaNODE then writes metaNODE.txt (in a race condition proof manner) which contains a dictionary of orderbook and account data. Other apps can then read like a high speed personal API of verified DEX data.  I have also provided 5000+ word whitepaper describing the metaNODE's workings. 

manualSIGNING.py
----------------------------

manualSIGNING is a fork of pybitshares.  It is purpose built for efficient limit order processing by botscript through BitShares Public RPC Nodes.   manualSINGING validates limit order operations and performs ECDSA upon transactions. The primary goal was presenting an easy to use API with absolute minimal dependencies, minimal lines of code, all within a single python script.  At about 1000 lines of code, it weighs in at 50 kb; about 1/50th of the 2500+ kb of pybitshares proper.  While few individuals fully comprehend the workings of pybitshares, it is my hope that manualSIGNING ellucidates to the trading community the process of BitShares transaction signing. To this end, the script is heavily commented and also includes 5000+ word whitepaper. 

extinctionEVENT.py
----------------------------

extinctionEVENT (EV) is a simple moving average trading tool which splits the market into Bull/Bear state and then trades on different thresholds depending on state. Is capable of producing live moving averages from 5m scale to daily candle scale; all at 5m resolution. EV also includes a backtesting engine for optimizing your algorithm. extinctionEVENT.py gets DEX data from metaNODE.txt. The utility also imports centralized exchange data from cryptocompare.com nomics.com and alphavantage.com for backtesting.

microDEX.py
----------------------------

microDEX is user interface much like you'd find when trading at a centralized exchange. It has order books, recent market trades, and authenticated buy/sell/cancel. Like EV gets its statistically curated DEX data from the metaNODE.

latencyTEST.py
----------------------------

latencyTEST first reaches out to github and searches for lists of bitshares nodes on user accounts known to keep up on such things. It then takes the lists from each user and makes one huge list; the universe. The nodes in the universe may or may not be active though, so then it attempts to contact each node to verify that it 1) responds quickly 2) is on the right chain 3) its clock is not stale. From the nodes in the known universe it generates a list of available public api websockets and writes a file nodes.txt with that list. It also outputs a nodesmap.png image file. nodes.txt is used later by metaNODE.py to to gather DEX data from known active nodes in the network for data curation.

proxyDEX.py
----------------------------

Getting candle data is notoriously difficult to do from the DEX. This utility cross checks data from multiple nodes. It interpolates the buckets retrieved into correct HLOCV candles. proxyDEX makes external calls wrapped in multiprocess timeouts.  Finally, it allows for up to 5 calls of 200 buckets to be concancated into a single array of 1000 candles. 

proxyCEX.py - proxyMIX.py - proxyALPHA.py
----------------------------

These tools gather daily candle data from cryptocompare.com; nomics.com; and alphavantage.com. This gives you every conceivable combination of altcoin:altcoin, bitcoin:altcoin, forex:altcoin, exchange specific crypto markets, us stock markets, and forex:forex. All data is in the same format as proxyDEX and like proxyDEX external requests are multiprocess wrapped.  This data is then available within extinctionEVENT for backtesting.   The goal being to refine trading strategies for new dex pairs that mimic long established financial markets through backtesting on external to dex historical data. 

proxyTEST.py
----------------------------

This tool allows you to visualize datasets from all available sources without backtesting. It also plots moving averages to demonstrate data structure, normalization, and interpolation.  Likewise this could be used as a plotting tool along side microDEX.  Given the nomalized data and plotting framwork, a developer can quickly plot any financial technical indication (SAR, RSI, EMA, etc.) to numpy array provided; in the same way I have applied the simple moving average defnition.  

accountBALANCES.py
----------------------------

Every hour your metaNODE will take a snapshot of your account balances for the market it is tending. accountBALANCES will then retrieve that data and plot for you ROI in `asset terms`, `currency terms`, and `sqrt(assetROI*currencyROI)` terms.
