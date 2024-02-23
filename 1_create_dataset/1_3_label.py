'''
    This script labels each instance of the csv file from
    the previous phase by searching keywords in each post.
'''

import csv, re


# csv files path
PATH = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\month'

# raw Parrot's emotions three levels dictionary
# removed liking, longing, contentment to avoid false positives
'''emotionsRaw = {
        'love': {'affection':['adoration', 'affection', 'love', 'fondness', 'attraction', 'caring', 'tenderness', 'compassion', 'sentimentality'],
                'lust':['arousal', 'desire', 'lust', 'passion', 'infatuation']},

        'joy': {'cheerfulness':['amusement', 'bliss', 'cheerfulness', 'gaiety', 'glee', 'jolliness', 'joviality', 'joy', 'delight', 'enjoyment', 'gladness', 'happiness', 'jubilation', 'elation', 'satisfaction', 'ecstasy', 'euphoria'],
                'zest':['enthusiasm', 'zeal', 'zest', 'excitement', 'thrill', 'exhilaration'],
                'contentment':['pleasure'], 
                'pride':['pride', 'triumph'],
                'optimism':['eagerness', 'hope', 'optimism'],
                'enthrallment':['enthrallment', 'rapture'], 
                'relief':['relief']},

        'surprise': {'surprise':['amazement', 'surprise', 'astonishment']},

        'anger': {'irritation':['aggravation', 'irritation', 'agitation', 'annoyance', 'grouchiness', 'grumpiness'],
                'exasperation':['exasperation', 'frustration'],
                'rage':['anger', 'rage', 'outrage', 'fury', 'wrath', 'hostility', 'ferocity', 'bitterness', 'hate', 'loathing', 'scorn', 'spite', 'vengefulness', 'dislike', 'resentment'],
                'disgust':['disgust', 'revulsion', 'contempt'],
                'envy':['envy', 'jealousy'],
                'torment':['torment']},

        'sadness': {'suffering':['agony', 'suffering', 'hurt', 'anguish'],
                    'sadness':['depression', 'despair', 'hopelessness', 'gloom', 'glumness', 'sadness', 'unhappiness', 'grief', 'sorrow', 'woe', 'misery', 'melancholy'],
                    'disappointment':['dismay', 'disappointment', 'displeasure'],
                    'shame':['guilt', 'shame', 'regret', 'remorse'],
                    'neglect':['alienation', 'isolation', 'neglect', 'loneliness', 'rejection', 'homesickness', 'defeat', 'dejection', 'insecurity', 'embarassment', 'humiliation', 'insult'],
                    'sympathy':['pity', 'sympathy']},

        'fear': {'nervousness':['anxiety', 'nervousness', 'tenseness', 'uneasiness', 'apprehension', 'worry', 'distress', 'dread'],
                'horror':['alarm', 'shock', 'fear', 'fright', 'horror', 'terror', 'panic', 'hysteria', 'mortification']}
}'''

# stemmed Parrot's emotions two levels dictionary, the previous third and second levels are merged into one
# removed like, long, content to avoid false positives
emotionsStemmedFlat = {
        'love': ['ador', 'affect', 'fond', 'attract', 'care', 'tender', 'compass', 'sentiment', 'arous', 'desir', 'lust', 'passion', 'infatu'],
        'joy': ['amus', 'bliss', 'cheer', 'gaieti', 'glee', 'jolli', 'jovial', 'delight', 'enjoy', 'glad', 'happi', 'jubil', 'elat', 'satisfact', 'ecstasi', 'euphoria', 'enthusiasm', 'zeal', 'zest', 'excit', 'thrill', 'exhilar', 'pleasur', 'pride', 'triumph', 'eager', 'hope', 'optim', 'enthral', 'raptur', 'relief'],
        'surpris':['amaz', 'astonish'],
        'anger': ['aggrav', 'irrit', 'agit', 'annoy', 'grouchi', 'grumpi', 'exasperation', 'exasper', 'frustrat', 'rage', 'outrag', 'furi', 'wrath', 'hostil', 'feroc', 'bitter', 'hate', 'loath', 'scorn', 'spite', 'veng', 'dislik', 'resent', 'disgust', 'revuls', 'contempt', 'envi', 'jealousi', 'torment'],
        'sad': ['agoni', 'suffer', 'hurt', 'anguish', 'depress', 'despair', 'hopeless', 'gloom', 'glum', 'sad', 'unhappi', 'grief', 'sorrow', 'woe', 'miseri', 'melancholi', 'dismay', 'disappoint', 'displeasur', 'guilt', 'shame', 'regret', 'remors', 'alien', 'isol', 'neglect', 'loneli', 'reject', 'homesick', 'defeat', 'deject', 'insecur', 'embarass', 'humili', 'insult', 'piti', 'sympathi'],
        'fear': ['anxieti', 'nervous', 'tens', 'uneasi', 'apprehens', 'worri', 'distress', 'dread', 'alarm', 'shock', 'fright', 'horror', 'terror', 'panic', 'hysteria', 'mortif']
}


