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
        self.weight = weight
        super(RuleWithWeight, self).__init__(lhs, rhs, context)

    def __repr__(self):
        '''Nice string representation. Use weight also'''
        return "<Rule {0} -> {1} W = {2}>".format(self.lhs, ' '.join(self.rhs), self.weight)


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

        grammar = GrammarWithCorrection.transform_grammar(grammar)

        return grammar

    @staticmethod
    def from_file(filename):
        '''Returns a Grammar instance created from a text file.
           The file lines should have the format:
               lhs -> outcome | outcome | outcome'''

        grammar = GrammarWithCorrection()
        for line in open(filename):
            # ignore comments
            line = line[0:line.find('#')]
            if len(line) < 3:
                continue

            rule = line.split('->')
            lhs = rule[0].strip()
            for outcome in rule[1].split('|'):
                rhs = outcome.strip()
                symbols = rhs.split(' ') if rhs else []
                r = RuleWithWeight(lhs, symbols)
                grammar.add_rule(r)

        return grammar

    @staticmethod
    def transform_grammar(grammar):
        terminals = grammar.get_terminals()
        correction_grammar = GrammarWithCorrection()

        for neterminal in grammar.rules:
            for rule in grammar.rules[neterminal]:
                tr_rule = GrammarWithCorrection.get_transformed_rule(rule, terminals)
                correction_grammar.add_rule(tr_rule)

        for terminal in terminals:
            rules = GrammarWithCorrection.get_substitution_terminal_rules(terminal, terminals)
            for rule in rules:
                correction_grammar.add_rule(rule)

        for terminal in terminals:
            rules = GrammarWithCorrection.get_insertion_terminal_rules(terminal, terminals)
            for rule in rules:
                correction_grammar.add_rule(rule)

        return correction_grammar

    @staticmethod
    def get_transformed_rule(rule, terminals):
        rhs = []
        for item in rule.rhs:
            if item in terminals:
                rhs.append(item + '*')
            else:
                rhs.append(item)
        return RuleWithWeight(rule.lhs, rhs , rule.context, 0)

    @staticmethod
    def get_substitution_terminal_rules(t, terminals):
        rules = []
        for terminal in terminals:
            if t == terminal:
                rules.append(RuleWithWeight(t + '*', [t], None, 0))
            else:
                rules.append(RuleWithWeight(t + '*', [terminal], None, 1))
        return rules

    @staticmethod
    def get_insertion_terminal_rules(t, terminals):
        rules = []
        for terminal in terminals:
            rules.append(RuleWithWeight(t + '*', [terminal, t + '*'], None, 1))
        return rules
