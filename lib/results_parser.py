#!/usr/bin/env python
#  Copyright (c) 2010 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#  
#  This file is part of Multi-Mechanize



from collections import defaultdict



def main():
    results = Results('results.csv')
    
    print 'total transactions: %i' % results.total_transactions
    print ''
    
    # custom timers
    for timer_name in sorted(results.uniq_timer_names):
        timer_vals = []
        for resp_stats in results.resp_stats_list:
            timer_vals.append(resp_stats.custom_timers[timer_name])
        print timer_name
        print 'min: %.3f' % min(timer_vals)
        print 'avg: %.3f' % avg(timer_vals)
        print '80pct: %.3f' % percentile(timer_vals, 80)
        print '90pct: %.3f' % percentile(timer_vals, 90)
        print '95pct: %.3f' % percentile(timer_vals, 95)
        print 'max: %.3f' % max(timer_vals)
        print ''
        
   
    


class Results(object):
    def __init__(self, results_file_name):
        self.results_file_name = results_file_name
        self.total_transactions = 0
        self.uniq_timer_names = set()
        
        self.resp_stats_list = self.__parse_file()
        
        
    def __parse_file(self):
        f = open(self.results_file_name, 'rb')
        resp_stats_list = []
        for line in f:
            fields = line.strip().split(',')
            request_num = int(fields[0])
            elapsed_time = float(fields[1])
            user_group_name = fields[2]
            trans_time = float(fields[3])
            status = fields[4]
            bytes_received = int(fields[5])
            error = fields[6]
            
            custom_timers = {}
            timers_string = ''.join(fields[7:]).replace('{', '').replace('}', '')
            splat = timers_string.split("'")[1:]
            timers = []
            vals = []
            for x in splat:
                if ':' in x:
                    x = float(x.replace(': ', ''))
                    vals.append(x)
                else:
                    timers.append(x)
                    self.uniq_timer_names.add(x)
            for timer, val in zip(timers, vals):
                custom_timers[timer] = val
            
            r = ResponseStats(request_num, elapsed_time, user_group_name, trans_time, status, bytes_received, error, custom_timers)
            resp_stats_list.append(r)
            self.total_transactions += 1
            
        return resp_stats_list    
   

class ResponseStats(object):
    def __init__(self, request_num, elapsed_time, user_group_name, trans_time, status, bytes_received, error, custom_timers):
        self.request_num = request_num
        self.elapsed_time = elapsed_time
        self.user_group_name = user_group_name
        self.trans_time = trans_time
        self.status = status
        self.bytes_received = bytes_received
        self.error = error
        self.custom_timers = custom_timers
        

#def split_series(points, interval):
#    offset = points[0][0]
#    maxval = int((points[-1][0] - offset) // interval)
#    vals = defaultdict(list)
#    for key, value in points:
#        vals[(key - offset) // interval].append(value)
#    series = [vals[i] for i in xrange(maxval + 1)]
#    return series


def avg(seq):
    return float(sum(seq) / len(seq)) 

def percentile(seq, percentile):
    i = int(len(seq) * (percentile / 100.0))
    seq.sort()
    return seq[i]


if __name__ == '__main__':
    main()
