'''
Author: scikkk 203536673@qq.com
Date: 2022-07-08 16:28:16
LastEditors: scikkk
LastEditTime: 2022-07-21 11:41:11
Description: Generate parameters of HMM
'''

from math import log
import freqdata
from tqdm import tqdm
import pypinyin


from util.tools import save_json, load_json
from conf.config import TRAIN_CONFIG, MODEL_PATH


def compute_start():
    """    
    Generate the start probability matrix π.    

    start_log_prob[Chinese character] = Logarithmic probability
    """
    start_cnt = {}
    tot = 0
    for word, freq in tqdm(freqdata.wordfreq(), total=3521036):
        tot += freq
        start_cnt[word[0]] = start_cnt.get(word[0], 0) + freq
    start_log_prob = {}
    for ch in start_cnt.keys():
        start_log_prob[ch] = log(start_cnt.get(ch) / tot)
    save_json(start_log_prob, MODEL_PATH['start'])


def compute_emission():
    """    
    Generate the emission probability matrix B.   

    emission_log_prob[Chinese character] = {Pinyin_1: Prob_1, ...}
    """
    emission_py_cnt = {}

    def add_to_cnt(py, ch, num):
        emission_py_cnt[ch][py] = emission_py_cnt[ch].get(
            py, 0) + num * freq // cnt_of_pinyins
    for word, freq in tqdm(freqdata.wordfreq(), total=3521036):
        all_pinyins = pypinyin.pinyin(word, style=pypinyin.NORMAL)
        for ch, pinyins in zip(word, all_pinyins):
            cnt_of_pinyins = len(pinyins)
            if ch not in emission_py_cnt:
                emission_py_cnt[ch] = {}
            for py in pinyins:

                if len(py) >= 1:
                    add_to_cnt(py, ch, TRAIN_CONFIG['intact_weight'])
                if len(py) >= 2:
                    if py[:2] in ('zh', 'ch', 'sh'):
                        add_to_cnt(py[:2], ch, TRAIN_CONFIG['zcs_weight'])
                    add_to_cnt(py[0], ch, TRAIN_CONFIG['first_weight'])
    emission_log_prob = {}
    for ch, pinyin_cnt in emission_py_cnt.items():
        tot = sum(pinyin_cnt.values())
        emission_log_prob[ch] = {}
        for pinyin in pinyin_cnt.keys():
            emission_log_prob[ch][pinyin] = log(pinyin_cnt[pinyin] / tot)
    save_json(emission_log_prob, MODEL_PATH['emission'])


def compute_transition():
    """    
    Generate the transition probability matrix A.   

    transition_log_prob[Previous Chinese character] = {Post Chinese character, Logarithmic probability}
    """
    transition_ch_cnt = {}
    for word, freq in tqdm(freqdata.wordfreq(), total=3521036):
        for i in range(len(word) - 1):
            pre, post = word[i], word[i+1]
            if not transition_ch_cnt.get(pre, None):
                transition_ch_cnt[pre] = {}
            transition_ch_cnt[pre][post] = \
                transition_ch_cnt[pre].get(post, 0) + freq
    transition_log_prob = {}
    for pre, post_ch_cnt in transition_ch_cnt.items():
        tot = sum(post_ch_cnt.values())
        transition_log_prob[pre] = {}
        for post in post_ch_cnt.keys():
            transition_log_prob[pre][post] = log(post_ch_cnt[post] / tot)
    save_json(transition_log_prob, MODEL_PATH['transition'])


def compute_reversed_emission(emission_log_prob):
    """    
    Generate the reversed emission probability matrix.    

    reversed_emission_log_prob[Pinyin] = {Character_1: Prob_1, ...}
    """
    reversed_emission_log_prob = {}
    for char in tqdm(emission_log_prob):
        for pinyin, prob in emission_log_prob[char].items():
            if pinyin not in reversed_emission_log_prob:
                reversed_emission_log_prob[pinyin] = {}
            reversed_emission_log_prob[pinyin][char] = prob
    save_json(reversed_emission_log_prob, MODEL_PATH['reversed_emission'])


def compute_reversed_transition():
    """    
    Generate the reversed transition probability matrix.    

    reversed_transition_log_prob[Post Chinese character] = {Previous Chinese character, Logarithmic probability}
    """
    reversed_transition_ch_cnt = {}
    for word, freq in tqdm(freqdata.wordfreq(), total=3521036):
        for i in range(len(word) - 1):
            pre, post = word[i], word[i+1]
            if not reversed_transition_ch_cnt.get(post, None):
                reversed_transition_ch_cnt[post] = {}
            reversed_transition_ch_cnt[post][pre] = \
                reversed_transition_ch_cnt[post].get(pre, 0) + freq

    reversed_transition_log_prob = {}
    for post, pre_ch_cnt in reversed_transition_ch_cnt.items():
        tot = sum(pre_ch_cnt.values())
        reversed_transition_log_prob[post] = {}
        for pre in pre_ch_cnt.keys():
            reversed_transition_log_prob[post][pre] = log(
                pre_ch_cnt[pre] / tot)

    save_json(reversed_transition_log_prob, MODEL_PATH['reversed_transition'])


def compute_nxt(transition_matrix, emission_matrix):
    """    
    Generate the matrix to find the most likely next Chinese character given a Pinyin.  

    compute_nxt[Previous Chinese character][Pinyin] = (most likely Post Chinese character, Prob)
    """
    compute_nxt = {}
    for previous in tqdm(transition_matrix):
        compute_nxt[previous] = {}
        for behind in transition_matrix[previous]:
            for pinyin in emission_matrix[behind]:
                prob = transition_matrix[previous][behind] + \
                    emission_matrix[behind][pinyin]
                if pinyin not in compute_nxt[previous]:
                    compute_nxt[previous][pinyin] = (
                        behind, prob)
                elif prob > compute_nxt[previous][pinyin][1]:
                    compute_nxt[previous][pinyin] = (
                        behind, prob)
    save_json(compute_nxt, MODEL_PATH['compute_nxt'])


if __name__ == '__main__':
    print('Computing start probability...')
    compute_start()

    print('Computing emission probability...')
    compute_emission()

    print('Computing transition probability...')
    compute_transition()

    print('Computing reverse emission probability...')
    emission_matrix = load_json(MODEL_PATH['emission'])
    compute_reversed_emission(emission_matrix)

    print('Computing reverse transition probability...')
    compute_reversed_transition()

    print('Computing next...')
    emission_matrix = load_json(MODEL_PATH['emission'])
    transition_matrix = load_json(MODEL_PATH['transition'])
    compute_nxt(transition_matrix, emission_matrix)

    print('That is all...')
