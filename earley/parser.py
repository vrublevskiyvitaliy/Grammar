#!/usr/bin/python
# coding=utf-8
# -*- encoding: utf-8 -*-

from chart import *
from grammar import *

class Parser:
    GAMMA_SYMBOL = 'GAMMA'
    TRIM_BY_LENGTH = False

    def __init__(self, grammar, sentence, debug=False, start_rule='S'):
        '''Initialize parser with grammar and sentence'''
        self.grammar = grammar
        self.sentence = sentence
        self.debug = debug
        self.start_rule = start_rule

        # prepare a chart for every input word
        self.charts = [Chart([]) for i in range(len(self)+1)]
        self.complete_parses = []
        self.chart_complete_tokens = []
        self.words = []


    def __len__(self):
        '''Length of input sentence'''
        return len(self.sentence)

    def init_first_chart(self):
        '''Add initial Gamma rule to first chart'''
        row = ChartRow(Rule(Parser.GAMMA_SYMBOL, [self.start_rule]), 0, 0)
        self.charts[0].add_row(row)

    def is_valid_sentence(self):
        '''Returns true if sentence has a complete parse tree'''
        res = False
        self.complete_parses = []
        for row in self.charts[-1].rows:
            if row.start == 0:
                if row.rule.lhs == self.GAMMA_SYMBOL:
                    if row.is_complete():
                        self.complete_parses.append(row)
                        res = True
        return res


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
        while chart.predict_row_index < len(chart):
            row = chart.rows[chart.predict_row_index]
            if RULES_PER_CHART and RULES_PER_CHART <= len(chart.rows):
                break
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
            chart.predict_row_index += 1


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

            print 'Iteration {0}'.format(i)
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


class ParserLazy(Parser):

    def init_chart_complete_tokens(self):
        for word in self.sentence:
            if word:
                self.chart_complete_tokens.append(word.tags)
                self.words.append(word.word)
            else:
                break

    def predict_complete(self, next_cat, position, row):
        completing_row = ChartRow(Rule(next_cat, [self.words[position]]), 1, position, None, None, True)
        next_chart_rule = ChartRow(
            row.rule,
            row.dot + 1,
            row.start,
            row,
            completing_row,
            False,
            row
        )
        self.charts[position + 1].add_row(next_chart_rule)

    def predict(self, chart, position, words_left):
        '''Predict next parse by looking up grammar rules
           for pending categories in current chart'''
        while chart.predict_row_index < len(chart):
            row = chart.rows[chart.predict_row_index]
            if RULES_PER_CHART and RULES_PER_CHART <= len(chart.rows):
                break
            next_cat = row.next_category()
            if next_cat in self.chart_complete_tokens[position]:
                self.predict_complete(next_cat, position, row)
                chart.predict_row_index += 1
                return True
            else:
                read_next_token = False
                rules = self.grammar[next_cat]
                if rules:
                    for rule in rules:
                        if rule.is_chart_used(position):
                            continue
                        # valid only when we can guarantee there will be not a rule A -> epsilon
                        if Parser.TRIM_BY_LENGTH and len(rule.rhs) > words_left:
                            continue

                        new = ChartRow(rule, 0, position, None, None, False, row)
                        chart.add_row(new)
                        rule.add_chart(position)
                        new_next_cat = new.next_category()
                        if new_next_cat in self.chart_complete_tokens[position]:
                            read_next_token = True
                            self.predict_complete(new_next_cat, position, new)

                chart.predict_row_index += 1
                if read_next_token:
                    return True
        return False

    def complete(self, chart, position, words_left, force=False):
        '''Complete a rule that was done parsing, and
           promote previously pending rules'''
        if force:
            chart.complete_row_index = 0
        while chart.complete_row_index < len(chart):
            row = chart.rows[chart.complete_row_index]
            if row.is_complete():
                completed = row.rule.lhs
                for r in self.charts[row.start].rows:
                    if completed == r.next_category():
                        new = ChartRow(r.rule, r.dot + 1, r.start, r, row, False, row)
                        if Parser.TRIM_BY_LENGTH and new.get_left_len() > words_left:
                            continue
                        chart.add_row(new)
            chart.complete_row_index += 1

    def print_chart(self, index):
        if self.debug:
            print "Parsing charts:"
            print "-----------{0}-------------".format(index)
            print self.charts[index]
            print "-------------------------".format(index)


    def parse(self):
        '''Main Earley's Parser loop'''
        self.init_first_chart()
        self.init_chart_complete_tokens()

        token_to_read = 0
        while token_to_read <= len(self.sentence):

            chart = self.charts[token_to_read]
            chart.complete_row_index = 0

            self.prescan(chart, token_to_read)

            if token_to_read == len(self.sentence):
                while chart.complete_row_index < len(chart):
                    self.complete(chart, token_to_read, len(self.charts) - token_to_read - 1)
                if self.is_valid_sentence():
                    break
                else:
                    token_to_read -= 1
            else:
                print 'Try to read word {0}'.format(token_to_read)
                self.print_chart(token_to_read)

                read_next = False
                while not read_next:
                    read_next = self.predict(chart, token_to_read, len(self.charts) - token_to_read - 1)

                    if read_next:
                        token_to_read += 1
                        break
                    else:
                        if chart.complete_row_index == len(chart):
                            token_to_read -= 1
                            break
                        else:
                            self.complete(chart, token_to_read, len(self.charts) - token_to_read - 1)

