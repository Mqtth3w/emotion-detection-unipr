'''
    This script takes the csv file almost cleaned previously as input and
    outputs a clean csv file
'''

import csv, re, string
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

# csv files path
PATH = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\month'

# some costants to speed up the process
PATTERN = re.compile('[^\x00-\x7f]')
STOP_WORDS = stopwords.words('english')
SNOW = SnowballStemmer('english')
PUNCT = string.punctuation

def lowercasePunctation(post): 
    post = post.translate(str.maketrans('', '', PUNCT)).lower() # remove punctuation and set to lowercase
    post = re.sub(PATTERN,'', post) # remove non printable chars
    return post


def cleanPost(post): 
    post = ' '.join([word for word in post.split() if word not in STOP_WORDS]) # remove stopwords
    post = ' '.join([SNOW.stem(word) for word in post.split()]) # stemming
    return post



for month in range(1, 13):
    
    IN = PATH + str(month) + '\\almostCleanPosts.csv' # complete input path
    OUT = PATH + str(month) + '\\cleanPosts.csv' # complete output path
    
    open(OUT, 'w', encoding='utf-8').close() # erase file berfore writing
    with open(IN, 'r', encoding='utf-8') as inFile, open(OUT, 'a', encoding='utf-8', newline='') as outFile:
        inFileReader = csv.reader(inFile, delimiter=';')
        next(inFileReader) # skip header row (post;title;tags)
        outFileWriter = csv.writer(outFile, delimiter=';')
        outFileWriter.writerow(['post', 'title', 'tags', 'stoppost'])
        
        
        for rowIn in inFileReader:
            
            newRow = [] # new list to append as a row to the output file
            lowpost = lowercasePunctation(rowIn[0])
            newRow.append(lowpost) # post remain the same but lowercase 
            newRow.append(cleanPost(rowIn[1])) # title gets cleaned
            newRow.append(rowIn[2]) # tags remain the same
            newRow.append(cleanPost(lowpost)) # post gets cleaned with nltk for distant supervision 
            outFileWriter.writerow(newRow) # append new cleaned row to the output file  
    
    print('file Done', OUT)
    