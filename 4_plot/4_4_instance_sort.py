import csv

NP_SORTED_POPULAR = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\stats\\statsNPSorted.csv'
NP_SORTED_MOST_INSTANCE = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\stats\\instanceNPSorted.csv'


# create ranking (sorted)
rank = {}

with open(NP_SORTED_POPULAR, 'r', encoding='utf-8') as inFile, open(NP_SORTED_MOST_INSTANCE, 'w', encoding='utf-8', newline='') as outFile:
    
    fileReader = csv.reader(inFile, delimiter=';')
    next(fileReader) # skip header row
    writer = csv.writer(outFile, delimiter=';')
    writer.writerow(['language', 'tot'])
    
    for row in fileReader:
        
        rank[row[0]] = int(row[5])
    
    items = [(k, int(v)) for k, v in rank.items()]
    sorted_items = sorted(items, key=lambda x:x[1], reverse=True)
    
    for element in sorted_items:
            
        array = [element[0], element[1]]
        writer.writerow(array)

    