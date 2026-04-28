# 🚢 Atlantic Data Lab: Master Implementation Workbook

**Version 3**  
**Setup:** Blink Shell (iPad) + DigitalOcean Droplet + Claude Code + GitHub + Starlink  
**Philosophy:** Simple, elegant, and "couch potato" efficient.

-----

## Overview -- How Everything Fits Together

```
iPad (Blink Shell)
  └── mosh AI-Server
        └── DigitalOcean Droplet (Ubuntu 24.04)
              ├── Claude Code (claude --server-mode)
              │     └── QR code → Claude Mobile App on iPad
              │           └── Type prompts → apps get built & tested
              ├── python3 [app] → run apps directly in terminal
              └── git push → GitHub → Working Copy (offline backup)
```

**Two ways to work:**

- **Remote Control** -- scan QR in Blink, type from Claude mobile app (couch mode)
- **Direct** -- type prompts straight into Blink terminal (power mode)

-----

## Part 1: One-Time Server Setup

*Do this once. Everything here survives reboots. You will never need to repeat these steps.*

### 1.1 Create Your DigitalOcean Droplet

1. On your iPad open Edge and go to [cloud.digitalocean.com](https://cloud.digitalocean.com)
1. Log in → tap **Create** → **Droplets**
1. Settings:
- **OS:** Ubuntu 24.04 LTS
- **Plan:** Basic $4/mo
- **Region:** Closest to your current or next port
- **Authentication:** SSH key (if you have one) or Password
1. Tap **Create Droplet** -- takes about 60 seconds
1. Copy the **IP Address** -- you will use this in Blink

> **Billing note:** Your Droplet runs and bills 24/7 whether you use it or not. At $4/mo with a $200 sign-on credit you have ~50 months free. Leave it running for the cruise -- don’t power off.

> **IP note:** Your IP stays the same as long as the Droplet exists. It only changes if you Destroy and rebuild.

-----

### 1.2 Set Up Blink Shell on iPad

**Install Mosh on the Droplet first** (do this via the DigitalOcean web console or after first SSH login):

```bash
apt install -y mosh
```

**Why Mosh instead of SSH:**

|Problem                  |SSH                    |Mosh                       |
|-------------------------|-----------------------|---------------------------|
|Starlink drops 10 seconds|Session dies           |Reconnects silently        |
|Ship moves, IP changes   |SSH hangs forever      |Mosh follows automatically |
|iPad goes to sleep       |Connection lost        |Picks up where you left off|
|Port change at sea       |Must reconnect manually|Transparent handoff        |

**Configure Blink:**

1. Open Blink Shell on your iPad
1. Type `config` and tap Enter
1. Tap **Hosts** → **New Host**
1. Fill in:
- **Label:** `AI-Server`
- **Hostname:** your Droplet IP address
- **User:** `root`
- **Mosh:** toggle **ON**
1. Tap Save

**Connect:**

```bash
# First time or if Mosh isn't installed yet
ssh AI-Server

# Every time after -- always prefer this
mosh AI-Server
```

> **Tip:** After first login via SSH, install Mosh (`apt install -y mosh`), then disconnect and reconnect using `mosh AI-Server`. From that point on always use Mosh.

-----

### 1.3 Install Everything on the Droplet

Follow these steps in order. You are typing in your Blink terminal connected to the Droplet. The prompt looks like `root@your-droplet:~#`

#### Step 1 -- Add Swap Space (do this FIRST)

The $4/mo Droplet has only 458MB RAM -- not enough to run the Claude Code installer without swap. Do this before anything else:

```bash
fallocate -l 1G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

Verify swap is live:

```bash
free -h
```

You should see `1.0Gi` in the Swap row. If you skip this step the Claude Code installer will be killed silently.

#### Step 2 -- Update the Server

```bash
apt update && apt upgrade -y
```

This takes 1–2 minutes with a lot of scrolling output -- that is normal. If prompted about config files, type `N` and Enter for each one. On a fresh Droplet all config files are stock Ubuntu defaults -- there is nothing custom to protect.

#### Step 3 -- Install Python

```bash
apt install -y python3-pip
```

Verify:

```bash
python3 --version
```

Expected: `Python 3.12.x`

#### Step 4 -- Install Mosh

```bash
apt install -y mosh
```

No verification needed. After this step you can disconnect and reconnect using `mosh AI-Server` from Blink for all future sessions.

#### Step 5 -- Install Claude Code

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

The installer will warn that `~/.local/bin` is not in your PATH. Fix that immediately:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Verify:

```bash
claude --version
```

Expected: `2.1.x (Claude Code)` -- you need 2.1.51 or higher for Remote Control. Version 2.1.119 confirmed working.

#### Step 6 -- Authenticate Claude Code

Your Droplet is a headless server with no browser. Do not run `claude` directly to authenticate -- it will try to open a browser that doesn’t exist. Use an API key instead.

1. On your iPad open a new Edge tab: [console.anthropic.com](https://console.anthropic.com)
1. Go to **API Keys** → **Create Key** → copy the key (starts with `sk-ant-...`)
1. Back in Blink, set the key permanently:

```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-your-full-key-here"' >> ~/.bashrc
source ~/.bashrc
```

Verify the key is loaded:

```bash
echo $ANTHROPIC_API_KEY
```

It should print your full key. Then smoke test Claude Code:

```bash
claude -p "Say hello in one word"
```

Expected: a single word response like `Hello`. If you see an auth error, double-check the key was copied completely -- they are long strings.

> **Two separate accounts:** Your claude.ai Pro/Max subscription is needed for Remote Control. Your Anthropic API key (console.anthropic.com) is what Claude Code uses to run on the Droplet -- these are billed separately.

-----

### 1.4 Connect GitHub to the Droplet

*Complete this entire section before moving to 1.5. The clone in Step 1.5 won’t work without it.*

#### Step 1 -- Generate an SSH Key on the Droplet

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

Press Enter through all prompts -- no passphrase needed.

#### Step 2 -- Copy the Public Key

```bash
cat ~/.ssh/id_ed25519.pub
```

Select and copy the entire output. It starts with `ssh-ed25519` and ends with your email.

#### Step 3 -- Add the Key to GitHub

1. On your iPad go to [github.com](https://github.com) → your profile photo → **Settings**
1. Tap **SSH and GPG keys** → **New SSH key**
1. Title: `Cruise-Droplet`
1. Paste the key and tap **Add SSH key**

#### Step 4 -- Test the Connection

```bash
ssh -T git@github.com
```

If you see a fingerprint warning, type `yes` and Enter -- expected on first connection.

Expected: `Hi your_username! You've successfully authenticated...`

-----

### 1.5 Clone Your Repo and Create Project Folders

```bash
# Configure git identity (required for commits)
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"

# Clone your existing repo
cd ~
git clone git@github.com:your_username/Cruise-Workbook-2026.git
cd Cruise-Workbook-2026

# Create the 3 folders all 8 apps expect
mkdir -p Essentials Analytics Lab
```

Verify the structure:

```bash
ls -la
```

You should see `Essentials/`, `Analytics/`, and `Lab/` listed alongside any existing files.

-----

### 1.6 Remote Control Setup (Couch Mode)

Remote Control lets you type from the Claude mobile app on your iPad while Claude Code runs on the stable Droplet. If Starlink drops, Mosh keeps the Droplet session alive and Blink reconnects automatically.

#### Step 1 -- Start Claude Code in Server Mode

```bash
cd ~/Cruise-Workbook-2026
claude --server-mode
```

Claude Code starts and waits for a remote connection.

#### Step 2 -- Show the QR Code

Press **Spacebar**. A QR code appears in the terminal.

#### Step 3 -- Connect from iPad

Open your iPad camera, scan the QR code, tap **Open** when prompted. The Claude mobile app opens with your live Droplet session.

#### Step 4 -- Verify the Connection

In the Claude mobile app type:

```
List the files in the current directory
```

Claude Code should respond with the actual contents of your `Cruise-Workbook-2026` folder on the Droplet. If it does, Remote Control is fully working.

> **Requirements:** claude.ai Pro or Max subscription. Claude Code v2.1.51 or later (`claude --version` to check, `claude update` to upgrade).

-----

## Part 2: How Claude Code Works

### Starting and Stopping

```bash
claude                  # start interactive session (direct in terminal)
claude --server-mode    # start Remote Control session (scan QR from iPad)
claude -p "prompt"      # run a single prompt and exit (useful for testing)
```

Inside a Claude Code session:

```
/exit       # close Claude Code, return to terminal
/clear      # wipe conversation history, fresh start
/undo       # reverse the last file change Claude made
/status     # show which files have been changed this session
/cost       # show token usage and estimated API spend for this session
```

### The Prompt Formula

Every prompt you send to Claude Code should follow this structure for best results:

```
Create [filename] in [folder].

The script should:
1. [what it does -- be specific]
2. [next behaviour]
3. [next behaviour]

Use only Python standard library. [or name any packages allowed]

Test case 1: [specific input]
Expected: [specific output or range]

Test case 2: [specific input]
Expected: [specific output or range]

Fix any errors automatically and confirm when all tests pass.
```

The last line is important -- it tells Claude Code to loop on errors rather than stopping and asking you what to do.

### Running Apps Two Ways

**Option A -- Ask Claude Code to run it (easiest):**

```
Run Essentials/weather.py with the city Nassau and show me the output.
```

**Option B -- Run it yourself in the terminal:**

```bash
/exit                              # leave Claude Code first
python3 Essentials/weather.py      # run directly
claude                             # go back when done
```

### Debugging Prompts

**If an app crashes:**

```
weather.py crashed with this error:
[paste exact error message here]
Fix it and run it again to confirm it works.
```

**If results look wrong:**

```
bj_simple.py is showing 0% bust for a hand of 16.
That should be around 60%. Find the bug and fix it.
Run all three test cases again to confirm.
```

**If a package is missing:**

```
logger.py failed because a module is missing.
Install whatever is needed and run it again.
```

**Nuclear option -- start over:**

```
Delete Essentials/weather.py and rebuild it from scratch using this spec:
[paste original prompt]
```

-----

## Part 3: The 8 Apps

*Use these prompts exactly as written. Each includes multiple test cases so Claude Code validates its own work before confirming.*

-----

### App 1 -- Weather Advisor

**File:** `Essentials/weather.py`  
**What it does:** Fetches live temperature for any city using a free API. Recommends Lido Deck or Library based on conditions.

**Prompt:**

```
Create weather.py in the Essentials folder.

The script should:
1. Ask the user to type a city name
2. Fetch current temperature and weather condition from the Open-Meteo
   geocoding and forecast APIs -- no API key needed, completely free
3. Print the city name, temperature in both Celsius and Fahrenheit,
   and the current weather condition
4. Print a recommendation:
   - Temp above 22C and no rain → "🌞 Lido Deck recommended"
   - Temp below 18C or rainy conditions → "📚 Library recommended"
   - Otherwise → "☁️ Either works today"

Use only Python standard library plus the urllib module for HTTP requests.
Do not use the requests package.

Test case 1: Run with the city Nassau.
Expected: Temperature prints in C and F, recommendation prints, no errors.

Test case 2: Run with the city London.
Expected: Cooler temperature, likely Library recommendation.

Test case 3: Run with an invalid city name like "XYZABC123".
Expected: Script handles the error gracefully and prints a helpful message
instead of crashing.

Fix any errors automatically and confirm all three tests pass.
```

**After it’s built, verify manually:**

```
Run Essentials/weather.py with the city Barcelona.
Show me the full output.
```

-----

### App 2 -- Utility Kit

**File:** `Essentials/utils.py`  
**What it does:** Password generator and currency converter in one menu-driven script.

**Prompt:**

```
Create utils.py in the Essentials folder.

The script should show a repeating menu:
  1. Generate password
  2. Currency converter
  3. Exit

Option 1 -- Password Generator:
  Ask for desired length (default 16 if user just presses Enter).
  Generate a random password using uppercase letters, lowercase letters,
  numbers, and symbols (!@#$%^&*).
  Ensure at least one character from each category is included.
  Print the generated password.

Option 2 -- Currency Converter:
  Ask for direction: 1 for USD→EUR, 2 for EUR→USD.
  Use rate: 1 USD = 0.92 EUR.
  Ask for the amount.
  Print the converted value formatted to 2 decimal places.

Loop back to the menu after each operation until user picks Exit.

Use only Python standard library.

Test case 1: Generate a password of length 12.
Expected: Exactly 12 characters, contains mixed uppercase, lowercase,
numbers and symbols, no errors.

Test case 2: Generate a password of length 20.
Expected: Exactly 20 characters.

Test case 3: Convert 100 USD to EUR.
Expected: 92.00 EUR.

Test case 4: Convert 200 EUR to USD.
Expected: 217.39 USD.

Test case 5: Enter an invalid menu option.
Expected: Script shows an error message and loops back to menu, does not crash.

Fix any errors and confirm all five tests pass.
```

-----

### App 3 -- Activity Logger

**File:** `Essentials/logger.py`  
**What it does:** Logs daily entries with timestamps and calculates a Bayesian mood estimate from word patterns.

**Prompt:**

```
Create logger.py in the Essentials folder.

The script should:
1. Ask the user to type a log entry (free text)
2. Append the entry with a UTC timestamp to log.txt in the Essentials folder
3. Read all past entries from log.txt
4. Scan all entries for mood words:
   - Positive: great, good, amazing, wonderful, excellent, fantastic, love
   - Negative: bad, terrible, awful, rough, hard, horrible, hate
5. Calculate a Bayesian mood estimate:
   - Start with prior probability of 0.5
   - For each positive word found across all entries: multiply prior by 0.8
     and renormalize so probabilities sum to 1
   - For each negative word found across all entries: multiply prior by 0.2
     and renormalize
   - Cap the result between 5% and 95%
6. Print: "Mood estimate: X% positive" (as a percentage, 0 decimal places)
7. Print: "Entry saved. Total entries: N"

Use only Python standard library.

Test case 1: Run with entry "Great day, amazing cruise today".
Expected: Mood estimate above 70%, entry saved, total entries = 1.

Test case 2: Run again with entry "Rough seas, terrible weather, hard day".
Expected: Mood estimate drops significantly, total entries = 2.

Test case 3: Run a third time with entry "Just a normal day".
Expected: Mood estimate between the previous two values, total entries = 3.

Test case 4: Verify log.txt was created and contains all three entries
with timestamps.
Expected: cat Essentials/log.txt shows 3 entries.

Fix any errors and confirm all four tests pass.
```

-----

### App 4 -- Basic Blackjack

**File:** `Essentials/bj_simple.py`  
**What it does:** Monte Carlo simulation of bust probability for any starting hand total.

**Prompt:**

```
Create bj_simple.py in the Essentials folder.

The script should:
1. Ask the user for a starting hand total (integer between 1 and 20)
2. Validate input -- if out of range, ask again
3. Run 10,000 Monte Carlo trials (not 1,000 -- use 10,000 for accuracy)
4. Each trial: draw one random card from an infinite deck
   - Cards 2-9: face value
   - 10, J, Q, K: all worth 10 (so 4 out of 13 cards are worth 10)
   - Ace: worth 1 or 11, whichever does not cause a bust
     (if hand + 11 <= 21, use 11; otherwise use 1)
5. Count trials where (hand total + card value) exceeds 21 -- that is a bust
6. Print: "Hand: [total] -- Bust probability: X.X% over 10,000 trials"

Use only Python standard library.

Test case 1: Hand of 16.
Expected: Bust probability between 55% and 70%.

Test case 2: Hand of 11.
Expected: Bust probability of exactly 0% -- impossible to bust on one card
from a total of 11 (highest card is 10, giving 21).

Test case 3: Hand of 20.
Expected: Bust probability above 90% -- only an Ace (as 1) avoids bust.

Test case 4: Hand of 1.
Expected: Bust probability of 0% -- impossible to bust from 1.

Fix any errors and confirm all four tests pass.
```

-----

### App 5 -- Pro Blackjack Analyzer

**File:** `Analytics/bj_pro.py`  
**What it does:** Strategy comparison across all dealer upcards using 10,000 Monte Carlo trials per scenario, displayed as a text heatmap.

**Prompt:**

```
Create bj_pro.py in the Analytics folder.

The script should:
1. Run 10,000 Monte Carlo simulations for each combination of:
   - Player strategy: Always Stand vs Always Hit (player hand fixed at 16)
   - Dealer upcard: 2, 3, 4, 5, 6, 7, 8, 9, 10, Ace (10 upcards)
   That is 20 scenarios total × 10,000 trials = 200,000 simulations.

2. Simulate dealer play correctly:
   - Dealer draws from an infinite deck (equal probability for each card)
   - Dealer must hit on any total of 16 or less
   - Dealer must hit on soft 17 (Ace + 6)
   - Dealer stands on hard 17 or above

3. For Stand strategy: player keeps 16. Player wins if dealer busts
   or if dealer final total is less than 16 (impossible -- dealer always
   reaches 17+). Player wins only when dealer busts.

4. For Hit strategy: player draws one card to 16.
   - If player busts: player loses regardless of dealer.
   - If player does not bust: compare player total to dealer final total.
   - Higher total wins. Tie is a push (no win, no loss).

5. Print a formatted text heatmap table:

   BLACKJACK STRATEGY HEATMAP -- Player Hand: 16
   ─────────────────────────────────────────────────────────────
   Strategy │  2    3    4    5    6    7    8    9   10    A
   ─────────────────────────────────────────────────────────────
   Stand    │ 35%  37%  40%  43%  44%  26%  24%  23%  18%  17%
   Hit      │ 38%  39%  40%  40%  41%  40%  38%  35%  30%  28%
   ─────────────────────────────────────────────────────────────
   Better   │ Hit  Hit  --   --  Std  Hit  Hit  Hit  Hit  Hit

   (Percentages are examples -- actual results will vary by simulation)

6. Print overall win rate for each strategy across all dealer upcards.
7. Print the verdict: which strategy is better overall and by how much.

Use only Python standard library.

Test case 1: Dealer showing 6 -- Stand strategy win rate should be
within 5 percentage points of Hit or higher. Dealer busts most often
showing 6, so Stand is reasonable here.

Test case 2: Dealer showing Ace -- both strategies should show win rates
below 35%.

Test case 3: The heatmap table prints cleanly with no formatting errors,
all 10 upcards shown, percentages between 0% and 100%.

Test case 4: Overall verdict prints and identifies which strategy wins more.

Fix any errors and confirm all four tests pass.
```

-----

### App 6 -- Backgammon Analyzer

**File:** `Analytics/backgammon.py`  
**What it does:** Pip counter, dice probability heatmap, and double-6 frequency over 50,000 simulated rolls.

**Prompt:**

```
Create backgammon.py in the Analytics folder.

The script should:
1. Ask user for two pip counts: "Your pip count" and "Opponent pip count"
2. Validate both inputs are positive integers
3. Simulate 50,000 rolls of two six-sided dice
4. Calculate and store:
   - Frequency count of each possible sum (2 through 12)
   - Probability of each sum as a percentage
   - Number of doubles (both dice same value)
   - Number of double-6 specifically
5. Print a text heatmap of dice sum frequencies:

   BACKGAMMON DICE PROBABILITY HEATMAP (50,000 rolls)
   ────────────────────────────────────────────────────
   Sum │ Freq  │ Probability │ Bar
   ────┼───────┼─────────────┼────────────────────────
    2  │  1389 │    2.8%     │ ██
    3  │  2778 │    5.6%     │ █████
    7  │  8333 │   16.7%     │ ████████████████
   ...etc for all sums 2 through 12

6. Print pip advantage:
   - "You lead by X pips" or "Opponent leads by X pips" or "Even"
7. Print: "Any double: X.X%" (true value ≈ 16.67%)
8. Print: "Double-6: X.X%" (true value ≈ 2.78%)

Use only Python standard library.

Test case 1: Pip counts 120 vs 145.
Expected: "Opponent leads by 25 pips"

Test case 2: Double-6 probability over 50,000 rolls.
Expected: Result between 2.5% and 3.1% (true value is 2.78%).

Test case 3: Sum of 7 should have the highest frequency.
Expected: 7 appears more often than any other sum.

Test case 4: All 11 sums (2 through 12) appear in the heatmap,
bars scale proportionally to frequency.

Test case 5: Invalid pip count input (negative number or text).
Expected: Script asks again rather than crashing.

Fix any errors and confirm all five tests pass.
```

-----

### App 7 -- Monte Carlo Lab

**File:** `Lab/monte_carlo.py`  
**What it does:** Three experiments in one menu -- Pi estimation, Gambler’s Ruin simulator, and portfolio risk histogram.

**Prompt:**

```
Create monte_carlo.py in the Lab folder.

The script should display a menu and loop until the user exits:
  1. Pi Estimation
  2. Gambler's Ruin
  3. Portfolio Risk
  4. Exit

Option 1 -- Pi Estimation:
  Run 1,000,000 random point trials inside a unit square.
  For each point (x, y) where x and y are random between 0 and 1:
  check if x² + y² ≤ 1 (inside unit circle quadrant).
  Estimate Pi = 4 × (points inside circle / total points).
  Print: estimated Pi, error vs math.pi, and number of trials.
  Print a note showing the estimate improving as trials increase by
  also printing the estimate at 10,000 and 100,000 trial milestones.

Option 2 -- Gambler's Ruin:
  Ask for: starting bankroll (integer), bet size (integer),
  target amount (integer).
  Validate: target must be greater than starting bankroll,
  bet must be less than starting bankroll.
  Run 10,000 trials. Each trial:
    - Start with the given bankroll
    - Each round: flip a fair coin (50/50)
    - Win: bankroll += bet size
    - Lose: bankroll -= bet size
    - Stop when bankroll reaches 0 (ruin) or target (success)
  Print: probability of reaching target, probability of ruin,
  average number of bets before outcome.

Option 3 -- Portfolio Risk:
  Simulate 10,000 portfolio outcomes over 10 years.
  Assume: 7% average annual return, 15% annual standard deviation.
  Each simulation: compound 10 years of annual returns drawn from
  a normal distribution with mean 0.07 and std 0.15.
  Calculate final portfolio value starting from $10,000.
  Print a text histogram with 12 buckets showing distribution of
  final portfolio values. Scale bars to terminal width.
  Print: median outcome, 10th percentile (bad case),
  90th percentile (good case).

Use only Python standard library and the random module.

Test case 1 (Option 1): Pi estimate with 1,000,000 points.
Expected: Result between 3.13 and 3.15.

Test case 2 (Option 2): Bankroll 100, bet 10, target 200.
Expected: Win probability prints between 0% and 100%,
average bets prints as a positive number, no errors.

Test case 3 (Option 2): Bankroll 100, bet 50, target 200.
Expected: Win probability lower than test case 2 scenario.

Test case 4 (Option 3): Histogram prints with 12 buckets,
bars visible, median and percentile values print.
Expected: Median final value above $10,000 (positive expected return).

Test case 5: Menu loops correctly -- after each option completes,
menu reappears. Exit option terminates cleanly.

Fix any errors and confirm all five tests pass.
```

-----

### App 8 -- Bayesian Engine

**File:** `Lab/bayesian_engine.py`  
**What it does:** Coin fairness tester and A/B test analyzer using Bayesian inference.

**Prompt:**

```
Create bayesian_engine.py in the Lab folder.

The script should display a menu and loop until the user exits:
  1. Coin Fairness Test
  2. A/B Test Analyzer
  3. Exit

Option 1 -- Coin Fairness Test:
  Ask: how many heads observed? how many tails observed?
  Validate: both must be non-negative integers, total must be > 0.
  Use a Beta-Binomial conjugate model:
    - Prior: Beta(alpha=1, beta=1) -- uniform, no prior belief
    - Posterior: Beta(alpha = 1 + heads, beta = 1 + tails)
    - Posterior mean = alpha / (alpha + beta)
  Calculate 95% credible interval using a normal approximation:
    - mean = posterior_mean
    - std = sqrt(alpha * beta / ((alpha+beta)^2 * (alpha+beta+1)))
    - lower = mean - 1.96 * std
    - upper = mean + 1.96 * std
    - Clamp both bounds between 0 and 1
  Print:
    - Posterior mean (probability of heads): X.XX
    - 95% credible interval: [X.XX, X.XX]
    - Verdict: "Likely fair coin" if interval includes 0.5
      "Biased toward heads" if lower bound > 0.5
      "Biased toward tails" if upper bound < 0.5

Option 2 -- A/B Test Analyzer:
  Ask for:
    - Version A: number of conversions and total trials
    - Version B: number of conversions and total trials
  Validate: conversions cannot exceed trials, all values must be positive.
  Use Beta posteriors:
    - Version A posterior: Beta(1 + conversions_A, 1 + trials_A - conversions_A)
    - Version B posterior: Beta(1 + conversions_B, 1 + trials_B - conversions_B)
  Draw 100,000 samples from each posterior using the random module.
  Implement Beta distribution sampling using the relation:
    Beta(a, b) = Gamma(a) / (Gamma(a) + Gamma(b))
  where Gamma samples can be drawn using random.gammavariate(a, 1).
  Calculate:
    - Probability B beats A: fraction of samples where B_sample > A_sample
    - Conversion rate A: conversions_A / trials_A
    - Conversion rate B: conversions_B / trials_B
    - Expected lift: (rate_B - rate_A) / rate_A × 100%
  Print all four values clearly labelled.

Use only Python standard library and the random module.
Do not use numpy or scipy.

Test case 1 (Option 1): 10 heads, 2 tails.
Expected: Posterior mean near 0.83 (= 11/13), verdict biased toward heads.

Test case 2 (Option 1): 50 heads, 50 tails.
Expected: Posterior mean near 0.50, verdict is fair coin.

Test case 3 (Option 1): 0 heads, 10 tails.
Expected: Posterior mean near 0.09, verdict biased toward tails.

Test case 4 (Option 2): A gets 45 conversions from 100 trials,
B gets 55 conversions from 100 trials.
Expected: Probability B beats A above 80%.

Test case 5 (Option 2): A gets 50/100, B gets 51/100.
Expected: Probability B beats A close to 50% -- not a clear winner.

Test case 6: Menu loops correctly, exit terminates cleanly.

Fix any errors and confirm all six tests pass.
```

-----

## Part 4: Save to GitHub After Each App

After Claude Code confirms an app is working, push it to GitHub immediately. Don’t batch them up.

### Option A -- Tell Claude Code to Commit

```
Commit all changes with message "Add App 1: Weather Advisor -- all tests passing"
and push to GitHub.
```

### Option B -- Do It Yourself in the Terminal

```bash
/exit                                        # leave Claude Code
cd ~/Cruise-Workbook-2026
git add .
git commit -m "Add App 1: Weather Advisor -- all tests passing"
git push
claude --server-mode                         # restart Remote Control
```

### Commit Message Formula

```
Add App [N]: [Name] -- all tests passing
Fix App [N]: [Name] -- [what was fixed]
```

### Verify on GitHub

Go to [github.com](https://github.com) → your `Cruise-Workbook-2026` repo → you should see your files in `Essentials/`, `Analytics/`, and `Lab/`.

-----

## Part 5: Working Copy -- Offline Backup on iPad

After every push to GitHub:

1. Open **Working Copy** on your iPad
1. Tap your `Cruise-Workbook-2026` repo
1. Tap **Pull**

Your latest code is now saved locally on your iPad. If Starlink goes down you can still read all your code in Working Copy.

-----

## Part 6: Daily Workflow

Once setup is complete, this is the full loop every session:

```
1. Open Blink Shell → mosh AI-Server
2. cd ~/Cruise-Workbook-2026
3. claude --server-mode → press Space → scan QR with iPad
4. In Claude mobile app → paste app prompt → wait for confirmation
5. Ask Claude: "Run [app] and show me the output"
6. Tell Claude: "Commit and push to GitHub"
7. Open Working Copy on iPad → Pull
```

Or in power mode without Remote Control:

```
1. Open Blink Shell → mosh AI-Server
2. cd ~/Cruise-Workbook-2026
3. claude → paste prompt → confirm tests pass
4. /exit → python3 [app] → run it yourself
5. git add . && git commit -m "..." && git push
6. Working Copy → Pull
```

-----

## Part 7: Quick Reference

### All 8 Apps

|#|File              |Folder    |Key Tests                                         |
|-|------------------|----------|--------------------------------------------------|
|1|weather.py        |Essentials|Nassau temp + recommendation, invalid city handled|
|2|utils.py          |Essentials|12-char password, 100 USD = 92.00 EUR             |
|3|logger.py         |Essentials|Mood > 70% for positive entry, log.txt written    |
|4|bj_simple.py      |Essentials|Hand 16 = ~60% bust, Hand 11 = 0% bust            |
|5|bj_pro.py         |Analytics |Heatmap prints, Stand vs Hit verdict              |
|6|backgammon.py     |Analytics |Double-6 ≈ 2.78%, 7 most frequent                 |
|7|monte_carlo.py    |Lab       |Pi between 3.13–3.15, Gambler’s Ruin runs         |
|8|bayesian_engine.py|Lab       |10H/2T → posterior ≈ 0.83, A/B test runs          |

### Claude Code Commands

|Command               |What It Does                            |
|----------------------|----------------------------------------|
|`claude`              |Start interactive session               |
|`claude --server-mode`|Start Remote Control (then Space for QR)|
|`claude -p "prompt"`  |Single prompt, then exit                |
|`claude --version`    |Check version                           |
|`claude update`       |Update to latest                        |
|`/exit`               |Return to terminal                      |
|`/clear`              |Fresh conversation                      |
|`/undo`               |Reverse last file change                |
|`/cost`               |Token usage this session                |
|`/status`             |Files changed this session              |

### Troubleshooting

|Problem                        |Fix                                                    |
|-------------------------------|-------------------------------------------------------|
|`claude: command not found`    |`source ~/.bashrc`                                     |
|Auth error / invalid API key   |`echo $ANTHROPIC_API_KEY` -- check it’s set             |
|Installer killed silently      |Add swap: `fallocate -l 1G /swapfile` etc              |
|Mosh not found                 |`apt install -y mosh`                                  |
|Git push rejected              |`ssh -T git@github.com` -- check SSH key                |
|App crashes, missing module    |Tell Claude: "Install whatever is needed and run again"|
|Remote Control QR not appearing|Press Spacebar after `claude --server-mode` starts     |

-----

## Appendix: Known Gotchas for This Setup

1. **Always add swap before installing Claude Code.** The $4/mo Droplet has 458MB RAM -- the installer gets silently killed without 1GB of swap.
1. **Always use `mosh` not `ssh`.** On Starlink over open ocean, SSH sessions die regularly. Mosh reconnects transparently.
1. **The API key and claude.ai subscription are separate things.** The API key (console.anthropic.com) pays for Claude Code token usage. The claude.ai Pro/Max subscription enables Remote Control.
1. **Never just Power Off the Droplet to save money.** DigitalOcean bills whether it’s running or not. Destroy it (after Snapshot) if you want to stop charges.
1. **IP address only changes on Destroy + Rebuild.** Power off, reboot, apt upgrade -- all leave the IP unchanged.
1. **`~/.local/bin` is not in PATH by default.** The Claude Code installer warns about this. The fix is in Step 5 above -- if you skip it, `claude` will not be found.
1. **Config file prompts during `apt upgrade` -- always answer N.** On a fresh Droplet there is nothing custom to protect.

-----

*Blink Shell · DigitalOcean · Claude Code · GitHub · Working Copy*  
*MSC Meraviglia -- Starlink Maritime -- 2026*