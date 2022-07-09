'''
Author: scikkk 203536673@qq.com
Date: 2022-07-07 14:01:55
LastEditors: scikkk
LastEditTime: 2022-07-10 01:05:53
Description: some general tool functions
'''

import json


def load_json(filename):
    """
    Load a json file to a Python object.

    :param filename: the file to be loaded
    """
    with open(filename, 'r', encoding='utf-8') as fr:
        return json.load(fr)


def save_json(obj, filename) -> None:
    """
    Write a Python object into json files.

    :param obj: the contents to be saved
    :param filename: the name of the new json file
    """
    with open(filename, mode='w', encoding='utf-8') as fw:
        data = json.dumps(obj, indent=4, sort_keys=True, ensure_ascii=False)
        fw.write(data)
