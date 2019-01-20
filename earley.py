from earley.earley import run


def get_sentence():
    #```time/time<N> flies/fly<N>/fly<V> like/like<V>/like<P> an/a<D> arrow/arrow<N>```

    s = 'Call/Call<VB> me/me<PRP> Ishmael/Ishmael<JJ> ./.<.>'
    return s


def main():
    run('/Users/vitaliyvrublevskiy/projects/Grammar/rules.cfg',get_sentence(), True )
    y = 0

main()