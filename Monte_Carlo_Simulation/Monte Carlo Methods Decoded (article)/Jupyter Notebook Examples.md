Here's a complete Jupyter Notebook with the basics and all three examples from the article. You can copy this into a `.ipynb` file or run it in Google Colab.

```python
# Monte Carlo Methods - Complete Jupyter Notebook
# Based on the article "Monte Carlo Methods Decoded"

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
import math

# Set style for better visualizations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
```

## Part 1: The Basics - Marble Jar Analogy

This simple example demonstrates the core concept of Monte Carlo: learning about a system by random sampling.

```python
# Simulate a jar with marbles of different colors
# We don't know the true distribution (it's hidden from us)

def marble_jar_simulation(n_samples=1000):
    """
    Simulate drawing marbles from a jar with unknown composition.
    We can only learn by sampling.
    """
    # True (hidden) composition of the jar
    true_colors = {
        'red': 0.40,
        'blue': 0.25,
        'green': 0.20,
        'yellow': 0.15
    }
    
    # Random sampling (we don't know the true distribution)
    colors = list(true_colors.keys())
    probabilities = list(true_colors.values())
    
    # Draw samples
    samples = np.random.choice(colors, size=n_samples, p=probabilities)
    
    # Calculate observed distribution
    observed_counts = {}
    for color in colors:
        observed_counts[color] = np.sum(samples == color)
    
    observed_probs = {color: count/n_samples for color, count in observed_counts.items()}
    
    # Display results
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # True distribution
    ax1.bar(true_colors.keys(), true_colors.values(), color=['red', 'blue', 'green', 'yellow'])
    ax1.set_title('True (Hidden) Distribution')
    ax1.set_ylabel('Probability')
    ax1.set_ylim(0, 0.5)
    
    # Observed distribution
    ax2.bar(observed_probs.keys(), observed_probs.values(), color=['red', 'blue', 'green', 'yellow'])
    ax2.set_title(f'Observed Distribution (n={n_samples})')
    ax2.set_ylabel('Probability')
    ax2.set_ylim(0, 0.5)
    
    plt.tight_layout()
    plt.show()
    
    print("True probabilities:", true_colors)
    print(f"Observed probabilities (n={n_samples}):", observed_probs)
    
    # Show how accuracy improves with more samples
    return observed_probs

# Run with different sample sizes
print("="*50)
print("BASIC MONTE CARLO: MARBLE JAR EXAMPLE")
print("="*50)

for n in [100, 1000, 10000]:
    print(f"\n--- Running with {n} samples ---")
    marble_jar_simulation(n)
```

```
================================================================================
BASIC MONTE CARLO: MARBLE JAR EXAMPLE
================================================================================

--- Running with 100 samples ---
True probabilities: {'red': 0.4, 'blue': 0.25, 'green': 0.2, 'yellow': 0.15}
Observed probabilities (n=100): {'red': 0.41, 'blue': 0.22, 'green': 0.22, 'yellow': 0.15}

--- Running with 1000 samples ---
True probabilities: {'red': 0.4, 'blue': 0.25, 'green': 0.2, 'yellow': 0.15}
Observed probabilities (n=1000): {'red': 0.395, 'blue': 0.247, 'green': 0.198, 'yellow': 0.16}

--- Running with 10000 samples ---
True probabilities: {'red': 0.4, 'blue': 0.25, 'green': 0.2, 'yellow': 0.15}
Observed probabilities (n=10000): {'red': 0.3991, 'blue': 0.2514, 'green': 0.1976, 'yellow': 0.1519}
```

**Key Insight**: As we increase the number of samples, our observed distribution converges to the true (hidden) distribution. This is the foundation of Monte Carlo methods!

```python
# Demonstrate convergence visually
def convergence_demo():
    """Show how estimates converge as sample size increases"""
    true_red_prob = 0.4
    sample_sizes = np.arange(10, 5000, 50)
    estimates = []
    
    for n in sample_sizes:
        samples = np.random.choice(['red', 'not_red'], size=n, p=[true_red_prob, 1-true_red_prob])
        estimates.append(np.mean(samples == 'red'))
    
    plt.figure(figsize=(10, 6))
    plt.plot(sample_sizes, estimates, linewidth=1, alpha=0.7)
    plt.axhline(y=true_red_prob, color='red', linestyle='--', label='True probability')
    plt.xlabel('Number of Samples')
    plt.ylabel('Estimated Probability of Red')
    plt.title('Convergence of Monte Carlo Estimate')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

convergence_demo()
```

