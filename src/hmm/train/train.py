'''
Description: Generate parameters of HMM
Author: SciK
Date: 2022-07-08 16:28:16
LastEditors: SciK
LastEditTime: 2022-07-10 00:24:03
FilePath: \mypinyin\src\hmm\train\train.py
'''
from math import log

# 用于加载词频数据
import freqdata
from tqdm import tqdm
# 用于将汉字转化为拼音
import pypinyin


from util.tools import save_json, load_json
from conf.config import TRAIN_CONFIG


# 以 JSON 格式保存稀疏矩阵的路径
# 分别是初始状态概率向量 π、转移矩阵 A 和发射矩阵 B
hmm_start_path = 'model\\start_probability.json'
hmm_transition_path = 'model\\transition_probability.json'
hmm_emission_path = 'model\\emission_probability.json'
# 倒查表
hmm_reversed_emission_path = 'model\\reverse\\reversed_emission.json'
hmm_reversed_emission_transition_path = 'model\\reverse\\reversed_emission_transition.json'
hmm_reversed_transition_path = 'model\\reverse\\reversed_transition.json'
hmm_compute_nxt_path = 'model\\reverse\\compute_nxt.json'


def compute_start():
    """    
    Generate the start probability matrix π.    
    """
    start_cnt = {}  # 用于计数
    tot = 0
    for word, freq in tqdm(freqdata.wordfreq(), total=3521036):
        tot += freq
        start_cnt[word[0]] = start_cnt.get(word[0], 0) + freq
    start_lprob = {}  # 需要保存的对数结果
    for ch in start_cnt.keys():
        start_lprob[ch] = log(start_cnt.get(ch) / tot)

    # 保存为 JSON 格式
    save_json(start_lprob, hmm_start_path)


def compute_transition():
    """    
    Generate the transition probability matrix A.   

    transition_prob[Previous Chinese character] = {Post Chinese character, Logarithmic probability}
    """
    transition_ch_cnt = {}  # 用于计数
    for word, freq in tqdm(freqdata.wordfreq(), total=3521036):
        for i in range(len(word) - 1):
            # 保存从前一个字到后一个字的频率
            pre, post = word[i], word[i+1]
            if not transition_ch_cnt.get(pre, None):
                transition_ch_cnt[pre] = {}
            transition_ch_cnt[pre][post] = \
                transition_ch_cnt[pre].get(post, 0) + freq

    transition_prob = {}  # 需要保存的结果
    for pre, post_ch_cnt in transition_ch_cnt.items():
        tot = sum(post_ch_cnt.values())
        transition_prob[pre] = {}
        for post in post_ch_cnt.keys():
            transition_prob[pre][post] = log(post_ch_cnt[post] / tot)

    # 保存为 JSON 格式
    save_json(transition_prob, hmm_transition_path)


def compute_reversed_transition():
    """    
    Generate the reversed transition probability matrix.    

    transition_prob[Post Chinese character] = {Previous Chinese character, Logarithmic probability}
    """
    transition_ch_cnt = {}  # 用于计数
    for word, freq in tqdm(freqdata.wordfreq(), total=3521036):
        for i in range(len(word) - 1):
            # 保存从后一个字到前一个字的频率
            pre, post = word[i], word[i+1]
            if not transition_ch_cnt.get(post, None):
                transition_ch_cnt[post] = {}
            transition_ch_cnt[post][pre] = \
                transition_ch_cnt[post].get(pre, 0) + freq

    transition_prob = {}  # 需要保存的结果
    for post, pre_ch_cnt in transition_ch_cnt.items():
        tot = sum(pre_ch_cnt.values())
        transition_prob[post] = {}
        for pre in pre_ch_cnt.keys():
            transition_prob[post][pre] = log(pre_ch_cnt[pre] / tot)

    # 保存为 JSON 格式
    save_json(transition_prob, hmm_reversed_transition_path)


def compute_emission():
    """    
    Generate the emission probability matrix B.   

    emission_prob[Chinese character] = {Pinyin_1: Prob_1, ...}
    """
    emission_py_cnt = {}
    for word, freq in tqdm(freqdata.wordfreq(), total=3521036):
        all_pinyins = pypinyin.pinyin(word, style=pypinyin.NORMAL)
        for ch, pinyins in zip(word, all_pinyins):
            cnt_of_pinyins = len(pinyins)
            if ch not in emission_py_cnt:
                emission_py_cnt[ch] = {}
            for py in pinyins:
                def add_to_cnt(py, num):
                    emission_py_cnt[ch][py] = emission_py_cnt[ch].get(py, 0) + \
                        num * freq // cnt_of_pinyins
                if len(py) >= 1:
                    # 处理完整拼音情况
                    add_to_cnt(py, TRAIN_CONFIG['intact_weight'])
                if len(py) >= 2:
                    if py[:2] in ('zh', 'ch', 'sh'):
                        add_to_cnt(py[:2], TRAIN_CONFIG['zcs_weight'])
                    add_to_cnt(py[0], TRAIN_CONFIG['first_weight'])
    emission_prob = {}
    for ch, pinyin_cnt in emission_py_cnt.items():
        tot = sum(pinyin_cnt.values())
        emission_prob[ch] = {}
        for pinyin in pinyin_cnt.keys():
            emission_prob[ch][pinyin] = log(pinyin_cnt[pinyin] / tot)
    # 保存为 JSON 格式
    save_json(emission_prob, hmm_emission_path)


def compute_reversed_emission(emission_prob):
    """    
    Generate the reversed emission probability matrix.    

    reversed_emission_prob[Pinyin] = {Character_1: Prob_1, ...}
    """
    # 生成 emission_prob 的倒查表, 即 reversed_emission_prob[拼音] = {汉字: 概率}
    reversed_emission_prob = {}
    for char in tqdm(emission_prob):
        for pinyin, prob in emission_prob[char].items():
            if pinyin not in reversed_emission_prob:
                reversed_emission_prob[pinyin] = {}
            reversed_emission_prob[pinyin][char] = prob
    save_json(reversed_emission_prob, hmm_reversed_emission_path)


def compute_nxt(transition_matrix, emission_matrix):
    """    
    Generate the matrix to find the most likely next Chinese character given a Pinyin.  

    reversed_transition_matrix[Previous Chinese character][Pinyin] = (most likely Post Chinese character, Prob)
    """
    reversed_transition_matrix = {}
    for previous in tqdm(transition_matrix):
        reversed_transition_matrix[previous] = {}
        for behind in transition_matrix[previous]:
            for pinyin in emission_matrix[behind]:
                prob = transition_matrix[previous][behind] + \
                    emission_matrix[behind][pinyin]
                if pinyin not in reversed_transition_matrix[previous]:
                    reversed_transition_matrix[previous][pinyin] = (
                        behind, prob)
                elif prob > reversed_transition_matrix[previous][pinyin][1]:
                    reversed_transition_matrix[previous][pinyin] = (
                        behind, prob)
    save_json(reversed_transition_matrix, hmm_compute_nxt_path)


if __name__ == '__main__':
    print('Compute start probability...')
    compute_start()

    print('Compute emission probability...')
    compute_emission()

    print('Compute transition probability...')
    compute_transition()

    print('Compute reverse transition probability...')
    compute_reversed_transition()

    print('Compute reverse emission probability...')
    emission_matrix = load_json(hmm_emission_path)
    compute_reversed_emission(emission_matrix)

    print('Compute next...')
    emission_matrix = load_json(hmm_emission_path)
    transition_matrix = load_json(hmm_transition_path)
    compute_nxt(transition_matrix, emission_matrix)

    print('That is all...')