EMOTIONS = emotionsStemmedFlat.items()
# create lists with first and second level words
primaryPos = ['love', 'joy', 'surpris']
primaryNeg = ['anger', 'sad', 'fear']

secondaryPos = []
for secondary in [emotionsStemmedFlat['love'], emotionsStemmedFlat['joy'], emotionsStemmedFlat['surpris']]:
    for element in secondary:
        secondaryPos.append(element)

secondaryNeg = []
for secondary in [emotionsStemmedFlat['anger'], emotionsStemmedFlat['sad'], emotionsStemmedFlat['fear']]:
    for element in secondary:
        secondaryNeg.append(element)


def searchWord(post):
    
    label = '' # neutral, love, joy, supris, anger, sad, fear
    keywordToRemove = '' 
    keywordList = []
    posCount = 0
    negCount = 0
    loveCount = 0
    joyCount = 0
    surpriseCount = 0
    angerCount = 0
    sadCount = 0
    fearCount = 0
    
    for word in post.split():
        
        for primary, secondaryList in EMOTIONS:
            # look for primary emotions first
            if word == primary:
                if primary == 'love':
                    posCount += 1
                    loveCount += 1
                elif primary == 'joy':
                    posCount += 1
                    joyCount += 1
                elif primary == 'surpris':
                    posCount += 1
                    surpriseCount += 1
                elif primary == 'anger':
                    negCount += 1
                    angerCount += 1
                elif primary == 'sad':
                    negCount += 1
                    sadCount += 1
                elif primary == 'fear':
                    negCount += 1
                    fearCount += 1
                
                if primary not in keywordList:
                    keywordList.append(primary)
                    
            # if no primary emotions were found look for secondary
            else:
                
                for keyword in secondaryList:
                    if word == keyword:
                        if primary == 'love':
                            posCount += 1
                            loveCount += 1
                        elif primary == 'joy':
                            posCount += 1
                            joyCount += 1
                        elif primary == 'surpris':
                            posCount += 1
                            surpriseCount += 1
                        elif primary == 'anger':
                            negCount += 1
                            angerCount += 1
                        elif primary == 'sad':
                            negCount += 1
                            sadCount += 1
                        elif primary == 'fear':
                            negCount += 1
                            fearCount += 1
                        
                        if keyword not in keywordList:
                            keywordList.append(keyword)
                          
    if posCount > negCount:
        label = 'positive'
    elif posCount < negCount:
        label = 'negative'
    else :  # if positive keywords are the same numbers as the negative or if no keywords are found label it as neutral
        label = 'neutral'


    # find what keyword to remove
    # set the label at the most used emotion
    if label == 'positive':
        
        countersPos = {'love': loveCount, 'joy': joyCount, 'surprise': surpriseCount}
        label = max(countersPos, key=lambda k: countersPos[k])
        
        for word in keywordList:
            if word in primaryPos:
                keywordToRemove = word
                break
        if keywordToRemove == '':
            for word in keywordList:
                if word in secondaryPos:
                    keywordToRemove = word
                    break

    elif label == 'negative':
        
        countersNeg = {'anger': angerCount, 'sadness': sadCount, 'fear': fearCount}
        label = max(countersNeg, key=lambda k: countersNeg[k])
        
        for word in keywordList:
            if word in primaryNeg:
                keywordToRemove = word
                break
        if keywordToRemove == '':
            for word in keywordList:
                if word in secondaryNeg:
                    keywordToRemove = word
                    break
                                                                
    # if not found return an array with empty values
    return [label, keywordToRemove]


for month in range(1, 13): # for each month folder
    
    IN = PATH + str(month) + '\\cleanPosts.csv' # complete input path
    OUT = PATH + str(month) + '\\labelPosts.csv' # complete output path
    
    
    open(OUT, 'w', encoding='utf-8').close() # overwrite files with emptyness
    with open(IN, 'r', encoding='utf-8') as inFile, open(OUT, 'a', encoding='utf-8', newline='') as outFile:
        
        inReader = csv.reader(inFile, delimiter=';')
        next(inReader) # skip header
        
        outWriter = csv.writer(outFile, delimiter=';')
        outWriter.writerow(['label','post','tags']) # write header

        for row in inReader:
            
            # search keyword
            listFromSearch = searchWord(row[3])
            
            # remove keyword from post if it's not objective
            if listFromSearch[0] != 'neutral':

                regex = re.compile(r'\b{0}[a-z]+\b'.format(re.escape(listFromSearch[1])))
                result = regex.sub('', row[0])
                # doing so creates a duplicate whitespace, remove it
                row[0] = " ".join(result.split())
                
            # write label, post, tags
            outWriter.writerow([listFromSearch[0],row[0],row[2]])
    
    print('\nDone', OUT)
        
