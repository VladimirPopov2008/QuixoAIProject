import json
import numpy as np
from game import Game

class Tournament:
    """
    Tournament that can use `lookup_dict` for move evaluation inside Game
    but accumulate scored states into a separate `storage_dict`.
    """

    def __init__(self, games=100, play_mode="RANDOM", epsilon=0.1,
                 lookup_dict=None, storage_dict=None):
        self.games = games
        self.play_mode = play_mode
        self.epsilon = epsilon
        # lookup_dict is passed into each Game so the agent can consult it when ranking moves
        self.lookup_dict = lookup_dict or {}
        # storage_dict accumulates scored states from the games in this tournament
        self.storage_dict = storage_dict or {}
        self.stats = {"VICTORY_X": 0, "VICTORY_O": 0, "TIE": 0}
        self.unknown_ratios = []

    def run(self):
        # reset stats each run
        self.stats = {"VICTORY_X": 0, "VICTORY_O": 0, "TIE": 0}
        self.unknown_ratios = []

        for _ in range(self.games):
            # pass lookup_dict into Game for move ranking
            game = Game(
                play_mode=self.play_mode,
                states_dict=self.lookup_dict,
                epsilon=self.epsilon
            )
            result = game.play()
            self.stats[result] += 1

            # accumulate scored states into storage_dict (not into lookup_dict)
            self.save_game_to_dict(game)

            self.unknown_ratios.append(game.unknown_ratio())

    def save_game_to_dict(self, game):
        for state, score in game.score_boards():
            if state not in self.storage_dict:
                self.storage_dict[state] = [score, 1]
            else:
                avg, count = self.storage_dict[state]
                self.storage_dict[state][0] = (avg * count + score) / (count + 1)
                self.storage_dict[state][1] += 1

    def save_dict(self, filename):
        # keys are strings already in your setup; convert to str to be safe
        serializable = {str(k): v for k, v in self.storage_dict.items()}
        with open(filename, "w") as f:
            json.dump(serializable, f)

    def unknown_stats(self):
        if not self.unknown_ratios:
            return 0.0, 0.0
        arr = np.array(self.unknown_ratios)
        return float(arr.mean()), float(arr.var())