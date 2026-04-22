import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load csv file
file_path =r"EDITED_CSV_FILES\Book1.csv" 
df = pd.read_csv(file_path)

# Ensure numeric columns
df['TEAM_1_XG'] = pd.to_numeric(df['TEAM_1_XG'], errors='coerce')
df['TEAM_2_XG'] = pd.to_numeric(df['TEAM_2_XG'], errors='coerce')

# Drop rows with missing data
df = df.dropna(subset=['TEAM_1_XG', 'TEAM_2_XG'])

# Extract all unique teams
teams = sorted(set(df['TEAM_1']).union(df['TEAM_2']))
n = len(teams)
team_index = {team: i for i, team in enumerate(teams)}

# Set up Massey system
M = np.zeros((n, n))
p = np.zeros(n)

# Build the system
for _, row in df.iterrows():
    t1, t2 = row['TEAM_1'], row['TEAM_2']
    xg1, xg2 = row['TEAM_1_XG'], row['TEAM_2_XG']
    
    i, j = team_index[t1], team_index[t2]

    # Update Massey matrix
    M[i, i] += 1
    M[j, j] += 1
    M[i, j] -= 1
    M[j, i] -= 1

    # Update point differentials 
    p[i] += xg1 * 1.15 - xg2
    p[j] += xg2 - xg1 *1.15

# Adjust for solvability
M[-1, :] = 1
p[-1] = 0

# Solve for ratings
r = np.linalg.lstsq(M, p, rcond=None)[0]

# Create results DataFrame
ratings_df = pd.DataFrame({
    'Team': teams,
    'Massey_Rating': r
}).sort_values(by='Massey_Rating', ascending=False)

print(ratings_df)



plt.figure(figsize=(10, 6)) 
plt.bar(ratings_df['Team'], ratings_df['Massey_Rating'], color='skyblue')
plt.xlabel('Team')
plt.ylabel('Massey Rating')
plt.title('Massey Ratings of Teams')
plt.xticks(rotation=45, ha='right') 
plt.tight_layout() 
plt.hlines(y=[0], xmin=0, xmax=35, colors=['r'], linestyles=['-'])
plt.savefig(r"IMAGES\HOME_AWAY.png")

plt.show()
print(M)
print(p)