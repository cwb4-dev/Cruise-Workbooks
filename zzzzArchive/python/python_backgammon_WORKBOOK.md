# Backgammon — Python Workbook

> Python • Google IDX • Firebase • iPad  
> *Analyze backgammon probabilities and strategy with data*

---

## What This Is

The Python version of Backgammon is a **probability and strategy analysis tool**.
You simulate dice distributions, hit probabilities, and bearing-off scenarios.
The playable game is in `ipad-workbooks-typescript`.

---

## Part 0 — IDX Setup

### Session Startup

```bash
cd backgammon
pip3 install numpy matplotlib pandas scipy firebase-admin
```

### Firebase Connection

```python
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from itertools import product

if not firebase_admin._apps:
    cred = credentials.Certificate('../firebase/service-account.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()
print('Ready!')
```

### Gemini Prompt Template

```
I am writing Python in Google IDX terminal.
numpy, matplotlib, pandas, scipy, firebase-admin all installed.
Firebase db client already initialized.
Give me complete Python code to save as a .py file and run with python3.
```

---

## Part 1 — Backgammon Probability Foundations

### The Rules Reminder

| Rule | Details |
|---|---|
| Board | 24 points, numbered 1-24. Bar in center. |
| Direction | White moves 24→1. Black moves 1→24. |
| Doubles | Same number on both dice = 4 moves of that value |
| Blot | Single checker — vulnerable to being hit |
| Block | 2+ same-color checkers — opponent cannot land |
| Bar | Hit checkers must re-enter before other moves |

### Key Probabilities to Know

| Scenario | Exact Probability | Notes |
|---|---|---|
| Rolling doubles | 1/6 = 16.7% | Any pair |
| Hitting a blot 1 away | 11/36 = 30.6% | Any combo reaching that point |
| Hitting a blot 7 away | 6/36 = 16.7% | Only doubles help |
| Rolling a specific number | 11/36 = 30.6% | That number on either die |

---

## Part 2 — Dice Probability Analysis

### Step 2.1 — Ask Gemini for the Dice Analyzer

```
I am writing Python in Google IDX.
Write a comprehensive backgammon dice probability analyzer:

1. Generate all 36 possible dice combinations (1,1) through (6,6)
2. For each combination compute: total pips, moves available (4 if doubles, 2 if not)
3. Compute probability of reaching each point (1-24) from point 0
   assuming no blockers
4. Create a hitting probability table:
   For each distance (1-24), what is P(being hit this turn)?
5. Plot: hitting probability vs distance as a bar chart
6. Save results to Firebase collection 'backgammon_analysis'
   Fields: analysis_type='dice_probabilities', distance, hit_probability, timestamp

Give me complete Python code to save as dice_analysis.py and run with python3.
```

### Run It

```bash
python3 dice_analysis.py
```

---

## Part 3 — Blot Vulnerability Analysis

When is a lone checker (blot) safe vs dangerous?

### Ask Gemini

```
Write Python to analyze backgammon blot safety:
- For each point distance 1-24, compute P(opponent hits this turn)
  assuming opponent has checkers that could potentially hit
- Account for blocking: if there are 2+ of our checkers between
  the opponent and the blot, those intermediate points block movement
- Simulate 1,000,000 random dice rolls
- Create a safety heatmap: distance vs number of blockers vs hit probability
- Identify the 'danger zones' — distances with highest hit probability
- Plot results clearly with matplotlib
- Save to Firebase collection 'backgammon_analysis'
  Fields: analysis_type='blot_safety', distance, n_blockers,
  hit_probability, n_simulations, timestamp

Give me complete Python code to save as blot_analysis.py.
```

---

## Part 4 — Bearing Off Probability

When can you bear off and how fast?

### Ask Gemini

