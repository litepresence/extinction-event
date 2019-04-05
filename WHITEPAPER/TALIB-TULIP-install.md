
TALIB & TULIP
-------------------

**TECHNICAL ANALYSIS LIBRARY INSTALLATION**


**WITH VIRTUAL ENVIRONMENT ALREADY CREATED**

OPEN A NEW TERMINAL, CHANGE DIRECTORY TO:

    (...)/extinction-event

**ENTER VIRUAL ENVIRONMENT**

    source env/bin/activate

**CYTHON (prerequisite)**

    pip install Cython numpy 

**TULIP 0.8.0**

    wget https://github.com/TulipCharts/tulipindicators/archive/v0.8.0.tar.gz
    tar -xzf tulipindicators-0.8.0.tar.gz
    cd tulipindicators-0.8.0
    make 
    pip install --upgrade --force-reinstall tulipy

**TALIB 0.4.0**

    wget https://downloads.sourceforge.net/project/ta-lib/ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz
    tar -xzf ta-lib-0.4.0-src.tar.gz
    cd ta-lib/
    ./configure --prefix=/usr
    make
    sudo make install
    pip install TA-Lib 
    pip install --upgrade --force-reinstall TA-Lib
    
**OPEN proxyTEST.py WITH TEXT EDITOR**
ADD THESE LINES:

    import talib as ta
    import tulipy as tu

    taEMA = ta.EMA(data['close'], 30)[-500:]
    taEMAx = data['unix'][-500:]
    tuSAR = tu.psar(data['high'], data['low'], 0.01, 0.1)[-500:]
    tuSARx = data['unix'][-500:]    

    plt.plot(taEMAx, taEMA, color="red")
    plt.plot(tuSARx, tuSAR, color="darkorange")     
    
**OPEN NEW TERMINAL, CHANGE DIRECTORY**

RUN proxyTEST.py

    (...)/extinction-event
    source env/bin/activate
    cd EV
    python3 proxyTEST.py

**BITSHARE DEX FINANCIAL TECHNICAL ANALYSIS**

FULL INDICATOR LISTS FOUND HERE:
        
    https://tulipindicators.org/list
    https://ta-lib.org/function.html
