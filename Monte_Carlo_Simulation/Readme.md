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
- **6 Progressive Modules** from simple to advanced
- **Real-World Applications**: Finance, physics, engineering, social science
- **How Monte Carlo Intersects with Game Theory**: Strategic uncertainty meets random uncertainty

---

## 🎯 What Is Monte Carlo Simulation?

**The One-Sentence Definition**: Monte Carlo simulation is a computational technique that uses repeated random sampling to estimate numerical results when deterministic solutions are difficult or impossible.

**The Core Insight**: If you can't solve a problem exactly, simulate it many times and let the statistics reveal the answer.

**The Key Idea**: Randomness + Repetition = Understanding

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

## MODULE 1: Estimating Pi (π)

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

### 🛠️ HOW Does It Work in Code?

```python
import random
import math
import matplotlib.pyplot as plt

def estimate_pi(num_samples):
    """
    Estimate π using Monte Carlo method.
    
    Parameters:
    num_samples: Number of random points to generate
    
    Returns:
    pi_estimate: Estimated value of π
    history: List of running estimates
    """
    inside_circle = 0
    history = []
    
    for i in range(1, num_samples + 1):
        # Generate random point in [-1, 1] x [-1, 1]
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        
        # Check if point is inside circle (x² + y² <= 1)
        if x*x + y*y <= 1:
            inside_circle += 1
        
        # Running estimate of π
        pi_estimate = 4 * (inside_circle / i)
        history.append(pi_estimate)
    
    return pi_estimate, history

# Run the simulation
num_samples = 100000
pi_estimate, history = estimate_pi(num_samples)

print(f"Estimated π: {pi_estimate:.6f}")
print(f"Actual π:    {math.pi:.6f}")
print(f"Error:       {abs(pi_estimate - math.pi):.6f}")
```

### 📊 Visualization

```python
# Plot convergence
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Convergence over time
ax1.plot(history)
ax1.axhline(y=math.pi, color='r', linestyle='--', label='True π')
ax1.set_xlabel('Number of Samples')
ax1.set_ylabel('π Estimate')
ax1.set_title('Convergence of π Estimate')
ax1.legend()
ax1.grid(True)

# Plot 2: Error over time
error = [abs(h - math.pi) for h in history]
ax2.plot(error)
ax2.set_xlabel('Number of Samples')
ax2.set_ylabel('Error')
ax2.set_title('Convergence Error')
ax2.set_yscale('log')  # Log scale shows convergence rate
ax2.grid(True)

plt.tight_layout()
plt.show()
```

### 🧪 EXERCISE: Vary Number of Samples

```python
def test_convergence(sample_sizes):
    """Test how quickly π converges with different sample sizes"""
    results = {}
    
    for size in sample_sizes:
        estimate, _ = estimate_pi(size)
        error = abs(estimate - math.pi)
        results[size] = {'estimate': estimate, 'error': error}
    
    print("Convergence Analysis")
    print("=" * 50)
    print(f"{'Samples':>10} | {'π Estimate':>12} | {'Error':>12}")
    print("-" * 50)
    for size, data in results.items():
        print(f"{size:>10} | {data['estimate']:>12.6f} | {data['error']:>12.6f}")
    
    return results

# Test different sample sizes
sizes = [10, 100, 1000, 10000, 100000, 1000000]
test_convergence(sizes)
```

---

## MODULE 2: The Birthday Problem

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
- Understanding rare events

### 🛠️ HOW Does It Work in Code?

```python
import random
from collections import Counter

def birthday_simulation(num_people, num_trials=10000):
    """
    Simulate the Birthday Problem.
    
    Parameters:
    num_people: Number of people in the room
    num_trials: Number of simulation runs
    
    Returns:
    probability: Probability of at least one shared birthday
    """
    matches = 0
    
    for _ in range(num_trials):
        # Generate random birthdays
        birthdays = [random.randint(1, 365) for _ in range(num_people)]
        
        # Check for duplicates
        if len(set(birthdays)) < num_people:
            matches += 1
    
    return matches / num_trials

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
print("=" * 50)
print(f"{'People':>8} | {'Simulation':>12} | {'Theoretical':>12} | {'Difference':>12}")
print("-" * 50)

for people in [5, 10, 15, 20, 23, 30, 40, 50]:
    sim_prob = birthday_simulation(people)
    theo_prob = theoretical_probability(people)
    diff = abs(sim_prob - theo_prob)
    print(f"{people:>8} | {sim_prob:>12.4f} | {theo_prob:>12.4f} | {diff:>12.4f}")
```

