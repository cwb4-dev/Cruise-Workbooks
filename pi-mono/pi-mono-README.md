# Pi-Mono Workbook -- iPad SSH Edition

> 3 projects · Blink Shell + remote server · open source

-----

This workbook walks you through installing and using **pi-mono**’s coding agent (`pi`) from your iPad over SSH. Pi is a minimal terminal AI agent -- just four tools (read, write, edit, bash) -- that you direct with plain English. Each project below is a self-contained experiment to help you learn how pi thinks and works.

> ⚡ Pi runs on your *remote server*, not on the iPad itself. Your iPad is just the terminal screen. You’ll need a VPS, cloud VM, or any Linux machine you can SSH into.

-----
Your workbook is ready. Here’s what’s inside:
Phase 1 -- Setup walks you through Blink Shell on iPad → SSH to your server → install Node → install pi → add your API key → run a sanity check. Includes a Mosh tip for cruise ship wifi.
3 Projects:
	1.	Static Site Generator -- pure Node.js Markdown-to-HTML blog, no dependencies. Good first run to see how pi scaffolds a whole project.
	2.	CLI To-Do App -- builds a real td command you can actually use, with color output and priorities. Great for watching pi use bash to test its own work.
	3.	TypeScript API Wrapper -- wraps the free Open-Meteo weather API, full types, then has pi write a publish-ready README. Pushes pi harder.
Each project has copy-able prompts in sequence, a clickable checklist with a progress bar, and tips on what to watch for in pi’s behavior. The copy buttons grab the shell commands cleanly for easy pasting from Blink

-----

## Phase 1 -- iPad + Server Setup

### Step 1 · iPad terminal app

Use **Blink Shell** (best SSH/Mosh experience on iPad, $19.99/yr) or **a-Shell** (free). Blink supports Mosh for resilient connections on spotty wifi.

```bash
# SSH into your server:
ssh user@your-server.com

# Or with Mosh (survives network drops -- great for cruise wifi):
mosh user@your-server.com
```

### Step 2 · Server prerequisites

On your remote Linux server, you need Node.js 20+ and npm.

```bash
# Check versions
node --version   # needs 20+
npm --version    # needs 9+

# If missing, install via nvm (easiest):
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm install 22
nvm use 22
```

### Step 3 · Install pi

```bash
# One-line install (recommended)
curl -fsSL https://pi.dev/install.sh | bash

# OR via npm
npm install -g @mariozechner/pi-coding-agent

# Verify
pi --version
```

### Step 4 · Add your API key

Pi supports Anthropic, OpenAI, Google, and more. Pick one and export your key.

```bash
# Anthropic (Claude) -- recommended
export ANTHROPIC_API_KEY="sk-ant-..."

# Or OpenAI
export OPENAI_API_KEY="sk-..."

# Make permanent -- add to ~/.bashrc or ~/.zshrc:
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.bashrc
source ~/.bashrc
```

> → If you have a Claude Pro/Max subscription, you can auth via `/login` inside pi instead of using an API key.

### Step 5 · Sanity check

```bash
mkdir ~/pi-sandbox && cd ~/pi-sandbox
pi "Say hello and list the files in this directory"
```

Pi should respond and run `ls`. If it does, you’re ready.

-----

## Project 1 -- Static Site Generator

**Difficulty:** Beginner  
**What you’re building:** A tiny Markdown-to-HTML blog generator. Pure Node.js, no frameworks, pi does the whole build.

### Setup

```bash
mkdir -p ~/pi-projects/blog && cd ~/pi-projects/blog
pi   # launch pi interactively
```

### Prompts -- run in order

**Prompt 1 -- scaffold**

```
Create a Node.js project here that converts Markdown files in a /posts folder into HTML files in a /dist folder. Use no external dependencies -- just Node's built-in fs and path modules. Create a simple Markdown parser that handles headings, bold, italic, links, and paragraphs.
```

**Prompt 2 -- add content**

```
Create 3 sample blog posts in /posts as .md files. First post about learning to code on an iPad. Second about minimalist tools. Third about open source AI agents. Give them realistic content, not Lorem Ipsum.
```

**Prompt 3 -- layout**

```
Add a shared HTML template with a dark-themed CSS stylesheet. Include a navigation header and a footer. Make it look clean and readable. Regenerate all the HTML files using this template.
```

**Prompt 4 -- index page**

```
Generate an index.html that lists all posts with their titles and a one-sentence excerpt. Sort them by filename. Add a build script in package.json so I can run "npm run build" to regenerate everything.
```

### Checklist

- [ ] Pi generates project structure and package.json
- [ ] 3 markdown posts created in /posts
- [ ] HTML files appear in /dist after running build
- [ ] Dark CSS theme applied to all pages
- [ ] index.html lists all posts
- [ ] `npm run build` works cleanly

