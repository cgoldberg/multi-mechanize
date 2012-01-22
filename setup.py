#!/usr/bin/env python
#
#  Copyright (c) 2010-2012 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3 - distributed under the terms of the GNU Lesser General Public License version 3
#  
#  This file is part of Multi-Mechanize:
#       Multi-Process, Multi-Threaded, Web Load Generator, with python-mechanize agents
#
#  requires Python 2.6+


"""
setup.py for multimechanize
"""

import os

from setuptools import setup

from multimechanize import __version__


this_dir = os.path.abspath(os.path.dirname(__file__))


NAME = 'multimechanize'
VERSION = __version__
PACKAGES = ['multimechanize',]
SCRIPTS = ['multimech-run',]
DESCRIPTION = 'Multi-Mechanize - Performance Test Framework'
URL = 'http://testutils.org/multimechanize'
LICENSE = 'GNU LGPLv3'
LONG_DESCRIPTION = '\n%s' % open(os.path.join(this_dir, 'README.rst')).read()
REQUIREMENTS = filter(None, open(os.path.join(this_dir, 'requirements.txt')).read().splitlines())
AUTHOR = 'Corey Goldberg'
AUTHOR_EMAIL = 'corey@goldb.org'
KEYWORDS = ('performance scalability load test testing benchmark').split(' ')
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Software Development :: Testing',
    'Topic :: Software Development :: Testing :: Traffic Generation',
    'Topic :: System :: Benchmark',
]

params = dict(
    name=NAME,
    version=VERSION,
    packages=PACKAGES,
    scripts=SCRIPTS,
    install_requires = REQUIREMENTS,
    
    # metadata for upload to PyPI
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    keywords=KEYWORDS,
    url=URL,
    classifiers=CLASSIFIERS,
)

setup(**params)
