# Usage Guide - Quixo AI Project

## Quick Start

### 1. Install Dependencies
```bash
pip install numpy
```

### 2. Run a Demo (Fast Test)
```bash
python demo.py
```
This demonstrates all three stages with smaller numbers (takes ~1 minute).

### 3. Run Individual Stages

#### Stage א - Basic Game
```bash
python main.py a
```
- Runs 1 verbose game to see gameplay
- Runs 100-game tournament
- Shows statistics

#### Stage ב - Generate Training Data
```bash
python main.py b
```
- Runs 100,000 random vs random games
- Generates `states_random.json`
- Takes ~5-15 minutes depending on your computer
- Shows progress every 1000 games

#### Stage ג - Greedy Agent
```bash
python main.py c
```
**Prerequisites:** Must run Stage ב first!
- Tests greedy agent with 1000 games
- Generates 100,000 greedy vs random games
- Creates `states_greedy.json`
- Takes ~5-15 minutes

### 4. Run Everything at Once
```bash
python main.py
```
This runs all three stages sequentially (takes ~15-30 minutes total).

## Output Files

### states_random.json
Board states from 100,000 random vs random games.

Format:
```json
{
  "                         ": [0.022789292043800397, 100000],
  "                        X": [0.024911113142920573, 6373],
  "X                        ": [0.0315, 8245]
}
```
- Key: 25-character board string (space=empty, X=X piece, O=O piece)
- Value: [average_score, occurrence_count]

### states_greedy.json
Board states from 100,000 greedy vs random games.
Same format as `states_random.json`.

## Understanding the Board Format

Each board is stored as a 25-character string representing the 5x5 grid read left-to-right, top-to-bottom:

```
  0 1 2 3 4
0 . . . . .     →  "                         "  (all empty)
1 . . . . .
2 . . . . .
3 . . . . .
4 . . . . .

  0 1 2 3 4
0 . . . . .     →  "                        X"  (X at position 4,4)
1 . . . . .
2 . . . . .
3 . . . . .
4 . . . . X

  0 1 2 3 4
0 X O . . .     →  "XO       X   O          "
1 . . . . .
2 X . . . O
3 . . . . .
4 . . . . .
```

## Performance Expectations

### Random Agent
- Win rate: ~50% (50/50 against another random agent)
- This is your baseline

### Greedy Agent  
- Win rate: 55-65% against random agent
- Improvement shows the AI is learning from experience
- Better training data (more games) → better performance

## Customization

You can adjust parameters in [game.py](game.py):

```python
game = Game(
    play_mode='GREEDY',       # 'RANDOM' or 'GREEDY'
    output_mode='VERBOSE',     # 'SILENT' or 'VERBOSE'
    epsilon=0.1,               # Exploration rate (0.0-1.0)
    discount_factor=0.85,      # Reward discounting (0.0-1.0)
    unknown_score=0.5          # Score for unseen states
)
```

## Troubleshooting

### Error: "states_random.json not found"
Run Stage ב first:
```bash
python main.py b
```

### Greedy agent not performing better
- Need more training data (increase games in Stage ב)
- Check epsilon value (0.1 is good, 1.0 is fully random)
- Verify greedy_dict is loaded correctly

### Games are too slow
- Running 100,000 games is normal to take several minutes
- For quick testing, use `demo.py` or modify num_games in main.py

## Testing

Quick validation tests:

```bash
python test_basic.py    # Basic functionality (10 games, ~5 seconds)
python test_states.py   # State collection (100 games, ~30 seconds)
python test_greedy.py   # Greedy agent (100 games, ~30 seconds)
```

## Expected Runtime

On a typical modern computer:
- Single game: <1 second
- 100 games: ~5-10 seconds
- 1,000 games: ~30-60 seconds
- 100,000 games: ~5-15 minutes

## Next Steps

After completing stages א-ג:
1. Analyze the board state statistics
2. Experiment with different parameters (epsilon, discount_factor)
3. Compare random vs greedy performance
4. Consider implementing more sophisticated AI (Q-learning, neural networks)

## Support

Check these files for implementation details:
- [game.py](game.py) - Game logic and agents
- [tournament.py](tournament.py) - Tournament runner
- [main.py](main.py) - Main execution script
- [README.md](README.md) - Project overview
