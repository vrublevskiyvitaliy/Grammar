from earley.grammar import *


BUILD_ALL = 'all'
BUILD_MINI = 'mini'

MINI_TREES = [19]
MINI_TREES = xrange(100, 200, 1)

MODE = BUILD_ALL


def get_trees():
    with open("tree.txt", "r") as myfile:
        lines = myfile.readlines()
        return lines


def extract_rules(tree, grammar, source):
    if tree['children']:
        seq = []
        for el in tree['children']:
            seq.append(el['v'][0])
        head = tree['v'][0]
        grammar.add_rule(Rule(head, seq, source))
        for el in tree['children']:
            extract_rules(el, grammar, source)


def parse_tree(tree, grammar):
    l = len(tree)
    root = {'v' : [], 'children' : []}
    stack = [root]
    current_element = root
    current_level = 0
    token = ''
    for i in xrange(l):
        if tree[i] not in ['(', ')', ' ']:
            token += tree[i]
        else:
            if tree[i] == '(':
                v = []
                if token:
                    v.append(token)
                el = {'v': v, 'children': []}
                current_element['children'].append(el)
                current_element = el
                current_level += 1
                while len(stack) <= current_level:
                    stack.append([])
                stack[current_level] = current_element
            elif tree[i] == ')':
                if token:
                    current_element['v'].append(token)
                current_level -= 1
                current_element = stack[current_level]
                if current_level == 0:
                    break
            elif tree[i] == ' ':
                if len(token):
                    current_element['v'].append(token)

            token = ''
    root = root['children'][0]
    extract_rules(root, grammar, tree)


def get_rules_file():
    if MODE == BUILD_MINI:
        return 'rules_mini.cfg'
    else:
        return 'rules.cfg'


def get_main_grammar():
    grammar = Grammar()
    trees = get_trees()
    for tree in trees:
        parse_tree(tree, grammar)

    return grammar


def main():
    grammar = get_main_grammar()
    grammar.trim_rules_by_context(2)
    grammar.save_to_file(get_rules_file())
    return


def main_mini():
    trees = get_trees()
    grammar = Grammar()

    for i in MINI_TREES:
        print trees[i]
        parse_tree(trees[i], grammar)

    grammar.save_to_file(get_rules_file())

if __name__ == '__main__':
    if MODE == BUILD_MINI:
        main_mini()
    else:
        main()