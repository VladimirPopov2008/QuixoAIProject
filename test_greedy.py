import json
from game import Game
from tournament import Tournament

# Load test states
print('Loading test states...')
with open('test_states.json', 'r') as f:
    greedy_dict = json.load(f)
print(f'Loaded {len(greedy_dict)} board states')

# Test greedy agent
print('\nTesting greedy agent (100 games)...')
greedy_tournament = Tournament(
    num_games=100,
    play_mode='GREEDY',
    greedy_dict=greedy_dict
)
greedy_tournament.run()

print('\nGreedy agent test completed!')
print('The greedy agent should perform better than random (~50%).')
