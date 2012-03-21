#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
REPLACE: multi-mechanize exec()/eval() magic with real imports.
"""

import glob
import inspect
import os.path
import sys

class InvalidScriptError(StandardError):
    """
    Should be raised when a Script does not confirm to required interface.

    SCRIPT INTERFACE:
      - Transaction class exists.
      - Transaction.run() method exists.
    """

class ScriptValidator(object):
    """
    Utility class to ensure that scripts are valid and conforms to conventions.
    """

    @staticmethod
    def check_module_invalid(module):
        """
        Check if a script module is invalid and does not comply w/ conventions
        :returns: Problem as string, if any is found.
        :returns: None, if no problems are detected.
        """
        transaction_class = getattr(module, "Transaction", None)
        if not transaction_class:
            return "{module}.Transaction class missing".format(
                        module=module.__name__)
        run_method = getattr(transaction_class, "run", None)
        if not run_method:
            return "{module}.Transaction.run() method is missing".format(
                        module=module.__name__)
        if not callable(run_method):
            return "{module}.Transaction.run() method is not callable".format(
                        module=module.__name__)
        # -- EVERYTHING CHECKED: No problems detected.
        return None

    @classmethod
    def ensure_module_valid(cls, module):
        """
        Ensures that a script module is valid.
        :raises: InvalidScriptError, if any convention is violated.
        """
        problem = cls.check_module_invalid(module)
        if problem:
            raise InvalidScriptError, problem

class ScriptLoader(object):
    """Utility class to load scripts as python modules."""

    @staticmethod
    def load(path):
        """
        Load a script by using a path.
        :returns: Loaded script module-
        :raise: ImportError, when script module cannot be loaded.
        """
        module_name    = inspect.getmodulename(path).replace("-", "_")
        module_dirname = os.path.dirname(path)
        if not module_dirname:
            module_dirname = os.curdir
        if not os.path.exists(path):
            raise ImportError("File not found: %s" % path)
        module_dirnamea = os.path.abspath(module_dirname)
        if not sys.path or module_dirnamea != sys.path[0]:
            sys.path.insert(0, module_dirnamea)

        module = None
        try:
            module = __import__(module_name)
            # module.__name__ = module_name
            # module.__file__ = path
        except ImportError, e:
            print "IMPORT-ERROR: %s (file=%s, curdir=%s)" % \
                  (module_name, path, os.getcwd())
            sys.stderr.write("Cannot import: %s\n" % e)
            for index, searchpath in enumerate(sys.path):
                print "  %2s.  %s" % (index, searchpath)
            raise
        return module

    @classmethod
    def load_all(cls, scripts_path, validate=False):
        """
        Load all python scripts in a path.
        :returns: Loaded script modules as dictionary.
        """
        if not os.path.isdir(scripts_path):
            return None
        pattern = "%s/*.py" % scripts_path
        modules = dict()
        for script in glob.glob(pattern):  #< import all scripts as modules
            basename = os.path.basename(script)
            if basename.startswith("_"):
                continue    #< SKIP: __init__.py, ...
            module = cls.load(os.path.normpath(script))
            modules[module.__name__] = module
            if validate:
                ScriptValidator.ensure_module_valid(module)
        return modules

