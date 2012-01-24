#!/usr/bin/env python
#
#  Copyright (c) 2010-2012 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#
#  This file is part of Multi-Mechanize | Performance Test Framework
#


class Report(object):
    def __init__(self, results_dir):
        self.results_dir = results_dir
        self.fn = results_dir + 'results.html'
        self.write_head_html()


    def write_line(self, line):
        with open(self.fn, 'a') as f:
            f.write('%s\n' % line)


    def write_head_html(self):
        with open(self.fn, 'w') as f:
            f.write("""\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
    <title>Multi-Mechanize - Results</title>
    <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
    <meta http-equiv="Content-Language" content="en" />
    <style type="text/css">
        body {
            background-color: #FFFFFF;
            color: #000000;
            font-family: Verdana, sans-serif;
            font-size: 11px;
            padding: 5px;
        }
        h1 {
            font-size: 16px;
            background: #FF9933;
            margin-bottom: 0;
            padding-left: 5px;
            padding-top: 2px;
        }
        h2 {
            font-size: 13px;
            background: #C0C0C0;
            padding-left: 5px;
            margin-top: 2em;
            margin-bottom: .75em;
        }
        h3 {
            font-size: 12px;
            background: #EEEEEE;
            padding-left: 5px;
            margin-bottom: 0.5em;
        }
        h4 {
            font-size: 11px;
            padding-left: 20px;
            margin-bottom: 0;
        }
        p {
            margin: 0;
            padding: 0;
        }
        table {
            margin-left: 10px;
        }
        td {
            text-align: right;
            color: #000000;
            background: #FFFFFF;
            padding-left: 10px;
            padding-right: 10px;
            padding-bottom: 0;
        }
        th {
            text-align: center;
            padding-right: 10px;
            padding-left: 10px;
            color: #000000;
            background: #FFFFFF;
        }
        div.summary {
            padding-left: 20px;
        }
    </style>
</head>
<body>
""")


    def write_closing_html(self):
        with open(self.fn, 'a') as f:
            f.write("""\
</body>
</html>
""")





