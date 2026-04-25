# The "Power Potato" Setup: Detailed AI Coding Guide
## iPad Pro + GitHub Codespaces + Blink Shell + Claude Code

This document outlines the professional "couch potato" workflow for agentic AI coding. By combining cloud-hosted compute with a native iPad terminal, you achieve a "maximum curiosity, minimum friction" environment that works anywhere.

---

## Phase 1: The "Brain" (GitHub Codespaces)
GitHub Codespaces provides a dedicated Linux machine in the cloud. This ensures your iPad isn't doing the heavy lifting, saving battery and providing a true development environment.

### 1.1 Create the Repository
* Navigate to [GitHub.com](https://github.com) and create a new repository (e.g., `ai-dev-setup`). 
* **Note:** For personal projects like tax simulations or private data, ensure the repository is set to **Private**.

### 1.2 Initialize the Codespace
* Click the green **"<> Code"** button.
* Select the **Codespaces** tab.
* Click **"Create codespace on main"**. GitHub will spin up a virtual machine (VM) with a pre-configured VS Code environment.

### 1.3 Financial Guardrails (Crucial)
To prevent racking up charges if you fall asleep on the couch:
* Go to [GitHub Codespaces Settings](https://github.com/settings/codespaces).
* Under **"Default idle timeout"**, set the value to **5 minutes**. 
* This ensures that 5 minutes after you close your iPad cover or disconnect, the VM shuts down and compute charges stop.

---

## Phase 2: The "Link" (Blink Shell to Codespaces)
While you can use Safari, **Blink Shell** is a native iPad app that handles Bluetooth keyboards/mice perfectly and maintains connections even if you switch apps.

### 2.1 Install and Key Generation
* Install [Blink Shell](https://apps.apple.com/app/blink-shell-build-code/id1156707581) from the App Store.
* Open Blink and type `config`.
* Select **Keys** > **Add New**. Name it `iPad-Pro-Key`.
* Tap the new key and select **"Copy Public Key"**.

### 2.2 Link to GitHub
* Go to [GitHub SSH Settings](https://github.com/settings/keys).
* Click **New SSH Key**, give it a title (e.g., "iPad Pro Blink"), and paste the key you copied.

### 2.3 Establishing the SSH Tunnel
* In the Blink terminal, type:
  ```bash
  gh auth login
  ```
* Follow the prompts to authenticate via your browser.
* Once logged in, type:
  ```bash
  gh codespace ssh
  ```
* Select your active Codespace. You are now controlling your remote Linux "Brain" directly from the iPad terminal.

---

## Phase 3: The "Hands" (Installing Claude Code)
Claude Code is the CLI-based agent from Anthropic that can read files, write code, and execute terminal commands.

### 3.1 Installation
Inside your Blink terminal (connected to the Codespace), run:
```bash
npm install -g @anthropic-ai/claude-code
```

### 3.2 Authentication
* Type `claude` and press Enter.
* You will be given a one-time 8-digit code and a URL.
* Open the URL in Safari, log in to your Anthropic account, and enter the code to authorize the CLI.

### 3.3 Set the "Constitution" (CLAUDE.md)
Create a file in your project root called `CLAUDE.md`. This provides persistent context for the AI:
```markdown
# Project Rules
- Tech Stack: Python, Pandas (for data science).
- Style: Simple, elegant, readable.
- Tone: Minimum friction, "couch potato" efficiency.
```

---

## Phase 4: The Workflow (Prompt-Based Coding)
With your Bluetooth keyboard and mouse connected, you can now build applications using natural language.

### 4.1 Persistence with tmux
Before starting Claude, always type `tmux`. 
* **Why:** If you lose your Wi-Fi connection or switch to another app, your session stays alive on the server. To reconnect, just type `tmux attach`.

### 4.2 Starting a Coding Session
Type `claude` to enter the interactive mode. You can now issue complex instructions:
* **Creation:** *"Claude, create a Python script that pulls my CSV tax data and runs a Monte Carlo simulation for retirement spending."*
* **Refactoring:** *"Rewrite this function to be more efficient and add docstrings."*
* **Execution:** *"Run the script and tell me if it produces any errors."*

### 4.3 Review and Approval
* Claude will present a "diff" (a visual representation of changes).
* Use your mouse to scroll through the changes.
* Type `y` or hit the **Approve** button to apply the changes to your actual files.

### 4.4 Clean Exit
When finished:
1. Type `/exit` inside Claude.
2. Type `exit` to close the SSH tunnel.
3. Close your iPad. Your 5-minute timeout will handle the rest.
