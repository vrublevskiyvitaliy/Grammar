import nltk
from nltk import word_tokenize
from earley.earley import run
from common import *
from earley.grammar import *


@timing
def parse(s):
    run(
        grammar_path='/Users/vitaliyvrublevskiy/projects/Grammar/rules_v1.cfg',
        s=build_sentence(s),
        debug=False,
        start_rule='ROOT',
        # lazy=True
        lazy=False
    )

def main():
    sentances = [
        'I go home.',
        'I went home.',
        'I gone home.',
        'I has gone home.',
    ]

    for s in sentances:
        print build_sentence(s)
        parse(s)


def get_trees():
    with open("tree.txt", "r") as myfile:
        lines = myfile.readlines()
        return lines


def find_trees_by_rule():
    rule = Rule('NP', ['VBN', 'NN'])



main()