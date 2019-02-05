import nltk
from nltk import word_tokenize


def timing(f):
    def wrap(*args):
        import time
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f s' % (f.func_name, (time2-time1))
        return ret
    return wrap


def build_sentence(s):
    text = word_tokenize(s)
    s_with_pos = nltk.pos_tag(text)
    s = ' '.join([x[0] + '/' + x[0] + '<' + x[1] + '>' for x in s_with_pos])
    return s
