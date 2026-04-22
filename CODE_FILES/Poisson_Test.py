import numpy as np 
from scipy.stats import poisson 


#This was an idea I had, at one stage, but did not end up using it. 

Team_1 = [2.9]
Team_2 = [1.0]

# Maximum number of goals to consider 
max_goals = 9

# Calculate goal probabilities for Team A and Team B 
team_A_goal_probs = [poisson.pmf(i, team_1_lambda) for i in range(max_goals + 1) for team_1_lambda in Team_1]
team_B_goal_probs = [poisson.pmf(i, team_2_lambda) for i in range(max_goals + 1) for team_2_lambda in Team_2]


match_probs = np.outer(team_A_goal_probs, team_B_goal_probs)

# Probability of Team A winning 
P_win = np.sum(np.tril(match_probs, -1)) 


P_draw = np.sum(np.diag(match_probs)) 


P_loss = np.sum(np.triu(match_probs, 1)) 

print(f"Probability of Win: {P_win:.4f}") 
print(f"Probability of Draw: {P_draw:.4f}") 
print(f"Probability of Loss: {P_loss:.4f}")


expected_points = (3 * P_win) + (1 * P_draw) 

print(f"Expected Points for Team 2: {expected_points:.2f}")

print(f"Expected Points for Team 2: {(3 * P_loss) + (1 * P_draw):.2f}")

