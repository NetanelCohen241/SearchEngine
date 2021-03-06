from math import log

k1 = 1.5
b = 0.75

class Ranker(object):


    def score_BM25(self,n, f, N, dl, avgl, cf,title):
        K = self.compute_K(dl, avgl)
        idf = log((N+1)/n)
        second = ((k1 + 1) * f) / (K + f)
        return int(cf) * idf * second + title*int(cf) * idf * second *0.1

    def compute_K(self, dl, avgl):
        return k1 * ((1 - b) + b * (float(dl) / float(avgl)))