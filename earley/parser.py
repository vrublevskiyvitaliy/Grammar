#!/usr/bin/python
# coding=utf-8
# -*- encoding: utf-8 -*-

from chart import *
from grammar import *

class Parser:
    GAMMA_SYMBOL = 'GAMMA'
    TRIM_BY_LENGTH = True

    def __init__(self, grammar, sentence, debug=False, start_rule='S'):
        '''Initialize parser with grammar and sentence'''
        self.grammar = grammar
        self.sentence = sentence
        self.debug = debug
        self.start_rule = start_rule

        # prepare a chart for every input word
        self.charts = [Chart([]) for i in range(len(self)+1)]
        self.complete_parses = []

    def __len__(self):
        '''Length of input sentence'''
        return len(self.sentence)

    def init_first_chart(self):
        '''Add initial Gamma rule to first chart'''
        row = ChartRow(Rule(Parser.GAMMA_SYMBOL, [self.start_rule]), 0, 0)
        self.charts[0].add_row(row)

    def prescan(self, chart, position):
        '''Scan current word in sentence, and add appropriate
           grammar categories to current chart'''
        word = self.sentence[position-1]
        if word:
            rules = [Rule(tag, [word.word]) for tag in word.tags]
            for rule in rules:
                chart.add_row(ChartRow(rule, 1, position-1))

    def predict(self, chart, position, words_left):
        '''Predict next parse by looking up grammar rules
           for pending categories in current chart'''
        for row in chart.rows:
            next_cat = row.next_category()
            rules = self.grammar[next_cat]
            if rules:
                for rule in rules:
                    if rule.is_chart_used(position):
                        continue
                    # valid only when we can guarantee there will be not a rule A -> epsilon
                    if Parser.TRIM_BY_LENGTH and len(rule.rhs) > words_left:
                        continue
                    new = ChartRow(rule, 0, position)
                    chart.add_row(new)
                    rule.add_chart(position)

    def complete(self, chart, position, words_left):
        '''Complete a rule that was done parsing, and
           promote previously pending rules'''
        for row in chart.rows:
            if row.is_complete():
                completed = row.rule.lhs
                for r in self.charts[row.start].rows:
                    if completed == r.next_category():
                        new = ChartRow(r.rule, r.dot + 1, r.start, r, row)
                        if Parser.TRIM_BY_LENGTH and new.get_left_len() > words_left:
                            continue
                        chart.add_row(new)

    def print_chart(self, index):
        if self.debug:
            print "Parsing charts:"
            print "-----------{0}-------------".format(index)
            print self.charts[index]
            print "-------------------------".format(index)


    def parse(self):
        '''Main Earley's Parser loop'''
        self.init_first_chart()

        i = 0
        sentence_len = len(self.charts)
        # we go word by word
        while i < sentence_len:
            chart = self.charts[i]
            self.prescan(chart, i) # scan current input

            if self.debug:
                print 'After prescan:'
            self.print_chart(i)

            # predict & complete loop
            # rinse & repeat until chart stops changing
            length = len(chart)
            old_length = -1
            while old_length != length:
                self.predict(chart, i, len(self.charts) - i - 1)
                self.complete(chart, i, len(self.charts) - i - 1)

                old_length = length
                length = len(chart)
                if self.debug:
                    print 'After iteration:'
                self.print_chart(i)
            # print charts for debuggers
            self.print_chart(i)
            i+= 1




    def is_valid_sentence(self):
        '''Returns true if sentence has a complete parse tree'''
        res = False
        for row in self.charts[-1].rows:
            if row.start == 0:
                if row.rule.lhs == self.GAMMA_SYMBOL:
                    if row.is_complete():
                        self.complete_parses.append(row)
                        res = True
        return res

