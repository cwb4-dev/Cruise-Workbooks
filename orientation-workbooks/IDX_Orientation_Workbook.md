# Google IDX — Orientation Workbook

> Google's Browser IDE — TypeScript, Python, Firebase, CLI — on iPad  
> *Kick the tires before committing — this workbook tests IDX on your iPad*

**Tools:** Google IDX • Gemini • Firebase • Working Copy • Edge • iPad

---

## Part 0 — What is Google IDX?

IDX (idx.dev) is Google's browser-based integrated development environment. It is Google's answer to GitHub Codespaces — a full VS Code editor plus terminal, running entirely in your browser. No installation, no laptop required.

### 0.1 Why IDX For Your Setup

| Feature | IDX | StackBlitz | Codespaces |
|---|---|---|---|
| Made by | Google | StackBlitz Inc | Microsoft/GitHub |
| Firebase integration | Native built-in | Manual | Manual |
| Gemini AI built in | Yes | No | No |
| Full terminal / CLI | Yes | Limited | Yes |
| TypeScript | Yes | Yes | Yes |
| Python | Yes | Limited | Yes |
| npm / pip | Both | npm only | Both |
| GitHub sync | Yes | Yes | Native |
| Google account SSO | Yes — one login | No | No |
| Free tier | Yes | Yes | 60 hrs/month |
| Works in Edge iPad | Yes | Yes | Yes |

### 0.2 The Big Picture

IDX replaces both StackBlitz and Juno in your workflow. One IDE for everything — TypeScript, Python, and anything else. Firebase connects natively. Gemini is built in as an AI assistant.

```
Edge Tab 1              Edge Tab 2              Edge Tab 3
(Gemini AI Studio)      (Google IDX)            (Firebase Console)
──────────────────      ────────────────────    ──────────────────
Describe what      →    Paste code, run it →    Results saved to
you want to build       full CLI terminal        Firestore database
                        GitHub sync built in
```

> **Purpose of this workbook:** This is a test drive — not a full project. Work through each part to verify IDX runs well on your iPad over Starlink before rewriting all four main workbooks around it.

---

## Part 1 — Getting Into IDX

### 1.1 First Login

