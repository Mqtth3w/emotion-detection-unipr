import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
import csv

LANGUAGES = ['javascript','html','css','sql','python','typescript','java','bash','shell','c#','c++','php',
             'c','powershell','go','rust','kotlin','dart','ruby','assembly','swift','r','vba','matlab',
             'lua','groovy','delphi','scala','objective-c','perl','haskell','elixir','julia','clojure',
             'solidity','lisp','f#','fortran','erlang','apl','cobol','sas','ocaml','crystal']

LANGUAGESPRO = ['JavaScript','HTML','CSS','SQL','Python','TypeScript','Java','Bash','Shell','C#','C++','PHP',
             'C','PowerShell','Go','Rust','Kotlin','Dart','Ruby','Assembly','Swift','R','VBA','MATLAB',
             'Lua','Groovy','Delphi','Scala','Objective-C','Perl','Haskell','Elixir','Julia','Clojure',
             'Solidity','LISP','F#','Fortran','Erlang','APL','COBOL','sas','OCaml','Crystal']

# file path
STATS = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\stats\\statsLanguagesEmotions.csv'

# get language from user, then get the index of that language
langIndex = LANGUAGES.index(input("Enter language\n"))

# x axis labels
labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# values for each bar type
neutral = []
joy = []
love = []
surprise = []
sad = []
fear = []
anger = []

# populate lists with values
with open(STATS, 'r', encoding='utf-8') as inFile:
    
    fileReader = csv.reader(inFile, delimiter=';')
    next(fileReader) # skip header row
    
    for row in fileReader:
        
        if row[0] == LANGUAGES[langIndex]:
            
#             # decomment to use percentile
#             neutral.append(float(row[12]))
#             joy.append(float(row[13]))
#             love.append(float(row[14]))
#             surprise.append(float(row[15]))
#             sad.append(float(row[16]))
#             fear.append(float(row[17]))
#             anger.append(float(row[18]))
            
            # decomment to use number of instances
            #neutral.append(float(row[5]))
            joy.append(float(row[6]))
            love.append(float(row[7]))
            surprise.append(float(row[8]))
            sad.append(float(row[9]))
            fear.append(float(row[10]))
            anger.append(float(row[11]))


xpos = np.arange(len(labels))
plt.xticks(xpos, labels)
plt.ylabel('Numero di istanze')
plt.xlabel('Anno 2022')
plt.title(LANGUAGESPRO[langIndex])

# # commet them to use line plot
# plt.bar(xpos-0.05, surprise, width=0.1, label='Surprise', color='#753BBD') # purple
# plt.bar(xpos+0.05, sad, width=0.1, label='Sad', color='#FF7F41') # orange
# plt.bar(xpos-0.15, love, width=0.1, label='Love', color='#2DC84D') # green
# plt.bar(xpos+0.15, fear, width=0.1, label='Fear', color='#F7EA48') # yellow
# plt.bar(xpos-0.25, joy, width=0.1, label='Joy', color='#147BD1') # blue
# plt.bar(xpos+0.25, anger, width=0.1, label='Anger', color='#E03C31') # red
# plt.bar(xpos-0.35, neutral, width=0.1, label='Neutral', color='#D2D2D2') # grey


# decomment them to use line plot
plt.plot(xpos-0.05, surprise, label='Surprise', color='#753BBD') # purple
plt.plot(xpos+0.05, sad, label='Sad', color='#FF7F41') # orange
plt.plot(xpos-0.15, love, label='Love', color='#2DC84D') # green
plt.plot(xpos+0.15, fear, label='Fear', color='#F7EA48') # yellow
plt.plot(xpos-0.25, joy, label='Joy', color='#147BD1') # blue
plt.plot(xpos+0.25, anger, label='Anger', color='#E03C31') # red
#plt.plot(xpos-0.35, neutral, label='Neutral', color='#D2D2D2') # grey


legend_elements = [
    #Patch(facecolor='#D2D2D2', label='neutral'),
    Patch(facecolor='#147BD1', label='joy'),
    Patch(facecolor='#2DC84D', label='love'),
    Patch(facecolor='#753BBD', label='surprise'),
    Patch(facecolor='#FF7F41', label='sadness'),
    Patch(facecolor='#F7EA48', label='fear'),
    Patch(facecolor='#E03C31', label='anger')]


plt.legend(handles=legend_elements, loc='best')
plt.show()
