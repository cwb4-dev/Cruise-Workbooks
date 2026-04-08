This is the definitive "Ground Zero" guide for your crossing. It treats your technical setup like a high-end home security system: elegant, automated, and fail-safe. 

---

# 🚢 Atlantic Data Lab: Master Operations Manual
**Guiding Principle:** Simple, elegant, couch potato.  
**Connectivity:** Woodbury Fiber ➡️ Starlink Satellite.

---

## 🏛 The Ecosystem: The "Main Vault" Concept
To keep this "minimum friction," you need to visualize where your work actually lives. 

* **GitHub is the "Main Vault":** It’s a secure locker in the cloud. It holds your code, your logs, and your history.
* **The Mac is a "Terminal":** A big-screen way to walk into the vault and move things around while you’re at home.
* **The iPad (Edge) is a "Mobile Terminal":** A portable way to walk into the vault from a lounge chair using Starlink.
* **Working Copy (iPad App) is the "Safe":** A small, physical copy of the vault kept inside your iPad for when the internet (the "bridge" to the vault) goes out.



---

## 💻 Phase 1: Mac Ground Zero (Building the Vault)

### **1. Create the Vault (GitHub)**
* Go to [GitHub](https://github.com/new "Create your Private Repository") and create a **Private** repo named `Cruise-Workbook-2026`.
* **Important:** Go to *Settings > Developer Settings > Tokens (classic)* and generate a Personal Access Token (PAT) with `repo` scopes. Save this in **Google Keep**.

### **2. Launch Firebase Studio (IDX) on Mac**
* Go to [Firebase Studio](https://studio.firebase.google.com "Open your Cloud Workspace").
* **The Handshake:** Open the Terminal at the bottom and link it to the vault:
    `git remote add origin https://github.com/<USER>/Cruise-Workbook-2026.git`

---

## 📂 Phase 2: Mac Builds (Apps 1 & 2)

### **The "Source Control" Secret**
To save your work to the Vault, you must use the **Source Control Icon**.
* **Look:** On the far-left vertical strip, it’s the **third icon down**. It looks like a **stylized "Y" or a tree branch**.
* **Action:** Click it ➡️ Type a message (e.g., "Seed App 1") ➡️ Click **Commit** ➡️ Click **Sync Changes**.

### **The Apps**
* **App 1: Weather Advisor (`/weather.py`)**: Logic for Lido vs. Library.
* **App 2: Utility Kit (`/utils.py`)**: Password generator and USD/Euro converter.

---

## 📱 Phase 3: The Atlantic iPad Pivot (Apps 3-8)

### **1. The iPad Browser (Edge)**
* Open Edge ➡️ [Firebase Studio](https://studio.firebase.google.com).
* **Import:** Select "Import from GitHub" and choose your repo.
* **The Token Fix:** If the iPad won't log in, go to the Terminal and paste:
    `git remote set-url origin https://<YOUR_TOKEN>@github.com/<USER>/Cruise-Workbook-2026.git`

### **2. Building Apps 3 - 8 (The Prompts)**

| App | The Sidebar Prompt | Test Case |
| :--- | :--- | :--- |
| **3. Logger** | "@folder Create `logger.py`. Log to `log.txt` + Bayesian mood predictor + Firestore." | Log 'Great Day'; verify posterior > 0.5. |
| **4. Basic BJ** | "@folder Create `bj_simple.py`. Monte Carlo (1k trials) for bust % on hand of 16." | Hand of 11; verify 0% bust. |
| **5. Pro BJ** | "@folder Create `bj_pro.py`. Strategy comparison + Dealer Heatmap + Firestore." | Compare Dealer 6 vs. Ace win rates. |
| **6. Backgammon** | "@folder Create `backgammon.py`. Pip tracker + Blot heatmap + Firestore." | Verify 'Double 6' is ~2.7% over 10k rolls. |
| **7. Monte Carlo** | "@folder Create `monte_carlo.py`. Pi estimation + Gambler's Ruin + Risk histograms." | Pi with 1M points; verify 3.14. |
| **8. Bayesian** | "@folder Create `bayesian_engine.py`. Coin fairness + A/B test + Firestore." | 10 heads/2 tails; verify peak near 0.83. |

---

## 🛡 Phase 4: The iPad "Insurance Policy" (Working Copy)
If you want to view your code without an internet connection:
1.  Open the **Working Copy** app.
2.  Tap **+** ➡️ **Clone Repository**.
3.  Paste your GitHub URL and use your **Token** as the password.
4.  **The Result:** You now have a physical copy of the "Vault" on your iPad. If Starlink fails, open this app to read your code.

---

## 🚀 The Couch Potato Workflow Summary
1.  **Code** in the Edge Browser (Firebase Studio).
2.  **Save** to the Vault (GitHub) using the **"Y" Branch Icon** in the sidebar.
3.  **Check** your results in **Firestore** on your phone.
4.  **Relax** knowing your work is in the cloud vault and on your iPad's physical drive.



Does this "Main Vault" structure feel more solid? Since we’re at "Ground Zero," would you like to generate the code for **App 1 (Weather)** on your Mac right now to test the "Y" Branch sync?
