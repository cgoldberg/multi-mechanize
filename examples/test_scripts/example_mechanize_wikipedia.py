#
#  Copyright (c) 2010 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#
#  This file is part of Multi-Mechanize
#


import mechanize
import time



class Transaction(object):
    def __init__(self):
        self.custom_timers = {}

    def run(self):
        # create a Browser instance
        br = mechanize.Browser()
        # don't bother with robots.txt
        br.set_handle_robots(False)
        # add a custom header so wikipedia allows our requests
        br.addheaders = [('User-agent', 'Mozilla/5.0 Compatible')]

        # start the timer
        start_timer = time.time()
        # submit the request
        resp = br.open('http://www.wikipedia.org/')
        resp.read()
        # stop the timer
        latency = time.time() - start_timer

        # store the custom timer
        self.custom_timers['Load_Front_Page'] = latency

        # verify responses are valid
        assert (resp.code == 200), 'Bad HTTP Response'
        assert ('Wikipedia, the free encyclopedia' in resp.get_data()), 'Text Assertion Failed'

        # think-time
        time.sleep(2)

        # select first (zero-based) form on page
        br.select_form(nr=0)
        # set form field
        br.form['search'] = 'foo'

        # start the timer
        start_timer = time.time()
        # submit the form
        resp = br.submit()
        resp.read()
        # stop the timer
        latency = time.time() - start_timer

        # store the custom timer
        self.custom_timers['Search'] = latency

        # verify responses are valid
        assert (resp.code == 200), 'Bad HTTP Response'
        assert ('foobar' in resp.get_data()), 'Text Assertion Failed'

        # think-time
        time.sleep(2)



if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    print trans.custom_timers
