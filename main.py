import json
import sys
from game import Game
from tournament import Tournament

if __name__ == "__main__":


    with open('states_greedy.json', 'r') as f:
        states_dict = json.load(f)


    tournament = Tournament(states_dict=states_dict)
    tournament.run(1000, play_mode='GREEDY', train_mode=True)
    tournament.print_results()