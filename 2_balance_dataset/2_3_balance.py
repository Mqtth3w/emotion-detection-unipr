'''
    this script perfectly balace the dataset.
'''

import csv

# files path
STATS = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\stats\\statsEmotions.csv'

TRAIN = ['C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\trainingSet60.csv',
         'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\validationSet20.csv',
         'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\trainingSetBalanced60.csv',
         'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\validationSetBalanced20.csv']

PATH = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\month'


def balancer(MAX, IN, OUT):
    
    # get the number of instances of the emotion with fewest instances
    #MAX = min(stat) #max(stat[1],stat[2],stat[3],stat[4],stat[5],stat[6])
    
    with open(IN, 'r', encoding='utf-8') as inFile, open(OUT, 'w', encoding='utf-8', newline='') as outFile:
        
        breader = csv.reader(inFile, delimiter=';')
        next(breader) # skip header
        bwriter = csv.writer(outFile, delimiter=';')
        bwriter.writerow(['label','post','tags'])
        
        # counters
        joy = 0
        surpris = 0
        anger = 0
        love = 0
        sad = 0
        fear = 0
        neutral = 0

        for row in breader:
            
            if row[0] == 'neutral' and neutral < MAX:
                bwriter.writerow(row)
                neutral += 1
            if row[0] == 'love' and love < MAX:
                bwriter.writerow(row)
                love += 1
            if row[0] == 'joy' and joy < MAX:
                bwriter.writerow(row)
                joy += 1
            if row[0] == 'surprise' and surpris < MAX:
                bwriter.writerow(row)
                surpris += 1
            if row[0] == 'anger' and anger < MAX:
                bwriter.writerow(row)
                anger += 1
            if row[0] == 'sadness' and sad < MAX:
                bwriter.writerow(row)
                sad += 1
            if row[0] == 'fear' and fear < MAX:
                bwriter.writerow(row)
                fear += 1
        
        print('neutral = {0}\nlove = {1}\njoy = {2}\nsurprise = {3}\nanger = {4}\nsadness = {5}\nfear = {6}\n'.format(
            neutral, love, joy, surpris, anger, sad, fear))



def findMinInstance():
    
    with open(STATS, 'r', encoding='utf-8') as stats:
    
        reader = csv.reader(stats, delimiter=';')
        next(reader) # skip header

        # find minimum instance training stats
        min_tr = min(map(int, next(reader)))

        # find minimum instance validation stats
        min_v = min(map(int, next(reader)))
    
        # find minimum instance test stats
        min_te  = 999999
        for row in reader:
            
            vals = [int(x) for x in row]
            vals.append(min_te)
            min_te = min(vals)
    
        return (min_tr, min_v, min_te)
    
 
min_train, min_val, min_test = findMinInstance()

# balance training set 
balancer(min_train, TRAIN[0], TRAIN[2])

# balance validation set 
balancer(min_val, TRAIN[1], TRAIN[3])

# balance test sets
for index in range(1, 13):
    
    testInFile = PATH + str(index) + '\\testSet20.csv'
    testOutFile = PATH + str(index) + '\\testSetBalanced20.csv'
    balancer(min_test, testInFile, testOutFile)
    
