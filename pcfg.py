def pcfg_demo():
    """
    A demonstration showing how a ``PCFG`` can be created and used.
    """

    from nltk.corpus import treebank
    from nltk import treetransforms
    from nltk import induce_pcfg
    from nltk.parse import pchart

    # pcfg_prods = toy_pcfg1.productions()
    #
    # pcfg_prod = pcfg_prods[2]
    # print('A PCFG production:', repr(pcfg_prod))
    # print('    pcfg_prod.lhs()  =>', repr(pcfg_prod.lhs()))
    # print('    pcfg_prod.rhs()  =>', repr(pcfg_prod.rhs()))
    # print('    pcfg_prod.prob() =>', repr(pcfg_prod.prob()))
    # print()
    #
    # grammar = toy_pcfg2
    # print('A PCFG grammar:', repr(grammar))
    # print('    grammar.start()       =>', repr(grammar.start()))
    # print '    grammar.productions() =>',
    # # Use .replace(...) is to line-wrap the output.
    # print(repr(grammar.productions()).replace(',', ',\n' + ' ' * 26))
    # print()

    # extract productions from three trees and induce the PCFG
    print("Induce PCFG grammar from treebank data:")

    productions = []
    item = treebank._fileids[0]
    for tree in treebank.parsed_sents(item)[:3]:
        # perform optional tree transformations, e.g.:
        tree.collapse_unary(collapsePOS=False)
        tree.chomsky_normal_form(horzMarkov=2)

        productions += tree.productions()

    # S = Nonterminal('S')
    # grammar = induce_pcfg(S, productions)
    print(productions)
    print()

    print("Parse sentence using induced grammar:")

    parser = pchart.InsideChartParser(grammar)
    parser.trace(3)

    # doesn't work as tokens are different:
    # sent = treebank.tokenized('wsj_0001.mrg')[0]

    sent = treebank.parsed_sents(item)[0].leaves()
    print(sent)
    for parse in parser.parse(sent):
        print(parse)


pcfg_demo()