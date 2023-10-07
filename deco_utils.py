import inspect
import types
from collections import OrderedDict
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


def length_verification(cls):
    original_attribute = cls.__getattribute__

    def verify(self, name):
        if len('{0}'.format(name)) > 5:
            raise Exception('Defined attribute is too long. Please try again !')
        return original_attribute(self, name)

    cls.__getattribute__ = verify
    return cls


class Typed:
    _expected_type = type(None)

    def __init__(self, name=None):
        self._name = name

    def __set__(self, instance, value):
        if not isinstance(value, self._expected_type):
            raise ValueError('Expected type' + str(self._expected_type) + ' got ' + str(type(value)))
        instance.__dict__[self._name] = value


class Integer(Typed):
    _expected_type = int


class Float(Typed):
    _expected_type = float


class OrderedData(type):
    def __new__(cls, clsname, bases, clsdict):
        got_dict = dict(clsdict)
        final_list = []
        for name, value in clsdict.items():
            if isinstance(value, Typed):
                value._name = name
                final_list.append(value)
        got_dict['_result'] = final_list
        return type.__new__(cls, clsname, bases, got_dict)

    @classmethod
    def __prepare__(cls, clsname, bases):
        return OrderedDict()


class Store(metaclass=OrderedData):
    integer = Integer()
    float = Float()

    def __init__(self, x, y):
        self.integer = x
        self.float = y


# for controlling attribute. Let's see !


class ControlAttr(OrderedDict):
    def __init__(self, clsname):
        self.clsname = clsname
        super().__init__()

    def __setitem__(self, name, value):
        if name in self:
            raise TypeError('{} is already defined in attributes of {}'.format(name, self.clsname), )
        super().__setitem__(name, value)


class PatchOrderedDict(type):
    def __new__(cls, clsname, bases, clsidct):
        d = dict()
        d['_order'] = [name for name in clsidct if name[0] != '_']

        return type.__new__(cls, clsname, bases, d)

    @classmethod
    def __prepare__(metacls, clsname, bases):
        return ControlAttr(clsname)


class NeverDuplicate(metaclass=PatchOrderedDict):
    integer = Integer()
    # integer = Float()

# if you want to define an additional arguments


class MyMeta(type):
    """using for defining a class that accept additional arguments"""

    @classmethod
    def __prepare__(metacls, name, bases, add=True, is_for=False):
        super().__prepare__(name, bases)

    def __new__(cls, name , bases, ns, add=True, is_for=False):
        super().__new__(name, bases, ns)

    def __init__(self, name, bases, ns, add=True, is_for=False):
        super().__init__(name, bases, ns)


class MyClassWithAdditional(metaclass=MyMeta, add=True, is_for=False):
    pass




