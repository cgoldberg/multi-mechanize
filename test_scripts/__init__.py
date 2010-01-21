import glob
import sys

TESTCASE_DIR = 'test_scripts'

if sys.platform.startswith('win'):
    sep = '\\'
else:
    sep = '/'
    
for f in glob.glob(TESTCASE_DIR + sep + '*.py'):
    if f != '__init__.py':
        f = f.replace(TESTCASE_DIR + sep, '')
        f = f.replace('.py', '')
        line = 'import %s' % f
        exec(line)
