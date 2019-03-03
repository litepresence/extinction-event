Installation
================


NOTE: this toolset is currently in alpha state of development; more new toys coming soon!


(BTS) litpresence1 
----------------------

```
def WTFPL_v0_March_1765():
    if any([stamps, licenses, taxation, regulation, fiat, etat]):
        try:
            print('no thank you')
        except:    
            return [tar, feathers]
```

CEX MUST DIE
=============

The repo name "Extinction Event" was born of the notion that DEX tech combined with AI controlled algo trading tech reaching the common user, in unison, would be an extinction level event for both centralized web-based exchanges and "monthly fee" algo trading services.

Cryptocurrency algo trading tools
===============================

latencyTEST.py
------------
	scans all known nodes in the Bitshares public network for lowest latency
metaNODE.py
------------
	statistical curation of market data from multiple public DEX nodes into a streaming text file
extinctionEVENT.py 
------------
	algo trading bot framework for trading on the Bitshares DEX with external CEX data; requires metaNODE
microDEX.py 
------------
	lightweight user interface to perform manual buy/sell/cancel operations on the Bitshares DEX
proxyDEX.py
-----------
        create true HLOCV candles from bishares public API market_history buckets
manualSIGNING.py
-------------
        pybitshares fork, purpose built for efficiently signing limit orders


Create an account on Bishares Reference UI
-----------------------------------------------

	To create an account:
	
    https://bitshares.org/download/
    install bitshares by double clicking on *.deb file

    create a new account on the bitshares exchange
    sign into bitshares graphical interface
    settings >>> accounts >>> show keys
    click on KEY ICON
    click SHOW private key in WIF FORMAT

    You will need this WIF key when authenticating with microDEX and extinctionEVENT
    
    DO NOT SHARE THIS KEY WITH ANYONE
    DO NOT AUTHENTICATE WITHOUT READING AND UNDERSTANDING MY SCRIPTS


Make sure you are on an updated linux machine
-----------------------------------------------

	$ sudo apt-get update
	
	if not, visit https://linuxmint-installation-guide.readthedocs.io/en/latest/choose.html


Clone repository
-----------------------------------------------

In terminal change directory to location you would like to install my repository, then:

	$ git clone https://github.com/litepresence/extinction-event.git
	
Thanks to: @sschiessl for setup.py & Makefile

Change directory to:
-----------------------------------------------
	
	$ cd extinction-event
	$ dir

You should see a folder `EV` along with some other dex tools under development.

Install environment
-----------------------------------------------
	
	$ sudo apt-get install -y python3 python3-pip
	
*NOTE this requirement may already be satisified on your system, do it anyway to check

Install virtual environment and requirements
-----------------------------------------------

while in the extinction-event folder:

	$ sudo pip3 install virtualenv
	$ virtualenv -p python3 env 
	$ source env/bin/activate
	$ pip install -r requirements.txt
	
switch to EV folder
-----------------------------------------------

	$ cd EV	
	$ dir
	
you should see:

	latencyTEST.py
	metaNODE.py
	manualSIGNING.py
	extinctionEVENT.py
	microDEX.py
	
along with some other tools under developement
	
Test latencyTEST in virtual environment
-----------------------------------------------

you must do this prior to running any of my other apps

	$ python3 latencyTEST.py	
	
this will create your initial nodes.txt which will be used by metaNODE.py 
	
Test metaNODE in virtual environment
-----------------------------------------------

when latencyTEST is done, do Ctrl+Shft+\ to kill the process, then:

	$ python3 metaNODE.py	
	
this will begin writing metaNODE.txt which is streaming orderbook data
	
Test microDEX in virtual environment
-----------------------------------------------

in a new terminal tab, with metaNODE still running in first tab: 
navigate to extinction-event, 
activate your virtual environment 
then navigate to EV folder
	
	$ cd extinction-event
	$ source env/bin/activate
	$ cd EV
	
you will need to perform the 3 step "activate virtual environment" routine above every time you begin a new instance of my scripts in a new terminal

now you may begin your first microDEX.py instance

	$ python3 microDEX.py
	
Test Extinction Event in virtual environment
-----------------------------------------------


in a new terminal tab, with metaNODE still running in first tab: 
navigate to extinction-event 
activate your virtual environment 
then navigate to EV folder
	
	$ cd extinction-event
	$ source env/bin/activate
	$ cd EV

	$ python3 extinctionEVENT.py
	
you can now run your first backtest on the extinctionEVENT platform   


Obtain latest scripts
-----------------------------------------------

    Check back regularly to obtain latest version of Extinction Event and microDEX from official source:

    https://github.com/litepresence/extinction-event/blob/master/microDEX/microDEX.py
    https://github.com/litepresence/extinction-event/blob/master/EV/EV.py

    In Github press raw button and then do select all and copy.  
    Paste it in a text editor and save as microDEX.py and extinctionEVENT.py respectively.
    Save it into a folder you want to use for trading.  
    You will be changing into that directory to run the script.

    These are stand alone python scripts.  You do not need to clone my repos, though you are welcome to do so. 
    Extinction Event is an algo trading bot framework including backtest and live session engine.
    microDEX is a live orderbook, chart, and UI for manual trading
    You can learn more about both by visiting bitsharestalk General Forum.
    I also have Elitist Bred Quantum Particle Swarm tuned algorithms for sale in the forum.

    Visit litepresence.com to learn more.

    Read scripts before you put passwords in; take personal responsibility!
    If you don't and I am scammer I take your funds quick and easy.  

    extinctionEVENT and microDEX are BLEEDING EDGE TECHNOLOGY in active DEVELOPMENT. 
    These are alpha release to public domain without warranty.  
    YOU SHOULD EXPECT UPDATES AND BUG FIXES in the near future.

    READ THE CODE - Check litepresence github regularly for latest version.

    find me:
    
	    telegram @litepresence  <<< most responsive
	    email finitestate@tutamail.com
	    twitter @oraclepresence
	    ronpaulforums.com @presence
	    bitsharestalk @litepresence
	    (BTS) litepresence1
	    litepresence.com
    
    NOTE: "litepresence" at bitcointalk is a hacked account I no longer control

Visit litepresence.com for machine optimized algorithms
========================================================

	using elitist bred quantum particle swarms I run hundreds of thousands of backtests to optimize algorithms
	you can optimize algorithms yourself by trial and error, but why not let my AI handle it?

	litepresence.com
	

