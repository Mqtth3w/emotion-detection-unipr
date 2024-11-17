'''
    This script counts instances of each language tags found in type 1 posts (questions).
    This script is only used to know test set instances number of languages.
'''

import csv, array

# csv files path
STATS = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\stats\\statsLanguages.csv'
PATH = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\month'

# words to match
LANGUAGES = ['javascript','html','css','sql','python','typescript','java','bash','shell','c#','c++','php',
             'c','powershell','go','rust','kotlin','dart','ruby','assembly','swift','r','vba','matlab',
             'lua','groovy','delphi','scala','objective-c','perl','haskell','elixir','julia','clojure',
             'solidity','lisp','f#','fortran','erlang','apl','cobol','sas','ocaml','crystal']

LANG_LENGTH = len(LANGUAGES)

# create header for the csv
header = ['month','javascript','html','css','sql','python','typescript','java','bash','shell','c#','c++','php',
             'c','powershell','go','rust','kotlin','dart','ruby','assembly','swift','r','vba','matlab',
             'lua','groovy','delphi','scala','objective-c','perl','haskell','elixir','julia','clojure',
             'solidity','lisp','f#','fortran','erlang','apl','cobol','sas','ocaml','crystal','total']


with open(STATS, 'w', encoding='utf-8', newline='') as outFile:
    
    writer = csv.writer(outFile, delimiter=';')
    writer.writerow(header)
    
    for month in range(1, 13):
    
        test20_filtered = PATH + str(month) + '\\testSet20.csv' # complete input path
        
        # each element is the number of instances of that language, indexs are matching with LANGUAGES
        langOccurences = [0] * LANG_LENGTH
        
        with open(test20_filtered, 'r', encoding='utf-8') as inFile:
            
            reader = csv.reader(inFile, delimiter=';')
            next(reader) # skip header
            
            found = 0
            
            # tags -> row[3], seprator -> sapce
            for row in reader: # for each file line (after headers)
                
                    for word in row[2].split(): # for each word in the 'tags' field
                        
                        if word in LANGUAGES: # check if that word is in 'LANGUAGES'
                            
                            langOccurences[LANGUAGES.index(word)] += 1
        
        newRow = [str(month)]
        total = 0
        
        for value in langOccurences:
            
            newRow.append(value)
            total += value
            
        newRow.append(total)
        writer.writerow(newRow)

    
