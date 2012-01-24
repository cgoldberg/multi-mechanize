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
        br = mechanize.Browser()
        br.set_handle_robots(False)

        start_timer = time.time()
        resp = br.open('http://www.example.com/')
        resp.read()
        latency = time.time() - start_timer

        self.custom_timers['Example_Homepage'] = latency

        assert (resp.code == 200), 'Bad HTTP Response'
        assert ('Example Web Page' in resp.get_data()), 'Failed Content Verification'


if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    print trans.custom_timers
