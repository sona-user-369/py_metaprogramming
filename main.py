import logging

import utils


def file_dot():
    utils.write_content_file(40, 'any.txt')
    print(utils.write_content_file.__name__)
    print(utils.write_content_file.__doc__)
    print(utils.write_content_file.__annotations__)
    utils.write_content_file.__wrapped__(-1, 'any.txt')


def calculation(x, y):
    return utils.calculate(x, y)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.WARNING)
    # a = calculation(2, 7)
    # a.set_message('New message')
    # print(a())
    utils.compare_object(2, 'string')
