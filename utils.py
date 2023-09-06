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
    @deco_utils.logged(*data.calculate_state(x, y))
    def response():
        return x - y

    return response
