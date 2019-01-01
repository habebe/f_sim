import math
import statistics

class StreamingStat:
    def __init__(self):
        self.m = 0
        self.v = 0
        self.k = 0

    def push(self,x):
        if self.k == 0:
            self.m = x
            self.v = 0
        else:
            m_previous = self.m
            v_previous = self.v
            self.m = m_previous + (x - m_previous) / self.k
            self.v = v_previous + (x - m_previous) * (x - self.m)
            pass
        self.k += 1

    def mean(self):
        return self.m

    def variance(self):
        if self.k <= 0:
            return 0
        else:
            return (self.v) / (self.k - 1)

    def stddev(self):
        return math.sqrt(self.variance())

