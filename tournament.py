import json
from game import Game

class Tournament:
    def __init__(self, states_dict=None):
        """
        Initialize a tournament of multiple games.
        
        Args:
            states_dict: Dictionary of board states for greedy agent
        """
        
        self.states_dict = states_dict or {}

        
        # Statistics
        self.stats = {
            'VICTORY_X': 0,
            'VICTORY_O': 0
        }
        

    def run(self, num_games=1000, play_mode='RANDOM', train_mode=False):
        """
        Run the tournament for the specified number of games.
        """
        unknown_rates = []
        for _ in range(num_games):
            game = Game(play_mode=play_mode, states_dict=self.states_dict)
            scores, unknown_rate = game.play()  # Get unknown rate from game

            self.save_game_to_dict(scores)

            unknown_rates.append(unknown_rate)  # Store unknown rate
            if game.outcome == 'VICTORY_X':
                self.stats['VICTORY_X'] += 1
            elif game.outcome == 'VICTORY_O':
                self.stats['VICTORY_O'] += 1

        # Calculate average and variance of unknown rates
        avg_unknown_rate = sum(unknown_rates) / len(unknown_rates) if unknown_rates else 0
        variance_unknown_rate = sum((x - avg_unknown_rate) ** 2 for x in unknown_rates) / len(unknown_rates) if unknown_rates else 0

        print("\nUnknown Board Statistics:")
        print(f"Average Unknown Rate: {avg_unknown_rate:.4f}")
        print(f"Variance of Unknown Rate: {variance_unknown_rate:.4f}")

        return unknown_rates

    def save_game_to_dict(self, game_scores):
       for board_hash, score in game_scores.items():
           if board_hash not in self.states_dict:
               self.states_dict[board_hash] = [score, 1]
           else:
               total, count = self.states_dict[board_hash]
               new_count = count + 1
               new_avg = (total * count + score) / new_count
               self.states_dict[board_hash] = [new_avg, new_count]

    def save_dict_to_file(self, filename):
        """
        Save the board dictionary to a JSON file.
        
        Args:
            filename: Path to the JSON file
        """
        with open(filename, 'w') as f:
            json.dump(self.states_dict, f)

    def print_results(self):
        """Print tournament statistics."""
        print("\n" + "="*50)
        print("TOURNAMENT RESULTS")
        print("="*50)
        print(f"X Wins: {self.stats['VICTORY_X']}")
        print(f"O Wins: {self.stats['VICTORY_O']}")
        print("="*50 + "\n")
