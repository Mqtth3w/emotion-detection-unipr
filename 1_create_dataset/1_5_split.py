'''
    this script divides the dataset labeled by a pre-trained model also based on BERT
    (consisting of 12 files, one for each month) into 60, 20 and 20%.
    60% will be used for training.
    first 20% will be used for training parameters validation.
    first 20% will be used for test and performance measure.
'''

import csv, random

# csv files path
PATH = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\month' 
OUT_TRAIN = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\trainingSet60.csv'
OUT_VAL = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\validationSet20.csv'

# these lists will contain the 60 and 20% parts to be merged into one 60 and 20% 
train_set = []
val_set = []

# header files
header = ['label','post','tags']

for month in range(1, 13):
    
    IN = PATH + str(month) + '\\filteredPosts.csv' # complete input path
    OUT_TEST = PATH + str(month) + '\\testSet20.csv' # complete output test data path

    # open the csv file and read all data
    with open(IN, 'r', encoding='utf-8') as inFile:
        
        inFileReader = csv.reader(inFile, delimiter=';')
        next(inFileReader) # skip header row
        data = [row for row in inFileReader]

    # calculate the data length for the separation
    length1 = int(len(data) * 0.6)
    length2 = int(len(data) * 0.2)

    # shuffle data randomly
    random.shuffle(data)  

    # divide data into three parts
    train60 = data[:length1]  
    val20 = data[length1:length1+length2]  
    test20 = data[length1+length2:]

    # add parts to lists
    train_set.extend(train60)
    val_set.extend(val20) 
    
    # write test20 data
    open(OUT_TEST, 'w', encoding='utf-8').close() # erase file berfore writing
    with open(OUT_TEST, 'a', encoding='utf-8', newline='') as outTestFile:
        
        outTestFileWriter = csv.writer(outTestFile, delimiter=';')
        outTestFileWriter.writerow(header)
        outTestFileWriter.writerows(test20)
        
print('test sets DONE\n')


# write val_set data
with open(OUT_VAL, 'w', encoding='utf-8', newline='') as outValFile:
    
    outValFileWriter = csv.writer(outValFile, delimiter=';')
    outValFileWriter.writerow(header)
    outValFileWriter.writerows(val_set)
    
print('val set DONE\n')


# write train_set data
with open(OUT_TRAIN, 'w', encoding='utf-8', newline='') as outTrainFile:
    
    outTrainFileWriter = csv.writer(outTrainFile, delimiter=';')
    outTrainFileWriter.writerow(header)
    outTrainFileWriter.writerows(train_set)
    
print('train set DONE\n')
  