# FFT Learning Workbook: Setup Guide

**Complete setup instructions for running Claude Code on DigitalOcean from your Mac.**

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [GitHub Setup](#github-setup)
3. [DigitalOcean Setup](#digitalocean-setup)
4. [Daily Workflow](#daily-workflow)
5. [Troubleshooting](#troubleshooting)

---

## ⚡ Quick Start

```bash
# 1. Create DigitalOcean droplet (Ubuntu 24.04, $5/month)
# 2. Add your SSH public key

# 3. SSH from Mac
ssh root@YOUR_DROPLET_IP

# 4. Install Claude Code & tmux
sudo npm install -g @anthropic-ai/claude-code
sudo apt install -y tmux

# 5. Create tmux session
tmux new-session -d -s claude -c ~/projects

# 6. Clone your workbook
git clone https://github.com/YOUR_USERNAME/fft-learning-workbook.git
cd fft-learning-workbook

# 7. Start working
tmux attach -t claude
claude-code my_project.py

# 8. Disconnect (keeps running!)
# Press Ctrl+B, then D
```

---

## 📊 Toolchain Architecture

```
Your Mac (Terminal)
    ↓ SSH Connection
DigitalOcean Droplet ($5/month)
    ↓ Contains
Claude Code + Node.js + Python
    ↓ Running in
tmux Sessions (stays alive 24/7)
    ↓ Executes
Your Projects (FFT, Python, JavaScript, etc.)
```

---

# GITHUB SETUP

## Why GitHub?

- Share your work and learning journey
- Collaborate with others
- Version control for your projects
- Build your portfolio

## Repository Structure

```
fft-learning-workbook/
├── README.md                    # Main guide (points to SETUP.md & CLAUDE_CODE_GUIDE.md)
├── SETUP.md                     # This file
├── CLAUDE_CODE_GUIDE.md         # How to use Claude Code with 8 use cases
├── toolchain-diagram.svg        # Visual architecture
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
└── projects/                    # Your Claude Code projects
    ├── use-case-1/
    ├── use-case-2/
    └── your-custom-project/
```

## Step 1: Create Repository on GitHub

1. Go to [github.com/new](https://github.com/new)
2. **Repository name:** `fft-learning-workbook`
3. **Description:** "FFT learning with Claude Code on DigitalOcean - 8 interactive use cases"
4. **Public** (so others can learn from it)
5. ✅ Check "Add a README file"
6. ✅ Check "Add .gitignore" → Select "Python"
7. Click **Create repository**

## Step 2: Clone to Your Mac

```bash
git clone https://github.com/YOUR_USERNAME/fft-learning-workbook.git
cd fft-learning-workbook
```

## Step 3: Add Files

```bash
# Copy setup files
cp ~/Downloads/SETUP.md .
cp ~/Downloads/CLAUDE_CODE_GUIDE.md .
cp ~/Downloads/toolchain-diagram.svg .

# Create requirements.txt
cat > requirements.txt << 'EOF'
numpy>=1.20.0
scipy>=1.7.0
matplotlib>=3.4.0
librosa>=0.9.0
EOF
```

## Step 4: Update Main README.md

Edit `README.md` in your repo:

```markdown
# FFT Learning Workbook

Learn Fast Fourier Transform by building real projects with Claude Code on DigitalOcean.

## 📖 Documentation

1. **[SETUP.md](SETUP.md)** - Get your environment running
   - DigitalOcean droplet setup
   - SSH from Mac
   - Install Claude Code
   - Daily workflow with tmux

2. **[CLAUDE_CODE_GUIDE.md](FFT_ClaudeCodeGuide.md)** - Learn FFT with Claude Code
   - 8 interactive use cases
   - Prompting techniques for Claude Code
   - Running code examples
   - Challenges and extensions

## 🎯 Quick Start

See [SETUP.md](SETUP.md) for complete instructions. TL;DR:

```bash
# Create DigitalOcean droplet ($5/month)
# Add SSH key, then:
ssh root@YOUR_IP
sudo npm install -g @anthropic-ai/claude-code
tmux new-session -d -s claude
tmux attach -t claude
claude-code file.py
```

## 📊 Architecture

See `toolchain-diagram.svg` for visual overview.

## 📚 Learn FFT

See [CLAUDE_CODE_GUIDE.md](FFT_ClaudeCodeGuide.md) for 8 use cases:
1. Simple Sine Wave
2. Audio Frequency Analysis
3. Noise Filtering
4. Image Blur (2D FFT)
5. Periodic Patterns
6. Spectrograms
7. Pitch Detection
8. Compression

## 💬 Questions?

Check the Troubleshooting section in each guide.

---

See [SETUP.md](SETUP.md) to get started!
```

## Step 5: Commit and Push

```bash
git add .
git commit -m "Add FFT Learning Workbook with setup and Claude Code guide"
git push origin main
```

---

# DIGITALOCEAN SETUP

## Why DigitalOcean?

| Feature | Your Mac | DigitalOcean |
|---------|----------|--------------|
| Always running | ❌ | ✅ 24/7 |
| Session persists | ❌ Close when quit | ✅ tmux keeps alive |
| Access anywhere | ❌ This Mac only | ✅ Any device |
| Cost | Free | ✅ $5/month (~17¢/day) |
| Power | Limited | ✅ Scales with needs |
| Like Blink? | N/A | ✅ SSH + more powerful |

## Complete Setup Steps

### Step 1: Create Account & SSH Key

On your Mac:

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Press Enter for defaults
# Optional: set passphrase

# View your PUBLIC key (copy this!)
cat ~/.ssh/id_ed25519.pub
```

**Important:** Copy the output. You'll paste this into DigitalOcean.

### Step 2: Create DigitalOcean Droplet

1. Go to [digitalocean.com](https://www.digitalocean.com)
2. Sign up (might get $100-200 free credits)
3. Click **Create** → **Droplet**

**Configure:**
- **Image:** Ubuntu 24.04 x64
- **Plan:** $5/month (2GB RAM, 1 CPU, 50GB storage)
- **Region:** Closest to you
- **Authentication:** SSH Key
  - Click "New SSH Key"
  - Paste your public key from above
  - Name it "Mac Dev Key"
- **Hostname:** `claude-code-mac`

Click **Create Droplet** and wait 1-2 minutes.

### Step 3: Get Droplet IP

In DigitalOcean dashboard, find your droplet's **IPv4 address** (looks like `123.45.67.89`)

### Step 4: SSH from Mac

```bash
# First connection (you'll verify fingerprint)
ssh root@YOUR_DROPLET_IP

# Example:
ssh root@123.45.67.89

# Type 'yes' when asked to verify fingerprint
```

✅ You're now on your droplet!

### Step 5: Initial System Setup

```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Install Node.js (required for Claude Code)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Install Python
sudo apt install -y python3 python3-pip

# Install tmux (keeps sessions alive)
sudo apt install -y tmux

# Install Git
sudo apt install -y git

# Verify everything
node --version
npm --version
python3 --version
tmux -V
git --version
```

### Step 6: Install Claude Code

```bash
# Global installation
sudo npm install -g @anthropic-ai/claude-code

# Verify
claude-code --version
```

### Step 7: Create Projects Directory

```bash
mkdir -p ~/projects/fft-learning
cd ~/projects/fft-learning
```

### Step 8: Clone Your Workbook

```bash
# Clone from GitHub
git clone https://github.com/YOUR_USERNAME/fft-learning-workbook.git

cd fft-learning-workbook

# Install Python dependencies
pip3 install -r requirements.txt
```

### Step 9: Create tmux Session

```bash
# Create named session that stays alive
tmux new-session -d -s claude -c ~/projects/fft-learning/fft-learning-workbook

# Verify
tmux list-sessions
```

✅ **Your droplet is ready!**

---

## Make SSH Easier on Mac

Edit `~/.ssh/config` on your Mac:

```bash
nano ~/.ssh/config
```

Add:

```
Host claude-do
    HostName YOUR_DROPLET_IP
    User root
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

Now instead of `ssh root@123.45.67.89`:

```bash
ssh claude-do
```

Much easier! 🎉

---

## Using Warp Terminal (Modern Terminal for Mac)

If you use **Warp** (or similar modern terminals like iTerm2), this section is for you.

### Option A: Warp + SSH + tmux (Recommended)

This is the standard approach - no changes needed!

```bash
# In Warp, connect normally
ssh claude-do

# Attach to tmux session
tmux attach -t claude

# Work as usual
claude-code my_file.py

# Detach (keeps running)
Ctrl+B, D
```

**Advantages:**
- ✅ Works everywhere (no firewall issues)
- ✅ Same workflow as SSH
- ✅ tmux is industry standard

### Option B: Warp + mosh (Better for Mobile/Network Changes)

**mosh** (mobile shell) is like SSH but better for:
- Switching networks (WiFi → LTE)
- Unreliable connections
- Similar to Blink on iPad

#### Step 1: Install mosh on Droplet

```bash
ssh claude-do

# Install mosh
sudo apt install -y mosh
```

#### Step 2: Configure Firewall (if needed)

```bash
# DigitalOcean cloud firewall: allow UDP 60000-61000
# In DigitalOcean dashboard → Firewall → Add Rules
# Custom: UDP, Ports 60000-61000
```

#### Step 3: Update SSH Config for mosh

Edit `~/.ssh/config` on your Mac:

```
Host claude-do
    HostName YOUR_DROPLET_IP
    User root
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60
    ServerAliveCountMax 3

Host mosh-claude
    HostName YOUR_DROPLET_IP
    User root
    # mosh config goes here
```

#### Step 4: Connect with mosh

```bash
# In Warp
mosh claude-do

# Or directly
mosh root@YOUR_DROPLET_IP

# Now you're connected with better network resilience!
```

### Option C: Warp + tmux + mosh (Best of Both)

Use mosh for the connection, tmux for sessions:

```bash
# In Warp
mosh claude-do

# On droplet, attach to tmux
tmux attach -t claude

# Work away
claude-code my_file.py

# Disconnect from tmux (keeps running)
Ctrl+B, D

# Close mosh if you want
exit
```

**This gives you:**
- ✅ Network resilience from mosh
- ✅ Session persistence from tmux
- ✅ Best of both worlds!

---

## Warp-Specific Tips

### Warp's Command Palette

Warp has a command palette (like VS Code). You can:

```
# In Warp, press Cmd+P
fzf  # Find and run recent commands
ssh  # Find SSH hosts
mosh # Find mosh hosts
```

### Warp's AI Features

Warp includes AI command suggestions. You can use this to remember commands:

```
"How do I attach to tmux?"
→ Warp suggests: tmux attach -t claude
```

### Warp SSH Profiles

In Warp, you can store SSH profiles:

```
# Open Warp settings
Cmd+,

# Add SSH profile
- Name: claude-droplet
- Host: claude-do
- User: root
- Key: ~/.ssh/id_ed25519
```

Then in Warp:
```
# Cmd+P → type "claude" → connects instantly
```

---

## Comparison: SSH vs mosh

| Feature | SSH + tmux | mosh + tmux |
|---------|-----------|-----------|
| Network resilience | ⚠️ Drops on network change | ✅ Survives network changes |
| Firewall compatibility | ✅ TCP 22 (always works) | ⚠️ UDP 60000-61000 |
| Setup complexity | ✅ Simple | ⚠️ More setup |
| Session persistence | ✅ With tmux | ✅ With tmux |
| Mobile use (iPad/phone) | ✅ Works | ✅ Better |
| Like Blink on iPad? | ⚠️ Similar | ✅ Very similar |
| Speed | Good | Faster (local echo) |

**Recommendation:**
- **Start with:** SSH + tmux (works everywhere)
- **Switch to:** mosh when you need network resilience
- **Best:** mosh + tmux for all features

---

## Troubleshooting Warp + mosh

**"mosh: command not found"**
```bash
# Install mosh on your Mac
brew install mosh

# Or from Warp's command palette
mosh  # Warp will suggest installation
```

**"mosh connection fails"**
1. Check firewall allows UDP 60000-61000
2. Verify mosh installed on droplet: `mosh --version`
3. Try SSH first to confirm network works: `ssh claude-do`
4. Fall back to SSH + tmux if mosh doesn't work

**"Warp can't find mosh-server"**
```bash
# Make sure mosh is installed on droplet
ssh claude-do
which mosh-server

# If not found, reinstall
sudo apt install --reinstall mosh
```

---

---

## mosh Only vs mosh + tmux

**Important:** With mosh, **you don't need tmux!** Here's your choice:

### Choice 1: mosh ONLY (Simpler) ✨ Recommended for Learning

```bash
# 1. Install mosh
brew install mosh
ssh claude-do
sudo apt install -y mosh

# 2. Connect with mosh
mosh claude-do

# 3. Start your code
claude-code use_case_1.py

# 4. Close Warp when done
# (Your code keeps running on server!)

# 5. Later, reconnect anytime
mosh claude-do
# Your code is still there!
```

**Pros:**
- ✅ Simpler (no tmux commands to learn)
- ✅ mosh auto-reconnects if network drops
- ✅ Perfect for learning FFT
- ✅ Code keeps running on server

**Cons:**
- ❌ Can't have multiple terminal windows
- ❌ Only one project at a time

**Best for:** Learning FFT, single projects, simplicity

---

### Choice 2: mosh + tmux (More Power) 💪

```bash
# 1. Install both
brew install mosh
ssh claude-do
sudo apt install -y mosh tmux

# 2. Connect with mosh
mosh claude-do

# 3. Create multiple tmux sessions for different projects
tmux new-session -s fft
tmux new-session -s audio
tmux new-session -s custom

# 4. Work on one project
tmux attach -t fft
claude-code use_case_1.py
Ctrl+B, D  # Detach

# 5. Switch to another project
tmux attach -t audio
claude-code audio_project.py

# 6. Both keep running!
```

**Pros:**
- ✅ Multiple projects simultaneously
- ✅ Multiple terminal windows
- ✅ Professional workflow
- ✅ mosh + tmux = bulletproof resilience

**Cons:**
- ⚠️ More to learn (tmux commands)
- ⚠️ More complexity

**Best for:** Professional dev, multiple projects, advanced workflows

---

## Recommendation for You

**Start with:** mosh ONLY

```bash
# Simple setup:
mosh claude-do
claude-code my_file.py

# When done: just close Warp
# Code keeps running!
# Reconnect later: mosh claude-do
```

**Upgrade to:** mosh + tmux (if/when you need multiple projects)

---

## Quick Start for Warp Users

```bash
# OPTION A: mosh Only (Simpler)
brew install mosh
ssh claude-do
sudo apt install -y mosh
mosh claude-do
claude-code my_file.py

# OPTION B: mosh + tmux (More Power)
brew install mosh
ssh claude-do
sudo apt install -y mosh tmux
mosh claude-do
tmux new-session -s claude
tmux attach -t claude
claude-code my_file.py
Ctrl+B, D  # Keep running!
```

**That's it!** Now you have the Blink-like experience on your Mac with Warp. 🎉

---

## Session Persistence Comparison

| Method | Session Persistent | Network Resilient | Multiple Projects | Complexity |
|--------|-------------------|------------------|------------------|-----------|
| SSH only | ❌ | ❌ | ❌ | ⭐ |
| SSH + tmux | ✅ | ❌ | ✅ | ⭐⭐⭐ |
| mosh only | ✅ | ✅ | ❌ | ⭐ |
| **mosh + tmux** | ✅ | ✅ | ✅ | ⭐⭐⭐ |

**You probably want:** mosh only (for learning) or mosh + tmux (for production)

---

# DAILY WORKFLOW

## Every Day: Connect & Code

### Morning: SSH to Droplet

```bash
ssh claude-do
```

### Attach to Your Session

```bash
# See all sessions
tmux list-sessions

# Attach to your claude session
tmux attach -t claude
```

### Work on Projects

```bash
# Your files are here
ls -la

# Run Claude Code
claude-code my_file.py

# Or start something new
echo "print('Hello')" > test.py
claude-code test.py
```

### When Done: Disconnect

```bash
# Press Ctrl+B, then D
# (Hold Ctrl+B, release, then press D)

# You're back on your Mac
# Code keeps running on droplet 24/7!
```

### Later: Reconnect Anytime

```bash
ssh claude-do
tmux attach -t claude

# Your code is still there!
```

## tmux Quick Reference

```bash
# Create session
tmux new-session -d -s name -c ~/path

# Attach to session
tmux attach -t name

# List sessions
tmux list-sessions

# Detach (keep running)
Ctrl+B, D

# Create new window in session
Ctrl+B, C

# Switch windows
Ctrl+B, N (next) or P (previous)

# Kill session (stop everything)
tmux kill-session -t name

# Split horizontally
Ctrl+B, "

# Split vertically
Ctrl+B, %

# Navigate panes
Ctrl+B, arrow keys
```

## Multiple Projects

Create separate sessions:

```bash
# Session 1: FFT Learning
tmux new-session -d -s fft -c ~/projects/fft-learning

# Session 2: Audio Analysis
tmux new-session -d -s audio -c ~/projects/audio-analysis

# Session 3: Your project
tmux new-session -d -s custom -c ~/projects/custom

# Switch between them
tmux attach -t fft
tmux attach -t audio
tmux attach -t custom
```

---

# TROUBLESHOOTING

## Connection Issues

**"Connection refused"**
- Droplet might be starting. Wait 1-2 minutes.
- Check droplet is powered on in DigitalOcean dashboard
- Verify IP address is correct
- Check SSH key permissions: `chmod 600 ~/.ssh/id_ed25519`

**"Permission denied (publickey)"**
- Verify public key (not private!) was pasted: `cat ~/.ssh/id_ed25519.pub`
- Check you're using correct key in SSH config
- Try: `ssh -i ~/.ssh/id_ed25519 root@YOUR_IP`

**"Host key verification failed"**
- First time connecting, type 'yes' to verify fingerprint
- If you get this again: `ssh-keygen -R YOUR_DROPLET_IP`

## Installation Issues

**"Node not found"**
```bash
# Reinstall Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

**"Claude Code not found"**
```bash
# Reinstall Claude Code
sudo npm install -g @anthropic-ai/claude-code
```

**"tmux not found"**
```bash
sudo apt install -y tmux
```

**"Python packages missing"**
```bash
pip3 install -r requirements.txt
```

## Session Issues

**"Lost my tmux session"**
```bash
# Create new one
tmux new-session -d -s claude -c ~/projects
tmux attach -t claude
```

**"Session crashed"**
```bash
# List sessions
tmux list-sessions

# Kill crashed one
tmux kill-session -t claude

# Create new one
tmux new-session -d -s claude
```

## Performance Issues

**"Droplet is slow"**
- Check resource usage: `top` or `free -h`
- Upgrade to $6+ plan in DigitalOcean dashboard
- Close unused tmux windows/sessions

**"Claude Code slow to start"**
- First run is slower (downloading dependencies)
- Subsequent runs are faster
- Check Node.js version: `node --version` (need 14+)

---

## Cost & Saving Money

### Check Droplet Usage

```bash
ssh claude-do

# Disk usage
df -h

# Memory
free -h

# CPU
top
```

### Save Money

- **Power off when not using:** Costs $0 when powered off (can restart anytime)
- **Use smallest droplet:** $5/month is plenty for Claude Code
- **Upgrade only if needed:** Start small, scale up later

### Monitor Costs

- Check DigitalOcean billing in dashboard
- Powered-off droplets are free!
- Only pay for what you use

---

## Questions?

1. **Check this guide** - Most answers are here
2. **Review error messages** - They're usually helpful
3. **Google the error** - "ssh permission denied" often has answers
4. **Check DigitalOcean docs** - Very good documentation
5. **Ask in GitHub issues** - Share your problem with others

---

## Summary Checklist

- [ ] SSH key generated on Mac
- [ ] DigitalOcean account created
- [ ] Droplet created ($5/month, Ubuntu 24.04)
- [ ] SSH key added to droplet
- [ ] Can SSH in from Mac
- [ ] Node.js installed
- [ ] Python installed
- [ ] Claude Code installed
- [ ] tmux installed
- [ ] Workbook cloned from GitHub
- [ ] tmux session created
- [ ] Ready to start learning FFT!

---

## Next Steps

1. **Complete this setup** ✅
2. **Read [CLAUDE_CODE_GUIDE.md](FFT_ClaudeCodeGuide.md)** - Learn how to use Claude Code for FFT
3. **Start Use Case 1** - Simple Sine Wave
4. **Build your way up** - Complete all 8 use cases

---

## Additional Resources

- [DigitalOcean Docs](https://docs.digitalocean.com/)
- [SSH Key Guide](https://docs.digitalocean.com/products/droplets/how-to/add-ssh-keys/)
- [tmux Cheat Sheet](https://tmuxcheatsheet.com/)
- [SSH Config Guide](https://linuxize.com/post/using-the-ssh-config-file/)

---

**You're all set! Now go to [CLAUDE_CODE_GUIDE.md](FFT_ClaudeCodeGuide.md) to start learning FFT.** 🚀
