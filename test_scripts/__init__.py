#!/usr/bin/env python
#
#  Copyright (c) 2010 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#  
#  This file is part of Multi-Mechanize
#
#
#  keep this file in your script_directory


import ConfigParser
import glob
import sys



config = ConfigParser.ConfigParser()
config.read('config.cfg')
script_dir = config.get('global', 'script_directory')

if sys.platform.startswith('win'):
    sep = '\\'
else:
    sep = '/'

dir = script_dir + sep

for f in glob.glob( '%s*.py' % dir):
    if f != '__init__.py':
        f = f.replace(dir, '')
        f = f.replace('.py', '')
        line = 'import %s' % f
        exec(line)
