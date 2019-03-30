#!/usr/bin/python
# coding=utf-8
# -*- encoding: utf-8 -*-

import sys

class Rule:
    def __init__(self, lhs, rhs, context=None):
        '''Initializes grammar rule: LHS -> [RHS]'''
        self.lhs = lhs
        self.rhs = rhs
        if isinstance(context, basestring):
            self.context = [context]
        else:
            self.context = context

        self.already_used_in_charts = []

    def __len__(self):
        '''A rule's length is its RHS's length'''
        return len(self.rhs)

    def __repr__(self):
        '''Nice string representation'''
        return "<Rule {0} -> {1}>".format(self.lhs, ' '.join(self.rhs))

    def __getitem__(self, item):
        '''Return a member of the RHS'''
        return self.rhs[item]

    def __cmp__(self, other):
        '''Rules are equal iff both their sides are equal'''
        if self.lhs == other.lhs:
            if self.rhs == other.rhs:
                return 0
        return 1

    def add_chart(self, index):
        self.already_used_in_charts.append(index)

    def is_chart_used(self, index):
        return index in self.already_used_in_charts


class Grammar:
    def __init__(self):
        '''A grammar is a collection of rules, sorted by LHS'''
        self.rules = {}

    def __repr__(self):
        '''Nice string representation'''
        st = '<Grammar>\n'
        for group in self.rules.values():
            for rule in group:
                st+= '\t{0}\n'.format(str(rule))
        st+= '</Grammar>'
        return st

    def __getitem__(self, lhs):
        '''Return rules for a given LHS'''
        if lhs in self.rules:
            return self.rules[lhs]
        else:
            return []

    def add_rule(self, rule):
        '''Add a rule to the grammar'''
        lhs = rule.lhs
        if lhs in self.rules:
            if rule not in self.rules[lhs]:
                self.rules[lhs].append(rule)
            else:
                for _r in self.rules[lhs]:
                    if _r == rule:
                        if rule.context:
                            _r.context += rule.context
        else:
            self.rules[lhs] = [rule]

    def get_rule(self, rule):
        '''Gat a rule from the grammar'''
        rules = []
        lhs = rule.lhs
        if lhs in self.rules:
            for _r in self.rules[lhs]:
                if _r == rule:
                    rules.append(_r)

            return rules
        else:
            return None

    @staticmethod
    def from_file(filename):
        '''Returns a Grammar instance created from a text file.
           The file lines should have the format:
               lhs -> outcome | outcome | outcome'''

        grammar = Grammar()
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
                r = Rule(lhs, symbols)
                grammar.add_rule(r)

        return grammar

    def save_to_file(self, path):
        with open(path, "w") as myfile:
            for neterminal in self.rules:
                myfile.write(neterminal + ' -> ')
                myfile.write(' | '.join([' '.join(rule) for rule in self.rules[neterminal]]))
                myfile.write('\n')
            myfile.close()

    def trim_rules_by_context(self, min_context_len):
        '''
        Delete rules which was found in example text less than context_len.
        :param min_context_len:
        :return:
        '''
        keys_to_delete = []
        for lhs in self.rules:
            for rule in self.rules[lhs]:
                if len(rule.context) < min_context_len:
                    self.rules[lhs].remove(rule)
            if len(self.rules[lhs]) == 0:
                keys_to_delete.append(lhs)

        for key in keys_to_delete:
            self.rules.pop(key)