### 📊 Visualization

```python
# Calculate probabilities for group sizes 1-60
group_sizes = list(range(1, 61))
sim_probs = [birthday_simulation(n, 5000) for n in group_sizes]
theo_probs = [theoretical_probability(n) for n in group_sizes]

# Plot
plt.figure(figsize=(10, 6))
plt.plot(group_sizes, sim_probs, 'bo-', label='Simulation', alpha=0.7)
plt.plot(group_sizes, theo_probs, 'r--', label='Theoretical', alpha=0.7)

# Mark the 50% threshold
plt.axhline(y=0.5, color='gray', linestyle=':', alpha=0.5)
plt.axvline(x=23, color='gray', linestyle=':', alpha=0.5)

plt.xlabel('Number of People')
plt.ylabel('Probability of Shared Birthday')
plt.title('Birthday Problem: Simulation vs Theory')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print(f"Simulated 50% threshold: {next(i for i, p in enumerate(sim_probs) if p >= 0.5)} people")
print(f"Theoretical 50% threshold: 23 people")
```

### 🧪 EXERCISE: Find Your Own Birthday

```python
def find_my_birthday_match(my_birthday, num_people):
    """Simulate finding someone with your specific birthday"""
    matches = 0
    trials = 10000
    
    for _ in range(trials):
        birthdays = [random.randint(1, 365) for _ in range(num_people)]
        if my_birthday in birthdays:
            matches += 1
    
    return matches / trials

# Test with your birthday (1-365)
my_bday = 180  # July 1st (approximate)
print(f"\nProbability of sharing YOUR birthday with {25} people: {find_my_birthday_match(my_bday, 25):.4f}")
```

---

## MODULE 3: The Monty Hall Problem

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

### 🛠️ HOW Does It Work in Code?

```python
import random

def monty_hall_simulation(strategy, num_trials=10000):
    """
    Simulate the Monty Hall Problem.
    
    Parameters:
    strategy: 'stay' or 'switch'
    num_trials: Number of simulation runs
    
    Returns:
    win_rate: Probability of winning
    """
    wins = 0
    
    for _ in range(num_trials):
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
            final_pick = [i for i in range(3) if i != player_pick and i != host_opens][0]
        
        # Check if player won
        if final_pick == car_door:
            wins += 1
    
    return wins / num_trials

# Test both strategies
num_trials = 10000
stay_rate = monty_hall_simulation('stay', num_trials)
switch_rate = monty_hall_simulation('switch', num_trials)

print(f"Monty Hall Simulation ({num_trials:,} trials)")
print("=" * 40)
print(f"Stay strategy win rate:   {stay_rate:.2%}")
print(f"Switch strategy win rate: {switch_rate:.2%}")
print(f"Difference:               {switch_rate - stay_rate:.2%}")
print("\nConclusion: You should ALWAYS switch!")
```

### 📊 Visualization

```python
# Visualize the difference
strategies = ['Stay', 'Switch']
win_rates = [stay_rate, switch_rate]

plt.figure(figsize=(8, 6))
bars = plt.bar(strategies, win_rates, color=['red', 'green'])
plt.ylim(0, 1)

# Add value labels on bars
for bar, rate in zip(bars, win_rates):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.02,
             f'{rate:.1%}', ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.ylabel('Win Rate')
plt.title('Monty Hall: Stay vs Switch Strategy')
plt.grid(True, alpha=0.3, axis='y')
plt.show()

# Explanation
print("\nWhy Switching Works:")
print("=" * 40)
print("Initial choice: 1/3 chance of car, 2/3 chance of goat")
print("Host ALWAYS reveals a goat")
print("Switching wins if initial choice was a goat (2/3 probability)")
print("Staying wins if initial choice was a car (1/3 probability)")
```

### 🧪 EXERCISE: Try Different Scenarios

