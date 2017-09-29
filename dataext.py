'''data extraction'''

import funcs

import numpy, scipy, os, matplotlib, imageio
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.preprocessing import scale

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


'''Functions'''
def settostrat(stri,y):
    s ='s'+str(y)
    eval(s).append(stri)
    return

    
def readfile(stri):
    fil = basefile+'/normdatadump/'+stri+'.csv'
    df1=pd.read_table(fil,header=None)
    df1.columns=colHeads
    return(df1)

def readtsv(stri):
    fil = basefile+'data/datadump/'+stri+'.tsv'
    df1=pd.read_table(fil,header=None)
    cols=['frame','time','RHX','RHY','RHZ','LHX','LHY','LHZ']
    df1.columns=cols
    return(df1)

def qomtsv(stri):
    fil = basefile+'data/datadump/'+stri+'.tsv'
    df1=pd.read_table(fil,header=None)
    cols=['frame','time','RHX','RHY','RHZ','LHX','LHY','LHZ']
    df1.columns=cols
    df = df1.iloc[:,2:]
    qomval = numpy.sqrt(numpy.square(df).sum(axis =1))
    return(qomval)


def qom(stri):
    fil = basefile+'data/normdatadump/'+stri+'.csv'
    df1=pd.read_table(fil,header=None)
    df1.columns=colHeads
    df = df1.iloc[:,2:]
    qomval = numpy.sqrt(numpy.square(df).sum(axis =1))
    return(qomval)

def qomnew(stri):
    fil = basefile+'data/normdatadump/'+stri+'.csv'
    df1=pd.read_table(fil,header=None)
    df1.columns=colHeads
    df = df1.iloc[:,2:]
    qomval = numpy.sqrt(numpy.square(df).sum(axis =1))
    return(qomval)

def getlhrh(stri):
    lh = makedf(stri)[:,2:4]
    rh = makedf(stri)[:,5:7]
    return(lh,rh)
    
def upsamp(stri):
    y = readfile(stri)
    y = sg.resample(y,600)
    y = scale(y, axis=0, with_mean=True, with_std=True, copy=True )
    y = pd.DataFrame(y)
    return(y)

def ups(array):
    y = sg.resample(array,600)
#    y = scale(y,axis=0,with_mean=True,with_std=True,copy = True)
    y = pd.DataFrame(y)
    return(y)

def readpitch(stri):
    fil = basefile+'sound/pitch/'+stri
    z = pd.read_csv(fil, sep='   ', engine = 'python',header =0)
    return(z)
    

def returnDetails(string):
    split = string.split('_')
    partID = split[0]
    melID = split[1]
    typeID = split[2]
    return{'partID':partID, 'melID':melID, 'typeID':typeID}

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


'''Finding all pieces that have MelID bet 1 and 16'''
normMels = []
synMels = []
im = [1,2,3,4,17,18,19,20]
jo = [5,6,7,8,21,22,23,24]
sc = [9,10,11,12,25,26,27,28]
vo = [13,14,15,16,29,30,31,32]
alljo, allim, allsc, allvo = ([] for i in range(4))
s1,s2,s3,s4,s5,s6 = ([]for i in range(6))
def settostrat(stri,y):
    s ='s'+str(y)
    eval(s).append(stri)
    return

folder = basefile+'data/datadump/'
pieces = os.listdir(folder)
for i in range(0,len(pieces),1):
    pieces[i] = pieces[i][:-4]
    melID = returnDetails(pieces[i])['melID']
    typeID = returnDetails(pieces[i])['typeID']
    settostrat(pieces[i],typeID) #distribute according to piece ID
    if int(melID) <= 16:
        normMels.append(pieces[i]) 
    elif int(melID)>16:
        synMels.append(pieces[i])
    if int(melID) in im:
        allim.append(pieces[i])
    elif int(melID) in jo:
        alljo.append(pieces[i])
    elif int(melID) in sc:
        allsc.append(pieces[i])
    elif int(melID) in vo:
        allvo.append(pieces[i])

        
pitches = []
fig, ax9= plt.subplots()
for i in range(1,17,1):
    strings = str(i)+'.txt'
    pitches.append(ups(readpitch(strings)['F0_Hz']))


'''plot genre qoms'''
qomjo,qomvo,qomim,qomsc = ([]for i in range(4))
fig, ax1 = plt.subplots()
for i in range(0,len(alljo)):
    qomjo.append(qom(alljo[i]))
    # ax1.plot(qomjo[i])
for i in range(0,len(allvo)):
    qomvo.append(qom(allvo[i]))
    # ax1.plot(qomvo[i])
for i in range(0,len(allsc)):
    qomsc.append(qom(allsc[i]))
    # ax1.plot(qomsc[i])
for i in range(0,len(allim)):
    qomim.append(qom(allim[i]))
    # ax1.plot(qomim[i])



'''normvs syn'''
qomnorm = []
qomsyn = []
# fig, ax2 = plt.subplots()
for i in range(0,len(normMels)):
    qomnorm.append(qom(normMels[i]))
for i in range(0,len(synMels)):
    qomsyn.append(qom(synMels[i]))
    # ax2.plot(qomsyn[i])



'''plot all qoms of strategies 1-6'''
qoms1,qoms2,qoms3,qoms4,qoms5,qoms6 = ([]for i in range(6))
fig, ax = plt.subplots()
for i in range(0,len(s1)):
    qoms1.append(qom(s1[i]))
    # ax.plot(qoms1[i])
for i in range(0,len(s2)):
    qoms2.append(qom(s2[i]))
    # ax.plot(qoms2[i])
for i in range(0,len(s3)):
    qoms3.append(qom(s3[i]))
    # ax.plot(qoms3[i])
for i in range(0,len(s4)):
    qoms4.append(qom(s4[i]))
    # ax.plot(qoms4[i])
for i in range(0,len(s5)):
    qoms5.append(qom(s5[i]))
    # ax.plot(qoms5[i])
for i in range(0,len(s6)):
    qoms6.append(qom(s6[i]))
    # ax.plot(qoms6[i])


