import logging


def calculate_state(x, y):
    if x < y:
        return logging.ERROR
    elif x == y:
        return logging.WARNING
    return logging.INFO
