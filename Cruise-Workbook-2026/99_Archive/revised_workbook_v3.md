# 🚢 Atlantic Data Lab: Master Implementation Workbook (2026 Edition)

**Setup:** Blink Shell (iPad) + DigitalOcean Droplet + Claude Code + Starlink  
**Philosophy:** Simple, elegant, and "couch potato" efficient.

-----

## Part 1: The iPad AI Command Center Setup

*Run these steps once to create a persistent environment that survives Starlink latency.*

### 1.1 The "Brain" (DigitalOcean)

1. Log in to [DigitalOcean](https://cloud.digitalocean.com).
1. **Create Droplet:**
- **OS:** Ubuntu 24.04 (LTS)
- **Plan:** Basic ($4 or $6/mo) is perfect.
- **Region:** Closest to your ship’s next port.
1. Copy the **IP Address**.

### 1.2 The "Screen" (Blink Shell)

1. Open **Blink Shell** on your iPad.
1. Type `config` > **Hosts** > **New Host**.
- **Label:** `AI-Server`
- **Hostname:** [Your Droplet IP]
- **User:** `root`
1. **Crucial:** Ensure **Mosh** is toggled **ON**. Mosh allows your terminal to survive Starlink latency spikes and IP changes as the ship moves.
1. Type `ssh AI-Server` to log in.

### 1.3 The AI Engine (2026 Toolchain)

Follow these steps carefully and in order. You are typing everything in your **Blink terminal**, connected to the Droplet.

#### Step 1 -- Update the server

```bash
apt update && apt upgrade -y
```

This refreshes the package list and installs any pending OS updates. It may take a minute or two. You will see a lot of scrolling output -- that is normal. Wait for the prompt to return.

#### Step 2 -- Install Python

```bash
apt install -y python3-pip
```

This installs Python and its package manager, which all 8 of your apps will use. Confirm it worked:

```bash
python3 --version
```

You should see something like `Python 3.12.x`.

#### Step 3 -- Install Claude Code

The official method as of 2026 is the native installer -- no Node.js required:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

When it finishes, reload your shell so the `claude` command is available:

```bash
source ~/.bashrc
```

Confirm it installed:

```bash
claude --version
```

You should see `claude 2.x.x` or higher. If the command is not found, try `source ~/.profile` and run it again.

#### Step 4 -- Authenticate Claude Code

> **Important:** Your Droplet is a headless Linux server -- it has no browser. The standard `claude` login opens a browser window, which will not work here. Instead, authenticate using your **Anthropic API key**.

1. On your iPad, go to [console.anthropic.com](https://console.anthropic.com) → **API Keys** → **Create Key**. Copy the key (it starts with `sk-ant-...`).
1. Back in Blink, set it as an environment variable so Claude Code can find it:

```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

1. To make this permanent so it survives reboots, add it to your shell profile:

```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

1. Verify Claude Code can connect:

```bash
claude --version
echo "Auth check -- if the key is wrong, the next command will error:"
claude -p "Say hello in one word"
```

You should see a single-word response. If you see an authentication error, double-check that you copied the full API key correctly.

> **Note:** A Pro or Max **claude.ai** subscription is required for Remote Control (Section 1.4). The API key above covers Claude Code usage and billing separately through [console.anthropic.com](https://console.anthropic.com).

#### Step 5 -- Clone your repo and create the project folders

Before launching Claude Code, bring your existing GitHub repo onto the Droplet and create the subdirectories your 8 apps will live in. *(Full GitHub SSH setup is in Part 3 -- complete that first if you haven’t already, then come back here.)*

```bash
# Clone your existing repo
cd ~
git clone git@github.com:your_username/Cruise-Workbook-2026.git
cd Cruise-Workbook-2026

# Set your git identity (required for commits)
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"

# Create the 3 folders your 8 apps expect
mkdir -p Essentials Analytics Lab
```

Confirm the structure looks right:

```bash
ls -la
```

You should see `Essentials/`, `Analytics/`, and `Lab/` listed.

-----

### 1.4 The "Remote Control" Hand-off

Remote Control is built directly into Claude Code -- no extra package needed. Your repo is already cloned from Step 5 above.

#### Step 1 -- Start Claude Code in server mode

In Blink, with your Droplet connected:

```bash
cd ~/Cruise-Workbook-2026
claude --server-mode
```

Claude Code will start, display a session URL, and show a message that it is waiting for a remote connection.

#### Step 2 -- Display the QR code

Press **Spacebar**. A QR code will appear in the terminal.

#### Step 3 -- Connect from your iPad

Open your iPad camera and scan the QR code. It will prompt you to open the session in the **Claude mobile app**. Tap **Open**.

#### Step 4 -- Verify the connection

In the Claude mobile app, you should see the active session with your `Cruise-Workbook-2026` project context loaded. Type a quick test message like `list the files in this directory` and confirm Claude Code responds with the actual contents of your Droplet.

**Result:** Claude Code runs continuously on your stable Droplet. If Starlink drops, Mosh holds the terminal session open. When it reconnects, your session is exactly where you left it -- and you continue typing from the iPad app.

> **Requirements:** Pro or Max subscription on claude.ai. Claude Code v2.1.51 or later -- confirm with `claude --version`. If below that, run `claude update`.

-----

## Part 2: The 8-App Playbook

*Once Remote Control is active, use the Claude mobile app on your iPad to issue these prompts. Claude Code will build, test, and save the files directly on your Droplet.*

### Phase 1: The Essentials

**1. Weather Advisor (`weather.py`)**

- **Prompt:** "Claude, create Essentials/weather.py. Fetch or simulate Nassau temperature. If > 80°, suggest the beach; else, suggest a museum. Run it."

**2. Multi-Utility Tool (`utils.py`)**

- **Prompt:** "Create Essentials/utils.py with a 12-char password generator and a USD to EUR converter (rate 0.92). Verify both functions work."

**3. Cruise Mood Logger (`logger.py`)**

- **Prompt:** "Create Essentials/logger.py. Ask for a ‘Cruise Mood %’. If > 70%, append ‘Great Day Amazing Cruise’ to mood_log.txt."

**4. Blackjack Probability (`bj_simple.py`)**

- **Prompt:** "Create Essentials/bj_simple.py. Calculate the bust probability of a hand of 16. It should output approximately 60%."

### Phase 2: Analytics & Simulations

**5. Strategy Comparison (`bj_pro.py`)**

- **Prompt:** "Create Analytics/bj_pro.py. Run 10,000 trials comparing a Dealer showing 6 vs. a Dealer showing Ace. Show why 6 is better for the player."

**6. Backgammon Dice Stats (`backgammon.py`)**

- **Prompt:** "Create Analytics/backgammon.py. Simulate 50,000 dice rolls. Confirm Double-6 frequency is ~2.78% and 7 is the most common sum."

**7. Monte Carlo Pi Estimator (`monte_carlo.py`)**

- **Prompt:** "Create Lab/monte_carlo.py. Use Monte Carlo needle-dropping to estimate Pi. Run enough trials to land between 3.13 and 3.15."

**8. Bayesian Inference (`bayesian_engine.py`)**

- **Prompt:** "Create Lab/bayesian_engine.py. Build a Bayesian updater. For 10 Heads and 2 Tails, calculate a posterior mean of ~0.83."

-----

## Part 3: Connecting Your Existing Repository

*Complete this section before finishing Section 1.3 Step 5. You need the SSH key on GitHub before the `git clone` will work.*

### 3.1 Create the Security Bridge (SSH Key)

1. In your **Blink terminal** (connected to the Droplet), generate a secure key:
   
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
   
   Press Enter through all prompts to accept the defaults and skip a passphrase.
1. Display and copy the public key:
   
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
   
   Select and copy the entire output -- it starts with `ssh-ed25519` and ends with your email address.

### 3.2 The Handshake (GitHub Settings)

1. On your iPad, go to **GitHub.com** → your profile → **Settings** → **SSH and GPG keys** → **New SSH key**.
1. Title it `Cruise-Droplet`.
1. Paste the key text you copied and click **Add SSH key**.

### 3.3 Test the Connection

Back in Blink, confirm the Droplet can talk to GitHub:

```bash
ssh -T git@github.com
```

You should see: `Hi your_username! You've successfully authenticated...`

If you see a fingerprint warning, type `yes` and press Enter -- this is expected on first connection. Once confirmed, head back to **Section 1.3 Step 5** to clone your repo.

-----

## Part 4: Verification & Sync

1. **Cost Check:** In your Claude Code session, type `/cost` to see token usage and estimated spend for the current session.
1. **Git Push:** Tell Claude: "Commit all these apps and push them to my existing GitHub repo."
1. **iPad Access:** Open the **Working Copy** app on your iPad and tap ‘Pull’ to sync the repo. Your 8 apps are now available for offline reading even if Starlink drops.