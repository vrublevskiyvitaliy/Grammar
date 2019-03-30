#!/usr/bin/python
# coding=utf-8
# -*- encoding: utf-8 -*-

from earley.parser import Parser
from grammar.grammar import *
from earley.sentence import Sentence
from earley.parse_trees import ParseTrees
from earley.config import *
from earley.chart import *


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

    def prescan(self, chart, position):
        '''
           Scan current word in sentence, and add appropriate
           grammar categories to current chart
           Generally just add word with all combination of tags.
           Do nothing else.
        :param chart: Chart
        :param position: int
        :return: None
        '''
        word = self.sentence[position - 1]
        if word:
            rules = [RuleWithWeight(tag, [word.word]) for tag in word.tags]
            for rule in rules:
                chart.add_row(ChartRow(rule, 1, position - 1))

    def predict(self, chart, position, words_left):
        '''
            Predict next parse by looking up grammar rules for pending categories in current chart.
            Try to move dot to next position by 'opening' new rule.
        :param chart: Chart
        :param position: int
        :param words_left: int Amount of words left to parse. Can be used in trimming trees.
        :return:
        '''
        while chart.predict_row_index < len(chart):
            row = chart.rows[chart.predict_row_index]
            next_cat = row.next_category()
            rules = self.grammar[next_cat]
            if rules:
                for rule in rules:
                    if rule.is_chart_used(position):
                        continue
                    new = ChartRow(rule, 0, position, weight=row.weight + rule.weight)
                    chart.add_row(new)
                    rule.add_chart(position)
            chart.predict_row_index += 1

    def complete(self, chart, position, words_left):
        '''
            Complete a rule that was done parsing, and promote previously pending rules
        :param chart: Chart
        :param position: int
        :param words_left: int Amount of words left to parse. Can be used in trimming trees.
        :return:
        '''
        for row in chart.rows:
            if row.is_complete():
                completed = row.rule.lhs
                for r in self.charts[row.start].rows:
                    if completed == r.next_category():
                        new = ChartRow(r.rule, r.dot + 1, r.start, r, row, weight=row.weight)
                        # if Parser.TRIM_BY_LENGTH and new.get_left_len() > words_left:
                        #     continue
                        chart.add_row(new)