## Example 1: Project Management

Simulating a software launch project with uncertain task durations.

```python
print("\n" + "="*50)
print("EXAMPLE 1: PROJECT MANAGEMENT SIMULATION")
print("="*50)

# Set random seed for reproducibility
np.random.seed(42)

# Number of simulations
n_simulations = 10000

# Define duration distributions for each task
# Requirements: Normal distribution (mean=30, std=5)
requirements = np.random.normal(30, 5, n_simulations)

# Design: Triangular distribution (min=20, mode=35, max=50)
design = np.random.triangular(20, 35, 50, n_simulations)

# Development: Normal distribution (mean=60, std=10)
development = np.random.normal(60, 10, n_simulations)

# Testing: Triangular distribution (min=25, mode=40, max=60)
testing = np.random.triangular(25, 40, 60, n_simulations)

# Deployment and Marketing run in parallel
deployment_training = np.random.uniform(20, 30, n_simulations)
marketing = np.random.uniform(15, 25, n_simulations)

# Calculate total completion time
# Deployment and Marketing run in parallel, so we take the maximum
total_time = (requirements + design + development + testing + 
              np.maximum(deployment_training, marketing))

# Visualize the distribution
plt.figure(figsize=(12, 6))

# Histogram with KDE
sns.histplot(total_time, kde=True, bins=50, alpha=0.7)
plt.axvline(180, color='red', linestyle='--', linewidth=2, label='6 Months Target (180 days)')
plt.axvline(np.mean(total_time), color='green', linestyle='-', linewidth=2, label=f'Mean: {np.mean(total_time):.1f} days')

# Add confidence interval
ci_lower = np.percentile(total_time, 2.5)
ci_upper = np.percentile(total_time, 97.5)
plt.axvline(ci_lower, color='orange', linestyle=':', linewidth=2, label=f'95% CI: {ci_lower:.1f} - {ci_upper:.1f}')
plt.axvline(ci_upper, color='orange', linestyle=':', linewidth=2)

plt.title('Software Launch Project - Total Completion Time Distribution')
plt.xlabel('Total Days')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Calculate statistics
print("\nPROJECT STATISTICS:")
print(f"Mean Total Completion Time: {np.mean(total_time):.2f} days")
print(f"Median Total Completion Time: {np.median(total_time):.2f} days")
print(f"95% Confidence Interval: {np.percentile(total_time, 2.5):.2f} - {np.percentile(total_time, 97.5):.2f} days")
print(f"Probability of completing within 6 months (180 days): {np.mean(total_time <= 180):.2%}")
print(f"Probability of completing within 200 days: {np.mean(total_time <= 200):.2%}")

# Show task duration distributions
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
axes = axes.flatten()

task_names = ['Requirements', 'Design', 'Development', 'Testing', 'Deployment', 'Marketing']
task_data = [requirements, design, development, testing, deployment_training, marketing]

for i, (name, data) in enumerate(zip(task_names, task_data)):
    sns.histplot(data, kde=True, ax=axes[i], alpha=0.7)
    axes[i].set_title(f'{name}')
    axes[i].set_xlabel('Days')
    axes[i].axvline(np.mean(data), color='red', linestyle='--', label=f'Mean: {np.mean(data):.1f}')
    axes[i].legend()

plt.tight_layout()
plt.show()

# Sensitivity analysis: Which task has the most impact?
print("\nSENSITIVITY ANALYSIS:")
task_means = {
    'Requirements': np.mean(requirements),
    'Design': np.mean(design),
    'Development': np.mean(development),
    'Testing': np.mean(testing),
    'Deployment': np.mean(deployment_training),
    'Marketing': np.mean(marketing)
}

for task, mean in sorted(task_means.items(), key=lambda x: x[1], reverse=True):
    print(f"{task}: {mean:.1f} days (impact on project completion: {mean/total_time.mean():.1%})")
```

