# FFT Learning Workbook

**Learn Fast Fourier Transform by building real projects with Claude Code on DigitalOcean.**

A complete guide combining:
- ☁️ DigitalOcean droplet setup
- 🎵 8 interactive FFT use cases  
- 💻 Claude Code prompting techniques
- 🚀 Always-on development environment

---

## 📖 Documentation Structure

This project has **two main guides**:

### 1. [SETUP.md](SETUP.md) - Get Your Environment Running

**Everything about infrastructure:**
- Create DigitalOcean account and droplet ($5/month)
- Generate SSH keys on Mac
- Install Claude Code, Node.js, Python
- Set up tmux for persistent sessions
- Daily workflow: How to connect and work
- Troubleshooting for connection issues

**Read this first!** ✅

### 2. [CLAUDE_CODE_GUIDE.md](CLAUDE_CODE_GUIDE.md) - Learn FFT with Claude Code

**Everything about learning:**
- How to prompt Claude Code effectively
- 8 progressive use cases (sine waves → compression)
- Code examples you can copy/paste
- Challenges to try for each use case
- Challenge projects (equalizer, pitch shifter, etc.)
- Key FFT concepts explained simply
- Prompting templates you can reuse

**Read this after setup!** ✅

---

## ⚡ Quick Start

### For the Impatient (5 minutes)

```bash
# On your Mac

# 1. Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/id_ed25519.pub  # Copy this

# 2. Create DigitalOcean droplet
# - Go to digitalocean.com
# - Create droplet: Ubuntu 24.04, $5/month
# - Paste your SSH public key

# 3. Get your droplet's IP address, then:
ssh root@YOUR_DROPLET_IP

# 4. Install everything (on droplet)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs python3 python3-pip tmux git
sudo npm install -g @anthropic-ai/claude-code

# 5. Create session and start coding
tmux new-session -d -s claude -c ~/projects
tmux attach -t claude
claude-code my_file.py

# 6. Disconnect (keeps running!)
# Ctrl+B, then D
```

✅ You're ready! Now read [CLAUDE_CODE_GUIDE.md](CLAUDE_CODE_GUIDE.md) for learning.

---

## 📚 Complete Learning Path

```
Step 1: READ SETUP.md (30 minutes)
   └─ Get your environment running on DigitalOcean

Step 2: READ CLAUDE_CODE_GUIDE.md (Intro section)
   └─ Understand how to prompt Claude Code

Step 3: START USE CASE 1 (15 minutes)
   └─ Simple Sine Wave - learn FFT basics
   └─ See real output on your droplet

Step 4: TRY CHALLENGES (20 minutes)
   └─ Modify the code, experiment, learn

Step 5: DO USE CASES 2-3 (1 hour)
   └─ Audio analysis, noise filtering
   └─ These are the most intuitive

Step 6: PICK YOUR PATH (2-3 hours)
   ├─ Love audio? → Cases 6, 7 (spectrograms, pitch detection)
   ├─ Like images? → Case 4 (2D FFT, image blur)
   └─ Analyzing data? → Cases 5, 8 (patterns, compression)

Step 7: BUILD A PROJECT (1-2 days)
   └─ Equalizer, visualizer, pitch shifter, etc.
   └─ Combine multiple use cases

Step 8: APPLY TO YOUR DATA
   └─ Use FFT on your own audio, images, or data
   └─ See it work in practice!
```

**Total time:** 1-2 weeks with practice

---

## 🎯 The Two-Document System

**Why split into two?**

| Document | Focus | When to Read |
|----------|-------|--------------|
| [SETUP.md](SETUP.md) | Infrastructure | Before you start |
| [CLAUDE_CODE_GUIDE.md](CLAUDE_CODE_GUIDE.md) | Learning FFT | After setup is done |

This keeps each guide focused and easier to follow.

---

## 📋 What's Included

### SETUP.md Contains

✅ Quick start  
✅ GitHub repository setup  
✅ DigitalOcean droplet creation  
✅ SSH key generation  
✅ Claude Code installation  
✅ tmux session management  
✅ Daily workflow instructions  
✅ Troubleshooting for all setup issues  
✅ Cost optimization tips  

### CLAUDE_CODE_GUIDE.md Contains

✅ How to prompt Claude Code effectively  
✅ 8 use cases with full explanations  
✅ Claude Code prompts you can copy/paste  
✅ Challenges for each use case  
✅ Challenge projects  
✅ Key concepts explained simply  
✅ Prompting templates  
✅ Learning path recommendations  

---

## 🚀 Your Workflow

### Daily (30 minutes)

```bash
# 1. SSH to your droplet
ssh claude-do

# 2. Attach to your session
tmux attach -t claude

# 3. Work on your current use case
claude-code use_case_3.py

# 4. When done: disconnect (keeps running!)
# Ctrl+B, then D
```

---

## 💡 Key Advantages

### vs Learning on Your Mac

| Feature | Your Mac | This Setup |
|---------|----------|-----------|
| Always available | ❌ | ✅ 24/7 |
| Session persists | ❌ | ✅ With tmux |
| Use multiple devices | ❌ | ✅ Any device |
| Easy to share | ❌ | ✅ GitHub |

---

## 🎓 Learning Outcomes

By the end of this workbook, you'll understand:

- [ ] What FFT does (time → frequency)
- [ ] Why it's fast (O(n log n) algorithm)
- [ ] How to use it in Python (numpy, scipy)
- [ ] Real-world applications (audio, images, signals)
- [ ] How to work in the cloud with SSH/tmux
- [ ] How to prompt Claude Code for coding tasks

---

## ✅ Quick Checklist

- [ ] Read this README
- [ ] Read [SETUP.md](SETUP.md) - Get environment ready
- [ ] Complete setup steps
- [ ] Read [CLAUDE_CODE_GUIDE.md](CLAUDE_CODE_GUIDE.md)
- [ ] Run Use Case 1 - Simple Sine Wave
- [ ] Try the challenges
- [ ] Continue through use cases
- [ ] Build a project

---

## 📚 Files in This Repository

```
.
├── README.md                      # This file
├── SETUP.md                       # Infrastructure & setup guide
├── CLAUDE_CODE_GUIDE.md           # FFT learning with prompts
├── toolchain-diagram.svg          # Visual architecture
├── requirements.txt               # Python dependencies
└── .gitignore                     # Git ignore rules
```

---

## 🌟 Next Steps

**Ready? Start with [SETUP.md](SETUP.md)** 🚀

---

## 📝 License

MIT License - Use freely for learning and teaching!

---

*Last updated: June 2026*
*Works with Claude Haiku 4.5, Claude Sonnet 4.6, and newer versions*
