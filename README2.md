INSTALLATION
==============

**GATHER HARDWARE**

This stack is heavy on read/write, ram, and cpu. 
You could print every matrix it handles if you wish to understand why.

- SSD SOLID STATE DRIVE of any size; 120GB drives are $20; plenty good.
- *DO NOT* install exinction-event on a spinning platter HDD
- 4 GB RAM for full stack, 8 recommended
- CPU speed amounts to backtest speed, I run AMD 7950
- Gold/Platinum power as this is your 24/7 crypto-on-the-line botscript machine
- I run FM2+ milspec/ultra durable boards from ASUS or GIGABYTE

**INSTALL LINUX OS**

Any debian or ubuntu should do.  The stack is NOT Mac or Windows compliant. 

I am running Cinnamon Mint 19.04, learn more:

    https://linuxmint.com/

**UPDATE APT-GET**

    $ sudo apt-get update

**INSTALL PYTHON 3.7+**

I used this writeup:

    https://tecadmin.net/install-python-3-7-on-ubuntu-linuxmint/

**INSTALL PIP 3**

    $ sudo apt-get install -y python3-pip

**INSTALL GIT**

    $ sudo apt install git

**GIT CLONE EXTINCTION-EVENT REPO**

Navigate to the folder you want to run your bots from:

    $ cd <folder name>
    $ git clone https://github.com/litepresence/extinction-event.git

**INSTALL VIRTUAL ENVIRONMENT**

Enter the extinction-event folder

    $ cd extinction-event
    $ sudo pip3 install virtualenv
    $ virtualenv -p python3 env 

**ENTER VIRTUAL ENVIRONMENT**

*NOTE* you will need to activate from extinction-event folder every time you start a new terminal tab when running my python scripts

    $ source env/bin/activate

**APT-GET INSTALL REQUIREMENTS**

    $ sudo apt-get install python3-tk
    $ sudo apt-get install python3-dev
    $ sudo apt-get install libsecp256k1-dev

**INSTALL REQUIREMENTS**

    $ pip install -r requirements.txt

**LATENCY TEST**

Open a new terminal tab. Run a latency test, it will take a few minutes.  This will write nodes.txt which will be used by metaNODE.py.  Navigate to:

    $ .../extinction-event
    $ source env/bin/activate
    $ cd EV
    $ python3 latencyTEST.py

When you get more serious about running botscript full time you can change `USER CONTROLS` within latencyTEST.py for recurring loop, custom whitelists, or to scan github for newly posted nodes. You can even plot the node locations and upload your results to the web.  After latency test has written node.txt, open node.txt in a text editor to confirm you have a list of latency sorted nodes for your region.

**METANODE**

Next you will begin your first metaNODE session.  New terminal tab, cd navigate to:

    $ .../extinction-event
    $ source env/bin/activate
    $ cd EV
    $ python3 metaNODE.py
	
Enter your account name and dex market of choice, you can press enter to skip and a default account and market will be chosen:

account: abc123
currency: open.btc
ssest: bts

Capitalization does not matter for the asset and currency.  metaNODE CANNOT access your funds.

**MICRODEX**

This will ensure you have all dependencies to sign transactions installed.  In a new terminal tab, with metaNODE still running in first tab, navigate to:

    $ .../extinction-event
    $ source env/bin/activate
    $ cd EV
    $ python3 microDEX.py

You will be presented with the OPTION to enter your WIF.   Alternatively you can press ENTER to skip.  You do not need to give your WIF at this time to ensure complete setup.

*NOTE* You SHOULD familiarize yourself and friends with the source code before entering your WIF.  Your WIF is what signs transactions of any type.  DO NOT authenitcate unless you understand and fully trust the scripts I have given to you.

The best way to get your WIF is by opening the reference Bitshares UI:

settings >> accounts >> show keys
click on "KEY" icon
click "show private key in WIF format"

to obtain a copy of the reference UI, visit:

http://bitshares.org/download/

**APIKEYS**

The latest version of the backtest engine allows you to backtest against bitshares dex data as well as several outside sources.  Each of these sources was chosen because of the vast data available and ease of obtaining FREE api keys. 

Go get api keys from: 

    www.cryptocompare.com
    www.alphavantage.com
    www.nomics.com

open apiKEYS.py and install your keys where they go in the dictionary, save file and close

use DOUBLE QUOTES and COMMA after each entry except the last; no comma
DO NOT include any commments or other text in this document

These keys are public api keys and CANNOT effect your funds if they are stolen, however they do limit your daily api calls to prevent ddos.  See each website for details.

If you skip this step, you will only be able to backtest with `CANDLE_SOURCE = 'DEX'` in `tune_install()`

**PROXYTEST**

proxyTEST.py will ensure that you have installed your backtest api keys correctly.

open proxyTEST and there is user input `API` near the top of the script.  Run a test on `API` numbers 1 through 6. 

**EXTINCTION EVENT**

In a new terminal tab, with metaNODE still running in first tab, navigate to:

    $ .../extinction-event
    $ source env/bin/activate
    $ cd EV
    $ python3 extinctionEVENT.py

You will be presented with some options:

    **BACKTEST** allows you to backtest and tune strategies using the `tune_install()` definition within extictionEVENT.py
    **PAPER** allows you to run a live session without giving the bot your keys, no live trades will be made
    **LIVE** is live trading with funds per your `control_panel()` and `tune_install()` settings
    **SALES** allows you to sell extinctionEVENT strategy tunes by posting images of trade points without showing your moving average thresholds
    **ORDER_TEST** is a live trading session WITH FUNDS but places orders far from the margins to test authentication
    **OPTIMIZE** autotunes backtests, this is NOT currently open source; I'm currently considering a worker for this and more.

**ACCOUNT HISTORY**

Whenever your metaNODE is running your account history is being logged to file.  accountHISTORY.py can read this file and plot your changes in account balances over time. 


