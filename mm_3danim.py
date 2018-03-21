import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from os import listdir
from os.path import isfile, join
from sklearn.decomposition import PCA

slabel = 11

pitchdata = np.loadtxt('C:\\Users\\uditroy\\Documents\\data\\applsci-08-00135-s001\\applsci-243313-supplementary\\data\\pitch\\' \
                        + str(slabel) + '.txt', usecols=(1), skiprows=1)

fig = plt.figure(0)
plt.plot(pitchdata)
plt.draw()

mydatapath='C:\\Users\\uditroy\\Documents\\data\\applsci-08-00135-s001\\applsci-243313-supplementary\\data\\motionTracings'
onlyfiles = [f for f in listdir(mydatapath) if isfile(join(mydatapath, f))]
labels = []

truelabels = np.load('dataset\\mmlabels.npy')

print(sum((truelabels == slabel).astype(int)))

# extract labels from filenames
for file in onlyfiles:
    parts = file.split('_')
    v = int(parts[1])
    if v > 16:
        v = v - 16
    labels.append(v)
    
labels = np.array(labels)
print(sum((labels == slabel).astype(int)))

plot3D = True

dataset = []
fig = plt.figure(1)
for idx, file in enumerate(onlyfiles):
    if labels[idx] != slabel:
        continue
    #cols=['frame','time','RHX','RHY','RHZ','LHX','LHY','LHZ']
    datum = np.loadtxt(mydatapath + '\\' + file, usecols=(2,3,4,5,6,7))
    dataset.append(datum)
    if plot3D:
        ax = fig.add_subplot(111, projection = '3d')
        ax.plot(datum[:, 0], datum[:, 1], datum[:, 2],'r', label='left')
        ax.plot(datum[:, 3], datum[:, 4], datum[:, 5],'b', label='right')
        ax.plot(datum[0:1, 0], datum[0:1, 1], datum[0:1, 2],'ko')
        ax.plot(datum[0:1, 3], datum[0:1, 4], datum[0:1, 5],'ko')
        ax.legend()
    else:
        pcal = PCA(n_components=1)
        pcar = PCA(n_components=1)
        pcal.fit(datum[:,(0,1,2)])
        pcar.fit(datum[:,(3,4,5)])
        lhsnew = pcal.transform(datum[:,(0,1,2)])
        rhsnew = pcal.transform(datum[:,(3,4,5)])
        plt.plot(lhsnew, 'r', label='left')
        plt.plot(rhsnew, 'b', label='right')
        plt.legend()
    #plt.show()
    plt.pause(1) # <-------
    plt.waitforbuttonpress(0)
    #plt.close(fig)
    plt.clf()
    
