# Monte Carlo Simulation — Python Workbook

> Python • Google IDX • Firebase • iPad  
> *Background, Theory & 5 Simulations*

---

## Part 0 — IDX Setup

### Session Startup

```bash
cd monte-carlo
pip3 install numpy matplotlib pandas scipy firebase-admin
```

### Standard Imports — Every Script

```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

np.random.seed(42)
plt.style.use('seaborn-v0_8-darkgrid')

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
Firebase db client already initialized. np.random.seed(42) already set.
Give me complete Python code I can save as a .py file and run with python3.
```

---

## Part 1 — What is Monte Carlo? The Origin Story

### Born in the Manhattan Project

In 1946, physicist Stanislaw Ulam was recovering from illness and playing solitaire.
He wondered: what is the probability of winning? The math was too complex to solve directly.
His insight: just play it 100 times and count the wins. He took this idea to John von Neumann,
they formalized it, gave it the code name **Monte Carlo** after the casino in Monaco,
and applied it immediately to neutron diffusion in nuclear weapons research.

**The core idea:** when a problem is too complex for exact math, simulate it randomly
thousands of times and let the Law of Large Numbers give you the answer.

### The Law of Large Numbers

| Simulations | Typical Error | Good Enough For |
|---|---|---|
| 1,000 | ~3% | Quick estimates |
| 10,000 | ~1% | Most practical decisions |
| 100,000 | ~0.3% | Financial and engineering decisions |
| 1,000,000 | ~0.1% | Scientific research |

### The Four Steps

| Step | What You Do |
|---|---|
| 1. Define inputs | Identify what is uncertain |
| 2. Generate randomness | Draw from the right probability distribution |
| 3. Run model | Plug values in, record output |
| 4. Repeat and analyze | Do steps 2-3 thousands of times |

### NumPy Random Quick Reference

```python
np.random.uniform(low, high, n)    # equal probability between bounds
np.random.normal(mean, std, n)     # bell curve
np.random.triangular(min, mode, max, n)  # has a most-likely value
np.random.randint(low, high, n)    # whole numbers
np.random.choice([-1, 1], n)       # random picks from array
np.percentile(results, [5, 50, 95])  # key percentiles
```

---

## Part 2 — Simulation 1: Estimating Pi

### Ask Gemini

```
I am writing Python in Google IDX.
Write a Monte Carlo Pi estimation simulation:
- Throw 1,000,000 random (x,y) points in a 2x2 square [-1,1]
- Count how many land inside the unit circle (x^2 + y^2 <= 1)
- Pi = 4 * (points inside) / total
- Use NumPy vectorization — no Python loops
- Print: estimated Pi, true Pi, error
- Plot 1: dart board — blue dots inside circle, red outside (sample of 10,000)
- Plot 2: convergence chart — Pi estimate vs number of simulations
- Save to Firebase collection 'monte_carlo_runs'
  Fields: simulation_type='pi', n_simulations, pi_estimate, error, timestamp
Give me complete Python code to save as pi_simulation.py.
```

### Run It

```bash
python3 pi_simulation.py
```

> **What to observe:** The estimate bounces wildly at 100 simulations but locks onto 3.14 by 100,000. This is the Law of Large Numbers made visible.

---

## Part 3 — Simulation 2: The Gambler's Ruin

### Ask Gemini

```
I am writing Python in Google IDX.
Write a Monte Carlo Gambler's Ruin simulation:
- A gambler starts with $50. Each flip: +$1 (heads) or -$1 (tails)
- Game ends at $0 (ruin) or $100 (goal)
- Simulate 10,000 games using NumPy vectorization where possible
- Print: probability of ruin, average game length
- Plot 1: 20 sample game paths (red=ruined, blue=won)
- Plot 2: ruin probability table for win rates 50%, 49%, 48%, 45%
- Save to Firebase collection 'monte_carlo_runs'
  Fields: simulation_type='gamblers_ruin', ruin_probability,
  avg_steps, win_probability, start_wealth, goal, timestamp
Give me complete Python code to save as gamblers_ruin.py.
```

