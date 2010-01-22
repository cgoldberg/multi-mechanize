#!/usr/bin/env python
#  Copyright (c) 2010 Corey Goldberg (corey@goldb.org)
#  License: GNU GPLv3

import random
import time



class Transaction(object):
    def __init__(self):
        self.bytes_received = 0
        self.custom_timers = {}
    
    def run(self):
        r = random.uniform(1, 2)
        time.sleep(r)
        
        self.custom_timers['Example_Timer'] = r
        self.bytes_received += int(random.uniform(1000, 2000))
        
 
 
if __name__ == '__main__':
    trans = MechTransaction()
    trans.run()
    print trans.bytes_received
    print trans.custom_timers