> → Pi’s bash tool will run your build script for you. Ask: *"Run npm run build and show me any errors."*

-----

## Project 2 -- CLI To-Do App

**Difficulty:** Intermediate  
**What you’re building:** A command-line task manager that stores todos as JSON. Tests pi’s ability to design a clean API, handle state, and write usable UX.

### Setup

```bash
mkdir -p ~/pi-projects/todo && cd ~/pi-projects/todo
pi
```

### Prompts -- run in order

**Prompt 1 -- core**

```
Build a CLI todo app in Node.js called "td". It should store tasks in ~/.td/tasks.json. Commands: td add "task name", td list, td done [id], td delete [id], td clear. Each task gets an auto-incrementing id, a title, a done flag, and a created timestamp. No external dependencies.
```

**Prompt 2 -- usability**

```
Make td list output nicely formatted with colors using ANSI escape codes. Show done tasks with a strikethrough. Group incomplete tasks first, then completed ones. Add a count summary at the bottom like "3 pending, 2 done".
```

**Prompt 3 -- install it**

```
Make td globally available. Add a proper shebang line, make the file executable, and either use npm link or create a symlink in ~/bin so I can run "td" from anywhere. Then test it works by adding 3 tasks and listing them.
```

**Prompt 4 -- bonus: priorities**

```
Add an optional priority flag to td add: "td add 'Fix bug' --high". Priorities are low, medium (default), high. Show priority in td list output with a color-coded indicator. Update the storage format to include priority.
```

### Things to notice while pi works

- **Tool use** -- watch pi use bash to run `chmod +x` and test the app itself, iterating on errors automatically.
- **Steering** -- while pi is working, press Enter to send a steering message mid-run without waiting for it to finish.

### Checklist

- [ ] `td add` / `list` / `done` / `delete` all work
- [ ] Tasks persist between terminal sessions
- [ ] Colored, readable output in list
- [ ] `td` works from any directory
- [ ] Priority flags implemented

-----

## Project 3 -- TypeScript API Wrapper + README

**Difficulty:** Advanced  
**What you’re building:** A small TypeScript library wrapping a public API, plus a full README and publish-ready package.json. Tests pi’s ability to produce *complete* software artifacts.

### Setup

```bash
mkdir -p ~/pi-projects/weather-sdk && cd ~/pi-projects/weather-sdk
pi
```

### Prompts -- run in order

**Prompt 1 -- scaffold TypeScript project**

```
Create a TypeScript npm package called "open-weather-sdk" that wraps the Open-Meteo API (https://open-meteo.com -- it's free, needs no API key). Set up tsconfig.json, package.json with build script, and a src/index.ts entry point. Install typescript as a dev dependency.
```

**Prompt 2 -- build the client**

```
In src/index.ts, build a WeatherClient class with these methods: getCurrentWeather(lat, lon) returns temperature, windspeed, weathercode. getForecast(lat, lon, days) returns an array of daily forecasts with max/min temp. Use the fetch API, handle errors properly, and export full TypeScript types for all return values.
```

**Prompt 3 -- test it**

```
Build the project and write a quick test script in examples/test.ts that fetches current weather for New York City (40.71, -74.00) and prints it. Run it with ts-node or after building. Fix any type errors.
```

**Prompt 4 -- write the docs**

```
Write a complete README.md for this package as if it's going to be published on npm. Include: a badge row, installation instructions, quick start example, full API reference with TypeScript signatures, the list of weather codes mapped to descriptions, and a contributing section. Make it genuinely useful, not just a template.
```

### Checklist

- [ ] TypeScript project builds without errors
- [ ] WeatherClient fetches real data from Open-Meteo
- [ ] Return types are fully typed
- [ ] Example script runs and prints weather
- [ ] README is complete and publish-ready
- [ ] package.json has correct `main`/`types`/`exports` fields

-----

## Pi Cheat Sheet

### Session management

```bash
pi -c           # resume last session
pi -r           # browse and pick a session
pi --no-session # ephemeral, don't save
```

### Model switching

```bash
# At launch:
pi --model sonnet:high

# Inside a session:
/model          # opens model picker
```

### Non-interactive mode

```bash
pi -p "Summarize this codebase"
cat file.ts | pi -p "Review this code"
```

### Update pi

```bash
pi update         # update pi + all packages
pi update --self  # pi only
```

> ⚡ Pi packages run with full system access. Only install packages from sources you trust.

-----

## Bonus -- Share your sessions

If you do open source work with pi, you can contribute sessions back to help improve models.

```bash
# Needs a Hugging Face account + HF CLI
pip install huggingface_hub
huggingface-cli login

# Install the share tool:
pi install git:github.com/badlogic/pi-share-hf
```

-----

*pi-mono · github.com/badlogic/pi-mono · pi.dev*