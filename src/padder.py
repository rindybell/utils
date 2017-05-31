# coding:utf-8
#
# Author: Masayuki Komai
#

""" imports """
import sys
import os
import argparse

""" variables """
""" arguments """


class Padder:

    def __init__(self, max_sen, max_doc=None,
                 pad_symbol="*", sen_pad_style="right", doc_pad_style="bottom",
                 auto_sen_padding=False, auto_doc_padding=False):

        self.max_sen = max_sen
        self.max_doc = max_doc
        self.pad_symbol = pad_symbol
        self.sen_pad_style = sen_pad_style
        self.doc_pad_style = doc_pad_style
        self.auto_sen_padding = auto_sen_padding
        self.auto_doc_padding = auto_doc_padding

    def sentence_padding(self, sentence):
        if self.auto_sen_padding == False:
            assert len(
                sentence) <= self.max_sen, "Length Error: sentence_padding"

        if self.sen_pad_style == "right":
            return sentence[:self.max_sen] + (self.max_sen - len(sentence)) * [self.pad_symbol]
        elif self.sen_pad_style == "left":
            return (self.max_sen - len(sentence)) * [self.pad_symbol] + sentence[:self.max_sen]
        else:
            sys.stderr.write("Error: pad style error")
            exit(-1)

    def doc_padding(self, doc):
        if self.auto_doc_padding == False:
            assert len(doc) <= self.max_doc, "Length Error: doc_padding"

        new_doc = map(self.sentence_padding, doc[:self.max_doc])
        diff_nb_sen = self.max_doc - len(new_doc)
        diff_sens = [[self.pad_symbol] * self.max_sen] * diff_nb_sen

        if self.doc_pad_style == "bottom":
            return new_doc + diff_sens
        elif self.doc_pad_style == "upper":
            return diff_sens + new_doc
        else:
            sys.stderr.write("Error: pad style error")
            exit(-1)
