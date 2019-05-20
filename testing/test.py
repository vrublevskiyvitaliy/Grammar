from build_rules import *
from random import randint

def get_trees():
    with open("brown-tree.txt", "r") as myfile:
        lines = myfile.readlines()
        return lines


def create_error(sentence):
    s = sentence[::]
    del s[1]
    return s


def main():
    for tree in get_trees()[:2]:
        parse_t = get_parse_tree(tree)
        grammar = get_grammar_by_trees([tree])
        correct_pos_tags = []
        extract_pos_tags(parse_t, correct_pos_tags)
        wrong_sentence = create_error(correct_pos_tags)
        y = 0






if __name__ == '__main__':
    main()