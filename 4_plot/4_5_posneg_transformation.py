import csv

# csv files path
PATH = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\month'

posEm = ['love', 'joy', 'surprise']
negEm = ['anger', 'sadness', 'fear'] 

for month in range(1, 13):
    
    IN = PATH + str(month) + '\\testSetPredictions20.csv' # complete input path
    OUT = PATH + str(month) + '\\posNegPredictions.csv' # complete output path
    
    open(OUT, 'w', encoding='utf-8').close() # erase file berfore writing
    with open(IN, 'r', encoding='utf-8') as inFile, open(OUT, 'a', encoding='utf-8', newline='') as outFile:
        inFileReader = csv.reader(inFile, delimiter=';')
        next(inFileReader) # skip header 
        outFileWriter = csv.writer(outFile, delimiter=';')
        outFileWriter.writerow(['pred', 'label', 'post', 'tags'])
        
        
        for rowIn in inFileReader:
            
            newRow = []
            
            if rowIn[1] == 'neutral':
                continue
            
            if rowIn[0] in posEm:
                newRow.append('pos')
            elif rowIn[0] in negEm:
                newRow.append('neg')
            else:
                newRow.append(rowIn[0])
            
            if rowIn[1] in posEm:
                newRow.append('pos')
            elif rowIn[1] in negEm:
                newRow.append('neg')
            else:
                newRow.append(rowIn[1])
                
            newRow.append(rowIn[2]) 
            newRow.append(rowIn[3]) 
            outFileWriter.writerow(newRow)  
    
    print('file Done', OUT)
    