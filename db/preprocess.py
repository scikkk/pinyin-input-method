'''
Author: scikkk 203536673@qq.com
Date: 2022-07-07 09:46:10
LastEditors: scikkk
LastEditTime: 2022-07-11 17:09:20
Description: corpus preprocessing
'''

import os
import re
import jieba
from tqdm import tqdm
chinese = re.compile(
    r'[\d|\u4e00-\u9fa5|\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b|\n]'
)


def gain_new_web():
    for item in os.walk(".\\data\\corpus\\web\\web_zh_2019"):
        dirpath = item[0]
        for filename in item[2]:
            with open(os.path.join(dirpath, filename), 'r', encoding='utf-8', errors='ignore') as fr:
                new_file = os.path.join(
                    "data", "corpus", "web", "web_pure_zh", filename[-10:-5])
                with open(new_file, 'w', encoding='utf-8') as fw:
                    for line in tqdm(fr.readlines()):
                        for w in chinese.findall(line):
                            fw.write(w)


def gain_new_wiki():
    for item in tqdm(os.walk(".\\data\\corpus\\wiki\\wiki_zh_2019")):
        dirpath = item[0]
        for filename in tqdm(item[2]):
            with open(os.path.join(dirpath, filename), 'r', encoding='utf-8', errors='ignore') as fr:
                new_file = os.path.join(
                    "data", "corpus", "wiki", "wiki_pure_zh", dirpath[-2:]+filename[-2:])
                with open(new_file, 'w', encoding='utf-8') as fw:
                    txt = fr.read()
                    for w in chinese.findall(txt):
                        fw.write(w)


def contact_wiki():
    with open(".\\data\\corpus\\wiki.txt", 'w', encoding='utf-8') as fw:
        for item in tqdm(os.walk(".\\data\\corpus\\wiki\\wiki_pure_zh")):
            dirpath = item[0]
            for filename in tqdm(item[2]):
                with open(os.path.join(dirpath, filename), 'r', encoding='utf-8', errors='ignore') as fr:

                    for line in fr.readlines():
                        fw.write(line)


def contact_web():
    with open(".\\data\\corpus\\web.txt", 'w', encoding='utf-8') as fw:
        for item in os.walk(".\\data\\corpus\\web\\web_pure_zh"):
            dirpath = item[0]
            for filename in item[2]:
                with open(os.path.join(dirpath, filename), 'r', encoding='utf-8', errors='ignore') as fr:
                    for line in tqdm(fr.readlines()):
                        fw.write(line)


def gain_wordfreq():
    wordfreq = {}
    with open(".\\data\\corpus\\wiki.txt", 'r', encoding='utf-8') as fr:
        for line in fr.readlines():
            if len(line) == 0:
                continue
            for w in jieba.cut(line):
                wordfreq[w] = wordfreq.get(w, 0) + 1
    with open(".\\data\\corpus\\web.txt", 'r', encoding='utf-8') as fr:
        for line in fr.readlines():
            if len(line) == 0:
                continue
            for w in jieba.cut(line):
                wordfreq[w] = wordfreq.get(w, 0) + 1
    with open(".\\data\\wordfreq.txt", 'w', encoding='utf-8') as fw:
        for word, freq in sorted(wordfreq.items(), key=lambda x: x[1], reverse=True):
            if '\u4e00' <= word <= '\u9fa5':
                fw.write(''.join([word, ' ', str(freq), '\n']))


if __name__ == '__main__':
    gain_new_web()
    contact_web()
    gain_new_wiki()
    contact_wiki()
    gain_wordfreq()
