# Blackjack — WORKBOOK

> TypeScript • Google IDX • Firebase • iPad  
> *Ask Gemini. Code in IDX. Save to Firebase.*

---

## Part 0 — Your IDX Workflow

### The Three Edge Tabs

```
Tab 1 — idx.dev          Tab 2 — aistudio.google.com    Tab 3 — console.firebase.google.com
(Google IDX)             (Gemini AI Studio)               (Firebase Console)
─────────────            ──────────────────               ──────────────────
Write and run  ←──────── Paste generated     ──────────→  View saved
TypeScript code          TypeScript code                   game results
git push from
terminal
```

### Session Startup

1. Open IDX — open `ipad-workbooks-typescript` repo
2. Open AI Studio in Tab 2
3. Open Firebase Console in Tab 3
4. Working Copy → Pull
5. Start working

### Gemini Prompt Template

```
I am building a [feature] for my Blackjack game in vanilla TypeScript.
It runs in Google IDX — full Node.js environment.
Use Firebase Web SDK v9 modular imports.
Give me complete TypeScript I can paste into IDX.
Include all imports at the top.
```

---

## Part 1 — Plan

### What You Are Building

A fully playable Blackjack game that runs in the browser as a single HTML/TypeScript project. TypeScript handles all game logic. Results save to Firebase Firestore.

### Blackjack Rules

| Rule | Details |
|---|---|
| Goal | Get closer to 21 than dealer without going over |
| Card values | 2-10 = face value, J/Q/K = 10, Ace = 1 or 11 |
| Blackjack | Ace + any 10-value on first deal = instant win |
| Bust | Total over 21 = automatic loss |
| Dealer rule | Dealer must hit until total is 17 or higher |

### Feature Checklist

| ✓ | Feature | Part |
|---|---|---|
| ☐ | Green felt layout with card areas | 2 |
| ☐ | TypeScript Card and Deck types | 2 |
| ☐ | Shuffle and deal opening hand | 3 |
| ☐ | Hit button — draw a card | 3 |
| ☐ | Stand button — dealer plays out | 3 |
| ☐ | Bust and Blackjack detection | 3 |
| ☐ | Winner determination | 3 |
| ☐ | Score tracker | 4 |
| ☐ | Save game results to Firebase | 5 |
| ☐ | Query and display game history | 5 |

### Why TypeScript for Blackjack

- Define a `Card` type — enforces correct card structure everywhere
- Define a `GameState` type — impossible to mix up player and dealer hands
- Ace logic errors caught at compile time not runtime
- IDX shows errors inline as you type — no surprise bugs at runtime

---

## Part 2 — Ask Gemini: Layout and Types

Open AI Studio in Tab 2. Copy these prompts exactly.

### Step 2.1 — Create the IDX Project

In IDX terminal:

```bash
cd blackjack
npm init -y
npm install -g typescript
```

Create `index.html`, `main.ts`, and `style.css` in the `blackjack/` folder.

### Step 2.2 — Ask Gemini for the Layout

```
I am building a Blackjack game in vanilla TypeScript running in Google IDX.
Write the complete index.html for:
- A dark green felt-style background
- Title 'Blackjack' at the top in white
- Two card areas labeled 'Dealer' and 'Player'
- Three buttons: Hit, Stand, New Game
- A message area for game results
- A score display showing Wins, Losses, Pushes
- Link to style.css and main.js (compiled output)
No game logic yet — just the HTML structure.
Also write the style.css.
Give me complete index.html and style.css.
```

> **Test it:** Open `index.html` in IDX's preview or run a local server: `npx serve .`

### Step 2.3 — Ask Gemini for the TypeScript Types

```
In my Blackjack TypeScript project, write main.ts with these types:
- Suit type: 'Hearts' | 'Diamonds' | 'Clubs' | 'Spades'
- Card interface: { suit: Suit, value: number, display: string, faceDown: boolean }
- GameState interface: { deck: Card[], playerHand: Card[], dealerHand: Card[],
  playerScore: number, dealerScore: number, wins: number, losses: number,
  pushes: number, gameOver: boolean }
- Function createDeck(): Card[] — builds a shuffled 52-card deck
- Fisher-Yates shuffle function
- Function calculateHandValue(hand: Card[]): number
  Aces count as 11 unless that causes bust, then count as 1
Give me the complete main.ts with all types and functions.
```

Compile and check in IDX terminal:

```bash
tsc main.ts
```

> **CHECKPOINT:** No TypeScript errors — your types are solid.

---

## Part 3 — Ask Gemini: Game Logic

### Step 3.1 — Deal the Opening Hand

