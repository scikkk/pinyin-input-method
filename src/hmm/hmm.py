# -*- coding: utf-8 -*-
"""
HMM class
参考https://zh.wikipedia.org/wiki/维特比算法
"""
from util.tools import load_json


class HMM:
    def __init__(self):
        """
        Load parameters necessary for HMM calculation.
        """
        self.start_prob = load_json('model\\start_probability.json')
        self.emiss_prob = load_json('model\\emission_probability.json')
        self.rev_trans_prob = load_json(
            'model\\reverse\\reversed_transition.json')
        self.trans_prob = load_json('model\\transition_probability.json')
        self.reversed_emission = load_json(
            'model\\reverse\\reversed_emission.json')
        self.compute_nxt = load_json(
            'model\\reverse\\compute_nxt.json')

    def trans(self, pinyin: tuple, limit=100) -> tuple:
        """
        Translate Pinyin into Chinese character sequences by viterbi algorithm.

        :param pinyin: tuple of Pinyin, e.g., ('wo','ai','ni')
        :param limit: maxmium number of the possible Chinese character sequences
        :return: Return up to limit the most possible Chinese character sequences, and return the remaining untranslated Pinyin.
        """
        # initialize, find out the Chinese character corresponding to the first Pinyin and the product of the probability of start and emission, and add it under the logarithm.
        char_and_prob = ((ch, self.start_prob.get(
            ch, -1e100) + self.reversed_emission[pinyin[0]][ch]) for ch in self.reversed_emission[pinyin[0]])
        V = {char: prob for char, prob in char_and_prob}
        for i in range(1, len(pinyin)):
            py = pinyin[i]
            prob_map = {}
            for phrase, prob in V.items():
                previous = phrase[-1]

                if previous in self.compute_nxt and py in self.compute_nxt[previous]:
                    state, new_prob = self.compute_nxt[previous][py]
                    prob_map[phrase + state] = new_prob + prob
            if prob_map:
                V = prob_map
            else:
                # no probability, unable to continue translation, return the current result and untranslated Pinyin: pinyin[i:]
                return tuple([elem[0] for elem in sorted(V.items(), key=lambda x: x[1], reverse=True)][:limit]), pinyin[i:]
        return tuple([elem[0] for elem in sorted(V.items(), key=lambda x: x[1], reverse=True)[:limit]]), ''


if __name__ == '__main__':
    t = HMM()
    print(t.trans(('wo', 'ai', 'ni'), 6))  # 我爱你
    print(t.trans(('w', 'a', 'n'), 6))  # 我爱你
    print(t.trans(('zh', 'ge'), 6))  # 这个
