import logging

import deco_utils
import utils


def file_dot():
    utils.write_content_file(40, 'any.txt')
    print(utils.write_content_file.__name__)
    print(utils.write_content_file.__doc__)
    print(utils.write_content_file.__annotations__)
    utils.write_content_file.__wrapped__(-1, 'any.txt')


def calculation(x, y):
    return utils.calculate(x, y)


def extra(x, y, **kwargs):
    return utils.extra_verif(**kwargs)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.WARNING)
    # a = calculation(2, 7)
    # a.set_message('New message')
    # print(a())
    # utils.compare_object(2, 'string')
    # print(utils.facto(90))
    # print(utils.facto.ncall)
    # extra(1, 2)
    # execu = utils.Execution(2)
    # print(execu.initValue)
    s = deco_utils.Store(2, 5.)
    a = deco_utils.Integer()

    print(a)
    # print(s.integer)


