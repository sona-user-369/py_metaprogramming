import deco_utils
import os


@deco_utils.file_deco
def write_content_file(content_limit: int, filename: str):
    """write content of given file and content limit"""
    with open(filename, 'r') as file:
        text = file.read()
        print('The content of file is {0}'.format(text[:content_limit]))
