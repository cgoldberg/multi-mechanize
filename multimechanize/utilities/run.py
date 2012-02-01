#!/usr/bin/env python
#
#  Copyright (c) 2010-2012 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#
#  This file is part of Multi-Mechanize | Performance Test Framework
#



import ConfigParser
import multiprocessing
import optparse
import os
import Queue
import shutil
import subprocess
import sys
import time

try:
    # installed
    import multimechanize
except ImportError:
    # from dev/source
    this_dir = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(os.path.join(this_dir, '../../'))
    import multimechanize

import multimechanize.core as core
import multimechanize.results as results
import multimechanize.resultswriter as resultswriter
import multimechanize.progressbar as progressbar
    

usage = 'Usage: %prog <project name> [options]'
parser = optparse.OptionParser(usage=usage)
parser.add_option('-p', '--port', dest='port', type='int', help='rpc listener port')
parser.add_option('-r', '--results', dest='results_dir', help='results directory to reprocess')
parser.add_option('-b', '--bind-addr', dest='bind_addr', help='rpc bind address', default='localhost')
parser.add_option('-d', '--directory', dest='projects_dir', help='directory containing project folder', default='.')
cmd_opts, args = parser.parse_args()

try:
    project_name = args[0]
except IndexError:
    sys.stderr.write('\nERROR: no project specified\n\n')
    sys.stderr.write('%s\n' % usage)
    sys.stderr.write('Example: multimech-run my_project\n\n')
    sys.exit(1)

core.init(cmd_opts.projects_dir, project_name)




def main():
    if cmd_opts.results_dir:  # don't run a test, just re-process results
        rerun_results(cmd_opts.results_dir)
    elif cmd_opts.port:
        import multimechanize.rpcserver
        multimechanize.rpcserver.launch_rpc_server(cmd_opts.bind_addr, cmd_opts.port, project_name, run_test)
    else:
        run_test()
    return



def run_test(remote_starter=None):
    if remote_starter is not None:
        remote_starter.test_running = True
        remote_starter.output_dir = None

    run_time, rampup, results_ts_interval, console_logging, progress_bar, results_database, post_run_script, xml_report, user_group_configs = configure(project_name)

    run_localtime = time.localtime()
    output_dir = '%s/%s/results/results_%s' % (cmd_opts.projects_dir, project_name, time.strftime('%Y.%m.%d_%H.%M.%S/', run_localtime))

    # this queue is shared between all processes/threads
    queue = multiprocessing.Queue()
    rw = resultswriter.ResultsWriter(queue, output_dir, console_logging)
    rw.daemon = True
    rw.start()

    user_groups = []
    for i, ug_config in enumerate(user_group_configs):
        ug = core.UserGroup(queue, i, ug_config.name, ug_config.num_threads, ug_config.script_file, run_time, rampup)
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

        if progress_bar:
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
            if progress_bar:
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
    results.output_results(output_dir, 'results.csv', run_time, rampup, results_ts_interval, user_group_configs, xml_report)
    print 'created: %sresults.html\n' % output_dir
    if xml_report:
        print 'created: %sresults.jtl' % output_dir
        print 'created: last_results.jtl\n'

    # copy config file to results directory
    project_config = os.sep.join([cmd_opts.projects_dir, project_name, 'config.cfg'])
    saved_config = os.sep.join([output_dir, 'config.cfg'])
    shutil.copy(project_config, saved_config)

    if results_database is not None:
        print 'loading results into database: %s\n' % results_database
        import multimechanize.resultsloader
        multimechanize.resultsloader.load_results_database(project_name, run_localtime, output_dir, results_database,
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
    output_dir = '%s/%s/results/%s/' % (cmd_opts.projects_dir, project_name, results_dir)
    saved_config = '%s/config.cfg' % output_dir
    run_time, rampup, results_ts_interval, console_logging, progress_bar, results_database, post_run_script, xml_report, user_group_configs = configure(project_name, config_file=saved_config)
    print '\n\nanalyzing results...\n'
    results.output_results(output_dir, 'results.csv', run_time, rampup, results_ts_interval, user_group_configs, xml_report)
    print 'created: %sresults.html\n' % output_dir
    if xml_report:
        print 'created: %sresults.jtl' % output_dir
        print 'created: last_results.jtl\n'



def configure(project_name, config_file=None):
    user_group_configs = []
    config = ConfigParser.ConfigParser()
    if config_file is None:
        config_file = '%s/%s/config.cfg' % (cmd_opts.projects_dir, project_name)
    config.read(config_file)
    for section in config.sections():
        if section == 'global':
            run_time = config.getint(section, 'run_time')
            rampup = config.getint(section, 'rampup')
            results_ts_interval = config.getint(section, 'results_ts_interval')
            try:
                console_logging = config.getboolean(section, 'console_logging')
            except ConfigParser.NoOptionError:
                console_logging = False
            try:
                progress_bar = config.getboolean(section, 'progress_bar')
            except ConfigParser.NoOptionError:
                progress_bar = True
            try:
                results_database = config.get(section, 'results_database')
                if results_database == 'None': results_database = None
            except ConfigParser.NoOptionError:
                results_database = None
            try:
                post_run_script = config.get(section, 'post_run_script')
                if post_run_script == 'None': post_run_script = None
            except ConfigParser.NoOptionError:
                post_run_script = None
            try:
                xml_report = config.getboolean(section, 'xml_report')
            except ConfigParser.NoOptionError:
                xml_report = False
        else:
            threads = config.getint(section, 'threads')
            script = config.get(section, 'script')
            user_group_name = section
            ug_config = UserGroupConfig(threads, user_group_name, script)
            user_group_configs.append(ug_config)

    return (run_time, rampup, results_ts_interval, console_logging, progress_bar, results_database, post_run_script, xml_report, user_group_configs)



class UserGroupConfig(object):
    def __init__(self, num_threads, name, script_file):
        self.num_threads = num_threads
        self.name = name
        self.script_file = script_file



if __name__ == '__main__':
    main()
