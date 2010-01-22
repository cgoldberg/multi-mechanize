#!/usr/bin/env python
#  Copyright (c) 2010 Corey Goldberg (corey@goldb.org)
#  License: GNU GPLv3
#  
#  This file is part of Multi-Mechanize:
#       Multi-Process, Multi-Threaded, Web Load Generator, with python-mechanize agents
#
#  requires Python 2.6+


import multiprocessing
import os
import Queue
import sys
import threading
import time

from test_scripts import *


PROCESSES = 100
PROCESS_THREADS = 300
RUN_TIME = 30  # secs
RAMPUP = 10  # secs



def main():
    queue = multiprocessing.Queue()
    r = Results(queue)
    r.daemon = True
    r.start()
    
    start_time = time.time() 
    
    managers = [] 
    for i in range(PROCESSES):
        manager = MultiMechanize(queue, start_time, i, PROCESS_THREADS, RUN_TIME, RAMPUP)
        managers.append(manager)
    for manager in managers:
        manager.start()
    
    

class MultiMechanize(multiprocessing.Process):
    def __init__(self, queue, start_time, process_num, num_threads=1, run_time=10, rampup=0):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.start_time = start_time
        self.process_num = process_num
        self.num_threads = num_threads
        self.run_time = run_time
        self.rampup = rampup
        
    def run(self):
        self.running = True
        thread_refs = []
        for i in range(self.num_threads):
            spacing = float(self.rampup) / float(self.num_threads)
            if i > 0:
                time.sleep(spacing)
            agent_thread = MechanizeAgent(self.queue, self.start_time, self.run_time)
            agent_thread.daemon = True
            thread_refs.append(agent_thread)
            #print 'starting process %i, thread %i' % (self.process_num + 1, i + 1)
            agent_thread.start()            
        for agent_thread in thread_refs:
            agent_thread.join()
        


class MechanizeAgent(threading.Thread):
    def __init__(self, queue, start_time, run_time):
        threading.Thread.__init__(self)
        self.queue = queue
        self.start_time = start_time
        self.run_time = run_time
        
        # choose timer to use
        if sys.platform.startswith('win'):
            self.default_timer = time.clock
        else:
            self.default_timer = time.time
            
    def run(self):
        elapsed = 0
        error = ''
        while elapsed < self.run_time:
            start = self.default_timer()               
            
            script_name = 'example_mock'
            trans = eval(script_name + '.Transaction()')
            try:
                trans.run()
                status = 'PASS'
            except Exception, e:
                status = 'FAIL'
                error = str(e)

            finish = self.default_timer()
            scriptrun_time = finish - start
            elapsed = time.time() - self.start_time 
            self.queue.put((elapsed, scriptrun_time, status, trans.bytes_received, trans.custom_timers, error))
            


class Results(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.trans_count = 0
    
    def run(self):
        with open('results.csv', 'w') as f:     
            while True:
                try:
                    elapsed, scriptrun_time, status, bytes_received, custom_timers, error = self.queue.get(False)
                    self.trans_count += 1
                    f.write('%i, %.3f,%.3f,%s,%i,%s,%s\n' % (self.trans_count, elapsed, scriptrun_time, status, bytes_received, repr(custom_timers), repr(error)))
                    f.flush()
                    print '%i, %.3f, %.3f, %s, %i, %s, %s' % (self.trans_count, elapsed, scriptrun_time, status, bytes_received, repr(custom_timers), repr(error))
                except Queue.Empty:
                    time.sleep(.1)


        
        
if __name__ == '__main__':
    main()