```python
def monty_hall_variations(num_doors, num_trials=10000):
    """
    Test Monty Hall with different numbers of doors.
    """
    stay_rate = 0
    switch_rate = 0
    
    for _ in range(num_trials):
        # Place the car
        car_door = random.randint(0, num_doors - 1)
        
        # Player picks
        player_pick = random.randint(0, num_doors - 1)
        
        # Host opens (num_doors - 2) doors revealing goats
        available_doors = [i for i in range(num_doors) if i != car_door and i != player_pick]
        host_opens = random.sample(available_doors, num_doors - 2)
        
        # Player's final decision
        # Stay
        if player_pick == car_door:
            stay_rate += 1
        
        # Switch (choose a different door not opened by host)
        remaining_doors = [i for i in range(num_doors) if i != player_pick and i not in host_opens]
        final_pick = remaining_doors[0]  # Only one door remains
        if final_pick == car_door:
            switch_rate += 1
    
    stay_rate /= num_trials
    switch_rate /= num_trials
    
    return stay_rate, switch_rate

# Test with different numbers of doors
print("Monty Hall Variations")
print("=" * 50)
for doors in [3, 5, 10, 20]:
    stay, switch = monty_hall_variations(doors)
    print(f"{doors:>2} doors: Stay: {stay:.1%}, Switch: {switch:.1%}, Advantage: {switch - stay:.1%}")
```

---

## MODULE 4: Stock Market Simulation

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

### 🛠️ HOW Does It Work in Code?

```python
import numpy as np
import pandas as pd

def simulate_stock_price(S0, mu, sigma, days, num_simulations=100):
    """
    Simulate stock prices using Geometric Brownian Motion.
    
    Parameters:
    S0: Initial price
    mu: Expected return (drift)
    sigma: Volatility
    days: Number of days to simulate
    num_simulations: Number of paths to generate
    
    Returns:
    prices: Array of simulated prices
    """
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

# Simulate a stock
S0 = 100          # Starting price
mu = 0.10         # 10% expected return
sigma = 0.25      # 25% volatility
days = 252        # One year
num_simulations = 1000

prices = simulate_stock_price(S0, mu, sigma, days, num_simulations)

# Calculate statistics
final_prices = prices[:, -1]
mean_final = np.mean(final_prices)
median_final = np.median(final_prices)
std_final = np.std(final_prices)

print(f"Stock Price Simulation")
print("=" * 50)
print(f"Initial Price: ${S0:.2f}")
print(f"Expected Return: {mu:.1%}")
print(f"Volatility: {sigma:.1%}")
print(f"Simulations: {num_simulations:,}")
print(f"Days: {days}")
print("\nResults:")
print(f"Mean Final Price: ${mean_final:.2f}")
print(f"Median Final Price: ${median_final:.2f}")
print(f"Std Dev Final Price: ${std_final:.2f}")
print(f"Probability of Loss: {(final_prices < S0).mean():.1%}")
print(f"Best Case: ${final_prices.max():.2f}")
print(f"Worst Case: ${final_prices.min():.2f}")
```

### 📊 Visualization

```python
# Plot sample paths
plt.figure(figsize=(12, 6))

# Plot a subset of paths
num_to_plot = 50
for i in range(num_to_plot):
    plt.plot(prices[i], alpha=0.3, color='blue', linewidth=0.5)

# Highlight the average path
avg_path = np.mean(prices, axis=0)
plt.plot(avg_path, color='red', linewidth=2, label='Average Path')

# Add confidence intervals
lower_bound = np.percentile(prices, 5, axis=0)
upper_bound = np.percentile(prices, 95, axis=0)
plt.fill_between(range(days), lower_bound, upper_bound, alpha=0.2, color='blue', label='90% Confidence Interval')

plt.xlabel('Trading Days')
plt.ylabel('Stock Price ($)')
plt.title('Stock Price Simulation (1000 Paths)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Final price distribution
plt.figure(figsize=(10, 6))
plt.hist(final_prices, bins=50, alpha=0.7, color='blue', density=True)
plt.axvline(S0, color='red', linestyle='--', label=f'Initial Price: ${S0:.2f}')
plt.axvline(mean_final, color='green', linestyle='--', label=f'Mean Final: ${mean_final:.2f}')
plt.xlabel('Final Price ($)')
plt.ylabel('Density')
plt.title('Distribution of Final Stock Prices')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

### 🧪 EXERCISE: Portfolio Simulation

```python
def simulate_portfolio(weights, mu, sigma, days, num_simulations=1000):
    """
    Simulate a portfolio of multiple assets.
    
    Parameters:
    weights: List of asset weights (sums to 1)
    mu: List of expected returns
    sigma: List of volatilities
    days: Number of days to simulate
    
    Returns:
    portfolio_returns: Array of total portfolio returns
    """
    num_assets = len(weights)
    dt = 1/252
    
    # Generate correlated returns
    # (simplified: independent assets for now)
    total_returns = np.zeros((num_simulations, days))
    
    for i in range(num_assets):
        returns = np.random.normal(
            (mu[i] - 0.5 * sigma[i]**2) * dt,
            sigma[i] * np.sqrt(dt),
            (num_simulations, days)
        )
        asset_returns = np.cumsum(returns, axis=1)
        total_returns += weights[i] * asset_returns
    
    # Calculate final prices
    S0 = 100
    portfolio_prices = S0 * np.exp(total_returns)
    
    return portfolio_prices

