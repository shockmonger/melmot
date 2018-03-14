import sys
import numpy as np
from scipy.spatial import distance_matrix
from scipy.spatial import distance
from sklearn.metrics import average_precision_score
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt

# compute kmeans on num_parts sub-sequences with each data row
# 3 categories (with labels): ascending - 0, flat - 1, descending - 2
def tokenize(data, num_parts, visualize=False):
    w = int(data.shape[1] / num_parts)
    samples = np.reshape(data, (-1, w))
    samples = samples.transpose() - samples[:,0].transpose()
    samples = samples.transpose()
    asc = np.array(range(w))
    desc = np.array(range(0,-w,-1))
    flat = np.zeros(w)
    if visualize:
        plt.plot(np.vstack((asc, flat, desc)).transpose(),'bo-')
    kmeans = KMeans(n_clusters=3, init=np.vstack((asc, flat, desc)), n_init=1).fit(samples)
    if visualize:
        plt.plot(kmeans.cluster_centers_.transpose(),'ro-')
        plt.show()
    return kmeans.labels_.reshape((data.shape[0],-1))

# compute pyramidal mean of the data
# level N = 0 to 2^N parts division
def spatialHistogram(data, level):
    num_parts = 2**level
    features = np.empty(())
    for i in range(num_parts):
        fs = int(i*data.shape[1] / num_parts)
        fe = int((i+1)*data.shape[1] / num_parts)
        subfeatures = np.mean(data[:,fs:fe,:], axis=1)
        if i == 0:
            features = subfeatures
        else:        
            features = np.hstack((features, subfeatures))
    if level != 0:
        features = np.hstack((features, spatialHistogram(data, level-1)))
    return features

# compute sliding mean/stddev of the data
def slidingHistogram(data, num_parts, calc_mean=True):
    features = np.empty((data.shape[0],0))
    for p in range(num_parts):
        fs = int(p*data.shape[1] / num_parts)
        fe = int((p+1)*data.shape[1] / num_parts)
        if calc_mean:
            subfeatures = np.mean(data[:,fs:fe,:], axis=1)
            features = np.hstack([features, subfeatures])
        else:
            subfeatures = np.std(data[:,fs:fe,:], axis=1)
            features = np.hstack([features, subfeatures])
    return features