> **Key lesson:** Even a 1% house edge (49% win rate) dramatically increases ruin probability. This is why casinos are always profitable.

---

## Part 4 — Simulation 3: Stock Portfolio Risk

### Ask Gemini

```
I am writing Python in Google IDX.
Write a Monte Carlo stock portfolio simulation:
- Starting value $10,000
- Daily returns drawn from normal distribution: mean=0.0004, std=0.012
- Simulate 252 trading days (1 year)
- Run 10,000 simulations using NumPy vectorization (no Python loops)
- Print: mean final value, median, 5th/95th percentiles,
  probability of loss, 95% Value at Risk
- Plot 1: fan chart — 200 sample paths + 5th, 50th, 95th percentile lines
- Plot 2: histogram of final portfolio values
- Save to Firebase collection 'monte_carlo_runs'
  Fields: simulation_type='stock_portfolio', starting_value, mean_final,
  p5, p95, prob_of_loss, var_95, n_simulations, timestamp
Give me complete Python code to save as stock_portfolio.py.
```

---

## Part 5 — Simulation 4: Project Schedule Risk

### Ask Gemini

```
I am writing Python in Google IDX.
Write a Monte Carlo project schedule risk simulation:
Tasks with triangular distributions (optimistic, most-likely, pessimistic days):
  Requirements:  3, 5, 10
  Backend:       8, 14, 25
  Frontend:      6, 10, 18
  Testing:       3, 6, 14
  Deployment:    2, 3, 7
Tasks run sequentially. Total = sum of all task durations.
- Run 100,000 simulations using np.random.triangular()
- Print: naive estimate (sum of most-likely), mean, 70/80/90/95% confidence days
- Plot: histogram with vertical lines for naive and confidence levels
- Save to Firebase collection 'monte_carlo_runs'
  Fields: simulation_type='project_schedule', naive_days, mean_days,
  p70, p80, p90, p95, n_simulations, timestamp
Give me complete Python code to save as project_schedule.py.
```

> **Key lesson:** The naive estimate is almost always 20-30% too optimistic due to uncertainty compounding across tasks. This is why software projects run late.

---

## Part 6 — Simulation 5: Blackjack Strategy Tester

### Ask Gemini

```
I am writing Python in Google IDX.
Write a Monte Carlo Blackjack strategy comparison:
Compare two strategies over 100,000 hands each:
  Strategy A (Naive): stand on 15+, hit on 14 or lower
  Strategy B (Basic): stand on 17+, hit on 16 or lower
Use a 6-deck shoe. Ace=11 unless bust then 1.
- Print: win%, loss%, push%, house edge for each strategy
- Plot: bar chart comparing win rates
- Save both to Firebase collection 'monte_carlo_runs'
  Fields: simulation_type='blackjack_strategy', strategy_name,
  win_rate, loss_rate, push_rate, house_edge, n_hands, timestamp
Give me complete Python code to save as blackjack_strategy.py.
```

---

## Part 7 — Query All Results

### Ask Gemini

```
Write Python that reads all results from Firebase Firestore
collection 'monte_carlo_runs' and:
- Prints a summary table grouped by simulation_type
- For stock_portfolio: shows how mean_final varied across runs
- For blackjack_strategy: ranks strategies by win rate
- Shows count of runs per simulation type
- Shows timestamps so you can compare runs across sessions
db client already initialized. Give me complete Python code.
```

---

## File Structure

```
monte-carlo/
├── WORKBOOK.md
├── pi_simulation.py
├── gamblers_ruin.py
├── stock_portfolio.py
├── project_schedule.py
└── blackjack_strategy.py
```

---

## Git and Wrap Up

```bash
git add .
git commit -m "Monte Carlo simulations complete"
git push
```

---

> *Monte Carlo • Python • Google IDX • Firebase • iPad*  
> *MSC Meraviglia — Starlink Maritime*
