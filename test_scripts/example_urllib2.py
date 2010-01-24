#!/usr/bin/env python
#  Copyright (c) 2010 Corey Goldberg (corey@goldb.org)
#  License: GNU GPLv3


import urllib2
import time



class Transaction(object):
    def __init__(self):
        self.bytes_received = 0
        self.custom_timers = {}
    
    def run(self):
        start_timer = time.time()
        resp = urllib2.urlopen('http://www.example.com/')
        content = resp.read()
        latency = time.time() - start_timer
        
        self.custom_timers['Example_Homepage'] = latency
        self.bytes_received += len(content)
        
        assert (resp.code == 200), 'Bad HTTP Response'
        assert ('Example Web Page' in content), 'Failed Content Verification'


if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    print trans.bytes_received
    print trans.custom_timers