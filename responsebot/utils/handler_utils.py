"""
Utilities for handling tweet handlers
"""
from __future__ import absolute_import
import os
import pkgutil

import sys
from importlib import import_module

from responsebot.handlers import registered_handlers


def discover_handler_classes(handlers_package):
    """
    Looks for handler classes within handler path module.

    Currently it's not looking deep into nested module.

    :param handlers_package: module path to handlers
    :type handlers_package: string
    :return: list of handler classes
    """
    if handlers_package is None:
        return

    # Add working directory into PYTHONPATH to import developer packages
    sys.path.insert(0, os.getcwd())

    package = import_module(handlers_package)

    # Continue searching for module if package is not a module
    if hasattr(package, '__path__'):
        for _, modname, _ in pkgutil.iter_modules(package.__path__):
            import_module('{package}.{module}'.format(package=package.__name__, module=modname))

    return registered_handlers
