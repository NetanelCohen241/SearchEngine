from math import log

k1 = 1.2
b = 0.75

class Ranker(object):


    def score_BM25(self,n, f, N, dl, avgl):
        K = self.compute_K(dl, avgl)
        idf = log((N - n + 0.5)/(n + 0.5))
        second = ((k1 + 1) * f) / (K + f)
        return idf * second

    def compute_K(self, dl, avgl):
        return k1 * ((1 - b) + b * (float(dl) / float(avgl)))