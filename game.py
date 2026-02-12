import numpy as np
import json
import random

def hash_board(board):
   return np.array2string(board.flatten(), separator='')

class Game:
    def __init__(self, play_mode='RANDOM', output_mode='SILENT', states_dict=None, 
                 epsilon=0.1, unknown_score=0.5, discount_factor=0.9, 
                 win_score=1.0, loss_score=0.0):
        self.play_mode = play_mode
        self.output_mode = output_mode
        self.states_dict = states_dict or {}
        self.epsilon = epsilon
        self.unknown_score = unknown_score
        self.discount_factor = discount_factor
        self.win_score = win_score
        self.loss_score = loss_score
        self.board = np.full((5, 5), ' ')
        self.current_player = 'X'
        self.board_history = []
        self.outcome = 'ONGOING'
        self.unknown_count = 0  # Counter for unknown boards
        self.total_moves = 0  # Counter for total moves

    def play(self):
        self.board_history = []
        self.unknown_count = 0  # Reset unknown count
        self.total_moves = 0  # Reset total moves
        while self.outcome == 'ONGOING':
            self.board_history.append(hash_board(self.board))
            self.total_moves += 1
            if hash_board(self.board) not in self.states_dict:
                self.unknown_count += 1
            if self.current_player == 'X':
                if self.play_mode == 'GREEDY':
                    self.perform_greedy_agent_move()
                else:
                    self.perform_random_agent_move()
            else:
                self.perform_random_opponent_move()
            self.outcome = self.check_win()
            if self.outcome == 'ONGOING':
                self.current_player = 'O' if self.current_player == 'X' else 'X'
        return self.score_boards(), self.unknown_count / self.total_moves if self.total_moves > 0 else 0

    def perform_random_agent_move(self):
        valid_moves = self.get_valid_moves()
        move = random.choice(valid_moves)
        self.make_move(*move)

    def perform_random_opponent_move(self):
        valid_moves = self.get_valid_moves()
        move = random.choice(valid_moves)
        self.make_move(*move)

    def perform_greedy_agent_move(self):
        valid_moves = self.get_valid_moves()
        if random.random() < self.epsilon:
            move = random.choice(valid_moves)
        else:
            best_score = -float('inf')
            best_moves = []
            for move in valid_moves:
                board_copy = self.board.copy()
                self.make_move(*move)
                board_hash = hash_board(self.board)
                score = self.states_dict.get(board_hash, [self.unknown_score, 1])[0]
                self.board = board_copy
                if score > best_score:
                    best_score = score
                    best_moves = [move]
                elif score == best_score:
                    best_moves.append(move)
            move = random.choice(best_moves)
        self.make_move(*move)

    def get_valid_moves(self):
        valid_moves = []
        for row in range(5):
            for col in range(5):
                if self.is_edge(row, col) and (self.board[row, col] in {self.current_player, ' '}):
                    for direction in self.get_valid_directions(row, col):
                        valid_moves.append((row, col, direction))
        return valid_moves

    def is_edge(self, row, col):
        return row == 0 or row == 4 or col == 0 or col == 4

    def get_valid_directions(self, row, col):
        directions = []
        if row == 0:
            directions.append(2)  # Down
        if row == 4:
            directions.append(0)  # Up
        if col == 0:
            directions.append(1)  # Right
        if col == 4:
            directions.append(3)  # Left
        return directions

    def make_move(self, row, col, direction):
        piece = self.current_player
        if direction == 0:  # Push up
            for r in range(row, 0, -1):
                self.board[r, col] = self.board[r-1, col]
            self.board[0, col] = piece
        elif direction == 1:  # Push right
            for c in range(col, 4):
                self.board[row, c] = self.board[row, c+1]
            self.board[row, 4] = piece
        elif direction == 2:  # Push down
            for r in range(row, 4):
                self.board[r, col] = self.board[r+1, col]
            self.board[4, col] = piece
        elif direction == 3:  # Push left
            for c in range(col, 0, -1):
                self.board[row, c] = self.board[row, c-1]
            self.board[row, 0] = piece

    def check_win(self):
        for symbol in {'X', 'O'}:
            for row in range(5):
                if all(self.board[row, col] == symbol for col in range(5)):
                    return 'VICTORY_X' if symbol == 'X' else 'VICTORY_O'
            for col in range(5):
                if all(self.board[row, col] == symbol for row in range(5)):
                    return 'VICTORY_X' if symbol == 'X' else 'VICTORY_O'
            if all(self.board[i, i] == symbol for i in range(5)):
                return 'VICTORY_X' if symbol == 'X' else 'VICTORY_O'
            if all(self.board[i, 4-i] == symbol for i in range(5)):
                return 'VICTORY_X' if symbol == 'X' else 'VICTORY_O'
        return 'ONGOING'

    def score_boards(self):
        scored_boards = {}
        n_boards = len(self.board_history)
        if self.outcome == 'VICTORY_X':
            final_score = self.win_score
        else:
            final_score = self.loss_score
        for i, board_hash in enumerate(self.board_history):
            discount = self.discount_factor ** (n_boards - i - 1)
            scored_boards[board_hash] = discount * final_score
        return scored_boards

    def print_board(self):
        for row in self.board:
            print("|" + "|".join(row) + "|")

    def print_result(self):
        if self.outcome == 'VICTORY_X':
            print("X Wins!")
        elif self.outcome == 'VICTORY_O':
            print("O Wins!")
        else:
            print("Game ongoing.")