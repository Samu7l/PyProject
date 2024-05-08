import os.path
from os import curdir, path, listdir
from math import log10, sqrt, fabs, inf


# Guillaume BERNARD , Samuel MOLIERE | chatbot project
# functions.py : where all function are stored and ready to be called by main.

def GetPresidentNamefromfileName(filename: str) -> str:
    '''
    In : a filename (using the file name norm given in the project guidlines) (str)
    Out : the president name (str)
    '''

    # extract the president name from the filename
    presidentName = filename.split('.')[0].split('_')[1]

    # check if the president has more than 1 madndat and remove the number at the end if it's the case
    # a president cant have more than 2 mandat in france
    if presidentName[-1] in ['1', '2']:
        presidentName = presidentName[:-1]

    # return the president name
    return presidentName


def ExtractNames(speechesPath: str) -> list:
    '''
    In : the folder path where all speeches are located
    Out : A list with all president names present in the files name of the file located in the speechesPath folder

    This function :
    - associate a first name with each president
    - return the list of president's names
    '''

    authors = []

    # go trought all speeches file names
    for speech in listdir(speechesPath):
        # add the president name to the author list using the GetPresidentNamefromfileName function
        authors.append(GetPresidentNamefromfileName(speech))

    # remove all duplicate
    authors = set(authors)

    # convert the authors variable back to a list and returns it
    return list(authors)


# /**********************************************************************************/
def ConvertAllSpeechesToLowerCase(speechesPath: str, cleanedPath: str) -> None:
    '''
    In : speechesPath (the path to the foler where all the input file are located), cleanedPath (the path to folder where all the modified files for this project will be stored)
    Out : A new folder called 'clean' with contain the new 8 files with only lowercase characters without accents
    '''

    upperAndAccentChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÊÉÈéêèëËÛÙÇçÔô'
    lowerChars = 'abcdefghijklmnopqrstuvwxyzeeeeeeeeuuccoo'

    # go trought all speeches
    for speech in listdir(speechesPath):

        # open the file and create a new one in the cleanedpath directory
        with open(path.join(speechesPath, speech), 'r', encoding='utf-8') as speechFile, open(
                path.join(cleanedPath, speech), 'w', encoding='utf-8') as cleanedFile:

            # go throught alll the line in the non cleaned file
            for line in speechFile.readlines():

                # reconstruct the line by replacing uppercase with lowercase
                l = ''
                for char in line:
                    if char in upperAndAccentChars:
                        l += lowerChars[upperAndAccentChars.index(char)]
                    else:
                        l += char

                # write the modified line in the new file
                cleanedFile.write(l)


# /**********************************************************************************/

def RemovePunctuationFromAllCleaned(cleanedPath: str):
    '''
    In : The directory where the cleaned file are
    Out : Nothing

    This function remove all punctuation of all file presend in the cleaned folder
    (it remove .,;:!? and replace _ ' and \n (line break) with a space for easier reading later)
    '''

    punctuation = '.,;:!?0123456789'

    # go trought all cleaned speeches
    for speech in listdir(cleanedPath):

        # open the file (in read mode)
        with open(path.join(cleanedPath, speech), 'r') as cleanedFile:

            # get the all the txt data (a list of string storing each line)
            lines = cleanedFile.readlines()

        # open the file (in write mode)
        with open(path.join(cleanedPath, speech), 'w') as cleanedFile:

            # go through all line the file (stored before)
            for i in range(len(lines)):
                # remove all .,;:!? characters
                for char in punctuation:
                    lines[i] = lines[i].replace(char, '')

                # replace all - ' and \n by a space
                lines[i] = lines[i].replace('-', ' ')
                lines[i] = lines[i].replace("'", ' ')
                lines[i] = lines[i].replace("\n", ' ')

            # stored the result in the cleaned file
            cleanedFile.writelines(lines)


# /**********************************************************************************/

def CalculateTF(sentence: str) -> dict:
    '''
    In : a string containing the data of a cleaned speech
    Out : a dictionnary of the TF score for each word (the word is the key and the value its the TF)
    '''

    # the TF score correspond the number of occurence of the word in a speech
    TF = dict()
    # isolate the word in a list of string
    words = sentence.split(' ')

    # go through all the word in the file
    for word in words:

        # check if the word isnt in the TF dictionnary and if it has more than one character
        if word != '' and not (word in TF.keys()):
            TF[word] = words.count(word)
    return TF


# /**********************************************************************************/

