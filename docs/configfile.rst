.. _config-label:

Configuration
=============

****************************
    Config File (config.cfg)
****************************

Each project contains a ``config.cfg`` file where test settings are defined.

The config file contains a ``[global]`` section and ``[user_group-*]`` sections.

*************************
    Minimal Configuration
*************************

Here is a sample ``config.cfg`` file showing minimal options, defining 1 group of virtual users::

    [global]
    run_time = 100
    rampup = 100
    results_ts_interval = 10

    [user_group-1]
    threads = 10
    script = vu_script.py

**********************
    Full Configuration
**********************

Here is a sample ``config.cfg`` file showing all possible options, defining 2 groups of virtual users::

    [global]
    run_time = 300
    rampup = 300
    results_ts_interval = 30
    progress_bar = on
    console_logging = off
    xml_report = off
    results_database = sqlite:///my_project/results.db
    post_run_script = python my_project/foo.py

    [user_group-1]
    threads = 30
    script = vu_script1.py

    [user_group-2]
    threads = 30
    script = vu_script2.py

******************
    Global Options
******************

The following settings/options are available in the ``[global]`` config section:

* ``run_time``: duration of test (seconds) [required]
* ``rampup``: duration of user rampup (seconds) [required]
* ``results_ts_interval``: time series interval for results analysis (seconds) [required]
* ``progress_bar``: turn on/off console progress bar during test run [optional, default = on]
* ``console_logging``: turn on/off logging to stdout [optional, default = off]
* ``xml_report``: turn on/off xml/jtl report [optional, default = off]
* ``results_database``: database connection string [optional]
* ``post_run_script``: hook to call a script at test completion [optional]

***************
    User Groups
***************

The following settings/options are available in each ``[user_group-*]`` config section:

* ``threads``: number of threads/virtual users
* ``script``: virtual user test script to run
