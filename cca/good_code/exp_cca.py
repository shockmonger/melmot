import sys
import numpy as np
from sklearn.model_selection import ParameterGrid
from sklearn.cross_decomposition import CCA
from sklearn.cross_decomposition import PLSRegression

from mm_features import *
from retrieval_metrics import meanAP2

##########
# MAIN
##########

# number of samples for training
spidx = 500

motion = np.load('motiondata1.npy')
music = np.load('melodiesFeatures.npy')
motion = np.nan_to_num(motion)
music = np.nan_to_num(music)

# zero meaned
for i in range(motion.shape[2]):
    motion[:,:,i] = (motion[:,:,i] - motion[:,:,i].mean(axis=0))# / motion[:,:,i].std(axis=0)
for i in range(music.shape[2]):
    music[:,:,i] = (music[:,:,i] - music[:,:,i].mean(axis=0))# / music[:,:,i].std(axis=0)

musiclabels = np.load('melodiesLabels.npy')

param_grid = {'num_parts' : [10, 20, 30, 40, 50, 60, 100], 'cca_d':range(2,20,2), 'dist':['cosine', 'correlation']}


bestpp = 0

for param in list(ParameterGrid(param_grid)):
    #motdata = spatialHistogram(motion, 2)
    #musdata = spatialHistogram(music, 2)
    motdata = slidingHistogram(motion, param['num_parts'], False)
    musdata = slidingHistogram(music, param['num_parts'], False)
    #motdata = tokenize(motion[:,:,1], param['num_parts'])
    #musdata = tokenize(music[:,:,0], param['num_parts'])
    #motdata = motion[:,:,1]
    #musdata = music[:,:,0]
    
    # save data
    #np.savetxt('motdata.txt', motdata, delimiter=' ', fmt='%4.2f')
    #np.savetxt('musdata.txt', musdata, delimiter=' ', fmt='%4.2f')

    # vanilla CCA
    cca = CCA(n_components=min(param['cca_d'], motdata.shape[1], musdata.shape[1]), scale=False)#np.minimum(motdata.shape[1], musdata.shape[1]))
    cca.fit(motdata[:spidx,:], musdata[:spidx,:])
    motc, musc = cca.transform(motdata, musdata)

    # kernel CCA
    #cca = rcca.CCA(kernelcca = True, ktype='gaussian', reg=.05, numCC=np.minimum(motdata.shape[1], musdata.shape[1]))
    #cca = rcca.CCACrossValidate(kernelcca=False, numCCs = [1, 2, 3, 4], regs = [0., 1e2, 1e4, 1e6])
    #cca.train([motdata, musdata])
    #allcorrs = cca.validate([motdata, musdata])
    #print(cca.cancorrs)
    #print(allcorrs[0])
    #print(allcorrs[1])

    #plt.plot(allcorrs[0], 'ro-')
    #plt.plot(allcorrs[1], 'go-')
    #plt.plot(cca.cancorrs, 'ro')
    #plt.show()
    #sys.exit()

    #print(cca.x_weights_)
    #print(cca.y_weights_)
    #print(cca.x_loadings_)
    #print(cca.y_loadings_)

    # calc mean average precision
    pp = []

    for tmusiclabels, tmotc, tmusc in [(musiclabels[:spidx], motc[:spidx,:], musc[:spidx,:]), (musiclabels[spidx:], motc[spidx:,:], musc[spidx:,:])]:
        umusiclabels, uindices = np.unique(tmusiclabels, return_index=True)
        if umusiclabels.shape[0] != 16:
            raise AssertionError
        #Dxy = distance_matrix(tmotc, tmusc, p=1)
        Dxy = distance.cdist(tmotc, tmusc[uindices,:], param['dist'])
        pp.append(meanAP2(Dxy, tmusiclabels, uindices))
    bestpp = max(bestpp, pp[1])
    print(param, 'Train mAP: ', "{:2.3f}".format(pp[0]), ' Test mAP: ', "{:2.3f}".format(pp[1]))
    if bestpp == pp[1]:
        print('-------Best-so-far-------')

