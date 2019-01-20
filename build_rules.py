

def get_trees():
    with open("tree.txt", "r") as myfile:
        lines = myfile.readlines()
        return lines


def extract_rules(tree, rules):
    if tree['children']:
        seq = []
        for el in tree['children']:
            seq.append(el['v'][0])
        head = tree['v'][0]
        if head not in rules:
            rules[head] = []
        rules[head].append(seq)
        for el in tree['children']:
            extract_rules(el, rules)


def parse_tree(tree, rules):
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
            # if len(token):
            #     #while len(stack) <= current_level:
            #     #    stack.append([])
            #     current_element['children'].append(token)
            #     # stack[current_level].append(token)
            #     token = ''
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
    extract_rules(root, rules)
    y = 0


def save_rules(rules):
    with open("rules.txt", "a") as myfile:
        for el in rules:
            myfile.write(el + ' -> ')
            myfile.write(' | '.join([' '.join(rule) for rule in rules[el]]))
            myfile.write('\n')
        myfile.close()


def main():
    trees = get_trees()
#    print trees[0]
    rules = {}
    for tree in trees:
        parse_tree(tree, rules)
    for el in rules:
        rules[el] = [y.split('|') for y in set([('|').join(x) for x in rules[el]])]
    save_rules(rules)
    y = 0




main()