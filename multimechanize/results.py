#!/usr/bin/env python
#
#  Copyright (c) 2010-2012 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#
#  This file is part of Multi-Mechanize | Performance Test Framework
#


import time
from collections import defaultdict
import graph
import reportwriter
import reportwriterxml



def output_results(results_dir, results_file, run_time, rampup, ts_interval, user_group_configs=None, xml_reports=False):
    results = Results(results_dir + results_file, run_time)

    report = reportwriter.Report(results_dir)

    print 'transactions: %i' % results.total_transactions
    print 'errors: %i' % results.total_errors
    print ''
    print 'test start: %s' % results.start_datetime
    print 'test finish: %s' % results.finish_datetime
    print ''

    # write the results in XML
    if xml_reports:
        reportwriterxml.write_jmeter_output(results.resp_stats_list, results_dir)

    report.write_line('<h1>Performance Results Report</h1>')

    report.write_line('<h2>Summary</h2>')

    report.write_line('<div class="summary">')
    report.write_line('<b>transactions:</b> %d<br />' % results.total_transactions)
    report.write_line('<b>errors:</b> %d<br />' % results.total_errors)
    report.write_line('<b>run time:</b> %d secs<br />' % run_time)
    report.write_line('<b>rampup:</b> %d secs<br /><br />' % rampup)
    report.write_line('<b>test start:</b> %s<br />' % results.start_datetime)
    report.write_line('<b>test finish:</b> %s<br /><br />' % results.finish_datetime)
    report.write_line('<b>time-series interval:</b> %s secs<br /><br /><br />' % ts_interval)
    if user_group_configs:
        report.write_line('<b>workload configuration:</b><br /><br />')
        report.write_line('<table>')
        report.write_line('<tr><th>group name</th><th>threads</th><th>script name</th></tr>')
        for user_group_config in user_group_configs:
            report.write_line('<tr><td>%s</td><td>%d</td><td>%s</td></tr>' %
                (user_group_config.name, user_group_config.num_threads, user_group_config.script_file))
        report.write_line('</table>')
    report.write_line('</div>')

    report.write_line('<h2>All Transactions</h2>')

    # all transactions - response times
    trans_timer_points = []  # [elapsed, timervalue]
    trans_timer_vals = []
    for resp_stats in results.resp_stats_list:
        t = (resp_stats.elapsed_time, resp_stats.trans_time)
        trans_timer_points.append(t)
        trans_timer_vals.append(resp_stats.trans_time)
    graph.resp_graph_raw(trans_timer_points, 'All_Transactions_response_times.png', results_dir)

    report.write_line('<h3>Transaction Response Summary (secs)</h3>')
    report.write_line('<table>')
    report.write_line('<tr><th>count</th><th>min</th><th>avg</th><th>80pct</th><th>90pct</th><th>95pct</th><th>max</th><th>stdev</th></tr>')
    report.write_line('<tr><td>%i</td><td>%.3f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td></tr>'  % (
        results.total_transactions,
        min(trans_timer_vals),
        average(trans_timer_vals),
        percentile(trans_timer_vals, 80),
        percentile(trans_timer_vals, 90),
        percentile(trans_timer_vals, 95),
        max(trans_timer_vals),
        standard_dev(trans_timer_vals),
    ))
    report.write_line('</table>')


    # all transactions - interval details
    avg_resptime_points = {}  # {intervalnumber: avg_resptime}
    percentile_80_resptime_points = {}  # {intervalnumber: 80pct_resptime}
    percentile_90_resptime_points = {}  # {intervalnumber: 90pct_resptime}
    interval_secs = ts_interval
    splat_series = split_series(trans_timer_points, interval_secs)
    report.write_line('<h3>Interval Details (secs)</h3>')
    report.write_line('<table>')
    report.write_line('<tr><th>interval</th><th>count</th><th>rate</th><th>min</th><th>avg</th><th>80pct</th><th>90pct</th><th>95pct</th><th>max</th><th>stdev</th></tr>')
    for i, bucket in enumerate(splat_series):
        interval_start = int((i + 1) * interval_secs)
        cnt = len(bucket)

        if cnt == 0:
            report.write_line('<tr><td>%i</td><td>0</td><td>0</td><td>N/A</td><td>N/A</td><td>N/A</td><td>N/A</td><td>N/A</td><td>N/A</td><td>N/A</td></tr>' % (i + 1))
        else:
            rate = cnt / float(interval_secs)
            mn = min(bucket)
            avg = average(bucket)
            pct_80 = percentile(bucket, 80)
            pct_90 = percentile(bucket, 90)
            pct_95 = percentile(bucket, 95)
            mx = max(bucket)
            stdev = standard_dev(bucket)
            report.write_line('<tr><td>%i</td><td>%i</td><td>%.2f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td></tr>' % (i + 1, cnt, rate, mn, avg, pct_80, pct_90, pct_95, mx, stdev))

            avg_resptime_points[interval_start] = avg
            percentile_80_resptime_points[interval_start] = pct_80
            percentile_90_resptime_points[interval_start] = pct_90

    report.write_line('</table>')
    graph.resp_graph(avg_resptime_points, percentile_80_resptime_points, percentile_90_resptime_points, 'All_Transactions_response_times_intervals.png', results_dir)


    report.write_line('<h3>Graphs</h3>')
    report.write_line('<h4>Response Time: %s sec time-series</h4>' % ts_interval)
    report.write_line('<img src="All_Transactions_response_times_intervals.png"></img>')
    report.write_line('<h4>Response Time: raw data (all points)</h4>')
    report.write_line('<img src="All_Transactions_response_times.png"></img>')
    report.write_line('<h4>Throughput: 5 sec time-series</h4>')
    report.write_line('<img src="All_Transactions_throughput.png"></img>')



    # all transactions - throughput
    throughput_points = {}  # {intervalnumber: numberofrequests}
    interval_secs = ts_interval
    splat_series = split_series(trans_timer_points, interval_secs)
    for i, bucket in enumerate(splat_series):
        throughput_points[int((i + 1) * interval_secs)] = (len(bucket) / interval_secs)
    graph.tp_graph(throughput_points, 'All_Transactions_throughput.png', results_dir)



    # custom timers
    for timer_name in sorted(results.uniq_timer_names):
        custom_timer_vals = []
        custom_timer_points = []
        for resp_stats in results.resp_stats_list:
            try:
                val = resp_stats.custom_timers[timer_name]
                custom_timer_points.append((resp_stats.elapsed_time, val))
                custom_timer_vals.append(val)
            except KeyError:
                pass
        graph.resp_graph_raw(custom_timer_points, timer_name + '_response_times.png', results_dir)

        throughput_points = {}  # {intervalnumber: numberofrequests}
        interval_secs = ts_interval
        splat_series = split_series(custom_timer_points, interval_secs)
        for i, bucket in enumerate(splat_series):
            throughput_points[int((i + 1) * interval_secs)] = (len(bucket) / interval_secs)
        graph.tp_graph(throughput_points, timer_name + '_throughput.png', results_dir)

        report.write_line('<hr />')
        report.write_line('<h2>Custom Timer: %s</h2>' % timer_name)

        report.write_line('<h3>Timer Summary (secs)</h3>')

        report.write_line('<table>')
        report.write_line('<tr><th>count</th><th>min</th><th>avg</th><th>80pct</th><th>90pct</th><th>95pct</th><th>max</th><th>stdev</th></tr>')
        report.write_line('<tr><td>%i</td><td>%.3f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td></tr>'  % (
            len(custom_timer_vals),
            min(custom_timer_vals),
            average(custom_timer_vals),
            percentile(custom_timer_vals, 80),
            percentile(custom_timer_vals, 90),
            percentile(custom_timer_vals, 95),
            max(custom_timer_vals),
            standard_dev(custom_timer_vals)
        ))
        report.write_line('</table>')


        # custom timers - interval details
        avg_resptime_points = {}  # {intervalnumber: avg_resptime}
        percentile_80_resptime_points = {}  # {intervalnumber: 80pct_resptime}
        percentile_90_resptime_points = {}  # {intervalnumber: 90pct_resptime}
        interval_secs = ts_interval
        splat_series = split_series(custom_timer_points, interval_secs)
        report.write_line('<h3>Interval Details (secs)</h3>')
        report.write_line('<table>')
        report.write_line('<tr><th>interval</th><th>count</th><th>rate</th><th>min</th><th>avg</th><th>80pct</th><th>90pct</th><th>95pct</th><th>max</th><th>stdev</th></tr>')
        for i, bucket in enumerate(splat_series):
            interval_start = int((i + 1) * interval_secs)
            cnt = len(bucket)

            if cnt == 0:
                report.write_line('<tr><td>%i</td><td>0</td><td>0</td><td>N/A</td><td>N/A</td><td>N/A</td><td>N/A</td><td>N/A</td><td>N/A</td><td>N/A</td></tr>' % (i + 1))
            else:
                rate = cnt / float(interval_secs)
                mn = min(bucket)
                avg = average(bucket)
                pct_80 = percentile(bucket, 80)
                pct_90 = percentile(bucket, 90)
                pct_95 = percentile(bucket, 95)
                mx = max(bucket)
                stdev = standard_dev(bucket)

                report.write_line('<tr><td>%i</td><td>%i</td><td>%.2f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td></tr>' % (i + 1, cnt, rate, mn, avg, pct_80, pct_90, pct_95, mx, stdev))

                avg_resptime_points[interval_start] = avg
                percentile_80_resptime_points[interval_start] = pct_80
                percentile_90_resptime_points[interval_start] = pct_90
        report.write_line('</table>')
        graph.resp_graph(avg_resptime_points, percentile_80_resptime_points, percentile_90_resptime_points, timer_name + '_response_times_intervals.png', results_dir)


        report.write_line('<h3>Graphs</h3>')
        report.write_line('<h4>Response Time: %s sec time-series</h4>' % ts_interval)
        report.write_line('<img src="%s_response_times_intervals.png"></img>' % timer_name)
        report.write_line('<h4>Response Time: raw data (all points)</h4>')
        report.write_line('<img src="%s_response_times.png"></img>' % timer_name)
        report.write_line('<h4>Throughput: %s sec time-series</h4>' % ts_interval)
        report.write_line('<img src="%s_throughput.png"></img>' % timer_name)



    ## user group times
    #for user_group_name in sorted(results.uniq_user_group_names):
    #    ug_timer_vals = []
    #    for resp_stats in results.resp_stats_list:
    #        if resp_stats.user_group_name == user_group_name:
    #            ug_timer_vals.append(resp_stats.trans_time)
    #    print user_group_name
    #    print 'min: %.3f' % min(ug_timer_vals)
    #    print 'avg: %.3f' % average(ug_timer_vals)
    #    print '80pct: %.3f' % percentile(ug_timer_vals, 80)
    #    print '90pct: %.3f' % percentile(ug_timer_vals, 90)
    #    print '95pct: %.3f' % percentile(ug_timer_vals, 95)
    #    print 'max: %.3f' % max(ug_timer_vals)
    #    print ''

    report.write_line('<hr />')
    report.write_closing_html()




