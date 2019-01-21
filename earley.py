import nltk
from nltk import word_tokenize

from earley.earley import run


def get_sentence():
    #```time/time<N> flies/fly<N>/fly<V> like/like<V>/like<P> an/a<D> arrow/arrow<N>```

    #s = 'Call/Call<VB> me/me<PRP> Ishmael/Ishmael<JJ> ./.<.>'
    '(ROOT  (SQ (VBP Are)    (NP (DT the) (JJ green) (NNS fields))    (ADJP (VBN gone))    (. ?)))'
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
    run('/Users/vitaliyvrublevskiy/projects/Grammar/rules.cfg', build_sentence(), True, 'ROOT')
    # run('/Users/vitaliyvrublevskiy/projects/Grammar/rules_mini.cfg', build_sentence(), True, 'ROOT')
    y = 0

main()
print build_sentence()