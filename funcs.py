
import numpy, scipy, os, matplotlib, imageio
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.preprocessing import scale
from scipy.spatial import distance


import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
import scipy.signal as sg

basefile = '/home/tejaswik/Documents/CurrentProjects/melmot/'
colHeads=['id','RHX','RHY','RHZ','LHX','LHY','LHZ']

colHeads_old=['id','frame','time','RHX','RHY','RHZ','LHX','LHY','LHZ']

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




'''Functions'''
def settostrat(stri,y):
    s ='s'+str(y)
    eval(s).append(stri)
    return

    
def readfile(stri):
    fil = basefile+'data/normdatadump/'+stri+'.csv'
    df1=pd.read_table(fil,header=0)
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
    df1=pd.read_table(fil,header=1)
    df1.columns=colHeads
    df = df1.iloc[:,1:]
    qomval = numpy.sqrt(numpy.square(df).sum(axis =1))
    return(qomval)

def qomnew(stri):
    fil = basefile+'data/normdatadump/'+stri+'.csv'
    df1=pd.read_table(fil,header=1)
    df1.columns=colHeads
    df = df1.iloc[:,1:]
    qomval = numpy.sqrt(numpy.square(df).sum(axis =1))
    return(qomval)


def getlhrh(stri):
    rh = readfile(stri).iloc[:,1:4]
    lh = readfile(stri).iloc[:,4:7]
    return{'lh':lh,'rh':rh}

def upsamp(stri):
    y = readfile(stri)
    y = sg.resample(y,600)
    y = scale(y, axis=0, with_mean=True, with_std=True, copy=True )
    y = pd.DataFrame(y)
    return(y)

def ups(array):
    y = sg.resample(array,600)
    y = pd.DataFrame(y)
    return(y)

def readpitch(stri):
    fil = basefile+'sound/pitch/'+stri
    z = pd.read_csv(fil, sep='   ', engine = 'python',header =0)
    return(z)
    
def maxminret(stri):
    qy = qom(stri)
    return{'max':max(qy),'min':min(qy)}

def maxminz(stri):
    r = readfile(stri)['RHZ']   
    l = readfile(stri)['LHZ']
    zmax = max(r)
    zmin = min(r)
    if max(l)>max(r):
        zmax = max(l)
    if min(l)<min(r):
        zmin = min(l)
    return{'zmax':zmax,'zmin':zmin}

def handdist(stri):
    rh = pd.DataFrame.as_matrix(readfile(stri).iloc[:,1:4])
    lh = pd.DataFrame.as_matrix(readfile(stri).iloc[:,4:7])
    dist = []
    for i in range(len(rh)):
        dist.append(distance.euclidean(lh[i],rh[i]))
    return(dist)

def displrh(stri):
    rh = pd.DataFrame.as_matrix(readfile(stri).iloc[:,1:4])
    lh = pd.DataFrame.as_matrix(readfile(stri).iloc[:,4:7])
    distlh = []
    distrh = []
    for i in range(1,len(lh)):
        distlh.append(distance.euclidean(lh[i],lh[i-1]))
        distrh.append(distance.euclidean(rh[i],rh[i-1]))
    return{'distlh':sum(distlh),'distrh':sum(distrh)}


def displyax(stri):
    r = readfile(stri)['RHZ']   
    l = readfile(stri)['LHZ']
    e = 0   
    for i in range(1,len(l)):
        e = e+distance.euclidean(l[i],l[i-1])+distance.euclidean(r[i],r[i-1])
    return(e)


def returnDetails(string):
    split = string.split('_')
    partID = split[0]
    melID = split[1]
    typeID = split[2]
    return{'partID':partID, 'melID':melID, 'typeID':typeID}


# def vel(string):
#     for i in range()

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value
