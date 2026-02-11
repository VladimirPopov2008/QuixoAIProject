# Quick Reference Card - Quixo AI Project

## 🎯 Project Complete - All Stages (א-ג) Implemented

### 📁 Main Files
```
game.py         - Game logic and AI agents
tournament.py   - Tournament runner
main.py         - Main execution script
```

### ⚡ Quick Commands

```bash
# Quick demo (1 minute)
python demo.py

# Run specific stage
python main.py a    # שלב א: Basic game
python main.py b    # שלב ב: Generate training data (10 min)
python main.py c    # שלב ג: Greedy agent (10 min)

# Run everything
python main.py

# Quick tests
python test_basic.py      # Basic functionality
python test_states.py     # Board state collection
python test_greedy.py     # Greedy agent test
python explain_format.py  # Format demonstration
```

### 📊 Board Format

Boards stored as 25-character strings:
```
  0 1 2 3 4         String format:
0 . . . . .   →    "                         "
1 . . . . .
2 . . . . .        (space=empty, X=X, O=O)
3 . . . . .
4 . . . . .

JSON format:
"                         ": [avg_score, count]
```

### 🎮 Game Rules (Quixo)

- 5x5 board, players X and O
- Take piece from edge (blank or yours)
- Push back from perpendicular edge
- Win: 5 in a row (↔, ↕, ⤡, ⤢)
- **No ties!**

### 🤖 AI Agents

**Random Agent**
- Chooses random valid move
- ~50% win rate baseline

**Greedy Agent**
- Uses learned board values
- Epsilon-greedy (ε=0.1)
- 90% best move, 10% random
- 55-65% win rate

### 📈 Expected Performance

| Agent | Win Rate |
|-------|----------|
| Random | ~50% |
| Greedy (100k training) | 55-65% |

### ⚙️ Key Parameters

```python
epsilon = 0.1            # Exploration rate
discount_factor = 0.85   # Reward discount (γ)
win_score = 1.0          # Win value
loss_score = 0.0         # Loss value
unknown_score = 0.5      # Unknown state value
```

### 📚 Documentation

- `README.md` - Full project docs
- `USAGE.md` - Detailed usage guide
- `PROJECT_SUMMARY.md` - Implementation summary
- `QUICK_REFERENCE.md` - This file

### ✅ Implementation Checklist

- [x] שלב א: Game & Tournament classes
- [x] שלב ב: 100k games, board scoring, JSON export
- [x] שלב ג: Greedy agent, epsilon-greedy, performance
- [x] Board format as requested
- [x] No tie condition
- [x] Real Quixo rules
- [x] All tests passing

### 🚀 Output Files

After full run:
- `states_random.json` - 100k random games
- `states_greedy.json` - 100k greedy games

### 💡 Tips

- Use `demo.py` for quick validation
- Stage ב must run before stage ג
- Full runs take 5-15 minutes each
- Progress shown every 1000 games

### 🎓 Project Structure

```
שלב א (Stage A)
├── Game class
│   ├── Board state
│   ├── Random moves
│   └── Win checking
└── Tournament class
    └── Statistics

שלב ב (Stage B)
├── Board tracking
├── Discounted scoring
├── Dictionary: board → [score, count]
└── JSON export

שלב ג (Stage C)
├── Greedy agent
├── Epsilon-greedy strategy
├── Performance validation
└── Greedy training data
```

### 📞 Support

All code is documented and tested.
See documentation files for details.

---
**Status**: ✅ Complete and Working
**Last Updated**: February 2026
