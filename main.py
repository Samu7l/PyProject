import os.path
from os import curdir, path, listdir
from math import log10,sqrt,fabs,inf
from functions import *

#Guillaume BERNARD , Samuel MOLIERE | chatbot project
# main.py : main file used for menu

#/**********************************************************************************/

#path variables
speechesPath = path.join(curdir,'speeches')
cleanedPath = path.join(curdir,'cleaned')

allowCustomPythonLine=True

if __name__=='__main__':
    while True:
        cmd=None
        print('********************************************************************************** \n Menu : \n 1 : Ask a question to Bob\n 2 : Change speeches folder path\n 3 : Change cleaned speeches folder path\n 4 : Execute custom python line\n 5 : Reload (use it to generate the cleaned speeches set of file from the speeches)\n 6 : Exit \n**********************************************************************************')
        cmd=input()
        try:
            cmd=int(cmd)
        except:
            print('Error : invalid command')
        if cmd!=None:
            if cmd==6:
                print('you chose to exit')
                break
            elif cmd==5:
                try:
                    ConvertAllSpeechesToLowerCase(speechesPath,cleanedPath)
                    RemovePunctuationFromAllCleaned(cleanedPath)
                    print('Reload done !')
                except:
                    print('Error : reload error')
            elif cmd==4:
                if allowCustomPythonLine:
                    print('enter a python line to execute')
                    try:
                        exec(input())
                    except:
                        print('Error : python line ')
                else:
                    print('Security : this feature is blocked')
            elif cmd==3:
                print('Enter a new cleaned directory path :')
                tempCleanedPath=input()
                if os.path.exists(tempCleanedPath):
                    cleanedPath=tempCleanedPath
                else:print('Error : invalid path')
            elif cmd==2:
                print('Enter a new speeches directory path :')
                tempSpeechesPath=input()
                if os.path.exists(tempSpeechesPath):
                    speechesPath=tempSpeechesPath
                else:print('Error : invalid path')
            elif cmd==1:
                answer=AskQuestion(input('Enter a question :\n'),speechesPath,cleanedPath)
                if answer=='': print('Error : unknown topic; not enough data to answer youre question, try to add more content into the speech folder')
                else: print('Bob > '+answer)




