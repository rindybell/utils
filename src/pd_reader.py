# coding:utf-8
__author__ = "Masayuki Komai"

""" imports """
import sys
import os
import argparse

""" python lib path """
currendir = os.path.abspath(os.path.dirname(__file__))
# sys.path.append(os.path.join(abspath, "../utils/src"))

""" general lib  """
import pandas as pd
import logging
import scipy.sparse as sp
import numpy as np
import pprint

""" user-defined lib """

class PdReader:
    def __init__(self, filename, use_header=False, logger=logging):
        self.filename = filename
        self.logger = logging

        # self.header = header

        if use_header == True:
            self.pd_item = pd.read_csv(
                self.filename, delimiter="\t")
        else:
            self.pd_item = pd.read_csv(
                self.filename, delimiter="\t", header=None)

    def segment(self, target_header, fun=lambda x: x.strip().split(" ")):
        self.pd_item[target_header] = self.pd_item[target_header].map(fun)

    def read_symbol(self, target_header, dictum):
        self.pd_item[target_header].map(dictum.push)

    def read_symbols(self, target_header, dictum):
        self.pd_item[target_header].map(dictum.push_list)

    def vectorize(self, target_headers, dictums):
        assert len(target_headers) == len(
            dictums), "headersとdictumsの長さが異なっています"

        map(lambda target_header: sp.vstack(
            self.pd_item[target_header]), target_headers)
        self.pd_item[target_header]
        self.pd_item[target_headers] = self.pd_item[target_headers]

    def sparse_vectorize(self, target_headers, dictum_vectorizers, vec_name="vec", init_vector=False):
        if init_vector == True:
            self.pd_item[vec_name] = sp.coo_matrix((1, 0))

        multi_vectorizer = self.merge_vectorizer(dictum_vectorizers)

        self.pd_item[vec_name] = map(lambda x:
                                     multi_vectorizer(
                                         map(lambda header: x[1][header], target_headers)),
                                     self.pd_item.iterrows())

        return

    def get_matrix(self, vec_name="vec"):
        return sp.vstack(self.pd_item[vec_name])

    def get(self):
        return self.pd_item

    def add_column(self, label, gen_fun):
        self.pd_item[label] = map(gen_fun, self.pd_item.iterrows())

    def add_negative(self, key, dictum, size, subst):

        def z(item, key, size, subst):
            nss = dictum.negative_sample(size, set([item[key]]))

            alist = []
            print item
            for ns in nss:
                item[key] = ns
                alist.append(item)

            print alist
            raw_input()

        def gen_negatives(item):
            nss = dictum.negative_sample(size, set([item[1][key]]))
            return nss

        def gen_item(item, ns, index):
            item[1][key] = ns[index]
            for (s_key, s_value) in subst:
                item[1][s_key] = s_value

            return item[1]

        # negatives = map(lambda x: z(x[1], key, size, subst), self.pd_item.iterrows())
        negatives = map(gen_negatives, self.pd_item.iterrows())
        new_items = map(lambda index:
                        map(lambda ins: gen_item(ins[0], ins[1], index), zip(
                            self.pd_item.iterrows(), negatives)),
                        xrange(size))

        for new_item in new_items:
            self.pd_item = self.pd_item.append(new_item)

        self.pd_item = self.pd_item.reset_index(drop=True)

        return

    def shuffle(self):
        self.pd_item = self.pd_item.reindex(np.random.permutation(
            self.pd_item.index)).reset_index(drop=True)

    def separate(self, train_rate, dev_rate):
        samples = len(self.pd_item)

        train_segment = int(train_rate * samples)
        dev_segment = int((train_rate + dev_rate) * samples)

        train = self.pd_item[0: train_segment]
        dev = self.pd_item[train_segment: dev_segment]
        test = self.pd_item[dev_segment:]

        return train, dev, test

    def get(self):
        return self.pd_item
    
    @staticmethod
    def merge_vectorizer(dictum_vectorizers):
        # ベクタライザの合成
        return lambda items: sp.hstack(
            map(lambda iv: iv[1](iv[0]), zip(items, dictum_vectorizers)))
