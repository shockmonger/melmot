tracings = os.listdir('/home/tejaswik/Documents/CurrentProjects/melmot/data/normdatadump/')
for i in range(len(tracings)):
    tracings[i] = tracings[i][:-4]

im = [1,2,3,4,17,18,19,20]
jo = [5,6,7,8,21,22,23,24]
sc = [9,10,11,12,25,26,27,28]
vo = [13,14,15,16,29,30,31,32]
    
key, handstrat, participant, melody, sex, age, score, genre,proc, qoms, handdists, rz, lz  = ([] for i in range(13))
cols=['key', 'handstrat', 'participant', 'melody', 'sex', 'age', 'score', 'genre','proc', 'qom', 'handdist', 'rz', 'lz']

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
    dataset.columns=cols

 