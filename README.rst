
============================================
Multi-Mechanize - Performance Test Framework
============================================

* Copyright: (c) 2010-2012 Corey Goldberg (corey@goldb.org)
* License: GNU LGPLv3
* Requires: Python 2.6 or 2.7

----

:Web: `multimechanize.com <http://multimechanize.com>`_
:Dev: `git repo <http://github.com/cgoldberg/multi-mechanize>`_
:Twitter: `multimechanize tweets <http://twitter.com/multimechanize>`_
:IRC: #multimech (freenode)

----

-------------------
    Setup / Install
-------------------

install dependencies on Debian/Ubuntu::

    $ sudo apt-get install python-virtualenv python-matplotlib

install from dev branch in a virtualenv::

    $ virtualenv --system-site-packages multimech
    $ cd multimech
    $ source bin/activate
    (multimech)$ pip install -e git+http://github.com/cgoldberg/multi-mechanize.git#egg=multimechanize

create a new project::

    (multimech)$ multimech-newproject my_project

run a project::

    (multimech)$ multimech-run my_project

