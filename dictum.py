# coding: utf-8

'''
Created on 2017/04/15

@author: rindybell
'''

from collections import Counter
import gensim
import numpy as np


class Dictum(object):
    '''
    classdocs
    '''

    def __init__(self, use_unknown=False, use_pad_symbol=False):
        '''
        Constructor
        '''
        self.dictum = {}
        self.term = Counter()
        self.idf_m = Counter()
        self.pixel_amount = Counter()
        self.sample_amount = 0.0
        self.inv_dictum = {}
        self.is_locked = False
        self.unknown_symbol = "<u>"
        self.pad_symbol = "*"

        if use_pad_symbol:
            self.push(self.pad_symbol)

        if use_unknown:
            self.push(self.unknown_symbol)

    def push(self, symbol):
        if self.is_locked == True:
            return

        if not symbol in self.dictum:
            self.dictum[symbol] = len(self.dictum)
            self.inv_dictum[self.dictum[symbol]] = symbol

        self.term[symbol] += 1

    def push_img(self, img):
        if self.is_locked == True:
            return

        (channel, column, row) = img.shape
        item_set = set()

        for ch in range(channel):
            for co in range(column):
                for ro in range(row):
                    key = (ch, img[ch, co, ro])
                    self.push(key)
                    item_set.add(key)

        for i in item_set:
            self.idf_m[i] += 1
            self.pixel_amount[i] += 1

    def push_list(self, symbol_list):
        if self.is_locked == True:
            return

        map(self.push, symbol_list)

        for symbol in set(symbol_list):
            self.idf_m[symbol] += 1

        self.sample_amount += 1

        return

    def locking(self):
        self.locked = True

    def symbol_to_id(self, symbol):
        if symbol in self.dictum:
            return self.dictum[symbol]

        return self.dictum[self.unknown_symbol]

    def symbol_to_vec(self, symbol):
        return self.id_to_vec(self.symbol_to_id(symbol))

    def id_to_symbol(self, _id):
        if _id in self.inv_dictum:
            return self.inv_dictum[_id]

        return "<error>"

    def id_to_vec(self, _id):
        retvec = np.zeros(self.size())
        retvec[_id] = 1

        return retvec

    def vec_to_id(self, vec):
        return np.argmax(vec)

    def vec_to_symbol(self, vec):
        _id = self.vec_to_id(vec)
        return self.id_to_symbol(_id)

    def symbol_to_idf(self, symbol):
        if self.idf_m[symbol] == 0:
            idf = 0.0
        else:
            idf = np.log(self.sample_amount / self.idf_m[symbol])

        return (self.symbol_to_id(symbol), idf)

    def img_tf(self, img):
        ret_vec = np.zeros(self.size())
        (channel, column, row) = img.shape
        sigma_m = channel * column * row

        for ch in range(channel):
            for co in range(column):
                for ro in range(row):
                    key = (ch, img[ch, co, ro])
                    ret_vec[self.symbol_to_id(key)] += 1

        return ret_vec / sigma_m

    def img_idf(self, img):
        ret_vec = np.zeros(self.size())
        (channel, column, row) = img.shape

        for ch in range(channel):
            for co in range(column):
                for ro in range(row):
                    key = (ch, img[ch, co, ro])
                    (_id, idf) = self.symbol_to_idf(key)
                    ret_vec[_id] = idf

        return ret_vec

    def img_tfidf(self, img):
        return self.img_tf(img) * self.img_idf(img)

    def size(self):
        return len(self.dictum)

    def vec_tf(self, symbol_list, is_binary=False):
        sigma_m = len(symbol_list) * 1.0
        ret_vec = np.zeros(self.size())

        for _id in self.map_symbol_to_id(symbol_list):
            if is_binary:
                ret_vec[_id] = 1
            else:
                ret_vec[_id] += 1

        return ret_vec / sigma_m

    def vec_idf(self, symbol_list):
        ret_vec = np.zeros(self.size())

        symbol_vocab = set(symbol_list)

        for (_id, idf) in self.map_symbol_to_idf(symbol_list):
            ret_vec[_id] = idf

        return ret_vec

    def vec_tfidf(self, symbol_list):
        return self.vec_tf(symbol_list) * self.vec_idf(symbol_list)

    def map_symbol_to_id(self, symbol_list):
        return map(self.symbol_to_id, symbol_list)

    def map_symbol_to_vec(self, symbol_list):
        return np.array(map(self.symbol_to_vec, symbol_list))

    def map_id_to_symbol(self, id_list):
        return map(self.id_to_symbol, id_list)

    def map_id_to_vec(self, id_list):
        return np.array(map(self.id_to_vec, id_list))

    def map_vec_to_id(self, vec_list):
        return map(self.vec_to_id, vec_list)

    def map_vec_to_symbol(self, vec_list):
        return map(self.vec_to_symbol, vec_list)

    def map_symbol_to_idf(self, symbol_list):
        return map(self.symbol_to_idf, symbol_list)

    def map_symbol_to_vec(self, symbol_list, mode="tfidf", do_unit_vec=False):
        if mode == "tfidf":
            result_vec = self.vec_tfidf(symbol_list)
        elif mode == "tf":
            result_vec = self.vec_tf(symbol_list)
        elif mode == "idf":
            result_vec = self.vec_tfidf(symbol_list)
        else:
            sys.stderr.write("Error: Undefined command in symbol_list_to_vec.")
            exit(-1)

        if do_unit_vec == True:
            return gensim.matutils.unitvec(result_vec, norm="l2")
        else:
            return result_vec

    def size(self):
        return len(self.dictum)

    def pad(self, sequence, max_len, pad_style="right"):
        assert len(sequence) <= max_len
        if pad_style == "right":
            return sequence + (max_len - len(sequence)) * [self.pad_symbol]
        elif pad_style == "left":
            return (max_len - len(sequence)) * [self.pad_symbol] + sequence
        else:
            sys.stderr.write("Error: Undefined mode in pad.")

    @staticmethod
    def preprocess_matirx(M, do_zero_center=True, do_normalize=True):
        if do_zero_center == True:
            M -= np.mean(M)
        if do_normalize == True:
            M /= np.std(M)

        return M
