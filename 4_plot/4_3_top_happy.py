import csv

# files path
STATS = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\stats\\statsLanguagesEmotions.csv'
NP_NOTSORTED = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\stats\\statsNPNotSorted.csv'
NP_SORTED = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\stats\\statsNPSorted.csv'

# create happy languages list (not sorted)
with open(STATS, 'r', encoding='utf-8') as inFile, open(NP_NOTSORTED, 'w', encoding='utf-8', newline='') as outFile:

    fileReader = csv.reader(inFile, delimiter=';')
    next(fileReader) # skip header row
    writer = csv.writer(outFile, delimiter=';')
    writer.writerow(['language', 'pospct', 'negpct', 'postot', 'negtot'])

    i = 0
    pos = 0
    neg = 0
    
    for row in fileReader:
        
        if i <= 11:
            i += 1
            lang = row[0]

        elif i > 11:
            
            pct1=0.0
            pct2=0.0
            
            if (pos+neg) != 0:
                pct1=pos*100/(pos+neg)
                pct2=neg*100/(pos+neg)
                
            writer.writerow([lang, pct1, pct2, pos, neg])
            pos = 0
            neg = 0
            i = 1
        
        pos += int(row[3])
        neg += int(row[4])
    
# create ranking (sorted)

rank = {}

with open(NP_NOTSORTED, 'r', encoding='utf-8') as inFile, open(NP_SORTED, 'w', encoding='utf-8', newline='') as outFile:
    
    fileReader = csv.reader(inFile, delimiter=';')
    next(fileReader) # skip header row
    writer = csv.writer(outFile, delimiter=';')
    writer.writerow(['language','pospct','negpct', 'postot', 'negtot', 'tot'])
    
    for row in fileReader:
        
        rank[row[0]] = (row[1], row[2], row[3], row[4], (int(row[3]) + int(row[4])))
    
    
    items = [(k, float(v[0]), float(v[1]), v[2], v[3], v[4]) for k, v in rank.items()]
    sorted_items = sorted(items, key=lambda x:x[1], reverse=True)
    
    for element in sorted_items:
            
        array = [element[0], round(float(element[1]),2), round(float(element[2]),2), element[3], element[4], element[5]]
        writer.writerow(array)

    