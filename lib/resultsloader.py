#!/usr/bin/env python
#
#  Copyright (c) 2010 Brian Knox (taotetek@gmail.com)
#  License: GNU LGPLv3
#  
#  This file is part of Multi-Mechanize
#


import re
import fileinput
import sys
from datetime import datetime

try:
    from sqlalchemy.orm import sessionmaker, mapper, relation
    from sqlalchemy import create_engine
    from sqlalchemy import Table, Column, Integer, String, Float, DateTime
    from sqlalchemy import ForeignKey, UniqueConstraint
    from sqlalchemy import MetaData
except ImportError:
    print 'ERROR: install sqlalchemy to enable db logging, or remove results_database from your config.cfg\n'
    sys.exit(1)




def load_results_database(results_database, project_name, run_localtime, results_dir):
    """parse and load a multi-mechanize results csv file into a database"""
    engine = create_engine(results_database, echo=False)
    metadata = MetaData()

    results_db_table = Table('results', metadata,
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
        UniqueConstraint('run_id','trans_count', name='uix_1'),
        )

    timers_db_table = Table('timers', metadata,
        Column('id', Integer, nullable=False, primary_key=True),
        Column('result_id', Integer, ForeignKey('results.id'), nullable=False),
        Column('timer_name', String, nullable=False, index=True),
        Column('elapsed', Float, nullable=False, index=True),
        )

    metadata.create_all(engine)

    mapper(ResultRow, results_db_table, properties = {
        'timers': relation(TimerRow)
        })
    
    mapper(TimerRow, timers_db_table)
    session = sessionmaker(bind=engine)
    current_session = session()

    run_id = datetime(run_localtime.tm_year, run_localtime.tm_mon, run_localtime.tm_mday, run_localtime.tm_hour, run_localtime.tm_min, run_localtime.tm_sec)

    results_file = results_dir + 'results.csv'
    engine = create_engine(results_database)
    line_re = re.compile('(.+),(.+),(.+),(.+),(.+),(.?),(\{.+\})')
    for line in fileinput.input([results_file]):
        line = line.rstrip()
        match = line_re.match(line)
        if match:
            trans_count = int(match.group(1))
            elapsed = float(match.group(2))
            epoch = int(match.group(3))
            user_group_name = str(match.group(4))
            scriptrun_time = float(match.group(5))
            error = str(match.group(6))
            custom_timers = str(match.group(7))
            timer_data = eval(custom_timers)
            result_row = ResultRow(project_name, run_id, trans_count, elapsed, epoch, user_group_name, scriptrun_time, error, custom_timers)
            for index in timer_data:
                timer_row = TimerRow(index, timer_data[index])
                result_row.timers.append(timer_row)

            current_session.add(result_row)
    
    current_session.commit()
    current_session.close()

class ResultRow(object):
    """class representing a multi-mechanize results.csv row"""
    def __init__(self, project_name, run_id, trans_count, elapsed, epoch, 
            user_group_name, scriptrun_time, error, custom_timers):
        self.project_name = project_name
        self.run_id = run_id
        self.trans_count = trans_count
        self.elapsed = elapsed
        self.epoch = epoch
        self.user_group_name = user_group_name
        self.scriptrun_time = scriptrun_time
        self.error = error
        self.custom_timers = custom_timers

    def __repr__(self):
        return "<StoredResult('%s', '%s', '%i', '%.3f', '%i', '%s', '%.3f', '%s', '%s')>" % (
                self.project_name, self.run_id, self.trans_count, self.elapsed, 
                self.epoch, self.user_group_name, self.scriptrun_time, 
                self.error, self.custom_timers
                )

class TimerRow(object):
    """class representing a multi-mechanize custom timer result"""
    def __init__(self, timer_name, elapsed):
        self.timer_name = timer_name
        self.elapsed = elapsed

    def __repr__(self):
        return "<TimerRow('%s', '%s')>" % (self.timer_name, self.elapsed)
