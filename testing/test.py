from build_rules import *
from random import randint
from parser.ParserErrorCorrect import ParserErrorCorrect


def get_trees():
    with open("brown-tree.txt", "r") as myfile:
        lines = myfile.readlines()
        return lines


def create_error(sentence):
    r = randint(0, 3)
    s = sentence[::]
    if r == 0:
        r = randint(0, len(s) - 2)
        del s[r + 1]
    elif r == 1:
        r = randint(0, len(s) - 3)
        s[r + 1], s[r + 2] = s[r + 2], s[r + 1]
    elif r == 2:
        r = randint(0, len(s) - 4)
        s[r + 1], s[r + 2], s[r + 3] = s[r + 2], s[r + 3], s[r + 1]
    elif r == 3:
        s = [('the', x[1]) if x[0] == 'a' else x for x in s]
    return s


def build_sentence(s):
    return ' '.join([x[0] + '/' + x[0] + '<' + x[1] + '>' for x in s])




def main():
    c = []
    w = []
    for tree in get_trees()[:50]:
        parse_t = get_parse_tree(tree)
        grammar = get_grammar_by_trees([tree])
        correct_pos_tags = []
        extract_pos_tags(parse_t, correct_pos_tags)
        wrong_sentence = create_error(correct_pos_tags)
        cr = ' '.join([x[0] for x in correct_pos_tags])
        wr = ' '.join([x[0] for x in wrong_sentence])

        cr = cr.replace(' ,', ',')
        cr = cr.replace(' .', '.')
        wr = wr.replace(' ,', ',')
        wr = wr.replace(' .', '.')
        c.append(cr)
        w.append(wr)
        print wr
        print correct_pos_tags
        ParserErrorCorrect.run(
            grammar_path='dummy',
            grammar=grammar,
            s=build_sentence(wrong_sentence),
            debug=False,
        )
        print '***************'


if __name__ == '__main__':
    main()