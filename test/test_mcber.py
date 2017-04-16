# coding: utf-8
'''
Created on 2017/04/16

@author: rindybell
'''
import unittest
from mcber import Mcber


class Test(unittest.TestCase):

    def test_parse(self):
        sentence = "東京都に行った。"
        print "test_parse"
        m1 = Mcber()
        print " ".join(m1.parse(sentence))

        m2 = Mcber(lemma=False)
        print " ".join(m2.parse(sentence))

    def test_wakati(self):
        sentence = "東京都に行った。"
        print "test_wakati"
        m1 = Mcber()
        print m1.wakati(sentence)

        m2 = Mcber(lemma=False)
        print m2.wakati(sentence)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
