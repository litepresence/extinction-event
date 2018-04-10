#!/usr/bin/env python

from setuptools import setup, find_packages
import sys

__VERSION__ = '0.13'

assert sys.version_info[0] == 3, "We require Python > 3"

setup(
    name='extinction-event',
    version=__VERSION__,
    description=(
        'Extinction event.'
        'Cryptocurrency algo trading tools.'
    ),
    long_description=open('README.md').read(),
    download_url='https://github.com/litepresence/extinction-event/tarball/' + __VERSION__,
    author='litepresence',
    author_email='info@litepresence.com',
    url='http://www.litepresence.com',
    keywords=['bitshares', 'microDEX', 'extinction event'],
    packages=find_packages(),
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
    ],
    entry_points={
        'console_scripts': [
            'microDEX = microDEX.microDEX:main'
        ],
    },
    install_requires=open('requirements.txt').read().split(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    include_package_data=True,
)
