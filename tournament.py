import json
from game import Game


class Tournament:
    def __init__(self, states_dict=None):
        """
        Initialize a tournament of multiple games.

        Args:
            states_dict: Dictionary of board states for greedy/heuristic agent
        """
        self.states_dict = states_dict or {}
        self.stats = {
            'VICTORY_X': 0,
            'VICTORY_O': 0
        }

    def run(self, num_games=1000, play_mode='RANDOM', epsilon=0.1):
        """
        Run the tournament for the specified number of games.

        Args:
            num_games: Number of games to play
            play_mode: 'RANDOM', 'GREEDY', or 'HEURISTIC'
            epsilon: Exploration rate for greedy/heuristic agents

        Returns:
            List of unknown_rates per game
        """
        unknown_rates = []
        for i in range(num_games):
            game = Game(play_mode=play_mode, states_dict=self.states_dict,
                        epsilon=epsilon)
            scores, unknown_rate = game.play()
            self.save_game_to_dict(scores)
            unknown_rates.append(unknown_rate)
            if game.outcome == 'VICTORY_X':
                self.stats['VICTORY_X'] += 1
            elif game.outcome == 'VICTORY_O':
                self.stats['VICTORY_O'] += 1

        return unknown_rates

    def save_game_to_dict(self, game_scores):
        """Update the states dictionary with scores from a completed game."""
        for board_hash, score in game_scores.items():
            if board_hash not in self.states_dict:
                self.states_dict[board_hash] = [score, 1]
            else:
                total, count = self.states_dict[board_hash]
                new_count = count + 1
                new_avg = (total * count + score) / new_count
                self.states_dict[board_hash] = [new_avg, new_count]

    def save_dict_to_file(self, filename):
        """Save the board dictionary to a JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.states_dict, f, indent=4)

    def print_results(self, label=""):
        """Print tournament statistics."""
        total = self.stats['VICTORY_X'] + self.stats['VICTORY_O']
        print("\n" + "=" * 50)
        if label:
            print(f"TOURNAMENT RESULTS – {label}")
        else:
            print("TOURNAMENT RESULTS")
        print("=" * 50)
        print(f"X Wins: {self.stats['VICTORY_X']}")
        print(f"O Wins: {self.stats['VICTORY_O']}")
        if total > 0:
            print(f"X Win Rate: {self.stats['VICTORY_X'] / total * 100:.1f}%")
        print("=" * 50 + "\n")

    @staticmethod
    def print_unknown_stats(unknown_rates, label=""):
        """Print average and variance of unknown board rates."""
        if not unknown_rates:
            return
        avg = sum(unknown_rates) / len(unknown_rates)
        var = sum((x - avg) ** 2 for x in unknown_rates) / len(unknown_rates)
        if label:
            print(f"Unknown Board Statistics – {label}:")
        else:
            print("Unknown Board Statistics:")
        print(f"  Average Unknown Rate: {avg:.4f}")
        print(f"  Variance:             {var:.6f}")

    @staticmethod
    def print_dict_quality(states_dict, label=""):
        """Print score distribution of a dictionary."""
        excellent = 0  # score > 0.8
        good = 0       # 0.6 < score <= 0.8
        medium = 0     # 0.4 < score <= 0.6
        weak = 0       # score <= 0.4
        for board_hash, (score, count) in states_dict.items():
            if score > 0.8:
                excellent += 1
            elif score > 0.6:
                good += 1
            elif score > 0.4:
                medium += 1
            else:
                weak += 1
        total = len(states_dict)
        if label:
            print(f"\nDictionary Quality – {label} ({total} boards total):")
        else:
            print(f"\nDictionary Quality ({total} boards total):")
        print(f"  Excellent (score > 0.8): {excellent}")
        print(f"  Good  (0.6 < score <= 0.8): {good}")
        print(f"  Medium (0.4 < score <= 0.6): {medium}")
        print(f"  Weak   (score <= 0.4): {weak}")
