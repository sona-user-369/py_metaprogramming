from functools import wraps

import deco_utils
import data
import os


@deco_utils.file_deco
def write_content_file(content_limit: int, filename: str):
    """write content of given file and content limit"""
    with open(filename, 'r') as file:
        text = file.read()
        print('The content of file is {0}'.format(text[:content_limit]))


def calculate(x, y):
    @deco_utils.time_examination
    @deco_utils.logged(*data.calculate_state(x, y))
    def response():
        return x - y

    return response


@deco_utils.typing_verification(int, int)
def compare_object(x, y):
    print('You gonna compare two int')
    return x < y


@deco_utils.Counter
def facto(x):
    if x == 0:
        return 1
    return x * facto(x - 1)


# @deco_utils.provide_extra
# def extra_verif(x, y, extra=None):
#     return x, y, x + y


@deco_utils.length_verification
class Execution:
    initValue = 0

    def __init__(self, value):
        self.initValue = value

    def first_attr(self):
        return 1 > 2 < 3 < 5
