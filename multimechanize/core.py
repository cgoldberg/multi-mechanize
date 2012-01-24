#!/usr/bin/env python
#
#  Copyright (c) 2010-2012 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#
#  This file is part of Multi-Mechanize | Performance Test Framework
#


import glob
import multiprocessing
import os
import sys
import threading
import time



def init(projects_dir, project_name):
    scripts_path = '%s/%s/test_scripts' % (projects_dir, project_name)
    if not os.path.exists(scripts_path):
        sys.stderr.write('\nERROR: can not find project: %s\n\n' % project_name)
        sys.exit(1)
    sys.path.append(scripts_path)
    for f in glob.glob( '%s/*.py' % scripts_path):  # import all test scripts as modules
        f = f.replace(scripts_path, '').replace(os.sep, '').replace('.py', '')
        exec('import %s' % f) in globals()



class UserGroup(multiprocessing.Process):
    def __init__(self, queue, process_num, user_group_name, num_threads, script_file, run_time, rampup):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.process_num = process_num
        self.user_group_name = user_group_name
        self.num_threads = num_threads
        self.script_file = script_file
        self.run_time = run_time
        self.rampup = rampup
        self.start_time = time.time()

    def run(self):
        threads = []
        for i in range(self.num_threads):
            spacing = float(self.rampup) / float(self.num_threads)
            if i > 0:
                time.sleep(spacing)
            agent_thread = Agent(self.queue, self.process_num, i, self.start_time, self.run_time, self.user_group_name, self.script_file)
            agent_thread.daemon = True
            threads.append(agent_thread)
            agent_thread.start()
        for agent_thread in threads:
            agent_thread.join()



class Agent(threading.Thread):
    def __init__(self, queue, process_num, thread_num, start_time, run_time, user_group_name, script_file):
        threading.Thread.__init__(self)
        self.queue = queue
        self.process_num = process_num
        self.thread_num = thread_num
        self.start_time = start_time
        self.run_time = run_time
        self.user_group_name = user_group_name
        self.script_file = script_file

        # choose most accurate timer to use (time.clock has finer granularity than time.time on windows, but shouldn't be used on other systems)
        if sys.platform.startswith('win'):
            self.default_timer = time.clock
        else:
            self.default_timer = time.time


    def run(self):
        elapsed = 0

        if self.script_file.lower().endswith('.py'):
            module_name = self.script_file.replace('.py', '')
        else:
            sys.stderr.write('ERROR: scripts must have .py extension. can not run test script: %s.  aborting user group: %s\n' % (self.script_file, self.user_group_name))
            return
        try:
            trans = eval(module_name + '.Transaction()')
        except NameError, e:
            sys.stderr.write('ERROR: can not find test script: %s.  aborting user group: %s\n' % (self.script_file, self.user_group_name))
            return
        #except Exception, e:
        #    sys.stderr.write('ERROR: failed initializing Transaction: %s.  aborting user group: %s\n' % (self.script_file, self.user_group_name))
        #    return

        trans.custom_timers = {}

        # scripts have access to these vars, which can be useful for loading unique data
        trans.thread_num = self.thread_num
        trans.process_num = self.process_num

        while elapsed < self.run_time:
            error = ''
            start = self.default_timer()

            try:
                trans.run()
            except Exception, e:  # test runner catches all script exceptions here
                error = str(e).replace(',', '')

            finish = self.default_timer()

            scriptrun_time = finish - start
            elapsed = time.time() - self.start_time

            epoch = time.mktime(time.localtime())

            fields = (elapsed, epoch, self.user_group_name, scriptrun_time, error, trans.custom_timers)
            self.queue.put(fields)
