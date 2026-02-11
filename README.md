# Quixo AI Project

A Python implementation of the Quixo board game with AI agents using reinforcement learning principles.

## Game Rules

Quixo is a 5x5 board game where:
- Players (X and O) take turns moving pieces
- You can only take a piece from the edge that is blank or marked with your symbol
- After taking a piece, you push it back into the board from a perpendicular edge
- Win by getting 5 in a row (horizontal, vertical, or diagonal)
- **No ties** - the game continues until someone wins

## Project Structure

```
game.py         - Game logic, board state, and agent strategies
tournament.py   - Tournament runner and statistics collection
main.py         - Main execution script
test_*.py       - Test scripts for validation
states_random.json  - Board states from random agent games
states_greedy.json  - Board states from greedy agent games
```

## Implementation Stages

### שלב א' (Stage A): Basic Game
- Implemented `Game` class with:
  - 5x5 board representation
  - Random agent moves
  - Win condition checking
  - Game loop and state management
- Implemented `Tournament` class for running multiple games
- Statistics tracking (X wins, O wins)

### שלב ב' (Stage B): Data Collection
- Collect board states from 100,000 random vs random games
- Score each board state using discounted rewards:
  - Final state: 1.0 for win, 0.0 for loss
  - Earlier states: discounted by factor γ^(N-1-i) where γ=0.85
- Store in dictionary format: `{"board_state": [avg_score, count]}`
- Save to `states_random.json`

### שלב ג' (Stage C): Greedy Agent
- Implemented epsilon-greedy strategy (ε=0.1)
  - 90% exploitation: choose highest-value move from dictionary
  - 10% exploration: random move
- Unknown board states scored as 0.5 (uncertainty)
- Performance validation:
  - Greedy agent should outperform random agent (>50% win rate)
- Generate new training data with 100,000 greedy games
- Save to `states_greedy.json`

## Usage

### Run all stages:
```bash
python main.py
```

### Run specific stage:
```bash
python main.py a    # Stage א only
python main.py b    # Stage ב only (generates states_random.json)
python main.py c    # Stage ג only (requires states_random.json)
```

### Quick tests:
```bash
python test_basic.py    # Test basic game functionality
python test_states.py   # Test board state collection (100 games)
python test_greedy.py   # Test greedy agent performance
```

## Board State Format

Boards are stored as 25-character strings:
- Space ` ` = empty cell
- `X` = X player
- `O` = O player

Example:
```json
"                         ": [0.022789292043800397, 100000],
"                        X": [0.024911113142920573, 6373]
```

## Configuration Parameters

You can adjust these in the `Game` class:
- `epsilon`: Exploration rate for greedy agent (default: 0.1)
- `discount_factor`: Reward discounting γ (default: 0.85)
- `win_score`: Score for winning state (default: 1.0)
- `loss_score`: Score for losing state (default: 0.0)
- `unknown_score`: Score for unseen states (default: 0.5)

## Expected Performance

- **Random vs Random**: ~50% win rate for each player
- **Greedy vs Random**: >50% win rate for greedy agent (typically 55-65%)
- **Training Data**: 100,000 games generate ~30,000-50,000 unique board states

## Requirements

```bash
pip install numpy
```

## Project Requirements (Hebrew)

This project implements stages א-ג of the AI project requirements:
1. ✅ Game implementation with random agents
2. ✅ Board state collection and scoring system
3. ✅ Greedy agent using learned board values

## Notes

- The game has no tie condition (as per real Quixo rules)
- All board states are tracked during gameplay for learning
- The greedy agent learns from historical game outcomes
- Board dictionary stores average scores and occurrence counts for statistical reliability
