import sys
import numpy as np
from sklearn.cross_decomposition import CCA
import matplotlib.pyplot as plt

def spatialHistogram(data, level):
    num_parts = 2**level
    features = np.array([])
    for i in range(num_parts):
        fs = int(i*data.shape[1] / num_parts)
        fe = int((i+1)*data.shape[1] / num_parts)
        #print('Level ', level, ' fs ', fs, ' fe ', fe)
        subfeatures = np.mean(data[:,fs:fe,:], axis=1)
        if i == 0:
            features = subfeatures
        else:        
            features = np.hstack((features, subfeatures))
    if level != 0:
        features = np.hstack((features, spatialHistogram(data, level-1)))
    return features

motion = np.load('motiondata.npy')
music = np.load('musicFeatures.npy')

# sanity check: no nan/inf values in data
# fixme
#print(np.argwhere(np.isnan(motion)))
print(np.argwhere(np.isnan(music)))

print(motion.shape, music.shape)

sys.exit() # remove me

motdata = spatialHistogram(motion, 0)
musdata = spatialHistogram(music, 0)
print(motdata.shape, musdata.shape)

# fixme
motdata = np.nan_to_num(motdata)
musdata = np.nan_to_num(musdata)

# vanilla CCA
cca = CCA(n_components=2)
cca.fit(motdata, musdata)
motc, musc = cca.transform(motdata, musdata)

print(cca.x_weights_)
print(cca.y_weights_)

print(cca.x_loadings_)
print(cca.y_loadings_)

# visualize
visualize = False
if visualize:
    for i in range(0, motc.shape[0], 10):
        for k in range(i, i + 10):
            pt = motc[k,:]
            # plot motion (blue) music (red) pair
            plt.plot([motc[k,0], musc[k,0]], [motc[k, 1], musc[k, 1]], 'ro-')
            plt.plot([motc[k,0]], [motc[k, 1]], 'bo')
        plt.show()
