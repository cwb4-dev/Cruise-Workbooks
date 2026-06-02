# FFT Learning Workbook + Claude Code on DigitalOcean

**Complete guide to learning FFT with Claude Code, hosted on DigitalOcean, accessed from your Mac.**

Combines three things:
1. 🎵 **FFT Learning Workbook** - 8 interactive use cases to master signal processing
2. 📚 **GitHub Documentation** - Everything you need to share and collaborate
3. ☁️ **DigitalOcean Setup** - Run Claude Code 24/7 on a $5/month cloud droplet

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

**Visual Diagram:** See `toolchain-diagram.svg` for complete architecture

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Part 1: FFT Learning Workbook](#part-1-fft-learning-workbook)
3. [Part 2: GitHub Setup](#part-2-github-setup)
4. [Part 3: DigitalOcean Setup](#part-3-digitalocean-setup)
5. [Part 4: Daily Workflow](#part-4-daily-workflow)
6. [FAQ & Troubleshooting](#faq--troubleshooting)

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
claude-code FFT_Learning_Workbook.md

# 8. Disconnect (keeps running!)
# Press Ctrl+B, then D
```

✅ **Done!** Your FFT environment is running 24/7 on the cloud.

---

# PART 1: FFT LEARNING WORKBOOK

## What You'll Learn

- **Audio & Music** - Analyze frequencies in sound, detect notes
- **Noise Filtering** - Clean up noisy signals
- **Image Processing** - Blur, enhance, compress images
- **Pattern Detection** - Find hidden cycles in data
- **Compression** - Learn how MP3/JPG actually work
- **Pitch Detection** - Build a simple music tuner

## 8 Progressive Use Cases

| # | Use Case | Topic | Difficulty | Time |
|---|----------|-------|------------|------|
| 1 | Simple Sine Wave | FFT Basics | ⭐ | 15 min |
| 2 | Audio Frequency Analysis | Music & Sound | ⭐ | 20 min |
| 3 | Noise Filtering | Signal Processing | ⭐⭐ | 25 min |
| 4 | Image Blur | 2D FFT | ⭐⭐ | 20 min |
| 5 | Periodic Patterns | Time Series | ⭐⭐ | 25 min |
| 6 | Spectrograms | Frequency Over Time | ⭐⭐ | 20 min |
| 7 | Pitch Detection | Audio Recognition | ⭐⭐⭐ | 30 min |
| 8 | Compression | Data Reduction | ⭐⭐⭐ | 30 min |

### Recommended Learning Path

**Foundation (1-2 hours):**
1. Use Case 1 - Sine Wave basics
2. Use Case 2 - Audio analysis (most intuitive!)
3. Use Case 3 - Filtering

**Choose Your Path:**
- **Love audio?** → Use Cases 6, 7
- **Like images?** → Use Case 4
- **Analyzing data?** → Use Cases 5, 8
- **Want it all?** → Do them in order

### Sample Code: Use Case 1 - Simple Sine Wave

```python
import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

# Create a sine wave at 5 Hz
duration = 1.0
sample_rate = 1000
t = np.linspace(0, duration, sample_rate, endpoint=False)
frequency = 5
signal = np.sin(2 * np.pi * frequency * t)

# Compute FFT
fft_values = fft(signal)
frequencies = fftfreq(len(signal), 1/sample_rate)

# Get positive frequencies
positive_freq_idx = frequencies > 0
positive_freqs = frequencies[positive_freq_idx]
positive_fft = np.abs(fft_values[positive_freq_idx])

# Plot results
fig, (ax1, ax2) = plt.subplots(2, 1)

# Time domain
ax1.plot(t[:200], signal[:200])
ax1.set_title("Time Domain: Original Signal")
ax1.set_xlabel("Time (s)")
ax1.grid(True, alpha=0.3)

# Frequency domain
ax2.plot(positive_freqs[:100], positive_fft[:100])
ax2.set_title("Frequency Domain: FFT Result")
ax2.set_xlabel("Frequency (Hz)")
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print(f"Peak frequency: {positive_freqs[np.argmax(positive_fft[:100])]} Hz")
```

### What to Try with Each Use Case

Each use case includes "What to Try" challenges like:
- [ ] Change the frequency parameter
- [ ] Add multiple signals together
- [ ] Increase noise and observe
- [ ] Load your own audio file
- [ ] Create variations

See `FFT_Learning_Workbook.md` for complete code and all 8 use cases.

### Installation & Setup

```bash
# Install required packages
pip install numpy scipy matplotlib librosa

# Verify installation
python3 -c "import numpy, scipy, matplotlib, librosa; print('✓ All packages ready!')"
```

---

# PART 2: GITHUB SETUP

## Repository Structure

```
fft-learning-workbook/
├── README.md                          # This file
├── FFT_Learning_Workbook.md          # 8 use cases + starter code
├── toolchain-diagram.svg              # Architecture diagram
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore rules
└── projects/                          # Your Claude Code projects
    ├── audio-analysis/
    ├── image-processing/
    └── your-project/
```

## Create GitHub Repository

### Step 1: Create Repo on GitHub

1. Go to [github.com/new](https://github.com/new)
2. Name: `fft-learning-workbook`
3. Description: "FFT learning with Claude Code on DigitalOcean"
4. Public (so others can learn from it)
5. Add `.gitignore`: Python
6. Create repository

### Step 2: Clone Locally (on your Mac)

```bash
git clone https://github.com/YOUR_USERNAME/fft-learning-workbook.git
cd fft-learning-workbook
```

### Step 3: Add Files

```bash
# Copy workbook files
cp ~/Downloads/FFT_Learning_Workbook.md .
cp ~/Downloads/README.md .
cp ~/Downloads/toolchain-diagram.svg .

# Create requirements.txt
cat > requirements.txt << 'EOF'
numpy>=1.20.0
scipy>=1.7.0
matplotlib>=3.4.0
librosa>=0.9.0
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Jupyter
.ipynb_checkpoints/

# Project files
*.png
*.jpg
*.jpeg
*.wav
*.mp3
EOF
```

### Step 4: Commit & Push

```bash
git add .
git commit -m "Initial commit: FFT Learning Workbook + DigitalOcean setup"
git push origin main
```

### Step 5: Make It Nice

Add to your GitHub README description:
```
🎵 Learn FFT (Fast Fourier Transform) by doing!
8 interactive use cases + starter code
Run on DigitalOcean with Claude Code
Always-on development environment with tmux
```

## Share Your Work

```bash
# Make sure everything is committed
git status

# Push to GitHub
git push origin main

# Share the link
# https://github.com/YOUR_USERNAME/fft-learning-workbook
```

---

# PART 3: DIGITALOCEAN SETUP

## Why DigitalOcean?

| Feature | Your Mac | DigitalOcean |
|---------|----------|--------------|
| Always running | ❌ | ✅ 24/7 |
| Session persists | ❌ Close when quit | ✅ tmux keeps alive |
| Access from anywhere | ❌ This Mac only | ✅ Any device, any place |
| Cost | Free | ✅ $5/month (~17¢/day) |
| Power | Limited by Mac | ✅ Scales with needs |
| Compare to Blink | N/A | ✅ SSH + more powerful |

## Step-by-Step Setup

### Step 1: Create DigitalOcean Account

1. Go to [digitalocean.com](https://www.digitalocean.com)
2. Sign up (might get free $100-200 credits)
3. Add payment method

### Step 2: Create SSH Key on Mac

```bash
# Generate key (if you don't have one)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Press Enter for default location
# Optionally set passphrase

# Copy public key
cat ~/.ssh/id_ed25519.pub
```

**Keep this output - you'll paste it into DigitalOcean!**

### Step 3: Create Droplet in DigitalOcean

1. Click **Create** → **Droplet**
2. **Image:** Ubuntu 24.04 x64 (latest LTS)
3. **Plan:** $5/month (perfect for Claude Code)
4. **Region:** Closest to you
5. **Authentication:** 
   - Select **SSH Key**
   - Paste your public key from `id_ed25519.pub`
6. **Hostname:** `claude-code-mac` (or your choice)
7. Click **Create Droplet**

✅ Droplet created! Wait 1-2 minutes for it to boot.

### Step 4: Get Droplet IP Address

In DigitalOcean dashboard, find your droplet's **IPv4 address** (looks like `123.456.789.000`)

### Step 5: SSH into Droplet

On your Mac:

```bash
# First time connection
ssh root@YOUR_DROPLET_IP

# Example:
ssh root@123.45.67.89

# Type 'yes' when asked to verify fingerprint
```

✅ You're now on your droplet!

### Step 6: Initial Setup

```bash
# Update everything
sudo apt update && sudo apt upgrade -y

# Install Node.js (required for Claude Code)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Install Python
sudo apt install -y python3 python3-pip

# Install tmux (keeps sessions alive)
sudo apt install -y tmux

# Verify
node --version
npm --version
python3 --version
tmux -V
```

### Step 7: Install Claude Code

```bash
# Global installation
sudo npm install -g @anthropic-ai/claude-code

# Verify
claude-code --version
```

### Step 8: Create Project Directory

```bash
# Create projects folder
mkdir -p ~/projects/fft-learning

# Navigate there
cd ~/projects/fft-learning
```

### Step 9: Clone Your Workbook (from GitHub)

```bash
# Clone your repository
git clone https://github.com/YOUR_USERNAME/fft-learning-workbook.git

# Navigate into it
cd fft-learning-workbook

# Install Python dependencies
pip3 install -r requirements.txt
```

### Step 10: Create tmux Session

```bash
# Create a named session that stays alive
tmux new-session -d -s claude -c ~/projects/fft-learning/fft-learning-workbook

# Verify it exists
tmux list-sessions

# Output should show:
# claude: 1 windows (created ...)
```

✅ **Your droplet is ready!**

## Make SSH Easier on Mac

Add this to `~/.ssh/config`:

```
Host claude-do
    HostName YOUR_DROPLET_IP
    User root
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60
```

Now instead of `ssh root@123.456.789.000`, just do:

```bash
ssh claude-do
```

---

# PART 4: DAILY WORKFLOW

## Every Day: Connect & Code

### Morning: Connect to Your Environment

```bash
# On your Mac Terminal
ssh claude-do

# You're on the droplet now
```

### Attach to Your Session

```bash
# See all sessions
tmux list-sessions

# Attach to claude session
tmux attach -t claude

# You're back in your coding environment!
```

### Work on Your Projects

```bash
# Your files are here
ls -la

# Run Claude Code on any file
claude-code FFT_Learning_Workbook.md

# Or start a new project
echo "import numpy as np" > my_project.py
claude-code my_project.py
```

### When You're Done: Disconnect (Keep Running!)

```bash
# Press Ctrl+B, then D
# (That's: Hold Ctrl+B, release, then press D)

# You're now back on your Mac
# Your code keeps running on the droplet 24/7!
```

### Later: Check Your Work

```bash
# SSH in from anywhere
ssh claude-do

# Reattach to see your session
tmux attach -t claude

# Your code is still there!
```

## tmux Cheat Sheet

```bash
# Create session
tmux new-session -d -s name -c ~/path

# Attach to session
tmux attach -t name

# List sessions
tmux list-sessions

# Create new window in session
tmux new-window -t name

# Detach (keep running)
Ctrl+B, D

# Kill session (stop everything)
tmux kill-session -t name

# Switch windows
Ctrl+B, N (next) or P (previous)

# Split window horizontally
Ctrl+B, "

# Split window vertically
Ctrl+B, %

# Navigate panes
Ctrl+B, arrow keys
```

## Multiple Projects

Create separate sessions for different projects:

```bash
# Session 1: FFT Learning
tmux new-session -d -s fft -c ~/projects/fft-learning

# Session 2: Audio Analysis
tmux new-session -d -s audio -c ~/projects/audio-analysis

# Session 3: Your custom project
tmux new-session -d -s custom -c ~/projects/custom

# List all
tmux list-sessions

# Switch between them
tmux attach -t fft
tmux attach -t audio
tmux attach -t custom
```

---

# FAQ & Troubleshooting

## FFT Questions

**Q: Do I need to know advanced math?**
A: No! We explain concepts intuitively. Math is optional.

**Q: How long to learn?**
A: Quick overview: 2-3 hours. Full workbook: 1-2 weeks with experimentation.

**Q: Can I use my own data?**
A: Yes! Many use cases support loading real audio, images, or data.

**Q: Does FFT only work for audio?**
A: No! Works for stock prices, sensor data, images, seismic data, radio signals, etc.

## DigitalOcean Questions

**Q: Why $5/month droplet?**
A: 2GB RAM, 1 CPU, 50GB storage is plenty for Claude Code + Python projects.

**Q: Can I upgrade later?**
A: Yes! You can resize your droplet anytime.

**Q: What if I want to save money?**
A: Power off droplet when not using (costs $0). Can restart anytime.

**Q: How do I stop the droplet?**
A: DigitalOcean dashboard → Your droplet → Power Off

**Q: Can I access from my iPad too?**
A: Yes! Use Blink or any SSH app on iPad to connect.

## Connection Issues

**"Connection refused"**
- Droplet might be starting. Wait 1-2 minutes.
- Check droplet is powered on in dashboard.
- Verify IP address is correct.

**"Permission denied (publickey)"**
- Your SSH key might not be on droplet.
- Verify public key was pasted correctly in DigitalOcean.
- Check: `~/.ssh/id_ed25519.pub` (not `id_ed25519`)

**"tmux not found"**
```bash
sudo apt install -y tmux
```

**"Claude Code not starting"**
```bash
# Check installation
which claude-code

# Reinstall if needed
sudo npm install -g @anthropic-ai/claude-code

# Check Node.js version (need 14+)
node --version
```

## Code Issues

**"FFT values look wrong"**
- Make sure sample rate is 2x your highest frequency
- Use `np.real(ifft(...))` when converting back
- Check indexing (off-by-one errors)

**"Performance is slow"**
- Make FFT length a power of 2: `len = 2^n`
- Use `scipy.fft` instead of `numpy.fft`
- Process in chunks for large data

**"Lost my tmux session"**
```bash
# Create new one
tmux new-session -d -s claude -c ~/projects
tmux attach -t claude
```

---

## Next Steps After This Workbook

### Challenge Projects

1. **Build an Equalizer** - Control bass, mids, treble
2. **Pitch Shifter** - Change audio pitch without speed
3. **Real-time Visualizer** - Animate frequency spectrum live
4. **Anomaly Detector** - Find when machinery acts weird
5. **Noise Remover** - Learn and remove background noise

### Advanced Topics

- Windowing functions (improve FFT accuracy)
- FIR/IIR filters (more sophisticated filtering)
- Wavelets (alternative to FFT)
- GPU acceleration with CuPy
- Web apps with Web Audio API

### Production Deployment

- Docker container for your project
- Auto-scaling with multiple droplets
- GitHub Actions for CI/CD
- Load balancing with nginx

---

## Learning Resources

### Included
- `FFT_Learning_Workbook.md` - All 8 use cases
- `toolchain-diagram.svg` - Visual architecture
- `requirements.txt` - Python dependencies

### External
- [3Blue1Brown FFT Video](https://www.youtube.com/watch?v=spUNpyF58BY) - Best visual explanation
- [NumPy FFT Docs](https://numpy.org/doc/stable/reference/routines.fft.html)
- [SciPy Signal](https://docs.scipy.org/doc/scipy/reference/signal.html)
- [Librosa Audio](https://librosa.org/)
- [DigitalOcean Docs](https://docs.digitalocean.com/)
- [tmux Guide](https://tmuxcheatsheet.com/)

---

## Complete Workflow Summary

```
┌─────────────────────────────────────────────────────┐
│ 1. Create DigitalOcean Account ($5/month droplet)   │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│ 2. Add SSH Key to Droplet                           │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│ 3. SSH from Mac: ssh claude-do                      │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│ 4. Install Claude Code, Node.js, Python, tmux      │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│ 5. Clone workbook from GitHub                       │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│ 6. Create tmux session: tmux new-session -d -s...  │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│ 7. Attach & Code: tmux attach -t claude             │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│ 8. Run Claude Code: claude-code file.py             │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│ 9. Detach (Ctrl+B, D) → Code runs 24/7!            │
└─────────────────────────────────────────────────────┘
```

---

## Getting Started Now

### Right Now (5 minutes)
1. ✅ Read this README
2. ✅ Look at `toolchain-diagram.svg`
3. ✅ Bookmark this repo

### Today (30 minutes)
1. Create DigitalOcean account
2. Create droplet with Ubuntu 24.04
3. SSH in and install Claude Code
4. Create tmux session

### This Week
1. Clone workbook to droplet
2. Start Use Case 1 (Sine Wave)
3. Work through Use Cases 2-3
4. Pick your path (audio/image/data)

### This Month
1. Complete all 8 use cases
2. Build a challenge project
3. Share your GitHub repo
4. Help others learn FFT!

---

## Support & Contributing

### Found a Bug?
- Open an issue on GitHub
- Include error message
- Tell us your environment

### Want to Improve?
1. Fork the repo
2. Create feature branch
3. Commit your changes
4. Submit pull request

### Questions?
- Check Troubleshooting section
- Review use case comments
- Search existing GitHub issues
- Ask in discussions

---

## License

MIT License - feel free to use, modify, share!

---

## Show Your Support

- ⭐ Star this repo
- 📢 Share with others learning signal processing
- 💬 Tell us what you built!
- 🤝 Contribute improvements

---

## Quick Links

- **Workbook:** `FFT_Learning_Workbook.md`
- **Diagram:** `toolchain-diagram.svg`
- **Requirements:** `requirements.txt`
- **DigitalOcean:** https://www.digitalocean.com
- **GitHub:** https://github.com/YOUR_USERNAME/fft-learning-workbook

---

## Final Checklist

- [ ] DigitalOcean account created
- [ ] SSH key generated on Mac
- [ ] Droplet created ($5/month)
- [ ] SSH connection works
- [ ] Claude Code installed on droplet
- [ ] tmux installed
- [ ] First tmux session created
- [ ] Workbook cloned from GitHub
- [ ] Ready to start learning FFT!

**Happy learning! 🎵🔊📊**

---

*Last updated: June 2026*
*Works with Claude Haiku 4.5, Claude Sonnet 4.6, and newer*
