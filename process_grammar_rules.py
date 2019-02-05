from earley.grammar import *
from common import *

GRAMMAR_PATH = '/Users/vitaliyvrublevskiy/projects/Grammar/rules.cfg'
MAIN_RULE = 'ROOT'


def main():
    grammar = Grammar.from_file(GRAMMAR_PATH)
    processed_grammar = Grammar()

    neterminal_priority = dict()
    neterminal_priority[MAIN_RULE] = 0

    queue = [MAIN_RULE]
    termainals = get_termainals()

    while len(queue):
        neterminal = queue[0]
        queue.remove(neterminal)
        current_priority = neterminal_priority[neterminal] + 1
        for rule in grammar[neterminal]:
            valid = True
            for node in rule.rhs:
                if node in termainals:
                    continue
                if node in neterminal_priority and neterminal_priority[node] < neterminal_priority[neterminal]:
                    print 'Error with rule', rule
                    valid = False
                    continue
                if node not in neterminal_priority:
                    neterminal_priority[node] = current_priority
                    queue.append(node)
            if valid:
                processed_grammar.add_rule(rule)

    processed_grammar.save_to_file('/Users/vitaliyvrublevskiy/projects/Grammar/rules_v1.cfg')



if __name__ == '__main__':
    main()