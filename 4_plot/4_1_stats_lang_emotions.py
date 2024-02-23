import csv

PATH = 'C:\\Users\\MATTEO\\Desktop\\SOliteBigData\\month'
STATS = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\stats\\statsLanguagesEmotions.csv'

LANGUAGES = ['javascript','html','css','sql','python','typescript','java','bash','shell','c#','c++','php',
             'c','powershell','go','rust','kotlin','dart','ruby','assembly','swift','r','vba','matlab',
             'lua','groovy','delphi','scala','objective-c','perl','haskell','elixir','julia','clojure',
             'solidity','lisp','f#','fortran','erlang','apl','cobol','sas','ocaml','crystal']


open(STATS, mode='w', encoding='utf-8').close()
with open(STATS, mode='a', encoding='utf-8', newline='') as outFile:
    
    writer = csv.writer(outFile, delimiter=';')
    writer.writerow(['language','month','total','positive total','negative total','neutral','joy','love',
        'surprise','sad','fear','anger','neutral %','joy %','love %','surprise %','sad %','fear %','anger %'])
    
    for language in LANGUAGES:
        
        for month in range(1, 13):
    
            IN = PATH + str(month) + '\\bigDataPredictions.csv' # complete input path
            
            newRow = []
            
            # absolute number of istances of each class
            neutralCnt = joyCnt = loveCnt = surpriseCnt = angerCnt = fearCnt = sadCnt = 0

            with open(IN, 'r', encoding='utf-8') as inFile:
                
                reader = csv.reader(inFile, delimiter=';')
                next(reader) # skip header row
                
                for row in reader:
                    
                    for word in row[3].split(): # for each word in the 'tags' field
                        
                        if word == language:
                            
                            if row[0] == 'neutral':
                                neutralCnt+=1
                            elif row[0] == 'joy':
                                joyCnt+=1
                            elif row[0] == 'love':
                                loveCnt+=1
                            elif row[0] == 'surprise':
                                surpriseCnt+=1
                            elif row[0] == 'sadness':
                                sadCnt+=1
                            elif row[0] == 'fear':
                                fearCnt+=1
                            elif row[0] == 'anger':
                                angerCnt+=1
                            break
            
            
            posTotal = joyCnt + loveCnt + surpriseCnt
            negTotal =  sadCnt + fearCnt + angerCnt
            allTotal = posTotal + negTotal + neutralCnt

            # % of istances of each class
            neutralPct = joyPct = lovePct = surprisePct = sadPct = fearPct = angerPct = 0.0
            
            if neutralCnt != 0: 
                neutralPct = neutralCnt*100/allTotal
                
            if joyCnt != 0: 
                joyPct = joyCnt*100/allTotal

            if loveCnt != 0:
                lovePct = loveCnt*100/allTotal
            
            if surpriseCnt != 0:
                surprisePct = surpriseCnt*100/allTotal
            
            if sadCnt != 0:    
                sadPct = sadCnt*100/allTotal
            
            if fearCnt != 0:    
                fearPct = fearCnt*100/allTotal
            
            if angerCnt != 0:    
                angerPct = angerCnt*100/allTotal

            newRow.append(language)
            newRow.append(month)
            newRow.append(allTotal)
            newRow.append(posTotal)
            newRow.append(negTotal)
            newRow.append(neutralCnt)
            newRow.append(joyCnt)
            newRow.append(loveCnt)
            newRow.append(surpriseCnt)
            newRow.append(sadCnt)
            newRow.append(fearCnt)
            newRow.append(angerCnt)
            newRow.append(neutralPct)
            newRow.append(joyPct)
            newRow.append(lovePct)
            newRow.append(surprisePct)
            newRow.append(sadPct)
            newRow.append(fearPct)
            newRow.append(angerPct)
            writer.writerow(newRow)
            print('DONE', language, month)

