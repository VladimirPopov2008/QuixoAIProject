import numpy as np
import random

BOARD_SIZE = 5
EMPTY = 0
PLAYER_X = 1
PLAYER_O = -1


def hash_board(board, current_player):
    # flatten to tuple then stringify with a delimiter
    return ','.join(map(str, board.flatten().tolist())) + '|' + str(current_player)


class Game:
    """
    Quixo game (full push mechanics for a 5x5 board).

    Rules implemented:
    - A player may choose any cube that lies on the outer border (edge or corner)
      provided that the cube is either empty or already shows that player's symbol.
    - When selecting a border cube, the player turns the cube to show their symbol
      and pushes it back into its row or column from that side:
        * If the selected cube is on the top edge (r == 0) -> column push: the cube
          is inserted at the bottom of the column and the column shifts up.
        * If on the bottom edge (r == 4) -> column push inserted at top (column shifts down).
        * If on the left edge (c == 0) -> row push inserted at right (row shifts left).
        * If on the right edge (c == 4) -> row push inserted at left (row shifts right).
        * Corner cubes allow either row or column push (player chooses).
    - A player may NOT select an opponent's cube.
    - The game ends when a player has five of their marks in a row (row/col/diag).
    - To prevent pathological infinite games, an optional max_turns cap is available.
      By default it's large (10_000) but can be set smaller for testing.
    """
    def __init__(self, play_mode="RANDOM", states_dict=None,
                 win_reward=10.0, draw_reward=0.5, lose_reward=0.0,
                 gamma=0.9, unknown_state_score=0.5, epsilon=0.1,
                 max_turns=10000):
        self.play_mode = play_mode
        self.states_dict = states_dict or {}
        self.win_reward = win_reward
        self.draw_reward = draw_reward
        self.lose_reward = lose_reward
        self.gamma = gamma
        self.unknown_state_score = unknown_state_score
        self.epsilon = epsilon
        self.max_turns = max_turns
        self.reset_game()

    def reset_game(self):
        # In Quixo all cells are always occupied with some face (we use 0 for blank)
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.current_player = PLAYER_X
        self.state = "ONGOING"
        self.history = []
        # stats for greedy unknown moves
        self.unknown_moves = 0
        self.total_moves = 0
        self.turns_played = 0

    # ----------------------
    # Utility / mechanics
    # ----------------------
    def outer_positions(self):
        """Return list of border positions (r,c)"""
        positions = []
        n = BOARD_SIZE - 1
        for c in range(BOARD_SIZE):
            positions.append((0, c))
            if n != 0:
                positions.append((n, c))
        for r in range(1, BOARD_SIZE - 1):
            positions.append((r, 0))
            if n != 0:
                positions.append((r, n))
        # remove duplicates (corners were added twice if BOARD_SIZE==1 etc.)
        return list(dict.fromkeys(positions))

    def allowed_outer_moves(self, player):
        """
        Return list of candidate moves available for `player`.
        Each candidate is (pos, axis) where axis is 'row' or 'col'.
        Non-corner edges have a single axis; corners have both.
        A border cube may be selected only if it's EMPTY or already shows player's mark.
        """
        candidates = []
        for (r, c) in self.outer_positions():
            val = int(self.board[r, c])
            if val != EMPTY and val != player:
                continue  # cannot select opponent's cube
            # determine possible axes
            is_top = (r == 0)
            is_bottom = (r == BOARD_SIZE - 1)
            is_left = (c == 0)
            is_right = (c == BOARD_SIZE - 1)

            # corners: allow both axes
            if (is_top or is_bottom) and (is_left or is_right):
                # corner: both row and column pushes are allowed
                candidates.append(((r, c), 'row'))
                candidates.append(((r, c), 'col'))
            else:
                # edge (non-corner): axis is determined by which edge
                if is_top or is_bottom:
                    candidates.append(((r, c), 'col'))
                else:
                    candidates.append(((r, c), 'row'))
        return candidates

    def  _simulate_push(self, board, pos, axis, player):
        """
        Return a new board (numpy array) that results from selecting `pos`,
        turning it to `player`, and pushing along `axis` ('row'/'col').
        This does not modify `board`.
        """
        r, c = pos
        moved = int(player)  # the cube placed will show the player's mark
        new = board.copy()

        if axis == 'col':
            # vertical push: direction depends on whether pos is top or bottom
            if r == 0:
                # selected at top -> insert at bottom, shift column up
                col = list(new[:, c])
                # remove top element (pos), shift upward and append moved at bottom
                # but since we replace at pos with player, we simply build new col:
                # new_col = [col[1], col[2], ..., col[4], moved]
                new_col = col[1:] + [moved]
                new[:, c] = new_col
            elif r == BOARD_SIZE - 1:
                # selected at bottom -> insert at top, shift column down
                col = list(new[:, c])
                # new_col = [moved, col[0], col[1], ..., col[3]]
                new_col = [moved] + col[:-1]
                new[:, c] = new_col
            else:
                # shouldn't happen: col pushes only allowed on border positions
                raise ValueError("Column push requested from non-border position")
        elif axis == 'row':
            # horizontal push: direction depends on left/right
            if c == 0:
                # selected at left -> insert at right, shift row left
                row = list(new[r, :])
                new_row = row[1:] + [moved]
                new[r, :] = new_row
            elif c == BOARD_SIZE - 1:
                # selected at right -> insert at left, shift row right
                row = list(new[r, :])
                new_row = [moved] + row[:-1]
                new[r, :] = new_row
            else:
                raise ValueError("Row push requested from non-border position")
        else:
            raise ValueError("Unknown axis: " + str(axis))

        return new

    def _apply_push(self, pos, axis, player):
        """
        Apply a push to self.board in-place: select pos, set face to player, push along axis.
        """
        self.board = self._simulate_push(self.board, pos, axis, player)

    # ----------------------
    # Move performers
    # ----------------------
    def perform_random_move(self):
        """
        Random legal Quixo move:
        - choose a random allowed outer (pos,axis)
        - apply push
        """
        candidates = self.allowed_outer_moves(self.current_player)
        if not candidates:
            # theoretically impossible in Quixo, but keep safe
            return
        pos, axis = random.choice(candidates)
        self._apply_push(pos, axis, self.current_player)

    def perform_agent_move(self):
        if self.play_mode == "GREEDY":
            # epsilon-greedy
            if random.random() < self.epsilon:
                self.perform_random_move()
            else:
                self.perform_greedy_agent_move()
        else:
            self.perform_random_move()

    def perform_greedy_agent_move(self):
        """
        Evaluate all possible legal Quixo moves using states_dict (lookup of post-move states).
        If a resulting post-move state is unknown, use unknown_state_score.
        Choose random among best moves. Update unknown counters.
        """
        candidates = self.allowed_outer_moves(self.current_player)
        if not candidates:
            return

        best_score = -float('inf')
        best_moves = []

        for pos, axis in candidates:
            temp_board = self._simulate_push(self.board, pos, axis, self.current_player)
            key = hash_board(temp_board, -self.current_player)  # next player to move

            if key not in self.states_dict:
                score = self.unknown_state_score
            else:
                score = self.states_dict[key][0]

            if score > best_score:
                best_score = score
                best_moves = [(pos, axis, key)]
            elif score == best_score:
                best_moves.append((pos, axis, key))

        pos, axis, key = random.choice(best_moves)

        # stats
        self.total_moves += 1
        if key not in self.states_dict:
            self.unknown_moves += 1

        self._apply_push(pos, axis, self.current_player)

    # ----------------------
    # Core loop & checking
    # ----------------------
    def play(self):
        self.turns_played = 0
        while self.state == "ONGOING" and self.turns_played < self.max_turns:
            # record pre-move state with current player-to-move
            self.history.append(hash_board(self.board, self.current_player))

            if self.current_player == PLAYER_X:
                self.perform_agent_move()
            else:
                self.perform_random_move()

            self.state = self.check_game_state()
            self.current_player *= -1
            self.turns_played += 1

        # If we hit the max_turns cap without a winner, declare TIE as a safety fallback.
        # In true Quixo the game continues until a win; this cap prevents infinite loops.
        if self.state == "ONGOING":
            self.state = "TIE"
        return self.state

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

        return "ONGOING"

    # ----------------------
    # Scoring & diagnostics
    # ----------------------
    def score_boards(self):
        """
        Return list of (state_string, discounted_score) where `state_string` is exactly
        what you stored in history (hash_board(..., current_player)). The score is
        the reward from the perspective of the player to move in that state.
        """
        scored_states = []

        def player_from_state_string(state_str):
            # hash_board appends str(current_player) at the end
            if state_str.endswith('-1'):
                return PLAYER_O
            elif state_str.endswith('1'):
                return PLAYER_X
            else:
                return None

        for i, state in enumerate(reversed(self.history)):
            state_player = player_from_state_string(state)

            if self.state == "VICTORY_X":
                final_for_state = self.win_reward if state_player == PLAYER_X else self.lose_reward
            elif self.state == "VICTORY_O":
                final_for_state = self.win_reward if state_player == PLAYER_O else self.lose_reward
            else:  # "TIE"
                final_for_state = self.draw_reward

            score = final_for_state * (self.gamma ** i)
            scored_states.append((state, score))

        return scored_states

    def unknown_ratio(self):
        if self.total_moves == 0:
            return 0.0
        return self.unknown_moves / self.total_moves