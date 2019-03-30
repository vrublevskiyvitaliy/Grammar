#!/usr/bin/python
# coding=utf-8
# -*- encoding: utf-8 -*-

from earley.parser import Parser
from grammar.grammar import GrammarWithCorrection
from earley.sentence import Sentence
from earley.parse_trees import ParseTrees
from earley.config import *

class ParserErrorCorrect(Parser):

    def __init__(self, grammar, sentence, debug=False, start_rule='ROOT'):
        '''Initialize parser with grammar and sentence'''
        super(ParserErrorCorrect, self).__init__(grammar, sentence, debug, start_rule)

    @staticmethod
    def run(grammar_path, s, debug=False, start_rule='S'):
        grammar = GrammarWithCorrection.build_error_correction_grammar(grammar_path)
        sentence = Sentence.from_string(s)
        earley = ParserErrorCorrect(grammar, sentence, debug, start_rule)

        earley.parse()  # output sentence validity
        if earley.is_valid_sentence():
            print '==> Sentence is valid.'
            trees = ParseTrees(earley)
            print 'Valid parse trees:'
            print trees
        else:
            print '==> Sentence is invalid.'