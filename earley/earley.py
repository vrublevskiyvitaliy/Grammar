#!/usr/bin/python
# coding=utf-8
# -*- encoding: utf-8 -*-

import sys
from grammar import *
from sentence import *
from parser import *
from parse_trees import *


def run(grammar_path, s, debug=False, start_rule='S', lazy=False):
    # load grammar from file

    grammar = Grammar.from_file(grammar_path)

    sentence = Sentence.from_string(s)

    # run parser
    if lazy:
        earley = ParserLazy(grammar, sentence, debug, start_rule)
    else:
        earley = Parser(grammar, sentence, debug, start_rule)


    earley.parse()  # output sentence validity
    if earley.is_valid_sentence():
        print '==> Sentence is valid.'

        trees = ParseTrees(earley)
        print 'Valid parse trees:'
        print trees
    else:
        print '==> Sentence is invalid.'
