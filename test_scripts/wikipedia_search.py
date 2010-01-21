#!/usr/bin/env python
#  Copyright (c) 2010 Corey Goldberg (corey@goldb.org)
#  License: GNU GPLv3


import mechanize
import time



class MechTransaction(object):
    def __init__(self):
        self.bytes_received = 0
        self.custom_timers = {}
    
    def run(self):
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 Compatible')]
        
        start_timer = time.time()
        resp = br.open('http://www.wikipedia.org/')
        resp.read()
        time.time() - start_timer
        self.custom_timers['Load_Front_Page'] = latency  # store the custom timer
        
        self.bytes_received += len(resp.get_data())  # store the amount of data received
        
        # verify responses are valid
        assert (resp.code == 200), 'Bad HTTP Response'
        assert ('Wikipedia, the free encyclopedia' in resp.get_data()), 'Text Assertion Failed'
        
        time.sleep(2)  # think-time
        
        br.select_form(nr=0)  # select first (zero-based) form on page
        br.form['search'] = 'foo'  # set form field
        
        start_timer = time.time()
        resp = br.submit()  # submit the form
        resp.read()
        latency = time.time() - start_timer
        self.custom_timers['Load_Front_Page'] = latency  # store the custom timer
        
        self.bytes_received += len(resp.get_data())  # store the amount of data received
        
        # verify responses are valid
        assert (resp.code == 200), 'Bad HTTP Response'
        assert ('foobar' in resp.get_data()), 'Text Assertion Failed'
        
        time.sleep(3)  # think-time


if __name__ == '__main__':
    trans = MechTransaction()
    trans.run()
    print trans.bytes_received
    print trans.custom_timers
