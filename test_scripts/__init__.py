

import glob
import sys



TESTCASE_DIR = 'test_scripts'

if sys.platform.startswith('win'):
    sep = '\\'
else:
    sep = '/'

dir = TESTCASE_DIR + sep

for f in glob.glob( '%s*.py' % dir):
    if f != '__init__.py':
        f = f.replace(dir, '')
        f = f.replace('.py', '')
        line = 'import %s' % f
        exec(line)
