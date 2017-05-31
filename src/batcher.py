'''
Created on 2017/04/15

@author: rindybell
'''
import numpy as np


class Batcher(object):

    def __init__(self, X, batch_size=32):
        self.X = X
        self.batch_size = batch_size
        self.current_position = 0

    def batch_gen(self):
        if self.batch_size == -1:
            return (True, self.X)

        batch_X = np.array(
            self.X[self.current_position: self.current_position + self.batch_size])

        self.current_position += self.batch_size

        x_size = batch_X.shape[0]

        is_end = (x_size != self.batch_size)

        if is_end == True:
            self.current_position = 0

        return (is_end, batch_X)

    def ranodm_gen(self):
        if self.batch_size == -1:
            return (True, self.X)

        rand_indices = map(lambda _: np.random.randint(
            o, len(self.X)), range(self.batch_size))
        ret_tensor = np.array(map(lambda x: self.X[x], self.X))
        return ret_tensor

    @staticmethod
    def simple_out(item):
        (is_end, batch_X) = item

        print "[is_end]: {}, [batch_X]: {}".format(is_end, batch_X.shape)
