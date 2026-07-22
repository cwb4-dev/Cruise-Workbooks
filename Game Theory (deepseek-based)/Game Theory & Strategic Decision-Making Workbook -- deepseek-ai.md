# Game Theory & Strategic Decision-Making Workbook -- deepseek-ai
## A Practical Guide to Understanding Strategy, Incentives, and Interactive Decisions

---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Jupyter](https://img.shields.io/badge/Jupyter-F37626.svg?&logo=Jupyter&logoColor=white)](https://jupyter.org/)

---

## 📚 Overview

Game theory is the study of strategic decision-making—how people (or organizations, or even nations) make choices when their outcomes depend on the choices of others. Instead of analyzing decisions in isolation, game theory models interactive situations where each player's optimal strategy depends on what others do.

### What You'll Learn

- **Core Concepts**: Players, strategies, payoffs, Nash equilibrium
- **6 Progressive Modules** from simple to advanced
- **Real-World Applications**: Business strategy, auctions, negotiations, evolutionary biology
- **How Game Theory Intersects with Monte Carlo**: Strategic uncertainty meets random uncertainty
- **Python Implementation**: Build game theory models from scratch

---

## 🎓 Prerequisites

Before starting, you should be familiar with:
- **Basic Python**: Variables, loops, functions, lists, dictionaries
- **NumPy & Matplotlib**: Arrays and basic plotting
- **Basic Probability**: Expected value, conditional probability
- **Linear Algebra** (optional): For advanced games

### Quick Setup

```bash
pip install numpy matplotlib pandas scipy networkx seaborn
```

### Verify Your Setup

```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import seaborn as sns
from collections import Counter, defaultdict
from scipy import stats
import random

print("✅ All imports successful!")
print(f"NumPy version: {np.__version__}")
print(f"NetworkX version: {nx.__version__}")
```

---

## 📚 Key Terminology

| Term | Definition | Example |
|------|------------|---------|
| **Player** | An individual or entity making decisions | Firms, individuals, governments |
| **Strategy** | A complete plan of action | "Always cooperate" or "Defect if opponent defected" |
| **Payoff** | The utility or reward a player receives | Profit, utility, survival |
| **Nash Equilibrium** | Stable state where no player benefits from changing strategy | Both firms choosing optimal prices |
| **Dominant Strategy** | Best strategy regardless of others' choices | Confessing in Prisoner's Dilemma |
| **Pareto Optimal** | State where no one can be better off without hurting someone else | Win-win outcomes |
| **Zero-Sum Game** | One player's gain equals others' loss | Poker, chess, sports |
| **Cooperative Game** | Players can form binding agreements | Cartels, alliances |
| **Non-Cooperative Game** | Players act independently | Most market competition |
| **Mixed Strategy** | Randomized choice between strategies | Rock-paper-scissors |
| **Perfect Information** | All players know all previous moves | Chess |
| **Imperfect Information** | Hidden information exists | Poker, business negotiations |

---

## 🎯 What Is Game Theory?

**The One-Sentence Definition**: Game theory is the mathematical study of strategic decision-making where players' outcomes depend on the choices of others.

**The Core Insight**: The best choice for you depends on what others choose, and the best choice for others depends on what you choose.

**The Key Idea**: Strategic thinking = "I know that you know that I know..."

---

## 📖 Module Structure

Each module follows the same pattern:
1. **WHAT**: What is the concept?
2. **WHY**: Why does it matter?
3. **HOW**: How does it work in code?
4. **EXAMPLE**: A concrete example
5. **EXERCISE**: Something to try yourself
6. **VISUALIZATION**: See the results

---

# MODULE 1: Prisoner's Dilemma

### 📖 WHAT Is It?

Two suspects are arrested and separated. The police offer each prisoner a deal:

| | **Prisoner B: Cooperate** | **Prisoner B: Defect** |
|---|---|---|
| **Prisoner A: Cooperate** | Both get 1 year | A gets 3 years, B goes free |
| **Prisoner A: Defect** | A goes free, B gets 3 years | Both get 2 years |

**The Dilemma**: Despite mutual cooperation being best for both (1 year each), rational self-interest leads both to defect (2 years each). This is a Nash equilibrium that's not Pareto optimal.

### 🤔 WHY Does It Matter?

The Prisoner's Dilemma demonstrates:
- Why cooperation is difficult to sustain
- How individual rationality leads to collective irrationality
- Applications in business, politics, and social sciences
- The tension between self-interest and group welfare
- How trust and repeated interactions change outcomes

### 🛠️ HOW Does It Work in Code?

```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

class PrisonersDilemma:
    """
    A class to model and analyze the Prisoner's Dilemma.
    """
    
    def __init__(self):
        # Payoff matrix: (Player A's payoff, Player B's payoff)
        self.payoffs = {
            ('Cooperate', 'Cooperate'): (3, 3),    # Both cooperate: moderate sentence
            ('Cooperate', 'Defect'): (0, 5),       # A cooperates, B defects: B goes free
            ('Defect', 'Cooperate'): (5, 0),       # A defects, B cooperates: A goes free
            ('Defect', 'Defect'): (1, 1)           # Both defect: both get 2 years
        }
        
        self.strategies = ['Cooperate', 'Defect']
        self.game_name = "Prisoner's Dilemma"
    
    def get_payoff(self, strategy_a, strategy_b):
        """Get payoffs for a given strategy pair"""
        return self.payoffs[(strategy_a, strategy_b)]
    
    def play_round(self, strategy_a, strategy_b):
        """Play one round of the game"""
        payoff_a, payoff_b = self.get_payoff(strategy_a, strategy_b)
        return {
            'player_a': strategy_a,
            'player_b': strategy_b,
            'payoff_a': payoff_a,
            'payoff_b': payoff_b
        }
    
    def find_nash_equilibrium(self):
        """
        Find Nash equilibria by checking all strategy combinations.
        In Prisoner's Dilemma, (Defect, Defect) is the only Nash equilibrium.
        """
        equilibria = []
        
        for sa in self.strategies:
            for sb in self.strategies:
                # Check if Player A can improve by changing strategy
                pa_current, pb_current = self.get_payoff(sa, sb)
                
                # Check if either player can benefit from unilaterally changing
                a_best = True
                b_best = True
                
                # Check A's alternatives
                for sa_alt in self.strategies:
                    if sa_alt != sa:
                        pa_alt, _ = self.get_payoff(sa_alt, sb)
                        if pa_alt > pa_current:
                            a_best = False
                            break
                
                # Check B's alternatives
                for sb_alt in self.strategies:
                    if sb_alt != sb:
                        _, pb_alt = self.get_payoff(sa, sb_alt)
                        if pb_alt > pb_current:
                            b_best = False
                            break
                
                if a_best and b_best:
                    equilibria.append((sa, sb))
        
        return equilibria
    
    def display_payoff_matrix(self):
        """Display the payoff matrix as a formatted table"""
        df = pd.DataFrame(index=self.strategies, columns=self.strategies)
        
        for sa in self.strategies:
            for sb in self.strategies:
                pa, pb = self.get_payoff(sa, sb)
                df.loc[sa, sb] = f"{pa},{pb}"
        
        print("Payoff Matrix (A, B)")
        print("=" * 30)
        print(df)

# Create and analyze the game
game = PrisonersDilemma()

print(f"🎮 {game.game_name}")
print("=" * 50)
game.display_payoff_matrix()

print("\n🎯 Nash Equilibria:")
print("=" * 50)
equilibria = game.find_nash_equilibrium()
for eq in equilibria:
    print(f"  {eq}")

print("\n📊 Analysis:")
print("=" * 50)
print("• Mutual cooperation gives (3,3) - best collective outcome")
print("• Both defect gives (1,1) - Nash equilibrium")
print("• Each player is tempted to defect for (5,0)")
print("• Result: Rational self-interest leads to suboptimal outcome")
```

### 📊 Visualization: Payoff Matrix

```python
def visualize_payoff_matrix(game):
    """Visualize the payoff matrix as a heatmap"""
    strategies = game.strategies
    n = len(strategies)
    
    # Create separate matrices for player A and B payoffs
    payoff_a = np.zeros((n, n))
    payoff_b = np.zeros((n, n))
    
    for i, sa in enumerate(strategies):
        for j, sb in enumerate(strategies):
            pa, pb = game.get_payoff(sa, sb)
            payoff_a[i, j] = pa
            payoff_b[i, j] = pb
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Player A's payoffs
    sns.heatmap(payoff_a, annot=True, fmt='.0f', xticklabels=strategies, 
                yticklabels=strategies, cmap='RdYlGn', ax=axes[0],
                cbar_kws={'label': 'Player A Payoff'})
    axes[0].set_title('Player A Payoffs')
    axes[0].set_xlabel("Player B's Strategy")
    axes[0].set_ylabel("Player A's Strategy")
    
    # Player B's payoffs
    sns.heatmap(payoff_b, annot=True, fmt='.0f', xticklabels=strategies, 
                yticklabels=strategies, cmap='RdYlGn', ax=axes[1],
                cbar_kws={'label': 'Player B Payoff'})
    axes[1].set_title('Player B Payoffs')
    axes[1].set_xlabel("Player B's Strategy")
    axes[1].set_ylabel("Player A's Strategy")
    
    plt.tight_layout()
    plt.show()

# Visualize the payoff matrix
visualize_payoff_matrix(game)
```

### 🧪 EXERCISE: Iterated Prisoner's Dilemma

```python
def iterated_prisoners_dilemma(strategy_a, strategy_b, num_rounds=100):
    """
    Play the Prisoner's Dilemma for multiple rounds with history-dependent strategies.
    """
    total_payoff_a = 0
    total_payoff_b = 0
    history_a = []
    history_b = []
    
    for round_num in range(num_rounds):
        # Get strategies based on history
        move_a = strategy_a(history_a, history_b)
        move_b = strategy_b(history_b, history_a)
        
        # Get payoffs
        pa, pb = game.get_payoff(move_a, move_b)
        
        # Update totals
        total_payoff_a += pa
        total_payoff_b += pb
        
        # Update history
        history_a.append(move_a)
        history_b.append(move_b)
    
    return total_payoff_a, total_payoff_b, history_a, history_b

# Define some strategies
def always_cooperate(my_history, opponent_history):
    return 'Cooperate'

def always_defect(my_history, opponent_history):
    return 'Defect'

def tit_for_tat(my_history, opponent_history):
    # Start with cooperate, then mirror opponent's last move
    if not opponent_history:
        return 'Cooperate'
    return opponent_history[-1]

def grudger(my_history, opponent_history):
    # Cooperate until opponent defects, then defect forever
    if 'Defect' in opponent_history:
        return 'Defect'
    return 'Cooperate'

def random_strategy(my_history, opponent_history):
    return np.random.choice(['Cooperate', 'Defect'])

# Test different strategy matchups
strategies = {
    'Always Cooperate': always_cooperate,
    'Always Defect': always_defect,
    'Tit for Tat': tit_for_tat,
    'Grudger': grudger,
    'Random': random_strategy
}

print("🏆 Iterated Prisoner's Dilemma Tournament")
print("=" * 70)
print(f"{'Strategy A':<20} | {'Strategy B':<20} | {'A Score':<10} | {'B Score':<10}")
print("-" * 70)

for name_a, strat_a in strategies.items():
    for name_b, strat_b in strategies.items():
        if name_a < name_b:  # Avoid duplicates
            score_a, score_b, _, _ = iterated_prisoners_dilemma(strat_a, strat_b, num_rounds=100)
            print(f"{name_a:<20} | {name_b:<20} | {score_a:>9.0f} | {score_b:>9.0f}")
```

### 📊 Iterated Prisoner's Dilemma Visualization

```python
def visualize_iterated_game(history_a, history_b, name_a, name_b):
    """Visualize the history of moves in an iterated game"""
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    
    # Convert moves to numeric values for plotting
    move_to_num = {'Cooperate': 0, 'Defect': 1}
    moves_a = [move_to_num[m] for m in history_a]
    moves_b = [move_to_num[m] for m in history_b]
    
    # Plot moves over time
    axes[0].plot(moves_a, 'go-', label=name_a, alpha=0.7, linewidth=2)
    axes[0].plot(moves_b, 'bo-', label=name_b, alpha=0.7, linewidth=2)
    axes[0].set_ylabel('Move (0=Cooperate, 1=Defect)')
    axes[0].set_title(f'Move History: {name_a} vs {name_b}')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim(-0.1, 1.1)
    axes[0].set_yticks([0, 1])
    axes[0].set_yticklabels(['Cooperate', 'Defect'])
    
    # Plot cumulative cooperation over time
    coop_a = [1 if m == 'Cooperate' else 0 for m in history_a]
    coop_b = [1 if m == 'Cooperate' else 0 for m in history_b]
    
    cumulative_coop_a = np.cumsum(coop_a) / np.arange(1, len(coop_a) + 1)
    cumulative_coop_b = np.cumsum(coop_b) / np.arange(1, len(coop_b) + 1)
    
    axes[1].plot(cumulative_coop_a, 'g-', label=name_a, alpha=0.7, linewidth=2)
    axes[1].plot(cumulative_coop_b, 'b-', label=name_b, alpha=0.7, linewidth=2)
    axes[1].set_xlabel('Round')
    axes[1].set_ylabel('Cumulative Cooperation Rate')
    axes[1].set_title('Cooperation Over Time')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    axes[1].set_ylim(0, 1.1)
    
    plt.tight_layout()
    plt.show()

# Run a match between Tit for Tat and Grudger
score_a, score_b, history_a, history_b = iterated_prisoners_dilemma(
    tit_for_tat, grudger, num_rounds=50
)

print(f"Tit for Tat: {score_a}, Grudger: {score_b}")
visualize_iterated_game(history_a, history_b, 'Tit for Tat', 'Grudger')
```

---

# MODULE 2: Rock-Paper-Scissors

### 📖 WHAT Is It?

A classic game where each strategy beats one and loses to another:
- Rock beats Scissors
- Scissors beats Paper
- Paper beats Rock

**The Twist**: This game has no pure strategy Nash equilibrium. The only Nash equilibrium is a mixed strategy where players randomize 1/3, 1/3, 1/3.

### 🤔 WHY Does It Matter?

Rock-Paper-Scissors demonstrates:
- Mixed strategies and randomization
- Cyclical dominance
- Applications in evolutionary biology and economics
- Why having no dominant strategy leads to randomization

### 🛠️ HOW Does It Work in Code?

```python
class RockPaperScissors:
    """
    A class to model and analyze Rock-Paper-Scissors.
    """
    
    def __init__(self):
        self.strategies = ['Rock', 'Paper', 'Scissors']
        
        # Payoff matrix: (Player A's payoff, Player B's payoff)
        # 1 = win, 0 = draw, -1 = loss
        self.payoffs = {
            ('Rock', 'Rock'): (0, 0),
            ('Rock', 'Paper'): (-1, 1),
            ('Rock', 'Scissors'): (1, -1),
            ('Paper', 'Rock'): (1, -1),
            ('Paper', 'Paper'): (0, 0),
            ('Paper', 'Scissors'): (-1, 1),
            ('Scissors', 'Rock'): (-1, 1),
            ('Scissors', 'Paper'): (1, -1),
            ('Scissors', 'Scissors'): (0, 0)
        }
        
        self.beats = {
            'Rock': 'Scissors',
            'Paper': 'Rock',
            'Scissors': 'Paper'
        }
    
    def get_payoff(self, move_a, move_b):
        """Get payoffs for a given strategy pair"""
        return self.payoffs[(move_a, move_b)]
    
    def play_round(self, move_a, move_b):
        """Play one round of the game"""
        payoff_a, payoff_b = self.get_payoff(move_a, move_b)
        return {
            'player_a': move_a,
            'player_b': move_b,
            'payoff_a': payoff_a,
            'payoff_b': payoff_b,
            'winner': 'A' if payoff_a > 0 else 'B' if payoff_b > 0 else 'Draw'
        }
    
    def find_best_response(self, opponent_move, player_payoffs):
        """Find the best response to an opponent's move"""
        best_payoff = -float('inf')
        best_moves = []
        
        for move in self.strategies:
            payoff, _ = self.get_payoff(move, opponent_move)
            if payoff > best_payoff:
                best_payoff = payoff
                best_moves = [move]
            elif payoff == best_payoff:
                best_moves.append(move)
        
        return best_moves
    
    def mixed_strategy_nash(self):
        """
        Return the mixed strategy Nash equilibrium.
        In RPS, it's (1/3, 1/3, 1/3) for both players.
        """
        return {s: 1/3 for s in self.strategies}
    
    def simulate_mixed_strategy(self, num_rounds=1000):
        """
        Simulate play when both players use mixed strategies.
        """
        results = {'A': 0, 'B': 0, 'Draw': 0}
        move_counts = {s: 0 for s in self.strategies}
        
        for _ in range(num_rounds):
            # Both players randomize uniformly
            move_a = np.random.choice(self.strategies)
            move_b = np.random.choice(self.strategies)
            
            result = self.play_round(move_a, move_b)
            results[result['winner']] += 1
            move_counts[move_a] += 1
        
        return results, move_counts

# Create and analyze the game
rps = RockPaperScissors()

print(f"🎮 Rock-Paper-Scissors")
print("=" * 50)

# Display the payoff matrix
print("\nPayoff Matrix (A, B):")
print("    " + "  ".join([f"{s:>8}" for s in rps.strategies]))
print("-" * 35)
for sa in rps.strategies:
    row = f"{sa:<6}"
    for sb in rps.strategies:
        pa, pb = rps.get_payoff(sa, sb)
        row += f"  {pa},{pb:>3}"
    print(row)

# Find best responses
print("\n🎯 Best Responses:")
print("-" * 50)
for move in rps.strategies:
    best = rps.find_best_response(move, None)
    print(f"Against {move}: Best response is {best}")

print("\n🎲 Mixed Strategy Nash Equilibrium:")
print("-" * 50)
mixed_nash = rps.mixed_strategy_nash()
for s, prob in mixed_nash.items():
    print(f"  {s}: {prob:.2%}")

# Simulate mixed strategy play
print("\n📊 Simulation Results (Mixed Strategies):")
print("-" * 50)
results, moves = rps.simulate_mixed_strategy(10000)
print(f"Player A wins: {results['A']/10000:.1%}")
print(f"Player B wins: {results['B']/10000:.1%}")
print(f"Draws: {results['Draw']/10000:.1%}")
print(f"\nMove frequencies: {moves}")
```

### 📊 Rock-Paper-Scissors Visualization

```python
def visualize_rps_results(results, moves):
    """Visualize Rock-Paper-Scissors results"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Win/Loss/Draw distribution
    categories = list(results.keys())
    values = [results[k] for k in categories]
    
    colors = ['green', 'red', 'gray']
    bars = axes[0].bar(categories, values, color=colors, alpha=0.7)
    
    for bar, val in zip(bars, values):
        axes[0].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 20,
                    f'{val/10000:.1%}', ha='center', va='bottom', fontsize=12)
    
    axes[0].set_ylabel('Number of Rounds')
    axes[0].set_title('Game Outcomes (10,000 rounds)')
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # Plot 2: Move frequencies
    moves_list = list(moves.keys())
    move_counts = [moves[m] for m in moves_list]
    
    bars = axes[1].bar(moves_list, move_counts, color=['blue', 'orange', 'purple'], alpha=0.7)
    
    for bar, count in zip(bars, move_counts):
        axes[1].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 20,
                    f'{count/10000:.1%}', ha='center', va='bottom', fontsize=12)
    
    axes[1].set_ylabel('Number of Moves')
    axes[1].set_title('Move Distribution (Player A)')
    axes[1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.show()

# Visualize results
visualize_rps_results(results, moves)

# Show the cyclical nature
print("\n🔄 The Cycle:")
print("    Rock beats Scissors")
print("       ↑         ↓")
print("    Paper beats Rock")
print("       ↑         ↓")
print("    Scissors beats Paper")
```

### 🧪 EXERCISE: Tournament of Strategies

```python
def rps_tournament(strategy_a, strategy_b, num_rounds=1000):
    """Run a tournament between two RPS strategies"""
    scores_a = 0
    scores_b = 0
    
    for _ in range(num_rounds):
        # Get moves from strategies
        move_a = strategy_a()
        move_b = strategy_b()
        
        result = rps.play_round(move_a, move_b)
        scores_a += result['payoff_a']
        scores_b += result['payoff_b']
    
    return scores_a, scores_b

# Define some interesting strategies
def always_rock():
    return 'Rock'

def always_paper():
    return 'Paper'

def always_scissors():
    return 'Scissors'

def random_strategy():
    return np.random.choice(['Rock', 'Paper', 'Scissors'])

def counter_pattern(pattern):
    """Create a strategy that counters a specific pattern"""
    counter = {'Rock': 'Paper', 'Paper': 'Scissors', 'Scissors': 'Rock'}
    def strategy():
        move = next(pattern)
        return counter[move]
    return strategy

# Run tournament
strategies = {
    'Rock': always_rock,
    'Paper': always_paper,
    'Scissors': always_scissors,
    'Random': random_strategy,
}

print("🏆 RPS Tournament Results")
print("=" * 60)
print(f"{'Strategy A':<12} vs {'Strategy B':<12} | {'A Score':<10} | {'B Score':<10}")
print("-" * 60)

for name_a, strat_a in strategies.items():
    for name_b, strat_b in strategies.items():
        if name_a < name_b:
            score_a, score_b = rps_tournament(strat_a, strat_b)
            print(f"{name_a:<12} vs {name_b:<12} | {score_a:>9.0f} | {score_b:>9.0f}")
```

---

# MODULE 3: Battle of the Sexes

### 📖 WHAT Is It?

A couple wants to spend the evening together but prefers different activities:
- One prefers a football game
- The other prefers the opera
- Both prefer being together over being apart

**The Setup**:

| | **Partner B: Football** | **Partner B: Opera** |
|---|---|---|
| **Partner A: Football** | (2, 1) | (0, 0) |
| **Partner A: Opera** | (0, 0) | (1, 2) |

**The Challenge**: There are two Nash equilibria (Football, Football) and (Opera, Opera), but the players have conflicting preferences.

### 🤔 WHY Does It Matter?

The Battle of the Sexes demonstrates:
- Coordination games
- Multiple equilibria
- Communication and focal points
- Conflicting preferences within cooperation
- The importance of signaling and commitment

### 🛠️ HOW Does It Work in Code?

```python
class BattleOfSexes:
    """
    A class to model and analyze the Battle of the Sexes.
    """
    
    def __init__(self, a_preference='Football', b_preference='Opera'):
        self.strategies = ['Football', 'Opera']
        
        # Payoff matrix with asymmetric preferences
        if a_preference == 'Football' and b_preference == 'Opera':
            self.payoffs = {
                ('Football', 'Football'): (2, 1),
                ('Football', 'Opera'): (0, 0),
                ('Opera', 'Football'): (0, 0),
                ('Opera', 'Opera'): (1, 2)
            }
        else:
            # Reverse preferences
            self.payoffs = {
                ('Football', 'Football'): (1, 2),
                ('Football', 'Opera'): (0, 0),
                ('Opera', 'Football'): (0, 0),
                ('Opera', 'Opera'): (2, 1)
            }
        
        self.a_preference = a_preference
        self.b_preference = b_preference
        self.game_name = "Battle of the Sexes"
    
    def get_payoff(self, move_a, move_b):
        """Get payoffs for a given strategy pair"""
        return self.payoffs[(move_a, move_b)]
    
    def find_nash_equilibria(self):
        """
        Find all Nash equilibria (pure and mixed).
        """
        pure_equilibria = []
        
        for sa in self.strategies:
            for sb in self.strategies:
                pa_current, pb_current = self.get_payoff(sa, sb)
                
                # Check if either player can improve
                a_best = True
                b_best = True
                
                for sa_alt in self.strategies:
                    if sa_alt != sa:
                        pa_alt, _ = self.get_payoff(sa_alt, sb)
                        if pa_alt > pa_current:
                            a_best = False
                            break
                
                for sb_alt in self.strategies:
                    if sb_alt != sb:
                        _, pb_alt = self.get_payoff(sa, sb_alt)
                        if pb_alt > pb_current:
                            b_best = False
                            break
                
                if a_best and b_best:
                    pure_equilibria.append((sa, sb))
        
        # Find mixed strategy equilibrium
        # For Battle of the Sexes, the mixed equilibrium gives each player
        # a probability of picking their preferred outcome
        mixed_equilibria = self.find_mixed_equilibrium()
        
        return pure_equilibria, mixed_equilibria
    
    def find_mixed_equilibrium(self):
        """
        Find the mixed strategy Nash equilibrium.
        """
        # Let p = probability A chooses Football
        # Let q = probability B chooses Football
        # For A's indifference: 2q + 0(1-q) = 0q + 1(1-q)
        # => 2q = 1 - q => q = 1/3
        
        # For B's indifference: 1p + 0(1-p) = 0p + 2(1-p)
        # => p = 2 - 2p => 3p = 2 => p = 2/3
        
        # But this depends on preferences
        if self.a_preference == 'Football' and self.b_preference == 'Opera':
            return {
                'A_prob_football': 2/3,
                'B_prob_football': 1/3
            }
        else:
            return {
                'A_prob_football': 1/3,
                'B_prob_football': 2/3
            }
    
    def display_payoff_matrix(self):
        """Display the payoff matrix"""
        df = pd.DataFrame(index=self.strategies, columns=self.strategies)
        
        for sa in self.strategies:
            for sb in self.strategies:
                pa, pb = self.get_payoff(sa, sb)
                df.loc[sa, sb] = f"{pa},{pb}"
        
        print("Payoff Matrix (A, B)")
        print("=" * 30)
        print(df)

# Create and analyze the game
game = BattleOfSexes(a_preference='Football', b_preference='Opera')

print(f"🎮 {game.game_name}")
print("=" * 50)
game.display_payoff_matrix()

print("\n🎯 Nash Equilibria:")
print("-" * 50)
pure_eq, mixed_eq = game.find_nash_equilibria()
print("Pure Strategy Equilibria:")
for eq in pure_eq:
    print(f"  {eq}")
print("\nMixed Strategy Equilibrium:")
for k, v in mixed_eq.items():
    print(f"  {k}: {v:.3f}")

print("\n📊 Analysis:")
print("-" * 50)
print("• Two pure equilibria: (Football, Football) and (Opera, Opera)")
print("• Players prefer different equilibria")
print("• Mixed equilibrium where players randomize")
print("• Coordination is challenging without communication")
```

### 📊 Battle of the Sexes Visualization

```python
def visualize_battle_of_sexes(game, num_simulations=1000):
    """Visualize Battle of the Sexes dynamics"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Payoff matrix heatmap
    strategies = game.strategies
    n = len(strategies)
    payoff_a = np.zeros((n, n))
    payoff_b = np.zeros((n, n))
    
    for i, sa in enumerate(strategies):
        for j, sb in enumerate(strategies):
            pa, pb = game.get_payoff(sa, sb)
            payoff_a[i, j] = pa
            payoff_b[i, j] = pb
    
    # Combined heatmap with annotations
    combined = payoff_a + payoff_b
    sns.heatmap(combined, annot=True, fmt='.0f', xticklabels=strategies, 
                yticklabels=strategies, cmap='Blues', ax=axes[0],
                cbar_kws={'label': 'Total Utility'})
    axes[0].set_title('Combined Payoffs\n(High means Pareto efficient)')
    axes[0].set_xlabel("Player B's Strategy")
    axes[0].set_ylabel("Player A's Strategy")
    
    # Plot 2: Simulation of learning dynamics
    # Simulate players adjusting strategies over time
    p_A = 0.5  # Probability A chooses Football
    p_B = 0.5  # Probability B chooses Football
    
    history_A = []
    history_B = []
    
    for t in range(num_simulations):
        # Players adjust based on best response
        # A's expected payoff for Football: 2*p_B + 0*(1-p_B) = 2*p_B
        # A's expected payoff for Opera: 0*p_B + 1*(1-p_B) = 1-p_B
        # A's best response: Football if 2*p_B > 1-p_B, i.e., p_B > 1/3
        
        # B's expected payoff for Football: 1*p_A + 0*(1-p_A) = p_A
        # B's expected payoff for Opera: 0*p_A + 2*(1-p_A) = 2-2*p_A
        # B's best response: Football if p_A > 2 - 2*p_A, i.e., p_A > 2/3
        
        # Update probabilities with some inertia
        p_A = 0.9 * p_A + 0.1 * (1 if p_B > 1/3 else 0)
        p_B = 0.9 * p_B + 0.1 * (1 if p_A > 2/3 else 0)
        
        # Ensure probabilities stay in [0, 1]
        p_A = max(0, min(1, p_A))
        p_B = max(0, min(1, p_B))
        
        history_A.append(p_A)
        history_B.append(p_B)
    
    axes[1].plot(history_A, label="Player A's Football Probability", alpha=0.7)
    axes[1].plot(history_B, label="Player B's Football Probability", alpha=0.7)
    axes[1].axhline(y=1/3, color='gray', linestyle='--', alpha=0.5, label='A threshold (1/3)')
    axes[1].axhline(y=2/3, color='gray', linestyle=':', alpha=0.5, label='B threshold (2/3)')
    axes[1].set_xlabel('Iteration')
    axes[1].set_ylabel('Probability of Choosing Football')
    axes[1].set_title('Learning Dynamics (Best Response with Inertia)')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    axes[1].set_ylim(0, 1)
    
    plt.tight_layout()
    plt.show()

# Visualize
visualize_battle_of_sexes(game)
```

### 🧪 EXERCISE: Coordination with Communication

```python
def coordination_with_communication(communication_possible=True, num_simulations=10000):
    """Simulate coordination with and without communication"""
    
    def coordinate():
        # Players have a focal point (e.g., both pick 'Football')
        if communication_possible:
            # With communication, players can coordinate
            # Simulating that they reach a consensus (maybe 50/50)
            if np.random.random() < 0.6:
                return ('Football', 'Football')  # Focal point
            else:
                return ('Opera', 'Opera')  # Alternative
        else:
            # Without communication, random choice
            choice_a = np.random.choice(['Football', 'Opera'])
            choice_b = np.random.choice(['Football', 'Opera'])
            return (choice_a, choice_b)
    
    outcomes = Counter()
    total_payoff = 0
    
    for _ in range(num_simulations):
        moves = coordinate()
        payoff_a, payoff_b = game.get_payoff(moves[0], moves[1])
        total_payoff += payoff_a + payoff_b
        outcomes[moves] += 1
    
    print(f"{'Communication: ' + ('YES' if communication_possible else 'NO')}")
    print("-" * 50)
    print(f"Success rate: {sum(outcomes.values()) / num_simulations:.1%}")
    print(f"Average total payoff: {total_payoff / num_simulations:.2f}")
    print("Outcome frequencies:")
    for outcome, count in outcomes.most_common():
        print(f"  {outcome}: {count/num_simulations:.1%}")

print("📢 Coordination Analysis")
print("=" * 60)
coordination_with_communication(True)
print("\n" + "-" * 60 + "\n")
coordination_with_communication(False)
```

---

# MODULE 4: Cournot Competition

### 📖 WHAT Is It?

Two firms compete by choosing quantities of a homogeneous product. The market price depends on total quantity supplied.

**The Setup**:
- Firm 1 chooses quantity q₁
- Firm 2 chooses quantity q₂
- Market price: P = a - b(q₁ + q₂)
- Cost: C_i(q_i) = c * q_i
- Profit: π_i = (a - b(q₁ + q₂) - c) * q_i

**The Game**: Firms choose quantities simultaneously to maximize profit. The Nash equilibrium is where each firm's quantity is a best response to the other's quantity.

### 🤔 WHY Does It Matter?

Cournot competition demonstrates:
- Oligopoly behavior
- Strategic quantity setting
- Market power and competition
- How firms' profits depend on total industry output
- Applications in industrial organization

### 🛠️ HOW Does It Work in Code?

```python
class CournotCompetition:
    """
    A class to model Cournot duopoly competition.
    """
    
    def __init__(self, a=100, b=1, c=10):
        """
        Initialize Cournot model.
        
        Parameters:
        a: Demand intercept
        b: Demand slope
        c: Marginal cost (assumed constant)
        """
        self.a = a
        self.b = b
        self.c = c
        self.game_name = "Cournot Duopoly"
    
    def profit(self, q1, q2, player):
        """
        Calculate profit for a given player.
        
        Parameters:
        q1: Quantity of firm 1
        q2: Quantity of firm 2
        player: 1 or 2
        """
        Q = q1 + q2
        P = max(0, self.a - self.b * Q)  # Price cannot be negative
        
        if player == 1:
            return P * q1 - self.c * q1
        else:
            return P * q2 - self.c * q2
    
    def best_response(self, other_q, player):
        """
        Calculate best response quantity.
        """
        # For linear demand, best response is (a - c - b*other_q) / (2*b)
        q_br = (self.a - self.c - self.b * other_q) / (2 * self.b)
        return max(0, q_br)  # Cannot be negative
    
    def find_nash_equilibrium(self):
        """
        Find Nash equilibrium quantities.
        """
        # For symmetric Cournot: q1 = q2 = (a - c) / (3*b)
        q_eq = (self.a - self.c) / (3 * self.b)
        return q_eq, q_eq
    
    def simulate_reaction(self, num_rounds=10):
        """
        Simulate firms adjusting quantities over time.
        """
        q1_history = [0]
        q2_history = [0]
        
        for _ in range(num_rounds):
            q1_new = self.best_response(q2_history[-1], 1)
            q2_new = self.best_response(q1_history[-1], 2)
            
            q1_history.append(q1_new)
            q2_history.append(q2_new)
        
        return q1_history, q2_history
    
    def profit_landscape(self, q1_range, q2_range):
        """
        Calculate profit landscape for visualization.
        """
        q1_vals = np.linspace(*q1_range, 50)
        q2_vals = np.linspace(*q2_range, 50)
        
        profit1 = np.zeros((len(q1_vals), len(q2_vals)))
        profit2 = np.zeros((len(q1_vals), len(q2_vals)))
        
        for i, q1 in enumerate(q1_vals):
            for j, q2 in enumerate(q2_vals):
                profit1[i, j] = self.profit(q1, q2, 1)
                profit2[i, j] = self.profit(q1, q2, 2)
        
        return q1_vals, q2_vals, profit1, profit2

# Create a Cournot game
cournot = CournotCompetition(a=100, b=1, c=10)

print(f"🎮 {cournot.game_name}")
print("=" * 60)
print(f"Demand: P = {cournot.a} - {cournot.b}*Q")
print(f"Marginal Cost: c = {cournot.c}")
print(f"Demand Intercept: a = {cournot.a}")

q_eq = cournot.find_nash_equilibrium()
print(f"\n🎯 Nash Equilibrium Quantities:")
print(f"q₁* = q₂* = {q_eq[0]:.2f}")
print(f"Total Q = {q_eq[0] + q_eq[1]:.2f}")
print(f"Price = {cournot.a - cournot.b * (q_eq[0] + q_eq[1]):.2f}")
print(f"Profit per firm = {cournot.profit(q_eq[0], q_eq[1], 1):.2f}")

# Simulate reaction dynamics
q1_hist, q2_hist = cournot.simulate_reaction(15)

print(f"\n📊 Reaction Dynamics:")
print("-" * 60)
for t, (q1, q2) in enumerate(zip(q1_hist, q2_hist)):
    if t == 0:
        print(f"t={t}: q1={q1:.2f}, q2={q2:.2f} (initial)")
    else:
        print(f"t={t}: q1={q1:.2f}, q2={q2:.2f}")
```

### 📊 Cournot Competition Visualization

```python
def visualize_cournot(cournot):
    """Enhanced visualization of Cournot competition"""
    q1_range = (0, 50)
    q2_range = (0, 50)
    q1_vals, q2_vals, profit1, profit2 = cournot.profit_landscape(q1_range, q2_range)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # Plot 1: Profit landscape for Firm 1
    X, Y = np.meshgrid(q1_vals, q2_vals)
    contour1 = axes[0, 0].contourf(X, Y, profit1.T, levels=20, cmap='RdYlGn')
    axes[0, 0].set_xlabel('Firm 1 Quantity')
    axes[0, 0].set_ylabel('Firm 2 Quantity')
    axes[0, 0].set_title('Firm 1 Profit Landscape')
    plt.colorbar(contour1, ax=axes[0, 0])
    
    # Plot 2: Best response functions
    q1_br = [cournot.best_response(q2, 1) for q2 in np.linspace(0, 50, 100)]
    q2_br = [cournot.best_response(q1, 2) for q1 in np.linspace(0, 50, 100)]
    
    axes[0, 1].plot(np.linspace(0, 50, 100), q1_br, 'b-', label="Firm 1's Best Response", linewidth=2)
    axes[0, 1].plot(q2_br, np.linspace(0, 50, 100), 'r-', label="Firm 2's Best Response", linewidth=2)
    
    # Nash equilibrium point
    q_eq = cournot.find_nash_equilibrium()
    axes[0, 1].scatter(q_eq[0], q_eq[1], color='green', s=200, zorder=5, 
                      label=f'Nash Eq ({q_eq[0]:.1f}, {q_eq[1]:.1f})')
    
    axes[0, 1].set_xlabel('Firm 1 Quantity')
    axes[0, 1].set_ylabel('Firm 2 Quantity')
    axes[0, 1].set_title('Best Response Functions')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Reaction dynamics
    q1_hist, q2_hist = cournot.simulate_reaction(15)
    axes[1, 0].plot(q1_hist, q2_hist, 'bo-', alpha=0.7, linewidth=2, markersize=8)
    axes[1, 0].scatter(q1_hist[0], q2_hist[0], color='green', s=200, label='Start', zorder=5)
    axes[1, 0].scatter(q1_hist[-1], q2_hist[-1], color='red', s=200, label='End', zorder=5)
    axes[1, 0].set_xlabel('Firm 1 Quantity')
    axes[1, 0].set_ylabel('Firm 2 Quantity')
    axes[1, 0].set_title('Reaction Dynamics')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 4: Quantities and profits over time
    q1_hist, q2_hist = cournot.simulate_reaction(20)
    profits1 = [cournot.profit(q1, q2, 1) for q1, q2 in zip(q1_hist, q2_hist)]
    profits2 = [cournot.profit(q1, q2, 2) for q1, q2 in zip(q1_hist, q2_hist)]
    
    t = np.arange(len(q1_hist))
    axes[1, 1].plot(t, q1_hist, 'b-', label='Firm 1 Quantity', linewidth=2)
    axes[1, 1].plot(t, q2_hist, 'r-', label='Firm 2 Quantity', linewidth=2)
    axes[1, 1].set_xlabel('Time')
    axes[1, 1].set_ylabel('Quantity')
    axes[1, 1].set_title('Quantities Over Time')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# Visualize
visualize_cournot(cournot)
```

### 🧪 EXERCISE: Compare Cournot to Monopoly

```python
def compare_cournot_to_monopoly(a, b, c):
    """Compare Cournot competition to monopoly and perfect competition"""
    
    # Cournot equilibrium
    q_c = (a - c) / (3 * b)
    Q_c = 2 * q_c
    P_c = a - b * Q_c
    profit_c = (a - c)**2 / (9 * b)  # Per firm
    
    # Monopoly
    Q_m = (a - c) / (2 * b)
    P_m = a - b * Q_m
    profit_m = (a - c)**2 / (4 * b)
    
    # Perfect competition
    Q_pc = (a - c) / b
    P_pc = c
    profit_pc = 0
    
    results = {
        'Cournot': {'Q': Q_c, 'P': P_c, 'Profit': 2 * profit_c, 'Consumer_Surplus': 0.5 * (a - P_c) * Q_c},
        'Monopoly': {'Q': Q_m, 'P': P_m, 'Profit': profit_m, 'Consumer_Surplus': 0.5 * (a - P_m) * Q_m},
        'Perfect Competition': {'Q': Q_pc, 'P': P_pc, 'Profit': profit_pc, 'Consumer_Surplus': 0.5 * (a - P_pc) * Q_pc}
    }
    
    # Display results
    df = pd.DataFrame(results).T
    df.index.name = 'Market Structure'
    print("\n📊 Market Structure Comparison")
    print("=" * 70)
    print(df.round(2))
    
    # Calculate efficiency
    max_surplus = 0.5 * (a - c) * (a - c) / b  # Maximum possible total surplus
    
    for name, data in results.items():
        total_surplus = data['Profit'] + data['Consumer_Surplus']
        efficiency = total_surplus / max_surplus * 100
        print(f"{name} Efficiency: {efficiency:.1f}%")
    
    return results

# Compare market structures
results = compare_cournot_to_monopoly(a=100, b=1, c=10)
```

---

# MODULE 5: Evolutionary Game Theory

### 📖 WHAT Is It?

Evolutionary game theory studies how strategies evolve in populations over time. Strategies that yield higher payoffs become more prevalent through natural selection or social learning.

**Key Concepts**:
- **Replicator Dynamics**: Strategies with above-average payoffs increase in frequency
- **Evolutionarily Stable Strategy (ESS)**: A strategy that, if adopted by all, cannot be invaded by any mutant strategy
- **Cooperation Emergence**: How cooperation can emerge in populations

### 🤔 WHY Does It Matter?

Evolutionary game theory demonstrates:
- How cooperation evolves in nature
- The emergence of social norms and conventions
- Applications in biology, economics, and sociology
- The dynamics of strategy adoption and diffusion
- How populations converge to stable strategies

### 🛠️ HOW Does It Work in Code?

```python
class EvolutionaryGame:
    """
    A class to model evolutionary game dynamics.
    """
    
    def __init__(self, payoff_matrix, strategies):
        """
        Initialize evolutionary game.
        
        Parameters:
        payoff_matrix: Dict mapping (strategy_i, strategy_j) -> payoff
        strategies: List of available strategies
        """
        self.payoff_matrix = payoff_matrix
        self.strategies = strategies
        self.n_strategies = len(strategies)
    
    def expected_payoff(self, strategy, population_frequencies):
        """Calculate expected payoff for a strategy against the population."""
        total_payoff = 0
        for j, freq in enumerate(population_frequencies):
            total_payoff += self.payoff_matrix[(strategy, self.strategies[j])] * freq
        return total_payoff
    
    def population_payoff(self, population_frequencies):
        """Calculate average payoff in the population."""
        avg_payoff = 0
        for i, freq_i in enumerate(population_frequencies):
            avg_payoff += freq_i * self.expected_payoff(self.strategies[i], population_frequencies)
        return avg_payoff
    
    def replicator_dynamics(self, population_frequencies, delta_t=0.01):
        """
        Apply one step of replicator dynamics.
        """
        avg_payoff = self.population_payoff(population_frequencies)
        new_frequencies = []
        
        for i, freq in enumerate(population_frequencies):
            expected = self.expected_payoff(self.strategies[i], population_frequencies)
            growth = freq * (expected - avg_payoff)
            new_freq = freq + delta_t * growth
            new_frequencies.append(max(0, new_freq))
        
        # Normalize to sum to 1
        total = sum(new_frequencies)
        if total > 0:
            new_frequencies = [f/total for f in new_frequencies]
        else:
            new_frequencies = population_frequencies
        
        return new_frequencies
    
    def simulate_evolution(self, initial_frequencies, num_generations=1000, delta_t=0.01):
        """
        Simulate evolution over multiple generations.
        """
        history = [np.array(initial_frequencies)]
        
        for _ in range(num_generations):
            current = self.replicator_dynamics(history[-1], delta_t)
            history.append(np.array(current))
            
            # Check for convergence
            if np.max(np.abs(history[-1] - history[-2])) < 1e-6:
                break
        
        return np.array(history)

# Example: Hawk-Dove Game
class HawkDoveGame(EvolutionaryGame):
    """
    Hawk-Dove game model of conflict resolution.
    
    Hawks fight, Doves share.
    """
    
    def __init__(self, value=10, cost=50):
        """
        Initialize Hawk-Dove game.
        
        Parameters:
        value: Value of resource
        cost: Cost of fighting
        """
        strategies = ['Hawk', 'Dove']
        
        payoff_matrix = {
            ('Hawk', 'Hawk'): (value - cost) / 2,  # Both fight
            ('Hawk', 'Dove'): value,               # Hawk wins
            ('Dove', 'Hawk'): 0,                   # Dove loses
            ('Dove', 'Dove'): value / 2            # Both share
        }
        
        super().__init__(payoff_matrix, strategies)
        self.value = value
        self.cost = cost
        self.game_name = "Hawk-Dove Game"

# Create and analyze Hawk-Dove
hd = HawkDoveGame(value=10, cost=50)

print(f"🎮 {hd.game_name}")
print("=" * 60)
print(f"Resource Value: {hd.value}")
print(f"Fighting Cost: {hd.cost}")

print("\nPayoff Matrix:")
print("    " + "  ".join([f"{s:>8}" for s in hd.strategies]))
print("-" * 30)
for sa in hd.strategies:
    row = f"{sa:<6}"
    for sb in hd.strategies:
        payoff = hd.payoff_matrix[(sa, sb)]
        row += f"  {payoff:>8.1f}"
    print(row)

# Simulate evolution
initial_frequencies = [0.5, 0.5]  # Half Hawks, half Doves
history = hd.simulate_evolution(initial_frequencies, num_generations=500)

print(f"\n📊 Evolutionary Dynamics:")
print("-" * 60)
final = history[-1]
for s, freq in zip(hd.strategies, final):
    print(f"  {s}: {freq:.1%}")

# Find ESS
ess = []
for s in hd.strategies:
    # Check if s is an ESS
    is_ess = True
    for t in hd.strategies:
        if t != s:
            # s must do better against itself than t does against s
            payoff_ss = hd.payoff_matrix[(s, s)]
            payoff_ts = hd.payoff_matrix[(t, s)]
            if payoff_ts > payoff_ss:
                is_ess = False
                break
            elif payoff_ts == payoff_ss:
                # If equal, s must do better against t than t does against t
                payoff_st = hd.payoff_matrix[(s, t)]
                payoff_tt = hd.payoff_matrix[(t, t)]
                if payoff_st < payoff_tt:
                    is_ess = False
                    break
    
    if is_ess:
        ess.append(s)

print(f"\n🎯 Evolutionarily Stable Strategies: {ess if ess else 'None'}")
```

### 📊 Evolutionary Dynamics Visualization

```python
def visualize_evolutionary_game(history, strategies, game_name):
    """Visualize evolutionary game dynamics"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Strategy frequencies over time
    generations = np.arange(len(history))
    for i, strategy in enumerate(strategies):
        freq = history[:, i]
        axes[0].plot(generations, freq, label=strategy, linewidth=2)
    
    axes[0].set_xlabel('Generation')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title(f'{game_name}: Evolution of Strategies')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim(0, 1.05)
    
    # Plot 2: Phase portrait (simplex representation)
    if len(strategies) == 2:
        # 2 strategies - simple line plot
        freq1 = history[:, 0]
        axes[1].plot(freq1, 'b-', label='Hawk', linewidth=2)
        axes[1].plot(1 - freq1, 'r-', label='Dove', linewidth=2)
        axes[1].set_xlabel('Generation')
        axes[1].set_ylabel('Frequency')
        axes[1].set_title('Two-Strategy Dynamics')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        axes[1].set_ylim(0, 1.05)
        
        # Also show convergence point
        final_hawk = history[-1, 0]
        axes[1].axhline(y=final_hawk, color='gray', linestyle='--', alpha=0.5)
        axes[1].axhline(y=1-final_hawk, color='gray', linestyle='--', alpha=0.5)
    
    else:
        # 3 strategies - ternary plot (simplified)
        axes[1].text(0.5, 0.5, "Multi-strategy dynamics\n(use 3D visualization for better view)", 
                    ha='center', va='center', fontsize=12, transform=axes[1].transAxes)
        axes[1].set_title('Phase Portrait (Simplified)')
    
    plt.tight_layout()
    plt.show()

# Visualize Hawk-Dove evolution
visualize_evolutionary_game(history, hd.strategies, hd.game_name)
```

### 🧪 EXERCISE: Explore Different Payoffs

```python
def explore_hawk_dove_parameters():
    """Explore how changing parameters affects evolution"""
    values = [5, 10, 20]
    costs = [10, 30, 50]
    
    fig, axes = plt.subplots(len(values), len(costs), figsize=(12, 8))
    
    for i, value in enumerate(values):
        for j, cost in enumerate(costs):
            hd = HawkDoveGame(value=value, cost=cost)
            hist = hd.simulate_evolution([0.5, 0.5], num_generations=300)
            
            ax = axes[i, j]
            ax.plot(hist[:, 0], label='Hawk', color='blue', linewidth=2)
            ax.plot(hist[:, 1], label='Dove', color='red', linewidth=2)
            ax.set_title(f'V={value}, C={cost}')
            ax.set_ylim(0, 1)
            ax.grid(True, alpha=0.3)
            if j == 0:
                ax.set_ylabel('Frequency')
            if i == len(values) - 1:
                ax.set_xlabel('Generation')
    
    plt.tight_layout()
    plt.show()
    
    print("📊 Observations:")
    print("-" * 60)
    print("• When V > C/2: Hawks dominate (fighting is worthwhile)")
    print("• When V < C/2: Doves dominate (fighting is too costly)")
    print("• When V = C/2: Mixed equilibrium (Hawk-Dove balance)")

# Run the exploration
explore_hawk_dove_parameters()
```

---

# MODULE 6: Game Theory + Monte Carlo Integration

### 📖 WHAT Is It?

Combining game theory and Monte Carlo simulation to analyze strategic situations with random uncertainty.

**The Intersection**:
- **Game Theory**: Provides the strategic framework (players, strategies, payoffs)
- **Monte Carlo**: Handles random uncertainty (unknown events, stochastic outcomes)
- **Together**: Analyzing real-world strategic situations

### 🤔 WHY Does It Matter?

This integration is crucial for understanding:
- Strategic uncertainty (what will others do?)
- Random uncertainty (what random events will occur?)
- Complex real-world systems (financial markets, warfare, politics)
- How to make decisions when both types of uncertainty exist

### 🛠️ HOW Does It Work in Code?

```python
class StrategicGameWithUncertainty:
    """
    A game that combines strategic decision-making with random uncertainty.
    """
    
    def __init__(self, num_players, strategies, payoff_matrix, random_events=None):
        """
        Initialize the game.
        
        Parameters:
        num_players: Number of players
        strategies: List of available strategies for each player
        payoff_matrix: Payoff for each strategy combination
        random_events: List of random events with probabilities
        """
        self.num_players = num_players
        self.strategies = strategies
        self.payoff_matrix = payoff_matrix
        self.random_events = random_events or [{'name': 'No Event', 'modifier': 1.0, 'probability': 1.0}]
        self.history = []
    
    def play_round(self, strategy_choices, seed=None):
        """
        Play one round with given strategies.
        """
        if seed is not None:
            np.random.seed(seed)
        
        # Determine which random event occurs
        probs = [e['probability'] for e in self.random_events]
        probs = np.array(probs) / np.sum(probs)  # Normalize
        event_idx = np.random.choice(len(self.random_events), p=probs)
        event = self.random_events[event_idx]
        
        # Calculate payoff based on strategies and event
        base_payoff = self.payoff_matrix[tuple(strategy_choices)]
        
        # Modify payoff based on random event
        payoff_modifier = event.get('modifier', 1.0)
        event_name = event.get('name', 'No event')
        
        # Return payoff and event information
        return base_payoff * payoff_modifier, event_name
    
    def monte_carlo_analysis(self, num_simulations=10000, seed=None):
        """
        Run Monte Carlo simulation to analyze strategy performance.
        """
        if seed is not None:
            np.random.seed(seed)
        
        # Track results
        strategy_payoffs = defaultdict(float)
        strategy_counts = defaultdict(int)
        event_counts = Counter()
        
        for _ in range(num_simulations):
            # Randomly select strategies for each player
            strategy_tuple = tuple(
                np.random.choice(self.strategies[i]) 
                for i in range(self.num_players)
            )
            
            # Play the round
            payoff, event = self.play_round(strategy_tuple)
            
            # Record results
            strategy_key = ', '.join(f'P{i+1}: {s}' 
                                    for i, s in enumerate(strategy_tuple))
            strategy_payoffs[strategy_key] += payoff
            strategy_counts[strategy_key] += 1
            event_counts[event] += 1
        
        # Calculate average payoffs
        avg_payoffs = {
            key: strategy_payoffs[key] / strategy_counts[key]
            for key in strategy_payoffs.keys()
        }
        
        return avg_payoffs, strategy_counts, event_counts

# Example: Market Competition with Random Events
def run_strategic_game_with_uncertainty():
    """
    Example: A market competition game with random market conditions.
    """
    
    # Define strategies for two firms
    strategies = [
        ['Aggressive', 'Moderate', 'Passive'],  # Firm A
        ['Aggressive', 'Moderate', 'Passive']   # Firm B
    ]
    
    # Define payoff matrix (A's payoff, B's payoff)
    payoff_matrix = {}
    
    # Aggressive vs Aggressive: Both lose from price war
    payoff_matrix[('Aggressive', 'Aggressive')] = (2, 2)
    # Aggressive vs Moderate: Aggressive gains
    payoff_matrix[('Aggressive', 'Moderate')] = (6, 1)
    # Aggressive vs Passive: Aggressive dominates
    payoff_matrix[('Aggressive', 'Passive')] = (8, -1)
    # Moderate vs Aggressive: Aggressive wins
    payoff_matrix[('Moderate', 'Aggressive')] = (1, 6)
    # Moderate vs Moderate: Cooperation
    payoff_matrix[('Moderate', 'Moderate')] = (4, 4)
    # Moderate vs Passive: Moderate wins
    payoff_matrix[('Moderate', 'Passive')] = (5, 2)
    # Passive vs Aggressive: Aggressive wins
    payoff_matrix[('Passive', 'Aggressive')] = (-1, 8)
    # Passive vs Moderate: Moderate wins
    payoff_matrix[('Passive', 'Moderate')] = (2, 5)
    # Passive vs Passive: Both do poorly
    payoff_matrix[('Passive', 'Passive')] = (1, 1)
    
    # Define random events
    random_events = [
        {'name': 'Boom', 'modifier': 1.4, 'probability': 0.2},
        {'name': 'Normal', 'modifier': 1.0, 'probability': 0.5},
        {'name': 'Recession', 'modifier': 0.6, 'probability': 0.2},
        {'name': 'Crisis', 'modifier': 0.3, 'probability': 0.1}
    ]
    
    # Create and run the game
    game = StrategicGameWithUncertainty(2, strategies, payoff_matrix, random_events)
    avg_payoffs, counts, events = game.monte_carlo_analysis(10000, seed=42)
    
    print("🎮 Game Theory + Monte Carlo Analysis")
    print("=" * 70)
    print("Strategic Game: Market Competition with Random Events")
    print("-" * 70)
    print("Strategies: Aggressive, Moderate, Passive")
    print("Events: Boom (x1.4), Normal (x1.0), Recession (x0.6), Crisis (x0.3)")
    print("-" * 70)
    print("Strategy Pair".ljust(35) + "|" + "Avg Payoff".center(15) + "|" + "Frequency".center(15))
    print("-" * 70)
    
    total_count = sum(counts.values())
    for strategy, avg_payoff in sorted(avg_payoffs.items(), key=lambda x: x[1], reverse=True):
        count = counts[strategy]
        pct = count / total_count * 100
        print(f"{strategy[:35].ljust(35)} | {avg_payoff:>14.2f} | {pct:>14.1f}%")
    
    print("\n" + "-" * 70)
    print("Event Frequencies:")
    for event, count in events.items():
        print(f"  {event}: {count/10000:.1%}")
    
    print("\n📊 Key Insights:")
    print("-" * 70)
    print("• The optimal strategy depends on market conditions")
    print("• Aggressive strategies perform best in booms")
    print("• Moderate strategies are more robust to downturns")
    print("• Monte Carlo reveals the distribution of outcomes")
    
    return avg_payoffs, counts, events

# Run the analysis
avg_payoffs, counts, events = run_strategic_game_with_uncertainty()
```

### 📊 Visualization: Game Theory + Monte Carlo

```python
def visualize_game_with_uncertainty(avg_payoffs, counts, events):
    """Visualize strategic game with uncertainty results"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Plot 1: Average payoffs by strategy
    strategies = list(avg_payoffs.keys())
    payoffs = list(avg_payoffs.values())
    
    # Sort by payoff
    sorted_pairs = sorted(zip(strategies, payoffs), key=lambda x: x[1], reverse=True)
    strategies_sorted, payoffs_sorted = zip(*sorted_pairs)
    
    # Truncate long strategy names for display
    display_names = [s[:25] + '...' if len(s) > 25 else s for s in strategies_sorted]
    
    colors = ['green' if p > 4 else 'orange' if p > 2 else 'red' for p in payoffs_sorted]
    bars = axes[0].bar(display_names, payoffs_sorted, color=colors, alpha=0.7)
    axes[0].set_xlabel('Strategy Pair')
    axes[0].set_ylabel('Average Payoff')
    axes[0].set_title('Average Payoffs by Strategy')
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # Plot 2: Strategy frequency
    total_count = sum(counts.values())
    frequencies = [counts[s] / total_count for s in strategies_sorted]
    bars = axes[1].bar(display_names, frequencies, color='blue', alpha=0.7)
    axes[1].set_xlabel('Strategy Pair')
    axes[1].set_ylabel('Frequency (%)')
    axes[1].set_title('Strategy Usage Frequency')
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].grid(True, alpha=0.3, axis='y')
    
    # Plot 3: Event distribution
    event_names = list(events.keys())
    event_counts = [events[e] for e in event_names]
    event_pcts = [c / sum(event_counts) * 100 for c in event_counts]
    
    axes[2].pie(event_pcts, labels=event_names, autopct='%1.1f%%', 
                startangle=90, colors=['green', 'blue', 'orange', 'red'])
    axes[2].set_title('Random Event Distribution')
    
    plt.tight_layout()
    plt.show()
    
    print("\n📊 Strategy Performance Summary:")
    print("-" * 60)
    for s, p in sorted(zip(strategies_sorted, payoffs_sorted), key=lambda x: x[1], reverse=True):
        freq = counts[s] / total_count * 100
        print(f"{s[:40]:<40} | Avg: {p:>6.2f} | Freq: {freq:>6.1f}%")

# Visualize results
visualize_game_with_uncertainty(avg_payoffs, counts, events)
```

---

# MODULE 7: Auctions

### 📖 WHAT Is It?

Auctions are strategic games where bidders compete for items. Different auction formats lead to different bidding strategies.

**Common Auction Types**:
- **English Auction**: Ascending price, bidders raise bids until only one remains
- **Dutch Auction**: Descending price, first bidder to accept wins
- **First-Price Sealed-Bid**: Each bidder submits one bid, highest wins
- **Second-Price Sealed-Bid (Vickrey)**: Highest wins but pays second-highest bid

### 🤔 WHY Does It Matter?

Auctions demonstrate:
- Strategic bidding and revenue equivalence
- Winner's curse and information asymmetry
- Applications in business, government, and online markets
- How different auction designs affect outcomes

### 🛠️ HOW Does It Work in Code?

```python
class AuctionSimulator:
    """
    A class to simulate different auction formats.
    """
    
    def __init__(self, num_bidders, valuations, num_items=1):
        """
        Initialize auction.
        
        Parameters:
        num_bidders: Number of bidders
        valuations: List of valuations (private values)
        num_items: Number of items for sale
        """
        self.num_bidders = num_bidders
        self.valuations = valuations
        self.num_items = num_items
        self.bids = [None] * num_bidders
    
    def english_auction(self):
        """
        Simulate an English (ascending) auction.
        """
        remaining_bidders = list(range(self.num_bidders))
        current_price = 0
        active_bids = {i: 0 for i in range(self.num_bidders)}
        
        while len(remaining_bidders) > 1:
            current_price += 0.1  # Increment
            
            # Check who is willing to bid
            new_remaining = []
            for bidder in remaining_bidders:
                if self.valuations[bidder] >= current_price:
                    new_remaining.append(bidder)
                    active_bids[bidder] = current_price
            
            remaining_bidders = new_remaining
        
        winner = remaining_bidders[0] if remaining_bidders else None
        price = active_bids[winner] if winner is not None else 0
        
        return winner, price
    
    def sealed_bid_auction(self, is_first_price=True):
        """
        Simulate a sealed-bid auction.
        
        Parameters:
        is_first_price: True for first-price, False for second-price (Vickrey)
        """
        # Bidders submit bids (can be strategic)
        # Simplified: bidders bid their true value in Vickrey,
        # but shade bids in first-price
        bids = []
        
        for i, valuation in enumerate(self.valuations):
            if is_first_price:
                # Strategic shading: bid a fraction of true value
                # In equilibrium, bid = (n-1)/n * valuation
                bid = (self.num_bidders - 1) / self.num_bidders * valuation
            else:
                # In Vickrey, bidding true value is dominant strategy
                bid = valuation
            
            # Add random noise for realism
            bid *= np.random.uniform(0.95, 1.05)
            bids.append(max(0, bid))
        
        # Sort bids descending
        sorted_bids = sorted(enumerate(bids), key=lambda x: x[1], reverse=True)
        
        if is_first_price:
            winner = sorted_bids[0][0]
            price = sorted_bids[0][1]
        else:
            winner = sorted_bids[0][0]
            price = sorted_bids[1][1] if len(sorted_bids) > 1 else 0
        
        return winner, price, bids
    
    def dutch_auction(self):
        """
        Simulate a Dutch (descending) auction.
        """
        price = 100  # Starting price
        
        while price > 0:
            # Check if any bidder accepts current price
            for bidder in range(self.num_bidders):
                if self.valuations[bidder] >= price:
                    return bidder, price
            price -= 0.5
        
        return None, 0

# Run auction simulations
def analyze_auctions(num_bidders=10, min_value=50, max_value=100):
    """Analyze different auction formats"""
    
    # Generate random valuations
    np.random.seed(42)
    valuations = np.random.uniform(min_value, max_value, num_bidders)
    
    auction = AuctionSimulator(num_bidders, valuations)
    
    results = {
        'English': [],
        'First-Price': [],
        'Second-Price (Vickrey)': [],
        'Dutch': []
    }
    
    # Run multiple simulations
    for _ in range(1000):
        # English auction
        winner_eng, price_eng = auction.english_auction()
        if winner_eng is not None:
            results['English'].append(price_eng)
        
        # First-price sealed bid
        winner_fp, price_fp, _ = auction.sealed_bid_auction(is_first_price=True)
        if winner_fp is not None:
            results['First-Price'].append(price_fp)
        
        # Second-price sealed bid
        winner_sp, price_sp, _ = auction.sealed_bid_auction(is_first_price=False)
        if winner_sp is not None:
            results['Second-Price (Vickrey)'].append(price_sp)
        
        # Dutch auction
        winner_dutch, price_dutch = auction.dutch_auction()
        if winner_dutch is not None:
            results['Dutch'].append(price_dutch)
    
    # Analyze results
    print("🏆 Auction Analysis")
    print("=" * 70)
    print(f"Number of Bidders: {num_bidders}")
    print(f"Valuation Range: {min_value:.0f} - {max_value:.0f}")
    print("-" * 70)
    print(f"{'Auction Type':<25} | {'Avg Price':>12} | {'Std Dev':>12} | {'Revenue':>12}")
    print("-" * 70)
    
    for auction_type, prices in results.items():
        if prices:
            avg = np.mean(prices)
            std = np.std(prices)
            revenue = avg * auction.num_items
            print(f"{auction_type:<25} | {avg:>12.2f} | {std:>12.2f} | {revenue:>12.2f}")
    
    # Calculate efficiency
    max_valuation = max(valuations)
    print("\n📊 Efficiency Analysis:")
    print("-" * 70)
    for auction_type, prices in results.items():
        if prices:
            avg_winner_surplus = max_valuation - np.mean(prices)
            print(f"{auction_type}: Average Winner Surplus = {avg_winner_surplus:.2f}")

# Run auction analysis
analyze_auctions()
```

---

# MODULE 8: Nash Equilibrium Solver

### 📖 WHAT Is It?

A general-purpose Nash equilibrium solver for normal-form games.

**The Approach**:
1. Pure strategy equilibria: Check all strategy combinations
2. Mixed strategy equilibria: Solve using linear programming or iterative methods
3. Visualization: Show best response regions and equilibria

### 🤔 WHY Does It Matter?

Nash equilibrium is the fundamental solution concept in game theory. Understanding how to find equilibria helps analyze strategic situations across all domains.

### 🛠️ HOW Does It Work in Code?

```python
class NashEquilibriumSolver:
    """
    General-purpose Nash equilibrium solver for normal-form games.
    """
    
    def __init__(self, payoff_matrix_a, payoff_matrix_b, strategies_a, strategies_b):
        """
        Initialize the game.
        
        Parameters:
        payoff_matrix_a: Player A's payoffs (n x m matrix)
        payoff_matrix_b: Player B's payoffs (n x m matrix)
        strategies_a: List of Player A's strategies
        strategies_b: List of Player B's strategies
        """
        self.payoff_a = np.array(payoff_matrix_a)
        self.payoff_b = np.array(payoff_matrix_b)
        self.strategies_a = strategies_a
        self.strategies_b = strategies_b
        self.n = len(strategies_a)
        self.m = len(strategies_b)
    
    def pure_strategy_equilibria(self):
        """
        Find all pure strategy Nash equilibria.
        """
        equilibria = []
        
        for i in range(self.n):
            for j in range(self.m):
                # Check if this is a Nash equilibrium
                is_eq = True
                
                # Check Player A's best response
                payoff_current_a = self.payoff_a[i, j]
                for i2 in range(self.n):
                    if self.payoff_a[i2, j] > payoff_current_a:
                        is_eq = False
                        break
                
                if not is_eq:
                    continue
                
                # Check Player B's best response
                payoff_current_b = self.payoff_b[i, j]
                for j2 in range(self.m):
                    if self.payoff_b[i, j2] > payoff_current_b:
                        is_eq = False
                        break
                
                if is_eq:
                    equilibria.append((self.strategies_a[i], self.strategies_b[j]))
        
        return equilibria
    
    def best_response_regions(self):
        """
        Calculate best response regions for visualization.
        """
        # For mixed strategies, identify best responses
        # Simplified: return best responses for pure strategies
        br_a = {}
        br_b = {}
        
        for j in range(self.m):
            # Player A's best response to B's pure strategy
            max_payoff = np.max(self.payoff_a[:, j])
            br_a[self.strategies_b[j]] = [
                self.strategies_a[i] 
                for i in range(self.n) 
                if self.payoff_a[i, j] == max_payoff
            ]
        
        for i in range(self.n):
            # Player B's best response to A's pure strategy
            max_payoff = np.max(self.payoff_b[i, :])
            br_b[self.strategies_a[i]] = [
                self.strategies_b[j] 
                for j in range(self.m) 
                if self.payoff_b[i, j] == max_payoff
            ]
        
        return br_a, br_b
    
    def solve_mixed_strategy(self, max_iterations=1000, tol=1e-6):
        """
        Solve for mixed strategy Nash equilibrium using iterative method.
        
        This uses the replicator dynamics to converge to Nash equilibrium.
        """
        # Initialize random strategies
        p = np.ones(self.n) / self.n  # Player A's mixed strategy
        q = np.ones(self.m) / self.m  # Player B's mixed strategy
        
        for iteration in range(max_iterations):
            # Expected payoffs for Player A
            exp_payoff_a = self.payoff_a @ q
            
            # Expected payoffs for Player B
            exp_payoff_b = p @ self.payoff_b
            
            # Update strategies using replicator dynamics
            avg_payoff_a = p @ exp_payoff_a
            avg_payoff_b = exp_payoff_b @ q
            
            p_new = p * (exp_payoff_a / avg_payoff_a)
            q_new = q * (exp_payoff_b / avg_payoff_b)
            
            # Normalize
            p_new = p_new / np.sum(p_new)
            q_new = q_new / np.sum(q_new)
            
            # Check for convergence
            if (np.max(np.abs(p_new - p)) < tol and 
                np.max(np.abs(q_new - q)) < tol):
                break
            
            p = p_new
            q = q_new
        
        return p, q

# Example: Prisoner's Dilemma
print("🎯 Nash Equilibrium Solver")
print("=" * 70)

# Prisoner's Dilemma
payoff_a = np.array([[3, 0], [5, 1]])
payoff_b = np.array([[3, 5], [0, 1]])
strategies_a = ['Cooperate', 'Defect']
strategies_b = ['Cooperate', 'Defect']

solver = NashEquilibriumSolver(payoff_a, payoff_b, strategies_a, strategies_b)

print("📊 Prisoner's Dilemma")
print("-" * 70)
print("Payoff Matrix (A, B):")
for i, sa in enumerate(strategies_a):
    row = f"{sa:<10}"
    for j in range(len(strategies_b)):
        row += f"  ({payoff_a[i,j]}, {payoff_b[i,j]})"
    print(row)

pure_eq = solver.pure_strategy_equilibria()
print(f"\nPure Strategy Equilibria: {pure_eq}")

mixed_p, mixed_q = solver.solve_mixed_strategy()
print("\nMixed Strategy Equilibrium:")
print(f"  Player A: { {s: p for s, p in zip(strategies_a, mixed_p)} }")
print(f"  Player B: { {s: q for s, q in zip(strategies_b, mixed_q)} }")

# Example: Battle of the Sexes
print("\n" + "=" * 70)
print("📊 Battle of the Sexes")
print("-" * 70)

payoff_a = np.array([[2, 0], [0, 1]])
payoff_b = np.array([[1, 0], [0, 2]])
strategies_a = ['Football', 'Opera']
strategies_b = ['Football', 'Opera']

solver = NashEquilibriumSolver(payoff_a, payoff_b, strategies_a, strategies_b)

print("Payoff Matrix (A, B):")
for i, sa in enumerate(strategies_a):
    row = f"{sa:<10}"
    for j in range(len(strategies_b)):
        row += f"  ({payoff_a[i,j]}, {payoff_b[i,j]})"
    print(row)

pure_eq = solver.pure_strategy_equilibria()
print(f"\nPure Strategy Equilibria: {pure_eq}")

mixed_p, mixed_q = solver.solve_mixed_strategy()
print("\nMixed Strategy Equilibrium:")
print(f"  Player A: { {s: p for s, p in zip(strategies_a, mixed_p)} }")
print(f"  Player B: { {s: q for s, q in zip(strategies_b, mixed_q)} }")
```

---

# 🎓 Further Learning & Resources

## 📚 Books
1. **"Strategy: An Introduction to Game Theory"** - Joel Watson
2. **"Games of Strategy"** - Dixit, Skeath, Reiley
3. **"Theory of Games and Economic Behavior"** - von Neumann & Morgenstern
4. **"Evolutionary Game Theory"** - Jörgen Weibull

## 📺 Video Courses
1. **"Game Theory"** - Yale University (Open Yale Courses)
2. **"Game Theory 101"** - William Spaniel (YouTube)
3. **"Introduction to Game Theory"** - Stanford (Coursera)

## 🛠️ Python Libraries
1. **Axelrod** - Iterated Prisoner's Dilemma
2. **NashPy** - Nash equilibrium computation
3. **NetworkX** - Game theory on graphs
4. **GameTheory** - Various game theory tools

## 🌐 Online Resources
1. **"Game Theory Explorer"** - Interactive game theory
2. **"Nash Equilibrium Calculator"** - Online solver
3. **"The Evolution of Trust"** - Interactive game theory demo
4. **"Google's Game Theory"** - Applied game theory

---

# 🎓 Certificate of Completion

Congratulations on completing the Game Theory & Strategic Decision-Making Workbook!

### ✅ Skills Acquired
- [ ] Understanding strategic decision-making and incentives
- [ ] Analyzing classic games (Prisoner's Dilemma, Rock-Paper-Scissors, etc.)
- [ ] Finding Nash equilibria (pure and mixed)
- [ ] Modeling coordination and cooperation problems
- [ ] Implementing game theory in Python
- [ ] Integrating game theory with Monte Carlo simulation
- [ ] Understanding evolutionary game dynamics
- [ ] Analyzing auctions and bidding strategies

### 📊 Project Ideas
1. **Build an auction simulator** for different auction formats
2. **Create a tournament** for iterated Prisoner's Dilemma
3. **Model a market** with strategic firms
4. **Simulate evolution** of cooperation in populations
5. **Design a game** with Monte Carlo uncertainty

### 📝 Final Assessment
```python
# Final Project: Build a complete game theory simulation
# Choose one application:
# 1. Market competition with multiple firms
# 2. Political campaign strategy
# 3. Supply chain negotiation
# 4. International diplomacy game
# 5. Evolutionary cooperation model
```

---

*Monte Carlo methods provide the computational engine, but game theory provides the strategic framework. Together, they offer a complete toolkit for understanding complex interactive systems.*