# Extinction Event
Cryptocurrency algo trading tools

The repo name "Extinction Event" was born of the notion that DEX tech combined with AI controlled algo trading tech reaching the common user, in unison, would be an extinction level event for centralized web based exchanges, intrusive state AML/KYC policies, and orchestrated pump and dump schemes; all of which I consider anathema to individual financial liberty and decentralized free market economy. 

# Installation instruction

Clone repository

    $ git clone git@github.com:litepresence/extinction-event.git
    $ cd extinction-event

Install environment
	
	$ apt-get install -y python3 python3-pip

Install virtual environment and setup 

	$ pip3 install virtualenv
	$ virtualenv -p python3 env 
	$ source env/bin/activate
	$ pip install -r requirements.txt
	
Run microDEX in virtual environment

    $ python3 microDEX/microDEX.py
