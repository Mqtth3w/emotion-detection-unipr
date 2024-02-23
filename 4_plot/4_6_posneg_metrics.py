import csv
import pandas as pd
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# files path
PATH = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\month'
STATS = 'C:\\Users\\MATTEO\\Desktop\\StackOverflow archive\\stats\\statsPosNegPredictions.csv'

accuracy_average = 0 

# prepare file to save performance
with open(STATS, 'w', encoding='utf-8', newline='') as stats:
    writer = csv.writer(stats, delimiter=';')
    writer.writerow(['month','accuracy','precision','recall','f1']) # writee header

for month in range(1, 13):
    
    IN = PATH + str(month) + '\\posNegPredictions.csv'
    
    mydata = pd.read_csv(IN, encoding='utf-8', sep=';')    
    labels = mydata['label'].dropna().astype('str').tolist()
    pred_labels = mydata['pred'].dropna().astype('str').tolist()
    
    accuracy = accuracy_score(labels, pred_labels)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, pred_labels, average="weighted", zero_division=1) 
    
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
    
    accuracy_average += accuracy

accuracy_average = accuracy_average/12
print(f"Accuracy average: {accuracy_average:.4f}")
