#!/usr/bin/python
# coding=utf-8
# -*- encoding: utf-8 -*-
from config import *


class Chart:
    def __init__(self, rows):
        '''An Earley chart is a list of rows for every input word'''
        self.rows = rows
        self.rules_count = {}
        self.predict_row_index = 0
        self.complete_row_index = 0
        self.hash_set = set()
        self.hash_to_rule = dict()
        self.is_complete = False
        self.is_prescaned = False

    def __len__(self):
        '''Chart length'''
        return len(self.rows)

    def __repr__(self):
        '''Nice string representation'''
        st = '<Chart>\n\t'
        st += '\n\t'.join(str(r) for r in self.rows)
        st += '\n</Chart>'
        return st

    def add_row(self, row):
        '''Add a row to chart, only if wasn't already there'''
        hash = row.__hash__()
        if not row in self.hash_set:
            if self.should_add_row(row):
                self.rows.append(row)
                self.hash_set.add(row)
                self.hash_to_rule[hash] = {
                    'weight': row.weight,
                    'index': len(self.rows) - 1
                }
        else:
            if row.weight < self.hash_to_rule[hash]['weight']:
                index = self.hash_to_rule[hash]['index']
                if index > self.predict_row_index:
                    self.rows[index].weight = row.weight
                    self.hash_to_rule[hash]['weight'] = row.weight
                else:
                    self.rows.append(row)
                    self.hash_to_rule[hash] = {
                        'weight': row.weight,
                        'index': len(self.rows) - 1
                    }

    def should_add_row(self, row):
        if not GET_ALL_TREES:
            return True
        hash = str(row)
        if hash not in self.rules_count:
            self.rules_count[hash] = 0

        if self.rules_count[hash] >= AMOUNT_OF_DUPLICATE_RULES:
            return False
        else:
            self.rules_count[hash] += 1
            return True


class ChartRow:
    def __init__(self, rule, dot=0, start=0, previous=None, completing=None, is_token_rule=False, parent=None, weight=0):
        '''Initialize a chart row, consisting of a rule, a position
           index inside the rule, index of starting chart and
           pointers to parent rows'''
        self.rule = rule
        self.dot = dot
        self.start = start
        self.completing = completing
        self.previous = previous
        self.is_token_rule = is_token_rule
        self.parent = parent
        self.weight = weight

    def __len__(self):
        '''A chart's length is its rule's length'''
        return len(self.rule)

    def __repr__(self):
        '''Nice string representation:
            <Row <LHS -> RHS .> [start]>'''
        rhs = list(self.rule.rhs)
        rhs.insert(self.dot, '*')
        rule_str = "[{0} -> {1}]".format(self.rule.lhs, ' '.join(rhs))
        return "<Row {0} [{1}]>".format(rule_str, self.start)

    def __cmp__(self, other):
        '''Two rows are equal if they share the same rule, start and dot'''
        if len(self) == len(other):
            if self.dot == other.dot:
                if self.start == other.start:
                    if self.rule == other.rule:
                        if not GET_ALL_TREES or self.completing == other.completing:
                            return 0
        return 1

    def is_complete(self):
        '''Returns true if rule was completely parsed, i.e. the dot is at the end'''
        return len(self) == self.dot

    def next_category(self):
        '''Return next category to parse, i.e. the one after the dot'''
        if self.dot < len(self):
            return self.rule[self.dot]
        return None

    def prev_category(self):
        '''Returns last parsed category'''
        if self.dot > 0:
            return self.rule[self.dot-1]
        return None

    def get_left_len(self):
        return len(self) - self.dot

    def __hash__(self):
        if not GET_ALL_TREES:
            key = "{0} | {1} | {2} | {3}".format(len(self), self.dot, self.start, self.rule)
        else:
            key = "{0} | {1} | {2} | {3} | {4}".format(len(self), self.dot, self.start, self.rule, self.completing)

        return hash(key)