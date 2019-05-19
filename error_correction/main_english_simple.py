from common import *
from parser.ParserErrorCorrect import ParserErrorCorrect


@timing
def parse(s):
    ParserErrorCorrect.run(
        grammar_path='/Users/vitaliyvrublevskiy/projects/Grammar/rules_mini.cfg',
        # s=build_sentence(s),
        s=s,
        debug=False,
        start_rule='S'
    )

def main():
    sentances = [
        'Look at the crowds of water-gazers there.',
    ]

    s = 'Look/Look<VB> at/at<IN> of/of<IN> water-gazers/water-gazers<NNS> the/the<DT> crowds/crowds<NNS> there/there<RB> ./.<.>'

    #for s in sentances:
    #    print build_sentence(s)
    parse(s)


if __name__ == '__main__':
    main()