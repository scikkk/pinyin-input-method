'''
Author: scikkk 203536673@qq.com
Date: 2022-07-07 02:11:23
LastEditors: scikkk
LastEditTime: 2022-07-11 17:50:46
Description: split Pinyin

拼音数据来源: https://blog.csdn.net/Likianta/article/details/87871183
划分算法参考: https://www.jianshu.com/p/3e83129d70e2
'''

from conf.config import CUT_CONFIG


pytable = []
# load Pinyin table from file
with open('db\\pinyin.txt', 'r', encoding='utf-8') as f:
    pytable = list(s for s in f.read().split('\n'))
first_pytable = ('b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
                 'n', 'p', 'q', 'r', 's', 't', 'w', 'x', 'y', 'z')
zcs_pytable = ('zh', 'sh', 'ch')
if CUT_CONFIG['has_first']:
    pytable += first_pytable
if CUT_CONFIG['has_zcs']:
    pytable += zcs_pytable

# load correct dict from file
correct_dict = {}
with open('db\\correct.txt', 'r', encoding='utf-8') as f:
    for line in f:
        wrong, right = line.replace('\n', '').split('->')
        correct_dict[wrong] = right


def correct(pinyin: str) -> str:
    """ Correct Pinyin according to the correct_dict. """
    for wrong, right in correct_dict.items():
        pinyin = pinyin.replace(wrong, right)
    return pinyin


def pysplit(pinyin: str, pinyin_table=pytable) -> tuple:
    """
    Split pinyin by calling recursion_split.

    :param pinyin: the Pinyin sequence to be split
    :param pinyin_table: Pinyin table
    :return: a tuple of all possible split results
    """
    res = []
    correct_res = []
    recursion_split(res, pinyin, pinyin_table)
    if CUT_CONFIG['has_correct']:
        correct_pinyin = correct(pinyin)
        if correct_pinyin != pinyin:
            recursion_split(correct_res, correct_pinyin, pinyin_table)
    return tuple(correct_res+res)


def recursion_split(res, pinyin, pinyin_table, pre_pinyin_list=[]) -> None:
    """
    Split the sequence recursively.

    :param res: the list to save the split result
    :param pinyin: the Pinyin sequence to be split
    :param pinyin_table: Pinyin table
    :param pre_pinyin_list: pass previous result to next function call
    """
    pinyin_len = len(pinyin)
    for i in range(0, pinyin_len + 1):
        pinyin_list = [x for x in pre_pinyin_list]  # deepcopy
        if pinyin[0:i] in pinyin_table:
            if i == pinyin_len:
                pinyin_list.append(pinyin[0:i])
                res.append(tuple(pinyin_list))
            else:
                pinyin_list.append(pinyin[0:i])
                recursion_split(res, pinyin[i:], pinyin_table, pinyin_list)


if __name__ == '__main__':
    for test in ['xiao', 'wxhn', 'woxihuanni', 'xkong', 'woshyiger', 'maio']:
        print(pysplit(test))
        print('----------------------')
