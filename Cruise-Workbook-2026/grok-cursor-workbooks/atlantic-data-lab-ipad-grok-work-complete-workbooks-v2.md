# 🚢 Atlantic Data Lab — Complete Vibe Coding Workbooks v2
**MSC Meraviglia 2026 Edition**

**iPad + Blink + Working Copy + Mosh + DigitalOcean Setup Guide**

A single, self-contained guide for building your cruise apps using **iPad-only workflow** with remote Droplet.

---

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

## 🛠️ Full iPad Setup Guide (Blink + Working Copy + Mosh)

### 1. DigitalOcean Droplet Setup (One-time)

1. Go to [DigitalOcean.com](https://cloud.digitalocean.com) in **Edge browser** on iPad.
2. Create a new **Droplet**:
   - **Region**: Closest to you (e.g. NYC or Toronto)
   - **Image**: Ubuntu 24.04 LTS
   - **Size**: Basic ($6/mo) — 1 vCPU / 1GB RAM is enough
   - **Authentication**: Add your SSH key (see below)
   - Enable **Backups** if desired
3. After creation, note the Droplet IP address.

#### Generate SSH Key on iPad (if you don't have one)
- Open **Blink** app
- Run: `ssh-keygen -t ed25519 -C "your-email@example.com"`
- Press Enter for default location and no passphrase (or set one)

#### Add SSH Key to Droplet
- Copy public key: `cat ~/.ssh/id_ed25519.pub` in Blink
- Paste it in DigitalOcean Droplet creation or Settings → Security

### 2. Install & Configure Blink (SSH + Mosh)

**Blink** is your main terminal.

1. Open **Blink** on iPad.
2. Add Host:
   - Host: Your Droplet IP
   - User: `root` (or the user you created)
   - Port: 22
   - Key: Select your SSH key
3. **Enable Mosh** (recommended for iPad — survives sleep/background):
   - In Blink settings → Install Mosh if prompted (Blink includes it)
   - Connect with Mosh: `mosh user@droplet-ip`

**Mosh Tips**:
- Much better than SSH on mobile — reconnects automatically
- `mosh --predict=always user@ip` for faster typing feel

### 3. Git Setup with Working Copy

**Working Copy** is your Git client on iPad.

1. Open **Working Copy** app.
2. Clone your repo:
   - Add Repository → Clone → Enter GitHub URL (`git@github.com:yourusername/atlantic-data-lab.git`)
   - Use SSH key (Working Copy supports iCloud Keychain / Blink keys)
3. Grant Working Copy access to iCloud Drive if needed.

**Workflow**:
- Edit Markdown files and configs in Working Copy (great for iPad text editing)
- Commit & push directly from Working Copy
- For code: Pull → edit on Droplet via Blink → commit via Working Copy or CLI

### 4. Connect Everything

**Recommended Daily Workflow**:

1. Open **Edge** → GitHub (for issues, PRs, viewing code)
2. Open **Working Copy** → Pull latest changes
3. Open **Blink** → `mosh user@droplet-ip`
4. On Droplet:
   ```bash
   cd atlantic-data-lab
   source venv/bin/activate
   ```
5. Vibe code with Grok (in this chat) or Cursor (if using another device)

### 5. Initial Droplet Configuration (Run once via Blink/Mosh)

```bash
# Update system
apt update && apt upgrade -y

# Install essentials
apt install python3 python3-venv python3-pip git mosh curl -y

# Clone repo
git clone https://github.com/yourusername/atlantic-data-lab.git
cd atlantic-data-lab

# Setup virtual env
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Make venv activation easy
echo "source ~/atlantic-data-lab/venv/bin/activate" >> ~/.bashrc
```

### 6. Shared Project Files

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

**pyproject.toml**
```toml
[project]
name = "atlantic-data-lab"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["requests", "pandas", "numpy", "matplotlib", "scipy", "rich"]
```

**.gitignore**
```
__pycache__/
venv/
*.pyc
.DS_Store
.env
```

### 7. Cursor vs Grok Build on iPad

- **Grok Build** (this chat): Best for iPad — describe vibe here → I generate code → paste into Blink
- **Cursor**: Harder on pure iPad (use web version or another device for Cursor)

**Grok Build Prompts** are in the Grok Workbook section below.

---

## 📘 Cursor Workbook (For when you have a Mac/PC)

(Full details in v1 — use when available)

---

## 📗 Grok Build Workbook (Perfect for iPad)

**Workflow**: Talk to Grok → I give full code → Paste into file via Blink → Test → Iterate.

**Example for utils.py**:
> "Build the full Utility Kit in Essentials/utils.py ..."

(Ready prompts for all apps available on request)

---

**Version**: v2 — Added full iPad + Mosh guide  
**Last updated**: June 2026

Happy coding from the high seas! 🌊🚢
