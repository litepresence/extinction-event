# Extinction Event
Cryptocurrency algo trading tools

The repo name "Extinction Event" was born of the notion that DEX tech combined with AI controlled algo trading tech reaching the common user, in unison, would be an extinction level event for centralized web based exchanges, intrusive state AML/KYC policies, and orchestrated pump and dump schemes; all of which I consider anathema to individual financial liberty and decentralized free market economy. 

# Installation instructions

In terminal change directory to location you would like to install my repository, then:

Clone repository

	$ git clone https://github.com/litepresence/extinction-event.git

Change directory to clone of my repository:
	
	$ cd extinction-event

Install environment
	
	$ sudo apt-get install -y python3 python3-pip
	
	*NOTE this requirement may already be satisified on your system

Install virtual environment and requirements

	$ pip3 install virtualenv
	$ virtualenv -p python3 env 
	$ source env/bin/activate
	$ pip install -r requirements.txt
	
Run microDEX in virtual environment

	$ python3 microDEX/microDEX.py
	
Run Extinction Event in virtual environment

	$ python3 EV/EV.py

