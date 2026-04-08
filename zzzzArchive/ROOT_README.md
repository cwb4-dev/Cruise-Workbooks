# iPad Development Workbooks

A personal learning and development workspace built entirely on iPad,
designed to work at sea aboard MSC Meraviglia via Starlink.

---

## Start Here — Orientation Workbooks

**Before diving into any project, work through these two workbooks first.**
They are in the `orientation-workbooks/` folder and cover the two tools
you will use every single session.

| Workbook | File | Platform | What It Covers |
|---|---|---|---|
| Google IDX | `IDX_Orientation_Workbook_Mac.md` | Mac | IDE setup, terminal, TypeScript, Python, Firebase, Git — 7 checkpoints |
| Gemini AI Studio | `Gemini_AI_Studio_Workbook_Mac.md` | Mac | Prompt formula, System Instructions, code generation, error fixing — 9 checkpoints |
| Google IDX | `IDX_Orientation_Workbook.md` | iPad | Same as Mac version with iPad-specific tips |
| Gemini AI Studio | `Gemini_AI_Studio_Workbook.md` | iPad | Same as Mac version with iPad-specific tips |

**Recommended order:**
1. Start with the **Mac versions** — larger screen, easier to learn
2. Work through IDX first — get your environment solid
3. Work through Gemini AI Studio — get fluent with prompting
4. Then use the **iPad versions** at sea — same content, iPad-specific workflow
5. Then open any project `WORKBOOK.md` and start building

> Both workbooks have checkpoints and a scorecard. Aim for 5+ on IDX
> and 7+ on Gemini AI Studio before starting your first project.

---

## What This Is

Two parallel workbook sets — one in Python, one in TypeScript — covering the same
four projects from different angles. Python for data science and simulation.
TypeScript for browser-based apps and interactive tools.

| Repo | Language | IDE | Best For |
|---|---|---|---|
| `ipad-workbooks-python` | Python | Google IDX | Monte Carlo, Bayesian, data science |
| `ipad-workbooks-typescript` | TypeScript | Google IDX | Blackjack, Backgammon, browser apps |

---

## Projects

| Project | Python | TypeScript | What It Does |
|---|---|---|---|
| Blackjack | Data analysis of strategy | Playable browser game | Card game — strategy vs simulation |
| Backgammon | Move probability analysis | Playable browser game | Board game — for the wife 🎲 |
| Monte Carlo | Full simulation suite | Interactive visualizations | Pi, stocks, project risk, gambling |
| Bayesian | Full inference suite | Interactive visualizations | Medical diagnosis, A/B testing, spam |

---

## Why Two Languages?

- **Python** is the language of data science — NumPy, SciPy, matplotlib, pandas.
  Better for numerical simulation, statistical modeling, and Bayesian inference.
- **TypeScript** is the language of the browser — interactive apps, Canvas graphics,
  real-time UI. Better for building things people can actually play and use.
- **Both save to Firebase** — your results are in one place regardless of language.
- **Both run in Google IDX** — one IDE, one workflow, one toolchain.

---

## Toolchain

| Tool | Role | Where |
|---|---|---|
| Google IDX | Full IDE + terminal + Gemini sidebar | idx.dev in Edge |
| Gemini AI Studio | Writes all code | aistudio.google.com in Edge |
| Firebase Firestore | Permanent cloud database | console.firebase.google.com in Edge |
| Working Copy Pro | Git client — syncs both repos to iPad | iPad app |
| Edge browser | Runs all three tools in tabs | iPad browser |
| GitHub | Version control — the backbone | github.com |

> GitHub is the backbone that ties everything together.

---

## Startup Sequence

### Every Session (60 seconds)

