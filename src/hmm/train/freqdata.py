'''
Description: data interface
Author: SciK
Date: 2022-07-07 00:13:01
LastEditors: SciK
LastEditTime: 2022-07-10 00:23:24
FilePath: \mypinyin\src\hmm\train\freqdata.py
'''
words_path = '.\\data\\wordfreq.txt'


def wordfreq() -> tuple:
    """ Word frequency data set, iteratively return (word, freq). """
    with open(words_path, 'r', encoding='utf-8') as fr:
        for line in fr:
            word, frequency = line.split()
            yield word, int(frequency)
