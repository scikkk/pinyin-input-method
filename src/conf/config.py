'''
Author: scikkk 203536673@qq.com
Date: 2022-07-08 14:38:44
LastEditors: scikkk
LastEditTime: 2022-07-21 11:35:05
Description: configuration file
'''

TRAIN_CONFIG = {
    'intact_weight': 21,
    'zcs_weight': 6,
    'first_weight': 4
}

CUT_CONFIG = {
    'has_correct': True,
    'has_first': True,
    'has_zcs': True
}

IME_CONFIG = {
    'max_pinyin_len': 52,
    'candidate_per_page': 10
}

MODEL_PATH = {
    'start': 'model\\start_log_probability.json',
    'transition': 'model\\transition_log_probability.json',
    'emission': 'model\\emission_log_probability.json',
    'reversed_emission': 'model\\reverse\\reversed_emission.json',
    'reversed_transition': 'model\\reverse\\reversed_transition.json',
    'compute_nxt': 'model\\reverse\\compute_nxt.json'
}
