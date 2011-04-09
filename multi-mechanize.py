#!/usr/bin/env python
#
#  Copyright (c) 2010-2011 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3 - distributed under the terms of the GNU Lesser General Public License version 3
#  
#  This file is part of Multi-Mechanize:
#       Multi-Process, Multi-Threaded, Web Load Generator, with python-mechanize agents
#
#  requires Python 2.6+



import ConfigParser
import glob
import multiprocessing
import optparse
import os
import Queue
import shutil
import subprocess
import sys
import threading
import time
import lib.results as results
import lib.progressbar as progressbar        

usage = 'Usage: %prog <project name> [options]'
parser = optparse.OptionParser(usage=usage)
parser.add_option('-p', '--port', dest='port', type='int', help='rpc listener port')
parser.add_option('-r', '--results', dest='results_dir', help='results directory to reprocess')
cmd_opts, args = parser.parse_args()

try:
    project_name = args[0]
except IndexError:
    sys.stderr.write('\nERROR: no project specified\n\n')
    sys.stderr.write('usage: python multi-mechanize.py <project_name>\n')
    sys.stderr.write('example: python multi-mechanize.py default_project\n\n')
    sys.exit(1)  

scripts_path = 'projects/%s/test_scripts' % project_name
if not os.path.exists(scripts_path):
    sys.stderr.write('\nERROR: can not find project: %s\n\n' % project_name)
    sys.exit(1) 
sys.path.append(scripts_path)          
for f in glob.glob( '%s/*.py' % scripts_path):  # import all test scripts as modules
    f = f.replace(scripts_path, '').replace(os.sep, '').replace('.py', '')
    exec('import %s' % f)



def main():
    if cmd_opts.results_dir:  # don't run a test, just reprocess results
        rerun_results(cmd_opts.results_dir)
    elif cmd_opts.port:
        import lib.rpcserver
        lib.rpcserver.launch_rpc_server(cmd_opts.port, project_name, run_test)
    else:  
        run_test()
    return
        
        
    
def run_test(remote_starter=None):
    if remote_starter is not None:
        remote_starter.test_running = True
        remote_starter.output_dir = None
        
    run_time, rampup, console_logging, results_ts_interval, user_group_configs, results_database, post_run_script = configure(project_name)
    
    run_localtime = time.localtime() 
    output_dir = time.strftime('projects/' + project_name + '/results/results_%Y.%m.%d_%H.%M.%S/', run_localtime) 
        
    # this queue is shared between all processes/threads
    queue = multiprocessing.Queue()
    rw = ResultsWriter(queue, output_dir, console_logging)
    rw.daemon = True
    rw.start()
    
    user_groups = [] 
    for i, ug_config in enumerate(user_group_configs):
        ug = UserGroup(queue, i, ug_config.name, ug_config.num_threads, ug_config.script_file, run_time, rampup)
        user_groups.append(ug)    
    for user_group in user_groups:
        user_group.start()
        
    start_time = time.time() 
    
    if console_logging:
        for user_group in user_groups:
            user_group.join()
    else:
        print '\n  user_groups:  %i' % len(user_groups)
        print '  threads: %i\n' % (ug_config.num_threads * len(user_groups))
        p = progressbar.ProgressBar(run_time)
        elapsed = 0
        while elapsed < (run_time + 1):
            p.update_time(elapsed)
            if sys.platform.startswith('win'):
                print '%s   transactions: %i  timers: %i  errors: %i\r' % (p, rw.trans_count, rw.timer_count, rw.error_count),
            else:
                print '%s   transactions: %i  timers: %i  errors: %i' % (p, rw.trans_count, rw.timer_count, rw.error_count)
                sys.stdout.write(chr(27) + '[A' )
            time.sleep(1)
            elapsed = time.time() - start_time
        
        print p
        
        while [user_group for user_group in user_groups if user_group.is_alive()] != []:
            if sys.platform.startswith('win'):
                print 'waiting for all requests to finish...\r',
            else:
                print 'waiting for all requests to finish...\r'
                sys.stdout.write(chr(27) + '[A' )
            time.sleep(.5)
            
        if not sys.platform.startswith('win'):
            print

    # all agents are done running at this point
    time.sleep(.2) # make sure the writer queue is flushed
    print '\n\nanalyzing results...\n'
    results.output_results(output_dir, 'results.csv', run_time, rampup, results_ts_interval, user_group_configs)
    print 'created: %sresults.html\n' % output_dir
    
    # copy config file to results directory
    project_config = os.sep.join(['projects', project_name, 'config.cfg'])
    saved_config = os.sep.join([output_dir, 'config.cfg'])
    shutil.copy(project_config, saved_config)
    
    if results_database is not None:
        print 'loading results into database: %s\n' % results_database
        import lib.resultsloader
        lib.resultsloader.load_results_database(project_name, run_localtime, output_dir, results_database, 
                run_time, rampup, results_ts_interval, user_group_configs)
    
    if post_run_script is not None:
        print 'running post_run_script: %s\n' % post_run_script
        subprocess.call(post_run_script)
        
    print 'done.\n'
    
    if remote_starter is not None:
        remote_starter.test_running = False
        remote_starter.output_dir = output_dir
    
    return
    
    
    
