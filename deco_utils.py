from functools import wraps, partial
import time
import logging


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


def attach_scan(obj, func=None):
    if func is None:
        return partial(attach_scan, obj)
    setattr(obj, func.__name__, func)
    return func


def logged(level, name=None, message=None):
    def decorator(func):

        log_name = name if name is not None else func.__name__
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
