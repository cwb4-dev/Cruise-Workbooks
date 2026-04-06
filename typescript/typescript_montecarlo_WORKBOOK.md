# Monte Carlo Simulation — WORKBOOK

> TypeScript • Google IDX • Firebase • iPad  
> *Background, Theory & 5 Interactive Simulations*

---

## Part 0 — Your IDX Workflow

See the main `README.md` for the full startup sequence and toolchain.

### Gemini Prompt Template for This Project

```
I am building a Monte Carlo simulation in vanilla TypeScript in Google IDX.
Full Node.js environment with CLI access.
Use Firebase Web SDK v9 modular imports.
Give me complete index.html, main.ts, and style.css.
Include all imports at the top of each file.
```

---

## Part 1 — What is Monte Carlo? The Origin Story

### 1.1 Born in the Manhattan Project

In 1946, physicist Stanislaw Ulam was recovering from illness and playing solitaire.
He wondered: what is the probability of winning? The math was too complex to solve directly.
His insight: just play it 100 times and count the wins. He took this idea to John von Neumann,
they formalized it, gave it the code name **Monte Carlo** after the casino in Monaco,
and immediately applied it to neutron diffusion in nuclear weapons research.

**The core idea:** when a problem is too complex for exact math, simulate it randomly
thousands of times and let the Law of Large Numbers give you the answer.

### 1.2 The Law of Large Numbers

| Simulations | Typical Error | Good Enough For |
|---|---|---|
| 1,000 | ~3% | Quick estimates |
| 10,000 | ~1% | Most practical decisions |
| 100,000 | ~0.3% | Financial and engineering decisions |
| 1,000,000 | ~0.1% | Scientific research |

### 1.3 The Four Steps — Every Simulation

| Step | What You Do |
|---|---|
| 1. Define inputs | Identify what is uncertain — what values randomly vary? |
| 2. Generate randomness | Draw random values from the right probability distribution |
| 3. Run model | Plug values into formula, record the output |
| 4. Repeat and analyze | Do steps 2-3 thousands of times. Compute mean, percentiles. |

### 1.4 TypeScript Random Distribution Helpers

Ask Gemini to include these in every simulation project:

```typescript
function randomUniform(min: number, max: number): number {
  return min + Math.random() * (max - min);
}

function randomNormal(mean: number, std: number): number {
  // Box-Muller transform
  const u1 = Math.random(), u2 = Math.random();
  return mean + std * Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
}

function randomTriangular(min: number, mode: number, max: number): number {
  const u = Math.random();
  const fc = (mode - min) / (max - min);
  return u < fc
    ? min + Math.sqrt(u * (max - min) * (mode - min))
    : max - Math.sqrt((1 - u) * (max - min) * (max - mode));
}

function percentile(arr: number[], p: number): number {
  const sorted = [...arr].sort((a, b) => a - b);
  return sorted[Math.floor((p / 100) * sorted.length)];
}
```

---

## Part 2 — IDX Project Setup

```bash
cd monte-carlo
npm init -y
npm install firebase
npm install -g typescript
```

---

## Part 3 — Simulation 1: Estimating Pi

The classic Monte Carlo introduction. Throw random darts, count how many land inside a circle.

**The logic:** throw random (x,y) points in a 2x2 square [-1,1].
Points inside the unit circle satisfy `x² + y² ≤ 1`.
`Pi = 4 × (points inside) / (total points)`.

### Ask Gemini

```
I am building a Monte Carlo Pi estimation simulation in vanilla TypeScript in Google IDX.
Logic: throw random (x,y) points in a 2x2 square [-1,1].
Count how many land inside the unit circle (x^2 + y^2 <= 1).
Pi = 4 * (points inside) / total points.

TypeScript interface: SimResult { piEstimate: number, truePI: number, error: number, nSimulations: number }

Requirements:
- Run up to 1,000,000 simulations in batches to keep UI responsive
- Draw the dart board on Canvas: blue dots inside circle, red outside
- Draw convergence chart: Pi estimate vs simulation count on a second canvas
- Show live updating estimate as simulations run with a Start/Stop button
- Save final result to Firebase collection 'monte_carlo_runs'
  Fields: simulationType='pi', nSimulations, piEstimate, error, timestamp
- Here is my Firebase config: [paste firebaseConfig]

Give me complete index.html, main.ts, style.css for IDX.
```

> **What to observe:** Watch the Pi estimate stabilize as simulations increase. At 100 it bounces around. At 100,000 it locks onto 3.14. This is the Law of Large Numbers made visible.

---

## Part 4 — Simulation 2: The Gambler's Ruin

Models a gambler betting $1 per coin flip. Teaches random walks, ruin probability, and house edge — directly relevant to your Blackjack app.

**Setup:** Start with $50. Each flip: +$1 (heads) or -$1 (tails). Stop at $0 (ruin) or $100 (goal).

### Ask Gemini

```
I am building a Gambler's Ruin simulation in vanilla TypeScript in Google IDX.
A gambler starts with $50. Each flip: +$1 heads or -$1 tails. Stops at $0 or $100.

TypeScript interfaces:
  GameParams { startWealth: number, goal: number, winProbability: number, nGames: number }
  GameResult { ruined: boolean, steps: number, finalWealth: number }

Requirements:
- Simulate 10,000 games and compute ruin probability and average game length
- Draw 20 sample game paths on Canvas (red=ruined, blue=won)
- Show ruin probability table for win rates: 50%, 49%, 48%, 45%
- Sliders to adjust starting wealth, goal, and win probability — reruns simulation
- Save to Firebase collection 'monte_carlo_runs'
  Fields: simulationType='gamblers_ruin', ruinProbability, avgSteps, winProbability, timestamp
- Here is my Firebase config: [paste firebaseConfig]

Give me complete index.html, main.ts, style.css for IDX.
```

