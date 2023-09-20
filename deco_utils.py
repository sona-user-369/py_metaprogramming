import inspect
import types
from functools import wraps, partial
import time
import logging
from inspect import signature


def file_deco(func):
    @wraps(func)
    def file_manage(content_limit, filename: str):
        start = time.time()
        if content_limit < 0:
            raise ValueError

        if filename.endswith(('txt', 'docx', 'doc')):
            result = func(content_limit, filename)

        else:
            raise FileNotFoundError
        end = time.time()
        print(func.__name__, end - start)
        return result

    return file_manage


def time_examination(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        start = time.time()
        result = func(*args, *kwargs)
        print('execution time is {0}'.format(time.time() - start))
        return result
    return decorator


def attach_scan(obj, func=None):
    """this function attach another function as an attribute"""
    if func is None:
        return partial(attach_scan, obj)
    setattr(obj, func.__name__, func)
    return func


def logged(level, message=None, name=None):
    def decorator(func):

        log_name = name if name is not None else func.__module__
        msg_changed = False if message is not None else True
        msg = message if message is not None else 'Default message'
        log = logging.getLogger(log_name)

        @wraps(func)
        def scan_action(*args, **kwargs):
            possible_logging = (
                logging.CRITICAL,
                logging.ERROR,
                logging.INFO,
                logging.DEBUG,
                logging.WARNING
            )

            if level not in possible_logging:
                raise Exception('level logging provided is not approved. Please change !')
            if msg_changed:
                print('Try provide a correct message for logging in future !')
            log.log(level, msg)
            return func(*args, **kwargs)

        @attach_scan(scan_action)
        def set_level(new_level):
            nonlocal level
            level = new_level

        @attach_scan(scan_action)
        def set_message(new_message):
            nonlocal msg_changed
            nonlocal msg
            msg = new_message
            msg_changed = False

        return scan_action

    return decorator


def typing_verification(*ty_args, **ty_kwargs):

    def decorator(func):

        if not __debug__:
            return func
        sig = signature(func)
        target_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            return_types = sig.bind(*args, **kwargs).arguments.items()
            for name, value in return_types:
                if name in target_types:
                    if not isinstance(value, target_types[name]):
                        raise TypeError(
                            'Argument {0} must be {1}. Sorry !'.format(name, target_types[name])
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator


class Counter:
    def __init__(self, func):
        wraps(func)(self)
        self.ncall = 0

    def __call__(self, *args, **kwargs):
        self.ncall += 1
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, cls):
        if not instance:
            return self

        return types.MethodType(self, instance)


def provide_extra(func):
    if 'extra' in inspect.getfullargspec(func).args:
        raise Exception('You have provided extra parameter that will not be used')

    @wraps(func)
    def decorator(*args, **kwargs):
        print(inspect.getfullargspec(func).args)

        return func(*args, *kwargs)
    return decorator

