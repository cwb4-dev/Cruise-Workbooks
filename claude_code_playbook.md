# 🚢 Atlantic Data Lab -- Claude Code Playbook

**Guiding Principle:** Prompts only. Claude Code builds, runs, and fixes everything.  
**Toolchain:** GitHub Codespaces · Claude Code · GitHub · Working Copy

-----

## The Big Picture

```
GitHub Codespaces (Edge tab)
└── Claude Code terminal
    ├── Writes your code
    ├── Runs and tests it
    ├── Fixes errors automatically
    └── Saves to GitHub

Working Copy (iPad app)
└── Pulls your code for offline reading
```

**That’s it. Two tools. No Firebase. No Gemini. No IDX.**

-----

## Part 0 -- One-Time Setup

### 0.1 Launch Codespaces

1. Open Edge on your iPad
1. Go to [github.com](https://github.com) → your `Cruise-Workbook-2026` repo
1. Tap the green **Code** button → **Codespaces** tab → **Create codespace on main**
1. Wait about 30 seconds -- a full VS Code editor opens in your browser
1. At the bottom tap **Terminal** → you have a real Linux command line

> **Next time:** Go to [codespaces.github.com](https://codespaces.github.com) to reopen your existing codespace -- don’t create a new one each time or you’ll use up your free hours.

### 0.2 Install Claude Code

In the Codespaces terminal, paste:

```bash
npm install -g @anthropic-ai/claude-code
```

Verify it worked:

```bash
claude --version
```

### 0.3 Authenticate Claude Code

```bash
claude
```

Claude Code will give you a URL -- tap it, log in with your Anthropic account, paste the key back. You’re in.

> **Free tier:** Anthropic’s free plan covers plenty of usage for building all 8 apps.

### 0.4 Set Up Your Folder Structure

Still inside Claude Code, paste this prompt:

```
Create this folder structure in the current directory:
/Essentials
/Analytics
/Lab

Then create an empty README.md in each folder with just the folder name as a heading.
Confirm when done.
```

-----

## Part 1 -- How Claude Code Works

### Starting a Session

```bash
claude
```

You see a `>` prompt. Type your instruction. Press Enter. Claude Code does the work -- writes files, runs them, reads errors, fixes them.

### Ending a Session

```
/exit
```

### Key Commands

|Command  |What It Does                             |
|---------|-----------------------------------------|
|`/clear` |Fresh start -- clears conversation history|
|`/undo`  |Reverses the last file change            |
|`/status`|Shows what files have changed            |
|`/exit`  |Closes Claude Code                       |

### The Prompt Formula

```
Create [filename] in [folder].
It should [what it does].
Test it with [specific test case].
Expected result: [what you should see].
Fix any errors automatically and confirm when working.
```

-----

## Part 2 -- The 8 Apps

### App 1 -- Weather Advisor

**File:** `/Essentials/weather.py`  
**What it does:** Fetches live temperature for any city. Recommends Lido Deck or Library.

**Claude Code prompt:**

```
Create weather.py in the Essentials folder.

The script should:
1. Ask the user to type a city name
2. Fetch current temperature and weather condition from the Open-Meteo 
   geocoding and forecast APIs -- no API key needed
3. Print temperature in both Celsius and Fahrenheit
4. Print a recommendation:
   - Temp above 22C and no rain → "🌞 Lido Deck recommended"
   - Temp below 18C or rainy → "📚 Library recommended"  
   - Otherwise → "☁️ Either works today"

Test case: Run it with the city Nassau.
Expected: Temperature prints, recommendation prints, no errors.
Fix any errors automatically and confirm when working.
```

**Verify it works:**

```
Run Essentials/weather.py with the city London.
It should show a cooler temperature and recommend the Library.
```

-----

### App 2 -- Utility Kit

**File:** `/Essentials/utils.py`  
**What it does:** Password generator + USD/Euro converter in one menu-driven script.

**Claude Code prompt:**

```
Create utils.py in the Essentials folder.

The script should show a repeating menu:
  1. Generate password
  2. Currency converter
  3. Exit

Option 1: Ask for length (default 16). Generate a random password 
using letters, numbers, and symbols. Print it.

Option 2: Ask direction (USD→EUR or EUR→USD). Use rate 1 USD = 0.92 EUR.
Ask for amount. Print converted value.

Loop until user picks Exit.

Test case 1: Generate a password of length 12.
Expected: 12-character string with mixed characters, no errors.

Test case 2: Convert 100 USD to EUR.
Expected: 92.00 EUR.

Fix any errors and confirm both tests pass.
```

-----

### App 3 -- Activity Logger

**File:** `/Essentials/logger.py`  
**What it does:** Logs daily entries with timestamps. Bayesian mood predictor based on word patterns.

**Claude Code prompt:**

```
Create logger.py in the Essentials folder.

The script should:
1. Ask the user to type a log entry
2. Append the entry with a timestamp to log.txt in the same folder
3. Read all past entries from log.txt
4. Count positive words (great, good, amazing, wonderful, excellent)
   and negative words (bad, terrible, awful, rough, hard)
5. Calculate mood probability using Bayesian update:
   - Prior: 0.5
   - If positive words found: multiply by 0.8, normalize
   - If negative words found: multiply by 0.2, normalize
6. Print: "Mood estimate: X% positive"
7. Print: "Entry saved. Total entries: N"

Use only Python standard library. No external packages.

Test case 1: Run with entry "Great Day Amazing Cruise".
Expected: Mood estimate above 70%, entry saved to log.txt.

Test case 2: Run again with entry "Rough seas bad weather".
Expected: Mood estimate drops below 50%.

Test case 3: Run a third time and verify total entry count is 3.

Fix any errors and confirm all three tests pass.
```

-----

### App 4 -- Basic Blackjack

**File:** `/Essentials/bj_simple.py`  
**What it does:** Monte Carlo simulation of bust probability for any starting hand.

**Claude Code prompt:**

```
Create bj_simple.py in the Essentials folder.

The script should:
1. Ask the user for a starting hand total (e.g. 16)
2. Run 1,000 Monte Carlo trials
3. Each trial: draw one random card from a standard deck
   (2-10 face value, J/Q/K = 10, Ace = 1 or 11 whichever avoids bust)
4. Count trials where total exceeds 21 (bust)
5. Print bust percentage

Use only Python standard library.

Test case 1: Hand of 16.
Expected: Bust percentage between 55% and 70%.

Test case 2: Hand of 11.
Expected: Bust percentage of exactly 0% (impossible to bust on one hit).

Test case 3: Hand of 20.
Expected: Bust percentage above 90%.

Fix any errors and confirm all three tests pass.
```

-----

### App 5 -- Pro Blackjack

**File:** `/Analytics/bj_pro.py`  
**What it does:** Strategy comparison + dealer upcard heatmap.

**Claude Code prompt:**

```
Create bj_pro.py in the Analytics folder.

The script should:
1. Run 10,000 Monte Carlo simulations of blackjack hands
2. Compare two strategies for a player hand of 16:
   - Strategy A: Always stand
   - Strategy B: Always hit
3. Simulate dealer play (dealer hits on soft 17, stands on 17+)
4. Track player win rate for each strategy against each dealer upcard (2 through Ace)
5. Print a text heatmap table showing win rates:
   Dealer: 2    3    4    5    6    7    8    9    10   A
   Stand:  45%  47%  49%  51%  52%  37%  35%  34%  30%  25%
   Hit:    ...
6. Print which strategy wins overall and by how much

Test case 1: Dealer showing 6 -- Stand strategy should have higher win rate than Hit.
Test case 2: Dealer showing Ace -- both strategies should be below 40% win rate.
Test case 3: Overall -- print which strategy is better and the win rate difference.

Fix any errors and confirm all three tests pass.
```

-----

### App 6 -- Backgammon Analyzer

**File:** `/Analytics/backgammon.py`  
**What it does:** Pip counter + dice probability heatmap.

**Claude Code prompt:**

```
Create backgammon.py in the Analytics folder.

The script should:
1. Ask user for two pip counts (mine and opponent's)
2. Roll two virtual dice 10,000 times and calculate:
   - Frequency of each total (2 through 12)
   - Probability of any double
   - Probability of double-6 specifically
3. Print a text heatmap of dice frequencies:
   Roll:  2    3    4    5    6    7    8    9    10   11   12
   Freq:  3%   6%   8%   11%  14%  17%  14%  11%  8%   6%   3%
4. Print pip advantage (who is ahead and by how much)
5. Print: "Probability of any double: X%"
6. Print: "Probability of double-6: X%"

Use only Python standard library.

Test case 1: Pip counts 120 vs 145.
Expected: Player 2 is ahead by 25 pips.

Test case 2: Double-6 probability over 10,000 rolls.
Expected: Between 2.5% and 3.0% (true value is 2.78%).

Test case 3: Total of 7 should be the most frequent roll.
Expected: 7 appears more than any other total.

Fix any errors and confirm all three tests pass.
```

-----

### App 7 -- Monte Carlo Lab

**File:** `/Lab/monte_carlo.py`  
**What it does:** Three experiments -- Pi estimation, Gambler’s Ruin, risk histogram.

**Claude Code prompt:**

```
Create monte_carlo.py in the Lab folder.

The script should show a menu with three experiments:

Option 1 -- Pi Estimation:
  Run 1,000,000 random point trials inside a unit square.
  Count points inside the unit circle (x²+y²≤1).
  Estimate Pi = 4 × (points inside / total points).
  Print estimated Pi and error vs true Pi.

Option 2 -- Gambler's Ruin:
  Ask for starting bankroll, bet size, and target amount.
  Run 10,000 trials of a 50/50 game.
  Each trial: bet until bankroll hits 0 or reaches target.
  Print: probability of reaching target, average bets played.

Option 3 -- Risk Histogram:
  Simulate 10,000 portfolio outcomes.
  Assume 7% average annual return, 15% standard deviation, 10 years.
  Print a text histogram with 10 buckets showing return distribution.

Use only Python standard library.

Test case 1 (Option 1): Pi estimate with 1,000,000 points.
Expected: Result between 3.13 and 3.15.

Test case 2 (Option 2): Bankroll 100, bet 10, target 200.
Expected: Win probability prints, average bets prints, no errors.

Test case 3 (Option 3): Histogram shows a spread of outcomes.
Expected: 10 buckets print with ASCII bars, no errors.

Fix any errors and confirm all three tests pass.
```

-----

### App 8 -- Bayesian Engine

**File:** `/Lab/bayesian_engine.py`  
**What it does:** Coin fairness tester + A/B test analyzer.

**Claude Code prompt:**

```
Create bayesian_engine.py in the Lab folder.

The script should show a menu with two analyses:

Option 1 -- Coin Fairness Test:
  Ask: how many heads and tails observed?
  Start with uniform prior (Beta with alpha=1, beta=1).
  Update using conjugate Beta-Binomial: 
    new_alpha = 1 + heads, new_beta = 1 + tails
  Calculate posterior mean = alpha / (alpha + beta)
  Calculate 95% credible interval using normal approximation.
  Print: posterior mean, credible interval, verdict (fair if interval 
  includes 0.5, biased otherwise).

Option 2 -- A/B Test:
  Ask for conversions and trials for version A and version B.
  Draw 100,000 samples from Beta posteriors for each version.
  Print: probability B beats A, expected lift percentage.

Use only Python standard library and the random module.

Test case 1 (Option 1): 10 heads, 2 tails.
Expected: Posterior mean near 0.83, verdict is biased toward heads.

Test case 2 (Option 1): 50 heads, 50 tails.
Expected: Posterior mean near 0.5, verdict is fair.

Test case 3 (Option 2): A gets 45/100, B gets 55/100.
Expected: Probability B beats A above 80%.

Fix any errors and confirm all three tests pass.
```

-----

## Part 3 -- Running Apps in Codespaces

After Claude Code builds an app you have two ways to run it.

### Option A -- Ask Claude Code to Run It

Still inside a Claude Code session:

```
Run Essentials/weather.py and show me the output for the city Barcelona.
```

### Option B -- Run It Yourself in the Terminal

Exit Claude Code first:

```
/exit
```

Then in the regular Codespaces terminal:

```bash
# Python apps
python3 Essentials/weather.py
python3 Essentials/utils.py
python3 Essentials/logger.py
python3 Essentials/bj_simple.py
python3 Analytics/bj_pro.py
python3 Analytics/backgammon.py
python3 Lab/monte_carlo.py
python3 Lab/bayesian_engine.py
```

### Switching Between Claude Code and Terminal

```bash
claude        # enter Claude Code
/exit         # return to regular terminal
python3 ...   # run your app
claude        # go back to Claude Code
```

-----

## Part 4 -- Debugging with Claude Code

### If an App Crashes

Re-enter Claude Code and paste:

```
weather.py crashed with this error:
[paste the exact error message]
Fix it and run it again to confirm.
```

### If Results Look Wrong

```
bj_simple.py is showing 0% bust for a hand of 16.
That should be around 60%. Find the bug and fix it.
Run all three test cases again to confirm.
```

### If a Package Is Missing

```
logger.py failed because a module is missing.
Install whatever is needed and run it again.
```

### Nuclear Option -- Start the App Over

```
Delete Essentials/weather.py and rebuild it from scratch.
[paste the original prompt again]
```

-----

## Part 5 -- Save to GitHub

### After Each App -- Archive It

Exit Claude Code, then in the terminal:

```bash
git add .
git commit -m "Add App 1: Weather Advisor -- all tests passing"
git push
```

### Commit Message Formula

```
Add App [N]: [Name] -- all tests passing
```

Examples:

```bash
git commit -m "Add App 2: Utility Kit -- all tests passing"
git commit -m "Add App 5: Pro Blackjack -- heatmap working"
git commit -m "Fix App 3: Logger -- Bayesian calculation corrected"
```

### Or Ask Claude Code to Commit

```
Commit all changes with the message "Add App 1: Weather Advisor -- all tests passing" and push to GitHub.
```

### Verify on GitHub

Go to github.com → your repo → you should see your new files in the Essentials, Analytics, and Lab folders.

-----

## Part 6 -- Working Copy Sync (Offline Backup)

After each push to GitHub:

1. Open **Working Copy** on iPad
1. Tap your `Cruise-Workbook-2026` repo
1. Tap **Pull**
1. Your latest code is now saved locally on your iPad

If Starlink goes down you can still read all your code in Working Copy.

-----

## Part 7 -- Quick Reference

### Daily Workflow

```
1. Open Edge → codespaces.github.com → resume your codespace
2. Open terminal → type: claude
3. Paste a prompt → Claude Code builds and tests the app
4. /exit → python3 [app] to run it yourself (optional)
5. git add . && git commit -m "..." && git push
6. Working Copy → Pull
```

### All 8 Apps at a Glance

|#|File              |Folder     |Key Test                                 |
|-|------------------|-----------|-----------------------------------------|
|1|weather.py        |/Essentials|Nassau temp + recommendation             |
|2|utils.py          |/Essentials|12-char password, 100 USD = 92 EUR       |
|3|logger.py         |/Essentials|Mood > 70% for "Great Day Amazing Cruise"|
|4|bj_simple.py      |/Essentials|Hand 16 = ~60% bust, Hand 11 = 0% bust   |
|5|bj_pro.py         |/Analytics |Dealer 6 better than Dealer Ace          |
|6|backgammon.py     |/Analytics |Double-6 ≈ 2.78%, 7 is most frequent     |
|7|monte_carlo.py    |/Lab       |Pi estimate between 3.13 and 3.15        |
|8|bayesian_engine.py|/Lab       |10H/2T → posterior mean ≈ 0.83           |

### Codespaces Limits

- **Free:** 60 hours/month of active use
- **Tip:** Close the browser tab when not coding -- the clock pauses when inactive
- **Resume:** Always reopen at codespaces.github.com -- never create a new codespace

-----

> *Claude Code · GitHub Codespaces · iPad · Starlink Maritime*  
> *MSC Meraviglia -- Atlantic Crossing 2026*