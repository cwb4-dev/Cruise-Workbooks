# Blackjack — Python Workbook

> Python • Google IDX • Firebase • iPad  
> *Simulate and analyze Blackjack strategy with data*

---

## What This Is

The Python version of Blackjack is not a playable game — it is a **data science tool**.
You use Monte Carlo simulation to analyze strategies, measure house edge, and
save results to Firebase. The playable game is in `ipad-workbooks-typescript`.

---

## Part 0 — IDX Setup

### Session Startup

1. Open IDX — open `ipad-workbooks-python` repo
2. Open Gemini AI Studio in Edge Tab 2
3. Open Firebase Console in Edge Tab 3
4. Working Copy → Pull
5. In IDX terminal: `cd blackjack`

### Install Dependencies

```bash
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

if not firebase_admin._apps:
    cred = credentials.Certificate('../firebase/service-account.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()
print('Ready!')
```

### Gemini Prompt Template

```
I am writing Python in Google IDX terminal.
Full environment — numpy, matplotlib, pandas, scipy, firebase-admin all installed.
Firebase db client is already initialized.
Give me complete Python code I can save as a .py file and run with python3.
```

---

## Part 1 — Blackjack Rules and Strategy

### The Rules

| Rule | Details |
|---|---|
| Goal | Get closer to 21 than dealer without going over |
| Card values | 2-10 = face value, J/Q/K = 10, Ace = 1 or 11 |
| Blackjack | Ace + any 10-value on first deal |
| Bust | Total over 21 = automatic loss |
| Dealer rule | Dealer hits until total is 17 or higher |

### Strategies to Analyze

| Strategy | Description |
|---|---|
| Always stand | Never hit — take whatever you're dealt |
| Naive | Stand on 15+, hit on 14 or lower |
| Basic | Stand on 17+, hit on 16 or lower (mimics dealer) |
| Aggressive | Stand on 18+, always double on 10 or 11 |
| Perfect basic strategy | Hit/stand based on your total AND dealer's upcard |

---

## Part 2 — Build the Simulator

### Step 2.1 — Ask Gemini for the Core Simulator

```
I am writing Python in Google IDX.
Build a Blackjack simulator with these components:

Classes/functions needed:
  create_deck() -> list  — standard 52-card deck, shuffled
  card_value(card: str) -> int  — 2-10=face, J/Q/K=10, A=11
  hand_value(hand: list) -> int  — total with Ace soft/hard logic
  play_hand(strategy: str, deck: list) -> dict
    strategies: 'always_stand', 'naive', 'basic'
    returns: { result, player_total, dealer_total, player_hand, dealer_hand }

Use a 6-deck shoe. Reshuffle when fewer than 20% of cards remain.
Ace counts as 11 unless that causes bust, then counts as 1.

Give me complete Python code I can save as blackjack_sim.py and run with python3.
```

### Step 2.2 — Run a Quick Test

```bash
python3 blackjack_sim.py
```

Verify the output looks correct — check hand totals and results make sense.

---

## Part 3 — Strategy Comparison

### Step 3.1 — Ask Gemini for the Comparison

```
Using my blackjack_sim.py, write a strategy comparison script that:
- Simulates 100,000 hands for each strategy: 'always_stand', 'naive', 'basic'
- Computes win%, loss%, push%, and house edge for each
- Prints a formatted comparison table
- Plots a bar chart comparing win rates using matplotlib
- Saves all results to Firebase Firestore collection 'blackjack_analysis'
  with fields: strategy, win_rate, loss_rate, push_rate, house_edge,
  n_hands, timestamp
- Uses firebase-admin, db client already initialized

Give me complete Python code to save as strategy_comparison.py.
```

### Run It

```bash
python3 strategy_comparison.py
```

Check Firebase Console > Firestore > `blackjack_analysis` for your results.

---

## Part 4 — Dealer Upcard Analysis

How does the dealer's visible card affect your optimal play?

### Ask Gemini

```
Using my blackjack_sim.py, write an analysis script that:
- For each dealer upcard (2 through Ace):
  Simulates 50,000 hands using basic strategy
  Computes player win rate for that dealer upcard
- Creates a heatmap: player hand total (12-20) vs dealer upcard (2-A)
  showing win probability for each combination
- This is the foundation of basic strategy charts
- Saves results to Firebase collection 'blackjack_analysis'
  Fields: analysis_type='upcard_heatmap', dealer_upcard, player_total,
  win_rate, n_hands, timestamp

Give me complete Python code to save as upcard_analysis.py.
```

---

## Part 5 — Ace Handling Deep Dive

Aces are the most complex part of Blackjack. Prove with data how soft vs hard hands differ.

### Ask Gemini

```
Write a Python analysis of Ace handling in Blackjack:
- Simulate 200,000 hands
- Track: how often a soft hand (Ace=11) was dealt
  how often the Ace had to switch from 11 to 1 to avoid bust
  win rate for hands containing an Ace vs hands without
  win rate for soft 17 (Ace+6) vs hard 17 (e.g. 10+7)
- Plot distribution of outcomes for each scenario
- Save to Firebase collection 'blackjack_analysis'
  Fields: analysis_type='ace_analysis', soft_hand_rate, ace_reduction_rate,
  soft_win_rate, hard_win_rate, timestamp

Give me complete Python code to save as ace_analysis.py.
```

---

## Part 6 — Convergence Study

How many simulations do you need before results stabilize?

### Ask Gemini

```
Write a Python convergence study for Blackjack simulation:
- Run basic strategy simulation with increasing sample sizes:
  100, 500, 1000, 5000, 10000, 50000, 100000, 500000
- For each sample size: compute win rate and 95% confidence interval
- Plot: win rate vs sample size with confidence bands
  showing where the estimate stabilizes
- This demonstrates the Law of Large Numbers applied to card games
- Save to Firebase collection 'blackjack_analysis'
  Fields: analysis_type='convergence', n_hands, win_rate, ci_low, ci_high, timestamp

Give me complete Python code to save as convergence_study.py.
```

---

## Part 7 — Query and Compare Results

### Ask Gemini

```
Write Python that reads all results from Firebase Firestore
collection 'blackjack_analysis' and:
- Groups by analysis_type
- For strategy results: prints a ranked comparison table
- For convergence results: plots the convergence chart
- For upcard analysis: reconstructs and prints the heatmap
- Shows timestamp of each run so you can compare across sessions
db client already initialized. Give me complete Python code.
```

---

## Part 8 — File Structure

```
blackjack/
├── WORKBOOK.md           ← this file
├── blackjack_sim.py      ← core simulator (build first)
├── strategy_comparison.py
├── upcard_analysis.py
├── ace_analysis.py
└── convergence_study.py
```

---

## Git and Wrap Up

```bash
git add .
git commit -m "Blackjack Python analysis complete"
git push
```

---

> *Blackjack • Python • Google IDX • Firebase • iPad*  
> *MSC Meraviglia — Starlink Maritime*
