# 📱 Blink Shell -- Cheat Sheet

**iPad Terminal for the Atlantic Data Lab Workbook**

-----

## Blink Basics

|Action               |How                                      |
|---------------------|-----------------------------------------|
|Open new shell       |`Cmd + T`                                |
|Close shell          |`Cmd + W`                                |
|Switch between shells|`Cmd + [` / `Cmd + ]` or swipe left/right|
|Scroll up in terminal|Two-finger swipe up                      |
|Open config screen   |Type `config` + Enter                    |
|Full screen          |`Cmd + Shift + F`                        |
|Font size up/down    |`Cmd + +` / `Cmd + -`                    |

-----

## Connecting to Your Droplet

```bash
# First time -- set up the host in config
config                        # Open Blink settings
# Hosts > New Host > fill in Label, Hostname, User: root

# Connect
ssh AI-Server                 # Uses saved host config
mosh AI-Server                # Preferred -- survives Starlink drops

# If connecting manually
ssh root@YOUR_DROPLET_IP
mosh root@YOUR_DROPLET_IP
```

> **Always use `mosh` not `ssh`** -- if Starlink drops or the ship moves, Mosh reconnects automatically. `ssh` will hang and die.

-----

## Navigation -- Once Connected

```bash
pwd                           # Show current directory
ls                            # List files
ls -la                        # List with details + hidden files
cd ~                          # Go to home directory
cd ~/Cruise-Workbook-2026     # Go to your project
cd Essentials                 # Go into subfolder
cd ..                         # Go up one level
cd ../Analytics               # Up one, into Analytics
clear                         # Clear the screen
```

-----

## Files & Folders

```bash
mkdir Essentials              # Create a folder
mkdir -p Essentials Analytics Lab   # Create all 3 at once
touch weather.py              # Create an empty file
cp weather.py weather_backup.py     # Copy a file
mv oldname.py newname.py      # Rename a file
rm test.py                    # Delete a file (no undo)
rm -rf foldername             # Delete a folder (careful)
cat weather.py                # Print file contents to screen
```

-----

## Running Your 8 Apps

```bash
cd ~/Cruise-Workbook-2026

# Essentials
python3 Essentials/weather.py
python3 Essentials/utils.py
python3 Essentials/logger.py
python3 Essentials/bj_simple.py

# Analytics
python3 Analytics/bj_pro.py
python3 Analytics/backgammon.py

# Lab
python3 Lab/monte_carlo.py
python3 Lab/bayesian_engine.py
```

-----

## Python & Packages

```bash
python3 --version             # Confirm Python is installed
pip3 install numpy            # Install a package
pip3 install numpy pandas     # Install multiple
pip3 list                     # See installed packages
pip3 show numpy               # Info about a specific package
```

-----

## Claude Code

```bash
claude --version              # Confirm install + version
claude                        # Start interactive session
claude --server-mode          # Start Remote Control (then press Space for QR)
claude update                 # Update to latest version

# Inside a Claude Code session
/cost                         # Show token usage + spend this session
/status                       # Check connection and model
/clear                        # Clear conversation context
exit                          # End the session
```

-----

## Git -- The Essentials

```bash
git status                    # See what's changed
git pull                      # Pull latest from GitHub
git add .                     # Stage all changed files
git add Essentials/weather.py # Stage one specific file
git commit -m "Add weather app"  # Commit with message
git push                      # Push to GitHub
git log --oneline             # See recent commits
git diff                      # See exactly what changed
```

-----

## Useful System Commands

```bash
# Check the server is healthy
top                           # Live CPU/memory usage (q to quit)
df -h                         # Disk space
free -h                       # RAM usage
uptime                        # How long the Droplet has been running

# Find things
find . -name "*.py"           # Find all Python files in current dir
grep -r "estimate_pi" .       # Search inside files for text

# Network
ping google.com               # Test internet connection
curl -I https://google.com    # Test HTTPS connectivity
```

-----

## Keyboard Shortcuts Inside the Terminal

|Shortcut  |What It Does                          |
|----------|--------------------------------------|
|`Ctrl + C`|Kill the running process              |
|`Ctrl + Z`|Suspend process (bring back with `fg`)|
|`Ctrl + L`|Clear screen (same as `clear`)        |
|`Ctrl + A`|Jump to start of line                 |
|`Ctrl + E`|Jump to end of line                   |
|`Ctrl + U`|Delete everything before cursor       |
|`Ctrl + W`|Delete the last word                  |
|`↑` / `↓` |Scroll through command history        |
|`Tab`     |Autocomplete file/folder names        |
|`!!`      |Repeat last command                   |
|`!py`     |Repeat last command starting with `py`|

-----

## Mosh -- What It Handles For You

|Problem                  |Without Mosh           |With Mosh                  |
|-------------------------|-----------------------|---------------------------|
|Starlink drops for 10 sec|Session dies           |Reconnects silently        |
|Ship moves, IP changes   |SSH hangs              |Mosh follows automatically |
|iPad goes to sleep       |Connection lost        |Picks up where you left off|
|Port change at sea       |Must reconnect manually|Transparent handoff        |

-----

## Quick Troubleshooting

```bash
# Command not found after install
source ~/.bashrc              # Reload shell profile

# Claude Code auth error
echo $ANTHROPIC_API_KEY       # Check the key is set
source ~/.bashrc              # Reload if you just added it

# Permission denied
ls -la                        # Check file permissions
chmod +x script.py            # Make a file executable

# Python package missing
pip3 install PACKAGE_NAME --break-system-packages

# Droplet unreachable
# → Check DigitalOcean console -- Droplet may need a reboot
# → Try: mosh root@YOUR_DROPLET_IP (direct IP as fallback)
```

-----

## The Full Workflow in One View

```
iPad (Blink)
  └── mosh AI-Server
        └── DigitalOcean Droplet
              ├── claude --server-mode  ← Space bar → QR code
              │     └── Claude Mobile App (iPad) scans QR
              │           └── Type prompts → apps get built
              ├── python3 Essentials/weather.py  ← run apps
              └── git push  ← sync to GitHub → Working Copy
```

-----

*Blink Shell · DigitalOcean · Claude Code · Starlink Maritime*
*MSC Meraviglia -- 2026*