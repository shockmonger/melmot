
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


# def readfile(stri):
#     fil = basefile+'/datadump/'+stri+'.tsv'
#     df1=pd.read_table(fil,header=None)
#     df1.columns=colHeads
#     return(df1)

# def qom(stri):
#     fil = basefile+'/datadump/'+stri+'.tsv'
#     df1=pd.read_table(fil,header=None)
#     df1.columns=colHeads
#     df = df1.iloc[:,2:]
#     qomval = numpy.sqrt(numpy.square(df).sum(axis =1))
#     return(qomval)