# Define a portfolio
weights = [0.4, 0.3, 0.3]  # 40% stocks, 30% bonds, 30% commodities
mu = [0.12, 0.05, 0.08]     # Expected returns
sigma = [0.25, 0.10, 0.20]  # Volatilities

portfolio_prices = simulate_portfolio(weights, mu, sigma, days=252)

print("Portfolio Simulation Results")
print("=" * 50)
print(f"Portfolio Weights: {weights}")
print(f"Expected Returns: {[f'{m:.1%}' for m in mu]}")
print(f"Volatilities: {[f'{s:.1%}' for s in sigma]}")
print(f"Initial Value: $100")
print(f"Mean Final Value: ${np.mean(portfolio_prices[:, -1]):.2f}")
print(f"Value at Risk (95%): ${np.percentile(portfolio_prices[:, -1], 5):.2f}")
print(f"Max Loss: ${100 - np.min(portfolio_prices[:, -1]):.2f} ({- (np.min(portfolio_prices[:, -1])/100 - 1):.1%})")
```

---

## MODULE 5: Monte Carlo Integration

### 📖 WHAT Is It?

Using random sampling to calculate the area under a curve (definite integrals) when analytical solutions are difficult or impossible.

**The Method**:
1. Generate random points in a bounding rectangle
2. Count how many fall under the curve
3. Area ≈ (points under curve / total points) × area of bounding rectangle

### 🤔 WHY Does It Matter?

Monte Carlo Integration demonstrates:
- How to solve impossible integrals
- High-dimensional integration (curse of dimensionality)
- Applications in physics, engineering, and finance
- Connection to probability and statistics

### 🛠️ HOW Does It Work in Code?

```python
def monte_carlo_integrate(f, a, b, num_samples=10000):
    """
    Integrate function f(x) from a to b using Monte Carlo.
    
    Parameters:
    f: Function to integrate
    a, b: Integration bounds
    num_samples: Number of random samples
    
    Returns:
    integral: Estimated integral value
    """
    # Find maximum value of f in [a, b]
    x_vals = np.linspace(a, b, 1000)
    y_vals = f(x_vals)
    max_y = max(y_vals)
    
    # Generate random points
    x_random = np.random.uniform(a, b, num_samples)
    y_random = np.random.uniform(0, max_y, num_samples)
    
    # Count points under the curve
    under_curve = y_random <= f(x_random)
    points_under = np.sum(under_curve)
    
    # Calculate area
    rectangle_area = (b - a) * max_y
    integral = (points_under / num_samples) * rectangle_area
    
    return integral, x_random, y_random, under_curve

# Define some functions to integrate
def f1(x):
    return x**2

def f2(x):
    return np.sin(x)

def f3(x):
    return np.exp(-x**2/2)  # Gaussian

# Integrate f1 from 0 to 1 (analytical: 1/3 ≈ 0.3333)
integral, x, y, under = monte_carlo_integrate(f1, 0, 1)

