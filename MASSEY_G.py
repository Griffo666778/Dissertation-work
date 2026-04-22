import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load csv file
file_path = ####r"    EDITED_CSV_FILES\Goals.csv"  
df = pd.read_csv(file_path)

# Ensure numeric columns
df['TEAM_1_G'] = pd.to_numeric(df['TEAM_1_G'], errors='coerce')
df['TEAM_2_G'] = pd.to_numeric(df['TEAM_2_G'], errors='coerce')

# Drop rows with missing data
df = df.dropna(subset=['TEAM_1_G', 'TEAM_2_G'])

# sort all unique teams
teams = sorted(set(df['TEAM_1']).union(df['TEAM_2']))
n = len(teams)
team_index = {team: i for i, team in enumerate(teams)}

# Set up Massey system
M = np.zeros((n, n))
p = np.zeros(n)

# Build the system
for _, row in df.iterrows():
    t1, t2 = row['TEAM_1'], row['TEAM_2']
    g1, g2 = row['TEAM_1_G'], row['TEAM_2_G']
    
    i, j = team_index[t1], team_index[t2]

    # Update Massey matrix
    M[i, i] += 1
    M[j, j] += 1
    M[i, j] -= 1
    M[j, i] -= 1

    # Update point differentials (using expected goals)
    p[i] += g1 - g2
    p[j] += g2 - g1

# Adjust for solvability
print("initial M",M)
M[-1, :] = 1
p[-1] = 0

# Solve for ratings
r = np.linalg.lstsq(M, p, rcond=None)[0]

# Create results DataFrame
ratings_df = pd.DataFrame({
    'Team': teams,
    'Massey_Rating': r
}).sort_values(by='Massey_Rating', ascending=False)

ratings_df.to_csv(r"\Goals_Massey.csv", index=False)


print(ratings_df)

ratings_high = ratings_df[ratings_df['Massey_Rating'] > 0]

plt.figure(figsize=(10, 6)) 
plt.bar(ratings_df['Team'], ratings_df['Massey_Rating'], color='skyblue')
plt.xlabel('Team')
plt.ylabel('Massey Rating')
plt.title('Massey Ratings of Teams')
plt.xticks(rotation=45, ha='right')  
plt.tight_layout() 
plt.hlines(y=[0], xmin=0, xmax=35, colors=['r'], linestyles=['-'])
plt.savefig(r"\INCLUDEINDISS.png")

plt.show()
#print("rrrr", r)
#print('This is matrix M:::!!!',M)
#print(p)