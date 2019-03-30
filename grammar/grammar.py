#!/usr/bin/python
# coding=utf-8
# -*- encoding: utf-8 -*-

from earley.grammar import *


class RuleWithWeight(Rule):
    def __init__(self, lhs, rhs, context=None, weight=0):
        '''
            Initializes grammar rule: LHS -> [RHS]
            Init weight
        '''
        super.__init__(lhs, rhs, context)
        self.weight = 0

    def __repr__(self):
        '''Nice string representation. Use weight also'''
        return "<Rule {0} -> {1} W = {}>".format(self.lhs, ' '.join(self.rhs), self.weight)


class GrammarWithCorrection(Grammar):

    def add_rule(self, rule):
        '''
            Add a rule to the grammar
            If rule already exist, look at weight, and add with minimal weight
        '''
        lhs = rule.lhs
        if lhs in self.rules:
            if rule not in self.rules[lhs]:
                self.rules[lhs].append(rule)
            else:
                for _r in self.rules[lhs]:
                    if _r == rule:
                        _r.weight = min(_r.weight, rule.weight)
        else:
            self.rules[lhs] = [rule]

    @staticmethod
    def build_error_correction_grammar(filename):
        '''

        Load grammar from file.
        Add error correcting rules.

        :param filename: string
        :return: GrammarWithCorrection
        '''
        grammar = GrammarWithCorrection.from_file(filename)

        return grammar