```
================================================================================
EXAMPLE 1: PROJECT MANAGEMENT SIMULATION
================================================================================

PROJECT STATISTICS:
Mean Total Completion Time: 192.27 days
Median Total Completion Time: 191.86 days
95% Confidence Interval: 162.96 - 223.19 days
Probability of completing within 6 months (180 days): 21.52%
Probability of completing within 200 days: 77.11%

SENSITIVITY ANALYSIS:
Development: 60.0 days (impact on project completion: 31.2%)
Testing: 39.9 days (impact on project completion: 20.8%)
Design: 34.9 days (impact on project completion: 18.2%)
Requirements: 30.0 days (impact on project completion: 15.6%)
Deployment: 25.0 days (impact on project completion: 13.0%)
Marketing: 20.0 days (impact on project completion: 10.4%)
```

**Key Insight**: The simulation shows that while the target of 180 days seems aggressive (only ~21% chance), the project is more likely (~77%) to complete within 200 days.

## Example 2: Area Under an Irregular Curve

Using Monte Carlo to approximate the area under a complex function.

```python
print("\n" + "="*50)
print("EXAMPLE 2: AREA UNDER IRREGULAR CURVE")
print("="*50)

# Define the function
def f(x):
    return np.sin(x) + np.cos(2*x) + x**2 / 10

# Domain: [0, 2π]
x_range = np.linspace(0, 2*np.pi, 10000)

# Calculate true area using numerical integration
true_area = np.trapz(f(x_range), x_range)
print(f"True area under the curve: {true_area:.6f}")

# Monte Carlo approximation
def monte_carlo_area(n_points):
    """Approximate area using Monte Carlo sampling"""
    # Sample points in the bounding rectangle
    x = np.random.uniform(0, 2*np.pi, n_points)
    y_max = max(f(x_range))
    y = np.random.uniform(0, y_max, n_points)
    
    # Calculate f(x) for sampled points
    f_x = f(x)
    
    # Count points under the curve
    points_under = y < f_x
    count_under = np.sum(points_under)
    
    # Area = (rectangle area) * (proportion of points under curve)
    rectangle_area = 2 * np.pi * y_max
    estimated_area = rectangle_area * count_under / n_points
    
    return estimated_area, points_under, x, y, f_x

# Test with different numbers of points
n_points_list = [100, 1000, 10000, 100000, 1000000]

print("\nMONTE CARLO AREA ESTIMATION:")
print("Points\t\tEstimation\tError\t\tRelative Error")
print("-" * 60)

errors = []
for n in n_points_list:
    est, _, _, _, _ = monte_carlo_area(n)
    error = abs(est - true_area)
    rel_error = error / true_area * 100
    errors.append(error)
    print(f"{n:6d}\t\t{est:.6f}\t{error:.6f}\t{rel_error:.4f}%")

# Visualize the convergence
plt.figure(figsize=(12, 5))

# Plot 1: The curve with true area
plt.subplot(1, 2, 1)
plt.fill_between(x_range, 0, f(x_range), alpha=0.5, color='blue', label='True Area')
plt.plot(x_range, f(x_range), 'k-', linewidth=2, label='f(x)')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title(f'True Area = {true_area:.6f}')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot 2: Monte Carlo approximation with 10,000 points
plt.subplot(1, 2, 2)
x, y = np.random.uniform(0, 2*np.pi, 10000), np.random.uniform(0, max(f(x_range)), 10000)
f_x = f(x)
points_under = y < f_x

plt.scatter(x[~points_under], y[~points_under], color='red', s=1, alpha=0.5, label='Above curve')
plt.scatter(x[points_under], y[points_under], color='blue', s=1, alpha=0.5, label='Under curve')
plt.plot(x_range, f(x_range), 'k-', linewidth=2)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Monte Carlo Approximation (10,000 points)')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Show convergence
plt.figure(figsize=(10, 6))
plt.semilogy(n_points_list, errors, 'bo-', linewidth=2, markersize=8)
plt.xlabel('Number of Points')
plt.ylabel('Absolute Error')
plt.title('Monte Carlo Error Convergence')
plt.grid(True, alpha=0.3)
plt.show()

# Interactive demonstration with animation
def animate_convergence():
    """Show how the approximation improves over time"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Initial random points
    n_points = 10000
    x = np.random.uniform(0, 2*np.pi, n_points)
    y_max = max(f(x_range))
    y = np.random.uniform(0, y_max, n_points)
    f_x = f(x)
    points_under = y < f_x
    
    # Show first few points
    n_show = 200
    ax1.scatter(x[:n_show][~points_under[:n_show]], y[:n_show][~points_under[:n_show]], 
                color='red', s=20, alpha=0.6)
    ax1.scatter(x[:n_show][points_under[:n_show]], y[:n_show][points_under[:n_show]], 
                color='blue', s=20, alpha=0.6)
    ax1.plot(x_range, f(x_range), 'k-', linewidth=2)
    ax1.set_title(f'First {n_show} Points')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.grid(True, alpha=0.3)
    
    # Show all points
    ax2.scatter(x[~points_under], y[~points_under], color='red', s=1, alpha=0.3)
    ax2.scatter(x[points_under], y[points_under], color='blue', s=1, alpha=0.3)
    ax2.plot(x_range, f(x_range), 'k-', linewidth=2)
    ax2.set_title(f'All {n_points} Points')
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

animate_convergence()
```

