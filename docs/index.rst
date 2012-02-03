
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

Multi-Mechanize is an open source framework for API performance and load testing. 
It allows you to run simultaneous Python scripts to generate synthetic transactions 
against a web site or service.
    
Test output reports are saved as HTML (with PNG graphs), or JUnit-compatible XML 
for compatibility with CI systems.

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

* IRC: #multimech (freenode)
* Google Group: http://groups.google.com/group/multi-mechanize
* Twitter: http://twitter.com/multimechanize

*************************
    Quick Install / Setup
*************************

Multi-Mechanize can be installed from `PyPI <http://pypi.python.org/pypi/multi-mechanize>`_ using `pip <http://www.pip-installer.org>`_::
    
    pip install -U multi-mechanize

... or download the `source distribution from PyPI <http://pypi.python.org/pypi/multi-mechanize#downloads>`_, unarchive, and run::

    python setup.py install

****************
    Instructions
****************

------------------------
    Create a New Project
------------------------

Once installed, you can create a new project::

    $ multimech-newproject my_project

Each project contains the following:

 * ``config.cfg``: configuration file. set your test options
 * ``test_scripts``: directory for virtual user scripts. add your test scripts here.
 * ``results``: directory for results storage. a timestamped directory is created for each test run containing an html summary report, raw csv data, and png image files.

``multimech-newproject`` will create a mock project, with a single script that generates random timer data.  Check it out for a basic example. 

------------------------
    Run a Project
------------------------

    $ multimech-run my_project

-------------------------
    Project Configuration
-------------------------


------------------------
    Virtual User Scripts
------------------------

    create your virtual user scripts

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
