# GitHub Codespaces + Safari PWA + Claude Code

This is the definitive guide for a "maximum curiosity, minimum friction" AI coding environment. Optimized for the 11-inch iPad Pro with a Bluetooth keyboard and mouse.

---

## Phase 1: The "Brain" (GitHub Codespaces)

GitHub Codespaces provides the remote Linux environment. This handles the compute, saving your iPad's battery and processing power.

### 1.1 Create the Repository

- Go to GitHub.com and create a new private repository (e.g., financial-sims).

### 1.2 Initialize the Codespace

- Click the green "<> Code" button.
- Select the Codespaces tab and click "Create codespace on main."
    

### 1.3 Financial Safety (5-Minute Timeout)

- Go to GitHub Codespaces Settings in your profile.
- Set the "Default idle timeout" to 5 minutes.
- Couch Potato Logic: If you close your iPad cover or fall asleep, the machine stops billing you for compute 5 minutes later.
    

---

## Phase 2: The "Screen" (Safari PWA Setup)

On an 11-inch screen, browser tabs waste 15% of your space. Use the PWA (Progressive Web App) method to go full-screen.

### 2.1 Create the App

- Open your Codespace in Safari.
- Tap the Share icon (square with up arrow).
- Select "Add to Home Screen."
- Rename it "Claude Code" and save.
    
### 2.2 Launch & Layout

- Open the new "Claude Code" app from your Home Screen.
- Use Cmd + B to hide the sidebar explorer.
- Use Ctrl + ` (backtick) to open the terminal.
- 11-inch Tip: If the text is too small, press Cmd + , (comma), search for "Terminal Font Size," and set it to 14.
    
---

## Phase 3: The "Hands" (Installing Claude Code)

Claude Code is the CLI agent that writes code and executes terminal commands.

### 3.1 Installation

In the Codespace terminal, run:

npm install -g @anthropic-ai/claude-code

### 3.2 Authentication

- Type "claude" and press Enter.
- Follow the URL to authorize the CLI via your Anthropic account.
    

### 3.3 The Constitution (CLAUDE.md)

Create a CLAUDE.md file in the root directory:

- Tech Stack: Python (FastAPI/Pandas).
- Style: Simple, elegant, readable.
- Tone: No over-engineering; "couch potato" efficiency.

---

## Phase 4: The Workflow (Prompt-Based Coding)

### 4.1 Persistence with tmux

Before starting Claude, always type:

"tmux"

Why: If your iPad refreshes or you switch apps, your work stays active. To reconnect later, type "tmux a".

### 4.2 Interactive Coding

Type "claude" to enter interactive mode.

- Prompting: "Claude, build a Python script for a Monte Carlo tax simulation using the rules in CLAUDE.md."
- Reviewing: Use your Bluetooth mouse to scroll through the code changes (diffs).
- Approving: Hit the Approve button or type "y" to apply changes.
    
### 4.3 Testing

Tell Claude: "Run the simulation and output the results in a clean table."

### 4.4 Exit Routine

1. Type "/exit" inside Claude.
2. Type "exit" in the terminal to close the tmux session.
3. Finish: Close the iPad cover. The 5-minute timeout handles the rest.