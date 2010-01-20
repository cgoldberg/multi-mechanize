#!/usr/bin/env python
#  Copyright (c) 2010 Corey Goldberg (corey@goldb.org)
#  License: GNU GPLv3


import mechanize
import urllib2


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
            assert (resp.code == 200)
        except urllib2.URLError, e:
            self.errors.append(str(e))
        
        try:  
            br.select_form(nr=0)
            br.form['search'] = 'foo'
            resp = br.submit()
            resp.read()
            self.bytes_received += (len(resp.info()) + len(resp.get_data()))
            #print resp.info()
            #print resp.get_data()
            assert (resp.code == 200)
        except Exception, e:
            self.errors.append(str(e))
            
        return (self.bytes_received, self.custom_timers, self.errors)



if __name__ == '__main__':
    trans = MechTransaction()
    bytes_received, custom_timers, errors = trans.run()
    print bytes_received
    print custom_timers
    print errors
