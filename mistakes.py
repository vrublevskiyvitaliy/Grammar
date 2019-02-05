import nltk
from nltk import word_tokenize
from earley.earley import run
from common import *


@timing
def parse(s):
    run(
        grammar_path='/Users/vitaliyvrublevskiy/projects/Grammar/rules.cfg',
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



main()