def calculateIDF(cleanedPath: str) -> dict:
    '''
    In : The directory where the files to be analysed are located
    Out : The IDF score for each words in the different documents of the directory

    IDF of a word correspond to the inverse of the proportion of document where the
    word is present in the corpus and then apply the log10 function
    '''
    IDF = {}

    # go torught all file present in the cleanedpath directory
    for filename in listdir(cleanedPath):

        # open the file (in read mode)
        with open(path.join(cleanedPath, filename), 'r') as file:

            # isolate the word of the file in a list of string
            words = file.readline().split(' ')

            # go trought all word in the list words

            for i, word in enumerate(words):

                # check if the word is more thn one character
                if word != '':

                    # check if the word is the first in the words list
                    if words.index(word) == i:

                        # check if the word if already in the IDF dictionnary

                        if not (word in IDF.keys()):
                            IDF[word] = 1
                        else:
                            IDF[word] += 1
    # go trought all word in the dictionnary

    for word in IDF.keys():
        IDF[word] = log10(1 / (IDF[word] / len(listdir(cleanedPath))))
    return IDF


# /**********************************************************************************/
def MatrixTF_IDF(cleanedPath: str) -> dict:
    '''
    In : The directory where the files to be analysed are located (str)
    Out : A dictionary containing each word from the text documents within the selected file. For the dictionary (referred to as 'dico'), the keys consist of each unique word occurring only once, and for each of these keys, the corresponding values are a list of TF-IDF scores for that word in each text document within the file.
    '''

    Matrix = {}
    TF = {}

    # calculate the idf score of all word in the corpus
    IDF = calculateIDF(cleanedPath)

    # Create a 2D dict (Maxtrix) where the number of row correspond to the number of different word (key) in the corpus and the number of collumn correspond to the number of file (in the cleanedPath directory)
    for i in IDF.keys():
        Matrix[i] = [0] * len(listdir(cleanedPath))

    # go through all file in the cleanedPath folder
    for col, filename in enumerate(listdir(cleanedPath)):

        # open the file
        with open(path.join(cleanedPath, filename)) as file:

            # calculate the the TF of all word in the file
            TF_file = CalculateTF(file.readline())

        # fill the nth row/key with the IDF of the word and TF score of the word in current file selected
        for row, word in enumerate(IDF.keys()):
            if word in TF_file.keys():
                Matrix[word][col] = TF_file[word] * IDF[word]

    return Matrix


# Part II ---------------

# /**********************************************************************************/
def GetQuestionTokens(question: str):
    '''
    In : A question from the user
    Out : the list of words that make up the question in lower case and without accent
    '''

    upperAndAccentChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÊÉÈéêèëËÛÙÇçÔô'
    lowerChars = 'abcdefghijklmnopqrstuvwxyzeeeeeeeeuuccoo'

    # convert question to lower case without accents
    lowerCaseQuestion = ''

    for char in question:

        # check if the char is upppercase or is an accent
        if char in upperAndAccentChars:
            lowerCaseQuestion += lowerChars[upperAndAccentChars.index(char)]

        # check if the char is lower case or is \ (to prevent a n to be left alone)
        elif char in lowerChars or char == chr(92):
            lowerCaseQuestion += char
        else:

            # the char is not lower or upper case and is not \ so delete it
            lowerCaseQuestion += ' '
    # remove the line break (\n) from the lower case question

    lowerCaseQuestion.replace('\n', ' ')

    # convert it to a list of word
    tokens = lowerCaseQuestion.split(' ')

    # remove empty string from the word list (tokens)
    for i in range(tokens.count('')):
        tokens.remove('')

    # return the tokens (word list)
    return tokens


# /**********************************************************************************/

def SearchTokenInTF_IDF_Maxtrix(tokens:list, matrix:dict)->list:
    '''
    In : A list that contain the word of the question asked by the user (named tokens) & matrix, the matrix that give the TF-IDF for each word in the corpus
    Out : the list of words that are in the question asked by the user but also in the matrix TF-IDF
    '''
    inter = []
    for token in tokens:
        if token in matrix.keys():
            inter.append(token)
    return inter


def TF_IDF_question(questionTokens: list, cleanedPath: str, returnMax: bool):
    '''
    In : questionTokens: The word of the question in a list, cleanedPath : the corpus where the files, to be analysed, are located, and returnMax indicate if the function return the word with the max tf-idf
    Out : The TF-IDF vector of the question
    '''

    maxWord = ''
    maxWordValue = -1
    TF_IDF_words = MatrixTF_IDF(cleanedPath)
    Vector_TF_IDF_question = []
    IDF_words = calculateIDF(cleanedPath)
    for i in TF_IDF_words.keys():
        Vector_TF_IDF_question.append(questionTokens.count(i) / len(questionTokens))
        if Vector_TF_IDF_question[-1] != 0:
            try:
                Vector_TF_IDF_question[-1] *= IDF_words[i]
            except:
                pass
        if returnMax and maxWordValue < Vector_TF_IDF_question[-1]:
            maxWord = i
            maxWordValue = Vector_TF_IDF_question[-1]
    if returnMax: return Vector_TF_IDF_question, maxWord
    return Vector_TF_IDF_question


