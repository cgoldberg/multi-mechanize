#!/usr/bin/env python
#
#  Copyright (c) 2010 Brian Knox (taotetek@gmail.com)
#  License: GNU LGPLv3
#  
#  This file is part of Multi-Mechanize
#
"""a collection of functions and classes for multi-mechanize results files"""

import re
import fileinput
from datetime import datetime

try:
    from sqlalchemy.orm import sessionmaker, mapper, relation
    from sqlalchemy import create_engine
    from sqlalchemy import Table, Column, Integer, String, Float, DateTime
    from sqlalchemy import ForeignKey, UniqueConstraint
    from sqlalchemy import MetaData
except ImportError:
    print "(optional: please install sqlalchemy to enable db logging)"

LOGLINE_RE = re.compile('(.+),(.+),(.+),(.+),(.+),(.?),(\{.+\})')

class ResultRow(object):
    """class representing a multi-mechanize results.csv row"""
    def __init__(self, project_name, run_id, trans_count, elapsed, epoch, 
            user_group_name, scriptrun_time, error, custom_timers):
        self.project_name = str(project_name)
        self.run_id = run_id
        self.trans_count = int(trans_count)
        self.elapsed = float(elapsed)
        self.epoch = int(epoch)
        self.user_group_name = str(user_group_name)
        self.scriptrun_time = float(scriptrun_time)
        self.error = str(error)
        self.custom_timers = str(custom_timers)

    def __repr__(self):
        return "<ResultRow('%s','%s','%i','%.3f','%i','%s','%.3f','%s','%s')>" % (
                self.project_name, self.run_id, self.trans_count, self.elapsed, 
                self.epoch, self.user_group_name, self.scriptrun_time, 
                self.error, self.custom_timers)

    def __str__(self):
        """returns original csv row as in results.csv"""
        return "%i,%.3f,%i,%s,%.3f,%s,%s" % (
                self.trans_count, self.elapsed, self.epoch, 
                self.user_group_name, self.scriptrun_time, 
                self.error, self.custom_timers)

class TimerRow(object):
    """class representing a multi-mechanize custom timer result"""
    def __init__(self, timer_name, elapsed):
        self.timer_name = str(timer_name)
        self.elapsed = int(elapsed)

    def __repr__(self):
        return "<TimerRow('%s', '%s')>" % (self.timer_name, self.elapsed)

def get_run_id(run_localtime):
    """given a run localtime returns a datetime object"""
    run_id = datetime(run_localtime.tm_year, run_localtime.tm_mon,
        run_localtime.tm_mday, run_localtime.tm_hour, run_localtime.tm_min,
        run_localtime.tm_sec)
    return run_id

def sa_get_results_db_table(sa_metadata):
    """returns the mechanize_results table object"""
    table = Table('mechanize_results', sa_metadata,
        Column('id',Integer, nullable=False, primary_key=True),
        Column('project_name', String, nullable=False, index=True),
        Column('run_id', DateTime, nullable=False, index=True),
        Column('trans_count', Integer, nullable=False, index=True),
        Column('elapsed', Float, nullable=False, index=True),
        Column('epoch', Float, nullable=False, index=True),
        Column('user_group_name', String, nullable=False),
        Column('scriptrun_time', Float, nullable=False),
        Column('error', String),
        Column('custom_timers', String),
        UniqueConstraint('run_id','trans_count', name='uix_1')
        )
    return table

def sa_get_timers_db_table(sa_metadata):
    """returns the mechanize_timers table object"""
    table = Table('mechanize_timers', sa_metadata,
        Column('id', Integer, nullable=False, primary_key=True),
        Column('mechanize_results_id', Integer, ForeignKey('mechanize_results.id'), nullable=False),
        Column('timer_name', String, nullable=False, index=True),
        Column('elapsed', Float, nullable=False, index=True)
        )
    return table

def sa_create_mappings(results_db_table, timers_db_table):
    """create the sqlalchemy object to table mappings"""
    mapper(ResultRow, results_db_table, properties = {
        'timers': relation(TimerRow)
        })
    mapper(TimerRow, timers_db_table)

def load_results_database(project_name, run_localtime, results_dir, 
        results_database):
    """parse and load a multi-mechanize results csv file into a database"""
    engine = create_engine(results_database, echo=False)
    sa_metadata = MetaData()
    results_db_table = sa_get_results_db_table(sa_metadata)
    timers_db_table = sa_get_timers_db_table(sa_metadata)
    sa_metadata.create_all(engine)
    sa_create_mappings(results_db_table, timers_db_table)
    sa_session = sessionmaker(bind=engine)
    sa_current_session = sa_session()

    run_id = get_run_id(run_localtime)
    results_file = results_dir + 'results.csv'
    
    for line in fileinput.input([results_file]):
        line = line.rstrip()
        match = LOGLINE_RE.match(line)
        if match:
            result_row = ResultRow(project_name, run_id, match.group(1), 
                    match.group(2), match.group(3), match.group(4),
                    match.group(5), match.group(6), match.group(7))
           
            timer_data = eval(match.group(7))
            for index in timer_data:
                timer_row = TimerRow(index, timer_data[index])
                result_row.timers.append(timer_row)

            sa_current_session.add(result_row)
    
    sa_current_session.commit()
    sa_current_session.close()