1. Open **Edge** — three tabs:
   - Tab 1: [idx.dev](https://idx.dev) — open your project
   - Tab 2: [aistudio.google.com](https://aistudio.google.com) — Gemini
   - Tab 3: [console.firebase.google.com](https://console.firebase.google.com) — Firebase
2. Open **Working Copy** — Pull on whichever repo you are working in today
3. Back to **IDX** — terminal ready, files open
4. Start working

### End of Session

```bash
git add .
git commit -m "describe what you did"
git push
```

Working Copy > Pull to confirm everything is on your iPad.

---

## Gemini Prompt Templates

### For Python (in IDX terminal)

```
I am writing Python code in Google IDX.
Full terminal environment — pip, python3, all standard libraries available.
Use firebase-admin for Firebase. Key file is at: firebase/service-account.json
Give me complete Python code I can paste into a .py file in IDX.
```

### For TypeScript (in IDX terminal)

```
I am building a [project] in vanilla TypeScript in Google IDX.
Full Node.js environment with CLI access.
Use Firebase Web SDK v9 modular imports.
Give me complete index.html, main.ts, and style.css.
Include all imports at the top of each file.
```

---

## IDX Terminal Quick Reference

```bash
# Python
python3 script.py
pip3 install numpy matplotlib pandas scipy firebase-admin

# TypeScript
tsc main.ts
tsc --watch
node main.js
npm install firebase
npm install -g typescript

# Git (same for both)
git add .
git commit -m "message"
git push
git pull
```

---

## Firebase Setup

### Python (firebase-admin — service account)

```python
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

if not firebase_admin._apps:
    cred = credentials.Certificate('firebase/service-account.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()
print('Firebase connected!')
```

### TypeScript (Web SDK v9 — config object)

```typescript
import { initializeApp } from 'firebase/app';
import { getFirestore, collection, addDoc, Timestamp } from 'firebase/firestore';

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
```

> **Note:** Python uses a service account JSON (keep private, in a private repo).
> TypeScript uses the Web SDK config object (safe to include in client code).

---

## Offline Fallback — At-Sea Pattern

### Python

```python
import json

def save_result(db, collection_name: str, data: dict, fallback_file: str):
    try:
        db.collection(collection_name).add(data)
        print(f'Saved to Firebase: {collection_name}')
    except Exception as e:
        with open(fallback_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        print(f'Starlink down — saved locally: {fallback_file}')
```

### TypeScript

```typescript
async function saveResult(collectionName: string, data: object): Promise<void> {
  try {
    await addDoc(collection(db, collectionName), {
      ...data,
      timestamp: Timestamp.now()
    });
  } catch (e) {
    localStorage.setItem(`offline_${Date.now()}`, JSON.stringify(data));
    console.log('Starlink down — saved locally');
  }
}
```

---

## At-Sea Notes (MSC Meraviglia / Starlink)

| Feature | Needs Starlink? | Notes |
|---|---|---|
| IDX coding | Yes | Cloud IDE |
| Gemini code generation | Yes | Cloud AI |
| Firebase saves | Yes | Use fallback patterns above |
| Working Copy push/pull | Yes | Commit locally anytime, push when connected |
| Reading WORKBOOK.md files | No | Already on iPad via Working Copy |
| Running Python locally | No | IDX needs Starlink but you can prep code offline |

**Good at-sea strategy:** Generate code from Gemini while Starlink is solid.
Work through it in IDX. If signal drops your code is always saved in GitHub.

---

## Repo Structure

```
ipad-workbooks/                        ← you are here (root repo)
├── README.md                          ← this file
├── orientation-workbooks/
│   ├── IDX_Orientation_Workbook_Mac.md        ← start here on Mac (1 of 2)
│   ├── Gemini_AI_Studio_Workbook_Mac.md       ← start here on Mac (2 of 2)
│   ├── IDX_Orientation_Workbook.md            ← iPad version (1 of 2)
│   └── Gemini_AI_Studio_Workbook.md           ← iPad version (2 of 2)
├── ipad-workbooks-python/
└── ipad-workbooks-typescript/

ipad-workbooks-python/
├── README.md                  ← Python repo overview (coming soon)
├── firebase/
│   └── service-account.json   ← KEEP PRIVATE — never share
├── blackjack/
│   └── WORKBOOK.md
├── backgammon/
│   └── WORKBOOK.md
├── monte-carlo/
│   └── WORKBOOK.md
└── bayesian/
    └── WORKBOOK.md

ipad-workbooks-typescript/
├── README.md                  ← TypeScript repo overview (coming soon)
├── blackjack/
│   ├── WORKBOOK.md
│   ├── index.html
│   ├── main.ts
│   └── style.css
├── backgammon/
│   ├── WORKBOOK.md
│   ├── index.html
│   ├── main.ts
│   └── style.css
├── monte-carlo/
│   ├── WORKBOOK.md
│   ├── index.html
│   ├── main.ts
│   └── style.css
└── bayesian/
    ├── WORKBOOK.md
    ├── index.html
    ├── main.ts
    └── style.css
```

---

## Security

- `ipad-workbooks-python` contains a Firebase service account JSON — **keep this repo private**
- `ipad-workbooks-typescript` uses the Firebase Web SDK config — safe in private repo
- Both repos are private on GitHub — keep them that way

---

*Built on iPad — MSC Meraviglia — Starlink Maritime*
*Google IDX • Gemini AI • Python • TypeScript • Firebase • Working Copy • GitHub*
