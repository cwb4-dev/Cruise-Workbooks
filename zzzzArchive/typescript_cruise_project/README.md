# iPad Workbooks — ipad-workbooks

A personal learning and development workspace built entirely on iPad,
designed to work at sea aboard MSC Meraviglia via Starlink.

---

## What This Is

A collection of TypeScript projects and workbooks covering:

| Project | Folder | What It Does |
|---|---|---|
| Blackjack | `/blackjack` | Playable browser Blackjack app built with TypeScript |
| Backgammon | `/backgammon` | Full Backgammon game — for the wife 🎲 |
| Monte Carlo | `/monte-carlo` | Simulations: Pi, stock portfolios, project risk |
| Bayesian | `/bayesian` | Bayesian inference: medical diagnosis, A/B testing, spam filters |

Each project folder contains TypeScript source files (run live in StackBlitz)
and a .docx workbook (the soup-to-nuts guide for that project).

---

## Why This Setup

- **iPad only** — no laptop needed, works great at sea
- **TypeScript** — catches errors as you type, safer than plain JavaScript
- **StackBlitz** — full TypeScript IDE in an Edge browser tab, no install needed
- **Gemini** writes the code — describe what you want in plain English
- **Firebase** stores results permanently in the cloud
- **Working Copy** keeps everything versioned on GitHub
- **Starlink** handles cloud connectivity when needed

---

## Toolchain

| Tool | Role | Where |
|---|---|---|
| Gemini AI Studio | Writes all TypeScript code | aistudio.google.com |
| StackBlitz | TypeScript IDE — compiles and previews live | stackblitz.com |
| Firebase Firestore | Permanent cloud database for results | console.firebase.google.com |
| Working Copy Pro | Git client — push/pull to GitHub | iPad App |
| Edge browser | Runs everything — all three tools in tabs | iPad browser |
| GitHub | Version control and backup — the backbone | github.com |

---

## Startup Sequence

### Every Session (60 seconds)

1. Open **Edge** — three tabs:
   - Tab 1: aistudio.google.com (Gemini)
   - Tab 2: stackblitz.com (open your project)
   - Tab 3: console.firebase.google.com (Firebase)
2. Open **Working Copy** — tap Pull (no underline) to grab latest from GitHub
3. Back to StackBlitz — live preview is already running
4. Start working

### End of Session

1. In StackBlitz — GitHub icon > Commit > add message > Push
2. Working Copy — Pull to confirm sync
3. Everything is safely on GitHub

---

## Standard Firebase Setup

Paste this at the top of every main.ts:

```typescript
import { initializeApp } from 'firebase/app';
import { getFirestore, collection, addDoc, getDocs,
         orderBy, query, Timestamp } from 'firebase/firestore';

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
console.log('Firebase connected!');
```

---

## Standard Save Pattern (with Offline Fallback)

```typescript
async function saveResult(collectionName: string, data: object): Promise<void> {
  try {
    await addDoc(collection(db, collectionName), {
      ...data,
      timestamp: Timestamp.now()
    });
    console.log('Saved to Firebase:', collectionName);
  } catch (e) {
    // Starlink down — save locally
    localStorage.setItem(`offline_${Date.now()}`, JSON.stringify(data));
    console.log('Saved locally as fallback');
  }
}
```

---

## How to Use Gemini to Write Code

Always start your Gemini prompt with:

```
I am building a [project] in vanilla TypeScript in StackBlitz.
No frameworks. Use Firebase Web SDK v9 modular imports.
```

Always end with:

```
Give me complete index.html, main.ts, and style.css I can paste into StackBlitz.
Include all imports at the top of each file.
```

---

## At-Sea Notes (MSC Meraviglia / Starlink)

- StackBlitz, Gemini, and Firebase all need Starlink
- Use the localStorage fallback above when connectivity is spotty
- Generate code from Gemini while signal is solid, work through it offline if needed
- Commit locally in StackBlitz anytime, push to GitHub when Starlink is up

---

## Security Note

Firebase Web SDK config (apiKey etc.) is safe to include in client-side TypeScript
for Firestore in test mode. This is designed to be public — unlike a service
account JSON. Secure your data with Firebase Security Rules when moving out of test mode.

---

*Built on iPad — MSC Meraviglia — Starlink Maritime*
*Gemini AI  •  TypeScript  •  StackBlitz  •  Firebase  •  Working Copy  •  GitHub*
