#!/usr/bin/env python
#  Copyright (c) 2010 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#  
#  This file is part of Multi-Mechanize


import sys

try:
    from pylab import *  # Matplotlib for graphing.  Only used on systems that have it installed.
except ImportError, e:
    sys.stderr.write('Matplotlib ImportError: %s\n' % e)
    


# response time graph
def resp_graph(nested_resp_list, dir='./'):
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
    savefig(dir + 'response_time_graph.png') 
    
    

# throughput graph
def tp_graph(throughputs_dict, dir='./'):
    fig = figure(figsize=(8, 3.3))  # image dimensions  
    ax = fig.add_subplot(111)
    ax.set_xlabel('Elapsed Time In Test (secs)', size='x-small')
    ax.set_ylabel('Requests Per Second (count)' , size='x-small')
    ax.grid(True, color='#666666')
    xticks(size='x-small')
    yticks(size='x-small')
    keys = sorted(throughputs_dict.keys())
    vals = [throughputs_dict[key] for key in keys]
    ax.plot(keys, vals, 
        color='red', linestyle='-', linewidth=0.75, marker='o', 
        markeredgecolor='red', markerfacecolor='yellow', markersize=2.0)
    savefig(dir + 'throughput_graph.png') 
    