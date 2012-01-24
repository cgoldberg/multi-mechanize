#!/usr/bin/env python
#
#  Copyright (c) 2010-2012 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#
#  This file is part of Multi-Mechanize | Performance Test Framework
#


import os
import Queue
import threading
import time



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
