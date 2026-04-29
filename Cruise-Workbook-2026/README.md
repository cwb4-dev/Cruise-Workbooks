# 🚢 Cruise-Workbook-2026

**Atlantic Data Lab -- MSC Meraviglia 2026**  
**Setup:** Blink Shell + DigitalOcean + Claude Code + GitHub + Starlink

-----

## Project Structure

```
~/at-sea-ipad-workbooks/Cruise-Workbook-2026/
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

Each folder contains an `app_log.md` tracking the build prompt, test results, and sample output.

-----

## The 8 Apps

|#|App            |File              |Folder    |What It Does                                   |
|-|---------------|------------------|----------|-----------------------------------------------|
|1|Weather Advisor|weather.py        |Essentials|Live temp + Lido Deck vs Library recommendation|
|2|Utility Kit    |utils.py          |Essentials|Password generator + currency converter        |
|3|Activity Logger|logger.py         |Essentials|Daily log with Bayesian mood estimate          |
|4|Basic Blackjack|bj_simple.py      |Essentials|Bust probability for any hand total            |
|5|Pro Blackjack  |bj_pro.py         |Analytics |Stand vs Hit heatmap across all dealer upcards |
|6|Backgammon     |backgammon.py     |Analytics |Dice probability heatmap + pip counter         |
|7|Monte Carlo Lab|monte_carlo.py    |Lab       |Pi estimator, Gambler’s Ruin, portfolio risk   |
|8|Bayesian Engine|bayesian_engine.py|Lab       |Coin fairness tester + A/B test analyzer       |

-----

## How to Run Any App

```bash
# Connect to Droplet
mosh --verbose root@147.182.190.94

# Navigate to project
cd ~/at-sea-ipad-workbooks/Cruise-Workbook-2026

# Run an app directly
python3 Essentials/weather.py

# Or use Claude Code
claude
```

## How to Push to GitHub

```bash
git add .
git commit -m "Add App 1: Weather Advisor -- all tests passing"
git push
```

-----

## Stack

|Tool                |Role                              |
|--------------------|----------------------------------|
|iPad + Blink Shell  |Terminal interface                |
|DigitalOcean Droplet|Always-on Ubuntu server           |
|Mosh                |Resilient connection over Starlink|
|Claude Code         |AI that builds and tests the apps |
|GitHub              |Code backup and sync              |
|Working Copy        |Offline iPad access               |

-----

*Built at sea -- MSC Meraviglia -- Starlink Maritime -- 2026*