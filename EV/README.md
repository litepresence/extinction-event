Extinction Event
====================
I have developed a suite of tools for the bitshares distributed exchange (DEX).  
They are all open source and free to use, license:

`WTFPL v0 ca. 1765`

`if any([taxes,licenses]):`
`    return (tar, feathers)`

see 'Installation' in parent folder to begin trading
-----------------------------------

**metaNODE.py**
metaNODE is a client side mesh network tool I developed for interacting with Bitshares Public DEX Nodes in a trustless manner. The tool scans the bitshares network for latest orderbook and account data and then statistically verifies that data vs other nodes in the public network. metaNODE then writes metaNODE.txt (in a race condition proof manner) which contains a dictionary of orderbook and account data. Other apps can then read like a high speed personal API of verified DEX data. 

You can read the metaNODE whitepaper here: https://github.com/litepresence/extinction-event/tree/master/metaNODE

**extinctionEVENT.py**
extinctionEVENT (EV) is a simple moving average trading tool which splits the market into Bull/Bear state and then trades on different thresholds depending on state. Is capable of producing live moving averages from 5m scale to daily candle scale; all at 5m resolution. EV also includes a backtesting engine for optimizing your algorithm. extinctionEVENT.py gets DEX data from metaNODE.txt. The utilities also import centralized exchange data from cryptocompare.com for visualization, backtesting, and decision making. 

**microDEX.py**
microDEX is user interface much like you'd find when trading at a centralized exchange. It has a chart, order books, recent market trades, and authenticated buy/sell/cancel. Like EV gets its DEX data from metaNODE and CEX data from cryptocompare.

**latencyTEST.py**
latencyTEST first reaches out to github and searches for lists of bitshares nodes on user accounts known to keep up on such things. It then takes the lists from each user and makes one huge list; the universe. The nodes in the universe may or may not be active though, so then it attempts to contact each node to verify that it 1) responds 2) is running the correct software 3) its clock is not stale. From the nodes in the known universe it generates a list of available public api websockets and writes a file nodes.txt with that list. It also outputs a nodesmap.png image file. nodes.txt is used later by metaNODE.py to to gather DEX data. 

**proxyDEX.py**
Getting candle data is notoriously difficult to do from the DEX.  This utility cross checks data from multiple nodes.  It interpolates the buckets retrieved into correct HLOCV candles.  It makes external calls wrapped in multiprocess timeouts.  

**proxyCEX.py - proxyMIX.py - proxyALPHA.py**
These tools gather backtest data from cryptocompare.com nomics.com and alphavantage.com.  This gives you every conceivable combination of altcoin:altcoin, bitcoin:altcoin, forex:altcoin, exchange specific crypto markets, us stock markets, and forex:forex.  All data is in the same format as proxyDEX and like proxyDEX external requests are multiprocess wrapped. 

**proxyTEST.py**
This tool allows you to visualize datasets from all available sources without backtesting.  It also plots moving averages to demonstrate correct normalization and interpolation. 

**accountBALANCES.py**
Every hour your metaNODE will take a snapshot of your account balances for the market it is tending.  accountBALANCES will then retrieve that data and plot for you ROI in `asset terms`, `currency terms`, and `sqrt(assetROI*currencyROI)` terms. 

