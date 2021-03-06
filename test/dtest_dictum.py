# coding:utf-8
#
# Author: Masayuki Komai
#


""" imports """
import sys
import os
abspath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(abspath, "../"))
import argparse
from dictum import Dictum
import numpy as np
""" variables """
""" arguments """


def def_args():
    parser = argparse.ArgumentParser(
        description="dictumのテスト")

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
    sequences = map(lambda x: dictum_vocab.pad(
        x[1].split(" "), max_len), tsv_file)
    labels = map(lambda x: x[0], tsv_file)
    map(dictum_vocab.push_list, sequences)
    map(dictum_label.push, labels)
    dictum_vocab.locking()
    dictum_label.locking()

    print np.array(map(dictum_vocab.map_symbol_to_id, sequences))

    for i in map(dictum_vocab.map_id_to_symbol,
                 map(dictum_vocab.map_symbol_to_id, sequences)):
        print " ".join(i)

    print np.array(map(dictum_label.symbol_to_id, labels))

    print np.array(map(lambda x: dictum_vocab.map_symbol_to_vec(x, mode="tf"), sequences))
    print np.array(map(dictum_vocab.map_symbol_to_vec, sequences))

    print "test. 3"
    dictum_vocab.prune_vocab(min_count=2)

    print np.array(map(dictum_vocab.map_symbol_to_id, sequences))

    for i in map(dictum_vocab.map_id_to_symbol,
                 map(dictum_vocab.map_symbol_to_id, sequences)):
        print " ".join(i)


if __name__ == "__main__":
    options = def_args()
    main(options)
