
================================================
    Multi-Mechanize | Performance Test Framework
================================================

|

.. image:: assets/multimech-450.png

|

.. image:: assets/graphs.png

----

:Home: http://testutils.org/multimechanize
:Dev: http://github.com/cgoldberg/multimechanize
:PyPI: http://pypi.python.org/pypi/multimechanize
:License: GNU LGPLv3
:Author: Copyright (c) 2010-2012 Corey Goldberg

----

--------------------------------------
    Performance & Load Tests in Python
--------------------------------------

Multi-Mechanize is an open source framework for API performance and load testing. 
It allows you to run simultaneous python scripts to generate load (synthetic transactions) 
against a web site or API/service.

In your scripts, you have the convenience of mechanize along with the power of the full 
Python programming language at your disposal. You programmatically create test scripts to 
simulate virtual user activity. Your scripts will then generate HTTP requests to intelligently 
navigate a web site or send requests to a web service.

Multi-Mechanize uses a multi-process, multi-threaded engine to replay your scripts and 
generate concurrent virtual users.
    
Test output reports are saved as HTML (with PNG graphs), or JUnit-compatible XML for compatibility with 
CI systems.

----------------------
    Install / Download
----------------------

SST can be installed from `PyPI <http://pypi.python.org/pypi/multimechanize>`_ using `pip <http://www.pip-installer.org>`_::
    
    pip install -U multimechanize

... or download the 'source distribution from PyPI <http://pypi.python.org/pypi/multimechanize#downloads>`_, unarchive, and run::

    python setup.py install
    
------------------------------------
    Discussion / Help / Mailing List
------------------------------------

* http://groups.google.com/group/multi-mechanize

-------------
    Site Menu
-------------

.. toctree::
    :maxdepth: 1
    
    Configuration <configfile>
    Developing Scripts <developing>
    Sample Graphs <graphs>
    F.A.Q. <faq>
   
----

.. image:: assets/python-powered.png
