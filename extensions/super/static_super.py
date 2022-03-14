#  Copyright (c) 2022.  Yishai A. Feldman
import inspect
from functools import partial

from extensions.super.precursor import find_static_caller

SANITY_CHECKS = True


class SuperCaller:
    def __init__(self, obj, cls):
        self.obj = obj
        self.cls = cls

    def __getattr__(self, method):
        try:
            return partial(getattr(self.cls, method), self.obj)
        except AttributeError:
            raise Exception(
                f'Method {method} does not exist in superclass {self.cls.__qualname__}')


def static_super():
    calling_frame = inspect.getouterframes(inspect.currentframe())[1]
    target, calling_class = find_static_caller(calling_frame)
    bases = calling_class.__bases__
    if SANITY_CHECKS:
        method = calling_frame.function
        try:
            getattr(calling_class, method)
        except AttributeError:
            raise Exception('static_super() must be called from a method')
        if len(bases) != 1:
            raise Exception('static_super() without parameters only allowed in classes that have a single superclass')
    chosen_superclass = bases[0]
    return SuperCaller(target, chosen_superclass)


def static_super_of(superclass):
    calling_frame = inspect.getouterframes(inspect.currentframe())[1]
    target, calling_class = find_static_caller(calling_frame)
    if SANITY_CHECKS:
        method = calling_frame.function
        try:
            getattr(target.__class__, method)
        except AttributeError:
            raise Exception('static_super_of() must be called from a method')
        if not inspect.isclass(superclass):
            raise Exception(f'Superclass {superclass} must be a class for static_super_of()')
        if superclass not in calling_class.__mro__[1:]:
            raise Exception(
                f'Superclass {superclass} must be a superclass of {target.__class__.__qualname__} for static_super_of()')
    chosen_superclass = superclass
    return SuperCaller(target, chosen_superclass)
