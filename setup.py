#!/usr/bin/env python

from setuptools import setup, find_packages
from sys import platform, version_info
from os import system, sysconf, popen
from time import time, sleep

def welcome():

    print('\033c')
    print('')
    print('')
    print(it('blue', '      litepresence presents'))
    print('')
    print(it('yellow', '      BITSHARES EXTINCTION EVENT'), it('red','   CEX MUST DIE'))
    print('')

def it(style, text):
    # colored text in terminal
    emphasis = {
        "red": 91,
        "green": 92,
        "yellow": 93,
        "blue": 94,
        "purple": 95,
        "cyan": 96,
    }
    return ("\033[%sm" % emphasis[style]) + str(text) + "\033[0m"


def linux_test():

    assert "linux" in platform.lower(), it('red', "not linux OS, format drive and try again")  
    print(it('green','Linux Found'))

def python_test():

    version = int(version_info[0])+int(version_info[1])/10.0
    version_id = str(version_info[0])+'.'+str(version_info[1])+'.'+str(version_info[2])
    print('Version', version_id)
    assert version >= 3.6, it('red', 'Python Version must be 3.6 or greater')
    print(it('green', 'Python 3.6+ Found'))

def ram_test():

    mem_bytes = sysconf('SC_PAGE_SIZE') * sysconf('SC_PHYS_PAGES')
    mem_gib = mem_bytes/(1024.**3)
    print('%.1f GB RAM' % mem_gib)
    assert mem_gib > 3, it('red', 'you will need at least 3GB RAM to run this suite')
    print(it('green', 'minimum adequate RAM found'))

def cat_scsi_test():

    print('confirming you have an SSD on this machine with "cat /proc/scsi/scsi"')
    system("cat /proc/scsi/scsi")
    scsi = str(popen("cat /proc/scsi/scsi").read()).lower()
    if 'ssd' not in scsi:
        print(it('red','***WARN*** no SSD no drive LABEL on this machine'))
        null = input('press ENTER to continue or ctrl+shft+\ to EXIT') 
    else:
        print(it('green', 'SSD drive LABEL found on this machine'))

def drive_speed_test():

    doc = 'ssd_test.txt'
    start = time()
    for i in range(10000):
        with open(doc, 'w+') as f:
            f.write('ssd test')
            f.close()
        with open(doc, 'r') as f:
            ret = f.read()
            f.close()
    stop = time()
    elapsed = stop - start
    ios = int(10000/elapsed)
    hd = 'HDD'
    if ios > 6000: # ssd>8000; hdd <4000
        hd = 'SSD'

    print('detecting hard drive type by read/write speed')
    print('ios', ios, 'hard drive type', hd)
    if hd == 'HDD':
        print(it('red','***WARN*** it does not appear you are INSTALLING on an SSD'))
        null = input('press ENTER to continue or ctrl+shft+\ to EXIT') 
    print(it('green','it appears you are installing on an SSD drive'))

def accounts_held():

    print('please NOTE!')
    print('')
    print('I AM CURRENTLY:')
    print('')
    print('owner of litepresence.com')
    print('@litepresence telegram - quick to respond')
    print('finitestate@tutamail.com - slow to respond')
    print('litepresence stackoverflow')
    print('litepresence github')
    print('litepresence tradingview')
    print('@oraclepresence twitter')
    print('presence ronpaulforums.com')
    print('')
    print('I WAS FORMERLY:')
    print('')
    print('rpfpresence@gmail.com')
    print('litepresence freenode')
    print('litepresence btce trollbox')
    print('litepresence poloniex trollbox')
    print('litepresence cryptotrader')
    print('litepresence tradewave')
    print('litepresence quantopian')
    print('litepresence metatrader')
    print('')
    print('I AM NOT IN CONTROL OF THESE HACKED ACCTS:')
    print('')
    print('litepresence twitter, local bitcoins, or bitcointalk')
    print('')
    null = input('press ENTER to continue')    

def system_compatibility():

    print('\033c')
    print('')
    print('')
    print(it('blue', '      litepresence presents'))
    print('')
    print(it('yellow', '      BITSHARES EXTINCTION EVENT'), it('red','   CEX MUST DIE'))
    print('')
    print('')
    print('ENSURING LINUX OS')
    sleep(0.1)
    linux_test()
    print('ENSURING PYTHON 3')
    sleep(0.1)
    python_test()
    print('CHECKING YOUR SYSTEM RAM')
    sleep(0.1)
    ram_test()
    print('SOLID STATE DRIVE IS REQUIRED')
    print('RUNNING SOME TESTS WHICH MAY THROW FALSE NEGATIVE')
    print('SKIP IF YOU ARE SURE YOU ARE INSTALLING ON AN SSD')
    sleep(0.1)
    cat_scsi_test()
    drive_speed_test()
    print('SSD TEST COMPLETE')
    print('')

welcome()
system_compatibility()

__VERSION__ = '0.13'

setup(
    name='extinction-event',
    version=__VERSION__,
    description=(
        'Extinction Event'
        'Bitshares Distributed Exchange Algo Trading Tools'
    ),
    long_description=open('README.md').read(),
    download_url='https://github.com/litepresence/extinction-event/tarball/' + __VERSION__,
    author='litepresence',
    author_email='finitestate@tutamail.com',
    url='http://www.litepresence.com',
    keywords=['bts', 'bitshares',
              'btc', 'bitcoin',
              'crypto', 'altcoin', 'cryptocurrency',
              'distributed', 'exchange', 'dex', 
              'microdex', 'micro dex','micro',
              'metanode', 'meta node','meta',
              'latencytest', 'latency test', 'latency', 
              'back test', 'backtest', 'test', 
              'trading', 'bot', 'botscript', 'bot script', 
              'extinction event', 'extinction-event', 'extinctionevent'],
    packages=find_packages(),
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    install_requires=open('requirements.txt').read().split(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    include_package_data=True,
)

accounts_held()


