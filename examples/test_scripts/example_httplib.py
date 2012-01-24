#
#  Copyright (c) 2010 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#
#  This file is part of Multi-Mechanize
#


import httplib
import time



class Transaction(object):
    def __init__(self):
        self.custom_timers = {}

    def run(self):
        start_timer = time.time()
        conn = httplib.HTTPConnection('www.example.com')
        conn.request('GET', '/')
        resp = conn.getresponse()
        content = resp.read()
        latency = time.time() - start_timer

        self.custom_timers['Example_Homepage'] = latency

        assert (resp.status == 200), 'Bad HTTP Response'
        assert ('Example Web Page' in content), 'Failed Content Verification'


if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    print trans.custom_timers
