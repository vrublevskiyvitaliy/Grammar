from common import *
from earley.earley import run


def get_sentence():
    #```time/time<N> flies/fly<N>/fly<V> like/like<V>/like<P> an/a<D> arrow/arrow<N>```

    # s = 'Call/Call<VB> me/me<PRP> Ishmael/Ishmael<JJ> ./.<.>'
    s = 'Call me Ishmael.'
    mistakes = [
        'Everyone forgot their notebook.',
        'Anna and Mike is going skiing',
        'Matt like fish',
        'The notion of authority also extended vertically.',
        'I gone home.',
    ]
    #
    s = mistakes[4]
    s = 'While cleaning my external hard drive, I found this old project of mine.'
    s = word_tokenize(s)
    # s_with_pos = nltk.pos_tag(s)
    # '(ROOT  (SQ (VBP Are)    (NP (DT the) (JJ green) (NNS fields))    (ADJP (VBN gone))    (. ?)))'
    # s = 'Are/Are<VBP> the/the<DT> green/green<JJ> fields/fields<NNS> gone/gone<VBN> ?/?<.>'
    # s = 'Are the green fields gone?'
    return s

@timing
def main():
    run(
        grammar_path='/Users/vitaliyvrublevskiy/projects/Grammar/rules.cfg',
        s=build_sentence(get_sentence()),
        debug=False,
        start_rule='ROOT',
        lazy=True
        # lazy=False
    )

@timing
def main_mini():
    run('/Users/vitaliyvrublevskiy/projects/Grammar/rules_mini.cfg', build_sentence(get_sentence()), False, 'ROOT', True)


def main_nltk_rules():
    run('/Users/vitaliyvrublevskiy/projects/Grammar/rules_nltk.cfg', build_sentence(get_sentence()), False, 'S')


def main_artificial():
    s = 'a/a<A> b/b<B> b/b<B>'
    run(
        '/Users/vitaliyvrublevskiy/projects/Grammar/rules_artificial.cfg',
        s,
        True,
        'ROOT'
    )


main()
print build_sentence(get_sentence())
