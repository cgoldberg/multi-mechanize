#!/usr/bin/env python
#  Copyright (c) 2010 Corey Goldberg (corey@goldb.org)
#  License: GNU GPLv3


import mechanize


class MechTransaction(object):
    def __init__(self):
        self.bytes_received = 0
        self.custom_timers = {}
        self.errors = []
    
    def run(self):
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 Compatible')]
        
        try:
            resp = br.open('http://www.wikipedia.org/')
            resp.read()
            self.bytes_received += (len(resp.info()) + len(resp.get_data()))
            #print resp.info()
            #print resp.get_data()
        except Exception, e:
            self.errors.append(str(e))
        
        try:  
            br.select_form(nr=0)
            br.form['search'] = 'foo'
            resp = br.submit()
            resp.read()
            self.bytes_received += (len(resp.info()) + len(resp.get_data()))
            #print resp.info()
            #print resp.get_data()
            assert (resp.code == 200), 'Bad HTTP Response'
            assert ('foobar' in resp.get_data()), 'Text Assertion Failed'
        except Exception, e:
            self.errors.append(str(e))



if __name__ == '__main__':
    trans = MechTransaction()
    trans.run()
    print trans.bytes_received
    print trans.custom_timers
    print trans.errors
