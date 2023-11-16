from common import *
from parser.ParserErrorCorrect import ParserErrorCorrect


def get_sentence():
    return '()(()'


def build_sentence(s):
    s = ' '.join([char + '/' + char + '<' + char + '>' for char in s])
    return s

@timing
def main():
    s = build_sentence(get_sentence())
    ParserErrorCorrect.run(
        grammar_path='/Users/vrublevskyi/Uni/Grammar/grammars/rules_brackets.cfg',
        s=s,
        debug=True,
    )


if __name__ == '__main__':
    main()