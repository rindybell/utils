# coding:utf-8
#
# Author: Masayuki Komai
#


""" imports """
import sys
import os
abspath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(abspath, "../"))
sys.path.append(os.path.join(abspath, "../src"))
import argparse
from dictum import Dictum
from padder import Padder
import numpy as np
""" variables """
""" arguments """


def def_args():
    parser = argparse.ArgumentParser(
        description="padderのテスト")

    parser.add_argument("-t", "--tsv", type=str,
                        dest="TSV",
                        help=u"TSVファイル",
                        default=None,
                        required=True)

    args = parser.parse_args()
    options = args.__dict__

    if None in options.values():
        parser.print_help()
        exit(-1)

    return options

""" functions """

""" main """


def main(options={}):
    tsv = open(options["TSV"], "r")
    tsv_file = map(lambda x: x.strip().split("\t"), tsv.readlines())
    dictum_vocab = Dictum(use_unknown=True, use_pad_symbol=True)
    dictum_label = Dictum()
    max_len = max(map(lambda x: len(x[1].split(" ")), tsv_file))
    padder_sen = Padder(max_sen=max_len)

    sequences = map(lambda x: x[1].strip().split(" "), tsv_file)
    pad_sequences = map(padder_sen.sentence_padding, sequences)

    labels = map(lambda x: x[0], tsv_file)
    map(dictum_vocab.push_list, pad_sequences)
    map(dictum_label.push, labels)
    dictum_vocab.locking()
    dictum_label.locking()

    print "Test 1."
    print np.array(map(dictum_vocab.map_symbol_to_id, pad_sequences))

    for i in map(dictum_vocab.map_id_to_symbol,
                 map(dictum_vocab.map_symbol_to_id, pad_sequences)):
        print " ".join(i)

    print "\nTest 2."
    padder_doc = Padder(max_sen=4, max_doc=4,
                        auto_sen_padding=True, auto_doc_padding=True)

    pad_doc = padder_doc.doc_padding(sequences)
    for i in map(dictum_vocab.map_id_to_symbol,
                 map(dictum_vocab.map_symbol_to_id, pad_doc)):
        print " ".join(i)


if __name__ == "__main__":
    options = def_args()
    main(options)
