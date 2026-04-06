# Gemini AI Studio — Orientation Workbook

> Google's AI Code Generator — TypeScript, Python, Firebase — on iPad  
> *Learn the tool before you rely on it — this workbook gets you fluent in AI Studio*

**Tools:** Gemini AI Studio • Google IDX • Firebase • Edge • iPad

---

## Part 0 — What is Gemini AI Studio?

Google AI Studio (aistudio.google.com) is a free, browser-based interface for
Google's Gemini AI models. For your workflow it serves one primary purpose:
**you describe what you want to build, Gemini writes the code, you paste it into IDX.**

Think of it as a senior developer sitting next to you who never gets tired,
never judges your questions, and can write TypeScript and Python fluently.

### 0.1 Where It Fits in Your Toolchain

```
Edge Tab 1 — AI Studio          Edge Tab 2 — Google IDX         Edge Tab 3 — Firebase
──────────────────────          ───────────────────────         ──────────────────────
Describe what you want   →      Paste code, run it,      →      Results saved to
Gemini writes the code          fix errors in terminal           Firestore database
                         ←      Paste errors back for fixes
```

### 0.2 What It Can and Cannot Do

| Can Do | Cannot Do |
|---|---|
| Write complete TypeScript and Python | See your IDX environment directly |
| Fix errors you paste in | Remember previous conversations |
| Explain code line by line | Guarantee code always works first time |
| Suggest architecture and approaches | Access your Firebase data |
| Answer coding questions instantly | Run or test code itself |
| Work in any browser on iPad | Replace your judgment on what to build |

### 0.3 Getting In

