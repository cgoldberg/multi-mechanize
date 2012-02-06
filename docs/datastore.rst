Database Storage for Test Result Data
=====================================

Test data and results can be stored in a database when a test run completes. 
To enable database storage, you must add a ``results_database`` option to 
your ``config.cfg``, which defines the database connection string.

**************************
    Example config setting
**************************

::

    results_database: sqlite:///results.db

****************
    Requirements
****************

* database storage requires `sqlalchemy <http://www.sqlalchemy.org>`_

******************************
    Example connection strings
******************************

Several database back-ends are available to choose from:

:SQLite: ``sqlite:///dbname``
:MySQL: ``mysql://user:password@localhost/dbname``
:PostgreSQL: ``postgresql://user:password@host:port/dbname``
:MS SQL Server: ``mssql://mydsn``

* SQLite is supported natively by Python, so there is no installation or configuration necessary.
* The results database is created automatically on first use, no need to run your own DDL code.

****************************
    Results Database Diagram
****************************

.. image:: assets/results_database_erd.png

************************
    Sample DB Query Code
************************

Here is some sample code for retrieving results from the database via sqlalchemy::

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from multimechanize.resultsloader import ResultRow
    from multimechanize.resultsloader import GlobalConfig
    from multimechanize.resultsloader import UserGroupConfig
    from multimechanize.resultsloader import TimerRow

    engine = create_engine('sqlite:///results.db')
    session = sessionmaker(bind=engine)
    current = session()

    for rr in current.query(ResultRow).order_by(ResultRow.trans_count):
        print rr
        print rr.global_config
        print rr.global_config.user_group_configs
        print rr.timers
