
import pandas as pd

#This code is for calculating spearman correlation.

df = pd.read_csv(r"\EDITED_CSV_FILES\combined_ratings_3.csv")
fix = df.iloc[:, 1:]

print(fix.corr(method='spearman'))






