'''
    This script takes a raw xml file as input and outputs
    an almost clean csv file
'''    

import re, csv

# total posts in 2022 over StackOverflow 3326518
# file paths
# path of 68 csv files with all 2022 posts divided by months
# (month1/(0.csv,1.csv,..),month2/(0.csv,1.csv,..), ...) 
PATH = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\month' 

# regex patterns
TAG_PATTERN = re.compile('<|>')
NEW_LINE = re.compile('\n')
BODY_1 = re.compile('\n?<pre(.*?)><code>(.*?)<\/code><\/pre>\n?|<div class=".*<div class=".*>', flags=re.S)
BODY_2 = re.compile('\s?<code>\w*<\/code>.\s?|\s?<a href=.*\">|<\/a>')
BODY_3 = re.compile('\s?<\w*>|<\/\w*>(.|\s)?')
BODY_4 = re.compile('&nbsp;|http(s?)://\S*|<img src.*"*>|<hr />|<br/>*|br>|<br />*|<ol.*">|/p>|/strong>|/li>|&lt;key>|&lt;/key>|/code>|/a>|#?&\w\w\w?;?')

# method to clean instances using regex
def cleanup(dirty):
    clean = re.sub(NEW_LINE,' ', dirty)    
    clean = re.sub(BODY_1,' ', clean)
    clean = re.sub(BODY_2,' ', clean)
    clean = re.sub(BODY_3,' ', clean)
    clean = re.sub(BODY_4,' ', clean)
    return clean

        
for month in range(1, 13): # for each month folder
    
    IN0 = PATH + str(month) + '\\' # almost complete input path
    OUT = PATH + str(month) + '\\almostCleanPosts.csv' # complete output path
    
    maxind = 6 # [2, 3, 5, 6, 8, 9, 10, 11]
    if (month in [1, 4, 7, 12]): # get the max csv index
        maxind = 5 
    
    with open(OUT, 'w', encoding='utf-8', newline='') as outFile:
        outFileWriter = csv.writer(outFile, delimiter=';')
        outFileWriter.writerow(['post', 'title', 'tags']) # write header
    
        for index in range(0, maxind): # for each csv into month
        
            IN = IN0 + str(index) + '.csv'
        
            with open(IN, 'r', encoding='utf-8') as inFile:

                inFileReader = csv.reader(inFile, delimiter=',')
                next(inFileReader) # skip header row (Id,Body,Title,Tags,CreationDate)
                
                outFileWriter = csv.writer(outFile, delimiter=';')
                
                for rowIn in inFileReader:
                    newRow = [] # new list to append as a row to the output file
                    
                    if rowIn[2] == "" and rowIn[3] == "": # is an answer, title and tags attributes are missing
                        newRow.append(cleanup(rowIn[1])) # body first field 
                        # leave title and tag fields empty
                        newRow.append('') # third field
                        newRow.append('') # fourth field

                    else: # is a question
                        newRow.append(cleanup(rowIn[1])) # body first field
                        newRow.append(rowIn[2]) # title second field
                        newRow.append(re.sub(TAG_PATTERN,' ', rowIn[3])) # tags third field
                    
                    outFileWriter.writerow(newRow) # append cleaned row to the file
                    #print(newRow)
