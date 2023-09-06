import utils


if __name__ == '__main__':
    utils.write_content_file(40, 'any.txt')
    print(utils.write_content_file.__name__)
    print(utils.write_content_file.__doc__)
    print(utils.write_content_file.__annotations__)
    utils.write_content_file.__wrapped__(-1, 'any.txt')
