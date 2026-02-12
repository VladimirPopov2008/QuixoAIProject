

import random
import numpy as np
import json


def hash_board(board):
   return np.array2string(board.flatten(), separator='')


class Game:
   def __init__(self, play_mode='RANDOM', output_mode='SILENT', tournament_data=None):
       self.play_mode = play_mode
       self.output_mode = output_mode
       self.outcome = 'ONGOING'
       self.board = np.full((5,5), ' ')
       self.current_player = 'X'
       self.board_history = []
       self.win_score = 1.0
       self.lose_score = 0.0
       self.discount = 0.9
       self.epsilon = 0.1
       self.unknown_score = 0.5
       self.tournament_data = tournament_data or {}


   def play(self):
       self.board_history = []
       unknown_count = 0
       total_moves = 0


       while self.outcome == 'ONGOING':
           board_hash = hash_board(self.board.copy())
           self.board_history.append(board_hash)
           total_moves += 1
           if board_hash not in self.tournament_data:
               unknown_count += 1


           if self.current_player == 'X':
               if self.play_mode == 'RANDOM':
                   self.perform_random_agent_move()
               else:
                   self.perform_greedy_agent_move()
           else:
               self.perform_random_agent_move()


           self.outcome = self.check_win()
           self.current_player = 'O' if self.current_player == 'X' else 'X'


       if self.output_mode != 'SILENT':
           self.print_board()
           self.print_result()


       unknown_rate = unknown_count / total_moves if total_moves > 0 else 0
       return self.score_boards(), unknown_rate


   def is_valid_move(self, row, col):
       return row == 0 or row == 4 or col == 0 or col == 4


   def make_human_move(self, row, col):
       if self.is_valid_move(row, col):
           directions = self.get_valid_directions(row, col)
           direction = random.choice(directions)
           self.push_cube(row, col, direction, self.current_player)
           self.outcome = self.check_win()
           self.current_player = 'O' if self.current_player == 'X' else 'X'


   def perform_random_agent_move(self):
       edges = self.get_edge_positions()
       row, col = random.choice(edges)
       directions = self.get_valid_directions(row, col)
       direction = random.choice(directions)
       self.push_cube(row, col, direction, self.current_player)


   def perform_greedy_agent_move(self):
       edges = self.get_edge_positions()
       move_scores = []
       for row, col in edges:
           for direction in self.get_valid_directions(row, col):
               board_copy = self.board.copy()
               self.push_cube(row, col, direction, self.current_player)
               board_hash = hash_board(self.board)
               score = self.tournament_data.get(board_hash, [self.unknown_score, 1])[0]
               move_scores.append(((row, col, direction), score))
               self.board = board_copy
       if random.random() < self.epsilon:
           move = random.choice(move_scores)[0]
       else:
           move_scores.sort(key=lambda x: x[1], reverse=True)
           move = move_scores[0][0]
       self.push_cube(move[0], move[1], move[2], self.current_player)


   def get_edge_positions(self):
       return [(i,j) for i in range(5) for j in range(5)
               if i == 0 or i == 4 or j == 0 or j == 4]


   def get_valid_directions(self, row, col):
       directions = []
       if row == 0: directions.append("down")
       if row == 4: directions.append("up")
       if col == 0: directions.append("right")
       if col == 4: directions.append("left")
       return directions


   def push_cube(self, row, col, direction, symbol):
        if direction == "down":
            for i in range(row, 4):
                self.board[i][col] = self.board[i+1][col]
            self.board[4][col] = symbol
        elif direction == "up":
            for i in range(row, 0, -1):
                self.board[i][col] = self.board[i-1][col]
            self.board[0][col] = symbol
        elif direction == "right":
            for i in range(col, 4):
                self.board[row][i] = self.board[row][i+1]
            self.board[row][4] = symbol
        elif direction == "left":
            for i in range(col, 0, -1):
                self.board[row][i] = self.board[row][i-1]
            self.board[row][0] = symbol


   def check_win(self):
       for symbol in ['X', 'O']:
           for row in range(5):
               if all(self.board[row, col] == symbol for col in range(5)):
                   return 'VICTORY_X' if symbol == 'X' else 'VICTORY_Y'
           for col in range(5):
               if all(self.board[row, col] == symbol for row in range(5)):
                   return 'VICTORY_X' if symbol == 'X' else 'VICTORY_Y'
           if all(self.board[i, i] == symbol for i in range(5)) or \
              all(self.board[i, 4-i] == symbol for i in range(5)):
               return 'VICTORY_X' if symbol == 'X' else 'VICTORY_Y'
       return 'ONGOING'


   def score_boards(self):
       scores = {}
       n = len(self.board_history)
       if self.outcome == 'VICTORY_X':
           final_score = self.win_score
       else:
           final_score = self.lose_score
       for i, board_hash in enumerate(self.board_history):
           score = (self.discount ** (n - i - 1)) * final_score
           scores[board_hash] = score
       return scores


   def reset_game(self):
       self.board = np.full((5,5), ' ')
       self.current_player = 'X'
       self.outcome = 'ONGOING'
       self.board_history = []


   def print_board(self):
       for row in self.board:
           print("|" + "|".join(row) + "|")


   def print_result(self):
       if self.outcome == 'VICTORY_X':
           print("X ניצח")
       elif self.outcome == 'VICTORY_Y':
           print("O ניצח")


class Tournament:
   def __init__(self, tournament_data=None):
       self.data = tournament_data or {}
       self.x_wins = 0
       self.o_wins = 0


   def run_tournament(self, games_count, play_mode='RANDOM'):
       unknown_rates = []
       for _ in range(games_count):
           game = Game(play_mode=play_mode, tournament_data=self.data)
           scores, unknown_rate = game.play()
           self.save_game_to_dict(scores)
           unknown_rates.append(unknown_rate)
           if game.outcome == 'VICTORY_X':
               self.x_wins += 1
           elif game.outcome == 'VICTORY_Y':
               self.o_wins += 1
       return unknown_rates


   def save_game_to_dict(self, game_scores):
       for board_hash, score in game_scores.items():
           if board_hash not in self.data:
               self.data[board_hash] = [score, 1]
           else:
               total, count = self.data[board_hash]
               new_count = count + 1
               new_avg = (total * count + score) / new_count
               self.data[board_hash] = [new_avg, new_count]


   def print_results(self):
       print("X ניצח:", self.x_wins)
       print("O ניצח:", self.o_wins)


   def save_to_json(self, filename):
       with open(filename, 'w') as f:
           json.dump(self.data, f)




if __name__ == "__main__":
   

   with open('states_greedy.json', 'r') as f:
        tournament_data = json.load(f)

   tournament = Tournament(tournament_data=tournament_data)
   tournament.run_tournament(1000, play_mode='GREEDY')
   tournament.print_results()
   #tournament.save_to_json("game_data.json")