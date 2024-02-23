import csv
import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer 

# files path
PATH = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\month'
MODEL_PATH = "C:\\Users\\MATTEO\\Desktop\\SOarchiveLite\\BERTdata\\checkpoint-1680"

# create class for data preparation
class SimpleDataset:
    def __init__(self, input_ids, attention_masks): 
        self.input_ids = input_ids
        self.attention_masks = attention_masks 
    
    def __len__(self):
        return len(self.input_ids)
    
    def __getitem__(self, idx):
        return {'input_ids': self.input_ids[idx], 'attention_mask': self.attention_masks[idx]}


# define dictionary to map labels
id2label = {0: "neutral", 1: "love", 2: "joy", 3: "surprise", 4: "anger", 5: "sadness", 6: "fear"}
label2id = {"neutral": 0, "love": 1, "joy": 2, "surprise": 3, "anger": 4, "sadness": 5, "fear": 6}
# recover best trained model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained(MODEL_PATH, num_labels=7, id2label=id2label, label2id=label2id)

# define trainer
trainer = Trainer(
    # pre-trained-model
    model=model,
    # tokenizer
    tokenizer=tokenizer 
)


print('start predictions\n')

# make predictions on 12 months
for month in range(1, 13):
    
    # complete test set path and results (predictions) path
    IN = PATH + str(month) + '\\filteredPosts.csv'
    OUT = PATH + str(month) + '\\bigDataPredictions.csv'
    
    # prepare test set
    testset_csv = pd.read_csv(IN, encoding='utf-8', sep=';')
    test_texts = testset_csv['post'].dropna().astype('str').tolist()
    tokenized_testtexts = tokenizer(test_texts,truncation=True,padding=True,max_length=512)
    test_dataset = SimpleDataset(tokenized_testtexts['input_ids'], tokenized_testtexts['attention_mask'])
    
    # save other columns
    labels = testset_csv['label'].dropna().astype('str').tolist()
    tags = testset_csv['tags'].dropna().astype('str').tolist()
    
    # make predictions over test set
    predictions = trainer.predict(test_dataset)
    
    # convert prediction numbers to labels
    preds = predictions.predictions.argmax(-1)
    pred_labels = [id2label[pred] for pred in preds]
    
    
    # save predictions
    df = pd.DataFrame(list(zip(pred_labels,labels,test_texts,tags)), columns=['pred','label','post','tags'])
    with open(OUT, 'w', encoding='utf-8', newline='') as outFile:
        
        writer = csv.writer(outFile, delimiter=';')
        writer.writerow(['pred','label','post','tags']) # writee header
        writer.writerows(df.values.tolist())
    
    
    print('Done month', month)