def DotProduct(vector1:list, vector2:list)->float:
    '''
    In : Two vectors vector1 & vector2 (vector1 and vector2 need to have the same dimension / same length) vector1 (list) vector2 (list)
    Out : return vector1 ⋅ vector2 or as the name of the function, vector1 DotProduct vector2 (float)
    '''

    dot = 0

    for i in range(len(vector1)):
        dot += fabs(vector1[i] * vector2[i])

    return dot


def VectorNorm(vector: list) -> float:
    '''
    In : A Vector (list)
    Out : The norm of the Vector (float)
    '''

    return sqrt(DotProduct(vector, vector))


def Similarity(Vector_TF_IDF_question:list, temp_TF_IDF_words:list) -> list:
    '''
    In : Two vectors Vector_TF_IDF_question (list) & temp_TF_IDF_words (list)
    Out : The score of simmilarity of all the document-vectors and question-vectors (list of float (correspond to the similarity between the question vector and the document vector))
    '''
    TF_IDF_words = []
    score = []
    for i in range(len(temp_TF_IDF_words[list(temp_TF_IDF_words.keys())[0]])):
        TF_IDF_words.append([])
        for j in (temp_TF_IDF_words.keys()):
            TF_IDF_words[-1].append(temp_TF_IDF_words[j][i])

    for i in range(len(TF_IDF_words)):
        try:
            score.append(DotProduct(Vector_TF_IDF_question, TF_IDF_words[i]) / (
                        VectorNorm(Vector_TF_IDF_question) * VectorNorm(TF_IDF_words[i])))
        except:
            score.append(inf)
    return score


# /**********************************************************************************/

def mostRelevantFileNameInFolder(maxtrix_TF_IDF, maxtrix_TF_IDF_question, folderPath):
    score = Similarity(maxtrix_TF_IDF_question, maxtrix_TF_IDF)
    return listdir(folderPath)[score.index(max(score))]


def ConvertWordToLowerCaseWithoutAccent(word: str) -> str:
    '''
    In : a word (str)
    Out : the same word but in lower case without accent and punctuation (str)
    '''
    tempWord = ''
    upperAndAccentChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÊÉÈéêèëËÛÙÇçÔô'
    lowerChars = 'abcdefghijklmnopqrstuvwxyzeeeeeeeeuuccoo'
    replaceBySpace = "'-:"
    for char in word:
        if char in upperAndAccentChars:
            tempWord += lowerChars[upperAndAccentChars.index(char)]
        # check if the char is lower case
        if char in replaceBySpace:
            tempWord += ' '

        elif char in lowerChars:
            tempWord += char

    return tempWord


# /**********************************************************************************/

def AskQuestion(question, speechesPath, cleanedPath):
    question_starters = {
        "comment": "Après analyse, ",
        "pourquoi": "Car, ",
        "peux-tu": "Oui, bien sûr!"
    }

    questionTokens = GetQuestionTokens(question)

    TF_IDF_Vector_Question, mostRelevantWord = TF_IDF_question(questionTokens, cleanedPath, True)

    # get the most relevant speeches accorind to the Similarity function (return the similarity between the question vector tf-idf and the document vecotr tf-idf)
    mostRelevantFileNamefilename = mostRelevantFileNameInFolder(MatrixTF_IDF(cleanedPath), TF_IDF_Vector_Question,cleanedPath)


    #search the first sentence where the most relevant word in the question is used and return it
    with open(path.join(speechesPath, mostRelevantFileNamefilename), 'r', encoding='utf-8') as speechFile:
        answer = ''
        lines = speechFile.readlines()
        mostRelevantWordFound = False
        for line in lines:
            l = line.split(' ')
            for i in range(len(l)):
                if mostRelevantWord == ConvertWordToLowerCaseWithoutAccent(l[i]):
                    mostRelevantWordFound = True
                if '.' in l[i] or '!' in l[i] or '?' in l[i]:
                    if mostRelevantWordFound == False:
                        answer = ''
                    else:
                        answer += l[i].replace('\n','')
                        answer
                        if questionTokens[0] in question_starters.keys():
                            return question_starters[questionTokens[0]] + answer
                        else:
                            return answer

                else:
                    answer += l[i].replace('\n','') + ' '