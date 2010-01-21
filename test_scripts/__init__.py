import glob

testcase_dir = 'test_scripts\\'

for f in glob.glob(testcase_dir + '*.py'):
    if f != '__init__.py':
        f = f.replace(testcase_dir, '')
        f = f.replace('.py', '')
        line = 'import %s' % f
        exec(line)
