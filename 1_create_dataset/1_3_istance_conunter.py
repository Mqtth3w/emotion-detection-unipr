'''
    This script counts how many instances of each class each
    month contains and write it into a stats file.
    This script is only useed to make stats.
'''

import csv

# files path
STATS = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\stats\\statsMonths.csv'
PATH = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\month'


def monthCounter(INM):
    
    count = 0
    with open(INM, 'r', encoding='utf-8', newline='') as inFile:
    
        reader = csv.reader(inFile, delimiter=';')
        next(reader) # skip header
        
        for row in reader:
            count += 1
            
    return count


with open(STATS, 'w', encoding='utf-8', newline='') as stats:
    
    writer = csv.writer(stats, delimiter=';')
    writer.writerow(['month','istance']) # write header
    
    current = 0
    total = 0
    
    for month in range(1, 13): # for each month folder
        
        IN = PATH + str(month) + '\\labelPosts.csv' # complete input path
        
        counter = monthCounter(IN)
        total += counter
        
        print('{0}\t{1}\n'.format(IN, counter))
        writer.writerow([month,counter])
    
    print('total', total)
        
