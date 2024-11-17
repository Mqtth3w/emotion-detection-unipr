'''
    This script takes a dataset made of type 1 and 2 posts and
    creates a new dataset with only type 1 posts that have at least
    a matching tag with top languages.
'''

import csv

# csv files path
PATH = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\month'
#IN_TRAIN = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\trainingSet60.csv'
#IN_VAL = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\validationSet20.csv'
#OUT_TRAIN = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\trainingSetFiltered60.csv'
#OUT_VAL = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\validationSetFiltered20.csv'

LANGUAGES = ['javascript','html','css','sql','python','typescript','java','bash','shell','c#','c++','php',
             'c','powershell','go','rust','kotlin','dart','ruby','assembly','swift','r','vba','matlab',
             'lua','groovy','delphi','scala','objective-c','perl','haskell','elixir','julia','clojure',
             'solidity','lisp','f#','fortran','erlang','apl','cobol','sas','ocaml','crystal']


def myFilter(IN, OUT):
    
    count = 0
    
    with open(IN, 'r', encoding='utf-8') as inFile, open(OUT, 'w', encoding='utf-8', newline='') as outFile:
        
        reader = csv.reader(inFile, delimiter=';')
        next(reader) # skip header
        
        writer = csv.writer(outFile, delimiter=';')
        writer.writerow(['label','post','tags']) # write header
        
        for row in reader: # for each file line (after headers)
            
            if row[2] != '':
                
                for word in row[2].split(): # for each word in the 'tags' field (until found one)
                    
                    if word in LANGUAGES: # check if that word is in 'LANGUAGES', stop at the first found
                        
                        writer.writerow(row)
                        count += 1
                        
                        break
                
    print('{0}\t{1}\n'.format(IN, count))

# test set filter
for month in range(1, 13):
    
    IN0 = PATH + str(month) + '\\labelPosts.csv' # complete input path
    OUT0 = PATH + str(month) + '\\filteredPosts.csv' # complete output path
    
    myFilter(IN0, OUT0)
    
'''  
# training set filter
myFilter(IN_TRAIN, OUT_TRAIN)


# validation set filter
myFilter(IN_VAL, OUT_VAL)
'''
