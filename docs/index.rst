
================================================
    Multi-Mechanize | Performance Test Framework
================================================

|

.. image:: assets/multimech-450.png

|

.. image:: assets/graphs.png

----

:Web: http://multimechanize.com
:PyPI: http://pypi.python.org/pypi/multi-mechanize
:Dev: http://github.com/cgoldberg/multi-mechanize
:License: GNU LGPLv3
:Author: Copyright (c) 2010-2012 Corey Goldberg

----

**************************************
    Performance & Load Tests in Python
**************************************

Multi-Mechanize is an open source framework for performance and load testing. 
It runs concurrent Python scripts to generate load (synthetic transactions) 
against a remote site or service.

Multi-Mechanize is most commonly used for web performance and scalability 
testing, but can be used to generate workload against any remote API accessible 
from Python.

Test output reports are saved as HTML or JUnit-compatible XML for 
compatibility with CI systems.

*************
    Site Menu
*************

.. toctree::
    :maxdepth: 1
    
    configfile
    scripts
    graphs
    faq
    dev
    changelog
    
*******************************
    Discussion / Help / Updates
*******************************

* IRC: `Freenode <http://freenode.net/>`_ ``#multimech`` channel
* Mailing List: `Google Group <http://groups.google.com/group/multi-mechanize>`_
* Twitter: `twitter.com/multimechanize <http://twitter.com/multimechanize>`_

*************************
    Quick Install / Setup
*************************

Multi-Mechanize can be installed from `PyPI <http://pypi.python.org/pypi/multi-mechanize>`_ using `pip <http://www.pip-installer.org>`_::
    
    pip install -U multi-mechanize

... or download the `source distribution from PyPI <http://pypi.python.org/pypi/multi-mechanize#downloads>`_, unarchive, and run::

    python setup.py install

**********************
    Usage Instructions
**********************

------------------------
    Create a New Project
------------------------

Create a new test project with ``multimech-newproject``::

    $ multimech-newproject my_project

Each test project contains the following:

 * ``config.cfg``: configuration file. set your test options
 * ``test_scripts/``: directory for virtual user scripts. add your test scripts here.
 * ``results/``: directory for results storage. a timestamped directory is created for each test run containing an html summary report, raw csv data, and png image files.

``multimech-newproject`` will create a mock project, using a single script that generates random timer data.  Check it out for a basic example. 

-----------------
    Run a Project
-----------------

Run a test project with ``multimech-run``::

    $ multimech-run my_project

-------------------------
    Project Configuration
-------------------------


**********************************************
    Sample Scripts (Virtual User Transactions)
**********************************************

HTTP GETs using `Requests <http://docs.python-requests.org/>`_::

    import requests

    class Transaction(object):
        def run(self):
            r = requests.get('https://github.com/timeline.json')
            r.raw.read()

HTTP GETs using `Mechanize <http://wwwsearch.sourceforge.net/mechanize/>`_ (with timer and assertions)::

    import mechanize
    import time

    class Transaction(object):
        def run(self):
            br = mechanize.Browser()
            br.set_handle_robots(False)
            
            start_timer = time.time()
            resp = br.open('http://www.example.com/')
            resp.read()
            latency = time.time() - start_timer
            
            self.custom_timers['Example_Homepage'] = latency
            
            assert (resp.code == 200), 'Bad HTTP Response'
            assert ('Example Web Page' in resp.get_data())

****************************
    Detailed Install / Setup
****************************

The following detailed instructions are for Debian/Ubuntu Linux. 
For other platforms, the setup is generally the same, with the 
exeption of installing system dependencies.  

Required: Python 2.6 or 2.7

-----------------------
    system-wide install
-----------------------

* install dependencies on Debian/Ubuntu::

    $ sudo apt-get install python-pip python-matplotlib
    
* install multi-mechanize from PyPI using Pip::

    $ sudo pip install -U multi-mechanize

-------------------------------------------------------------
    virtualenv + pip install (with matplotlib system package)
-------------------------------------------------------------

* install dependencies on Debian/Ubuntu::

    $ sudo apt-get install python-virtualenv python-matplotlib

* install multi-mechanize from PyPI in a virtualenv::

    $ virtualenv --system-site-packages ENV
    $ cd ENV
    $ source bin/activate
    (ENV)$ pip install multi-mechanize
    
------------------------------------------------------
    virtualenv + pip install (with no-site-packages)
------------------------------------------------------

* install dependencies on Debian/Ubuntu::

    $ sudo apt-get install build-essential libfreetype6-dev libpng-dev
    $ sudo apt-get install python-dev python-virtualenv

* install multi-mechanize and matplotlib from PyPI in a virtualenv::

    $ virtualenv ENV
    $ cd ENV
    $ source bin/activate
    (ENV)$ pip install multi-mechanize
    (ENV)$ pip install matplotlib

----

.. image:: assets/python-powered.png
