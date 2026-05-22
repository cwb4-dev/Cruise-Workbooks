# 🚢 Cruise-Workbook-2026: Google Edition
**Atlantic Data Lab — MSC Meraviglia 2026**  
**Setup:** Blink Shell + DigitalOcean Droplet + Gemini CLI + GitHub + Starlink  
**Philosophy:** Same 8 apps, same couch potato workflow — Google stack instead of Anthropic.

---

## How This Differs From the Claude Edition

| Feature | Claude Edition | Google Edition |
|---|---|---|
| AI CLI | Claude Code | Gemini CLI |
| Model | Claude Sonnet | Gemini 2.5 Pro |
| Auth | Anthropic API key | Google account or AI Studio key |
| Free tier | No (Pro/Max required) | Yes — 1,000 requests/day free |
| Node.js required | No | Yes (v20+) |
| Droplet IP | 147.182.190.94 | *(new Droplet)* |
| GitHub repo | cwb4-dev/at-sea-ipad-workbooks | Same repo, separate branch |

> **Note:** Gemini CLI is transitioning to **Antigravity CLI** on June 18, 2026 for free/Google One users. This README covers Gemini CLI — update commands after the transition.

---

## Project Structure

```
~/at-sea-ipad-workbooks/Cruise-Workbook-2026-Google/
├── Essentials/
│   ├── weather.py        ← App 1: Weather Advisor
│   ├── utils.py          ← App 2: Utility Kit
│   ├── logger.py         ← App 3: Activity Logger
│   └── bj_simple.py      ← App 4: Basic Blackjack
├── Analytics/
│   ├── bj_pro.py         ← App 5: Pro Blackjack Analyzer
│   └── backgammon.py     ← App 6: Backgammon Analyzer
└── Lab/
    ├── monte_carlo.py    ← App 7: Monte Carlo Lab
    └── bayesian_engine.py ← App 8: Bayesian Engine
```

---

## Part 1: One-Time Server Setup

### 1.1 Create a New DigitalOcean Droplet