class Results(object):
    def __init__(self, results_file_name, run_time):
        self.results_file_name = results_file_name
        self.run_time = run_time
        self.total_transactions = 0
        self.total_errors = 0
        self.uniq_timer_names = set()
        self.uniq_user_group_names = set()

        self.resp_stats_list = self.__parse_file()

        self.epoch_start = self.resp_stats_list[0].epoch_secs
        self.epoch_finish = self.resp_stats_list[-1].epoch_secs
        self.start_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.epoch_start))
        self.finish_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.epoch_finish))



    def __parse_file(self):
        f = open(self.results_file_name, 'rb')
        resp_stats_list = []
        for line in f:
            fields = line.strip().split(',')

            request_num = int(fields[0])
            elapsed_time = float(fields[1])
            epoch_secs = int(fields[2])
            user_group_name = fields[3]
            trans_time = float(fields[4])
            error = fields[5]

            self.uniq_user_group_names.add(user_group_name)

            custom_timers = {}
            timers_string = ''.join(fields[6:]).replace('{', '').replace('}', '')
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

            r = ResponseStats(request_num, elapsed_time, epoch_secs, user_group_name, trans_time, error, custom_timers)

            if elapsed_time < self.run_time:  # drop all times that appear after the last request was sent (incomplete interval)
                resp_stats_list.append(r)

            if error != '':
                self.total_errors += 1

            self.total_transactions += 1

        return resp_stats_list



class ResponseStats(object):
    def __init__(self, request_num, elapsed_time, epoch_secs, user_group_name, trans_time, error, custom_timers):
        self.request_num = request_num
        self.elapsed_time = elapsed_time
        self.epoch_secs = epoch_secs
        self.user_group_name = user_group_name
        self.trans_time = trans_time
        self.error = error
        self.custom_timers = custom_timers



def split_series(points, interval):
    offset = points[0][0]
    maxval = int((points[-1][0] - offset) // interval)
    vals = defaultdict(list)
    for key, value in points:
        vals[(key - offset) // interval].append(value)
    series = [vals[i] for i in xrange(maxval + 1)]
    return series



def average(seq):
    avg = (float(sum(seq)) / len(seq))
    return avg



def standard_dev(seq):
    avg = average(seq)
    sdsq = sum([(i - avg) ** 2 for i in seq])
    try:
        stdev = (sdsq / (len(seq) - 1)) ** .5
    except ZeroDivisionError:
        stdev = 0
    return stdev



def percentile(seq, percentile):
    i = int(len(seq) * (percentile / 100.0))
    seq.sort()
    return seq[i]




if __name__ == '__main__':
    output_results('./', 'results.csv', 60, 30, 10)
