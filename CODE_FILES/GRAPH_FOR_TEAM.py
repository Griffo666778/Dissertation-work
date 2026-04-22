import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx




# Load csv file
file_path = r"\EDITED_CSV_FILES\Book1.csv"
df = pd.read_csv(file_path)

# Ensure numeric columns
df['TEAM_1_XG'] = pd.to_numeric(df['TEAM_1_XG'], errors='coerce')
df['TEAM_2_XG'] = pd.to_numeric(df['TEAM_2_XG'], errors='coerce')

# Drop rows with missing data
df = df.dropna(subset=['TEAM_1_XG', 'TEAM_2_XG'])

# Sort all unique teams
teams = sorted(set(df['TEAM_1']).union(df['TEAM_2']))
n = len(teams)
team_index = {team: i for i, team in enumerate(teams)}
print(teams)


G = nx.DiGraph()
G.add_nodes_from(teams)

G.add_edges_from([(row['TEAM_1'], row['TEAM_2']) for _, row in df.iterrows()])
G.add_edges_from([(row['TEAM_2'], row['TEAM_1']) for _, row in df.iterrows()])

# Create subgraph for specific teams
arsenal = 'Arsenal' 
barcelona = 'Barcelona'
#### clubs to include


neighbors = list(G.neighbors(arsenal)) + list(G.neighbors(barcelona))
nodes_to_keep = [arsenal] + [barcelona] + neighbors
subG = G.subgraph(nodes_to_keep).copy()

edge_labels = {(row['TEAM_1'], row['TEAM_2']): f"{row['TEAM_1_XG']}-{row['TEAM_2_XG']}" for _, row in df.iterrows() if row['TEAM_1'] in nodes_to_keep and row['TEAM_2'] in nodes_to_keep}
edge_labels = {(row['TEAM_2'], row['TEAM_1']): f"{row['TEAM_2_XG']}-{row['TEAM_1_XG']}" for _, row in df.iterrows() if row['TEAM_2'] in nodes_to_keep and row['TEAM_1'] in nodes_to_keep}
nx.draw_networkx_edge_labels(subG, pos=nx.spring_layout(subG, seed=32), edge_labels=edge_labels, font_size = 10, font_color='red', label_pos=0.3)


edge_num = len(subG.edges())
nodes_num = len(subG.nodes())
density = edge_num / (nodes_num * (nodes_num - 1)) if nodes_num > 1 else 0
print(f"Edge Density: {density}")


pos = nx.spring_layout(subG, seed=32) 
nx.draw(subG, pos=pos, with_labels=True,)
plt.show()
