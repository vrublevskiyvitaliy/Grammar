import nltk
from nltk import word_tokenize
from earley.earley import run
from common import *
from build_rules import *

@timing
def parse(s):
    run(
        grammar_path='/Users/vitaliyvrublevskiy/projects/Grammar/rules_transitive.cfg',
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
    grammar = get_main_grammar()
    rules = grammar.get_rule(rule)
    for r in rules:
        for s in r.context:
            print s


if __name__ == '__main__':
     main()
    # find_trees_by_rule()