1. Open Edge on your iPad
2. Go to [aistudio.google.com](https://aistudio.google.com)
3. Sign in with your Google account — same one as IDX and Firebase
4. Tap **New prompt** in the left sidebar
5. You are ready

> **TIP:** AI Studio saves every conversation automatically. You can return to any
> previous session and continue where you left off. Good prompts are worth saving.

---

## Part 1 — The Interface

### 1.1 Key Areas

| Area | What It Does | How You Use It |
|---|---|---|
| Prompt box | Where you type your request | Describe what you want Gemini to build |
| Response area | Where Gemini replies | Read code here, copy it, paste into IDX |
| Model selector | Which Gemini version | Pick your model before prompting |
| System Instructions | Background context | Set once per session — shapes all responses |
| Temperature slider | Controls creativity vs precision | Lower for code, higher for ideas |
| Token counter | Shows prompt length | Keep an eye on this for long sessions |
| Run button / Enter | Sends your prompt | Shift+Enter for new line, Enter to send |

### 1.2 Which Model to Use

| Model | Speed | Best For |
|---|---|---|
| **Gemini 2.0 Flash** | Fast | Everyday code generation — use this most |
| **Gemini 1.5 Pro** | Medium | Complex multi-file problems, long context |
| **Gemini 2.0 Pro** | Slower | Hardest problems, most capable reasoning |

**Start with Gemini 2.0 Flash** for everything in your workbooks.
Switch to 1.5 Pro or 2.0 Pro only if Flash gives you incomplete or confused results.

### 1.3 Temperature Setting

The temperature slider controls how predictable vs creative Gemini's output is.

| Temperature | Behavior | Use When |
|---|---|---|
| 0.0 — 0.3 | Precise, deterministic, consistent | Writing production code |
| 0.4 — 0.7 | Balanced | General coding and explanations |
| 0.8 — 1.0 | Creative, varied, sometimes surprising | Brainstorming, architecture ideas |

> **Set temperature to 0.2** for all code generation in your workbooks.
> You want reliable, consistent output — not creative surprises in your TypeScript.

---

## Part 2 — System Instructions

System Instructions are a hidden background prompt that shapes every response
in the session. Setting this correctly is the single most impactful thing
you can do to get better code from Gemini.

### 2.1 Set This at the Start of Every Session

Tap **System Instructions** and paste this:

```
I am building TypeScript and Python projects in Google IDX on iPad.

TypeScript projects:
- Vanilla TypeScript — no frameworks
- Firebase Web SDK v9 modular imports
- Target: browser, runs from index.html + main.ts + style.css

Python projects:
- Python 3, Google IDX terminal environment
- Libraries available: numpy, matplotlib, pandas, scipy, firebase-admin
- Firebase: use firebase-admin, db client already initialized

Always:
- Give me complete, runnable code I can paste directly into IDX
- Include all imports at the top of every file
- Use TypeScript interfaces for all data structures
- Add brief comments explaining non-obvious logic
```

### 2.2 Why This Matters

Without system instructions Gemini might:
- Write React or Node.js code when you want vanilla TypeScript
- Use old Firebase v8 syntax instead of v9 modular imports
- Give you partial snippets that need assembly
- Write Python assuming a Jupyter environment instead of IDX terminal

With system instructions set correctly, every response is automatically
calibrated to your exact environment.

---

## Part 3 — The Prompt Formula

### 3.1 The Four Parts of a Good Prompt

Every good coding prompt has these four parts:

```
1. CONTEXT:   What you are building and where it runs
2. TASK:      Exactly what you need right now
3. DATA:      Current code, errors, or Firebase details
4. FORMAT:    How to deliver the output
```

### 3.2 The Master Template — TypeScript

```
I am adding [FEATURE] to my [PROJECT] TypeScript project in Google IDX.

TypeScript interfaces needed:
  [Interface name] { field: type, field: type }

Requirements:
- [Requirement 1]
- [Requirement 2]
- Save to Firebase collection '[name]'
  Fields: field1, field2, timestamp
- Use Firebase Web SDK v9 modular imports
- Here is my Firebase config: [paste firebaseConfig]

Here is my current main.ts: [paste current code]

Give me complete updated index.html, main.ts, and style.css.
```

### 3.3 The Master Template — Python

```
I am writing Python in Google IDX terminal.
numpy, matplotlib, pandas, scipy, firebase-admin all installed.
Firebase db client already initialized.

Write a script that:
- [What it should do]
- Save results to Firebase collection '[name]'
  Fields: [list fields], timestamp

Give me complete Python code I can save as [filename].py
and run with python3.
```

### 3.4 Good vs Bad Prompts

| Bad Prompt | Good Prompt |
|---|---|
| Make a card game | Create a Blackjack game in vanilla TypeScript. Single HTML file. Green felt background, Hit/Stand/New Game buttons, hand value display. |
| Add Firebase | Add Firebase Web SDK v9 to my main.ts. Save game results to collection 'blackjack_games' with fields: result, playerTotal, dealerTotal, timestamp. Here is my config: [paste] |
| Fix it | I have this TypeScript error in IDX: [paste error]. Here is the relevant code: [paste]. Fix the type issue. |
| Make it better | Improve the visual design: add card drop shadows, slide-in animation when cards are dealt, result message flashes green for win and red for loss. |

---

## Part 4 — Test Prompts: TypeScript

Work through these in order. Each one tests a different type of prompt.

### 4.1 Code Generation from Scratch

Copy this prompt exactly into AI Studio:

```
I am building a simple TypeScript utility in Google IDX.
Write a complete main.ts that:
- Defines a Card interface: { suit: string, value: number, display: string }
- Creates a function createDeck(): Card[] that builds a shuffled 52-card deck
- Uses Fisher-Yates shuffle algorithm
- Logs the first 5 cards of the shuffled deck to console
- Logs the total count (should be 52)
Give me complete main.ts with all types and functions.
```

Paste Gemini's response into IDX and run:

```bash
tsc main.ts && node main.js
```

> **CHECKPOINT 1:** You should see 5 cards logged and count=52. If TypeScript errors appear paste them back to Gemini for fixes. ✓

### 4.2 Updating Existing Code

Take the `main.ts` from Checkpoint 1 and ask Gemini to extend it:

```
Update my TypeScript card deck code. Add:
- A function calculateHandValue(hand: Card[]): number
  Aces count as 11 unless that causes the total to exceed 21, then count as 1
- Test it with these hands:
  [Ace, King] should return 21
  [Ace, King, Five] should return 16 (Ace drops to 1)
  [Ace, Ace, Nine] should return 21 (one Ace=11, one Ace=1)
- Log the results of all three tests
Here is my current main.ts: [paste your code]
Give me the complete updated main.ts.
```

Run it in IDX and verify the three test cases produce the right results.

> **CHECKPOINT 2:** All three Ace calculations are correct. ✓

### 4.3 Fixing an Error

Deliberately introduce a bug — change `hand: Card[]` to `hand: card[]` (lowercase c)
in your calculateHandValue function. Then ask Gemini:

```
I have this TypeScript error in Google IDX:
[paste the exact error message from IDX terminal]
Here is the relevant code:
[paste the function with the bug]
Fix the type error.
```

> **CHECKPOINT 3:** Gemini identifies and fixes the type error correctly. ✓

### 4.4 Code Explanation

Paste any function from your code and ask:

```
Explain what this TypeScript function does line by line in plain English.
Assume I am new to TypeScript.
[paste the calculateHandValue function]
```

> **CHECKPOINT 4:** Gemini explains each line clearly without jargon. ✓

---

## Part 5 — Test Prompts: Python

### 5.1 Python Code Generation

```
I am writing Python in Google IDX terminal.
numpy installed. np.random.seed(42) already set.
Write a Monte Carlo Pi estimation script:
- Throw 100,000 random (x,y) points in [-1,1] using NumPy (no Python loops)
- Count how many land inside the unit circle (x^2 + y^2 <= 1)
- Pi = 4 * (inside count) / total
- Print: estimated Pi, true Pi, error
Give me complete Python code to save as pi_test.py and run with python3.
```

In IDX terminal:

```bash
python3 pi_test.py
```

> **CHECKPOINT 5:** Pi estimate is close to 3.14159. ✓

### 5.2 Python Error Fixing

Ask Gemini to write code with a deliberate mistake:

```
I am writing Python in Google IDX.
Write a function that computes the mean of a list using numpy.
Intentionally use the wrong numpy function name so it causes an AttributeError.
```

Then take the broken code, run it in IDX, paste the error back:

```
I got this error running my Python script in IDX:
[paste the AttributeError]
Here is my code:
[paste code]
Fix it.
```

> **CHECKPOINT 6:** Gemini correctly identifies and fixes the AttributeError. ✓

---

## Part 6 — Test Prompts: Firebase

### 6.1 Firebase TypeScript Integration

```
Add Firebase Firestore to my TypeScript card deck project in Google IDX.
Use Firebase Web SDK v9 modular imports.
After creating the deck, save a summary document to collection 'deck_tests' with:
  deckSize: number
  firstCard: string  (display of first card e.g. 'A of Spades')
  timestamp: Timestamp.now()
Here is my Firebase config: [paste your firebaseConfig from Firebase Console]
Here is my current main.ts: [paste current code]
Give me complete updated main.ts with Firebase integrated.
```

Run in IDX, then check Firebase Console > Firestore > `deck_tests`.

> **CHECKPOINT 7:** Document appears in Firebase Console with correct fields. ✓

### 6.2 Firebase Python Integration

```
I am writing Python in Google IDX terminal.
firebase-admin installed. 
Write a script that:
- Connects to Firebase using service account at '../firebase/service-account.json'
- Saves a test document to collection 'python_tests' with:
  message: 'Python Firebase test'
  value: 42
  timestamp: current UTC datetime
- Reads it back and prints it
Give me complete Python code to save as firebase_test.py.
```

> **CHECKPOINT 8:** Document saved and read back correctly. ✓

---

## Part 7 — Advanced Techniques

### 7.1 Using Gemini for Architecture

Before writing any code for a new feature, ask Gemini to think through the design:

```
I am building a Blackjack game in TypeScript in Google IDX.
Before writing any code, help me design the architecture:
- What TypeScript interfaces do I need?
- What are the main functions and their signatures?
- What game state needs to be tracked?
- How should I structure my main.ts?
Just give me the architecture plan — no code yet.
```

Then once you agree with the design, ask for the implementation.

### 7.2 Iterative Development

Never ask for everything at once. Build in layers:

```
Prompt 1: Just the TypeScript types and interfaces
Prompt 2: Just the core logic functions
Prompt 3: Just the DOM rendering
Prompt 4: Just the event handlers
Prompt 5: Just the Firebase integration
```

Each prompt builds on the last. Paste current code each time.

### 7.3 Asking Gemini to Review Your Code

```
Review this TypeScript code for:
- Type safety issues
- Logic bugs
- Missing edge cases
- Any improvements to suggest
[paste your code]
Don't rewrite it — just point out the issues.
```

### 7.4 The Rubber Duck Technique

When stuck, describe your problem to Gemini in plain English
before asking for code:

```
I am trying to implement Ace handling in Blackjack.
An Ace can count as 1 or 11. If counting as 11 would bust the hand,
it should count as 1. A hand can have multiple Aces.
Can you explain the logic I need before I ask you to write it?
```

---

## Part 8 — The Gemini Sidebar in IDX

IDX has Gemini built into the right sidebar — you do not always need AI Studio.

### When to Use the IDX Sidebar

- Quick questions about a specific function
- Explaining what a piece of code does
- Small fixes and tweaks
- "What does this error mean?"

### When to Use AI Studio

- Generating complete new files
- Complex multi-requirement prompts
- When you want to set System Instructions
- When you want to save and reuse a prompt
- Longer back-and-forth conversations

### How to Open the Gemini Sidebar in IDX

1. Look for the Gemini sparkle icon in the right sidebar
2. Tap it to open the chat panel
3. Ask your question directly — it has context of your open files

> **CHECKPOINT 9:** Ask the IDX Gemini sidebar to explain any function in your current open file. It should give a clear explanation. ✓

---

## Part 9 — Verdict and Scorecard

### 9.1 Checkpoint Scorecard

| # | What It Tests | Pass? |
|---|---|---|
| 1 | TypeScript code generation from scratch | ☐ |
| 2 | Updating existing TypeScript code | ☐ |
| 3 | Fixing a TypeScript error | ☐ |
| 4 | Code explanation in plain English | ☐ |
| 5 | Python code generation | ☐ |
| 6 | Python error fixing | ☐ |
| 7 | Firebase TypeScript integration | ☐ |
| 8 | Firebase Python integration | ☐ |
| 9 | Gemini sidebar in IDX | ☐ |

### 9.2 What the Score Means

| Score | Verdict |
|---|---|
| 9/9 | You are fluent in AI Studio — start your workbooks |
| 7-8/9 | Solid — note which checkpoints failed and revisit |
| 5-6/9 | Review Parts 3 and 4 — prompt formula needs work |
| 0-4/9 | Work through the prompts again more carefully |

### 9.3 Common Issues and Fixes

| Issue | Fix |
|---|---|
| Gemini gives partial code | Add "Give me the complete file" to your prompt |
| Code uses wrong Firebase syntax | Add "Use Firebase Web SDK v9 modular imports" |
| Code uses React or a framework | Add "Vanilla TypeScript only — no frameworks" |
| Code won't compile in IDX | Paste the exact error back to Gemini |
| Response is too short | Add "Include all helper functions and imports" |
| Response is too verbose | Add "Be concise — code only, minimal explanation" |

---

## Quick Reference Card

### TypeScript Prompt Endings

```
Give me complete index.html, main.ts, and style.css.
Include all imports at the top of each file.
Use Firebase Web SDK v9 modular imports.
```

### Python Prompt Endings

```
Give me complete Python code I can save as [filename].py
and run with python3 in Google IDX terminal.
```

### Error Fixing Template

```
I have this error in Google IDX:
[paste exact error]
Here is the relevant code:
[paste code]
Fix it and explain what was wrong.
```

### The Golden Rules

1. **Always paste your current code** when asking for updates
2. **One feature at a time** — smaller prompts get cleaner code
3. **Set System Instructions** at the start of every session
4. **Temperature 0.2** for all code generation
5. **Paste errors straight back** — don't try to fix them yourself first
6. **Test in IDX** before trusting any Gemini output

---

> *Gemini AI Studio • TypeScript • Python • Google IDX • Firebase • iPad*  
> *MSC Meraviglia — Starlink Maritime*
