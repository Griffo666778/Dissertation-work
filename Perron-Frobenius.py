import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load csv file
file_path = r"EDITED_CSV_FILES\Book1.csv"
df = pd.read_csv(file_path)

# Ensure numeric columns
df['TEAM_1_XG'] = pd.to_numeric(df['TEAM_1_XG'], errors='coerce')
df['TEAM_2_XG'] = pd.to_numeric(df['TEAM_2_XG'], errors='coerce')

# Drop rows with missing data
df = df.dropna(subset=['TEAM_1_XG', 'TEAM_2_XG'])

# sort all unique teams
teams = sorted(set(df['TEAM_1']).union(df['TEAM_2']))
n = len(teams)
team_index = {team: i for i, team in enumerate(teams)}

# Build the Perron-Frobenius matrix W
W = np.zeros((n, n))

for _, row in df.iterrows():
    t1, t2 = row['TEAM_1'], row['TEAM_2']
    xg1, xg2 = row['TEAM_1_XG'], row['TEAM_2_XG']
    
    i, j = team_index[t1], team_index[t2]
    
    # Populate the matrix of positive interactions
    #This uses the increased home xg to potentially allow for including home advantage.
    W[i, j] += xg1 * 1.15
    W[j, i] += xg2

# Find dominant Eigenvector
eigvals, eigvecs = np.linalg.eig(W)


# Find index of largest real eigenvalue
idx = np.argmax(eigvals.real)  # type: ignore[attr-defined]

# Dominant eigenvector
r = eigvecs[:, idx].real  # type: ignore[attr-defined]

# Normalize for readability
r = r / np.sum(r)

# Ensure all values are positive 
r = np.abs(r)

# Create DataFrame for ratings
ratings_df = pd.DataFrame({
    'Team': teams,
    'PF_Rating': r
}).sort_values(by='PF_Rating', ascending=False)

print(ratings_df)


plt.figure(figsize=(10, 6))
plt.bar(ratings_df['Team'], ratings_df['PF_Rating'], color='skyblue')
plt.xlabel('Team')
plt.ylabel('Perron–Frobenius Rating')
plt.title('PF Ratings of Teams (Dominant Eigenvector Method)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()



print("Perron-Frobenius Matrix (W):")
print(W)
plt.savefig(r"\IMAGES\Perron-Frobenius.png")

ratings_df.to_csv(r"\EDITED_CSV_FILES\Perron-Frobenius.csv", index=False)