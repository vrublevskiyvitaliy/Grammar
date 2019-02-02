import nltk
from nltk.grammar import Nonterminal
from nltk.corpus import treebank


def get_termainals():
    from nltk.data import load
    tagdict = load('help/tagsets/upenn_tagset.pickle')
    return tagdict.keys()


def remove_last_number(s, char='-'):
    parts = s.split(char)
    if len(parts) > 1:
        if parts[-1].isdigit():
            parts = parts[:-1]
    return char.join(parts)


def remove_numbers_from_terminals(s):
    s = remove_last_number(s, '-')
    s = remove_last_number(s, '=')
    return s


def process_production(p):
    p._lhs._symbol = remove_numbers_from_terminals(p._lhs._symbol)
    for r in p._rhs:
        if isinstance(r, Nonterminal):
            r._symbol = remove_numbers_from_terminals(r._symbol)
    return p


def get_all_productions():
    productions = []

    pos_tags = get_termainals()
    pos_tags.append('-NONE-')
    for tree in treebank.parsed_sents():
        # perform optional tree transformations, e.g.:
        #tree.collapse_unary(collapsePOS=False)
        #tree.chomsky_normal_form(childChar='@')
        # print tree
        # tree.draw()
        for p in tree.productions():
            if str(p._lhs) not in pos_tags:
                p = process_production(p)
                productions.append(p)
    return productions


def group_productions(productions):
    grouped_by_lhs = {}
    for p in productions:
        key = str(p._lhs)
        if key not in grouped_by_lhs:
            grouped_by_lhs[key] = []
        grouped_by_lhs[key].append(p)
    return grouped_by_lhs


def remove_duplicates(grouped_productions):
    filtered_groupes = {}
    for g_key in grouped_productions:
        productions = grouped_productions[g_key]
        str_productions = [' '.join([str(non_terminal) for non_terminal in x._rhs]) for x in grouped_productions[g_key]]
        str_productions = list(set(str_productions))
        filtered_groupes[g_key] = str_productions
    return filtered_groupes


def get_rules_file():
    return 'rules_nltk.cfg'


def save_rules(rules):
    with open(get_rules_file(), "w") as myfile:
        for el in rules:
            myfile.write(el + ' -> ')
            myfile.write(' | '.join(rules[el]))
            myfile.write('\n')
        myfile.close()


def build_rules():
    productions = get_all_productions()
    grouped_productions = group_productions(productions)
    grouped_productions = remove_duplicates(grouped_productions)
    save_rules(grouped_productions)


build_rules()


