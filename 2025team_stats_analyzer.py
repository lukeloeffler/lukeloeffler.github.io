import json

def load_data(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data

scraped_data = load_data('2025team_stats.json')

def calculate_possessions(team):
    return team['fg_attempted'] + 0.44 * team['ft_attempted'] - team['off_rebounds'] + team['turnovers']

def calculate_offensive_efficiency(team):
    possessions = calculate_possessions(team)
    if possessions == 0:
        return 0  # Handle division by zero
    return (team['points'] / possessions) * 100

def calculate_defensive_efficiency(team, opponent_stats):
    opponent_possessions = opponent_stats['fg_attempted'] + 0.44 * opponent_stats['ft_attempted'] - opponent_stats['off_rebounds'] + opponent_stats['turnovers']
    if opponent_possessions == 0:
        return 0
    return (team['opp_points'] / opponent_possessions) * 100

# Example usage
for team in scraped_data:
    team['possessions'] = calculate_possessions(team)
    team['offensive_efficiency'] = calculate_offensive_efficiency(team)

#To calculate defensive efficiency, you would need to iterate through each teams games and calculate the opponents stats for each game. That is a more complex undertaking.
#For the purposes of this example, I will leave defensive efficiency out, but it is important for the final product.