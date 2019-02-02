import nltk
from nltk import word_tokenize

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
    s = mistakes[1]
    # s = word_tokenize(s)
    # s_with_pos = nltk.pos_tag(s)
    # '(ROOT  (SQ (VBP Are)    (NP (DT the) (JJ green) (NNS fields))    (ADJP (VBN gone))    (. ?)))'
    # s = 'Are/Are<VBP> the/the<DT> green/green<JJ> fields/fields<NNS> gone/gone<VBN> ?/?<.>'
    s = 'Are the green fields gone?'
    return s


def build_sentence():
    s = get_sentence()
    text = word_tokenize(s)
    s_with_pos = nltk.pos_tag(text)
    s = ' '.join([x[0] + '/' + x[0] + '<' + x[1] + '>' for x in s_with_pos])
    return s


def main():
    run('/Users/vitaliyvrublevskiy/projects/Grammar/rules.cfg', build_sentence(), False, 'ROOT')


def main_nltk_rules():
    run('/Users/vitaliyvrublevskiy/projects/Grammar/rules_nltk.cfg', build_sentence(), False, 'S')


def main_artificial():
    s = 'a/a<A> b/b<B> b/b<B>'
    run(
        '/Users/vitaliyvrublevskiy/projects/Grammar/rules_artificial.cfg',
        s,
        True,
        'ROOT'
    )


main_nltk_rules()
print build_sentence()
