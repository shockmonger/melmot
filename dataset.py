execfile('/home/tejaswik/Documents/CurrentProjects/melmot/funcs.py')

tracings = os.listdir('/home/tejaswik/Documents/CurrentProjects/melmot/data/normdatadump/')
for i in range(len(tracings)):
    tracings[i] = tracings[i][:-4]

im = [1,2,3,4,17,18,19,20]
jo = [5,6,7,8,21,22,23,24]
sc = [9,10,11,12,25,26,27,28]
vo = [13,14,15,16,29,30,31,32]
    
key, handstrat, participant, melody, sex, age, score, genre,proc, qoms, handdists, rz, lz  = ([] for i in range(13))
cols1=['key', 'handstrat', 'participant', 'melody', 'sex', 'age', 'score', 'genre','proc', 'qom', 'handdist', 'rz', 'lz']

for i in range(len(tracings)):
    key.append(i)
    handstrat.append(returnDetails(tracings[i])['typeID'])
    partic = returnDetails(tracings[i])['partID']
    participant.append(partic)
    melID = returnDetails(tracings[i])['melID']
    melody.append(melID)
    sex.append(list(participants.loc[participants.index[int(partic)],['sex']])[0])
    age.append(int(participants.loc[participants.index[int(partic)],['age']]))
    score.append(int(participants.loc[participants.index[int(partic)],['scoreMus']]))
    qoms.append(qomnew(tracings[i]))
    handdists.append(handdist(tracings[i]))
    rz.append(readfile(tracings[i])['RHZ'])
    lz.append(readfile(tracings[i])['LHZ'])
    if int(melID) in im:
        genre.append('im')
    elif int(melID) in jo:
        genre.append('jo')
    elif int(melID) in sc:
        genre.append('sc')
    elif int(melID) in vo:
        genre.append('vo')
    if int(melID) <=16:
        proc.append('norm')
    elif int(melID) >=16:
        proc.append('syn')

for i in range(len(key)):
    dataset = pd.DataFrame(zip(key,handstrat,participant,melody,sex,age,score,genre,proc,qoms,handdists,rz,lz))
    dataset.columns=cols1


#pitches dataset
pitches = []
for i in range(1,17,1):
    strings = str(i)+'.txt'
    pitches.append(ups(readpitch(strings)['F0_Hz']))

    
pitch = pd.DataFrame(pitches)
pitch.columns = ['f0']



# avdataset, dataset separate
key,handstrat,participant,melody,sex,age,score,genre,proc,qommax,qommin,qomav,handdistmax,handdistmin,handdistav,zmax,zmin,distlh,distrh = ([] for i in range(19))
cols2=['key','handstrat','participant','melody','sex','age','score','genre','proc','qommax','qommin','qomav','handdistmax','handdistmin','handdistav','zmax','zmin','distlh','distrh']


for i in range(len(tracings)):
    key.append(i)
    handstrat.append(int(returnDetails(tracings[i])['typeID']))
    partic = int(returnDetails(tracings[i])['partID'])
    participant.append(partic)
    melID = int(returnDetails(tracings[i])['melID'])
    melody.append(melID)
    sex.append(list(participants.loc[participants.index[partic],['sex']])[0])
    age.append(int(participants.loc[participants.index[partic],['age']]))
    score.append(int(participants.loc[participants.index[partic],['scoreMus']]))
    if int(melID) in im:
        genre.append('im')
    elif int(melID) in jo:
        genre.append('jo')
    elif int(melID) in sc:
        genre.append('sc')
    elif int(melID) in vo:
        genre.append('vo')
    if int(melID) <=16:
        proc.append('norm')
    elif int(melID) >=16:
        proc.append('syn')
    qommax.append(max(qom(tracings[i])))
    qommin.append(min(qom(tracings[i])))
    qomav.append(numpy.mean(qom(tracings[i])))
    handdistmax.append(max(handdist(tracings[i])))
    handdistmin.append(min(handdist(tracings[i])))
    handdistav.append(numpy.mean(handdist(tracings[i])))
    zmax.append(maxminz(tracings[i])['zmax'])
    zmin.append(maxminz(tracings[i])['zmin'])
    distlh.append(displrh(tracings[i])['distlh'])
    distrh.append(displrh(tracings[i])['distrh'])

for i in range(len(key)):
    avdataset = pd.DataFrame(zip(key,handstrat,participant,melody,sex,age,score,genre,proc,qommax,qommin,qomav,handdistmax,handdistmin,handdistav,zmax,zmin,distlh,distrh))
    avdataset.columns=cols2

    	


 # continuous curves dataset
key,handstrat,participant,melody,sex,age,score,genre,proc,lz,rz,qomvals,velr,accr,mel,handdistvals = ([] for i in range(16))
cols3=['key','handstrat','participant','melody','sex','age','score','genre','proc','lz','rz','qomvals','velr','accr','mel','handdistvals']


for i in range(len(tracings)):
    key.append(i)
    handstrat.append(int(returnDetails(tracings[i])['typeID']))
    partic = int(returnDetails(tracings[i])['partID'])
    participant.append(partic)
    melID = int(returnDetails(tracings[i])['melID'])
    melody.append(melID)
    sex.append(list(participants.loc[participants.index[partic],['sex']])[0])
    age.append(int(participants.loc[participants.index[partic],['age']]))
    score.append(int(participants.loc[participants.index[partic],['scoreMus']]))
    m = melID
    if int(melID) in im:
        genre.append('im')
    elif int(melID) in jo:
        genre.append('jo')
    elif int(melID) in sc:
        genre.append('sc')
    elif int(melID) in vo:
        genre.append('vo')
    if int(melID) <=16:
        proc.append('norm')
    elif int(melID)>16:
        proc.append('syn')
    if int(m)<=16:
        mel.append(pitch['f0'][m-1])
    elif int(m)>16:
        mel.append(pitch['f0'][(m-17)])
    rz.append(readfile(tracings[i])['RHZ'])
    lz.append(readfile(tracings[i])['LHZ'])
    qomvals.append(qomnew(tracings[i]))
    handdistvals.append(handdist(tracings[i]))
    velr.append(numpy.diff(readfile(tracings[i])['RHZ']))
    accr.append(numpy.diff(numpy.diff((readfile(tracings[i])['RHZ']))))
    
for i in range(len(key)):
    contset = pd.DataFrame(zip(key,handstrat,participant,melody,sex,age,score,genre,proc,lz,rz,qomvals,velr,accr,mel,handdistvals))
    contset.columns=cols3


# avdataset = pd.read_excel('/home/tejaswik/Documents/CurrentProjects/melmot/avdataset.xls')
# avdataset.keys()