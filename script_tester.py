#!/usr/bin/env python
#  Copyright (c) 2010 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#  
#  This file is part of Multi-Mechanize


import ConfigParser
import glob
import sys

config = ConfigParser.ConfigParser()
config.read('config.cfg')
script_dir = config.get('global', 'script_directory')
exec 'from %s import *' % script_dir   



def main():
    if sys.platform.startswith('win'):
        sep = '\\'
    else:
        sep = '/'
        
    for file in glob.glob('%s/*.py' % script_dir):
        module_name = file.replace('.py', '').split(sep)[-1]
        if module_name != '__init__':
            print 'testing: %s' % file
            print '  creating Transaction() object'
            trans = eval('%s.Transaction()' % module_name)
            print '  calling run() method'
            trans.run()            
                
    print '\nall tests passed'
            
            

if __name__ == '__main__':
    main()
    