def rerun_results(results_dir):
    output_dir = 'projects/%s/results/%s/' % (project_name, results_dir)
    saved_config = '%s/config.cfg' % output_dir
    run_time, rampup, console_logging, results_ts_interval, user_group_configs, results_database, post_run_script = configure(project_name, config_file=saved_config)
    print '\n\nanalyzing results...\n'
    results.output_results(output_dir, 'results.csv', run_time, rampup, results_ts_interval, user_group_configs)
    print 'created: %sresults.html\n' % output_dir



def configure(project_name, config_file=None):
    user_group_configs = []
    config = ConfigParser.ConfigParser()
    if config_file is None:
        config_file = 'projects/%s/config.cfg' % project_name
    config.read(config_file)
    for section in config.sections():
        if section == 'global':
            run_time = config.getint(section, 'run_time')
            rampup = config.getint(section, 'rampup')
            console_logging = config.getboolean(section, 'console_logging')
            results_ts_interval = config.getint(section, 'results_ts_interval')
            try:
                results_database = config.get(section, 'results_database')
            except ConfigParser.NoOptionError:
                results_database = None
            try:
                post_run_script = config.get(section, 'post_run_script')
            except ConfigParser.NoOptionError:
                post_run_script = None
        else:
            threads = config.getint(section, 'threads')
            script = config.get(section, 'script')
            user_group_name = section
            ug_config = UserGroupConfig(threads, user_group_name, script)
            user_group_configs.append(ug_config)

    return (run_time, rampup, console_logging, results_ts_interval, user_group_configs, results_database, post_run_script)
    


class UserGroupConfig(object):
    def __init__(self, num_threads, name, script_file):
        self.num_threads = num_threads
        self.name = name
        self.script_file = script_file
    
    
    
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
        except Exception, e:
            sys.stderr.write('ERROR: failed initializing Transaction: %s.  aborting user group: %s\n' % (self.script_file, self.user_group_name))
            return
        
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
            


class ResultsWriter(threading.Thread):
    def __init__(self, queue, output_dir, console_logging):
        threading.Thread.__init__(self)
        self.queue = queue
        self.console_logging = console_logging
        self.output_dir = output_dir
        self.trans_count = 0
        self.timer_count = 0
        self.error_count = 0
        
        try:
            os.makedirs(self.output_dir, 0755)
        except OSError:
            sys.stderr.write('ERROR: Can not create output directory\n')
            sys.exit(1)    
    
    def run(self):
        with open(self.output_dir + 'results.csv', 'w') as f:     
            while True:
                try:
                    elapsed, epoch, self.user_group_name, scriptrun_time, error, custom_timers = self.queue.get(False)
                    self.trans_count += 1
                    self.timer_count += len(custom_timers)
                    if error != '':
                        self.error_count += 1
                    f.write('%i,%.3f,%i,%s,%f,%s,%s\n' % (self.trans_count, elapsed, epoch, self.user_group_name, scriptrun_time, error, repr(custom_timers)))
                    f.flush()
                    if self.console_logging:
                        print '%i, %.3f, %i, %s, %.3f, %s, %s' % (self.trans_count, elapsed, epoch, self.user_group_name, scriptrun_time, error, repr(custom_timers))
                except Queue.Empty:
                    time.sleep(.05)



if __name__ == '__main__':
    main()

