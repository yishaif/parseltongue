#  Copyright (c) 2022.  Yishai A. Feldman

import inspect

SANITY_CHECKS = True


def find_static_caller(frame_info):
    """
    Return target of call and static class
    """
    # based on https://stackoverflow.com/a/15704609, fixed and improved by using MRO to find locals as well as globals
    frame = frame_info.frame
    code = frame.f_code
    name = code.co_name
    argspec = inspect.getargvalues(frame_info.frame)
    assert len(argspec.args) >= 1, 'precursor() must be called from a method'
    target = argspec.locals[argspec.args[0]]
    for cls in target.__class__.__mro__:
        try:
            assert cls.__dict__[name].__code__ is code
        except Exception:
            pass
        else:  # cls is the class that defines our method
            return target, cls
    raise Exception(f'precursor() could not determine the calling class in {frame_info.filename}:{frame_info.lineno}')


def precursor(*args, **kwargs):
    calling_frame = inspect.getouterframes(inspect.currentframe())[1]
    method = calling_frame.function
    target, calling_class = find_static_caller(calling_frame)
    bases = calling_class.__bases__
    if SANITY_CHECKS:
        try:
            getattr(calling_class, method)
        except AttributeError:
            raise Exception('precursor() must be called from a method')
        if len(bases) != 1:
            raise Exception('precursor() without parameters only allowed in classes that have a single superclass')
    chosen_superclass = bases[0]

    if SANITY_CHECKS:
        if inspect.getouterframes(inspect.currentframe())[1] != calling_frame:
            raise Exception(f'Precursor must be called from original method {method}')
    try:
        super_method = getattr(chosen_superclass, method)
    except AttributeError:
        raise Exception(
            f'Method {method} does not exist in superclass {chosen_superclass.__qualname__}')
    return super_method(target, *args, **kwargs)


def precursor_of(superclass):
    calling_frame = inspect.getouterframes(inspect.currentframe())[1]
    argspec = inspect.getargvalues(calling_frame.frame)
    assert len(argspec.args) >= 1, 'precursor() must be called from a method'
    target = argspec.locals[argspec.args[0]]
    # assert inspect.ismethod(target)
    method = calling_frame.function
    if SANITY_CHECKS:
        try:
            getattr(target.__class__, method)
        except AttributeError:
            raise Exception('precursor_of() must be called from a method')
        if not inspect.isclass(superclass):
            raise Exception(f'Superclass {superclass} must be a class for precursor_of()')
        if superclass not in target.__class__.__mro__:
            raise Exception(
                f'Superclass {superclass} must be a superclass of {target.__class__.__qualname__} for precursor_of()')
    chosen_superclass = superclass

    def call_precursor(*args, **kwargs):
        if SANITY_CHECKS:
            if inspect.getouterframes(inspect.currentframe())[1] != calling_frame:
                raise Exception(f'precursor_of must be called from original method {method}')
        try:
            super_method = getattr(chosen_superclass, method)
        except AttributeError:
            raise Exception(
                f'Method {method} does not exist in superclass {chosen_superclass.__qualname__}')
        return super_method(target, *args, **kwargs)

    return call_precursor
