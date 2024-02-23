import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

#df = pd.read_csv("C://Users//MATTEO//Desktop//StackOverflow archive//modelLovedDreadedVsSOsurvey.csv", delimiter=';', decimal=',')
df = pd.read_csv("C://Users//MATTEO//Desktop//StackOverflow archive//modelPredVsSOsurvey.csv", delimiter=';', decimal=',')

sns.regplot(x="sosurvey", y="model", data=df)

#decomment to see labels 
for i, row in df.iterrows():
    plt.annotate(row['tecnology'], (row['sosurvey'], row['model']), textcoords="offset points", xytext=(0,5), ha='center')

plt.show()

x = df["sosurvey"]
y = df["model"]
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
print(f"Coefficient of correlation: {r_value:.4f}")
print(f"p-value: {p_value:.4f}")
