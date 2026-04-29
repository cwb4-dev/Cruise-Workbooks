# DigitalOcean Droplet Setup Log

**Atlantic Data Lab -- MSC Meraviglia 2026** | **Version 8**

-----

## Droplet Details

|Item          |Value                  |
|--------------|-----------------------|
|Provider      |DigitalOcean           |
|OS            |Ubuntu 24.04 LTS       |
|Plan          |Basic $4/mo            |
|Sign-on Credit|$200 (≈ 50 months free)|
|IP Address    |147.182.190.94         |
|Created       |April 28, 2026         |
|Region        |*(paste region here)*  |

-----

## Blink Shell Host Config

|Setting |Value         |
|--------|--------------|
|Label   |AI-Server     |
|Hostname|147.182.190.94|
|User    |root          |
|Mosh    |ON            |

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

-----

## Mosh Setup & Troubleshooting ✅

### What Was Done

```bash
apt install -y mosh          # installed on Droplet
ufw allow 60000:61000/udp    # opened UDP ports (firewall was inactive anyway)
reboot                       # required after apt upgrade kernel update
```

### Blink Config

- Host config: Alias = `AI-Server`, Hostname = `147.182.190.94`, User = `root`
- No explicit Mosh toggle in this version of Blink -- Mosh is invoked via command

### How to Connect

```bash
# From Blink prompt (not from inside Droplet)
mosh --verbose root@147.182.190.94
# Enter password when prompted
```

### Gotchas Encountered

- **Kernel mismatch error** on first Mosh attempt -- fixed by Power Cycling Droplet from DO console
- **`mosh AI-Server` falls back to SSH silently** -- use direct IP instead: `mosh --verbose root@147.182.190.94`
- **`--ssh` flag removed in Mosh 1.4.0** -- old syntax no longer works
- **`$SSH_CONNECTION` returns IP even on Mosh 1.4.0** -- not a reliable indicator in this version
- **Real test:** Put iPad to sleep 30 seconds, wake up, type `ls` -- if it responds immediately, Mosh is working ✓

### Verification

- iPad slept and woke -- session reconnected instantly ✓
- Mosh confirmed working despite `$SSH_CONNECTION` showing IP (Mosh 1.4.0 behaviour)

-----

## Step 4 -- Authenticate Claude Code ✅

```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-your-key-here"' >> ~/.bashrc
source ~/.bashrc
echo $ANTHROPIC_API_KEY       # verify key is set
claude -p "Say hello in one word"   # smoke test
```

- API key obtained from console.anthropic.com → API Keys → Create Key
- **Gotcha:** Key was blank -- `~.bashrc` had not been reloaded, key was never saved from earlier session
- **Fix:** Re-exported key and ran `source ~/.bashrc` -- key confirmed set with `echo $ANTHROPIC_API_KEY`
- **Smoke test:** `claude -p "Say hello in one word"` → returned "Hello" ✓
- **Key is permanent** -- saved in ~/.bashrc, survives reboots and Mosh reconnects

-----

## Step 5 -- GitHub SSH + Clone Repo ✅

```bash
# Generate SSH key on Droplet
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/id_ed25519.pub     # copy and add to GitHub

# Test connection
ssh -T git@github.com

# Clone repo and create folders
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
cd ~
git clone git@github.com:your_username/Cruise-Workbook-2026.git
cd Cruise-Workbook-2026
mkdir -p Essentials Analytics Lab
ls -la
```

### Notes

- SSH key generated at `/root/.ssh/id_ed25519.pub`
- Key added to GitHub → cwb4-dev → Settings → SSH keys → `Cruise-Droplet`
- **Gotcha:** `Cruise-Workbook-2026` is a folder inside the `at-sea-ipad-workbooks` repo, not its own repo
- **Correct clone command:**

```bash
git clone git@github.com:cwb4-dev/at-sea-ipad-workbooks.git
```

- Navigated into project: `cd at-sea-ipad-workbooks/Cruise-Workbook-2026`
- Created folders: `mkdir -p Essentials Analytics Lab` ✓
- Git identity set globally ✓
- **Result:** Full folder structure confirmed -- Essentials, Analytics, Lab, 99_Archive, plus existing md files ✓

-----

## Setup Complete ✅

All steps done. Full stack is live:

|Component                   |Status                                      |
|----------------------------|--------------------------------------------|
|DigitalOcean Droplet        |✅ Running -- 147.182.190.94                  |
|Ubuntu 24.04 + Python 3.12.3|✅                                           |
|Swap (1GB)                  |✅                                           |
|Mosh                        |✅ Confirmed working                         |
|Claude Code 2.1.119         |✅                                           |
|Anthropic API Key           |✅ Authenticated                             |
|GitHub SSH                  |✅ cwb4-dev connected                        |
|Repo cloned                 |✅ at-sea-ipad-workbooks/Cruise-Workbook-2026|
|Project folders             |✅ Essentials / Analytics / Lab              |

**Ready to build the 8 apps.**

-----

## Mosh Session Management

### Check Active Sessions

```bash
who
```

Shows all active Mosh sessions with PID, date, and connection info.

### Find Session PIDs

```bash
ps aux | grep mosh
```

Lists all running Mosh server processes with their PIDs.

### Kill a Specific Session

```bash
kill 1102    # replace 1102 with the actual PID
```

### Verify Session is Gone

```bash
who
```

### What the Detached Session Message Means

When you reconnect and see:

```
Mosh: You have a detached Mosh session on this server (mosh [1102]).
```

It means a previous session is still alive on the Droplet from before your iPad slept.

- Press **Enter** to start a fresh session alongside it
- Then kill the old one using the steps above
- You should only ever have one Mosh session running

### Always Connect With

```bash
mosh --verbose root@147.182.190.94
```

Not `ssh AI-Server` -- SSH drops when iPad sleeps, Mosh survives.

-----

## Project Folder Structure

```
~/at-sea-ipad-workbooks/Cruise-Workbook-2026/
├── Essentials/
│   ├── weather.py        ← App 1
│   ├── utils.py          ← App 2
│   ├── logger.py         ← App 3
│   └── bj_simple.py      ← App 4
├── Analytics/
│   ├── bj_pro.py         ← App 5
│   └── backgammon.py     ← App 6
└── Lab/
    ├── monte_carlo.py    ← App 7
    └── bayesian_engine.py ← App 8
```

Each folder also contains an `app_log.md` tracking build prompt, test results, and sample output.

-----

## Git Sync Workflow

**Source of truth is always GitHub.**

### Working Copy → Droplet

```
Working Copy → push → GitHub → git pull → Droplet
```

1. Make changes in Working Copy on iPad
1. Commit and push to GitHub from Working Copy
1. On the Droplet pull the latest:

```bash
cd ~/at-sea-ipad-workbooks/Cruise-Workbook-2026
git pull
```

### Droplet → Working Copy

```
Droplet → git push → GitHub → pull → Working Copy
```

1. After building/testing apps on Droplet:

```bash
git add .
git commit -m "Your message"
git push
```

1. Open Working Copy on iPad → tap **Pull**