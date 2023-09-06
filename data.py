import logging


def calculate_state(x, y):
    if x < y:
        return logging.ERROR, 'x value must be greater than y value'
    elif x == y:
        return logging.WARNING, '0 return. In case you will use this value, 0 is not recommended'
    return logging.INFO, 'Everything OK'
