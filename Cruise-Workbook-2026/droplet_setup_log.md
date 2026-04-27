# DigitalOcean Droplet Setup Log

**Atlantic Data Lab -- MSC Meraviglia 2026**
**Version 2**

-----

## Droplet Details

|Item          |Value                  |
|--------------|-----------------------|
|Provider      |DigitalOcean           |
|OS            |Ubuntu 24.04 LTS       |
|Plan          |Basic $4/mo            |
|Sign-on Credit|$200 (≈ 50 months free)|
|IP Address    |147.182.190.94         |
|Created       |*(paste date here)*    |
|Region        |*(paste region here)*  |

-----

## Blink Shell Host Config

|Setting |Value              |
|--------|-------------------|
|Label   |AI-Server          |
|Hostname|*(your Droplet IP)*|
|User    |root               |
|Mosh    |ON                 |

Connect with:

```bash
mosh AI-Server
```

-----

## Setup Steps Completed

### Step 1 -- System Update ✅

```bash
apt update && apt upgrade -y
```

- Ran on first login
- Config file prompts → answered `N` (keep local) for all
- Fresh Droplet, all configs are stock Ubuntu defaults -- nothing to protect

### Step 2 -- Install Python ✅

```bash
apt install -y python3-pip
python3 --version
```

- Installed cleanly, no issues
- **Result:** Python 3.12.3 ✓

### Step 3 -- Install Claude Code ✅

```bash
# First attempt failed -- Droplet only has 458MB RAM, no swap
# Fix: add 1GB swap file before installing
fallocate -l 1G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab   # permanent across reboots

# Then install succeeded
curl -fsSL https://claude.ai/install.sh | bash

# Installer flagged PATH issue -- fix with:
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc

claude --version
```

- **Gotcha:** $4/mo Droplet (458MB RAM, no swap) kills the installer -- always add swap first
- **Gotcha:** `~/.local/bin` not in PATH by default -- must add manually as above
- **Result:** Claude Code 2.1.119 ✓ (above 2.1.51 minimum for Remote Control)

### Step 4 -- Authenticate Claude Code *(next)*

```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
echo 'export ANTHROPIC_API_KEY="sk-ant-your-key-here"' >> ~/.bashrc
source ~/.bashrc
claude -p "Say hello in one word"   # smoke test
```

- API key from: console.anthropic.com → API Keys → Create Key
- Pro or Max subscription required for Remote Control

### Step 5 -- Clone Repo & Create Folders *(next)*

```bash
cd ~
git clone git@github.com:your_username/Cruise-Workbook-2026.git
cd Cruise-Workbook-2026
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
mkdir -p Essentials Analytics Lab
ls -la
```

-----

## GitHub SSH Setup (Part 3 -- do before Step 5)

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/id_ed25519.pub     # copy this output
```

- Paste public key into: GitHub → Settings → SSH and GPG keys → New SSH key
- Title: `Cruise-Droplet`

Test connection:

```bash
ssh -T git@github.com
# Expected: Hi your_username! You've successfully authenticated...
```

-----

## Remote Control (Section 1.4)

```bash
cd ~/Cruise-Workbook-2026
claude --server-mode           # press Space for QR code
```

- Scan QR with iPad camera
- Opens live session in Claude mobile app
- Droplet keeps running even if Starlink drops (Mosh handles reconnect)

-----

## Key Notes

- **IP is permanent** as long as the Droplet exists -- only changes if you Destroy and rebuild
- **Never just Power Off** -- billing continues regardless, Droplet must be Destroyed to stop charges
- **Snapshot before Destroy** -- DO Console → Droplet → Snapshots → Take Snapshot
- **After rebuild from Snapshot** -- update Blink host config with new IP (only change needed)
- **$200 credit at $4/mo = ~50 months** -- leave it running, don’t overthink it

-----

## Folder Structure

```
~/Cruise-Workbook-2026/
├── Essentials/
│   ├── weather.py
│   ├── utils.py
│   ├── logger.py
│   └── bj_simple.py
├── Analytics/
│   ├── bj_pro.py
│   └── backgammon.py
└── Lab/
    ├── monte_carlo.py
    └── bayesian_engine.py
```

-----

*DigitalOcean · Ubuntu 24.04 · Claude Code · Blink Shell*
*MSC Meraviglia -- Starlink Maritime -- 2026*