#! /usr/bin/python
import csv
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# files path
PATH = './month'
STATS = './stats/statsPredictions.csv'
TRAIN = './trainingSetBalanced60.csv'
VAL = './validationSetBalanced20.csv'


# create class for data preparation
class SimpleDataset:
    def __init__(self, input_ids, attention_masks, labels=None): 
        self.input_ids = input_ids
        self.attention_masks = attention_masks
        self.labels = labels 
    
    def __len__(self):
        return len(self.input_ids)
    
    def __getitem__(self, idx):
        if self.labels is not None: 
            return {'input_ids': self.input_ids[idx], 'attention_mask': self.attention_masks[idx], 'labels': self.labels[idx]}    
        else:
            return {'input_ids': self.input_ids[idx], 'attention_mask': self.attention_masks[idx]}


# define dictionary to map labels
id2label = {0: "neutral", 1: "love", 2: "joy", 3: "surprise", 4: "anger", 5: "sadness", 6: "fear"}
label2id = {"neutral": 0, "love": 1, "joy": 2, "surprise": 3, "anger": 4, "sadness": 5, "fear": 6}

# choose the class BertForSequenceClassification to load a BERT base pre-trained model
# because add an other layer (output layer) specially designed for text classification
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=7, id2label=id2label, label2id=label2id)
# define BERT tokenizer pre-trained
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')


# prepare training set
train_dataset_csv = pd.read_csv(TRAIN, encoding='utf-8', sep=';')
train_texts = train_dataset_csv['post'].dropna().astype('str').tolist()
train_labels = train_dataset_csv['label'].dropna().astype('str').tolist()
train_labels_int = [label2id[label] for label in train_labels]
tokenized_traintexts = tokenizer(train_texts,truncation=True,padding=True,max_length=512)
train_dataset = SimpleDataset(tokenized_traintexts['input_ids'],tokenized_traintexts['attention_mask'],train_labels_int)

# prepare validation set
val_dataset_csv = pd.read_csv(VAL, encoding='utf-8', sep=';')
val_texts = val_dataset_csv['post'].dropna().astype('str').tolist()
val_labels = val_dataset_csv['label'].dropna().astype('str').tolist()
tokenized_valtexts = tokenizer(val_texts,truncation=True,padding=True,max_length=512)
val_labels_int = [label2id[label] for label in val_labels]
val_dataset = SimpleDataset(tokenized_valtexts['input_ids'],tokenized_valtexts['attention_mask'],val_labels_int)


# define trainig arguments
training_args = TrainingArguments(
    # to save trained model and other info
    output_dir='./BERTdata',
    # evaluate the model at the end of each epoch
    evaluation_strategy = "epoch",
    # learning rate to use during training, tipically for little-medium dataset is in range [1e-5,5e-5]
    # start from 2e-5, find the best evaluating performance
    learning_rate=2e-5,
    # number of example to elaborate simultaneously over each CPU/GPU during training
    # it depends by CPU/GPU memory, tipically multiple of 2
    per_device_train_batch_size=16,   
    # " during evaluation
    per_device_eval_batch_size=16,
    # number of traininig made over the training set, should be low to avoid overfitting
    num_train_epochs=3,
    # L2 regularization, to avoid weights too much big then overfitting
    weight_decay=0.01,
    # don't save the model into hugging face hub
    push_to_hub=False,
    # save trainig logs 
    logging_dir='./BERTlogs',
    # logging is done evry epoch 
    save_strategy='epoch',
    # load at the end of trainig the model (n epochs -> n models) with best performance over validation set
    load_best_model_at_end=True,
)


# define trainer
trainer = Trainer(
    # pre-trained-model
    model=model,
    # training arguments
    args=training_args,
    # training dataset
    train_dataset=train_dataset,
    # evaluation dataset
    eval_dataset=val_dataset,
    # tokenizer
    tokenizer=tokenizer 
)

# train the model
trainer.train()

print('train DONE\n')


# prepare file to save performance
with open(STATS, 'w', encoding='utf-8', newline='') as stats:
    writer = csv.writer(stats, delimiter=';')
    writer.writerow(['month','accuracy','precision','recall','f1']) # writee header
    
# make predictions on 12 test sets
for month in range(1, 13):
    
    # complete test set path and results (predictions) path
    IN = PATH + str(month) + '/testSetBalanced20.csv'
    OUT = PATH + str(month) + '/testSetPredictions20.csv'
    
    # prepare test set
    test_dataset_csv = pd.read_csv(IN, encoding='utf-8', sep=';')
    test_texts = test_dataset_csv['post'].dropna().astype('str').tolist()
    tokenized_testtexts = tokenizer(test_texts,truncation=True,padding=True,max_length=512)
    test_dataset = SimpleDataset(tokenized_testtexts['input_ids'], tokenized_testtexts['attention_mask'])

    # save other columns
    labels = test_dataset_csv['label'].dropna().astype('str').tolist()
    tags = test_dataset_csv['tags'].dropna().astype('str').tolist()
    
    # make predictions over test set
    predictions = trainer.predict(test_dataset)
    
    # convert prediction numbers to labels
    preds = predictions.predictions.argmax(-1)
    pred_labels = [id2label[pred] for pred in preds]
    
    df = pd.DataFrame(list(zip(pred_labels,labels,test_texts,tags)), columns=['pred','label','post','tags'])
    df.to_csv(OUT, encoding='utf-8', sep=';', index=False, mode='w', header=True)
    
    
    # calculate performance metrics
    # calculate acurancy, total correct/total examples
    accuracy = accuracy_score(labels, pred_labels)
    # calculate precision, recall, f1
    # average="weighted" to calculate weighted average metrics based on the number of samples in each class
    # _ for support because it isn't neede with average="weighted" (return number of salmples for ech class) 
    precision, recall, f1, _ = precision_recall_fscore_support(labels, pred_labels, average="weighted") 
    
    # save performance 
    with open(STATS, 'a', encoding='utf-8', newline='') as stats:
        
        writer = csv.writer(stats, delimiter=';')
        writer.writerow([month,accuracy,precision,recall,f1]) 
    
    # print performance metrics
    print(month, "month")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1:.4f} \n")
