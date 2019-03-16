# Installation


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

Cryptocurrency algo trading tools

The repo name "Extinction Event" was born of the notion that DEX tech combined with AI controlled algo trading tech reaching the common user, in unison, would be an extinction level event for both centralized web-based exchanges and "monthly fee" algo trading services.


EV.py 
------------
	daily candle algo trading bot framework for trading on the Bitshares DEX with external CEX data
microDEX.py 
------------
	lightweight user interface to perform manual buy/sell/cancel operations on the Bitshares DEX
metaNODE.py
------------
	statistical curation of market data from multiple public DEX nodes into a streaming text file
bitshares-latency.py
------------
	scans all known nodes in the Bitshares public network for lowest latency
bitshares-database-reference.py
------------
	make api requests to Bitshares database without pybitshares







Make sure you are on an updated linux machine
-----------------------------------------------

	$ sudo apt-get update
	
	if not, visit https://linuxmint-installation-guide.readthedocs.io/en/latest/choose.html


Clone repository
-----------------------------------------------

    In terminal change directory to location you would like to install my repository, then:

	$ git clone https://github.com/litepresence/extinction-event.git
	
	h/t @sschiessl for setup.py & Makefile

Change directory to:
-----------------------------------------------
	
	$ cd extinction-event
	$ dir

	You should see two folders EV and microDEX which contain EV.py and microDEX.py respectively; 
	along with some other dex tools under development.

Install environment
-----------------------------------------------
	
	$ sudo apt-get install -y python3 python3-pip
	
	*NOTE this requirement may already be satisified on your system, do it anyway to check

Install virtual environment and requirements
-----------------------------------------------

	$ pip3 install virtualenv
	$ virtualenv -p python3 env 
	$ source env/bin/activate
	$ pip install -r requirements.txt
	
Test microDEX in virtual environment
-----------------------------------------------

	$ python3 microDEX/microDEX.py
	
Test Extinction Event in virtual environment
-----------------------------------------------


	$ python3 EV/EV.py
	
EV and microDEX are a bot framework and exchange interface respectively.
You cannot use these to create accounts or withdraw funds.


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

    You will need this WIF key in step 12

    You should come away from step 11 with

        account name
        Reference UI account password
        WIF KEY

    
Create a local wallet with uptick
-----------------------------------------------

    go to: https://media.readthedocs.org/pdf/uptick/latest/uptick.pdf
    perform steps:
        4.2.1
        4.2.2
        4.2.3

    Create a new account on uptick using your Bitshares Reference UI name:

	    uptick newaccount [account name from step 11]	

    ** Then create a password and enter new account's password twice
    ** This is your local wallet password WRITE IT DOWN
    ** You will need this to log into Extinction Event or microDEX

        uptick set default_account  [account name from step 11]	

    Add a private key to the wallet:

	    uptick addkey 

        will ask you for password from local wallet step 12
        will then ask you for WIF KEY from step 11


Obtain latest scripts
-----------------------------------------------

    Check back regularly to obtain latest version of Extinction Event and microDEX from official source:

    https://github.com/litepresence/extinction-event/blob/master/microDEX/microDEX.py
    https://github.com/litepresence/extinction-event/blob/master/EV/EV.py

    In Github press raw button and then do select all and copy.  
    Paste it in a text editor and save as microDEX.py and EV.py respectively.
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

    Extinction Event and microDEX are BLEEDING EDGE TECHNOLOGY in active DEVELOPMENT. 
    These are alpha release to public domain without warranty.  
    YOU SHOULD EXPECT UPDATES AND BUG FIXES in the near future.

    READ THE CODE - Check litepresence github regularly for latest version.


Run microDEX
-----------------------------------------------

        source env/bin/activate
	
    from the extinction-event folder will turn on your virtual environment

    in terminal navigate to the virtual environment folder containing microDEX.py

    commands: 'dir', 'cd ..', 'cd folder/folder' are helpful
    
        python3 microDEX.py

    enter account name from step 11
    enter market in format as shown
    enter local wallet password from step 12 
    (you can skip this and demo without password)

Run Extinction Event
-----------------------------------------------

    in terminal navigate to the virtual environment folder containing EV.py

        python3 EV.py

    you will be presented with options of MODE 0 through 5, select one and ENTER

    in def install_tune() you can optimize your algorithm

	ctrl + shift + \

	will exit to terminal from either script ending all processes


Visit litepresence.com for machine optimized algorithms
========================================================

	using elitist bred quantum particle swarms I run hundreds of thousands of backtests to optimize algorithms
	you can optimize algorithms yourself by trial and error, but why not let my AI handle it?

	litepresence.com
	

