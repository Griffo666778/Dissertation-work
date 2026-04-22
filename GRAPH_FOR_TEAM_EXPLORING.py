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


G = nx.Graph()
G.add_nodes_from(teams)

# Add undirected edges 
for _, row in df.iterrows():
    # Add edge if their is a match
    G.add_edge(row['TEAM_1'], row['TEAM_2'])

# Create subgraph for a specific team
TEAM_A = 'Arsenal' 

clubs_to_include = [TEAM_A]




connected_nodes = set(G.neighbors(TEAM_A))
nodes_to_keep = clubs_to_include + list(connected_nodes)
subG = G.subgraph(nodes_to_keep).copy()


# Create edge labels for edges
edge_labels = {}
for u, v in subG.edges():
    row = df[((df['TEAM_1'] == u) & (df['TEAM_2'] == v)) | ((df['TEAM_1'] == v) & (df['TEAM_2'] == u))]
    if not row.empty:
        row = row.iloc[0]
        xg_1 = row['TEAM_1_XG']
        xg_2 = row['TEAM_2_XG']
        edge_labels[(u, v)] = f"{xg_1}-{xg_2}"


#Draw edges properly, not necessary, doesn't make it look good, 
#nx.draw_networkx_edge_labels(subG, pos=nx.circular_layout(subG), edge_labels=edge_labels, font_size=10, font_color='red')


edge_num = len(subG.edges())
nodes_num = len(subG.nodes())
density = edge_num / (nodes_num * (nodes_num - 1))
print(f"Edge Density: {density}")

options = {"font_size": 8, "node_size": 1500, "node_color": "lightblue", "edge_color": "gray", "linewidths": 1, "width": 1}

pos = nx.circular_layout(subG)
nx.draw(subG, pos=pos, with_labels=True, **options)
plt.savefig(r"\IMAGES\graph.png")
plt.show()  