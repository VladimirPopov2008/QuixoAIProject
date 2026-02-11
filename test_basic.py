from game import Game
from tournament import Tournament

# Test a single game
print('Testing single game...')
game = Game(play_mode='RANDOM', output_mode='VERBOSE')
result = game.play()
print(f'Game result: {result}')

# Test a small tournament
print('\nTesting tournament...')
tournament = Tournament(num_games=10, play_mode='RANDOM')
tournament.run()

print('\nBasic tests passed!')
