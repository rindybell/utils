'''
Created on 2017/04/15

@author: rindybell
'''
import numpy as np


class Batcher(object):

    def __init__(self, X, batch_size=32):
        self.X = X
        self.limit = X.shape[0]
        self.batch_size = batch_size
        self.current_position = 0

    def batch_gen(self):
        if self.batch_size == -1:
            return (True, self.X)

        next_position = min (self.current_position + self.batch_size, self.limit)
        batch_X = self.X[self.current_position: next_position]
        
        is_end = (self.limit == next_position)

        if is_end == True:
            self.current_position = 0
        else:
            self.current_position = next_position

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
