import json
from game import Game
import numpy as np


class Tournament:
    def __init__(self, games=100, play_mode="RANDOM", epsilon=0.1):
        self.games = games
        self.play_mode = play_mode
        self.epsilon = epsilon
        self.stats = {"VICTORY_X": 0, "VICTORY_O": 0, "TIE": 0}
        self.states_dict = {}
        self.unknown_ratios = []

    def run(self):
        for _ in range(self.games):
            game = Game(
                play_mode=self.play_mode,
                states_dict=self.states_dict,
                epsilon=0  # חשוב! בלי אקראיות
            )
            result = game.play()
            self.stats[result] += 1
            self.save_game_to_dict(game)

            self.unknown_ratios.append(game.unknown_ratio())


    def save_game_to_dict(self, game):
        for state, score in game.score_boards():
            if state not in self.states_dict:
                self.states_dict[state] = [score, 1]
            else:
                avg, count = self.states_dict[state]
                self.states_dict[state][0] = (avg * count + score) / (count + 1)
                self.states_dict[state][1] += 1


    def save_dict(self, filename):
        serializable = {str(k): v for k, v in self.states_dict.items()}
        with open(filename, "w") as f:
            json.dump(serializable, f)

    def unknown_stats(self):
        arr = np.array(self.unknown_ratios)
        return arr.mean(), arr.var()