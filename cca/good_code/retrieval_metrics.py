import numpy as np
from scipy.spatial import distance_matrix

def precision_at_k(r, k):
    """Score is precision @ k
    Relevance is binary (nonzero is relevant).
    >>> r = [0, 0, 1]
    >>> precision_at_k(r, 1)
    0.0
    >>> precision_at_k(r, 2)
    0.0
    >>> precision_at_k(r, 3)
    0.33333333333333331
    >>> precision_at_k(r, 4)
    Traceback (most recent call last):
        File "<stdin>", line 1, in ?
    ValueError: Relevance score length < k
    Args:
        r: Relevance scores (list or numpy) in rank order
            (first element is the first item)
    Returns:
        Precision @ k
    Raises:
        ValueError: len(r) must be >= k
    """
    assert k >= 1
    r = np.asarray(r)[:k] != 0
    if r.size != k:
        raise ValueError('Relevance score length < k')
    return np.mean(r)


def average_precision(r):
    """Score is average precision (area under PR curve)
    Relevance is binary (nonzero is relevant).
    >>> r = [1, 1, 0, 1, 0, 1, 0, 0, 0, 1]
    >>> delta_r = 1. / sum(r)
    >>> sum([sum(r[:x + 1]) / (x + 1.) * delta_r for x, y in enumerate(r) if y])
    0.7833333333333333
    >>> average_precision(r)
    0.78333333333333333
    Args:
        r: Relevance scores (list or numpy) in rank order
            (first element is the first item)
    Returns:
        Average precision
    """
    r = np.asarray(r) != 0
    out = [precision_at_k(r, k + 1) for k in range(r.size) if r[k]]
    if not out:
        return 0.
    return np.mean(out)

def meanAP(X,Y, Yl, v):
    dXY = distance_matrix(X,Y, p=2)
    meanap = 0
    tXY = np.empty((0 ,v))
    for i in range(dXY.shape[0]):
        ind = np.argsort(dXY[i,:])
        tY = Yl[ind]
        tY = np.isin(tY, Yl[i])
        tY = tY.astype(int)
        tY = tY[:v]
        app = average_precision(tY)
        tXY = np.vstack((tXY, tY))
        meanap = meanap + app
    return meanap/dXY.shape[0]

def meanAP2(dXY, Ygt, Yunq):
    """
    Calculates mean average precision
    Inputs:
        dXY: N x D distance matrix for N queries and D items in retrieval dataset
        Ygt: N length array for ground truth for each query
        Yunq: indices of unique ground truth labels from Ygt (complicated, ask me)
    """
    meanap = 0
    tXY = np.empty((0 ,Yunq.shape[0]))
    for i in range(dXY.shape[0]):
        ind = np.argsort(dXY[i,:])
        tY = Ygt[Yunq[ind]]
        tY = np.isin(tY, Ygt[i])
        tY = tY.astype(int)
        app = average_precision(tY)
        meanap = meanap + app
    return meanap/dXY.shape[0]
