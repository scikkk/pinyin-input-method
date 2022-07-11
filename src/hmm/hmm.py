'''
Author: scikkk 203536673@qq.com
Date: 2022-07-07 13:55:21
LastEditors: scikkk
LastEditTime: 2022-07-12 00:35:07
Description: HMM class
'''

from util.tools import load_json


class HMM:
    """
    Hidden Markov Model

    :param start_log_prob: start_log_prob[Chinese character] = Logarithmic probability
    :param emiss_log_prob: emission_log_prob[Chinese character] = {Pinyin_1: Prob_1, ...}
    :param trans_log_prob: transition_log_prob[Previous Chinese character] = {Post Chinese character, Logarithmic probability}
    :param reversed_emission: reversed_emission_log_prob[Pinyin] = {Character_1: Prob_1, ...}
    :param rev_trans_log_prob: reversed_transition_log_prob[Post Chinese character] = {Previous Chinese character, Logarithmic probability}
    :param compute_nxt: compute_nxt[Previous Chinese character][Pinyin] = (most likely Post Chinese character, Prob)
    """

    def __init__(self):
        """ Load parameters necessary for HMM calculation. """
        print('Begin loading HMM.')

        print('Loading start_log_probability.json ...')
        self.start_log_prob = load_json('model\\start_log_probability.json')

        print('Loading reversed_emission.json ...')
        self.reversed_emission = load_json(
            'model\\reverse\\reversed_emission.json')

        print('Loading compute_nxt.json ...')
        self.compute_nxt = load_json('model\\reverse\\compute_nxt.json')

        print('All loading completed.')

    def trans(self, pinyin: tuple, limit=100) -> tuple:
        """
        Translate Pinyin into Chinese character sequences by viterbi algorithm.

        :param pinyin: tuple of Pinyin, e.g., ('wo','ai','ni')
        :param limit: maxmium number of the possible Chinese character sequences
        :return: Return up to limit the most possible Chinese character sequences, and return the remaining untranslated Pinyin.
        """
        # initialize, find out the Chinese character corresponding to the first Pinyin and the product of the probability of start and emission, and add it under the logarithm.
        char_and_log_prob = ((ch, self.start_log_prob.get(
            ch, -1e100) + self.reversed_emission[pinyin[0]][ch]) for ch in self.reversed_emission[pinyin[0]])
        viterbi = {char: log_prob for char, log_prob in char_and_log_prob}
        for i in range(1, len(pinyin)):
            py = pinyin[i]
            sequence_log_prob = {}
            for phrase, log_prob in viterbi.items():
                previous = phrase[-1]
                if previous in self.compute_nxt and py in self.compute_nxt[previous]:
                    state, new_log_prob = self.compute_nxt[previous][py]
                    sequence_log_prob[phrase + state] = new_log_prob + log_prob
            if sequence_log_prob:
                viterbi = sequence_log_prob
            else:
                # no probability, unable to continue translation, return the current result and untranslated Pinyin: pinyin[i:]
                return tuple([elem[0] for elem in sorted(viterbi.items(), key=lambda x: x[1], reverse=True)][:limit]), pinyin[i:]
        return tuple([elem[0] for elem in sorted(viterbi.items(), key=lambda x: x[1], reverse=True)[:limit]]), ''


if __name__ == '__main__':
    h = HMM()
    print(h.trans(('wo', 'ai', 'ni'), 6))  # 我爱你
    print(h.trans(('w', 'a', 'n'), 6))  # 我爱你
    print(h.trans(('zh', 'ge'), 6))  # 这个
