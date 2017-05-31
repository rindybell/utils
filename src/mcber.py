# coding: utf-8
'''
Created on 2017/04/16

@author: rindybell
'''
import MeCab
import neologdn


class Mcber(object):
    '''
    classdocs
    '''

    def __init__(self, lemma=True):
        '''
        Constructor
        '''
        self.mcber = MeCab.Tagger("-Ochasen").parse
        if lemma == True:
            self.index = 2
        else:
            self.index = 0

    def parse(self, sentence):
        sentence = neologdn.normalize(
            sentence.decode("utf-8")).encode("utf-8")
        wakati = map(lambda x: x.strip().split("\t")[self.index],
                     self.mcber(sentence).strip().split("\n")[:-1])
        return wakati

    def wakati(self, sentence):
        return " ".join(self.parse(sentence))

if __name__ == "__main__":
    mc = Mcber()
    mc.parse("東京都に行った。")