1. Open Edge on your iPad
2. Go to [idx.dev](https://idx.dev)
3. Tap **Sign in with Google**
4. Use your Google account — same one as Firebase and Gemini
5. You land on the IDX dashboard — this is your home screen

> **TIP:** Use the same Google account for IDX, Firebase, Gemini, and GitHub. Everything connects automatically when you use one account across Google's ecosystem.

### 1.2 The IDX Interface

| Area | What It Is | How You Use It |
|---|---|---|
| Left sidebar | File explorer — your project files | Tap to open files, right-tap to create new |
| Main editor | Code editor with syntax highlighting | Paste Gemini code here, edit it |
| Bottom panel | Terminal — full CLI | Run npm, tsc, python, git commands |
| Right sidebar | Gemini AI assistant | Ask coding questions without leaving IDX |
| Top menu | Run, debug, source control | Push to GitHub, run your project |

### 1.3 Open Your TypeScript Repo

1. On the IDX dashboard tap **Open a repo**
2. Sign in to GitHub if prompted — authorize IDX
3. Select your `ipad-workbooks-typescript` repo
4. IDX clones it and opens it — takes about 30 seconds
5. You should see your folder structure in the left sidebar

> **CHECKPOINT 1:** You should see your `ipad-workbooks-typescript` repo open in IDX with your folders visible in the left sidebar. If this works, IDX is connected to GitHub on your iPad. ✓

---

## Part 2 — Test the Terminal

The terminal is the most important thing to verify on iPad. If CLI works well in IDX on your device over Starlink, you have everything you need.

### 2.1 Open the Terminal

1. In IDX look for the terminal panel at the bottom
2. If not visible tap the menu at top > **Terminal** > **New Terminal**
3. A command prompt should appear

### 2.2 Run These Test Commands

**Check Node and npm:**
```bash
node --version
npm --version
```
You should see version numbers like v20.x.x and 10.x.x

**Check TypeScript:**
```bash
tsc --version
```
Should show TypeScript version — if not run: `npm install -g typescript`

**Check Python:**
```bash
python3 --version
```
Should show Python 3.x.x

**Check pip:**
```bash
pip3 --version
```
Should show pip version

**Check Git:**
```bash
git status
```
Should show `On branch main` and any changed files

> **CHECKPOINT 2:** If node, npm, tsc, python3, pip3, and git all return version numbers — your IDX terminal is fully functional on iPad. This is your CLI on iPad. ✓

---

## Part 3 — Test TypeScript

Create a simple TypeScript file, compile it, and run it. Verifies the full TypeScript workflow in IDX.

### 3.1 Create a Test File

1. In the left sidebar right-tap the `blackjack/` folder
2. Tap **New File** — name it `test.ts`
3. Paste this code:

```typescript
// TypeScript test — basic types and functions
interface Card {
  suit: 'Hearts' | 'Diamonds' | 'Clubs' | 'Spades';
  value: number;
  display: string;
}

function createCard(suit: Card['suit'], value: number): Card {
  const display = value === 1 ? 'A' : value === 11 ? 'J' :
                  value === 12 ? 'Q' : value === 13 ? 'K' : String(value);
  return { suit, value, display };
}

const card = createCard('Hearts', 1);
console.log(`Card: ${card.display} of ${card.suit}`);
console.log('TypeScript is working in IDX!');
```

### 3.2 Compile and Run

```bash
cd blackjack
tsc test.ts
node test.js
```

Expected output:
```
Card: A of Hearts
TypeScript is working in IDX!
```

> **CHECKPOINT 3:** TypeScript compiled and ran without errors — TypeScript workflow confirmed in IDX on iPad. Delete `test.ts` and `test.js` when done. ✓

---

## Part 4 — Test Python

Verify Python works in IDX terminal — important for Monte Carlo and Bayesian notebooks.

### 4.1 Create a Python Test

```bash
cd ../monte-carlo
touch test.py
```

Open `test.py` in the editor and paste:

```python
# Python Monte Carlo test
import random
import math

def estimate_pi(n: int) -> float:
    inside = sum(
        1 for _ in range(n)
        if math.sqrt(random.random()**2 + random.random()**2) <= 1
    )
    return 4 * inside / n

result = estimate_pi(100_000)
print(f'Pi estimate: {result:.4f}')
print(f'True Pi:     {math.pi:.4f}')
print('Python is working in IDX!')
```

### 4.2 Run It

```bash
python3 test.py
```

You should see a Pi estimate close to 3.1416 and the confirmation message.

> **CHECKPOINT 4:** Python running Monte Carlo math in IDX terminal on iPad. This means you can run Python workbooks directly in IDX without Juno. Clean up `test.py` when done. ✓

---

## Part 5 — Test Firebase Connection

### 5.1 Install Firebase

```bash
cd ..   # back to repo root
npm init -y
npm install firebase
```

### 5.2 Create a Firebase Test File

Create `firebase-test.ts` in your repo root:

```typescript
// Firebase connection test
import { initializeApp } from 'firebase/app';
import { getFirestore, collection, addDoc, Timestamp } from 'firebase/firestore';

// Paste your Firebase config from Firebase Console
const firebaseConfig = {
  apiKey: 'YOUR_API_KEY',
  authDomain: 'YOUR_PROJECT.firebaseapp.com',
  projectId: 'YOUR_PROJECT_ID',
  storageBucket: 'YOUR_PROJECT.appspot.com',
  messagingSenderId: 'YOUR_SENDER_ID',
  appId: 'YOUR_APP_ID'
};

const app = initializeApp(firebaseConfig);
const db  = getFirestore(app);

async function testSave(): Promise<void> {
  try {
    await addDoc(collection(db, 'idx_test'), {
      message: 'IDX Firebase test',
      source:  'IDX on iPad',
      timestamp: Timestamp.now()
    });
    console.log('Firebase save successful!');
    console.log('IDX + Firebase is fully working!');
  } catch (e) {
    console.error('Firebase error:', e);
  }
}

testSave();
```

### 5.3 Run the Firebase Test

```bash
tsc firebase-test.ts --esModuleInterop --module commonjs
node firebase-test.js
```

Then go to Firebase Console > Firestore > `idx_test` collection — you should see your test document.

> **CHECKPOINT 5:** Document appears in Firebase Console — IDX to Firebase is fully wired up. Delete `firebase-test.ts`, `firebase-test.js`, and the `idx_test` collection in Firebase Console when done. ✓

---

## Part 6 — Test Gemini Inside IDX

### 6.1 Open the Gemini Panel

1. Look for the Gemini icon (sparkle) in the right sidebar of IDX
2. Tap it to open the Gemini chat panel
3. You should see a chat interface inside IDX

### 6.2 Test Prompts

**Prompt 1 — Code generation:**
```
Write a TypeScript function that shuffles an array using
the Fisher-Yates algorithm. Include the type signature.
```

**Prompt 2 — Code explanation:**
```
Explain what this TypeScript code does line by line: [paste any code]
```

**Prompt 3 — Firebase help:**
```
Show me how to query the last 10 documents from a Firestore
collection ordered by timestamp using Firebase Web SDK v9.
```

> **CHECKPOINT 6:** Gemini responds inside IDX with useful TypeScript code — AI assistance is built into your IDE. You may not need a separate Gemini tab for simple questions. ✓

---

## Part 7 — Test Git Workflow

### 7.1 Make a Small Change

1. Open `README.md` in the IDX editor
2. Add one line at the bottom: `<!-- IDX test -->`
3. Save the file

### 7.2 Commit and Push From Terminal

```bash
git add README.md
git commit -m "IDX test commit"
git push
```

### 7.3 Verify in Working Copy

1. Switch to Working Copy on iPad
2. Tap **Pull** (no underline) on your `ipad-workbooks-typescript` repo
3. You should see the README change pulled down

> **CHECKPOINT 7:** Working Copy pulled your IDX commit — full Git loop confirmed: IDX edits → GitHub → Working Copy on iPad. ✓

---

## Part 8 — IDX Verdict

### 8.1 Checkpoint Scorecard

| # | What It Tests | Pass? |
|---|---|---|
| 1 | IDX opens and shows GitHub repo | ☐ |
| 2 | Terminal — node, npm, tsc, python3, git all work | ☐ |
| 3 | TypeScript compiles and runs in terminal | ☐ |
| 4 | Python runs Monte Carlo math in terminal | ☐ |
| 5 | Firebase save from IDX appears in Console | ☐ |
| 6 | Gemini panel works inside IDX | ☐ |
| 7 | Git commit/push from IDX, pull in Working Copy | ☐ |

### 8.2 What the Score Means

| Score | Verdict | Action |
|---|---|---|
| 7/7 | IDX is your IDE | Rewrite all 4 workbooks for IDX — drop StackBlitz and Juno |
| 5–6/7 | IDX is mostly solid | Rewrite workbooks, note which features to avoid |
| 3–4/7 | IDX has iPad gaps | Use IDX for TypeScript, keep Juno for Python |
| 0–2/7 | IDX not ready on iPad | Stick with StackBlitz + Juno for now |

### 8.3 Potential IDX Issues on iPad to Watch For

- Keyboard lag in the code editor — common in browser IDEs on iPad
- Terminal scroll behavior — may feel different from native apps
- Session timeout — IDX may pause after inactivity
- Starlink latency — cloud IDE more sensitive to connection quality than local apps
- Split screen — IDX in half screen may be too cramped for comfortable coding

### 8.4 Your Simplified Toolchain if IDX Scores 5+

```
Edge Tab 1 — Gemini AI Studio   (for complex code generation)
Edge Tab 2 — Google IDX         (IDE + terminal + Gemini sidebar)
Edge Tab 3 — Firebase Console   (view your data)
Working Copy                    (pull GitHub changes to iPad)
```

One IDE. Both languages. No Juno. No StackBlitz. All Google.

---

> *Google IDX • TypeScript • Python • Firebase • Gemini • iPad*  
> *MSC Meraviglia — Starlink Maritime*
