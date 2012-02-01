#!/usr/bin/env python
#
#  Copyright (c) 2010 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#  
#  This file is part of Multi-Mechanize


import urllib2
import time



class Transaction(object):
    def __init__(self):
        self.custom_timers = {}
    
    def run(self):
        start_timer = time.time()
        resp = urllib2.urlopen('http://192.168.1.69:8000/')
        content = resp.read()
        latency = time.time() - start_timer
        
        self.custom_timers['Django_Debug_Page'] = latency
        
        assert (resp.code == 200), 'Bad HTTP Response'
        assert ('It worked!' in content), 'Failed Content Verification'
        
        time.sleep(.5)
        

if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    print trans.custom_timers