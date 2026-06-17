# 🚢 Atlantic Data Lab — Complete Vibe Coding Workbooks v2.1

![Atlantic Data Lab Toolchain Overview](attachments/Generated Image.jpg)

**MSC Meraviglia 2026 Edition**  
**iPad + Blink + Mosh + Working Copy + Grok Build Focus**

## 📋 App Tracker (Cleaned Up)

| # | App                  | File                | Folder      | Description                                              | Status     |
|---|----------------------|---------------------|-------------|----------------------------------------------------------|------------|
| 1 | Weather Advisor      | `weather.py`        | Essentials  | Live temperature + Lido Deck vs Library recommendation   | ✅ Done    |
| 2 | Utility Kit          | `utils.py`          | Essentials  | Password generator + real-time USD/EUR converter         | ⬜ Todo    |
| 3 | Activity Logger      | `logger.py`         | Essentials  | Daily activity log with Bayesian mood estimation         | ⬜ Todo    |
| 4 | Basic Blackjack      | `bj_simple.py`      | Essentials  | Bust probability calculator for any hand total           | ⬜ Todo    |
| 5 | Pro Blackjack        | `bj_pro.py`         | Analytics   | Stand vs Hit heatmap across all dealer upcards           | ⬜ Todo    |
| 6 | Backgammon           | `backgammon.py`     | Analytics   | Dice probability heatmap + pip counter                   | ⬜ Todo    |
| 7 | Monte Carlo Lab      | `monte_carlo.py`    | Lab         | Pi estimator, Gambler's Ruin, portfolio risk simulator   | ⬜ Todo    |
| 8 | Bayesian Engine      | `bayesian_engine.py`| Lab         | Coin fairness tester + A/B test analyzer                 | ⬜ Todo    |

---

## iPad Setup Guide (Blink + Mosh + Working Copy)

1. Create DigitalOcean Droplet (Ubuntu 24.04, basic size)
2. In Blink: `mosh user@droplet-ip`
3. Install tools on Droplet: `apt update && apt install python3 python3-venv git mosh -y`
4. Use Working Copy app for Git sync with GitHub
5. Run Python apps directly in Mosh session

**Full detailed steps** are in the Grok Build section below.

## Grok Build Workflow (Recommended for iPad)
- Chat with Grok here for planning and code generation
- Paste code into files on Droplet via Blink/Mosh
- Test and iterate conversationally

---

## Shared Config Files

**requirements.txt**
```txt
requests
pandas
numpy
matplotlib
scipy
rich
python-dotenv
```

**Other files** (create on Droplet or GitHub):
- .gitignore, pyproject.toml, folder structure (Essentials/, Analytics/, Lab/)

---

**Next: Say "Build utils.py" to start coding!**  
*Version 2.1 — Updated with toolchain diagram*