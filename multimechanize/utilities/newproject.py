#!/usr/bin/env python
#
#  Copyright (c) 2010-2012 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#
#  This file is part of Multi-Mechanize | Performance Test Framework
#


import os
import sys


CONFIG_NAME = 'config.cfg'
SCRIPT_NAME = 'v_user.py'
SCRIPTS_DIR = 'test_scripts'


CONFIG_CONTENT = """
[global]
run_time = 30
rampup = 0
results_ts_interval = 10
progress_bar = on
console_logging = off
xml_report = off


[user_group-1]
threads = 3
script = %s

[user_group-2]
threads = 3
script = %s

""" % (SCRIPT_NAME, SCRIPT_NAME)


SCRIPT_CONTENT = """
import random
import time


class Transaction(object):
    def __init__(self):
        pass

    def run(self):
        r = random.uniform(1, 2)
        time.sleep(r)
        self.custom_timers['Example_Timer'] = r


if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    print trans.custom_timers
"""


def create_project(
        project_name,
        config_name=CONFIG_NAME,
        script_name=SCRIPT_NAME,
        scripts_dir=SCRIPTS_DIR,
        config_content=CONFIG_CONTENT,
        script_content=SCRIPT_CONTENT,
    ):
    if os.path.exists(project_name):
        sys.stderr.write('\nERROR: project already exists: %s\n\n' % project_name)
        sys.exit(1)
    try:
        os.makedirs(project_name)
        os.makedirs(os.path.join(project_name, scripts_dir))
    except OSError as e:
        sys.stderr.write('\nERROR: can not create directory for %r\n\n' % project_name)
        sys.exit(1)
    with open(os.path.join(project_name, config_name), 'w') as f:
        f.write(config_content)
    with open(os.path.join(project_name, scripts_dir, script_name), 'w') as f:
        f.write(script_content)


def main():
    try:
        project_name = sys.argv[1]
    except IndexError:
        sys.stderr.write('\nERROR: no project specified\n\n')
        sys.stderr.write('Usage: multimech-newproject <project name>\n\n')
        sys.exit(1)

    create_project(project_name)


if __name__ == '__main__':
    main()
