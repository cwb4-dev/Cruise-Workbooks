# Backgammon — WORKBOOK

> TypeScript • Google IDX • Firebase • iPad  
> *Ask Gemini. Code in IDX. Save to Firebase.*

---

## Part 0 — Your IDX Workflow

See the main `README.md` for the full startup sequence and toolchain.

### Gemini Prompt Template for This Project

```
I am building a [feature] for my Backgammon game in vanilla TypeScript.
It runs in Google IDX — full Node.js environment with Canvas support.
Use Firebase Web SDK v9 modular imports.
Give me complete TypeScript I can paste into IDX.
Include all imports at the top.
```

---

## Part 1 — Understand the Game First

Backgammon is complex. Read this before writing your first Gemini prompt.
Precise language produces better code.

### Core Rules — Use This Language With Gemini

| Rule | Plain English — Say This Exactly to Gemini |
|---|---|
| Board | 24 triangular points numbered 1-24. Center divider is the Bar. |
| Direction | White moves from point 24 toward point 1. Black moves from 1 toward 24. |
| Start position | White: 2 on 24, 5 on 13, 3 on 8, 5 on 6. Mirror for Black. |
| Doubles | Rolling the same number gives 4 moves of that value, not 2. |
| Blot | A single checker on a point. Landing on it sends it to the Bar. |
| Block | 2 or more same-color checkers. Opponent cannot land there. |
| Bar rule | Checkers on Bar must re-enter before any other move. |
| Bearing off | When all 15 checkers are in home board — bear them off to win. |

### Feature Checklist

| ✓ | Feature | Part |
|---|---|---|
| ☐ | Canvas board with 24 points | 2 |
| ☐ | TypeScript game state types | 2 |
| ☐ | Checkers in starting position | 2 |
| ☐ | Dice rolling with doubles support | 3 |
| ☐ | Click to select and move checkers | 3 |
| ☐ | Valid move highlighting | 3 |
| ☐ | Hit and Bar mechanic | 4 |
| ☐ | Force Bar re-entry first | 4 |
| ☐ | Bearing off and win detection | 5 |
| ☐ | Score tracker with Gammon/Backgammon | 6 |
| ☐ | Save game results to Firebase | 7 |

### Why TypeScript for Backgammon

- `Point` type enforces valid point numbers and checker counts
- `GameState` interface — impossible to corrupt board state accidentally
- Move validation is explicit and type-safe
- Dice doubles handling is clear — `values: number[]` with 4 entries for doubles

---

## Part 2 — Ask Gemini: Board and Types

### Step 2.1 — Set Up the IDX Project

```bash
cd backgammon
npm init -y
npm install -g typescript
```

### Step 2.2 — Ask Gemini for the Board

```
I am building a Backgammon game in vanilla TypeScript in Google IDX.
Write complete index.html and style.css for:
- An HTML Canvas element sized 900x600 pixels
- Draw the backgammon board on canvas:
  24 triangular points, 12 on top pointing down, 12 on bottom pointing up
  Alternate point colors: dark brown and cream/ivory
  Points numbered 1-24 (1-12 bottom right-to-left, 13-24 top left-to-right)
  Vertical bar in the center, dark wood outer border, green felt surface
- Status bar below canvas showing whose turn it is
- Roll Dice button and New Game button below canvas
No checkers yet — just the board drawn on canvas.
Give me complete index.html and style.css.
```

> **Test it:** Open `index.html` using IDX preview. You should see a wooden-bordered board with 24 alternating triangles.

### Step 2.3 — Ask Gemini for the TypeScript Types

```
In my Backgammon TypeScript project define these types in main.ts:
- Player type: 'white' | 'black'
- Point interface: { checkers: number, owner: Player | null }
- DiceRoll interface: { values: number[], used: boolean[] }
  Note: doubles give 4 values e.g. [4,4,4,4] not [4,4]
- GameState interface: {
    points: Point[]           // 24 points indexed 0-23
    bar: { white: number, black: number }
    borneOff: { white: number, black: number }
    currentPlayer: Player
    dice: DiceRoll | null
    selected: number | null
    gameOver: boolean
    winner: Player | null
  }
- Function initGameState(): GameState with standard starting position:
  White: 2 on point 24, 5 on point 13, 3 on point 8, 5 on point 6
  Black: mirror of White
Give me complete main.ts with all types and the init function.
```

---

## Part 3 — Ask Gemini: Dice and Movement

### Step 3.1 — Place Checkers and Roll Dice

```
Update my Backgammon main.ts. Add:
1. drawBoard(state: GameState) function that renders to canvas:
   - Checkers as filled circles stacked on their point
   - White: light gray with dark border. Black: dark red with light border
   - Count number if more than 5 on a point
   - Bar checkers on each side of the center divider
2. rollDice() function:
   - Generates two random 1-6 values
   - Doubles: values array has 4 entries e.g. [3,3,3,3]
   - Draws dice visually in bar area with pip dots
   - Disables Roll button until turn ends
   - Updates status bar: 'White rolled 3-5. Select a checker.'
Here is my current main.ts: [paste code]
Give me the complete updated main.ts.
```

> **Verify doubles:** Add `console.log(state.dice)` and roll until you get doubles. Confirm the array has 4 entries.

