import pandas as pd
import numpy as np



# Files combined_ratings_ 1, 2, 3 are different, 1 is original, 2 is with all teams, 3 is with the middle 28 teams. 
df = pd.read_csv(r"\EDITED_CSV_FILES\combined_ratings_3.csv")



# Create ranks
df['Rank_Official'] = df['Points'].rank(ascending=False, method='min').astype('Int64')
df['Rank_Massey_GD'] = df['Massey_Rating_G'].rank(ascending=False, method='min').astype('Int64')
df['Rank_Massey_XG'] = df['Massey_Rating_XG'].rank(ascending=False, method='min').astype('Int64')
df['Rank_PF'] = df['PF_Rating'].rank(ascending=False, method='min').astype('Int64')

# MARD function
def mard(col1, col2):
    return np.mean(np.abs(df[col1] - df[col2]))

# Print results
print("Official vs GD:", round(mard('Rank_Official','Rank_Massey_GD'),3))
print("Official vs XG:", round(mard('Rank_Official','Rank_Massey_XG'),3))
print("Official vs PF:", round(mard('Rank_Official','Rank_PF'),3))
print("GD vs XG:", round(mard('Rank_Massey_GD','Rank_Massey_XG'),3))
print("GD vs PF:", round(mard('Rank_Massey_GD','Rank_PF'),3))
print("XG vs PF:", round(mard('Rank_Massey_XG','Rank_PF'),3))

# Biggest differences
df['Diff_Official_PF'] = (df['Rank_Official'] - df['Rank_PF']).abs()

top5 = df.sort_values('Diff_Official_PF', ascending=False).head(28)

print(top5[['Team', 'Rank_Official', 'Rank_PF', 'Diff_Official_PF']])
