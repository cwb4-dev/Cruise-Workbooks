# 🚢 Atlantic Data Lab — Cursor + Mac + Warp + Droplet Workbook v1.0

**Complete Step-by-Step Guide for Cursor on Mac**  
**MSC Meraviglia 2026**

This is a **dedicated Cursor-focused workbook** for when you're on your Mac using:
- **Cursor** (AI code editor)
- **Warp** (modern terminal)
- **Edge** browser
- **DigitalOcean Droplet** (remote compute)

---

## 1. Hardware & Software Stack

| Tool          | Purpose                              | Where Used          |
|---------------|--------------------------------------|---------------------|
| Cursor        | Main AI coding environment           | Mac                 |
| Warp          | Terminal + SSH to Droplet            | Mac                 |
| Edge          | GitHub, DigitalOcean dashboard       | Mac                 |
| DigitalOcean Droplet | Remote Python environment       | Cloud               |
| Git           | Version control                      | Mac + Droplet       |

---

## 2. One-Time Setup

### Step 1: Create DigitalOcean Droplet (if not already done)

1. Open **Edge** → go to [cloud.digitalocean.com](https://cloud.digitalocean.com)
2. Create Droplet:
   - **Image**: Ubuntu 24.04 LTS
   - **Size**: Basic ($6–12/mo is plenty)
   - **Authentication**: Add your SSH key from Mac
3. Note the Droplet IP address.

### Step 2: SSH Key Setup on Mac

```bash
# In Warp terminal on Mac
ssh-keygen -t ed25519 -C "your-email@example.com"
cat ~/.ssh/id_ed25519.pub
```

Copy the output and add it to DigitalOcean (Security → SSH Keys).

### Step 3: Connect to Droplet from Mac (Warp)

Open **Warp** and run:

```bash
ssh root@YOUR_DROPLET_IP
```

Or use Mosh for better experience:

```bash
mosh root@YOUR_DROPLET_IP
```

### Step 4: Initial Droplet Configuration

Run these commands on the Droplet:

```bash
apt update && apt upgrade -y
apt install python3 python3-venv python3-pip git curl -y

# Clone repo
git clone https://github.com/YOURUSERNAME/atlantic-data-lab.git
cd atlantic-data-lab

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 3. Project Structure (Same as before)

```
atlantic-data-lab/
├── README.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── .cursor/
│   └── rules/
│       └── atlantic-lab.mdc
├── Essentials/
├── Analytics/
└── Lab/
```

---

## 4. Cursor Setup on Mac

### Step 1: Install Cursor
Download from [cursor.com](https://cursor.com) and install on your Mac.

### Step 2: Open the Project
1. Open **Cursor**
2. `File → Open Folder` → select your `atlantic-data-lab` folder

### Step 3: Add API Keys in Cursor
Go to **Cursor Settings → Models** and add:
- **Claude** (Sonnet 4 / Opus 4) ← Recommended primary
- **Grok** (xAI)
- **Gemini**

### Step 4: Create Cursor Rules

Create file: `.cursor/rules/atlantic-lab.mdc`

Paste this:

```markdown
# Atlantic Data Lab Cursor Rules

You are helping build fun, educational Python apps for a cruise ship data lab.

Guidelines:
- Use `rich` for beautiful terminal output
- Add cruise-themed comments and light ASCII art
- Prioritize clarity and educational value
- Use numpy/pandas/matplotlib for analytics
- Keep scripts runnable standalone with `if __name__ == "__main__":`
- Make output fun and engaging
```

### Step 5: Recommended Cursor Settings
- **Composer** = Primary way to build
- **Inline Chat** (Cmd+K) for quick edits
- Set **Claude Sonnet** as default for most tasks

---

## 5. Git Workflow (Mac + Cursor)

**Recommended Flow**:

1. **On Mac (Cursor / Warp)**: Edit code
2. **Commit & Push** from Warp or Cursor's built-in Git
3. **Pull on Droplet** when you want to run/test:
   ```bash
   cd atlantic-data-lab
   git pull
   source venv/bin/activate
   python Essentials/utils.py
   ```

---

## 6. Vibe Coding Workflow in Cursor

### Best Way to Build Apps

1. Open the target file (e.g. `Essentials/utils.py`)
2. Press **Cmd + K** (Composer)
3. Use high-level prompts like:

**General Template**:
```
Build [App Name] based on the description in app_tracker.md.

Requirements:
- Use rich for terminal output
- Cruise-themed and fun
- Good comments and docstrings
- Make it self-contained
```

### Example Prompts for Each App

**Utility Kit (`utils.py`)**
```
Build the Utility Kit:
- Password generator with options
- Real-time USD to EUR converter
- Beautiful rich menu interface
- Cruise ship theme
```

**Activity Logger (`logger.py`)**
```
Create Activity Logger with daily logging and simple Bayesian mood estimation.
Save data to JSON. Show nice summaries with rich.
```

**Basic Blackjack (`bj_simple.py`)**
```
Implement Basic Blackjack bust probability calculator.
Input hand total → show bust probability on hit.
Make it educational and fun.
```

**Pro Blackjack (`bj_pro.py`)**
```
Build Pro Blackjack analyzer:
- Generate full Stand vs Hit heatmap
- Use numpy + matplotlib
- Save chart as PNG
- Add rich terminal summary
```

**Backgammon, Monte Carlo Lab, Bayesian Engine** — same pattern.

---

## 7. Testing on Droplet

After pushing changes from Cursor:

On Droplet (via Warp):

```bash
cd atlantic-data-lab
git pull
source venv/bin/activate

# Example
python Essentials/utils.py
```

---

## 8. Recommended Daily Workflow

1. **Morning / Planning** — Open Edge → GitHub
2. **Coding** — Open Cursor → work on apps using Composer
3. **Testing** — Switch to Warp → SSH/Mosh into Droplet → run code
4. **Commit** — Use Cursor Git or Warp to push

---

**This workbook is now ready for your Mac + Cursor workflow.**

**Next?**  
Download this file, set up Cursor on your Mac, then tell me:

**"Build utils.py with Cursor prompts"**  
or just  
**"Start with Utility Kit"**

I’ll give you detailed Cursor-specific prompts + code.

Would you like me to expand this workbook with **full starter code templates** for all 7 remaining apps? Just say the word. 🚢

*Version 1.0 — June 2026*
