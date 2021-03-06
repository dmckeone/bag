# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from importlib import import_module
from types import ModuleType
# Module version, as defined in PEP-0396.
__version__ = '0.4.5'

_boolean_states = {'1': True, 'yes': True, 'true': True, 'on': True,
                   '0': False, 'no': False, 'false': False, 'off': False}


def asbool(thing):
    if thing is None or isinstance(thing, (bool, int)):
        return thing
    val = _boolean_states.get(thing.lower())
    if val is None:
        raise ValueError('Not a boolean: "%s"' % thing)
    return val


def resolve(resource_spec):
    if isinstance(resource_spec, ModuleType):  # arg is a python module
        return resource_spec
    module, var = resource_spec.split(':')  # arg is assumed to be a string
    module = import_module(module)
    return getattr(module, var)


def first(iterable):
    for o in iterable:
        return o
