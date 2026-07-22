# Monte Carlo Simulation Workbook
## A Practical Guide to Understanding Randomness, Uncertainty, and Probability

---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Jupyter](https://img.shields.io/badge/Jupyter-F37626.svg?&logo=Jupyter&logoColor=white)](https://jupyter.org/)

---

## 📚 Overview

Monte Carlo simulations are a powerful technique for understanding complex systems through random sampling. Instead of solving problems analytically (with pure math), Monte Carlo methods use repeated random sampling to approximate solutions.

### What You'll Learn

- **Core Concepts**: Randomness, probability distributions, law of large numbers
- **8 Progressive Modules** from simple to advanced
- **Real-World Applications**: Finance, physics, engineering, social science, machine learning
- **How Monte Carlo Intersects with Game Theory**: Strategic uncertainty meets random uncertainty
- **Uncertainty Quantification**: Understanding confidence in your estimates
- **Best Practices**: Writing efficient, reproducible, and reliable simulations

### 🎓 Prerequisites

Before starting, you should be familiar with:
- **Basic Python**: Variables, loops, functions, lists
- **NumPy & Matplotlib**: Arrays and basic plotting
- **Statistics**: Mean, variance, standard deviation

### Quick Setup

```bash
pip install numpy matplotlib pandas jupyter scipy tqdm ipywidgets
```

### Verify Your Setup

```python
import numpy as np
import matplotlib.pyplot as plt
import random
import math
from scipy import stats
from tqdm import tqdm
from collections import Counter

print("✅ All imports successful!")
print(f"NumPy version: {np.__version__}")
print(f"Matplotlib version: {plt.matplotlib.__version__}")
```

---

## 📚 Key Terminology

| Term | Definition | Example |
|------|------------|---------|
| **Random Sampling** | Drawing values from a probability distribution | `random.uniform(0,1)` |
| **Law of Large Numbers** | As sample size increases, average converges to expected value | π estimate improves with more darts |
| **Convergence** | The process of approaching a final value | Error decreases as n increases |
| **Variance** | Measure of spread around the mean | Uncertainty in estimates |
| **Confidence Interval** | Range containing true value with certain probability | 95% CI: [3.14, 3.15] |
| **Seed** | Starting point for random number generation | `random.seed(42)` for reproducibility |
| **Bootstrap** | Resampling with replacement to estimate uncertainty | Bootstrap sampling for confidence intervals |
| **Monte Carlo Error** | Error due to finite sampling; ∝ 1/√n | Error halves when samples quadruple |

---

## 🎯 What Is Monte Carlo Simulation?

**The One-Sentence Definition**: Monte Carlo simulation is a computational technique that uses repeated random sampling to estimate numerical results when deterministic solutions are difficult or impossible.

**The Core Insight**: If you can't solve a problem exactly, simulate it many times and let the statistics reveal the answer.

**The Key Idea**: Randomness + Repetition = Understanding

---

## ⚠️ Common Pitfalls & How to Avoid Them

### Pitfall 1: Not Setting a Random Seed
```python
# ❌ BAD: Results not reproducible
import random
print(random.random())  # Different every time

# ✅ GOOD: Reproducible results
random.seed(42)
np.random.seed(42)
print(random.random())  # Always 0.6394267984578837
```

### Pitfall 2: Too Few Simulations
```python
# ❌ BAD: Unreliable results
estimate_pi(100)  # Error ~0.1-0.2

# ✅ GOOD: Reliable results
estimate_pi(100000)  # Error ~0.001-0.005
```

### Pitfall 3: Misunderstanding Convergence
- More samples = better accuracy, but with diminishing returns
- Error ∝ 1/√n (doubling samples reduces error by ~30%)
- 100 samples → error ~0.1; 10,000 samples → error ~0.01

### Pitfall 4: Ignoring Variance
- Always report both the estimate AND the uncertainty
- A mean without variance is incomplete information

### Pitfall 5: Using Loops When Vectorization Works
```python
# ❌ SLOW: Python loop
results = []
for i in range(1000000):
    results.append(random.random())

# ✅ FAST: NumPy vectorization
results = np.random.random(1000000)
```

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

# MODULE 1: Estimating Pi (π)

### 📖 WHAT Is It?

The simplest Monte Carlo simulation: estimating the value of π by throwing darts at a circle inside a square.

**The Setup**:
- Draw a circle of radius 1 inside a square of side length 2
- Randomly throw darts at the square
- Count how many land inside the circle
- The ratio of darts inside the circle to total throws approximates π/4

**The Math**:
- Area of square = 4
- Area of circle = π
- Probability a dart lands in circle = π/4
- Therefore: π ≈ 4 × (darts in circle / total darts)

### 🤔 WHY Does It Matter?

This is the "Hello World" of Monte Carlo methods. It demonstrates:
- How random sampling can approximate deterministic values
- The law of large numbers (more samples = better approximation)
- The concept of convergence
- How to visualize uncertainty

### 🛠️ HOW Does It Work in Code?

```python
import random
import math
import numpy as np
import matplotlib.pyplot as plt

def estimate_pi(num_samples, seed=None):
    """
    Estimate π using Monte Carlo method.
    
    Parameters:
    num_samples: Number of random points to generate
    seed: Random seed for reproducibility
    
    Returns:
    pi_estimate: Estimated value of π
    history: List of running estimates
    points: Array of generated points (for visualization)
    inside: Boolean array of which points are inside circle
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    # Generate random points
    points = np.random.uniform(-1, 1, (num_samples, 2))
    
    # Check if points are inside circle
    inside = points[:,0]**2 + points[:,1]**2 <= 1
    
    # Running estimate of π
    inside_count = np.cumsum(inside)
    history = 4 * inside_count / np.arange(1, num_samples + 1)
    
    pi_estimate = history[-1]
    
    return pi_estimate, history, points, inside

# Run the simulation
num_samples = 100000
pi_estimate, history, points, inside = estimate_pi(num_samples, seed=42)

print(f"Estimated π: {pi_estimate:.6f}")
print(f"Actual π:    {math.pi:.6f}")
print(f"Error:       {abs(pi_estimate - math.pi):.6f}")
print(f"Error %:     {abs(pi_estimate - math.pi) / math.pi * 100:.4f}%")
```

### 🎨 Enhanced Visualization

```python
def visualize_pi_convergence_enhanced(points, inside, history):
    """Enhanced visualization with color-coded points"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Scatter plot with color coding
    ax1.scatter(points[inside, 0], points[inside, 1], 
               c='green', s=5, alpha=0.6, label=f'Inside (π/4)')
    ax1.scatter(points[~inside, 0], points[~inside, 1], 
               c='red', s=5, alpha=0.6, label='Outside')
    
    # Draw circle
    circle = plt.Circle((0, 0), 1, fill=False, edgecolor='blue', linewidth=2)
    ax1.add_patch(circle)
    ax1.set_aspect('equal')
    ax1.set_xlim(-1.1, 1.1)
    ax1.set_ylim(-1.1, 1.1)
    ax1.set_title(f'Monte Carlo π Estimation: n={len(points):,}')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    
    # Convergence plot with confidence bands
    n_points = len(history)
    x_vals = np.arange(1, n_points + 1)
    
    ax2.plot(x_vals, history, 'b-', alpha=0.7, label='Running Estimate')
    ax2.axhline(y=math.pi, color='red', linestyle='--', label='True π', linewidth=2)
    
    # Add ±0.01 error band
    ax2.fill_between(x_vals, 
                     math.pi - 0.01, math.pi + 0.01, 
                     alpha=0.2, color='red', label='±0.01 Error Band')
    
    ax2.set_xlabel('Number of Samples')
    ax2.set_ylabel('π Estimate')
    ax2.set_title(f'Convergence: Final π = {history[-1]:.6f}')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# Visualize results
visualize_pi_convergence_enhanced(points, inside, history)
```

### 📊 Convergence Analysis with Confidence Intervals

```python
def analyze_convergence(sample_sizes, num_trials=100):
    """
    Analyze convergence and compute confidence intervals.
    """
    results = {}
    
    for size in sample_sizes:
        estimates = []
        for _ in range(num_trials):
            pi_est, _, _, _ = estimate_pi(size, seed=None)
            estimates.append(pi_est)
        
        mean_est = np.mean(estimates)
        std_est = np.std(estimates)
        ci_95 = stats.norm.interval(0.95, loc=mean_est, scale=std_est/np.sqrt(num_trials))
        
        results[size] = {
            'mean': mean_est,
            'std': std_est,
            'ci_lower': ci_95[0],
            'ci_upper': ci_95[1],
            'error': abs(mean_est - math.pi)
        }
    
    # Display results
    print("Convergence Analysis with 95% Confidence Intervals")
    print("=" * 70)
    print(f"{'Samples':>10} | {'π Estimate':>12} | {'Error':>12} | {'95% CI':>20}")
    print("-" * 70)
    
    for size, data in results.items():
        ci_str = f"[{data['ci_lower']:.6f}, {data['ci_upper']:.6f}]"
        print(f"{size:>10} | {data['mean']:>12.6f} | {data['error']:>12.6f} | {ci_str:>20}")
    
    return results

# Test different sample sizes
sizes = [10, 100, 1000, 10000, 100000, 1000000]
results = analyze_convergence(sizes)
```

### 🧪 INTERACTIVE EXERCISE: Vary Number of Samples

```python
# Requires ipywidgets
from ipywidgets import interact, widgets

@interact(
    samples=widgets.IntSlider(min=100, max=100000, step=1000, value=10000),
    show_points=widgets.Checkbox(value=True, description='Show Points')
)
def interactive_pi(samples, show_points):
    """Interactive exploration of π estimation"""
    pi_est, hist, pts, inside = estimate_pi(samples, seed=42)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    if show_points:
        ax1.scatter(pts[inside, 0], pts[inside, 1], c='green', s=3, alpha=0.5)
        ax1.scatter(pts[~inside, 0], pts[~inside, 1], c='red', s=3, alpha=0.5)
        circle = plt.Circle((0, 0), 1, fill=False, edgecolor='blue', linewidth=2)
        ax1.add_patch(circle)
        ax1.set_aspect('equal')
        ax1.set_title(f'n={samples:,}, π≈{pi_est:.6f}')
    
    ax2.plot(hist)
    ax2.axhline(y=math.pi, color='r', linestyle='--', label='True π')
    ax2.set_xlabel('Samples')
    ax2.set_ylabel('π Estimate')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    print(f"Estimated π: {pi_est:.6f}")
    print(f"Error: {abs(pi_est - math.pi):.6f}")

# Uncomment to run interactive version
# interactive_pi()
```

---

# MODULE 2: The Birthday Problem

### 📖 WHAT Is It?

How many people do you need in a room before there's a >50% chance that two people share a birthday?

**The Math**:
- Probability no two share a birthday: P(no match) = 365/365 × 364/365 × ... × (365-n+1)/365
- Probability at least one match: P(match) = 1 - P(no match)

**The Surprising Result**: With just 23 people, there's >50% chance of a shared birthday!

### 🤔 WHY Does It Matter?

The Birthday Problem demonstrates:
- How intuition fails us with probability
- How Monte Carlo can verify analytical results
- Applications in cryptography (birthday attack)
- Understanding rare events and their probabilities

### 🛠️ HOW Does It Work in Code?

```python
import random
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

def birthday_simulation(num_people, num_trials=10000, seed=None):
    """
    Simulate the Birthday Problem.
    
    Parameters:
    num_people: Number of people in the room
    num_trials: Number of simulation runs
    seed: Random seed for reproducibility
    
    Returns:
    probability: Probability of at least one shared birthday
    distribution: Distribution of birthday matches
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    matches = 0
    match_counts = []
    
    for _ in range(num_trials):
        # Generate random birthdays (1-365)
        birthdays = np.random.randint(1, 366, num_people)
        
        # Count duplicates
        unique_birthdays = len(set(birthdays))
        match_count = num_people - unique_birthdays
        match_counts.append(match_count)
        
        if match_count > 0:
            matches += 1
    
    return matches / num_trials, match_counts

def theoretical_probability(num_people):
    """Calculate the theoretical probability of a shared birthday"""
    if num_people > 365:
        return 1.0
    
    prob_no_match = 1.0
    for i in range(num_people):
        prob_no_match *= (365 - i) / 365
    
    return 1 - prob_no_match

# Test different group sizes
print("Birthday Problem Analysis")
print("=" * 70)
print(f"{'People':>8} | {'Simulation':>12} | {'Theoretical':>12} | {'Difference':>12}")
print("-" * 70)

for people in [5, 10, 15, 20, 23, 30, 40, 50, 60]:
    sim_prob, _ = birthday_simulation(people, num_trials=10000, seed=42)
    theo_prob = theoretical_probability(people)
    diff = abs(sim_prob - theo_prob)
    print(f"{people:>8} | {sim_prob:>12.4f} | {theo_prob:>12.4f} | {diff:>12.4f}")
```

### 📊 Enhanced Visualization

```python
def visualize_birthday_problem():
    """Enhanced visualization of the Birthday Problem"""
    # Calculate probabilities for group sizes 1-70
    group_sizes = list(range(1, 71))
    sim_probs = []
    match_distributions = []
    
    for n in tqdm(group_sizes, desc="Simulating"):
        prob, matches = birthday_simulation(n, num_trials=5000, seed=42)
        sim_probs.append(prob)
        match_distributions.append(matches)
    
    theo_probs = [theoretical_probability(n) for n in group_sizes]
    
    # Create figure with subplots
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Probability vs group size
    axes[0].plot(group_sizes, sim_probs, 'bo-', label='Simulation', alpha=0.7, linewidth=2)
    axes[0].plot(group_sizes, theo_probs, 'r--', label='Theoretical', alpha=0.7, linewidth=2)
    
    # Mark the 50% threshold
    axes[0].axhline(y=0.5, color='gray', linestyle=':', alpha=0.7, linewidth=2)
    axes[0].axvline(x=23, color='gray', linestyle=':', alpha=0.7, linewidth=2)
    axes[0].annotate('50% threshold\n(23 people)', xy=(23, 0.5), xytext=(30, 0.6),
                     arrowprops=dict(arrowstyle='->', color='gray'))
    
    axes[0].set_xlabel('Number of People in Room')
    axes[0].set_ylabel('Probability of Shared Birthday')
    axes[0].set_title('Birthday Problem: Simulation vs Theory')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Plot 2: Distribution of matches for different group sizes
    group_sizes_to_show = [10, 23, 40, 60]
    colors = ['blue', 'green', 'orange', 'red']
    
    for size, color in zip(group_sizes_to_show, colors):
        idx = size - 1
        counts = Counter(match_distributions[idx])
        x_vals = sorted(counts.keys())
        y_vals = [counts[x] / 5000 * 100 for x in x_vals]  # Convert to percentage
        
        axes[1].plot(x_vals, y_vals, 'o-', color=color, label=f'n={size}', alpha=0.7, linewidth=2)
    
    axes[1].set_xlabel('Number of Matching Pairs')
    axes[1].set_ylabel('Frequency (%)')
    axes[1].set_title('Distribution of Birthday Matches')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Summary statistics
    print("\n📊 Key Insights:")
    print(f"• At 23 people: {sim_probs[22]:.1%} chance of shared birthday")
    print(f"• At 30 people: {sim_probs[29]:.1%} chance of shared birthday")
    print(f"• At 50 people: {sim_probs[49]:.1%} chance of shared birthday")
    print(f"• At 60 people: {sim_probs[59]:.1%} chance of shared birthday")

# Run the visualization
visualize_birthday_problem()
```

### 🧪 EXERCISE: Find Your Own Birthday

```python
def find_my_birthday_match(my_birthday, num_people, num_trials=10000):
    """Simulate finding someone with your specific birthday"""
    matches = 0
    
    for _ in range(num_trials):
        birthdays = np.random.randint(1, 366, num_people)
        if my_birthday in birthdays:
            matches += 1
    
    return matches / num_trials

# Test with different birthdays
print("\n🎂 Probability of Sharing YOUR Birthday")
print("=" * 50)

my_bday = 180  # July 1st (approximate)
for people in [23, 50, 100, 183, 365]:
    prob = find_my_birthday_match(my_bday, people)
    expected = 1 - (364/365)**people  # Expected for a specific date
    print(f"With {people:>3} people: {prob:.2%} (expected: {expected:.2%})")
```

---

# MODULE 3: The Monty Hall Problem

### 📖 WHAT Is It?

A classic probability puzzle based on a game show:
1. There are 3 doors: behind one is a car, behind two are goats
2. You pick a door
3. The host (who knows what's behind each door) opens a different door revealing a goat
4. You're offered the chance to switch to the remaining door

**The Counter-Intuitive Result**: You should **always switch**! Switching gives you a 2/3 chance of winning, while staying gives only 1/3.

### 🤔 WHY Does It Matter?

The Monty Hall Problem demonstrates:
- How intuition fails us with conditional probability
- The importance of understanding information (the host knows)
- How Monte Carlo can verify counter-intuitive results
- Decision-making under uncertainty
- Bayesian updating of probabilities

### 🛠️ HOW Does It Work in Code?

```python
import random
import numpy as np
import matplotlib.pyplot as plt

def monty_hall_simulation(strategy, num_trials=10000, seed=None):
    """
    Simulate the Monty Hall Problem.
    
    Parameters:
    strategy: 'stay' or 'switch'
    num_trials: Number of simulation runs
    seed: Random seed for reproducibility
    
    Returns:
    win_rate: Probability of winning
    outcome_history: List of outcomes for convergence analysis
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    wins = 0
    outcome_history = []
    
    for trial in range(num_trials):
        # Place the car behind a random door
        car_door = random.randint(0, 2)
        
        # Player picks a random door
        player_pick = random.randint(0, 2)
        
        # Host opens a door (not car, not player's pick)
        available_doors = [i for i in range(3) if i != car_door and i != player_pick]
        host_opens = random.choice(available_doors)
        
        # Player's final decision
        if strategy == 'stay':
            final_pick = player_pick
        else:  # switch
            remaining_doors = [i for i in range(3) if i != player_pick and i != host_opens]
            final_pick = remaining_doors[0]
        
        # Check if player won
        won = (final_pick == car_door)
        if won:
            wins += 1
        
        outcome_history.append(wins / (trial + 1))
    
    return wins / num_trials, outcome_history

# Test both strategies
num_trials = 10000
stay_rate, stay_history = monty_hall_simulation('stay', num_trials, seed=42)
switch_rate, switch_history = monty_hall_simulation('switch', num_trials, seed=42)

print(f"Monty Hall Simulation ({num_trials:,} trials)")
print("=" * 50)
print(f"Stay strategy win rate:   {stay_rate:.2%}")
print(f"Switch strategy win rate: {switch_rate:.2%}")
print(f"Difference:               {switch_rate - stay_rate:.2%}")
print("\n🎯 Conclusion: You should ALWAYS switch!")
```

### 📊 Enhanced Visualization

```python
def visualize_monty_hall(stay_history, switch_history):
    """Enhanced visualization of Monty Hall results"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Convergence of win rates
    x_vals = np.arange(1, len(stay_history) + 1)
    
    axes[0].plot(x_vals, stay_history, 'r-', alpha=0.7, label='Stay', linewidth=2)
    axes[0].plot(x_vals, switch_history, 'g-', alpha=0.7, label='Switch', linewidth=2)
    axes[0].axhline(y=1/3, color='red', linestyle=':', alpha=0.5, label='Expected (Stay)')
    axes[0].axhline(y=2/3, color='green', linestyle=':', alpha=0.5, label='Expected (Switch)')
    
    axes[0].set_xlabel('Number of Trials')
    axes[0].set_ylabel('Win Rate')
    axes[0].set_title('Convergence of Win Rates')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim(0, 1)
    
    # Plot 2: Bar chart comparison
    strategies = ['Stay', 'Switch']
    win_rates = [stay_history[-1], switch_history[-1]]
    bars = axes[1].bar(strategies, win_rates, color=['red', 'green'], alpha=0.7)
    
    # Add value labels on bars
    for bar, rate in zip(bars, win_rates):
        height = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{rate:.1%}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # Add expected values
    axes[1].axhline(y=1/3, color='red', linestyle='--', alpha=0.5, label='Expected (1/3)')
    axes[1].axhline(y=2/3, color='green', linestyle='--', alpha=0.5, label='Expected (2/3)')
    
    axes[1].set_ylim(0, 1)
    axes[1].set_ylabel('Win Rate')
    axes[1].set_title('Final Win Rates')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.show()
    
    # Explanation
    print("\n📖 Why Switching Works:")
    print("=" * 50)
    print("Initial choice: 1/3 chance of car, 2/3 chance of goat")
    print("Host ALWAYS reveals a goat (this is the key!)")
    print("Switching wins if initial choice was a goat (2/3 probability)")
    print("Staying wins if initial choice was a car (1/3 probability)")
    print("\nThe host's action provides information that changes the probability!")

# Visualize
visualize_monty_hall(stay_history, switch_history)
```

### 🧪 EXERCISE: Try Different Scenarios

```python
def monty_hall_variations(num_doors, num_trials=10000):
    """
    Test Monty Hall with different numbers of doors.
    """
    stay_wins = 0
    switch_wins = 0
    
    for _ in range(num_trials):
        # Place the car
        car_door = random.randint(0, num_doors - 1)
        
        # Player picks
        player_pick = random.randint(0, num_doors - 1)
        
        # Host opens (num_doors - 2) doors revealing goats
        available_doors = [i for i in range(num_doors) if i != car_door and i != player_pick]
        host_opens = random.sample(available_doors, num_doors - 2)
        
        # Stay strategy
        if player_pick == car_door:
            stay_wins += 1
        
        # Switch strategy (choose a door not opened by host)
        remaining_doors = [i for i in range(num_doors) if i != player_pick and i not in host_opens]
        if remaining_doors:  # Should always have 1 door
            final_pick = remaining_doors[0]
            if final_pick == car_door:
                switch_wins += 1
    
    stay_rate = stay_wins / num_trials
    switch_rate = switch_wins / num_trials
    
    return stay_rate, switch_rate

# Test with different numbers of doors
print("🏆 Monty Hall Variations")
print("=" * 60)
print(f"{'Doors':>6} | {'Stay':>10} | {'Switch':>10} | {'Advantage':>12}")
print("-" * 60)

for doors in [3, 5, 10, 20, 50]:
    stay, switch = monty_hall_variations(doors, num_trials=10000)
    advantage = switch - stay
    print(f"{doors:>6} | {stay:>9.1%} | {switch:>9.1%} | {advantage:>11.1%}")

print("\n📊 Pattern: More doors = Greater advantage for switching!")
```

---

# MODULE 4: Stock Market Simulation

### 📖 WHAT Is It?

Simulating stock price movements using Geometric Brownian Motion—a model widely used in finance.

**The Model**:
- Stock prices follow a random walk with drift
- Daily returns are normally distributed
- Price = Previous Price × exp((μ - σ²/2) × dt + σ × √dt × Z)
- Where Z is a random normal variable

### 🤔 WHY Does It Matter?

Stock market simulation demonstrates:
- How random processes create complex patterns
- Risk and uncertainty in finance
- Portfolio management and risk assessment
- Option pricing (Black-Scholes model)
- Value at Risk (VaR) calculations

### 🛠️ HOW Does It Work in Code?

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def simulate_stock_price(S0, mu, sigma, days, num_simulations=100, seed=None):
    """
    Simulate stock prices using Geometric Brownian Motion.
    
    Parameters:
    S0: Initial price
    mu: Expected return (drift)
    sigma: Volatility
    days: Number of days to simulate
    num_simulations: Number of paths to generate
    seed: Random seed for reproducibility
    
    Returns:
    prices: Array of simulated prices
    """
    if seed is not None:
        np.random.seed(seed)
    
    dt = 1/252  # Daily time step (252 trading days per year)
    
    # Generate random returns
    returns = np.random.normal(
        (mu - 0.5 * sigma**2) * dt,
        sigma * np.sqrt(dt),
        (num_simulations, days)
    )
    
    # Calculate cumulative returns and prices
    cumulative_returns = np.cumsum(returns, axis=1)
    prices = S0 * np.exp(cumulative_returns)
    
    return prices

def analyze_simulation(prices, S0):
    """
    Comprehensive analysis of simulated stock prices.
    """
    # Calculate returns
    returns = np.diff(prices, axis=1) / prices[:, :-1]
    
    # Basic statistics
    final_prices = prices[:, -1]
    mean_final = np.mean(final_prices)
    median_final = np.median(final_prices)
    std_final = np.std(final_prices)
    
    # Risk metrics
    # Annualized return and volatility
    mean_return = np.mean(returns) * 252
    volatility = np.std(returns) * np.sqrt(252)
    sharpe = mean_return / volatility if volatility > 0 else 0
    
    # Maximum drawdown
    running_max = np.maximum.accumulate(prices, axis=1)
    drawdown = (prices - running_max) / running_max
    max_drawdown = np.min(drawdown)
    
    # Value at Risk (VaR)
    var_95 = np.percentile(final_prices, 5)
    var_95_return = np.percentile(returns.flatten(), 5)
    
    # Confidence interval for final price
    ci_lower, ci_upper = stats.norm.interval(0.95, loc=mean_final, scale=std_final/np.sqrt(len(final_prices)))
    
    results = {
        'mean_final': mean_final,
        'median_final': median_final,
        'std_final': std_final,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'mean_return': mean_return,
        'volatility': volatility,
        'sharpe_ratio': sharpe,
        'max_drawdown': max_drawdown,
        'var_95': var_95,
        'var_95_return': var_95_return,
        'prob_loss': (final_prices < S0).mean(),
        'prob_gain_20': (final_prices > S0 * 1.2).mean()
    }
    
    return results

# Simulate a stock
S0 = 100          # Starting price
mu = 0.10         # 10% expected return
sigma = 0.25      # 25% volatility
days = 252        # One year
num_simulations = 1000

prices = simulate_stock_price(S0, mu, sigma, days, num_simulations, seed=42)
results = analyze_simulation(prices, S0)

print(f"📈 Stock Price Simulation")
print("=" * 60)
print(f"Initial Price: ${S0:.2f}")
print(f"Expected Return: {mu:.1%}")
print(f"Volatility: {sigma:.1%}")
print(f"Simulations: {num_simulations:,}")
print(f"Days: {days}")
print("\n📊 Results:")
print(f"Mean Final Price: ${results['mean_final']:.2f}")
print(f"Median Final Price: ${results['median_final']:.2f}")
print(f"Std Dev Final Price: ${results['std_final']:.2f}")
print(f"95% CI Final Price: [${results['ci_lower']:.2f}, ${results['ci_upper']:.2f}]")
print(f"Probability of Loss: {results['prob_loss']:.1%}")
print(f"Probability of 20% Gain: {results['prob_gain_20']:.1%}")
print(f"Annualized Return: {results['mean_return']:.1%}")
print(f"Volatility (Annual): {results['volatility']:.1%}")
print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
print(f"Max Drawdown: {results['max_drawdown']:.1%}")
print(f"VaR (95%): ${results['var_95']:.2f} (loss of ${S0 - results['var_95']:.2f})")
```

### 📊 Enhanced Visualization

```python
def visualize_stock_simulation(prices, S0, results):
    """Enhanced visualization of stock simulation"""
    num_simulations, days = prices.shape
    final_prices = prices[:, -1]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # Plot 1: Sample paths
    num_to_plot = min(50, num_simulations)
    for i in range(num_to_plot):
        axes[0, 0].plot(prices[i], alpha=0.3, color='blue', linewidth=0.5)
    
    # Average