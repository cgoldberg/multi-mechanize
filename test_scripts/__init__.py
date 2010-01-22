

import glob
import sys



script_dir = 'test_scripts'

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