1. Open Edge → [cloud.digitalocean.com](https://cloud.digitalocean.com)
2. Tap **Create** → **Droplets**
3. Settings:
   - **OS:** Ubuntu 24.04 LTS
   - **Plan:** Basic $4/mo
   - **Region:** Same as your Claude Droplet
   - **Authentication:** Password or SSH key
4. Tap **Create Droplet** — takes about 60 seconds
5. Copy the **IP Address**
6. Update your Blink host config with a new host label — e.g. `Google-Server`

> **Two Droplets, $8/mo total.** Both covered by your $200 DO credit.

---

### 1.2 Connect via Blink

```bash
# Add new host in Blink config
config
# Hosts → New Host
# Label: Google-Server
# Hostname: YOUR_NEW_DROPLET_IP
# User: root

# Connect
mosh --verbose root@YOUR_NEW_DROPLET_IP
```

---

### 1.3 Install Everything on the Droplet

Follow these steps in order from your Blink terminal connected to the **Google Droplet**.

#### Step 1 — Add Swap Space (do this FIRST)

The $4/mo Droplet has only 458MB RAM. Node.js and Gemini CLI need more. Add swap before anything else:

```bash
fallocate -l 1G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

Verify:

```bash
free -h
```

Expected: `1.0Gi` in the Swap row.

#### Step 2 — Update the Server

```bash
apt update && apt upgrade -y
```

If prompted about config files → type `N` and Enter for each. Takes 1–2 minutes.

#### Step 3 — Install Python

```bash
apt install -y python3-pip
python3 --version
```

Expected: `Python 3.12.x`

#### Step 4 — Install Mosh

```bash
apt install -y mosh
```

Disconnect and reconnect with `mosh --verbose root@YOUR_IP` for all future sessions.

#### Step 5 — Install Node.js 20

Gemini CLI requires Node.js version 20 or higher — this is the main difference from the Claude Code setup:

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs
```

Verify:

```bash
node --version
npm --version
```

Expected: `v20.x.x` and `10.x.x`

#### Step 6 — Install Gemini CLI

```bash
npm install -g @google/gemini-cli
```

Verify:

```bash
gemini --version
```

#### Step 7 — Authenticate Gemini CLI

Gemini CLI has two auth options. Choose based on your situation:

**Option A — Free tier (Google account login):**

Your Droplet is headless — no browser. Use the device code flow:

```bash
gemini auth login --no-browser
```

This prints a URL and a code. On your iPad open the URL in Edge, sign in with your Google account, and enter the code. Free tier gives you 1,000 requests/day.

**Option B — API key (higher limits):**

1. On your iPad go to [aistudio.google.com](https://aistudio.google.com) → **Get API key** → **Create API key**
2. Copy the key (starts with `AIza...`)
3. On the Droplet set it permanently:

```bash
echo 'export GEMINI_API_KEY="AIza-your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

Smoke test either option:

```bash
gemini -p "Say hello in one word"
```

Expected: a single word response.

---

### 1.4 Connect GitHub to the Google Droplet

The Google Droplet needs its own SSH key — you cannot reuse the key from your Claude Droplet.

#### Step 1 — Generate SSH Key

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

Press Enter through all prompts.

#### Step 2 — Copy the Public Key

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the entire output.

#### Step 3 — Add to GitHub

1. Go to [github.com](https://github.com) → **Settings** → **SSH and GPG keys** → **New SSH key**
2. Title: `Google-Droplet`
3. Paste the key → **Add SSH key**

#### Step 4 — Test Connection

```bash
ssh -T git@github.com
```

Expected: `Hi cwb4-dev! You've successfully authenticated...`

---

### 1.5 Clone Repo and Create Project Folders

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"

cd ~
git clone git@github.com:cwb4-dev/at-sea-ipad-workbooks.git
cd at-sea-ipad-workbooks

# Create a separate folder for Google edition apps
mkdir -p Cruise-Workbook-2026-Google/Essentials
mkdir -p Cruise-Workbook-2026-Google/Analytics
mkdir -p Cruise-Workbook-2026-Google/Lab

cd Cruise-Workbook-2026-Google
ls -la
```

---

## Part 2: How Gemini CLI Works

### Starting and Stopping

```bash
gemini                  # start interactive session
gemini -p "prompt"      # run a single prompt and exit
```

Inside a Gemini CLI session:

```
/exit       # close Gemini CLI, return to terminal
/clear      # wipe conversation history, fresh start
/help       # show available commands
/stats      # show token usage this session
```

### Key Differences From Claude Code

| Feature | Claude Code | Gemini CLI |
|---|---|---|
| Start command | `claude` | `gemini` |
| Single prompt | `claude -p "..."` | `gemini -p "..."` |
| Cost check | `/cost` | `/stats` |
| Context file | `CLAUDE.md` | `GEMINI.md` |
| Remote Control | `claude --server-mode` | Not available |
| Model | Claude Sonnet | Gemini 2.5 Pro |
| Context window | 200K tokens | 1M tokens |

> **No Remote Control in Gemini CLI** — you work directly in Blink terminal only. No QR code / mobile app bridge like Claude Code offers.

### The Prompt Formula

Same structure works for Gemini CLI:

```
Create [filename] in [folder].

The script should:
1. [specific behaviour]
2. [specific behaviour]

Use only Python standard library.

Test case 1: [input]
Expected: [output]

Test case 2: [input]
Expected: [output]

Fix any errors automatically and confirm when all tests pass.
```

---

## Part 3: The 8 Apps

*Use these prompts in Gemini CLI. Same apps as the Claude edition — compare the results.*

---

### App 1 — Weather Advisor
**File:** `Essentials/weather.py`

```
Create weather.py in the Essentials folder.

The script should:
1. Ask the user to type a city name
2. Fetch current temperature and weather condition from the Open-Meteo
   geocoding and forecast APIs — no API key needed, completely free
3. Print the city name, temperature in both Celsius and Fahrenheit,
   and the current weather condition
4. Print a recommendation:
   - Temp above 22C and no rain → "🌞 Lido Deck recommended"
   - Temp below 18C or rainy conditions → "📚 Library recommended"
   - Otherwise → "☁️ Either works today"

Use only Python standard library plus the urllib module for HTTP requests.
Do not use the requests package.

Test case 1: Run with the city Nassau.
Expected: Temperature in C and F, recommendation prints, no errors.

Test case 2: Run with the city London.
Expected: Cooler temperature, likely Library recommendation.

Test case 3: Run with an invalid city name like "XYZABC123".
Expected: Graceful error message, no crash.

Fix any errors automatically and confirm all three tests pass.
```

---

### App 2 — Utility Kit
**File:** `Essentials/utils.py`

```
Create utils.py in the Essentials folder.

The script should show a repeating menu:
  1. Generate password
  2. Currency converter
  3. Exit

Option 1 — Password Generator:
  Ask for desired length (default 16 if user just presses Enter).
  Generate a random password using uppercase, lowercase, numbers, symbols.
  Ensure at least one character from each category is included.
  Print the generated password.

Option 2 — Currency Converter:
  Ask for direction: 1 for USD→EUR, 2 for EUR→USD.
  Use rate: 1 USD = 0.92 EUR.
  Ask for the amount.
  Print the converted value formatted to 2 decimal places.

Loop back to the menu after each operation until user picks Exit.
Use only Python standard library.

Test case 1: Generate a password of length 12.
Expected: Exactly 12 characters, mixed types, no errors.

Test case 2: Convert 100 USD to EUR.
Expected: 92.00 EUR.

Test case 3: Convert 200 EUR to USD.
Expected: 217.39 USD.

Test case 4: Enter an invalid menu option.
Expected: Error message, loops back to menu, no crash.

Fix any errors and confirm all four tests pass.
```

---

### App 3 — Activity Logger
**File:** `Essentials/logger.py`

```
Create logger.py in the Essentials folder.

The script should:
1. Ask the user to type a log entry (free text)
2. Append the entry with a UTC timestamp to log.txt in the Essentials folder
3. Scan all entries for mood words:
   - Positive: great, good, amazing, wonderful, excellent, fantastic, love
   - Negative: bad, terrible, awful, rough, hard, horrible, hate
4. Calculate a Bayesian mood estimate starting from prior 0.5
5. Print: "Mood estimate: X% positive"
6. Print: "Entry saved. Total entries: N"

Use only Python standard library.

Test case 1: Entry "Great day, amazing cruise today".
Expected: Mood above 70%, entry saved, total = 1.

Test case 2: Entry "Rough seas, terrible weather, hard day".
Expected: Mood drops significantly, total = 2.

Test case 3: Verify log.txt contains both entries with timestamps.
Expected: cat Essentials/log.txt shows 2 timestamped entries.

Fix any errors and confirm all three tests pass.
```

---

### App 4 — Basic Blackjack
**File:** `Essentials/bj_simple.py`

```
Create bj_simple.py in the Essentials folder.

The script should:
1. Ask for a starting hand total (integer 1–20)
2. Validate input — ask again if out of range
3. Run 10,000 Monte Carlo trials
4. Each trial: draw one random card from an infinite deck
   - Cards 2-9: face value
   - 10, J, Q, K: worth 10 (4 out of 13 cards)
   - Ace: 1 or 11, whichever avoids bust
5. Count trials where hand total + card > 21
6. Print: "Hand: [total] — Bust probability: X.X% over 10,000 trials"

Use only Python standard library.

Test case 1: Hand of 16. Expected: 55%–70% bust.
Test case 2: Hand of 11. Expected: 0% bust.
Test case 3: Hand of 20. Expected: above 90% bust.

Fix any errors and confirm all three tests pass.
```

---

### App 5 — Pro Blackjack Analyzer
**File:** `Analytics/bj_pro.py`

```
Create bj_pro.py in the Analytics folder.

Run 10,000 Monte Carlo simulations for each combination of:
- Player strategy: Always Stand vs Always Hit (player hand fixed at 16)
- Dealer upcard: 2, 3, 4, 5, 6, 7, 8, 9, 10, Ace

Simulate dealer play correctly:
- Dealer hits on 16 or less and soft 17
- Dealer stands on hard 17 or above

Print a formatted text heatmap table showing win rates for each
strategy across all dealer upcards. Print overall verdict.

Test case 1: Heatmap prints cleanly, all 10 upcards shown.
Test case 2: Dealer showing Ace — both strategies below 35% win rate.
Test case 3: Overall verdict prints identifying better strategy.

Fix any errors and confirm all three tests pass.
```

---

### App 6 — Backgammon Analyzer
**File:** `Analytics/backgammon.py`

```
Create backgammon.py in the Analytics folder.

The script should:
1. Ask for two pip counts
2. Simulate 50,000 rolls of two six-sided dice
3. Print a text heatmap of dice sum frequencies
4. Print pip advantage
5. Print double-6 frequency

Use only Python standard library.

Test case 1: Pip counts 120 vs 145. Expected: "Opponent leads by 25 pips".
Test case 2: Double-6 probability. Expected: between 2.5% and 3.1%.
Test case 3: Sum of 7 has highest frequency.

Fix any errors and confirm all three tests pass.
```

---

### App 7 — Monte Carlo Lab
**File:** `Lab/monte_carlo.py`

```
Create monte_carlo.py in the Lab folder with a menu:
  1. Pi Estimation (1,000,000 trials)
  2. Gambler's Ruin simulator
  3. Portfolio Risk histogram
  4. Exit

Use only Python standard library and the random module.

Test case 1: Pi estimate between 3.13 and 3.15.
Test case 2: Gambler's Ruin — bankroll 100, bet 10, target 200 — runs without error.
Test case 3: Portfolio histogram prints with median above $10,000.
Test case 4: Menu loops correctly, exit works cleanly.

Fix any errors and confirm all four tests pass.
```

---

### App 8 — Bayesian Engine
**File:** `Lab/bayesian_engine.py`

```
Create bayesian_engine.py in the Lab folder with a menu:
  1. Coin Fairness Test
  2. A/B Test Analyzer
  3. Exit

Use Beta-Binomial conjugate model. Use only Python standard library
and random module. Do not use numpy or scipy.

Test case 1: 10 heads, 2 tails → posterior mean near 0.83, biased toward heads.
Test case 2: 50 heads, 50 tails → posterior mean near 0.50, fair coin.
Test case 3: A gets 45/100, B gets 55/100 → probability B beats A above 80%.
Test case 4: Menu loops, exit works cleanly.

Fix any errors and confirm all four tests pass.
```

---

## Part 4: Git Workflow

After each app is built and tested:

```bash
cd ~/at-sea-ipad-workbooks/Cruise-Workbook-2026-Google
git add .
git commit -m "Add App 1: Weather Advisor (Google) — all tests passing"
git push
```

Then in Working Copy on iPad → tap **Pull**.

---

## Part 5: Claude vs Gemini — What to Compare

Once both editions are complete, compare:

| Metric | Claude Code | Gemini CLI |
|---|---|---|
| Code quality | | |
| Tests passed first try | | |
| Iterations needed | | |
| Error handling | | |
| Code style | | |
| Speed | | |
| Cost | API key (paid) | Free tier |

---

## Quick Reference

### Gemini CLI Commands

| Command | What It Does |
|---|---|
| `gemini` | Start interactive session |
| `gemini -p "prompt"` | Single prompt, then exit |
| `gemini --version` | Check version |
| `/exit` | Return to terminal |
| `/clear` | Fresh conversation |
| `/stats` | Token usage this session |
| `/help` | Show all commands |

### Troubleshooting

| Problem | Fix |
|---|---|
| `gemini: command not found` | `source ~/.bashrc` or check npm install |
| Node.js not found | `curl -fsSL https://deb.nodesource.com/setup_20.x \| bash - && apt install -y nodejs` |
| Auth error | Re-run `gemini auth login --no-browser` |
| Installer killed | Add swap: `fallocate -l 1G /swapfile` etc |
| Git push rejected | `git pull` first then `git push` |

---

## Known Gotchas

1. **Node.js is required** — unlike Claude Code, Gemini CLI needs Node.js 20+. Install it before Gemini CLI.
2. **No Remote Control** — Gemini CLI doesn't have a QR code / mobile app bridge. Work directly in Blink.
3. **Antigravity CLI transition June 18, 2026** — free tier users will need to update commands after this date.
4. **New SSH key needed** — the Google Droplet needs its own key added to GitHub (`Google-Droplet`), separate from `Cruise-Droplet`.
5. **Always add swap first** — same RAM constraint as Claude Droplet, same fix.
6. **Always use `mosh --verbose`** — not `ssh`, for the same Starlink resilience reasons.

---

*Blink Shell · DigitalOcean · Gemini CLI · GitHub · Working Copy*  
*MSC Meraviglia — Starlink Maritime — 2026*
