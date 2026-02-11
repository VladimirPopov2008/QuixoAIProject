import json
import sys
from game import Game
from tournament import Tournament

with open('states_greedy.json', 'r') as f:
    greedy_dict = json.load(f)


if __name__ == "__main__":
   tournament = Tournament(num_games=1000, play_mode='GREEDY', greedy_dict=greedy_dict, save_boards=True)
   tournament.run()
   #tournament.save_to_json("game_data.json")