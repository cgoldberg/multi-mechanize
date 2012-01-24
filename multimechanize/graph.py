#!/usr/bin/env python
#
#  Copyright (c) 2010-2012 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#
#  This file is part of Multi-Mechanize | Performance Test Framework
#


import sys

try:
    import matplotlib
    matplotlib.use('Agg')  # use a non-GUI backend
    from pylab import *
except ImportError:
    print 'ERROR: can not import Matplotlib. install Matplotlib to generate graphs'



# response time graph for raw data
def resp_graph_raw(nested_resp_list, image_name, dir='./'):
    fig = figure(figsize=(8, 3.3))  # image dimensions
    ax = fig.add_subplot(111)
    ax.set_xlabel('Elapsed Time In Test (secs)', size='x-small')
    ax.set_ylabel('Response Time (secs)' , size='x-small')
    ax.grid(True, color='#666666')
    xticks(size='x-small')
    yticks(size='x-small')
    x_seq = [item[0] for item in nested_resp_list]
    y_seq = [item[1] for item in nested_resp_list]
    ax.plot(x_seq, y_seq,
        color='blue', linestyle='-', linewidth=0.0, marker='o',
        markeredgecolor='blue', markerfacecolor='blue', markersize=2.0)
    ax.plot([0.0,], [0.0,], linewidth=0.0, markersize=0.0)
    savefig(dir + image_name)



# response time graph for bucketed data
def resp_graph(avg_resptime_points_dict, percentile_80_resptime_points_dict, percentile_90_resptime_points_dict, image_name, dir='./'):
    fig = figure(figsize=(8, 3.3))  # image dimensions
    ax = fig.add_subplot(111)
    ax.set_xlabel('Elapsed Time In Test (secs)', size='x-small')
    ax.set_ylabel('Response Time (secs)' , size='x-small')
    ax.grid(True, color='#666666')
    xticks(size='x-small')
    yticks(size='x-small')

    x_seq = sorted(avg_resptime_points_dict.keys())
    y_seq = [avg_resptime_points_dict[x] for x in x_seq]
    ax.plot(x_seq, y_seq,
        color='green', linestyle='-', linewidth=0.75, marker='o',
        markeredgecolor='green', markerfacecolor='yellow', markersize=2.0)

    x_seq = sorted(percentile_80_resptime_points_dict.keys())
    y_seq = [percentile_80_resptime_points_dict[x] for x in x_seq]
    ax.plot(x_seq, y_seq,
        color='orange', linestyle='-', linewidth=0.75, marker='o',
        markeredgecolor='orange', markerfacecolor='yellow', markersize=2.0)

    x_seq = sorted(percentile_90_resptime_points_dict.keys())
    y_seq = [percentile_90_resptime_points_dict[x] for x in x_seq]
    ax.plot(x_seq, y_seq,
        color='purple', linestyle='-', linewidth=0.75, marker='o',
        markeredgecolor='purple', markerfacecolor='yellow', markersize=2.0)

    ax.plot([0.0,], [0.0,], linewidth=0.0, markersize=0.0)

    legend_lines = reversed(ax.get_lines()[:3])
    ax.legend(
            legend_lines,
            ('90pct', '80pct', 'Avg'),
            loc='best',
            handlelength=1,
            borderpad=1,
            prop=matplotlib.font_manager.FontProperties(size='xx-small')
            )

    savefig(dir + image_name)



# throughput graph
def tp_graph(throughputs_dict, image_name, dir='./'):
    fig = figure(figsize=(8, 3.3))  # image dimensions
    ax = fig.add_subplot(111)
    ax.set_xlabel('Elapsed Time In Test (secs)', size='x-small')
    ax.set_ylabel('Transactions Per Second (count)' , size='x-small')
    ax.grid(True, color='#666666')
    xticks(size='x-small')
    yticks(size='x-small')
    x_seq = sorted(throughputs_dict.keys())
    y_seq = [throughputs_dict[x] for x in x_seq]
    ax.plot(x_seq, y_seq,
        color='red', linestyle='-', linewidth=0.75, marker='o',
        markeredgecolor='red', markerfacecolor='yellow', markersize=2.0)
    ax.plot([0.0,], [0.0,], linewidth=0.0, markersize=0.0)
    savefig(dir + image_name)
