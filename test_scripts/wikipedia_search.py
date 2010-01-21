#!/usr/bin/env python
#  Copyright (c) 2010 Corey Goldberg (corey@goldb.org)
#  License: GNU GPLv3


import mechanize


class MechTransaction(object):
    def __init__(self):
        self.bytes_received = 0
        self.custom_timers = {}
    
    def run(self):
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 Compatible')]
        
        resp = br.open('http://www.wikipedia.org/')
        resp.read()
        self.bytes_received += (len(resp.info()) + len(resp.get_data()))
        assert (resp.code == 200), 'Bad HTTP Response'
        assert ('Wikipedia, the free encyclopedia' in resp.get_data()), 'Text Assertion Failed'

        br.select_form(nr=0)
        br.form['search'] = 'foo'
        resp = br.submit()
        resp.read()
        self.bytes_received += (len(resp.info()) + len(resp.get_data()))
        assert (resp.code == 200), 'Bad HTTP Response'
        assert ('foobar' in resp.get_data()), 'Text Assertion Failed'



if __name__ == '__main__':
    trans = MechTransaction()
    trans.run()
    print trans.bytes_received
    print trans.custom_timers
