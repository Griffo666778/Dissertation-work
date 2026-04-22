import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx





# Load csv file
file_path = r"EDITED_CSV_FILES\Book1.csv"
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

for _, row in df.iterrows():
    if row['TEAM_1_XG'] > row['TEAM_2_XG']:
        G.add_edge(row['TEAM_2'], row['TEAM_1'])
    elif row['TEAM_2_XG'] > row['TEAM_1_XG']:
        G.add_edge(row['TEAM_1'], row['TEAM_2'])
    elif row['TEAM_1_XG'] == row['TEAM_2_XG']:
        G.add_edge(row['TEAM_1'], row['TEAM_2'])
        G.add_edge(row['TEAM_2'], row['TEAM_1'])



edge_labels = {(row['TEAM_1'], row['TEAM_2']): f"{row['TEAM_1_XG']}-{row['TEAM_2_XG']}" for _, row in df.iterrows() if row['TEAM_1']}
edge_labels = {(row['TEAM_2'], row['TEAM_1']): f"{row['TEAM_2_XG']}-{row['TEAM_1_XG']}" for _, row in df.iterrows() if row['TEAM_2'] }
nx.draw_networkx_edge_labels(G, pos=nx.spring_layout(G, seed=33212), edge_labels=edge_labels, font_size = 10, font_color='red', label_pos=0.3)


edge_num = len(G.edges())
nodes_num = len(G.nodes())
density = edge_num / (nodes_num * (nodes_num - 1)) if nodes_num > 1 else 0
print(f"Edge Density: {density}")

options = {"font_size": 4, "node_size": 150, "node_color": "lightblue", "edge_color": "gray", "linewidths": 1, "width": 1}

pos = nx.spring_layout(G, seed=33212) 
nx.draw(G, pos=pos, with_labels=True, **options)
plt.show()