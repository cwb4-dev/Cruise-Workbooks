# Digital Ocean Droplet Setup Guide

## Complete Guide to Running Game Theory Workbook on Digital Ocean

---

## 📋 Prerequisites

Before starting, you'll need:
- A Digital Ocean account (sign up at [digitalocean.com](https://digitalocean.com))
- A payment method on file (credit card or PayPal)
- Basic familiarity with terminal/command line
- SSH client installed on your local machine

---

## 🚀 Step 1: Create a Digital Ocean Droplet

### Via Digital Ocean Dashboard

1. **Log in** to your Digital Ocean account

2. **Click "Create"** → **"Droplets"**

3. **Choose an Image**:
   - Select **"Ubuntu"** (latest LTS version, e.g., Ubuntu 22.04 LTS)
   - This is the most stable and well-documented option

4. **Choose a Plan**:
   - **Basic** plan is sufficient for this workbook
   - **Recommended**: $6/month (1 GB RAM, 1 vCPU) or $12/month (2 GB RAM, 1 vCPU)
   - The $6 plan works fine for simulations up to 10,000 agents

5. **Choose a Datacenter Region**:
   - Pick the region closest to you for lower latency
   - Options: NYC, SFO, LON, FRA, SGP, etc.

6. **Select Authentication Method**:
   - **Option A (Recommended)**: SSH Keys
     - Click "New SSH Key"
     - Copy your public key from `~/.ssh/id_rsa.pub` on your local machine
     - Paste it in the box
   - **Option B**: Password (less secure)
     - Set a strong password
     - You'll need it to log in

7. **Additional Options**:
   - Enable **Monitoring** (checkbox)
   - Enable **Backups** (optional, costs extra)
   - Choose a hostname (e.g., `game-theory-workbook`)

8. **Click "Create Droplet"**

### Generate SSH Key (if you don't have one)

```bash
# On your local machine (Mac/Linux)
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Follow prompts (press Enter for defaults)
# Your public key will be at: ~/.ssh/id_rsa.pub
# Your private key will be at: ~/.ssh/id_rsa

# View your public key to copy it
cat ~/.ssh/id_rsa.pub
```

---

## 🔌 Step 2: Connect to Your Droplet

### Get Your Droplet's IP Address

1. Go to your Digital Ocean dashboard
2. Click on your droplet
3. Copy the **IPv4 address** (e.g., `164.90.200.100`)

### SSH Into Your Droplet

```bash
# Connect to your droplet (replace with your IP)
ssh root@164.90.200.100

# If you set a password instead of SSH key, you'll be prompted for it
# If using SSH key, you should connect automatically
```

### If SSH Key Doesn't Work

```bash
# Make sure your SSH key is added
ssh-add ~/.ssh/id_rsa

# Or use password authentication
ssh -o PreferredAuthentications=password root@164.90.200.100
```

---

## 🛠️ Step 3: Initial Server Setup

Once connected via SSH, run these commands:

```bash
# Update system packages
apt update && apt upgrade -y

# Install essential tools
apt install -y git curl wget vim nano tmux htop

# Install Python and development tools
apt install -y python3 python3-pip python3-venv python3-dev

# Install build tools (needed for some Python packages)
apt install -y build-essential libssl-dev libffi-dev

# Install additional useful tools
apt install -y tree unzip
```

---

## 📁 Step 4: Install the Workbook

### Option A: Clone from GitHub (Recommended)

```bash
# Install git (if not already installed)
apt install -y git

# Navigate to home directory
cd ~

# Clone the repository (replace with your repository URL)
git clone https://github.com/yourusername/game-theory-workbook.git

# Navigate into the directory
cd game-theory-workbook

# List contents to verify
ls -la
```

### Option B: Create from Scratch (Manual Setup)

If you don't have a GitHub repo yet:

```bash
# Create project directory
mkdir -p ~/game-theory-workbook
cd ~/game-theory-workbook

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Create requirements.txt (see below for content)
nano requirements.txt

# Create the Python files (see code sections below)
nano workbook.py
nano strategies.py
nano cli.py
```

---

## 🔧 Step 5: Set Up Virtual Environment

```bash
# Make sure you're in the project directory
cd ~/game-theory-workbook

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) at the beginning of your prompt
# Example: (venv) root@droplet:~$
```

### Install Dependencies

Create `requirements.txt`:

```bash
nano requirements.txt
```

Paste the following:

```txt
numpy==1.24.3
pandas==2.0.3
matplotlib==3.7.2
seaborn==0.12.2
jupyter==1.0.0
ipython==8.14.0
plotly==5.15.0
scipy==1.10.1
rich==13.5.2
click==8.1.7
pytest==7.4.0
pytest-cov==4.1.0
black==23.7.0
```

Save and exit (in nano: `Ctrl+O`, `Enter`, `Ctrl+X`)

Then install:

```bash
# Install all dependencies
pip install -r requirements.txt

# Verify installations
pip list
```

---

## 📝 Step 6: Create Core Python Files

If you're not using a pre-made repository, create these files:

### File 1: workbook.py

```bash
nano workbook.py
```

Paste the core functions (see below for the complete code):

```python
#!/usr/bin/env python3
"""
Game Theory Workbook - Core Functions
"""

def prisoners_dilemma(my_choice, their_choice):
    """Simulate one round of the Prisoner's Dilemma"""
    if my_choice == 'cooperate' and their_choice == 'cooperate':
        return (1, 1)
    elif my_choice == 'defect' and their_choice == 'defect':
        return (3, 3)
    elif my_choice == 'cooperate' and their_choice == 'defect':
        return (5, 0)
    elif my_choice == 'defect' and their_choice == 'cooperate':
        return (0, 5)

def tit_for_tat(opponent_last_move):
    """Tit for Tat strategy"""
    if opponent_last_move is None:
        return 'cooperate'
    else:
        return opponent_last_move

def simulate_cascade(thresholds, max_rounds=100):
    """Simulate a social cascade"""
    sorted_thresholds = sorted(thresholds)
    joined = 0
    history = [0]
    
    for round_num in range(max_rounds):
        newly_joined = 0
        for threshold in sorted_thresholds:
            if joined >= threshold:
                newly_joined += 1
        
        joined += newly_joined
        history.append(joined)
        
        if newly_joined == 0:
            break
    
    return history

def asshole_threshold(cooperators, defectors):
    """Calculate asshole threshold status"""
    total = cooperators + defectors
    if total == 0:
        return "EMPTY: No population"
    
    defector_ratio = defectors / total
    
    if defector_ratio < 0.2:
        return "SAFE: Society is healthy"
    elif defector_ratio < 0.35:
        return "WARNING: Approaching threshold"
    elif defector_ratio < 0.5:
        return "CRITICAL: Threshold crossed, system deteriorating"
    else:
        return "COLLAPSED: Society is dysfunctional"

# Main function
def main():
    print("Game Theory Workbook")
    print("=" * 40)
    print("Available functions:")
    print("  - prisoners_dilemma(cooperate/defect, cooperate/defect)")
    print("  - tit_for_tat(opponent_last_move)")
    print("  - simulate_cascade(thresholds)")
    print("  - asshole_threshold(cooperators, defectors)")
    print()
    
    # Demo
    print("Demo: Prisoner's Dilemma")
    result = prisoners_dilemma('defect', 'defect')
    print(f"Both defect: {result}")
    
    print("\nDemo: Asshole Threshold")
    status = asshole_threshold(700, 300)
    print(f"Status: {status}")

if __name__ == "__main__":
    main()
```

### File 2: strategies.py

```bash
nano strategies.py
```

```python
#!/usr/bin/env python3
"""
Game Theory Strategies
"""

import random

def tit_for_tat(opponent_last_move):
    """Start cooperative, then mirror opponent"""
    return 'cooperate' if opponent_last_move is None else opponent_last_move

def always_defect(opponent_last_move):
    """Never cooperate, always betray"""
    return 'defect'

def always_cooperate(opponent_last_move):
    """Never betray, always cooperate (the sucker)"""
    return 'cooperate'

def grudge(opponent_last_move):
    """Cooperate until opponent defects once, then defect forever"""
    if not hasattr(grudge, 'cheated'):
        grudge.cheated = False
    
    if opponent_last_move == 'defect':
        grudge.cheated = True
    
    return 'cooperate' if not grudge.cheated else 'defect'

def random_strategy(opponent_last_move):
    """Randomly choose cooperate or defect"""
    return random.choice(['cooperate', 'defect'])

def play_tournament(strategies, rounds=100):
    """Run a tournament where all strategies play each other"""
    results = {}
    
    for name_a, strategy_a in strategies.items():
        for name_b, strategy_b in strategies.items():
            if name_a == name_b:
                continue
                
            score_a = 0
            score_b = 0
            last_a = None
            last_b = None
            
            for _ in range(rounds):
                move_a = strategy_a(last_b)
                move_b = strategy_b(last_a)
                
                # Calculate payoff
                if move_a == 'cooperate' and move_b == 'cooperate':
                    score_a += 1
                    score_b += 1
                elif move_a == 'defect' and move_b == 'defect':
                    score_a += 0
                    score_b += 0
                elif move_a == 'cooperate' and move_b == 'defect':
                    score_a += 0
                    score_b += 3
                elif move_a == 'defect' and move_b == 'cooperate':
                    score_a += 3
                    score_b += 0
                
                last_a = move_a
                last_b = move_b
            
            results[(name_a, name_b)] = (score_a, score_b)
    
    return results

def main():
    """Run a tournament demo"""
    strategies = {
        'Tit for Tat': tit_for_tat,
        'Always Defect': always_defect,
        'Always Cooperate': always_cooperate,
        'Grudge': grudge,
        'Random': random_strategy
    }
    
    print("Running Tournament...")
    results = play_tournament(strategies)
    
    # Calculate average scores
    scores = {name: 0 for name in strategies}
    counts = {name: 0 for name in strategies}
    
    for (a, b), (score_a, score_b) in results.items():
        scores[a] += score_a
        scores[b] += score_b
        counts[a] += 1
        counts[b] += 1
    
    print("\nTournament Results (Average Score per Game):")
    print("=" * 45)
    for name in strategies:
        avg = scores[name] / counts[name]
        print(f"{name:>15}: {avg:>5.2f}")

if __name__ == "__main__":
    main()
```

### File 3: cli.py (Command Line Interface)

```bash
nano cli.py
```

```python
#!/usr/bin/env python3
"""
Game Theory Workbook - Command Line Interface
"""

import click
from workbook import prisoners_dilemma, asshole_threshold
from strategies import play_tournament, tit_for_tat, always_defect, always_cooperate, grudge, random_strategy

@click.group()
def cli():
    """Game Theory Workbook CLI"""
    pass

@cli.command()
@click.option('--rounds', default=100, help='Number of rounds')
def tournament(rounds):
    """Run a tournament of strategies"""
    strategies = {
        'Tit for Tat': tit_for_tat,
        'Always Defect': always_defect,
        'Always Cooperate': always_cooperate,
        'Grudge': grudge,
        'Random': random_strategy
    }
    
    click.echo("Running Tournament...")
    results = play_tournament(strategies, rounds=rounds)
    
    # Calculate average scores
    scores = {name: 0 for name in strategies}
    counts = {name: 0 for name in strategies}
    
    for (a, b), (score_a, score_b) in results.items():
        scores[a] += score_a
        scores[b] += score_b
        counts[a] += 1
        counts[b] += 1
    
    click.echo("\nTournament Results:")
    click.echo("=" * 45)
    for name in strategies:
        avg = scores[name] / counts[name]
        click.echo(f"{name:>15}: {avg:>5.2f}")

@cli.command()
@click.option('--cooperators', default=700, help='Number of cooperators')
@click.option('--defectors', default=300, help='Number of defectors')
def threshold(cooperators, defectors):
    """Calculate asshole threshold status"""
    status = asshole_threshold(cooperators, defectors)
    click.echo(f"Population: {cooperators + defectors}")
    click.echo(f"Defector Rate: {defectors/(cooperators+defectors)*100:.1f}%")
    click.echo(f"Status: {status}")

@cli.command()
@click.option('--my-choice', default='cooperate', help='My choice')
@click.option('--their-choice', default='cooperate', help='Their choice')
def pd(my_choice, their_choice):
    """Run Prisoner's Dilemma"""
    result = prisoners_dilemma(my_choice, their_choice)
    click.echo(f"Result: You get {result[0]} years, They get {result[1]} years")

if __name__ == "__main__":
    cli()
```

---

## 🧪 Step 7: Test the Setup

### Test 1: Basic Python

```bash
# Make sure you're in the project directory and venv is activated
cd ~/game-theory-workbook
source venv/bin/activate

# Test Python version
python3 --version  # Should show 3.8 or higher

# Test imports
python3 -c "import numpy; import pandas; print('Imports successful')"
```

### Test 2: Run the Workbook

```bash
# Run the main workbook
python3 workbook.py

# Should show:
# Game Theory Workbook
# ========================================
# Available functions:
#   - prisoners_dilemma(...)
#   - tit_for_tat(...)
#   - simulate_cascade(...)
#   - asshole_threshold(...)
```

### Test 3: Run Strategies

```bash
# Run strategies module
python3 strategies.py

# Should show tournament results
```

### Test 4: Run CLI

```bash
# Run CLI with help
python3 cli.py --help

# Run tournament
python3 cli.py tournament --rounds 200

# Check threshold
python3 cli.py threshold --cooperators 600 --defectors 400

# Run Prisoner's Dilemma
python3 cli.py pd --my-choice defect --their-choice cooperate
```

---

## 🌐 Step 8: Set Up Jupyter Notebook (Optional)

For interactive development:

```bash
# Make sure venv is activated
source venv/bin/activate

# Install Jupyter
pip install jupyter

# Start Jupyter (on port 8888)
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser

# You'll see a URL like: http://127.0.0.1:8888/?token=...
```

### Access Jupyter from Your Browser

**Option A: SSH Tunneling (Recommended)**

On your local machine (in a new terminal window):

```bash
# Replace with your droplet IP and the token from the Jupyter output
ssh -L 8888:localhost:8888 root@164.90.200.100

# Then open in browser: http://localhost:8888
```

**Option B: Public Access (Less Secure)**

```bash
# Start Jupyter with password (not recommended for production)
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root

# Access at: http://164.90.200.100:8888
```

---

## 📊 Step 9: Run Simulations

### Basic Simulations

```bash
# Run a large social simulation
python3 -c "
from workbook import simulate_cascade
import random

# Create thresholds for 10,000 people
thresholds = [random.randint(0, 100) for _ in range(10000)]
history = simulate_cascade(thresholds)
print(f'Peak participation: {history[-1]}')
"

# Run multiple scenarios
python3 -c "
from workbook import asshole_threshold

# Test different scenarios
scenarios = [
    (900, 100),   # 10% defectors
    (700, 300),   # 30% defectors
    (500, 500),   # 50% defectors
    (300, 700),   # 70% defectors
]

for coops, defs in scenarios:
    status = asshole_threshold(coops, defs)
    print(f'{coops+defs} pop, {defs/(coops+defs)*100:.1f}% defectors: {status}')
"
```

### Advanced Simulations with Visualization

```python
# Create a script for advanced analysis
nano analysis.py
```

```python
#!/usr/bin/env python3
"""
Advanced Game Theory Analysis
"""

import random
import matplotlib.pyplot as plt
from workbook import simulate_cascade, asshole_threshold

def run_analysis():
    """Run comprehensive analysis"""
    print("Running Advanced Analysis...")
    print("=" * 50)
    
    # 1. Threshold analysis
    print("\n1. Social Cascade Analysis")
    thresholds = [random.randint(0, 100) for _ in range(1000)]
    history = simulate_cascade(thresholds)
    print(f"Final participation: {history[-1]}")
    
    # 2. Asshole threshold analysis
    print("\n2. Asshole Threshold Analysis")
    for defector_pct in [10, 20, 30, 40, 50, 60, 70]:
        coops = 1000 - (1000 * defector_pct // 100)
        defs = 1000 - coops
        status = asshole_threshold(coops, defs)
        print(f"  {defector_pct}% defectors: {status}")
    
    # 3. Create visualization
    print("\n3. Generating visualization...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Plot cascade
    ax1.plot(history)
    ax1.set_title('Social Cascade Over Time')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Participants')
    
    # Plot threshold analysis
    defector_rates = [10, 20, 30, 40, 50, 60, 70]
    statuses = []
    for pct in defector_rates:
        coops = 1000 - (1000 * pct // 100)
        defs = 1000 - coops
        status = asshole_threshold(coops, defs)
        # Convert status to numerical value for plotting
        status_map = {
            'SAFE: Society is healthy': 0,
            'WARNING: Approaching threshold': 1,
            'CRITICAL: Threshold crossed, system deteriorating': 2,
            'COLLAPSED: Society is dysfunctional': 3
        }
        statuses.append(status_map[status])
    
    ax2.plot(defector_rates, statuses, 'ro-')
    ax2.set_title('Asshole Threshold by Defector Rate')
    ax2.set_xlabel('Defector Percentage (%)')
    ax2.set_ylabel('Risk Level (0=Safe, 3=Collapsed)')
    ax2.set_yticks([0, 1, 2, 3])
    ax2.set_yticklabels(['Safe', 'Warning', 'Critical', 'Collapsed'])
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('analysis.png')
    print("Saved visualization to 'analysis.png'")

if __name__ == "__main__":
    run_analysis()
```

Run it:

```bash
python3 analysis.py
```

---

## 🔐 Step 10: Security Considerations

### Disable Root Login (Recommended)

```bash
# Create a new user
adduser username  # Replace with your username

# Add user to sudo group
usermod -aG sudo username

# Switch to new user
su - username

# Copy your SSH key to the new user
mkdir -p ~/.ssh
cat /root/.ssh/authorized_keys >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys

# Exit back to root
exit

# Edit SSH config
nano /etc/ssh/sshd_config

# Find and change these lines:
# PermitRootLogin no
# PasswordAuthentication no

# Restart SSH
systemctl restart sshd
```

### Set Up Firewall

```bash
# Install UFW
apt install -y ufw

# Allow SSH
ufw allow 22

# Allow HTTP/HTTPS (if needed)
ufw allow 80
ufw allow 443

# Allow Jupyter (if using)
ufw allow 8888

# Enable firewall
ufw enable

# Check status
ufw status
```

---

## 📁 Step 11: Complete Project Structure

Your droplet should now have:

```
~/game-theory-workbook/
├── venv/                      # Virtual environment
├── requirements.txt           # Python dependencies
├── workbook.py               # Core functions
├── strategies.py             # Game theory strategies
├── cli.py                    # Command line interface
├── analysis.py               # Advanced analysis
├── analysis.png              # Generated visualization
├── notebooks/                # (Optional) Jupyter notebooks
│   └── analysis.ipynb
└── data/                     # (Optional) Data files
    └── results.csv
```

---

## 🧪 Step 12: Run the Full Test Suite

```bash
# Create test file
nano test_workbook.py
```

```python
#!/usr/bin/env python3
"""
Test Suite for Game Theory Workbook
"""

import unittest
from workbook import prisoners_dilemma, tit_for_tat, simulate_cascade, asshole_threshold

class TestPrisonersDilemma(unittest.TestCase):
    def test_cooperate_cooperate(self):
        result = prisoners_dilemma('cooperate', 'cooperate')
        self.assertEqual(result, (1, 1))
    
    def test_defect_defect(self):
        result = prisoners_dilemma('defect', 'defect')
        self.assertEqual(result, (3, 3))
    
    def test_cooperate_defect(self):
        result = prisoners_dilemma('cooperate', 'defect')
        self.assertEqual(result, (5, 0))
    
    def test_defect_cooperate(self):
        result = prisoners_dilemma('defect', 'cooperate')
        self.assertEqual(result, (0, 5))

class TestTitForTat(unittest.TestCase):
    def test_first_move(self):
        result = tit_for_tat(None)
        self.assertEqual(result, 'cooperate')
    
    def test_mirror_cooperate(self):
        result = tit_for_tat('cooperate')
        self.assertEqual(result, 'cooperate')
    
    def test_mirror_defect(self):
        result = tit_for_tat('defect')
        self.assertEqual(result, 'defect')

class TestAssholeThreshold(unittest.TestCase):
    def test_safe(self):
        status = asshole_threshold(800, 200)
        self.assertIn('SAFE', status)
    
    def test_warning(self):
        status = asshole_threshold(700, 300)
        self.assertIn('WARNING', status)
    
    def test_critical(self):
        status = asshole_threshold(550, 450)
        self.assertIn('CRITICAL', status)
    
    def test_collapsed(self):
        status = asshole_threshold(300, 700)
        self.assertIn('COLLAPSED', status)

if __name__ == "__main__":
    unittest.main()
```

Run tests:

```bash
python3 test_workbook.py -v

# Should show all tests passing
```

---

## 📈 Step 13: Monitor Performance

### View System Resources

```bash
# Check memory usage
free -h

# Check CPU usage
top

# Check disk space
df -h

# Check running processes
ps aux

# Use htop (better than top)
htop
```

### Monitor Python Processes

```bash
# Find Python processes
ps aux | grep python

# Kill a Python process (replace PID with actual process ID)
kill -9 PID
```

---

## 🚨 Step 14: Troubleshooting

### Common Issues

**1. Python Version Issues**

```bash
# Check Python version
python3 --version

# If Python 3.8+ is not installed:
apt install -y python3.11
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
```

**2. Permission Issues**

```bash
# Fix permissions for the project
chown -R username:username ~/game-theory-workbook
chmod -R 755 ~/game-theory-workbook
```

**3. Virtual Environment Issues**

```bash
# Recreate virtual environment
cd ~/game-theory-workbook
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**4. Memory Issues**

```bash
# For large simulations, increase swap space
dd if=/dev/zero of=/swapfile bs=1M count=2048  # 2GB swap
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

**5. Package Installation Issues**

```bash
# Install missing system dependencies
apt install -y build-essential python3-dev libssl-dev libffi-dev
```

---

## 💾 Step 15: Backup and Save

### Save Your Work

```bash
# Create a backup script
nano backup.sh
```

```bash
#!/bin/bash
# Backup script for game theory workbook

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/root/backups"

mkdir -p $BACKUP_DIR
cd ~/game-theory-workbook
tar -czf $BACKUP_DIR/workbook_$TIMESTAMP.tar.gz .
echo "Backup created: $BACKUP_DIR/workbook_$TIMESTAMP.tar.gz"
```

Make it executable:

```bash
chmod +x backup.sh
./backup.sh
```

### Push Changes to GitHub

```bash
# Add your changes
git add .
git commit -m "Update workbook and analysis"

# Push to GitHub
git push origin main
```

---

## 🎯 Step 16: Quick Command Reference

```bash
# Connect to droplet
ssh root@164.90.200.100

# Activate virtual environment
cd ~/game-theory-workbook && source venv/bin/activate

# Run workbook
python3 workbook.py

# Run tournament
python3 cli.py tournament

# Check threshold
python3 cli.py threshold --cooperators 600 --defectors 400

# Run tests
python3 test_workbook.py -v

# Start Jupyter
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser

# SSH tunneling (on local machine)
ssh -L 8888:localhost:8888 root@164.90.200.100
```

---

## ✅ Checklist: Complete Setup

| Step | Task | Status |
|------|------|--------|
| 1 | Create Digital Ocean droplet | ☐ |
| 2 | SSH into droplet | ☐ |
| 3 | Update system packages | ☐ |
| 4 | Install Python and tools | ☐ |
| 5 | Clone or create repository | ☐ |
| 6 | Set up virtual environment | ☐ |
| 7 | Install dependencies | ☐ |
| 8 | Create core Python files | ☐ |
| 9 | Test basic functions | ☐ |
| 10 | Run simulations | ☐ |
| 11 | Set up Jupyter (optional) | ☐ |
| 12 | Configure security | ☐ |
| 13 | Run test suite | ☐ |
| 14 | Backup work | ☐ |

---

## 🎉 You're Ready!

Your Digital Ocean droplet is now fully set up to run the Game Theory Workbook. You can:

1. **Run simulations** interactively in Python
2. **Use the CLI** for quick experiments
3. **Launch Jupyter** for detailed analysis
4. **Create visualizations** of results
5. **Push changes** to GitHub
6. **Share access** with collaborators

### Next Steps

1. **Explore the modules**: Try different parameters in each simulation
2. **Modify the code**: Experiment with new strategies or models
3. **Create visualizations**: Generate plots of your results
4. **Share your findings**: Publish your analysis
5. **Extend the workbook**: Add new game theory concepts

---

**Happy analyzing!** 🚀📊🎮

---

## 📚 Appendix: Complete File Contents

### requirements.txt

```txt
numpy==1.24.3
pandas==2.0.3
matplotlib==3.7.2
seaborn==0.12.2
jupyter==1.0.0
ipython==8.14.0
plotly==5.15.0
scipy==1.10.1
rich==13.5.2
click==8.1.7
pytest==7.4.0
pytest-cov==4.1.0
black==23.7.0
```

### Make All Scripts Executable

```bash
chmod +x workbook.py strategies.py cli.py analysis.py test_workbook.py
```

### One-Liner to Set Up Everything

Create a setup script:

```bash
nano setup.sh
```

```bash
#!/bin/bash
# Complete setup script for Game Theory Workbook

echo "Setting up Game Theory Workbook..."

# Update system
apt update && apt upgrade -y

# Install dependencies
apt install -y python3 python3-pip python3-venv git build-essential

# Clone repo (or create directory)
mkdir -p ~/game-theory-workbook
cd ~/game-theory-workbook

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

echo "Setup complete!"
echo "Activate virtual environment: source venv/bin/activate"
```

Run it:

```bash
chmod +x setup.sh
./setup.sh
```

---

**That's it! Your Digital Ocean droplet is ready to run the Game Theory Workbook.**