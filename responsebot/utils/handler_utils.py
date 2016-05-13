# Copyright 2016 Invisible Institute
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Utilities for handling tweet handlers
"""
from __future__ import absolute_import

import inspect
import os
import pkgutil

import sys
from importlib import import_module

from responsebot.handlers.base import BaseTweetHandler


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

    try:
        package = import_module(handlers_package)
        handler_classes = [class_obj for _, class_obj in inspect.getmembers(package, is_handler_class)]

        # Continue searching for module if package is not a module
        if hasattr(package, '__path__'):
            for _, modname, _ in pkgutil.iter_modules(package.__path__):
                module = import_module('{package}.{module}'.format(package=package.__name__, module=modname))

                handler_classes += [class_obj for _, class_obj in inspect.getmembers(module, is_handler_class)]
    except ImportError:
        raise

    return handler_classes


def is_handler_class(class_obj):
    """
    Check if class_obj extend from BaseTweetHandler.

    :param class_obj: class obj that need to check
    :type class_obj: Class
    :return: bool
    """
    return inspect.isclass(class_obj) and class_obj is not BaseTweetHandler and issubclass(class_obj, BaseTweetHandler)