print(f"Monte Carlo Integration")
print("=" * 50)
print(f"Integral of x² from 0 to 1")
print(f"Monte Carlo estimate: {integral:.6f}")
print(f"Analytical answer:     0.333333")
print(f"Error: {abs(integral - 1/3):.6f}")
```

### 📊 Visualization

```python
def visualize_integration(f, a, b, num_samples=1000):
    """Visualize Monte Carlo integration"""
    integral, x_random, y_random, under = monte_carlo_integrate(f, a, b, num_samples)
    
    # Create smooth curve
    x_plot = np.linspace(a, b, 1000)
    y_plot = f(x_plot)
    
    # Find max y for rectangle
    max_y = max(y_plot)
    
    plt.figure(figsize=(12, 6))
    
    # Plot the function
    plt.plot(x_plot, y_plot, 'b-', linewidth=2, label='f(x)')
    
    # Plot random points
    plt.scatter(x_random[under], y_random[under], 
               color='green', s=10, alpha=0.5, label='Under curve')
    plt.scatter(x_random[~under], y_random[~under], 
               color='red', s=10, alpha=0.5, label='Above curve')
    
    # Draw the bounding rectangle
    plt.axhline(y=max_y, color='gray', linestyle='--', alpha=0.5)
    plt.axvline(x=a, color='gray', linestyle='--', alpha=0.5)
    plt.axvline(x=b, color='gray', linestyle='--', alpha=0.5)
    
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title(f'Monte Carlo Integration (n={num_samples})')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    
    print(f"Estimated area: {integral:.6f}")
    print(f"Points under curve: {sum(under)}/{num_samples}")
    print(f"Rectangle area: {(b-a)*max_y:.6f}")

# Visualize different functions
print("Visualizing f1(x) = x²")
visualize_integration(f1, 0, 1, 500)

print("\nVisualizing f2(x) = sin(x)")
visualize_integration(f2, 0, np.pi, 500)

print("\nVisualizing f3(x) = exp(-x²/2)")
visualize_integration(f3, -3, 3, 500)
```

### 🧪 EXERCISE: Integration Accuracy

```python
def test_integration_accuracy(f, a, b, true_value):
    """Test how integration accuracy improves with more samples"""
    sample_sizes = [10, 100, 1000, 10000, 100000]
    estimates = []
    errors = []
    
    for n in sample_sizes:
        integral, _, _, _ = monte_carlo_integrate(f, a, b, n)
        estimates.append(integral)
        errors.append(abs(integral - true_value))
    
    print(f"Integration Accuracy Analysis")
    print("=" * 50)
    print(f"Function: {f.__name__}, Interval: [{a}, {b}]")
    print(f"True value: {true_value:.6f}")
    print("\n" + "Samples".center(10) + "|" + "Estimate".center(15) + "|" + "Error".center(15))
    print("-" * 42)
    for n, est, err in zip(sample_sizes, estimates, errors):
        print(f"{n:>8} | {est:>14.6f} | {err:>14.6f}")
    
    # Plot convergence
    plt.figure(figsize=(10, 6))
    plt.loglog(sample_sizes, errors, 'bo-')
    plt.xlabel('Number of Samples')
    plt.ylabel('Error')
    plt.title('Monte Carlo Integration Convergence')
    plt.grid(True, alpha=0.3)
    plt.show()
    
    return estimates, errors

# Test integration accuracy
test_integration_accuracy(f1, 0, 1, 1/3)
```

---

## MODULE 6: Game Theory + Monte Carlo

### 📖 WHAT Is It?

Combining game theory and Monte Carlo simulation to analyze strategic situations with random uncertainty.

**The Intersection**:
- **Game Theory**: Provides the strategic framework (players, strategies, payoffs)
- **Monte Carlo**: Handles random uncertainty (unknown events, stochastic outcomes)
- **Together**: Analyzing real-world strategic situations

### 🤔 WHY Does It Matter?

This intersection is crucial for understanding:
- Strategic uncertainty (what will others do?)
- Random uncertainty (what random events will occur?)
- Complex real-world systems (financial markets, warfare, politics)
- How to make decisions when both types of uncertainty exist

### 🛠️ HOW Does It Work in Code?

```python
import random
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

