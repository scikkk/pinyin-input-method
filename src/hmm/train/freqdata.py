words_path = '.\\data\\wordfreq.txt'


def wordfreq() -> tuple:
    """ Word frequency data set, iteratively return (word, freq). """
    with open(words_path, 'r', encoding='utf-8') as fr:
        for line in fr:
            word, frequency = line.split()
            yield word, int(frequency)
