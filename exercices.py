from main import *
from functions import *

#Guillaume BERNARD , Samuel MOLIERE | chatbot project
# exercices.py : code and feature asked asked

#path variables
speechesPath = path.join(curdir,'speeches')
cleanedPath = path.join(curdir,'cleaned')
ConvertAllSpeechesToLowerCase(speechesPath,cleanedPath)
RemovePunctuationFromAllCleaned(cleanedPath)

mat=MatrixTF_IDF(cleanedPath)

# - 1 -

print('word with 0 TF-IDF in all file :')
for i in mat:
    if sum(mat[i])==0:
        print(i)


# - 2 -
maxi=[0,'']
for i in mat:
    if sum(mat[i])>=maxi[0]:
        maxi=[sum(mat[i]),i]
print('max TF-IDF : ',maxi[1])

# - 3 -
maxi
for speech in listdir(speechesPath):
    if GetPresidentNamefromfileName(speech)=='Chirac':
        with open(path.join(cleanedPath, speech), 'r') as speechFile:
            TF = CalculateTF(speechFile.readline())
            maxi = [max(TF),max(TF, key=TF.get)]
print('most used word by Chirac : ',maxi[1])

# - 4 -
print("president who said the word 'Nation' : ")
presi={}
for speech in listdir(speechesPath):
    with open(path.join(cleanedPath, speech), 'r') as speechFile:
        nationTF = speechFile.readline().count('nation')
        if nationTF>0:
            print(GetPresidentNamefromfileName(speech))
            if GetPresidentNamefromfileName(speech) in  presi.keys():
                presi[GetPresidentNamefromfileName(speech)]+=nationTF
            else:
                presi[GetPresidentNamefromfileName(speech)]=nationTF
print("president who said 'Nation' the most time : ", max(presi,key=presi.get))

#- 5 -

presi=[]
for speech in listdir(cleanedPath):
    with open(path.join(cleanedPath, speech), 'r') as speechFile:
        line=speechFile.readline()
        if max(line.count('ecologie'),line.count('climat'))>0:
            presi.append(GetPresidentNamefromfileName(speech))
print("president who said climat/ecology : ", presi)
# the first to speak about it is Sarkozy

# - 6 -
words=[]
for speech in listdir(speechesPath):
    with open(path.join(cleanedPath, speech), 'r') as speechFile:
        TF = CalculateTF(speechFile.readline())
        if words==[]: words=list(TF.keys())
        for i in words:
            if not(i in TF.keys()):
                words.remove(i)
print(words)