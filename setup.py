#!/usr/bin/env python
"""
pip3 installations
tulip and talib installations
"""
import os
from subprocess import call
from setuptools import setup, find_packages


class ChangeDirectory:
    """
    Context manager for changing the current working directory
    h/t @ brianmhunt
    """

    def __init__(self, new_path):
        self.new_path = os.path.expanduser(new_path)
        self.saved_path = os.getcwd()

    def __enter__(self):
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)


def it(style, text):
    """
    Colored text in terminal
    """
    emphasis = {
        "red": 91,
        "green": 92,
        "yellow": 93,
        "blue": 94,
        "purple": 95,
        "cyan": 96,
    }
    return ("\033[%sm" % emphasis[style]) + str(text) + "\033[0m"



def talib_tulip():
    """
    Intall Tulip and Talib quantiative indicators packages
    """
    # talib and tulip tarballs are included in extinction-event
    # if you prefer original copies use:
    # https://github.com/TulipCharts/
    #       tulipindicators/archive/v0.8.0.tar.gz
    # https://downloads.sourceforge.net/project/ta-lib/
    #       ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz
    print("\n\n")
    print("Installing TALIB and TULIP")
    print("\n\n")
    # un tarball, create two folders
    call(["tar", "-xzf", "ta-lib-0.4.0-src.tar.gz"])
    call(["tar", "-xzf", "tulipindicators-0.8.0.tar.gz"])
    # enter the folders individually, make, and ChangeDirectory ..
    folder = str(os.path.dirname(os.path.abspath(__file__))) + "/"
    with ChangeDirectory(folder + "ta-lib"):
        call(["./configure", "--prefix=/usr"])
        call(["make"])
        call(["sudo", "make", "install"])
    with ChangeDirectory(folder + "tulipindicators-0.8.0"):
        call("make")
    print("\n\n")
    print("TALIB and TULIP indicator package installs complete\n\n")


def upgrade_pylint():
    """
    Upgrade pylint to pylint3
    """
    call(["sudo", "-H", "pip3", "install", "pylint", "--upgrade"])


print("\n\nInstalling requirements.txt...\n\n")
__VERSION__ = "0.13"
talib_tulip()
setup(
    name="extinction-event",
    version=__VERSION__,
    description=(
        "Extinction Event" "Bitshares Distributed Exchange Algo Trading Tools"
    ),
    long_description=open("README.md").read(),
    download_url="https://github.com/litepresence/extinction-event/tarball/"
    + __VERSION__,
    author="litepresence",
    author_email="finitestate@tutamail.com",
    url="http://www.litepresence.com",
    keywords=[
        "bts",
        "bitshares",
        "bitsharesquant",
        "quant",
        "quantitative",
        "palmpay",
        "beet",
        "dexbot",
        "crypto-bridge",
        "rudex",
        "easydex",
        "cryptobridge",
        "btc",
        "bitcoin",
        "openledger",
        "open-ledger",
        "crypto",
        "altcoin",
        "cryptocurrency",
        "smart",
        "contract",
        "distributed",
        "exchange",
        "dex",
        "honey badger",
        "microdex",
        "micro dex",
        "micro",
        "honeybadger",
        "metanode",
        "meta node",
        "meta",
        "litepresence",
        "latencytest",
        "latency test",
        "latency",
        "back test",
        "backtest",
        "backtesting",
        "algo",
        "algorithmic",
        "test",
        "quant",
        "trading",
        "bot",
        "botscript",
        "bot script",
        "extinction event",
        "extinction-event",
        "extinctionevent",
    ],
    packages=find_packages(),
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    install_requires=open("requirements.txt").read().split(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    include_package_data=True,
)
upgrade_pylint()
print(it("green", "bitsharesQUANT installation complete\n\n"))
print("For your future convenience, ENTER this alias command:\n")
print(it("yellow", "    alias pylint=pylint3\n"))
