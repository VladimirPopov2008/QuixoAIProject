import numpy as np
import random

BOARD_SIZE = 5
EMPTY = 0
PLAYER_X = 1
PLAYER_O = -1


def hash_board(board, current_player):
    return np.array2string(board.flatten(), separator='') + str(current_player)




class Game:
    def __init__(self, play_mode="RANDOM", states_dict=None,
                 win_reward=10.0, draw_reward=0.5, lose_reward=0.0,
                 gamma=0.9, unknown_state_score=0.5, epsilon=0.1):
        self.play_mode = play_mode
        self.states_dict = states_dict or {}
        self.win_reward = win_reward
        self.draw_reward = draw_reward
        self.lose_reward = lose_reward
        self.gamma = gamma
        self.unknown_state_score = unknown_state_score
        self.epsilon = epsilon
        self.reset_game()

    def reset_game(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.free_positions = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)]
        self.current_player = PLAYER_X
        self.state = "ONGOING"
        self.history = []
        self.unknown_moves = 0
        self.total_moves = 0


    def play(self):
        while self.state == "ONGOING":
            self.history.append(hash_board(self.board, self.current_player))

            if self.current_player == PLAYER_X:
                self.perform_agent_move()
            else:
                self.perform_random_move()

            self.state = self.check_game_state()
            self.current_player *= -1

        return self.state

    def perform_agent_move(self):
        if self.play_mode == "GREEDY":
            # epsilon-greedy
            if random.random() < self.epsilon:
                self.perform_random_move()
            else:
                self.perform_greedy_agent_move()
        else:
            self.perform_random_move()


    def perform_random_move(self):
        pos = random.choice(self.free_positions)
        self.make_move(pos)

    def perform_greedy_agent_move(self):
        best_score = -1
        best_moves = []

        for pos in self.free_positions:
            temp_board = self.board.copy()
            temp_board[pos] = self.current_player
            key = hash_board(temp_board, -self.current_player)

            if key not in self.states_dict:
                score = self.unknown_state_score
            else:
                score = self.states_dict[key][0]

            if score > best_score:
                best_score = score
                best_moves = [(pos, key)]
            elif score == best_score:
                best_moves.append((pos, key))

        pos, key = random.choice(best_moves)

        # ספירה
        self.total_moves += 1
        if key not in self.states_dict:
            self.unknown_moves += 1

        self.make_move(pos)


    def make_move(self, pos):
        r, c = pos
        self.board[r, c] = self.current_player
        self.free_positions.remove(pos)

    def check_game_state(self):
        lines = []
        lines.extend(self.board)
        lines.extend(self.board.T)
        lines.append(np.diag(self.board))
        lines.append(np.diag(np.fliplr(self.board)))

        for line in lines:
            if np.all(line == PLAYER_X):
                return "VICTORY_X"
            if np.all(line == PLAYER_O):
                return "VICTORY_O"

        if not self.free_positions:
            return "TIE"

        return "ONGOING"
    

    def score_boards(self):
        final_score = {
            "VICTORY_X": self.win_reward,
            "VICTORY_O": self.lose_reward,
            "TIE": self.draw_reward
        }[self.state]

        scored_states = []
        for i, state in enumerate(reversed(self.history)):
            score = final_score * (self.gamma ** i)
            scored_states.append((state, score))

        return scored_states
    
    def unknown_ratio(self):
        if self.total_moves == 0:
            return 0.0
        return self.unknown_moves / self.total_moves