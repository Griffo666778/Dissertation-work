import pandas as pd

df = pd.read_csv(r"\BASE_CSV_FILES\Current_Season_week_5.")

# Remove the last word from TEAM_1
df['TEAM_1'] = df['TEAM_1'].str.replace(r'\s+\S+$', '', regex=True)
# Remove the first word from TEAM_2
df['TEAM_2'] = df['TEAM_2'].str.replace(r'^\S+\s+', '', regex=True)
# Change dodgy UTF character 
df['Score'] = df['Score'].str.replace('–','-')



#This is the python script that has sorted the originial csv file, removing flags and things that were causing issues with the code.


df.to_csv(r"\EDITED_CSV_FILES\Current_Season_Week5.csv", index=False)