```
Update my Blackjack main.ts. Add a dealOpeningHand() function that:
- Initializes a fresh GameState
- Shuffles a new deck and deals 2 cards each to player and dealer
- Sets dealer's first card as faceDown: true
- Calculates initial hand values
- Updates the DOM to show cards using ♠ ♣ ♥ ♦
- Red for Hearts/Diamonds, dark for Clubs/Spades
- Shows hand totals below each hand
- Enables Hit and Stand buttons
- Calls dealOpeningHand() when New Game is clicked
Here is my current main.ts: [paste current code]
Give me the complete updated main.ts.
```

### Step 3.2 — Hit, Stand, and Win Detection

```
Update my Blackjack main.ts. Add full game logic:
HIT: draw one card for player, recalculate total.
  If total > 21: bust — show 'Bust! Dealer wins.' disable buttons.
  Handle Aces: count as 11 unless bust, then count as 1.
STAND: reveal dealer's face-down card.
  Dealer draws until total >= 17.
  Compare totals: higher wins, dealer bust = player wins, equal = push.
  Show result clearly.
BLACKJACK: check for Ace + 10-value on opening deal.
After each game: update wins/losses/pushes display.
NEW GAME: fully reset and auto-deal.
Here is my current main.ts: [paste current code]
Give me the complete updated main.ts.
```

> **CHECKPOINT:** Play 5 full hands. Test bust, stand, tie. Describe any bugs to Gemini with your code pasted in.

### Step 3.3 — Score Tracker

```
Update my Blackjack main.ts. Add:
- Persistent score tracker showing Wins, Losses, Pushes
- Updates after each completed game
- 'Reset Scores' button that zeroes all counts
- Style the score display to stand out on the green background
Here is my current main.ts: [paste current code]
Give me the complete updated main.ts.
```

---

## Part 4 — Ask Gemini: Visual Polish

### Step 4.1 — Make It Look Great

```
Update my Blackjack project. Improve the visual design:
- Card drop shadows and rounded corners
- Smooth slide-in animation when cards are dealt (CSS transitions)
- Result message flashes green for win, red for loss, yellow for push
- Polished buttons with hover and active states
- Overall casino table aesthetic
- Looks great on iPad screen size
Here are my current files: [paste index.html, style.css, main.ts]
Give me complete updated files.
```

### Bonus Features

| Feature | Gemini Prompt |
|---|---|
| Betting system | Add chip betting: player starts with $1000, bets before each hand, wins double. Track bankroll in GameState. |
| Double Down | Add Double Down button: doubles bet, deals exactly one more card, then auto-stands. Only on first two cards. |
| Player name | Add player name input. Store in localStorage so it persists between sessions. |
| Card flip animation | Add CSS flip animation when dealer reveals their face-down card. |

---

## Part 5 — Save Results to Firebase

### Step 5.1 — Install Firebase in IDX

```bash
npm install firebase
```

### Step 5.2 — Ask Gemini for Firebase Integration

```
Add Firebase Firestore to my Blackjack TypeScript project.
Use Firebase Web SDK v9 modular imports.
After each game ends, save a result to collection 'blackjack_games' with:
  result: 'win' | 'loss' | 'push' | 'blackjack'
  playerTotal: number
  dealerTotal: number
  sessionWins: number
  timestamp: Timestamp.now()
Also add a loadHistory() function that reads the last 10 games
and displays them in a table below the game.
Here is my Firebase config: [paste firebaseConfig]
Here are my current files: [paste all files]
Give me complete updated files with Firebase integrated.
```

### Step 5.3 — Verify in Firebase Console

Go to Firebase Console Tab 3 > Firestore > `blackjack_games` collection.
You should see documents appearing after each game.

### The Save Pattern to Verify

Gemini should give you something like this:

```typescript
async function saveGameResult(result: GameResult): Promise<void> {
  try {
    await addDoc(collection(db, 'blackjack_games'), {
      ...result,
      timestamp: Timestamp.now()
    });
  } catch (e) {
    // Starlink fallback
    localStorage.setItem(`game_${Date.now()}`, JSON.stringify(result));
  }
}
```

### Troubleshooting

| Problem | Gemini Prompt |
|---|---|
| TypeScript error | I have this error in IDX: [paste error]. Here is my code: [paste]. Fix the type issue. |
| Cards not showing | My card elements are not appearing after dealing. Here is my renderHand() function: [paste]. What is wrong? |
| Firebase not saving | My addDoc call is failing with: [paste error]. Here is my Firebase setup: [paste]. Fix it. |
| Ace logic wrong | My hand total is wrong with multiple Aces. Fix calculateHandValue() so Aces reduce from 11 to 1 to prevent bust. |

---

## Part 6 — Git and Wrap Up

When your game is working, push it to GitHub from IDX terminal:

```bash
git add .
git commit -m "Blackjack game complete with Firebase"
git push
```

Then Working Copy > Pull to get it on your iPad.

---

> *Blackjack • TypeScript • Google IDX • Firebase • iPad*  
> *MSC Meraviglia — Starlink Maritime*
