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

    def is_epsilon_rule(self):
        '''
            Whether this rule is epsilon rule: N -> null.
        :return: bool
        '''
        return len(self.rhs) == 1 and self.rhs[0] == GrammarWithCorrection.EPSILON_RULE


class GrammarWithCorrection(Grammar):
    EPSILON_RULE = '#'

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
    def build_error_correction_grammar_from_grammar(grammar):
        '''

        Load grammar from file.
        Add error correcting rules.

        :param grammar: Grammar
        :return: GrammarWithCorrection
        '''

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
                tr_rules = GrammarWithCorrection.get_transformed_rule(rule, terminals)
                for rule in tr_rules:
                    correction_grammar.add_rule(rule)

        for terminal in terminals:
            rules = GrammarWithCorrection.get_substitution_terminal_rules(terminal, terminals)
            for rule in rules:
                correction_grammar.add_rule(rule)

        for terminal in terminals:
            rules = GrammarWithCorrection.get_insertion_terminal_rules(terminal, terminals)
            for rule in rules:
                correction_grammar.add_rule(rule)

        for terminal in terminals:
            rules = GrammarWithCorrection.get_delete_terminal_rules(terminal, terminals)
            for rule in rules:
                correction_grammar.add_rule(rule)

        return correction_grammar

    @staticmethod
    def get_transformed_rule(rule, terminals):
        rhs = []
        neterminal_group = []
        neterminal_groups = []
        for item in rule.rhs:
            if item in terminals:
                if len(neterminal_group) > 0:
                    rhs.append('*'.join(neterminal_group))
                    neterminal_groups.append(neterminal_group)
                    neterminal_group = []
                rhs.append(item + '*')
            else:
                neterminal_group.append(item)

        if len(neterminal_group) > 0:
            rhs.append('*'.join(neterminal_group))
            neterminal_groups.append(neterminal_group)

        # base rule - original one
        rules = [RuleWithWeight(rule.lhs, rhs, rule.context, 0)]

        for neterminal_group in neterminal_groups:
            rules += GrammarWithCorrection.get_swapped_neterminal_group_rules(neterminal_group, rule.context)

        return rules

    @staticmethod
    def get_swapped_neterminal_group_rules(neterminal_group, context):
        if len(neterminal_group) < 2:
            return []

        lhs = '*'.join(neterminal_group)

        rules = []
        rules.append(RuleWithWeight(lhs, neterminal_group, context, 0))

        for i in range(len(neterminal_group) - 1):
            rhs = neterminal_group[:]
            rhs[i], rhs[i + 1] = rhs[i + 1], rhs[i]

            rules.append(RuleWithWeight(lhs, rhs, context, 1))

        return rules

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

    @staticmethod
    def get_delete_terminal_rules(t, terminals):
        rules = []
        rules.append(RuleWithWeight(t + '*', [GrammarWithCorrection.EPSILON_RULE], None, 1))
        return rules
