#
#  Copyright (c) 2010 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#
#  This file is part of Multi-Mechanize
#
#
#
#  this is a mock plugin.
#  it does nothing but return random custom_timer data.


import random
import time



class Transaction(object):
    def __init__(self):
        self.custom_timers = {}

    def run(self):
        r = random.uniform(1, 2)
        time.sleep(r)
        self.custom_timers['Example_Timer'] = r


if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    print trans.custom_timers
