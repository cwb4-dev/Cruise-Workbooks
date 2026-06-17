# 🚢 Atlantic Data Lab — Grok Build + iPad Workbook v8

![Atlantic Data Lab Toolchain](atlantic-toolchain-diagram.jpg)

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

## Shared Ubuntu Droplet Setup (for both iPad and Mac)

**Both workflows use the same Ubuntu Droplet.**

### Create the Droplet
1. Go to DigitalOcean → Create Droplet
2. **Image**: Ubuntu 24.04 LTS
3. **Size**: Basic (1 vCPU / 1-2 GB RAM)
4. Add your SSH key
5. Name it `atlantic-data-lab`

### Initial Setup on Droplet
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv git mosh -y

mkdir -p ~/atlantic-data-lab && cd ~/atlantic-data-lab
git clone https://github.com/YOURUSERNAME/atlantic-data-lab.git .
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## iPad Workflow (Grok Build)

- Use **Blink Shell + Mosh** to connect to the Droplet.
- Use this chat with Grok for planning and code generation.
- Edit files directly on the Droplet or sync via Working Copy.

---

## Complete Step-by-Step for Each App (Grok Build Style)

### 1. Utility Kit (`Essentials/utils.py`)
**Description**: Password generator + real-time USD/EUR converter.

**Step-by-step**:
1. Connect to Droplet via Mosh in Blink.
2. Create/open `Essentials/utils.py`.
3. Tell me: "Build the Utility Kit in Essentials/utils.py. Include a strong password generator with options and a real-time USD to EUR converter using a free API. Use rich for beautiful cruise-themed output."
4. Copy the generated code into the file.
5. Test: `python Essentials/utils.py`
6. Iterate with follow-up prompts like "Make the UI more cruise-y" or "Add input validation".

### 2. Activity Logger (`Essentials/logger.py`)
**Description**: Daily activity log with Bayesian mood estimation.

**Step-by-step**:
1. Open `Essentials/logger.py`.
2. Prompt: "Build Activity Logger in Essentials/logger.py. Allow daily logging and use simple Bayesian inference for mood estimation. Save to JSON. Add rich summaries."
3. Test and refine on the Droplet.

### 3. Basic Blackjack (`Essentials/bj_simple.py`)
**Description**: Bust probability for any hand total.

**Step-by-step**:
1. Open the file.
2. Prompt: "Implement Basic Blackjack bust probability calculator. User inputs hand total and sees bust probability on hit. Make it educational and cruise-themed."
3. Test on Droplet.

### 4. Pro Blackjack (`Analytics/bj_pro.py`)
**Description**: Stand vs Hit heatmap.

**Step-by-step**:
1. Open the file.
2. Prompt: "Create Pro Blackjack analyzer with full stand vs hit heatmap using numpy and matplotlib. Save the chart as PNG and add rich terminal summary."
3. Run to generate heatmap.

### 5. Backgammon (`Analytics/backgammon.py`)
**Description**: Dice probability heatmap + pip counter.

**Step-by-step**:
1. Open the file.
2. Prompt: "Build Backgammon tool with dice roll probability heatmaps and a pip counter. Add visualizations and cruise theme."

### 6. Monte Carlo Lab (`Lab/monte_carlo.py`)
**Description**: Pi estimator, Gambler's Ruin, portfolio risk.

**Step-by-step**:
1. Open the file.
2. Prompt: "Implement Monte Carlo Lab with Pi estimation, Gambler's Ruin simulation, and simple portfolio risk. Add matplotlib visualizations."

### 7. Bayesian Engine (`Lab/bayesian_engine.py`)
**Description**: Coin fairness tester + A/B test analyzer.

**Step-by-step**:
1. Open the file.
2. Prompt: "Build Bayesian Engine with coin fairness tester and simple A/B test analyzer using Bayesian updating. Add rich output and visualizations."

### 8. (Already Done) Weather Advisor

---

**All apps run on the same Ubuntu Droplet.**  
Push changes from Cursor or edit directly via Mosh on iPad.

**Next**: Say **"Build utils.py"** if you want me to generate the full code for the first app right now.

*Version 8 — Complete step-by-step for each app (Grok/iPad)*