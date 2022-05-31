
from math import sqrt


def s2(xs):
    average = sum(xs)/len(xs)
    diffs2 = sum([(x-average)**2 for x in xs])
    return diffs2 / (len(xs) - 1)

def get_paired_confidence_interval(xs1, xs2):
    assert len(xs1) == len(xs2) 
    n = len(xs1)
    z = [xs2[i] - xs1[i] for i in range(n)]
    z_bar = sum(z) / n
    s_z2 = sum([(z_j - z_bar)**2 for z_j in z]) / (n - 1)
    t = 2.262 # for n=10, alpha = 0.05 
    plusminus = t * sqrt(s_z2/n)
    return (z_bar - plusminus, z_bar + plusminus)
