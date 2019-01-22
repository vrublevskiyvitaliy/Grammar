import nltk
from nltk.corpus import brown
from collections import defaultdict

x = defaultdict(set)


def get_all_corpora():
    corpora = [
        brown,
    ]
    for item in corpora:
        yield item.sents()


def proccess_sentence(s):
    s_with_pos = nltk.pos_tag(s)
    for word, pos in s_with_pos:
        x[word].add(pos)


def init_dictionary():
    if len(x) > 0:
        return
    for corpora in get_all_corpora():
        for sentence in corpora:
            proccess_sentence(sentence)


def get_pos_tag(word):
    init_dictionary()
    return x[word]


print get_pos_tag('sleep')