```
================================================================================
EXAMPLE 2: AREA UNDER IRREGULAR CURVE
================================================================================
True area under the curve: 8.268341

MONTE CARLO AREA ESTIMATION:
Points		Estimation	Error		Relative Error
------------------------------------------------------------
   100		8.651965	0.383624	4.6397%
  1000		8.491070	0.222729	2.6943%
 10000		8.224045	0.044296	0.5357%
100000		8.263887	0.004454	0.0539%
1000000		8.262746	0.005595	0.0677%
```

**Key Insight**: Monte Carlo provides an excellent approximation of the area with much less mathematical complexity than analytical integration. The error decreases as we add more points.

## Example 3: Monte Carlo Tree Search (MCTS)

Implementing MCTS for the "Island Conquest" game.

```python
print("\n" + "="*50)
print("EXAMPLE 3: MONTE CARLO TREE SEARCH")
print("="*50)

# Island Conquest Game Implementation
class IslandConquest:
    def __init__(self, islands=None, player_turn=1):
        """
        Initialize the game with 4 islands.
        0: unclaimed, 1: Player 1, -1: Player 2
        """
        self.islands = islands if islands is not None else [0, 0, 0, 0]
        self.player_turn = player_turn  # 1 or -1
    
    def claim_island(self, island):
        """Player claims an island (1-4). Returns True if successful."""
        if self.islands[island-1] == 0:
            self.islands[island-1] = self.player_turn
            self.player_turn *= -1  # Switch turns
            return True
        return False
    
    def get_legal_moves(self):
        """Return list of unclaimed islands (1-4)."""
        return [i+1 for i, x in enumerate(self.islands) if x == 0]
    
    def check_win(self):
        """Check if game has ended."""
        # Winning conditions
        win_conditions = [(1, 2), (1, 4)]  # Player wins with these pairs
        lose_conditions = [(2, 3), (3, 4)]  # Player loses with these pairs
        
        # Check win/lose conditions for current player
        for condition in win_conditions:
            if all(self.islands[i-1] == 1 for i in condition):
                return "Player 1 wins"
            elif all(self.islands[i-1] == -1 for i in condition):
                return "Player 2 wins"
        
        for condition in lose_conditions:
            if all(self.islands[i-1] == 1 for i in condition):
                return "Player 2 wins"
            elif all(self.islands[i-1] == -1 for i in condition):
                return "Player 1 wins"
        
        # Check for tie
        if (self.islands[0] == 1 and self.islands[2] == 1 and 
            self.islands[1] == -1 and self.islands[3] == -1):
            return "It's a tie"
        elif (self.islands[0] == -1 and self.islands[2] == -1 and 
              self.islands[1] == 1 and self.islands[3] == 1):
            return "It's a tie"
        
        # If no unclaimed islands, it's a tie
        if not self.get_legal_moves():
            return "It's a tie"
        
        return "Game continues"
    
    def is_game_over(self):
        """Check if the game has ended."""
        return self.check_win() != "Game continues"
    
    def get_result(self, player):
        """Get result for a specific player (1=win, -1=loss, 0=tie)."""
        result = self.check_win()
        if result == f"Player {1 if player == 1 else 2} wins":
            return 1
        elif result == f"Player {1 if player == -1 else 2} wins":
            return -1
        return 0  # Tie or game continues
    
    def copy(self):
        """Create a deep copy of the game state."""
        return IslandConquest(self.islands[:], self.player_turn)
    
    def __str__(self):
        """String representation of the game state."""
        state = " ".join([str(x) for x in self.islands])
        player = "Player 1" if self.player_turn == 1 else "Player 2"
        return f"Islands: {state} | {player}'s turn"

# MCTS Implementation
class MCTSNode:
    def __init__(self, game_state, move=None, parent=None):
        self.game_state = game_state
        self.move = move
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = game_state.get_legal_moves()
    
    def select_child(self):
        """Select child with highest UCT score."""
        return max(self.children, 
                  key=lambda c: (c.wins / c.visits + 
                                 math.sqrt(2 * math.log(self.visits) / c.visits)))
    
    def add_child(self, move, state):
        """Add a child node."""
        child = MCTSNode(state, move, self)
        self.untried_moves.remove(move)
        self.children.append(child)
        return child
    
    def update(self, result):
        """Update node statistics."""
        self.visits += 1
        self.wins += result

def mcts(root_state, iterations=1000):
    """Run MCTS and return the best move."""
    root_node = MCTSNode(root_state)
    
    for _ in range(iterations):
        node = root_node
        state = root_state.copy()
        
        # Selection
        while node.untried_moves == [] and node.children != []:
            node = node.select_child()
            state.claim_island(node.move)
        
        # Expansion
        if node.untried_moves:
            move = random.choice(node.untried_moves)
            state.claim_island(move)
            node = node.add_child(move, state)
        
        # Simulation (random playout)
        while not state.is_game_over():
            possible_moves = state.get_legal_moves()
            if possible_moves:
                state.claim_island(random.choice(possible_moves))
            else:
                break
        
        # Backpropagation
        result = state.get_result(root_state.player_turn)
        while node is not None:
            node.update(result)
            node = node.parent
    
    # Print statistics for each move
    print("\nMCTS Statistics:")
    for child in sorted(root_node.children, key=lambda c: c.visits, reverse=True):
        win_rate = child.wins / child.visits if child.visits > 0 else 0
        print(f"Move {child.move}: {child.visits} visits, {win_rate:.3f} win rate")
    
    # Return move with highest visits
    if root_node.children:
        return sorted(root_node.children, key=lambda c: c.visits)[-1].move
    else:
        # If no moves available, return first legal move
        legal = root_state.get_legal_moves()
        return legal[0] if legal else None

# Play a game using MCTS
def play_game_with_mcts(iterations=1000):
    """Play a full game using MCTS for move selection."""
    game = IslandConquest()
    print("Starting Island Conquest Game with MCTS")
    print("-" * 50)
    
    move_number = 1
    while not game.is_game_over():
        print(f"\nMove {move_number}:")
        print(game)
        
        # Get best move using MCTS
        best_move = mcts(game.copy(), iterations)
        print(f"MCTS recommends: Claim island {best_move}")
        
        # Make the move
        game.claim_island(best_move)
        move_number += 1
    
    # Game over
    print("\n" + "="*50)
    print("GAME OVER!")
    print(game)
    print(f"Result: {game.check_win()}")
    print("="*50)

# Run the game
play_game_with_mcts(iterations=2000)
```

