I hear you—"Round One" is about you staying in the driver's seat. You want the AI to provide the components exactly as requested, but you’ll be the one hitting "Run" and verifying the results. It’s the "Couch Potato" version of manual control: you let the AI do the heavy lifting of writing the code, but you keep your hands on the steering wheel.

Here is your **Master Operations Manual**, updated with the specific prompt style you prefer, organized for your Mac-to-iPad workflow.

---

# 🚢 Atlantic Data Lab: Master Operations Manual (2026)
**Philosophy:** Simple, elegant, couch potato.  
**Hardware:** Mac (Woodbury) ➡️ GitHub ➡️ iPad (Atlantic/Starlink).  
**Stack:** Firebase Studio (Edge Browser) + Python + Firestore.

---

## 🛠 Phase 1: The Woodbury Launch (Mac Setup)

1.  **GitHub Repo:** Create a **Private** repository named `Cruise-Workbook-2026`. Do not initialize with any files.
2.  **The Magic Key (Token):** Go to GitHub *Settings > Developer Settings > Tokens (classic)*. Generate a token with `repo` scopes. **Save this in Google Keep.**
3.  **Firebase Studio:** Go to [studio.firebase.google.com](https://studio.firebase.google.com) on your Mac. 
    * Create a New Workspace.
    * Open the Terminal and link it to GitHub:
        `git remote add origin https://github.com/<USER>/Cruise-Workbook-2026.git`
4.  **The Seed:** Create this `README.md` in your project root, commit, and push.

---

## 📂 Phase 2: The 8-App Build Plan
Use these prompts in the **Gemini Sidebar** (Firebase Studio). For each, create the file manually, then paste the prompt.

### **Level 1: The Essentials**

**App 1: Weather Advisor (`weather.py`)**
* **The Prompt:** "@folder Create `weather.py`. Include: 1. Input for temperature and wind speed. 2. Logic suggesting 'Library' (under 60°F) or 'Lido Deck' (over 60°F). 3. Simple Woodbury-style recommendations."
* **Test Case:** "Input 55°F; verify it suggests the Library."

**App 2: Utility Kit (`utils.py`)**
* **The Prompt:** "@folder Create `utils.py`. Include: 1. 12-character secure password generator. 2. USD to Euro converter (rate 0.92). 3. Simple print output for both."
* **Test Case:** "Convert $100; verify result is 92.0."

**App 3: Activity Logger (`logger.py`)**
* **The Prompt:** "@folder Create `logger.py`. Include: 1. Daily text log saved to `cruise_log.txt`. 2. Bayesian mood prior (0.5) to predict tomorrow's mood based on today's success. 3. Save result to Firestore."
* **Test Case:** "Log a 'Great Day'; verify the posterior probability is greater than 0.5."

**App 4: Basic Blackjack (`bj_simple.py`)**
* **The Prompt:** "@folder Create `bj_simple.py`. Include: 1. Monte Carlo simulation (1,000 trials). 2. Calculation of 'Bust' percentage for a hand of 16. 3. Simple percentage output."
* **Test Case:** "Run for a hand of 11; verify bust chance is 0%."

---

### **Level 2: The Deep Dives**

**App 5: Blackjack Pro (`bj_pro.py`)**
* **The Prompt:** "@folder Create `bj_pro.py`. Include: 1. Strategy comparison (Basic vs Aggressive). 2. Dealer upcard heatmap analysis using Matplotlib. 3. Ace handling (soft vs hard hands). 4. Convergence study showing win-rate over 100,000 sims. 5. Save to Firestore."
* **Test Case:** "Compare Win Rate of Dealer 6 vs Dealer Ace; verify Dealer 6 is higher."

**App 6: Backgammon Analyst (`backgammon.py`)**
* **The Prompt:** "@folder Create `backgammon.py`. Include: 1. Dice probability analyzer. 2. Blot vulnerability heatmap. 3. Bearing off probability simulator. 4. Pip count tracker. 5. Opening move analyzer. 6. Save data to Firestore."
* **Test Case:** "Run 10,000 rolls; verify 'Double 6' occurs roughly 2.7% of the time."

---

### **Level 3: The Statistical Lab**

**App 7: Monte Carlo Master (`monte_carlo.py`)**
* **The Prompt:** "@folder Create `monte_carlo.py`. Include: 1. Pi estimation (Circle method). 2. Gambler's Ruin simulation. 3. Stock portfolio risk. 4. Project schedule risk (PERT). 5. Generate Matplotlib histograms and save to Firestore."
* **Test Case:** "Run Pi estimation with 1M points; verify result is 3.14 +/- 0.01."

**App 8: The Bayesian Engine (`bayesian_engine.py`)**
* **The Prompt:** "@folder Create `bayesian_engine.py`. Include: 1. Coin fairness analyzer. 2. A/B Test analyzer. 3. Changepoint detection (trends). 4. Linear regression with uncertainty shading. 5. Save all posteriors to Firestore."
* **Test Case:** "Input 10 heads and 2 tails. Verify the 'fairness' posterior peaks near 0.83."

---

## 🔄 Phase 3: The iPad ➡️ Starlink Workflow

1.  **Retrieval:** In Edge on iPad, go to Firebase Studio and **Import from GitHub**.
2.  **The Token Handshake:** If the iPad blocks the login popup, use the Terminal:
    `git remote set-url origin https://<YOUR_TOKEN>@github.com/<USER>/Cruise-Workbook-2026.git`
3.  **Execution:** Run scripts via the terminal: `python blackjack_pro.py`.
4.  **Visuals:** Matplotlib charts will save as `.png` files in the sidebar. Tap to view your heatmaps.
5.  **Persistence:** Commit and Push regularly. If you lose signal, your work is saved in the cloud; once Starlink reconnects, hit **Sync**.

---

## 🎁 Extra Goodies for the iPad

* **Keyboard Shortcuts:** Use `Cmd + ~` to toggle the terminal quickly.
* **Firestore Viewing:** Keep the Firebase Console open in a second tab to see your data "land" in real-time.
* **Split View:** Keep this `README.md` on the left and your code on the right.



**Ready to roll?** Create the repo on your Mac, push this README, and we can start with **App 1** whenever you're ready. Which one are you tackling first?