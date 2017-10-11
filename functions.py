import numpy, scipy, os, matplotlib, imageio
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.preprocessing import scale
from scipy.spatial import distance
from scipy.interpolate import splprep, splev
from numpy import linspace


import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
import scipy.signal as sg

basefile = '/home/tejaswik/Documents/CurrentProjects/melmot/'
colHeads=['id','frame','time','RHX','RHY','RHZ','LHX','LHY','LHZ']


parts = os.listdir(basefile+'data/ind/')

allpieces = {}
for i in range(0,len(parts),1):
    folder = basefile+'data/ind/'+parts[i]
    pieces = os.listdir(folder)
    allpieces['{0}'.format(parts[i])] = pieces

    
for key in allpieces:
    for i in range(0,32,1):
        allpieces[key][i] = allpieces[key][i][:-4]
        
pitches = os.listdir(basefile+'sound/pitch/')


participants = pd.read_table('/home/tejaswik/Documents/CurrentProjects/melmot/participants.csv',sep=';')

tracings = os.listdir('/home/tejaswik/Documents/CurrentProjects/melmot/data/normdatadump/')
for i in range(len(tracings)):
    tracings[i] = tracings[i][:-4]

for i in range(0,len(tracings)):
    file_name = tracings[i]+'.csv'
    y = upsamp(tracings[i])
    y.to_csv(file_name,sep='\t')

