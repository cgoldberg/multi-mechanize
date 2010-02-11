#!/usr/bin/env python
#
#  Copyright (c) 2010 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#  
#  This file is part of Multi-Mechanize


import sys


if sys.version_info >= (3,):
    print 'sorry, no py3k support yet' 
elif sys.version_info < (2, 6):
    print 'incompatible python version detected: %s.  Minimum version supported is 2.6' % repr(sys.version_info)
else:
    print 'compatible python version detected: %s' % repr(sys.version_info)

try:
    import multiprocessing
    print 'imported Multiprocessing succesfully'
except ImportError:
    print 'can not import Multiprocessing'
    
try:
    import mechanize
    print 'imported Mechanize succesfully'
except ImportError:
    print 'can not import Mechanize'

try:
    import pylab
    print 'imported Matplotlib succesfully'
except ImportError:
    print 'can not import Matplotlib'
    
    
