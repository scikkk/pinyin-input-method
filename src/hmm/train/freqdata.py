'''
Author: scikkk 203536673@qq.com
Date: 2022-07-07 00:13:01
LastEditors: scikkk
LastEditTime: 2022-07-10 01:12:42
Description: dataset api
'''

words_path = 'db\\wordfreq.txt'


def wordfreq() -> tuple:
    """ Word frequency data set, iteratively return (word, freq). """
    with open(words_path, 'r', encoding='utf-8') as fr:
        for line in fr:
            word, frequency = line.split()
            yield word, int(frequency)