> **Key lesson:** Even a 1% house edge (49% win rate) dramatically increases ruin probability. Monte Carlo proves it concretely — and explains why casinos are always profitable.

---

## Part 5 — Simulation 3: Stock Portfolio Risk

One of the most widely used Monte Carlo applications in finance. Simulates 10,000 possible futures for a portfolio.

### Ask Gemini

```
I am building a stock portfolio Monte Carlo simulation in vanilla TypeScript in Google IDX.
Model: starting value $10,000. Each day draw a return from normal distribution
with mean 0.0004 (~10% annual) and std 0.012 (~19% annual).
Simulate 252 trading days (1 year).

TypeScript interfaces:
  PortfolioParams { startValue: number, dailyMean: number, dailyStd: number, tradingDays: number, nSimulations: number }
  RiskMetrics { mean: number, median: number, p5: number, p95: number, probOfLoss: number, var95: number }

Requirements:
- Run 10,000 simulations
- Draw fan chart on Canvas: 200 sample paths + 5th, 50th, 95th percentile lines
- Draw histogram of final portfolio values
- Display: mean, median, 5th/95th percentiles, probability of loss, 95% VaR
- Input fields for parameters with re-run button
- Save to Firebase collection 'monte_carlo_runs'
  Fields: simulationType='stock_portfolio', startValue, mean, p5, p95, probOfLoss, var95, timestamp
- Here is my Firebase config: [paste firebaseConfig]

Give me complete index.html, main.ts, style.css for IDX.
```

---

## Part 6 — Simulation 4: Project Schedule Risk

Directly useful for real work. Shows why projects run late and gives honest probability-based completion estimates.

### Ask Gemini

```
I am building a project schedule Monte Carlo simulation in vanilla TypeScript in Google IDX.
Use these 5 tasks with triangular distributions (optimistic, most-likely, pessimistic days):
  Requirements:  3, 5, 10
  Backend:       8, 14, 25
  Frontend:      6, 10, 18
  Testing:       3, 6, 14
  Deployment:    2, 3, 7
Tasks run sequentially. Total = sum of all task durations.

TypeScript interfaces:
  Task { name: string, optimistic: number, likely: number, pessimistic: number }
  ScheduleSummary { naiveDays: number, mean: number, p70: number, p80: number, p90: number, p95: number }

Requirements:
- Run 100,000 simulations using randomTriangular() helper
- Draw histogram with vertical lines for naive estimate and confidence levels
- Show: naive estimate (sum of most-likely), mean, 70/80/90/95% confidence days
- Editable task table — change durations and re-run instantly
- Save to Firebase collection 'monte_carlo_runs'
  Fields: simulationType='project_schedule', naiveDays, mean, p80, p90, p95, timestamp
- Here is my Firebase config: [paste firebaseConfig]

Give me complete index.html, main.ts, style.css for IDX.
```

> **Key lesson:** The naive estimate (sum of most-likely values) is almost always 20-30% too optimistic. This is why software projects run late.

---

## Part 7 — Simulation 5: Blackjack Strategy Tester

Ties back to your Blackjack project — prove which strategy is better with data before building the full game.

### Ask Gemini

```
I am building a Blackjack strategy Monte Carlo tester in vanilla TypeScript in Google IDX.
Compare two strategies over 100,000 hands each:
  Strategy A (Naive): Stand on 15+, hit on 14 or lower
  Strategy B (Basic): Stand on 17+, hit on 16 or lower
Use a 6-deck shoe. Ace counts as 11 unless bust then 1.

TypeScript interfaces:
  StrategyResult { name: string, winRate: number, lossRate: number, pushRate: number, houseEdge: number, nHands: number }

Requirements:
- Simulate 100,000 hands per strategy
- Display results table: win%, loss%, push%, house edge per strategy
- Draw bar chart comparing win rates on Canvas
- Progress bar while simulating (run in batches to keep UI responsive)
- Save both results to Firebase collection 'monte_carlo_runs'
  Fields: simulationType='blackjack_strategy', strategyName, winRate, lossRate, houseEdge, nHands, timestamp
- Here is my Firebase config: [paste firebaseConfig]

Give me complete index.html, main.ts, style.css for IDX.
```

---

## Part 8 — Query All Results from Firebase

### Ask Gemini

```
Build a Monte Carlo results dashboard in vanilla TypeScript in Google IDX.
Read all documents from Firebase Firestore collection 'monte_carlo_runs' and display:
- Summary table: simulation type, key metric, timestamp — newest first
- Group by simulationType with count per type
- Filter buttons to show only one simulation type at a time
- For stock_portfolio results: line chart of mean final value over time
Use Firebase Web SDK v9. Here is my firebaseConfig: [paste]
Give me complete index.html, main.ts, style.css for IDX.
```

---

## Part 9 — Git and Wrap Up

```bash
git add .
git commit -m "Monte Carlo simulations complete with Firebase"
git push
```

---

> *Monte Carlo • TypeScript • Google IDX • Firebase • iPad*  
> *MSC Meraviglia — Starlink Maritime*