### Step 3.2 — Checker Selection and Movement

```
Update my Backgammon main.ts. Add click-to-move:
SELECTION:
- Click a point with current player's checkers to select it (yellow highlight)
- Calculate valid destinations based on remaining dice values
- White moves from HIGH to LOW point numbers (24 toward 1)
- Black moves from LOW to HIGH point numbers (1 toward 24)
- Valid: points with 0, 1, or current player's checkers
- Invalid: points with 2+ opponent checkers
- Highlight valid destinations in green
MOVEMENT:
- Click a highlighted destination to move the checker
- Mark that die value as used in dice.used[]
- Redraw board after every move
- When all dice used or no valid moves: switch player turn
Here is my current main.ts: [paste code]
Give me the complete updated main.ts.
```

---

## Part 4 — Ask Gemini: Hitting and the Bar

### Step 4.1 — Hit Mechanic

```
Update my Backgammon main.ts. Add the hit and Bar mechanic:
HIT: moving to a point with exactly 1 opponent checker (a blot):
- Remove opponent checker from that point
- Add it to gameState.bar for that player
- Draw Bar checkers visually on each side of the center bar
BAR RE-ENTRY (critical rule):
- If current player has checkers on Bar, they MUST enter them first
- Block all other moves until Bar is clear
- White enters from Bar onto opponent home board (points 19-24)
  die value maps: 1=24, 2=23, 3=22, 4=21, 5=20, 6=19
- Black enters from Bar onto opponent home board (points 1-6)
  die value = point number directly
- Show message: 'White has 2 checker(s) on Bar. Must re-enter first.'
Here is my current main.ts: [paste code]
Give me the complete updated main.ts.
```

> **Test this:** Move White to a point with one Black checker. Black should appear on Bar. Try moving a different Black checker — the game must block it.

---

## Part 5 — Ask Gemini: Bearing Off and Winning

### Step 5.1 — Bearing Off

```
Update my Backgammon main.ts. Add bearing off:
WHEN ALLOWED: only when ALL 15 of a player's checkers are in their home board
  White home board = points 1-6 (indices 0-5)
  Black home board = points 19-24 (indices 18-23)
HOW IT WORKS:
- Exact die: die value equals checker's point number — bear it off
- Higher die: no checker on exact point — bear off highest available checker
- Add a Bear Off zone drawn beside the board showing borne-off count
- Track in gameState.borneOff
WIN DETECTION:
- 15 borne-off checkers = win
- Show winner overlay with Play Again button
- Gammon: winner bears off all 15 before opponent bears off any
- Backgammon: loser still has checkers on Bar or in opponent's home board
Here is my current main.ts: [paste code]
Give me the complete updated main.ts.
```

---

## Part 6 — Polish and Score Tracking

### Step 6.1 — Score Tracker

```
Update my Backgammon project. Add:
SCORE TRACKER:
- Track wins for White and Black across games
- Award 1 point for win, 2 for Gammon, 3 for Backgammon
- Display scores above canvas: 'White: 4  |  Black: 2'
- Reset Scores button
VISUAL POLISH:
- Smooth animation when a checker moves (interpolate position over 300ms)
- Bounce effect when checker lands on Bar
- Valid move highlights pulse gently
- Undo button — reverses last move within same turn
- Move log showing last 10 moves in notation e.g. '24/18, 13/8'
Here are my current files: [paste all files]
Give me complete updated files.
```

---

## Part 7 — Save Game History to Firebase

### Step 7.1 — Install Firebase

```bash
npm install firebase
```

### Step 7.2 — Ask Gemini for Firebase Integration

```
Add Firebase Firestore to my Backgammon TypeScript project.
Use Firebase Web SDK v9 modular imports.
After each game ends save to collection 'backgammon_games' with:
  winner: 'white' | 'black'
  winType: 'normal' | 'gammon' | 'backgammon'
  pointsScored: 1 | 2 | 3
  whiteScore: number
  blackScore: number
  timestamp: Timestamp.now()
Also add a history panel showing last 10 games below the board.
Here is my Firebase config: [paste firebaseConfig]
Here are my current files: [paste all files]
Give me complete updated files.
```

### Troubleshooting

| Problem | Gemini Prompt |
|---|---|
| Wrong move direction | White is moving from low to high but should move from 24 toward 1. Fix the move direction calculation. |
| Doubles giving 2 moves | Rolling doubles only gives 2 moves. Fix dice.values to store 4 entries for doubles e.g. [4,4,4,4]. |
| Bar not enforced | Player can move non-Bar checkers while having checkers on Bar. Add the Bar enforcement check to isValidMove(). |
| Bear-off too early | Player can bear off before all checkers are home. Add the all-checkers-home check. |
| TypeScript error | I have this error: [paste]. Here is the relevant code: [paste]. Fix the type issue. |

---

## Part 8 — Git and Wrap Up

```bash
git add .
git commit -m "Backgammon game complete with Firebase"
git push
```

Working Copy > Pull to get it on your iPad — and hand it to your wife. 🎲

---

> *Backgammon • TypeScript • Google IDX • Firebase • iPad*  
> *MSC Meraviglia — Starlink Maritime*
