# iPad Workbooks — ipad-workbooks

A personal learning and development workspace built entirely on iPad,
designed to work at sea aboard MSC Meraviglia via Starlink.

---

## What This Is

A collection of Python notebooks, workbooks, and projects covering:

| Project | Folder | What It Does |
|---|---|---|
| Blackjack | `/blackjack` | Playable browser-based Blackjack app built with Gemini |
| Backgammon | `/backgammon` | Full Backgammon game — for the wife 🎲 |
| Monte Carlo | `/monte-carlo` | Simulation techniques: Pi, stock portfolios, project risk |
| Bayesian | `/bayesian` | Bayesian inference: medical diagnosis, A/B testing, spam filters |
| Firebase | `/firebase` | Service account key lives here — **never share this file** |

Each project folder contains:
- `.ipynb` notebooks — run in Juno on iPad
- `.docx` workbook — the soup-to-nuts guide for that project

---

## Why This Setup

- **iPad only** — no laptop needed, works great at sea
- **Juno** runs Python locally — code executes even when offline
- **Gemini** writes the code — describe what you want in plain English
- **Firebase** stores results permanently in the cloud
- **Working Copy** keeps everything versioned on GitHub
- **Starlink** handles cloud connectivity when needed

---

## Toolchain

| Tool | Role | Where |
|---|---|---|
| Juno | Run Python notebooks locally | iPad App |
| Working Copy Pro | Git client — push/pull to GitHub | iPad App |
| Edge browser | Gemini AI Studio + Firebase Console | iPad browser |
| Gemini AI Studio | Writes all Python code | aistudio.google.com |
| Firebase Firestore | Permanent cloud database for results | console.firebase.google.com |
| GitHub | Version control and backup | github.com |

**GitHub is the backbone that ties all together.**

---

## Startup Sequence

### Every Session (60 seconds)

1. Open **Juno** — navigate to Working Copy > ipad-workbooks > your project folder
2. Open **Edge** — two tabs:
   - Tab 1: [aistudio.google.com](https://aistudio.google.com) (Gemini)
   - Tab 2: [console.firebase.google.com](https://console.firebase.google.com) (Firebase)
3. Open **Working Copy** — tap Pull to grab any changes from GitHub
4. Back in Juno — 
   - Browse > Working Copy > ipad-workbooks > your project folder
   - Open your notebook
   - run Cell 1 (imports) and Cell 2 (Firebase connect)
6. Start working

### End of Session

1. Switch to **Working Copy**
2. Tap **Commit** — add a short message describing what you did
3. Tap **Push** — everything is safely on GitHub

---

## Standard Notebook Structure

Every notebook follows this cell layout:

```
Cell 1 — Imports
Cell 2 — Firebase Connection
Cell 3+ — Your actual work
```

### Cell 1 — Standard Imports

```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from datetime import datetime

np.random.seed(42)
plt.style.use('seaborn-v0_8-darkgrid')
print('Libraries loaded!')
```

### Cell 2 — Firebase Connection

```python
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

KEY_PATH = '../firebase/your-service-account.json'

if not firebase_admin._apps:
    cred = credentials.Certificate(KEY_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()
print('Firebase connected!')
```

### Offline Fallback — Save Locally When Starlink is Down

```python
import json

def save_local(data, filename):
    """Save results locally when Firebase is unavailable."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    print(f'Saved locally: {filename}')

def save_result(data, collection, filename_fallback):
    """Try Firebase first, fall back to local file."""
    try:
        db.collection(collection).add(data)
        print(f'Saved to Firebase: {collection}')
    except Exception as e:
        print(f'Firebase unavailable ({e}) — saving locally')
        save_local(data, filename_fallback)
```

Use it like this:

```python
result = {
    'simulation_type': 'pi_estimation',
    'pi_estimate': 3.14159,
    'timestamp': datetime.utcnow()
}

save_result(result, 'monte_carlo_runs', 'pi_result.json')
```

When Starlink is back, push local JSON files to Firebase manually or 
write a sync cell to do it automatically.

---

## Installing Packages in Juno

Juno has its own package manager — do NOT use `!pip install` in cells.

1. In Juno tap the **wrench icon**
2. Tap **Packages**
3. Search and install what you need

### Packages to Install Once

| Package | Used In |
|---|---|
| `numpy` | All projects |
| `matplotlib` | All projects |
| `pandas` | All projects |
| `scipy` | Monte Carlo, Bayesian |
| `firebase-admin` | All projects |
| `pymc` | Bayesian (may be slow on iPad) |

---

## How to Use Gemini to Write Code

Always start your Gemini prompt with this context:

```
I am writing Python code in Juno on iPad.
Juno runs Python locally — do NOT use shell commands or !pip install.
Packages are pre-installed via Juno's package manager.
```

Then describe what you want. End every prompt with:

```
Give me complete, Juno-ready Python code for a single notebook cell.
```

### When to Save to Firebase

End your Gemini prompt with:

```
Save results to Firebase Firestore using firebase-admin.
The db client is already initialised. Collection name: '[name]'.
Include timestamp: datetime.utcnow()
```

---

## At-Sea Notes (MSC Meraviglia / Starlink)

- **Juno runs fully offline** — Python execution never needs internet
- **Gemini needs Starlink** — generate code before going to areas with no signal
- **Firebase needs Starlink** — use the offline fallback above when connectivity is spotty
- **Working Copy push/pull needs Starlink** — commit locally anytime, push when connected
- **Good strategy at sea:** write and run code offline, save results locally, 
  sync everything to Firebase and GitHub when Starlink is solid

---

## Repo Structure

```
ipad-workbooks/
├── README.md               ← you are here
├── blackjack/
│   ├── blackjack.ipynb     ← main notebook
│   └── blackjack.docx      ← workbook guide
├── backgammon/
│   ├── backgammon.ipynb
│   └── backgammon.docx
├── monte-carlo/
│   ├── monte_carlo.ipynb
│   └── monte_carlo.docx
├── bayesian/
│   ├── bayesian.ipynb
│   └── bayesian.docx
└── firebase/
    └── your-service-account.json   ← KEEP PRIVATE
```

---

## Security Reminder

- This repo is **private** on GitHub — keep it that way
- The `firebase/` folder contains your service account key
- **Never make this repo public** while the key is in it
- If you accidentally expose the key: regenerate it immediately in 
  Firebase Console > Project Settings > Service Accounts

---

*Built on iPad — MSC Meraviglia — Starlink Maritime*
*Gemini AI • Juno • Working Copy • Firebase • GitHub*