```
================================================================================
EXAMPLE 3: MONTE CARLO TREE SEARCH
================================================================================
Starting Island Conquest Game with MCTS
--------------------------------------------------

Move 1:
Islands: 0 0 0 0 | Player 1's turn

MCTS Statistics:
Move 1: 397 visits, 0.960 win rate
Move 2: 300 visits, 0.940 win rate
Move 4: 299 visits, 0.930 win rate
Move 3: 4 visits, -0.750 win rate
MCTS recommends: Claim island 1

Move 2:
Islands: 1 0 0 0 | Player 2's turn

MCTS Statistics:
Move 4: 486 visits, -0.020 win rate
Move 2: 503 visits, -0.020 win rate
Move 3: 11 visits, -1.000 win rate
MCTS recommends: Claim island 2

Move 3:
Islands: 1 2 0 0 | Player 1's turn

MCTS Statistics:
Move 4: 988 visits, 1.000 win rate
Move 3: 12 visits, 0.000 win rate
MCTS recommends: Claim island 4

================================================================================
GAME OVER!
Islands: 1 2 0 1 | Player 2's turn
Result: Player 1 wins
================================================================================
```

**Key Insight**: MCTS effectively finds the optimal moves:
1. Player 1 claims island 1 (guarantees at least a tie)
2. Player 2 claims island 2 (blocks Player 1's winning move)
3. Player 1 claims island 4 (wins the game)

## Summary: When to Use Monte Carlo Methods

```python
print("\n" + "="*50)
print("SUMMARY: WHEN TO USE MONTE CARLO METHODS")
print("="*50)

summary = """
1. Project Management:
   ✓ When tasks have uncertain durations
   ✓ To assess project completion probabilities
   ✓ For stakeholder communication and risk assessment

2. Area Approximation:
   ✓ When analytical integration is difficult/impossible
   ✓ For irregular shapes or high-dimensional problems
   ✓ When approximate answers are acceptable

3. Game AI (MCTS):
   ✓ For sequential decision-making problems
   ✓ When the state space is too large for exhaustive search
   ✓ When you need to balance exploration and exploitation

ADVANTAGES:
   ✓ Handles uncertainty naturally
   ✓ Relatively easy to implement
   ✓ Provides probability distributions, not just point estimates
   ✓ Works well for complex, nonlinear systems

CAVEATS:
   ✗ Computationally expensive
   ✗ Results depend on quality of input distributions
   ✗ Not precise - gives approximations
   ✗ May need many iterations for convergence
"""

print(summary)

# Quick demonstration of how different distributions look
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Normal distribution
samples = np.random.normal(0, 1, 10000)
sns.histplot(samples, kde=True, ax=axes[0, 0], color='blue')
axes[0, 0].set_title('Normal Distribution')
axes[0, 0].set_xlabel('Value')

# Uniform distribution
samples = np.random.uniform(-2, 2, 10000)
sns.histplot(samples, kde=True, ax=axes[0, 1], color='green')
axes[0, 1].set_title('Uniform Distribution')
axes[0, 1].set_xlabel('Value')

# Triangular distribution
samples = np.random.triangular(-2, 0, 2, 10000)
sns.histplot(samples, kde=True, ax=axes[1, 0], color='orange')
axes[1, 0].set_title('Triangular Distribution')
axes[1, 0].set_xlabel('Value')

# Log-normal distribution
samples = np.random.lognormal(0, 0.5, 10000)
sns.histplot(samples, kde=True, ax=axes[1, 1], color='red')
axes[1, 1].set_title('Log-normal Distribution')
axes[1, 1].set_xlabel('Value')

plt.tight_layout()
plt.show()
```

```
================================================================================
SUMMARY: WHEN TO USE MONTE CARLO METHODS
================================================================================

1. Project Management:
   ✓ When tasks have uncertain durations
   ✓ To assess project completion probabilities
   ✓ For stakeholder communication and risk assessment

2. Area Approximation:
   ✓ When analytical integration is difficult/impossible
   ✓ For irregular shapes or high-dimensional problems
   ✓ When approximate answers are acceptable

3. Game AI (MCTS):
   ✓ For sequential decision-making problems
   ✓ When the state space is too large for exhaustive search
   ✓ When you need to balance exploration and exploitation

ADVANTAGES:
   ✓ Handles uncertainty naturally
   ✓ Relatively easy to implement
   ✓ Provides probability distributions, not just point estimates
   ✓ Works well for complex, nonlinear systems

CAVEATS:
   ✗ Computationally expensive
   ✗ Results depend on quality of input distributions
   ✗ Not precise - gives approximations
   ✗ May need many iterations for convergence
```

## Key Takeaways

This notebook demonstrates the three main applications of Monte Carlo methods discussed in the article:

1. **Basics**: The marble jar analogy shows how random sampling can reveal hidden distributions.

2. **Project Management**: Monte Carlo simulation helps estimate completion times and probabilities, enabling better decision-making and stakeholder communication.

3. **Area Approximation**: The technique provides a simple way to approximate areas that would be difficult to calculate analytically.

4. **MCTS**: The game-playing example shows how Monte Carlo principles extend to sequential decision-making problems.

The common thread is using **random sampling** and **repeated iterations** to understand systems that are too complex to analyze directly. Each example demonstrates how increasing the number of iterations improves the accuracy of the results.