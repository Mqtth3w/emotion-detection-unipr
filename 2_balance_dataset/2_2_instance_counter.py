'''
    This script counts how many instances of each class each
    dataset part contains and write it into a stats file.
'''

import csv

# files path
STATS = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\stats\\statsEmotions.csv'
TRAIN = ['C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\trainingSet60.csv',
         'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\validationSet20.csv'] 
PATH = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\month'
            

def emotion_counters(f):
    # counters
    j = 0
    surp = 0
    ang = 0
    lov = 0
    sadn = 0
    fe = 0
    neu = 0
    
    with open(f, 'r', encoding='utf-8', newline='') as inFile:
        
        reader = csv.reader(inFile, delimiter=';')
        next(reader) # skip header

        for row in reader:
            
            #print(row)
            if row[0] == 'neutral':
                neu += 1
            elif row[0] == 'anger':
                ang += 1
            elif row[0] == 'love':
                lov += 1
            elif row[0] == 'joy':
                j += 1
            elif row[0] == 'surprise':
                surp += 1                    
            elif row[0] == 'sadness':
                sadn += 1
            elif row[0] == 'fear':
                fe += 1
    
    return (neu, lov, j, surp, ang, sadn, fe)


with open(STATS, 'w', encoding='utf-8', newline='') as stats:
    
    writer = csv.writer(stats, delimiter=';')
    writer.writerow(['neutral','love','joy','surpris','anger','sad','fear']) # write header
    
    
    for trainSet in TRAIN:
        
        neutral, love, joy, surpris, anger, sad, fear = emotion_counters(trainSet)

        print('neutral = {0}\nlove = {1}\njoy = {2}\nsurprise = {3}\nanger = {4}\nsadness = {5}\nfear = {6}\n'.format(
            neutral, love, joy, surpris, anger, sad, fear))
        
        writer.writerow([neutral,love,joy,surpris,anger,sad,fear])
    
    for month in range(1, 13): # for each month folder
        
        IN = PATH + str(month) + '\\testSet20.csv' # complete input path
        
        neutral, love, joy, surpris, anger, sad, fear = emotion_counters(IN)

        print('neutral = {0}\nlove = {1}\njoy = {2}\nsurpris = {3}\nanger = {4}\nsad = {5}\nfear = {6}\n'.format(
            neutral, love, joy, surpris, anger, sad, fear))
        
        writer.writerow([neutral,love,joy,surpris,anger,sad,fear])