class StrategicGameWithMonteCarlo:
    """
    A game that combines strategic decision-making with random uncertainty.
    """
    
    def __init__(self, num_players, strategies, payoff_matrix, random_events):
        """
        Initialize the game.
        
        Parameters:
        num_players: Number of players
        strategies: List of available strategies for each player
        payoff_matrix: Payoff for each strategy combination
        random_events: List of random events that can occur
        """
        self.num_players = num_players
        self.strategies = strategies
        self.payoff_matrix = payoff_matrix
        self.random_events = random_events
        self.history = []
    
    def play_round(self, strategy_choices):
        """
        Play one round with given strategies.
        """
        # First, determine which random event occurs
        # For simplicity, pick a random event with equal probability
        event = random.choice(self.random_events)
        
        # Calculate payoff based on strategies and event
        # For simplicity, we'll use a modified payoff
        base_payoff = self.payoff_matrix[tuple(strategy_choices)]
        
        # Modify payoff based on random event
        payoff_modifier = event.get('modifier', 1.0)
        event_name = event.get('name', 'No event')
        
        # Return payoff and event information
        return base_payoff * payoff_modifier, event_name
    
    def monte_carlo_analysis(self, num_rounds=10000):
        """
        Run Monte Carlo simulation to analyze strategy performance.
        """
        # Count total payoffs for each strategy
        strategy_payoffs = Counter()
        strategy_counts = Counter()
        
        # Track results for each round
        results = []
        
        for _ in range(num_rounds):
            # Randomly select strategies for each player
            strategy_tuple = tuple(random.choice(self.strategies[i]) 
                                  for i in range(self.num_players))
            
            # Play the round
            payoff, event = self.play_round(strategy_tuple)
            
            # Record results
            strategy_key = ', '.join(f'P{i+1}: {s}' 
                                    for i, s in enumerate(strategy_tuple))
            strategy_payoffs[strategy_key] += payoff
            strategy_counts[strategy_key] += 1
            results.append({
                'strategies': strategy_tuple,
                'payoff': payoff,
                'event': event
            })
        
        return strategy_payoffs, strategy_counts, results

# Define a strategic game
def run_game_theory_mc_example():
    """
    Example: A simplified market competition game.
    
    Players: Two companies deciding whether to compete or cooperate.
    Random events: Market conditions (good, neutral, bad).
    """
    
    # Define strategies
    strategies = [
        ['Compete', 'Cooperate'],  # Player 1 (Company A)
        ['Compete', 'Cooperate']   # Player 2 (Company B)
    ]
    
    # Define payoff matrix (P1, P2)
    # Format: (P1_strategy, P2_strategy) -> (P1_payoff, P2_payoff)
    payoff_matrix = {
        ('Compete', 'Compete'): (5, 5),    # Both compete: moderate profits
        ('Compete', 'Cooperate'): (8, 2),  # P1 competes, P2 cooperates: P1 wins
        ('Cooperate', 'Compete'): (2, 8),  # P1 cooperates, P2 competes: P2 wins
        ('Cooperate', 'Cooperate'): (6, 6) # Both cooperate: good for both
    }
    
    # Define random events
    random_events = [
        {'name': 'Good Market', 'modifier': 1.2, 'probability': 0.3},
        {'name': 'Neutral Market', 'modifier': 1.0, 'probability': 0.5},
        {'name': 'Bad Market', 'modifier': 0.8, 'probability': 0.2}
    ]
    
    # Create and run the game
    game = StrategicGameWithMonteCarlo(2, strategies, payoff_matrix, random_events)
    payoffs, counts, results = game.monte_carlo_analysis(10000)
    
    # Calculate average payoffs
    avg_payoffs = {}
    for strategy_key, total_payoff in payoffs.items():
        count = counts[strategy_key]
        avg_payoffs[strategy_key] = total_payoff / count
    
    print("Game Theory + Monte Carlo Analysis")
    print("=" * 60)
    print("Strategic Game: Market Competition")
    print("-" * 60)
    print("Strategy Pair".ljust(30) + "|" + "Avg Payoff".center(15) + "|" + "Frequency".center(15))
    print("-" * 70)
    
    total_count = sum(counts.values())
    for strategy, avg_payoff in sorted(avg_payoffs.items(), key=lambda x: x[1], reverse=True):
        count = counts[strategy]
        pct = count / total_count * 100
        print(f"{strategy[:30].ljust(30)} | {avg_payoff:>14.2f} | {pct:>14.1f}%")
    
    print("\n" + "=" * 60)
    print("Key Insight:")
    print("  Competing gives higher payoff in this model")
    print("  But cooperation is better for both (Pareto optimal)")
    print("  This is a Prisoner's Dilemma with random market effects!")
    
    return avg_payoffs, results

# Run the game theory + Monte Carlo example
run_game_theory_mc_example()
```

### 📊 Visualization: Game Theory + Monte Carlo

```python
def visualize_game_theory_mc(avg_payoffs, results):
    """
    Visualize the game theory + Monte Carlo results.
    """
    fig,