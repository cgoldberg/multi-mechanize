#!/usr/bin/env python
#
#  Copyright (c) 2010 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#  
#  This file is part of Multi-Mechanize
#
#
#  keep this file in your test-scripts directory


import glob
import os
import sys


project_path = sys.path.pop()

for f in glob.glob( '%s/*.py' % project_path):
    if '__init__.py' not in f:
        f = f.replace(project_path, '')
        f = f.replace(os.sep, '')
        f = f.replace('.py', '')
        line = 'import %s' % f
        exec(line)