```
Write Python to analyze backgammon bearing off:
- Simulate bearing off from various positions:
  All 15 checkers on the 6-point (best case)
  Checkers spread evenly across points 1-6
  Worst case: 5 checkers on point 6, rest stacked high
- For each position, simulate 100,000 games and measure:
  Average number of turns to bear off all 15
  Distribution of turns (min, max, percentiles)
  Probability of bearing off in exactly N turns
- Plot: distribution of turns for each starting position
- Save to Firebase collection 'backgammon_analysis'
  Fields: analysis_type='bearing_off', position_name,
  mean_turns, p25, p75, p90, n_simulations, timestamp

Give me complete Python code to save as bearing_off_analysis.py.
```

---

## Part 5 — Pip Count Analysis

The pip count is the total distance all your checkers must travel. Lower is better.

### Ask Gemini

```
Write Python to analyze backgammon pip counts:
- Compute pip count for the standard opening position
  White: 2 on 24, 5 on 13, 3 on 8, 5 on 6
  Black: mirror of White
- Simulate 10,000 random games (random legal moves each turn)
- Track pip count for both players each turn
- Plot: pip count over game turns for both players
  showing how the gap between players evolves
- Identify: average game length in turns, average pip count at game end
- Save to Firebase collection 'backgammon_analysis'
  Fields: analysis_type='pip_count', avg_game_length,
  opening_pip_count_white, opening_pip_count_black, timestamp

Give me complete Python code to save as pip_analysis.py.
```

---

## Part 6 — Opening Move Analysis

Which opening moves give the best position?

### Ask Gemini

```
Write Python to analyze backgammon opening moves:
- For each of the 21 possible opening rolls (1-2, 1-3, ... 5-6, plus doubles):
  Enumerate the top 2-3 standard opening responses
  Simulate 50,000 games from each opening position using random play
  Measure: win rate, average pip count after opening
- Rank openings by resulting win rate
- Print a table: roll | best move | win rate | avg pip advantage
- Plot: bar chart of win rates by opening roll
- Save to Firebase collection 'backgammon_analysis'
  Fields: analysis_type='opening_moves', roll, best_move,
  win_rate, pip_advantage, n_simulations, timestamp

Give me complete Python code to save as opening_analysis.py.
```

---

## Part 7 — Monte Carlo Game Simulator

Full game simulation to measure strategy effectiveness.

### Ask Gemini

```
Write Python to simulate complete backgammon games:
- Implement a complete backgammon game engine:
  Legal move generation respecting all rules (Bar, blocking, bearing off)
  Two strategy options: 'random' (pick random legal move) and
  'greedy' (maximize pip count reduction each turn)
- Simulate 10,000 games: random vs random, greedy vs random, greedy vs greedy
- Measure: win rate, game length, gammon rate, backgammon rate
- Plot: win rate comparison bar chart
- Save to Firebase collection 'backgammon_analysis'
  Fields: analysis_type='strategy_comparison', white_strategy, black_strategy,
  white_win_rate, gammon_rate, avg_game_length, n_games, timestamp

Give me complete Python code to save as game_simulator.py.
```

---

## Part 8 — Query Results

### Ask Gemini

```
Write Python that reads all results from Firebase Firestore
collection 'backgammon_analysis' and:
- Groups by analysis_type with count of runs per type
- For dice_probabilities: prints hitting probability table
- For blot_safety: prints danger zone summary
- For bearing_off: compares average turns across positions
- For strategy_comparison: prints win rate rankings
db client already initialized. Give me complete Python code.
```

---

## File Structure

```
backgammon/
├── WORKBOOK.md
├── dice_analysis.py
├── blot_analysis.py
├── bearing_off_analysis.py
├── pip_analysis.py
├── opening_analysis.py
└── game_simulator.py
```

---

## Git and Wrap Up

```bash
git add .
git commit -m "Backgammon Python analysis complete"
git push
```

---

> *Backgammon • Python • Google IDX • Firebase • iPad*  
> *MSC Meraviglia — Starlink Maritime*
