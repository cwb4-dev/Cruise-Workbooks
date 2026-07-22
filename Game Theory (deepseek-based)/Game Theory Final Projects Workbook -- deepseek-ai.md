# Game Theory Final Projects Workbook -- deepseek-ai
## Complete Guide to Strategic Decision-Making Simulations in Python & Jupyter

---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Jupyter](https://img.shields.io/badge/Jupyter-F37626.svg?&logo=Jupyter&logoColor=white)](https://jupyter.org/)

---

## 📚 Overview

This comprehensive workbook contains **5 complete projects** that apply game theory and Monte Carlo simulation to real-world strategic situations. Each project is self-contained and includes:

1. **Problem Statement**: What strategic situation are we modeling?
2. **Theoretical Framework**: Game theory foundations
3. **Implementation**: Complete Python code
4. **Visualization**: Interactive and static visualizations
5. **Analysis**: Interpreting results
6. **Extensions**: Ways to expand the model

---

## 🎓 Prerequisites & Setup

```bash
pip install numpy matplotlib pandas scipy networkx seaborn ipywidgets plotly
```

```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import seaborn as sns
from scipy import stats
from collections import defaultdict, Counter
import random
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

print("✅ All imports successful!")
```

---

# PROJECT 1: Market Competition with Multiple Firms

### 📖 Problem Statement

**Scenario**: Multiple firms compete in an oligopolistic market. Each firm chooses:
- **Price** (Bertrand competition) or **Quantity** (Cournot competition)
- **Investment level** in R&D or marketing
- **Market entry/exit** decisions

**Key Questions**:
1. What is the Nash equilibrium?
2. How does the number of firms affect prices and profits?
3. How do firms respond to changes in costs or demand?
4. Can firms collude successfully?

### 🤔 Theoretical Framework

**Cournot Competition with N Firms**:
- Market demand: P = a - b * Q (where Q = Σ qᵢ)
- Cost: Cᵢ(qᵢ) = c * qᵢ + F (where F is fixed cost)
- Profit: πᵢ = (a - b * Σq - c) * qᵢ - F

**Nash Equilibrium** (symmetric):
- q* = (a - c) / (b * (N + 1))
- P* = (a + N*c) / (N + 1)
- π* = (a - c)² / (b * (N + 1)²) - F

**Key Insight**: As N increases, price approaches marginal cost (perfect competition).

### 🛠️ Implementation

```python
class MultiFirmMarket:
    """
    Simulates market competition with multiple firms.
    Supports Cournot (quantity) and Bertrand (price) competition.
    """
    
    def __init__(self, 
                 num_firms=5,
                 demand_intercept=100,
                 demand_slope=1,
                 marginal_cost=10,
                 fixed_cost=0,
                 competition_type='cournot'):
        """
        Initialize the market.
        
        Parameters:
        num_firms: Number of firms in the market
        demand_intercept: a in P = a - b*Q
        demand_slope: b in P = a - b*Q
        marginal_cost: Constant marginal cost
        fixed_cost: Fixed cost per firm
        competition_type: 'cournot' or 'bertrand'
        """
        self.num_firms = num_firms
        self.a = demand_intercept
        self.b = demand_slope
        self.c = marginal_cost
        self.f = fixed_cost
        self.competition_type = competition_type
        
        # Initialize firms
        self.quantities = np.ones(num_firms) * self._initial_quantity()
        self.prices = np.ones(num_firms) * self._initial_price()
        self.profits = np.zeros(num_firms)
        self.history = {
            'quantities': [self.quantities.copy()],
            'prices': [self.prices.copy()],
            'profits': [self.profits.copy()],
            'total_quantity': [np.sum(self.quantities)],
            'market_price': [self._market_price()]
        }
    
    def _initial_quantity(self):
        """Initial quantity for each firm"""
        return (self.a - self.c) / (self.b * (self.num_firms + 1))
    
    def _initial_price(self):
        """Initial price for each firm"""
        return (self.a + self.num_firms * self.c) / (self.num_firms + 1)
    
    def _market_price(self):
        """Calculate market price"""
        if self.competition_type == 'cournot':
            total_q = np.sum(self.quantities)
            return max(0, self.a - self.b * total_q)
        else:
            # Bertrand: price is minimum of firm prices
            return np.min(self.prices)
    
    def _cournot_best_response(self, firm_index):
        """Best response quantity for Cournot competition"""
        other_quantity = np.sum(self.quantities) - self.quantities[firm_index]
        br = (self.a - self.c - self.b * other_quantity) / (2 * self.b)
        return max(0, br)
    
    def _bertrand_best_response(self, firm_index):
        """Best response price for Bertrand competition"""
        min_price = np.min(self.prices)
        if self.prices[firm_index] > min_price:
            # If price is above minimum, lower to just below min price
            return max(self.c, min_price - 0.01)
        else:
            # If at minimum, keep price or slightly increase
            return self.prices[firm_index]
    
    def step(self, learning_rate=0.5):
        """
        Update firms' strategies using best response with learning.
        """
        new_quantities = self.quantities.copy()
        new_prices = self.prices.copy()
        
        for i in range(self.num_firms):
            if self.competition_type == 'cournot':
                br = self._cournot_best_response(i)
                # Gradual adjustment
                new_quantities[i] = (1 - learning_rate) * self.quantities[i] + learning_rate * br
            else:  # Bertrand
                br = self._bertrand_best_response(i)
                new_prices[i] = (1 - learning_rate) * self.prices[i] + learning_rate * br
        
        self.quantities = new_quantities
        self.prices = new_prices
        
        # Calculate profits
        market_price = self._market_price()
        for i in range(self.num_firms):
            if self.competition_type == 'cournot':
                self.profits[i] = max(0, (market_price - self.c) * self.quantities[i] - self.f)
            else:
                # Bertrand: firm with lowest price gets all demand
                if self.prices[i] == np.min(self.prices):
                    demand = (self.a - self.prices[i]) / self.b
                    quantity = demand / np.sum(self.prices == np.min(self.prices))
                    self.profits[i] = max(0, (self.prices[i] - self.c) * quantity - self.f)
                else:
                    self.profits[i] = -self.f
        
        # Record history
        self.history['quantities'].append(self.quantities.copy())
        self.history['prices'].append(self.prices.copy())
        self.history['profits'].append(self.profits.copy())
        self.history['total_quantity'].append(np.sum(self.quantities))
        self.history['market_price'].append(market_price)
    
    def simulate(self, num_steps=100, learning_rate=0.5):
        """Run simulation for multiple steps"""
        for _ in range(num_steps):
            self.step(learning_rate)
    
    def get_results(self):
        """Get final results"""
        return {
            'quantities': self.quantities,
            'prices': self.prices,
            'profits': self.profits,
            'market_price': self.history['market_price'][-1],
            'total_quantity': self.history['total_quantity'][-1],
            'concentration': self._calculate_concentration(),
            'efficiency': self._calculate_efficiency()
        }
    
    def _calculate_concentration(self):
        """Calculate Herfindahl-Hirschman Index (HHI)"""
        shares = self.quantities / np.sum(self.quantities)
        return np.sum(shares**2) * 10000
    
    def _calculate_efficiency(self):
        """Calculate market efficiency (consumer surplus + producer surplus)"""
        market_price = self.history['market_price'][-1]
        total_q = np.sum(self.quantities)
        
        # Consumer surplus
        cs = 0.5 * (self.a - market_price) * total_q
        
        # Producer surplus
        ps = np.sum(self.profits)
        
        # Deadweight loss
        q_pc = (self.a - self.c) / self.b  # Perfect competition quantity
        dwl = 0.5 * (self.a - self.c) * (q_pc - total_q) / self.b
        
        return {
            'consumer_surplus': cs,
            'producer_surplus': ps,
            'deadweight_loss': max(0, dwl),
            'total_surplus': cs + ps
        }
    
    def plot_evolution(self):
        """Plot the evolution of key variables"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        
        steps = len(self.history['quantities'])
        time = np.arange(steps)
        
        # Plot 1: Quantities over time
        for i in range(self.num_firms):
            quantities = [q[i] for q in self.history['quantities']]
            axes[0, 0].plot(time, quantities, label=f'Firm {i+1}', alpha=0.7)
        axes[0, 0].set_xlabel('Time')
        axes[0, 0].set_ylabel('Quantity')
        axes[0, 0].set_title('Firm Quantities Over Time')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Prices over time
        for i in range(self.num_firms):
            prices = [p[i] for p in self.history['prices']]
            axes[0, 1].plot(time, prices, label=f'Firm {i+1}', alpha=0.7)
        axes[0, 1].plot(time, self.history['market_price'], 'k--', 
                      label='Market Price', linewidth=2)
        axes[0, 1].axhline(y=self.c, color='red', linestyle=':', 
                          label='Marginal Cost', alpha=0.7)
        axes[0, 1].set_xlabel('Time')
        axes[0, 1].set_ylabel('Price')
        axes[0, 1].set_title('Prices Over Time')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Profits over time
        for i in range(self.num_firms):
            profits = [p[i] for p in self.history['profits']]
            axes[1, 0].plot(time, profits, label=f'Firm {i+1}', alpha=0.7)
        axes[1, 0].axhline(y=0, color='red', linestyle='--', alpha=0.5)
        axes[1, 0].set_xlabel('Time')
        axes[1, 0].set_ylabel('Profit')
        axes[1, 0].set_title('Firm Profits Over Time')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 4: Market metrics
        axes[1, 1].plot(time, self.history['total_quantity'], 
                       'b-', label='Total Quantity', linewidth=2)
        axes[1, 1].plot(time, self.history['market_price'], 
                       'r-', label='Market Price', linewidth=2)
        axes[1, 1].set_xlabel('Time')
        axes[1, 1].set_ylabel('Value')
        axes[1, 1].set_title('Market Metrics')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def plot_market_analysis(self):
        """Plot comprehensive market analysis"""
        results = self.get_results()
        efficiency = self._calculate_efficiency()
        
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # Plot 1: Firm market shares
        shares = self.quantities / np.sum(self.quantities) * 100
        colors = sns.color_palette("viridis", self.num_firms)
        axes[0].pie(shares, labels=[f'Firm {i+1}' for i in range(self.num_firms)],
                   colors=colors, autopct='%1.1f%%', startangle=90)
        axes[0].set_title(f'Market Shares\nHHI: {results["concentration"]:.0f}')
        
        # Plot 2: Profit distribution
        colors = ['green' if p > 0 else 'red' for p in self.profits]
        bars = axes[1].bar(range(self.num_firms), self.profits, color=colors, alpha=0.7)
        axes[1].axhline(y=0, color='black', linestyle='-', alpha=0.3)
        axes[1].set_xlabel('Firm')
        axes[1].set_ylabel('Profit')
        axes[1].set_title('Profit Distribution')
        axes[1].set_xticks(range(self.num_firms))
        axes[1].set_xticklabels([f'F{i+1}' for i in range(self.num_firms)])
        axes[1].grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for bar, profit in zip(bars, self.profits):
            height = bar.get_height()
            axes[1].text(bar.get_x() + bar.get_width()/2., 
                        height + (0.1 if height > 0 else -0.1),
                        f'{profit:.0f}', ha='center', va='bottom' if height > 0 else 'top')
        
        # Plot 3: Efficiency analysis
        labels = ['Consumer Surplus', 'Producer Surplus', 'Deadweight Loss']
        values = [efficiency['consumer_surplus'], 
                 efficiency['producer_surplus'], 
                 efficiency['deadweight_loss']]
        colors = ['blue', 'green', 'red']
        
        axes[2].bar(labels, values, color=colors, alpha=0.7)
        axes[2].set_ylabel('Value')
        axes[2].set_title('Market Efficiency')
        axes[2].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.show()
        
        # Print summary
        print("\n📊 Market Summary")
        print("=" * 60)
        print(f"Number of Firms: {self.num_firms}")
        print(f"Competition Type: {self.competition_type.capitalize()}")
        print(f"Market Price: {results['market_price']:.2f}")
        print(f"Total Quantity: {results['total_quantity']:.2f}")
        print(f"HHI: {results['concentration']:.0f} ({'Concentrated' if results['concentration'] > 2500 else 'Moderate' if results['concentration'] > 1500 else 'Competitive'})")
        print(f"\nTotal Surplus: {efficiency['total_surplus']:.2f}")
        print(f"Consumer Surplus: {efficiency['consumer_surplus']:.2f}")
        print(f"Producer Surplus: {efficiency['producer_surplus']:.2f}")
        print(f"Deadweight Loss: {efficiency['deadweight_loss']:.2f}")

# Run the market simulation
print("🏪 Market Competition Simulation")
print("=" * 70)

# Create and simulate market
market = MultiFirmMarket(
    num_firms=5,
    demand_intercept=100,
    demand_slope=0.5,
    marginal_cost=10,
    fixed_cost=5,
    competition_type='cournot'
)

market.simulate(num_steps=100, learning_rate=0.3)
market.plot_evolution()
market.plot_market_analysis()
```

### 📊 Sensitivity Analysis

```python
def sensitivity_analysis():
    """Analyze how market outcomes change with different parameters"""
    
    results = []
    
    # Vary number of firms
    for n in [2, 3, 5, 10, 20]:
        market = MultiFirmMarket(
            num_firms=n,
            demand_intercept=100,
            demand_slope=0.5,
            marginal_cost=10,
            fixed_cost=5
        )
        market.simulate(num_steps=50)
        results.append({
            'num_firms': n,
            'price': market.history['market_price'][-1],
            'total_q': market.history['total_quantity'][-1],
            'avg_profit': np.mean(market.profits),
            'total_profit': np.sum(market.profits),
            'hhi': market._calculate_concentration()
        })
    
    # Create comparison plots
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    df = pd.DataFrame(results)
    
    # Plot 1: Price vs Number of Firms
    axes[0, 0].plot(df['num_firms'], df['price'], 'bo-', linewidth=2, markersize=8)
    axes[0, 0].axhline(y=market.c, color='red', linestyle='--', label='Marginal Cost')
    axes[0, 0].set_xlabel('Number of Firms')
    axes[0, 0].set_ylabel('Market Price')
    axes[0, 0].set_title('Price vs Number of Firms')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Total Quantity vs Number of Firms
    axes[0, 1].plot(df['num_firms'], df['total_q'], 'go-', linewidth=2, markersize=8)
    # Perfect competition quantity
    q_pc = (market.a - market.c) / market.b
    axes[0, 1].axhline(y=q_pc, color='green', linestyle='--', label='Perfect Competition')
    axes[0, 1].set_xlabel('Number of Firms')
    axes[0, 1].set_ylabel('Total Quantity')
    axes[0, 1].set_title('Total Quantity vs Number of Firms')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Average Profit vs Number of Firms
    axes[1, 0].plot(df['num_firms'], df['avg_profit'], 'ro-', linewidth=2, markersize=8)
    axes[1, 0].axhline(y=0, color='red', linestyle='--', alpha=0.5)
    axes[1, 0].set_xlabel('Number of Firms')
    axes[1, 0].set_ylabel('Average Profit')
    axes[1, 0].set_title('Average Profit vs Number of Firms')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 4: HHI vs Number of Firms
    axes[1, 1].plot(df['num_firms'], df['hhi'], 'mo-', linewidth=2, markersize=8)
    axes[1, 1].axhline(y=2500, color='red', linestyle='--', alpha=0.5, label='High Concentration')
    axes[1, 1].axhline(y=1500, color='orange', linestyle='--', alpha=0.5, label='Moderate Concentration')
    axes[1, 1].set_xlabel('Number of Firms')
    axes[1, 1].set_ylabel('Herfindahl-Hirschman Index (HHI)')
    axes[1, 1].set_title('Market Concentration vs Number of Firms')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    return df

# Run sensitivity analysis
sensitivity_results = sensitivity_analysis()
```

### 🎯 Extensions

```python
def extension_1_firm_heterogeneity():
    """Extension: Firms with different costs"""
    
    # Firms with different marginal costs
    costs = [10, 12, 15, 8, 11]  # Different efficiencies
    fixed_costs = [5, 7, 10, 3, 6]
    
    # Create custom market with heterogeneous firms
    class HeterogeneousMarket(MultiFirmMarket):
        def __init__(self, costs, fixed_costs, *args, **kwargs):
            self.firm_costs = costs
            self.firm_fixed = fixed_costs
            super().__init__(num_firms=len(costs), *args, **kwargs)
            self.c = np.mean(costs)  # Average cost for equilibrium calculation
        
        def _cournot_best_response(self, firm_index):
            other_quantity = np.sum(self.quantities) - self.quantities[firm_index]
            c_i = self.firm_costs[firm_index]
            br = (self.a - c_i - self.b * other_quantity) / (2 * self.b)
            return max(0, br)
    
    # Run simulation
    hetero_market = HeterogeneousMarket(
        costs=costs,
        fixed_costs=fixed_costs,
        demand_intercept=100,
        demand_slope=0.5,
        competition_type='cournot'
    )
    hetero_market.simulate(num_steps=100)
    hetero_market.plot_evolution()
    
    print("\n📊 Heterogeneous Firms Analysis")
    print("=" * 60)
    print("Firm | Cost | Fixed Cost | Quantity | Profit")
    print("-" * 60)
    for i in range(hetero_market.num_firms):
        print(f"  {i+1}  | {hetero_market.firm_costs[i]:.1f}  | {hetero_market.firm_fixed[i]:.1f}    | "
              f"{hetero_market.quantities[i]:.2f}   | {hetero_market.profits[i]:.2f}")

# Run extension
extension_1_firm_heterogeneity()
```

---

# PROJECT 2: Political Campaign Strategy

### 📖 Problem Statement

**Scenario**: Two (or more) candidates compete in an election. Each candidate chooses:
- **Policy position** on a spectrum (left-right)
- **Campaign spending** on advertising
- **Messaging strategy** (positive vs negative)

**Key Questions**:
1. Where should candidates position themselves?
2. How much should they spend on campaigns?
3. How does voter distribution affect outcomes?
4. Can third-party candidates be viable?

### 🤔 Theoretical Framework

**Hotelling-Downs Model**:
- Voters are distributed uniformly on [0, 1]
- Candidates choose positions x₁, x₂ ∈ [0, 1]
- Voters vote for the closest candidate
- **Median Voter Theorem**: Both candidates converge to the median

**Key Insight**: Candidates have incentive to move to the center to capture more voters.

### 🛠️ Implementation

```python
class PoliticalCampaign:
    """
    Simulates political campaigns with spatial competition.
    """
    
    def __init__(self, 
                 num_candidates=2,
                 voter_distribution='uniform',
                 campaign_budget=100,
                 voter_turnout=0.6):
        """
        Initialize the political campaign.
        
        Parameters:
        num_candidates: Number of candidates
        voter_distribution: 'uniform', 'normal', or 'bimodal'
        campaign_budget: Total budget for each candidate
        voter_turnout: Percentage of voters who vote
        """
        self.num_candidates = num_candidates
        self.voter_distribution = voter_distribution
        self.campaign_budget = campaign_budget
        self.voter_turnout = voter_turnout
        
        # Initialize candidate positions and spending
        self.positions = np.random.uniform(0.2, 0.8, num_candidates)
        self.spending = np.ones(num_candidates) * (campaign_budget / num_candidates)
        self.poll_results = np.zeros(num_candidates)
        
        # Track history
        self.history = {
            'positions': [self.positions.copy()],
            'spending': [self.spending.copy()],
            'votes': [],
            'poll_results': []
        }
        
        # Generate voters
        self.voters = self._generate_voters(10000)
    
    def _generate_voters(self, num_voters):
        """Generate voter positions based on distribution"""
        if self.voter_distribution == 'uniform':
            positions = np.random.uniform(0, 1, num_voters)
        elif self.voter_distribution == 'normal':
            positions = np.random.normal(0.5, 0.2, num_voters)
            positions = np.clip(positions, 0, 1)
        elif self.voter_distribution == 'bimodal':
            half = num_voters // 2
            positions = np.concatenate([
                np.random.normal(0.3, 0.1, half),
                np.random.normal(0.7, 0.1, num_voters - half)
            ])
            positions = np.clip(positions, 0, 1)
        else:
            positions = np.random.uniform(0, 1, num_voters)
        
        return positions
    
    def _voter_utility(self, voter_position, candidate_position, candidate_spending):
        """
        Calculate voter utility for a candidate.
        Utility = -distance + (spending effect)
        """
        distance = abs(voter_position - candidate_position)
        spending_effect = 0.1 * (candidate_spending / self.campaign_budget)
        return -distance + spending_effect
    
    def simulate_election(self):
        """
        Simulate the election based on current positions and spending.
        """
        # Determine which voters turn out
        turnout_mask = np.random.random(len(self.voters)) < self.voter_turnout
        active_voters = self.voters[turnout_mask]
        
        if len(active_voters) == 0:
            return
        
        # Calculate utilities for each voter
        votes = np.zeros(self.num_candidates)
        total_utility = np.zeros(self.num_candidates)
        
        for voter in active_voters:
            utilities = np.array([
                self._voter_utility(voter, self.positions[i], self.spending[i])
                for i in range(self.num_candidates)
            ])
            
            # Voter chooses candidate with highest utility
            winner = np.argmax(utilities)
            votes[winner] += 1
            total_utility += utilities
        
        # Calculate vote shares
        if len(active_voters) > 0:
            vote_shares = votes / len(active_voters)
        else:
            vote_shares = np.ones(self.num_candidates) / self.num_candidates
        
        # Update poll results
        self.poll_results = vote_shares
        self.history['votes'].append(vote_shares)
        self.history['poll_results'].append(self.poll_results.copy())
    
    def update_positions(self, learning_rate=0.1):
        """
        Update candidate positions based on election results.
        Candidates move toward the median voter position.
        """
        if len(self.voters) > 0:
            # Weighted average of voter positions (weighted by vote share)
            # This is a simplified learning rule
            median_voter = np.median(self.voters)
            
            for i in range(self.num_candidates):
                # Move toward median voter
                direction = median_voter - self.positions[i]
                self.positions[i] += learning_rate * direction * self.poll_results[i]
                self.positions[i] = np.clip(self.positions[i], 0, 1)
    
    def update_spending(self, learning_rate=0.1):
        """
        Update campaign spending based on poll results.
        Candidates spend more if they're behind.
        """
        avg_results = np.mean(self.poll_results)
        
        for i in range(self.num_candidates):
            # If below average, increase spending
            if self.poll_results[i] < avg_results:
                self.spending[i] *= (1 + learning_rate)
            else:
                self.spending[i] *= (1 - learning_rate * 0.5)
            
            # Keep spending within budget
            self.spending[i] = np.clip(self.spending[i], 0, self.campaign_budget)
    
    def step(self, learning_rate=0.1):
        """One simulation step"""
        self.simulate_election()
        self.update_positions(learning_rate)
        self.update_spending(learning_rate)
        
        # Record history
        self.history['positions'].append(self.positions.copy())
        self.history['spending'].append(self.spending.copy())
    
    def simulate(self, num_rounds=50, learning_rate=0.1):
        """Run multiple rounds of the campaign"""
        for _ in range(num_rounds):
            self.step(learning_rate)
    
    def plot_campaign_dynamics(self):
        """Visualize the campaign dynamics"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        
        time = np.arange(len(self.history['positions']))
        
        # Plot 1: Candidate positions over time
        for i in range(self.num_candidates):
            positions = [p[i] for p in self.history['positions']]
            axes[0, 0].plot(time, positions, label=f'Candidate {i+1}', linewidth=2)
        
        # Show median voter
        axes[0, 0].axhline(y=np.median(self.voters), color='red', 
                          linestyle='--', label='Median Voter', alpha=0.7)
        axes[0, 0].set_xlabel('Round')
        axes[0, 0].set_ylabel('Position')
        axes[0, 0].set_title('Candidate Positions Over Time')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].set_ylim(-0.05, 1.05)
        
        # Plot 2: Campaign spending over time
        for i in range(self.num_candidates):
            spending = [s[i] for s in self.history['spending']]
            axes[0, 1].plot(time, spending, label=f'Candidate {i+1}', linewidth=2)
        axes[0, 1].set_xlabel('Round')
        axes[0, 1].set_ylabel('Spending')
        axes[0, 1].set_title('Campaign Spending Over Time')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Vote shares over time
        if len(self.history['votes']) > 0:
            vote_history = np.array(self.history['votes'])
            for i in range(self.num_candidates):
                axes[1, 0].plot(time[1:], vote_history[:, i], 
                              label=f'Candidate {i+1}', linewidth=2)
        axes[1, 0].set_xlabel('Round')
        axes[1, 0].set_ylabel('Vote Share')
        axes[1, 0].set_title('Vote Shares Over Time')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].set_ylim(0, 1)
        
        # Plot 4: Voter distribution
        axes[1, 1].hist(self.voters, bins=50, alpha=0.7, color='blue', 
                       density=True, label='Voter Distribution')
        
        # Show candidate positions
        for i, pos in enumerate(self.positions):
            axes[1, 1].axvline(x=pos, color=f'C{i}', linestyle='-', 
                             linewidth=3, label=f'Candidate {i+1}')
        
        axes[1, 1].set_xlabel('Position')
        axes[1, 1].set_ylabel('Density')
        axes[1, 1].set_title('Voter Distribution and Candidate Positions')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def analyze_results(self):
        """Analyze the final results"""
        print("\n📊 Campaign Analysis")
        print("=" * 60)
        print(f"Voter Distribution: {self.voter_distribution}")
        print(f"Voter Turnout: {self.voter_turnout:.1%}")
        print("-" * 60)
        
        for i in range(self.num_candidates):
            print(f"Candidate {i+1}:")
            print(f"  Position: {self.positions[i]:.3f}")
            print(f"  Spending: {self.spending[i]:.2f}")
            print(f"  Vote Share: {self.poll_results[i]:.1%}")
        
        # Calculate polarization
        if self.num_candidates >= 2:
            polarization = np.std(self.positions)
            print(f"\nPolarization (std of positions): {polarization:.3f}")
            
        # Calculate competitiveness
        if len(self.poll_results) >= 2:
            sorted_votes = np.sort(self.poll_results)
            margin = sorted_votes[-1] - sorted_votes[-2]
            print(f"Margin of Victory: {margin:.1%}")

# Run the campaign simulation
print("🗳️ Political Campaign Simulation")
print("=" * 70)

# Create and simulate campaign
campaign = PoliticalCampaign(
    num_candidates=2,
    voter_distribution='uniform',
    campaign_budget=100,
    voter_turnout=0.6
)

campaign.simulate(num_rounds=30, learning_rate=0.1)
campaign.plot_campaign_dynamics()
campaign.analyze_results()
```

### 📊 Multi-Candidate Analysis

```python
def multi_candidate_analysis():
    """Compare outcomes with different numbers of candidates"""
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for n_candidates, ax in zip([2, 3, 4], axes):
        campaign = PoliticalCampaign(
            num_candidates=n_candidates,
            voter_distribution='uniform',
            campaign_budget=100,
            voter_turnout=0.6
        )
        campaign.simulate(num_rounds=50, learning_rate=0.05)
        
        # Plot final positions
        positions = campaign.positions
        vote_shares = campaign.poll_results
        
        ax.bar(range(n_candidates), vote_shares, alpha=0.7, 
               color=sns.color_palette("viridis", n_candidates))
        
        # Add position labels
        for i, (pos, share) in enumerate(zip(positions, vote_shares)):
            ax.text(i, share + 0.02, f'x={pos:.2f}', 
                   ha='center', va='bottom', fontsize=10)
        
        ax.set_xlabel('Candidate')
        ax.set_ylabel('Vote Share')
        ax.set_title(f'{n_candidates} Candidates')
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.show()

# Run multi-candidate analysis
multi_candidate_analysis()
```

---

# PROJECT 3: Supply Chain Negotiation

### 📖 Problem Statement

**Scenario**: Multiple firms in a supply chain negotiate prices and quantities. Each firm has:
- **Upstream suppliers** (providing raw materials)
- **Downstream customers** (buying finished products)
- **Production capacity** and **costs**
- **Market power** in their segment

**Key Questions**:
1. How does bargaining power affect prices and profits?
2. What happens when one firm has monopoly power?
3. Can vertical integration improve efficiency?
4. How do supply shocks propagate through the chain?

### 🤔 Theoretical Framework

**Stackelberg Competition with Multiple Stages**:
- **Upstream firms** set wholesale prices
- **Downstream firms** set retail prices
- **Bargaining** occurs between chain members
- **Double marginalization**: Each stage marks up prices

**Key Insight**: Supply chain profits are maximized when firms coordinate pricing decisions.

### 🛠️ Implementation

```python
class SupplyChainNegotiation:
    """
    Simulates supply chain with multiple firms and bargaining.
    """
    
    def __init__(self, 
                 num_upstream=2,
                 num_downstream=3,
                 demand_intercept=100,
                 demand_slope=1,
                 production_cost=5,
                 bargaining_power=0.5):
        """
        Initialize the supply chain.
        
        Parameters:
        num_upstream: Number of upstream (supplier) firms
        num_downstream: Number of downstream (retailer) firms
        demand_intercept: a in P = a - b*Q
        demand_slope: b in P = a - b*Q
        production_cost: Cost per unit for upstream firms
        bargaining_power: 0 = all power to downstream, 1 = all power to upstream
        """
        self.num_upstream = num_upstream
        self.num_downstream = num_downstream
        self.a = demand_intercept
        self.b = demand_slope
        self.c = production_cost
        self.bargaining_power = bargaining_power
        
        # Initialize quantities and prices
        self.upstream_quantities = np.ones(num_upstream) * 10
        self.downstream_quantities = np.ones(num_downstream) * 10
        self.wholesale_prices = np.ones(num_upstream) * 20
        self.retail_prices = np.ones(num_downstream) * 30
        
        # Track profit margins
        self.upstream_margins = np.zeros(num_upstream)
        self.downstream_margins = np.zeros(num_downstream)
        
        # History
        self.history = {
            'upstream_q': [self.upstream_quantities.copy()],
            'downstream_q': [self.downstream_quantities.copy()],
            'wholesale_prices': [self.wholesale_prices.copy()],
            'retail_prices': [self.retail_prices.copy()],
            'upstream_profits': [],
            'downstream_profits': []
        }
        
        # Create network structure
        self._create_network()
    
    def _create_network(self):
        """Create random connections between upstream and downstream firms"""
        # Each downstream firm buys from 1-3 upstream firms
        self.supply_links = {}
        for d in range(self.num_downstream):
            num_suppliers = np.random.randint(1, min(3, self.num_upstream) + 1)
            suppliers = np.random.choice(self.num_upstream, num_suppliers, replace=False)
            self.supply_links[d] = suppliers
    
    def _calculate_market_price(self):
        """Calculate market price based on total supply"""
        total_q = np.sum(self.downstream_quantities)
        return max(0, self.a - self.b * total_q)
    
    def _calculate_downstream_profit(self, firm_idx):
        """Calculate profit for a downstream firm"""
        # Find all upstream suppliers
        suppliers = self.supply_links[firm_idx]
        
        # Average wholesale price from suppliers
        avg_wholesale = np.mean([self.wholesale_prices[s] for s in suppliers])
        
        # Retail price (marked up from wholesale)
        retail_price = avg_wholesale * (1 + 0.3)
        self.retail_prices[firm_idx] = retail_price
        
        # Profit = (retail - wholesale) * quantity - fixed costs
        quantity = self.downstream_quantities[firm_idx]
        profit = (retail_price - avg_wholesale) * quantity
        
        return max(0, profit)
    
    def _calculate_upstream_profit(self, firm_idx):
        """Calculate profit for an upstream firm"""
        # Find all downstream customers
        customers = [d for d in range(self.num_downstream) if firm_idx in self.supply_links[d]]
        
        if not customers:
            return 0
        
        # Calculate total quantity supplied
        total_q = sum(self.downstream_quantities[d] for d in customers)
        
        # Profit = (wholesale - cost) * quantity
        profit = (self.wholesale_prices[firm_idx] - self.c) * total_q
        
        return max(0, profit)
    
    def negotiate_prices(self):
        """
        Negotiate wholesale prices between upstream and downstream firms.
        Uses Nash bargaining with variable bargaining power.
        """
        # Calculate total surplus
        market_price = self._calculate_market_price()
        total_surplus = 0
        
        for d in range(self.num_downstream):
            # Downstream surplus from each supplier
            for s in self.supply_links[d]:
                # Upstream cost
                upstream_cost = self.c
                
                # Downstream revenue
                downstream_revenue = market_price * self.downstream_quantities[d]
                
                # Total surplus = revenue - upstream cost
                surplus = downstream_revenue - upstream_cost * self.downstream_quantities[d]
                
                # Split surplus based on bargaining power
                upstream_share = surplus * self.bargaining_power
                downstream_share = surplus * (1 - self.bargaining_power)
                
                # Set wholesale price
                upstream_margin = upstream_share / self.downstream_quantities[d]
                wholesale_price = self.c + upstream_margin
                self.wholesale_prices[s] = wholesale_price
                
                # Track margins
                self.upstream_margins[s] = upstream_margin
                self.downstream_margins[d] = downstream_share / self.downstream_quantities[d]
        
        # Update retail prices
        for d in range(self.num_downstream):
            suppliers = self.supply_links[d]
            avg_wholesale = np.mean([self.wholesale_prices[s] for s in suppliers])
            self.retail_prices[d] = avg_wholesale * 1.3  # 30% markup
    
    def adjust_quantities(self, learning_rate=0.5):
        """
        Adjust quantities based on profitability.
        Firms increase quantity if profitable, decrease if not.
        """
        # Upstream quantity adjustment
        for s in range(self.num_upstream):
            profit = self._calculate_upstream_profit(s)
            # Find customers
            customers = [d for d in range(self.num_downstream) if s in self.supply_links[d]]
            
            if customers and profit > 0:
                # Increase if profitable
                self.upstream_quantities[s] *= (1 + learning_rate * 0.05)
            elif customers:
                # Decrease if not profitable
                self.upstream_quantities[s] *= (1 - learning_rate * 0.05)
            
            self.upstream_quantities[s] = max(0, self.upstream_quantities[s])
        
        # Downstream quantity adjustment
        for d in range(self.num_downstream):
            profit = self._calculate_downstream_profit(d)
            
            if profit > 0:
                self.downstream_quantities[d] *= (1 + learning_rate * 0.05)
            else:
                self.downstream_quantities[d] *= (1 - learning_rate * 0.05)
            
            self.downstream_quantities[d] = max(0, self.downstream_quantities[d])
    
    def step(self, learning_rate=0.5):
        """One step of the simulation"""
        self.negotiate_prices()
        self.adjust_quantities(learning_rate)
        
        # Calculate profits
        upstream_profits = [self._calculate_upstream_profit(s) for s in range(self.num_upstream)]
        downstream_profits = [self._calculate_downstream_profit(d) for d in range(self.num_downstream)]
        
        # Record history
        self.history['upstream_q'].append(self.upstream_quantities.copy())
        self.history['downstream_q'].append(self.downstream_quantities.copy())
        self.history['wholesale_prices'].append(self.wholesale_prices.copy())
        self.history['retail_prices'].append(self.retail_prices.copy())
        self.history['upstream_profits'].append(upstream_profits)
        self.history['downstream_profits'].append(downstream_profits)
    
    def simulate(self, num_steps=100, learning_rate=0.5):
        """Run simulation for multiple steps"""
        for _ in range(num_steps):
            self.step(learning_rate)
    
    def plot_supply_chain(self):
        """Visualize the supply chain network"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        
        time = np.arange(len(self.history['upstream_q']))
        
        # Plot 1: Network structure
        G = nx.DiGraph()
        
        # Add nodes
        for u in range(self.num_upstream):
            G.add_node(f'U{u}', node_type='upstream')
        for d in range(self.num_downstream):
            G.add_node(f'D{d}', node_type='downstream')
        
        # Add edges (supply links)
        for d, suppliers in self.supply_links.items():
            for s in suppliers:
                G.add_edge(f'U{s}', f'D{d}')
        
        # Position nodes
        pos = {}
        for u in range(self.num_upstream):
            pos[f'U{u}'] = (0, -u + self.num_upstream/2)
        for d in range(self.num_downstream):
            pos[f'D{d}'] = (1, -d + self.num_downstream/2)
        
        # Draw network
        nx.draw(G, pos, ax=axes[0, 0], with_labels=True, 
                node_color=['lightblue' if 'U' in n else 'lightgreen' for n in G.nodes()],
                node_size=1500, font_size=10, font_weight='bold',
                arrowsize=20, arrowstyle='->')
        axes[0, 0].set_title('Supply Chain Network Structure')
        
        # Plot 2: Prices over time
        wholesale_history = np.array(self.history['wholesale_prices'])
        retail_history = np.array(self.history['retail_prices'])
        
        for u in range(self.num_upstream):
            axes[0, 1].plot(time, wholesale_history[:, u], 
                          linestyle='--', label=f'Wholesale U{u}', alpha=0.7)
        for d in range(self.num_downstream):
            axes[0, 1].plot(time, retail_history[:, d], 
                          label=f'Retail D{d}', alpha=0.7)
        axes[0, 1].set_xlabel('Time')
        axes[0, 1].set_ylabel('Price')
        axes[0, 1].set_title('Prices Over Time')
        axes[0, 1].legend(loc='best')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Profits over time
        upstream_profits = np.array(self.history['upstream_profits'])
        downstream_profits = np.array(self.history['downstream_profits'])
        
        for u in range(self.num_upstream):
            axes[1, 0].plot(time[1:], upstream_profits[:, u], 
                          label=f'Upstream U{u}', alpha=0.7)
        for d in range(self.num_downstream):
            axes[1, 0].plot(time[1:], downstream_profits[:, d], 
                          linestyle='--', label=f'Downstream D{d}', alpha=0.7)
        axes[1, 0].set_xlabel('Time')
        axes[1, 0].set_ylabel('Profit')
        axes[1, 0].set_title('Profits Over Time')
        axes[1, 0].legend(loc='best')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 4: Total supply chain surplus
        total_surplus = []
        for t in range(len(upstream_profits)):
            total_surplus.append(np.sum(upstream_profits[t]) + np.sum(downstream_profits[t]))
        
        axes[1, 1].plot(time[1:], total_surplus, 'bo-', linewidth=2)
        axes[1, 1].set_xlabel('Time')
        axes[1, 1].set_ylabel('Total Surplus')
        axes[1, 1].set_title('Total Supply Chain Surplus')
        axes[1, 1].grid(True, alpha=0.3)
        
        # Add horizontal line for theoretical maximum
        max_surplus = (self.a - self.c)**2 / (4 * self.b)
        axes[1, 1].axhline(y=max_surplus, color='red', linestyle='--', 
                          label='Theoretical Max')
        axes[1, 1].legend()
        
        plt.tight_layout()
        plt.show()
    
    def analyze_supply_chain(self):
        """Comprehensive analysis of supply chain performance"""
        print("\n📊 Supply Chain Analysis")
        print("=" * 70)
        print(f"Upstream Firms: {self.num_upstream}")
        print(f"Downstream Firms: {self.num_downstream}")
        print(f"Bargaining Power: {self.bargaining_power:.2f}")
        print("-" * 70)
        
        # Final profits
        final_up_profits = [self._calculate_upstream_profit(s) for s in range(self.num_upstream)]
        final_down_profits = [self._calculate_downstream_profit(d) for d in range(self.num_downstream)]
        
        print("\nUpstream Firms:")
        for s in range(self.num_upstream):
            print(f"  U{s}: Quantity={self.upstream_quantities[s]:.2f}, "
                  f"Price={self.wholesale_prices[s]:.2f}, "
                  f"Profit={final_up_profits[s]:.2f}")
        
        print("\nDownstream Firms:")
        for d in range(self.num_downstream):
            print(f"  D{d}: Quantity={self.downstream_quantities[d]:.2f}, "
                  f"Price={self.retail_prices[d]:.2f}, "
                  f"Profit={final_down_profits[d]:.2f}")
        
        # Efficiency metrics
        total_profit = sum(final_up_profits) + sum(final_down_profits)
        market_price = self._calculate_market_price()
        
        # Consumer surplus
        total_q = np.sum(self.downstream_quantities)
        cs = 0.5 * (self.a - market_price) * total_q
        
        print(f"\n📈 Efficiency Metrics:")
        print(f"  Total Industry Profit: {total_profit:.2f}")
        print(f"  Consumer Surplus: {cs:.2f}")
        print(f"  Total Surplus: {total_profit + cs:.2f}")
        print(f"  Market Price: {market_price:.2f}")
        print(f"  Total Quantity: {total_q:.2f}")
        
        # Calculate double marginalization loss
        perfect_competition_q = (self.a - self.c) / self.b
        efficiency_loss = perfect_competition_q - total_q
        print(f"  Efficiency Loss: {efficiency_loss:.2f} units")
        
        return {
            'total_profit': total_profit,
            'consumer_surplus': cs,
            'total_surplus': total_profit + cs,
            'market_price': market_price,
            'total_quantity': total_q
        }

# Run supply chain simulation
print("🏗️ Supply Chain Negotiation Simulation")
print("=" * 70)

# Create and simulate supply chain
sc = SupplyChainNegotiation(
    num_upstream=3,
    num_downstream=4,
    demand_intercept=100,
    demand_slope=0.5,
    production_cost=10,
    bargaining_power=0.4
)

sc.simulate(num_steps=80)
sc.plot_supply_chain()
sc.analyze_supply_chain()
```

### 📊 Sensitivity to Bargaining Power

```python
def bargaining_power_analysis():
    """Analyze how bargaining power affects outcomes"""
    
    bargaining_powers = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    results = []
    
    for bp in bargaining_powers:
        sc = SupplyChainNegotiation(
            num_upstream=3,
            num_downstream=3,
            demand_intercept=100,
            demand_slope=0.5,
            production_cost=10,
            bargaining_power=bp
        )
        sc.simulate(num_steps=50)
        
        # Collect final results
        upstream_profits = [sc._calculate_upstream_profit(s) for s in range(sc.num_upstream)]
        downstream_profits = [sc._calculate_downstream_profit(d) for d in range(sc.num_downstream)]
        total_profit = sum(upstream_profits) + sum(downstream_profits)
        
        results.append({
            'bargaining_power': bp,
            'upstream_profit': np.mean(upstream_profits),
            'downstream_profit': np.mean(downstream_profits),
            'total_profit': total_profit,
            'wholesale_price': np.mean(sc.wholesale_prices),
            'retail_price': np.mean(sc.retail_prices)
        })
    
    # Create comparison plots
    df = pd.DataFrame(results)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # Plot 1: Profits vs Bargaining Power
    axes[0, 0].plot(df['bargaining_power'], df['upstream_profit'], 
                   'bo-', label='Upstream Profit', linewidth=2, markersize=8)
    axes[0, 0].plot(df['bargaining_power'], df['downstream_profit'], 
                   'ro-', label='Downstream Profit', linewidth=2, markersize=8)
    axes[0, 0].plot(df['bargaining_power'], df['total_profit'], 
                   'go-', label='Total Profit', linewidth=2, markersize=8)
    axes[0, 0].set_xlabel('Bargaining Power (Upstream)')
    axes[0, 0].set_ylabel('Profit')
    axes[0, 0].set_title('Profits vs Bargaining Power')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Prices vs Bargaining Power
    axes[0, 1].plot(df['bargaining_power'], df['wholesale_price'], 
                   'bo-', label='Wholesale Price', linewidth=2, markersize=8)
    axes[0, 1].plot(df['bargaining_power'], df['retail_price'], 
                   'ro-', label='Retail Price', linewidth=2, markersize=8)
    axes[0, 1].set_xlabel('Bargaining Power (Upstream)')
    axes[0, 1].set_ylabel('Price')
    axes[0, 1].set_title('Prices vs Bargaining Power')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Profit distribution
    width = 0.15
    x = np.arange(len(bargaining_powers))
    
    axes[1, 0].bar(x - width, df['upstream_profit'], width, 
                  label='Upstream', alpha=0.7)
    axes[1, 0].bar(x, df['downstream_profit'], width, 
                  label='Downstream', alpha=0.7)
    axes[1, 0].set_xlabel('Bargaining Power')
    axes[1, 0].set_ylabel('Profit')
    axes[1, 0].set_title('Profit Distribution by Bargaining Power')
    axes[1, 0].set_xticks(x)
    axes[1, 0].set_xticklabels([f'{bp:.1f}' for bp in bargaining_powers])
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    # Plot 4: Supply chain efficiency
    # Calculate efficiency (total surplus as % of theoretical maximum)
    max_surplus = (sc.a - sc.c)**2 / (4 * sc.b)
    efficiencies = [r['total_profit'] / max_surplus * 100 for r in results]
    
    axes[1, 1].plot(df['bargaining_power'], efficiencies, 
                   'mo-', linewidth=2, markersize=8)
    axes[1, 1].set_xlabel('Bargaining Power (Upstream)')
    axes[1, 1].set_ylabel('Efficiency (%)')
    axes[1, 1].set_title('Supply Chain Efficiency vs Bargaining Power')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    return df

# Run bargaining power analysis
bargaining_results = bargaining_power_analysis()
```

---

# PROJECT 4: International Diplomacy Game

### 📖 Problem Statement

**Scenario**: Multiple nations interact in a complex geopolitical environment. Each nation:
- Has **military power** and **economic strength**
- Can **cooperate** (trade, alliances) or **compete** (sanctions, conflict)
- Responds to **threats** and **incentives**
- Forms **alliances** and **coalitions**

**Key Questions**:
1. How do alliances form and dissolve?
2. What strategies prevent conflict?
3. How does power imbalance affect stability?
4. Can international institutions (like the UN) promote peace?

### 🤔 Theoretical Framework

**Modified Prisoner's Dilemma with Multiple Players**:
- Nations can choose **Peace** or **Conflict**
- Cooperation (peace) benefits everyone
- Defection (conflict) can benefit individual nations in the short run
- **Reputation** matters in repeated interactions
- **Alliances** provide security guarantees

**Key Insight**: International cooperation is sustained through repeated interaction, reputation, and the threat of retaliation.

### 🛠️ Implementation

```python
class InternationalDiplomacy:
    """
    Simulates international relations with multiple nations.
    """
    
    def __init__(self, 
                 num_nations=5,
                 power_distribution='random',
                 conflict_cost=0.6,
                 trade_benefit=0.4,
                 alliance_strength=0.3):
        """
        Initialize the international system.
        
        Parameters:
        num_nations: Number of nations
        power_distribution: 'random', 'equal', or 'hegemonic'
        conflict_cost: Cost of conflict as fraction of GDP
        trade_benefit: Benefit of trade as fraction of GDP
        alliance_strength: Bonus for alliance cooperation
        """
        self.num_nations = num_nations
        self.conflict_cost = conflict_cost
        self.trade_benefit = trade_benefit
        self.alliance_strength = alliance_strength
        
        # Initialize nation characteristics
        self.nation_names = [f'Nation {chr(65+i)}' for i in range(num_nations)]
        
        # GDP (economic strength)
        if power_distribution == 'equal':
            self.gdp = np.ones(num_nations) * 100
        elif power_distribution == 'hegemonic':
            self.gdp = np.array([200] + [50] * (num_nations - 1))
        else:  # random
            self.gdp = np.random.uniform(30, 150, num_nations)
        
        # Military power (correlated with GDP)
        self.military = self.gdp * np.random.uniform(0.1, 0.3, num_nations)
        
        # Relationships matrix (cooperation level between nations)
        self.relations = np.random.uniform(-1, 1, (num_nations, num_nations))
        np.fill_diagonal(self.relations, 0)  # No self-relations
        
        # Alliances (binary matrix)
        self.alliances = np.zeros((num_nations, num_nations), dtype=bool)
        
        # Trade flows
        self.trade = np.random.uniform(1, 10, (num_nations, num_nations))
        np.fill_diagonal(self.trade, 0)
        
        # History
        self.history = {
            'gdp': [self.gdp.copy()],
            'military': [self.military.copy()],
            'relations': [self.relations.copy()],
            'alliances': [self.alliances.copy()],
            'trade': [self.trade.copy()],
            'conflicts': [],
            'peace_level': []
        }
        
        # Initialize peace index
        self._update_peace_index()
    
    def _update_peace_index(self):
        """Calculate the global peace index"""
        # Average of all relations
        n = self.num_nations
        avg_relation = np.sum(self.relations) / (n * (n-1))
        self.peace_index = max(0, (avg_relation + 1) / 2)
        self.history['peace_level'].append(self.peace_index)
    
    def _calculate_nation_utility(self, nation_idx, strategies):
        """
        Calculate utility for a nation given its strategy choices.
        Strategies: [cooperate_peace, cooperate_trade, form_alliance]
        """
        utility = 0
        
        # Economic utility from GDP
        utility += self.gdp[nation_idx] / 100
        
        # Trade utility
        for j in range(self.num_nations):
            if j != nation_idx:
                if strategies.get('trade', True):
                    utility += self.trade[nation_idx, j] * self.trade_benefit
                else:
                    utility -= self.trade[nation_idx, j] * 0.1  # Trade barriers
        
        # Alliance utility
        if strategies.get('alliance', False):
            utility += self.alliance_strength * np.sum(self.alliances[nation_idx])
        
        # Peace utility
        if strategies.get('peace', True):
            utility += 0.5 * self.peace_index
        else:
            # Conflict utility (may increase GDP but costs military)
            utility += 0.2 - self.conflict_cost * (self.military[nation_idx] / 100)
        
        return utility
    
    def update_relations(self, learning_rate=0.1):
        """
        Update relations between nations based on interactions.
        """
        # Randomly select two nations to interact
        nations = np.random.choice(self.num_nations, 2, replace=False)
        i, j = nations
        
        # Probability of cooperation depends on current relations
        cooperation_prob = (self.relations[i, j] + 1) / 2
        
        # Decide actions
        i_cooperates = np.random.random() < cooperation_prob
        j_cooperates = np.random.random() < cooperation_prob
        
        # Update relations based on actions
        if i_cooperates and j_cooperates:
            # Mutual cooperation - relations improve
            self.relations[i, j] += learning_rate * 0.5
            self.relations[j, i] += learning_rate * 0.5
            self.trade[i, j] *= 1.05
            self.trade[j, i] *= 1.05
        elif i_cooperates and not j_cooperates:
            # i cooperates, j defects - relations worsen
            self.relations[i, j] -= learning_rate * 0.3
            self.relations[j, i] -= learning_rate * 0.3
        elif not i_cooperates and j_cooperates:
            # i defects, j cooperates - relations worsen
            self.relations[i, j] -= learning_rate * 0.3
            self.relations[j, i] -= learning_rate * 0.3
        else:  # both defect
            self.relations[i, j] -= learning_rate * 0.1
            self.relations[j, i] -= learning_rate * 0.1
        
        # Clamp relations to [-1, 1]
        self.relations = np.clip(self.relations, -1, 1)
    
    def update_alliances(self, threshold=0.5):
        """
        Update alliances based on relations and power.
        Nations with positive relations tend to form alliances.
        """
        for i in range(self.num_nations):
            for j in range(self.num_nations):
                if i != j:
                    # Probability of alliance based on relations and power
                    relation_score = (self.relations[i, j] + 1) / 2
                    
                    # Power balance - nations with similar power more likely to ally
                    power_balance = 1 - abs(self.military[i] - self.military[j]) / max(self.military)
                    
                    # Alliance probability
                    alliance_prob = (relation_score + power_balance) / 2
                    
                    # Form or break alliance based on probability
                    self.alliances[i, j] = np.random.random() < alliance_prob * threshold
        
        # Make alliances symmetric
        self.alliances = np.logical_or(self.alliances, self.alliances.T)
    
    def simulate_conflict(self):
        """
        Simulate potential conflicts between nations.
        Conflicts occur between nations with poor relations.
        """
        conflicts = []
        
        for i in range(self.num_nations):
            for j in range(i + 1, self.num_nations):
                # Probability of conflict inversely related to relations
                conflict_prob = max(0, -self.relations[i, j])
                
                if np.random.random() < conflict_prob * 0.3:
                    # Conflict occurs
                    conflict_strength = self.military[i] / (self.military[i] + self.military[j])
                    
                    # Costs of conflict
                    self.gdp[i] *= (1 - self.conflict_cost * 0.5 * (1 - conflict_strength))
                    self.gdp[j] *= (1 - self.conflict_cost * 0.5 * conflict_strength)
                    
                    # Relations worsen
                    self.relations[i, j] -= 0.3
                    self.relations[j, i] -= 0.3
                    
                    conflicts.append((i, j, conflict_strength))
        
        self.history['conflicts'].append(conflicts)
        return conflicts
    
    def update_economies(self):
        """
        Update economies based on trade and relations.
        """
        # Economic growth based on trade and peace
        for i in range(self.num_nations):
            # Growth from trade
            total_trade = np.sum(self.trade[i])
            trade_growth = total_trade / 1000
            
            # Growth from peace
            peace_growth = self.peace_index * 0.05
            
            # Growth from GDP
            base_growth = 0.02
            
            # Apply growth
            self.gdp[i] *= (1 + base_growth + trade_growth + peace_growth)
            
            # Update military proportional to GDP
            self.military[i] = self.gdp[i] * 0.2
    
    def step(self, learning_rate=0.1):
        """One simulation step"""
        # Update relations and alliances
        self.update_relations(learning_rate)
        self.update_alliances()
        
        # Simulate conflicts
        conflicts = self.simulate_conflict()
        
        # Update economies
        self.update_economies()
        
        # Update peace index
        self._update_peace_index()
        
        # Record history
        self.history['gdp'].append(self.gdp.copy())
        self.history['military'].append(self.military.copy())
        self.history['relations'].append(self.relations.copy())
        self.history['alliances'].append(self.alliances.copy())
        self.history['trade'].append(self.trade.copy())
    
    def simulate(self, num_steps=100, learning_rate=0.1):
        """Run simulation for multiple steps"""
        for _ in range(num_steps):
            self.step(learning_rate)
    
    def plot_diplomacy(self):
        """Visualize international diplomacy dynamics"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        
        time = np.arange(len(self.history['gdp']))
        
        # Plot 1: GDP over time
        for i in range(self.num_nations):
            gdp_history = [g[i] for g in self.history['gdp']]
            axes[0, 0].plot(time, gdp_history, 
                          label=self.nation_names[i], linewidth=2)
        axes[0, 0].set_xlabel('Time')
        axes[0, 0].set_ylabel('GDP')
        axes[0, 0].set_title('National GDP Over Time')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Peace index over time
        peace_levels = self.history['peace_level']
        axes[0, 1].plot(time, peace_levels, 'go-', linewidth=2, markersize=8)
        axes[0, 1].set_xlabel('Time')
        axes[0, 1].set_ylabel('Peace Index')
        axes[0, 1].set_title('Global Peace Index')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Add reference lines
        axes[0, 1].axhline(y=0.5, color='orange', linestyle='--', alpha=0.7, label='Neutral')
        axes[0, 1].axhline(y=0.7, color='green', linestyle='--', alpha=0.7, label='Peaceful')
        axes[0, 1].axhline(y=0.3, color='red', linestyle='--', alpha=0.7, label='Conflict')
        axes[0, 1].legend()
        
        # Plot 3: Alliances over time (heatmap at final time)
        final_alliances = self.history['alliances'][-1]
        axes[1, 0].imshow(final_alliances, cmap='Blues', interpolation='nearest')
        axes[1, 0].set_xticks(range(self.num_nations))
        axes[1, 0].set_yticks(range(self.num_nations))
        axes[1, 0].set_xticklabels(self.nation_names)
        axes[1, 0].set_yticklabels(self.nation_names)
        axes[1, 0].set_title('Final Alliance Structure')
        axes[1, 0].set_xlabel('Nation')
        axes[1, 0].set_ylabel('Nation')
        
        # Plot 4: Conflict history
        conflict_history = self.history['conflicts']
        if conflict_history:
            conflict_counts = []
            for conflicts in conflict_history:
                conflict_counts.append(len(conflicts))
            
            axes[1, 1].bar(range(len(conflict_counts)), conflict_counts, 
                          color='red', alpha=0.7)
            axes[1, 1].set_xlabel('Time')
            axes[1, 1].set_ylabel('Number of Conflicts')
            axes[1, 1].set_title('Conflict Frequency Over Time')
            axes[1, 1].grid(True, alpha=0.3)
        else:
            axes[1, 1].text(0.5, 0.5, 'No conflicts occurred', 
                           ha='center', va='center', transform=axes[1, 1].transAxes,
                           fontsize=14)
            axes[1, 1].set_title('Conflict History')
        
        plt.tight_layout()
        plt.show()
    
    def analyze_diplomacy(self):
        """Analyze the international system"""
        print("\n🌍 International Diplomacy Analysis")
        print("=" * 70)
        print(f"Number of Nations: {self.num_nations}")
        print(f"Current Peace Index: {self.peace_index:.3f}")
        print("-" * 70)
        
        # Analyze alliance structure
        final_alliances = self.history['alliances'][-1]
        alliance_counts = np.sum(final_alliances, axis=0)
        
        print("\n📊 Nation Status:")
        for i in range(self.num_nations):
            print(f"  {self.nation_names[i]}: GDP={self.gdp[i]:.1f}, "
                  f"Military={self.military[i]:.1f}, "
                  f"Alliances={alliance_counts[i]:.0f}")
        
        # Identify power blocks
        if np.any(final_alliances):
            G = nx.Graph()
            for i in range(self.num_nations):
                G.add_node(i)
                for j in range(i + 1, self.num_nations):
                    if final_alliances[i, j]:
                        G.add_edge(i, j)
            
            components = list(nx.connected_components(G))
            print(f"\n🤝 Power Blocks: {len(components)}")
            for idx, comp in enumerate(components):
                nations = [self.nation_names[i] for i in comp]
                print(f"  Block {idx+1}: {', '.join(nations)}")
        
        # Conflict analysis
        total_conflicts = sum(len(conflicts) for conflicts in self.history['conflicts'])
        print(f"\n⚔️ Total Conflicts: {total_conflicts}")
        
        # Calculate stability metrics
        gdp_volatility = np.std([g[0] for g in self.history['gdp']])
        print(f"📈 GDP Volatility: {gdp_volatility:.2f}")
        
        return {
            'peace_index': self.peace_index,
            'total_conflicts': total_conflicts,
            'gdp_volatility': gdp_volatility,
            'alliance_structure': final_alliances
        }

# Run diplomacy simulation
print("🌍 International Diplomacy Simulation")
print("=" * 70)

# Create and simulate
diplomacy = InternationalDiplomacy(
    num_nations=6,
    power_distribution='random',
    conflict_cost=0.5,
    trade_benefit=0.3,
    alliance_strength=0.4
)

diplomacy.simulate(num_steps=100, learning_rate=0.1)
diplomacy.plot_diplomacy()
diplomacy.analyze_diplomacy()
```

### 📊 Power Distribution Analysis

```python
def power_distribution_analysis():
    """Analyze how power distribution affects international stability"""
    
    distributions = ['equal', 'random', 'hegemonic']
    results = []
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for idx, dist in enumerate(distributions):
        diplomacy = InternationalDiplomacy(
            num_nations=6,
            power_distribution=dist,
            conflict_cost=0.5,
            trade_benefit=0.3,
            alliance_strength=0.4
        )
        diplomacy.simulate(num_steps=80)
        
        # Plot peace index
        peace_levels = diplomacy.history['peace_level']
        axes[idx].plot(peace_levels, label='Peace Index', linewidth=2)
        axes[idx].axhline(y=0.5, color='orange', linestyle='--', alpha=0.5)
        axes[idx].set_xlabel('Time')
        axes[idx].set_ylabel('Peace Index')
        axes[idx].set_title(f'Power Distribution: {dist.capitalize()}')
        axes[idx].grid(True, alpha=0.3)
        
        # Calculate metrics
        avg_peace = np.mean(peace_levels[-20:])  # Average of last 20 periods
        total_conflicts = sum(len(c) for c in diplomacy.history['conflicts'])
        results.append({
            'distribution': dist,
            'avg_peace': avg_peace,
            'total_conflicts': total_conflicts,
            'final_peace': peace_levels[-1]
        })
    
    plt.tight_layout()
    plt.show()
    
    # Print comparison
    print("\n📊 Power Distribution Comparison")
    print("=" * 70)
    df = pd.DataFrame(results)
    print(df)
    print("\n💡 Insights:")
    print("  - Equal power distribution tends to be most stable")
    print("  - Hegemonic systems can be stable if the hegemon is benevolent")
    print("  - Random distributions create uncertainty and conflict")

# Run analysis
power_distribution_analysis()
```

---

# PROJECT 5: Evolutionary Cooperation Model

### 📖 Problem Statement

**Scenario**: A population of individuals evolves over time. Each individual:
- Has a **strategy** (cooperate, defect, or conditionally cooperate)
- Receives **payoffs** from interactions
- Reproduces based on **fitness** (payoff)
- Can **learn** and change strategies

**Key Questions**:
1. How does cooperation emerge in a population?
2. What conditions favor cooperation?
3. How do punishment and reward affect cooperation?
4. What strategies are evolutionarily stable?

### 🤔 Theoretical Framework

**Replicator Dynamics with Spatial Structure**:
- Individuals play games with neighbors
- Payoffs determine reproductive success
- **Kin selection**: Related individuals cooperate more
- **Reciprocal altruism**: Repeated interactions promote cooperation
- **Group selection**: Groups with more cooperation succeed

**Key Insight**: Cooperation can evolve through multiple mechanisms despite individual incentives to defect.

### 🛠️ Implementation

```python
class EvolutionaryCooperation:
    """
    Simulates evolution of cooperation in a population.
    """
    
    def __init__(self, 
                 population_size=100,
                 grid_size=10,
                 game_type='prisoners_dilemma',
                 payoff_cooperation=3,
                 payoff_defection=5,
                 payoff_temptation=0,
                 payoff_penalty=1,
                 mutation_rate=0.01,
                 reproduction_rate=0.5,
                 death_rate=0.3):
        """
        Initialize evolutionary cooperation model.
        
        Parameters:
        population_size: Total population size
        grid_size: Size of spatial grid (sqrt of population)
        game_type: 'prisoners_dilemma' or 'public_goods'
        payoff_cooperation: Payoff when both cooperate
        payoff_defection: Payoff when both defect
        payoff_temptation: Payoff when defecting against cooperator
        payoff_penalty: Payoff when cooperating against defector
        mutation_rate: Probability of strategy mutation
        reproduction_rate: Rate of reproduction
        death_rate: Rate of death
        """
        self.population_size = population_size
        self.grid_size = grid_size
        self.game_type = game_type
        self.mutation_rate = mutation_rate
        self.reproduction_rate = reproduction_rate
        self.death_rate = death_rate
        
        # Payoff parameters
        self.R = payoff_cooperation  # Reward for mutual cooperation
        self.T = payoff_defection    # Temptation to defect
        self.S = payoff_penalty      # Sucker's payoff
        self.P = payoff_temptation   # Punishment for mutual defection
        
        # Initialize population on a grid
        self.grid = np.zeros((grid_size, grid_size), dtype=int)
        self.strategies = ['C', 'D', 'TFT', 'GRUDGER', 'RANDOM']
        
        # Assign initial strategies
        self.population = np.random.choice(
            len(self.strategies), 
            (grid_size, grid_size),
            p=[0.3, 0.2, 0.2, 0.15, 0.15]  # Initial distribution
        )
        
        # Track strategy counts
        self.strategy_counts = defaultdict(int)
        self._update_counts()
        
        # History
        self.history = {
            'strategy_counts': [dict(self.strategy_counts)],
            'cooperation_rate': [self.calculate_cooperation_rate()],
            'average_payoff': [],
            'diversity': []
        }
        
        # Payoff matrix
        self.payoffs = self._create_payoff_matrix()
    
    def _create_payoff_matrix(self):
        """Create payoff matrix for different strategy combinations"""
        # Strategies: C, D, TFT, GRUDGER, RANDOM
        # C = Cooperate, D = Defect, TFT = Tit-for-Tat, GRUDGER = Grudger, RANDOM = Random
        
        # Simplified payoff matrix for Prisoner's Dilemma
        payoffs = np.zeros((len(self.strategies), len(self.strategies)))
        
        for i, s1 in enumerate(self.strategies):
            for j, s2 in enumerate(self.strategies):
                # Determine actual moves for each strategy
                move1 = self._get_move(s1, s2)
                move2 = self._get_move(s2, s1)
                
                if move1 == 'C' and move2 == 'C':
                    payoffs[i, j] = self.R
                elif move1 == 'D' and move2 == 'D':
                    payoffs[i, j] = self.P
                elif move1 == 'C' and move2 == 'D':
                    payoffs[i, j] = self.S
                else:  # move1 == 'D' and move2 == 'C'
                    payoffs[i, j] = self.T
        
        return payoffs
    
    def _get_move(self, strategy, opponent_strategy):
        """Get actual move based on strategy type"""
        if strategy == 0:  # C - Always cooperate
            return 'C'
        elif strategy == 1:  # D - Always defect
            return 'D'
        elif strategy == 2:  # TFT - Tit-for-Tat
            # First move: cooperate, then mirror opponent's last move
            return 'C'  # Simplified - assume first move is cooperate
        elif strategy == 3:  # GRUDGER - Cooperate until opponent defects
            return 'C'
        else:  # RANDOM
            return 'C' if np.random.random() < 0.5 else 'D'
    
    def _update_counts(self):
        """Update strategy counts"""
        counts = np.zeros(len(self.strategies))
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                counts[self.population[i, j]] += 1
        self.strategy_counts = {self.strategies[k]: v for k, v in enumerate(counts)}
    
    def calculate_cooperation_rate(self):
        """Calculate the cooperation rate in the population"""
        # C = 0, TFT = 2, GRUDGER = 3 cooperate
        cooperators = np.sum((self.population == 0) | 
                             (self.population == 2) | 
                             (self.population == 3))
        return cooperators / self.population_size
    
    def get_neighbors(self, x, y):
        """Get the 8 neighbors of a cell"""
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = (x + dx) % self.grid_size, (y + dy) % self.grid_size
                neighbors.append((nx, ny))
        return neighbors
    
    def calculate_payoff(self, x, y):
        """Calculate payoff for an individual based on interactions with neighbors"""
        strategy = self.population[x, y]
        total_payoff = 0
        neighbors = self.get_neighbors(x, y)
        
        for nx, ny in neighbors:
            neighbor_strategy = self.population[nx, ny]
            total_payoff += self.payoffs[strategy, neighbor_strategy]
        
        return total_payoff / len(neighbors)
    
    def step(self):
        """One evolutionary step"""
        # Calculate payoffs for all individuals
        payoffs = np.zeros((self.grid_size, self.grid_size))
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                payoffs[i, j] = self.calculate_payoff(i, j)
        
        # Reproduction and death
        new_population = self.population.copy()
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                # Probability of death
                if np.random.random() < self.death_rate:
                    # Find a neighbor with high payoff to reproduce
                    neighbors = self.get_neighbors(i, j)
                    neighbor_payoffs = [payoffs[nx, ny] for nx, ny in neighbors]
                    
                    if neighbor_payoffs:
                        # Roulette wheel selection based on payoff
                        total_payoff = sum(neighbor_payoffs) + 1  # Avoid division by zero
                        probabilities = [(p + 1) / total_payoff for p in neighbor_payoffs]
                        selected = np.random.choice(len(neighbors), p=probabilities)
                        nx, ny = neighbors[selected]
                        
                        # Reproduce with mutation
                        child_strategy = self.population[nx, ny]
                        if np.random.random() < self.mutation_rate:
                            child_strategy = np.random.randint(len(self.strategies))
                        
                        new_population[i, j] = child_strategy
        
        self.population = new_population
        
        # Update history
        self._update_counts()
        self.history['strategy_counts'].append(dict(self.strategy_counts))
        self.history['cooperation_rate'].append(self.calculate_cooperation_rate())
        self.history['average_payoff'].append(np.mean(payoffs))
        self.history['diversity'].append(len([c for c in self.strategy_counts.values() if c > 0]))
    
    def simulate(self, num_steps=100):
        """Run simulation for multiple steps"""
        for _ in range(num_steps):
            self.step()
    
    def plot_evolution(self):
        """Visualize evolutionary dynamics"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        
        time = np.arange(len(self.history['cooperation_rate']))
        
        # Plot 1: Cooperation rate over time
        axes[0, 0].plot(time, self.history['cooperation_rate'], 
                       'go-', linewidth=2, markersize=4)
        axes[0, 0].axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='50% Threshold')
        axes[0, 0].set_xlabel('Time')
        axes[0, 0].set_ylabel('Cooperation Rate')
        axes[0, 0].set_title('Evolution of Cooperation')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].set_ylim(0, 1.05)
        
        # Plot 2: Strategy composition over time
        strategy_history = {s: [] for s in self.strategies}
        for t in range(len(self.history['strategy_counts'])):
            counts = self.history['strategy_counts'][t]
            for s in self.strategies:
                strategy_history[s].append(counts.get(s, 0) / self.population_size)
        
        for s in self.strategies:
            axes[0, 1].plot(time, strategy_history[s], 
                          label=s, linewidth=2)
        axes[0, 1].set_xlabel('Time')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].set_title('Strategy Frequencies Over Time')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Spatial distribution at final time
        final_pop = self.population
        cmap = plt.cm.Set3
        axes[1, 0].imshow(final_pop, cmap=cmap, interpolation='nearest')
        axes[1, 0].set_title('Final Spatial Distribution')
        axes[1, 0].set_xlabel('Grid X')
        axes[1, 0].set_ylabel('Grid Y')
        
        # Add colorbar with strategy labels
        cbar = plt.colorbar(axes[1, 0].imshow(final_pop, cmap=cmap, interpolation='nearest'), 
                           ax=axes[1, 0])
        cbar.set_ticks(range(len(self.strategies)))
        cbar.set_ticklabels(self.strategies)
        
        # Plot 4: Diversity over time
        axes[1, 1].plot(time, self.history['diversity'], 
                       'bo-', linewidth=2, markersize=4)
        axes[1, 1].axhline(y=len(self.strategies), color='red', linestyle='--', 
                          alpha=0.5, label=f'Maximum ({len(self.strategies)})')
        axes[1, 1].set_xlabel('Time')
        axes[1, 1].set_ylabel('Number of Strategies')
        axes[1, 1].set_title('Strategic Diversity')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def analyze_evolution(self):
        """Analyze evolutionary outcomes"""
        print("\n🧬 Evolutionary Cooperation Analysis")
        print("=" * 70)
        print(f"Population Size: {self.population_size}")
        print(f"Game Type: {self.game_type}")
        print(f"Mutation Rate: {self.mutation_rate:.3f}")
        print("-" * 70)
        
        # Final strategy distribution
        final_counts = self.history['strategy_counts'][-1]
        total = sum(final_counts.values())
        
        print("\n📊 Final Strategy Distribution:")
        for strategy in self.strategies:
            count = final_counts.get(strategy, 0)
            pct = count / total * 100
            print(f"  {strategy}: {pct:.1f}% ({count:.0f})")
        
        # Cooperation analysis
        final_cooperation = self.history['cooperation_rate'][-1]
        avg_cooperation = np.mean(self.history['cooperation_rate'])
        
        print(f"\n🤝 Cooperation Rates:")
        print(f"  Final Cooperation Rate: {final_cooperation:.1%}")
        print(f"  Average Cooperation Rate: {avg_cooperation:.1%}")
        
        # Stability analysis
        if len(self.history['cooperation_rate']) > 20:
            recent_coop = self.history['cooperation_rate'][-20:]
            stability = np.std(recent_coop)
            print(f"  Stability (Std Dev of last 20): {stability:.3f}")
        
        # Diversity analysis
        final_diversity = self.history['diversity'][-1]
        avg_diversity = np.mean(self.history['diversity'])
        
        print(f"\n🎯 Diversity:")
        print(f"  Final Diversity: {final_diversity:.0f} strategies")
        print(f"  Average Diversity: {avg_diversity:.1f} strategies")
        
        # Identify dominant strategy
        dominant = max(final_counts.items(), key=lambda x: x[1])
        print(f"\n🏆 Dominant Strategy: {dominant[0]} ({dominant[1]/total:.1%})")
        
        return {
            'final_cooperation': final_cooperation,
            'avg_cooperation': avg_cooperation,
            'final_diversity': final_diversity,
            'dominant_strategy': dominant[0]
        }
    
    def animate_evolution(self):
        """Create an animation of the evolution (requires matplotlib animation)"""
        from matplotlib.animation import FuncAnimation
        
        fig, ax = plt.subplots(figsize=(8, 8))
        
        def update(frame):
            ax.clear()
            ax.imshow(self.population_history[frame], cmap='Set3', interpolation='nearest')
            ax.set_title(f'Generation {frame}')
            ax.set_xlabel('Grid X')
            ax.set_ylabel('Grid Y')
        
        # Store population history
        self.population_history = []
        for i in range(len(self.history['strategy_counts'])):
            # Reconstruct population from history (simplified)
            self.population_history.append(self.population)
        
        anim = FuncAnimation(fig, update, frames=len(self.population_history), 
                           interval=200, repeat=True)
        return anim

# Run evolutionary cooperation simulation
print("🧬 Evolutionary Cooperation Simulation")
print("=" * 70)

# Create and simulate
evo = EvolutionaryCooperation(
    population_size=100,
    grid_size=10,
    game_type='prisoners_dilemma',
    payoff_cooperation=3,
    payoff_defection=5,
    payoff_penalty=0,
    payoff_temptation=1,
    mutation_rate=0.02,
    reproduction_rate=0.5,
    death_rate=0.3
)

evo.simulate(num_steps=100)
evo.plot_evolution()
evo.analyze_evolution()
```

### 📊 Parameter Sensitivity Analysis

```python
def parameter_sensitivity_analysis():
    """Analyze how parameters affect cooperation outcomes"""
    
    # Test different parameters
    parameters = {
        'mutation_rate': [0.001, 0.01, 0.05, 0.1],
        'death_rate': [0.1, 0.3, 0.5, 0.7],
        'payoff_cooperation': [2, 3, 4, 5]
    }
    
    results = []
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for idx, (param_name, values) in enumerate(parameters.items()):
        for value in values:
            # Create simulation with different parameter
            kwargs = {
                'population_size': 100,
                'grid_size': 10,
                'game_type': 'prisoners_dilemma',
                'mutation_rate': 0.02,
                'death_rate': 0.3,
                'payoff_cooperation': 3,
                'payoff_defection': 5,
                'payoff_penalty': 0,
                'payoff_temptation': 1
            }
            
            if param_name == 'mutation_rate':
                kwargs['mutation_rate'] = value
            elif param_name == 'death_rate':
                kwargs['death_rate'] = value
            elif param_name == 'payoff_cooperation':
                kwargs['payoff_cooperation'] = value
            
            evo = EvolutionaryCooperation(**kwargs)
            evo.simulate(num_steps=80)
            
            # Calculate metrics
            final_coop = evo.history['cooperation_rate'][-1]
            avg_coop = np.mean(evo.history['cooperation_rate'])
            
            results.append({
                'parameter': param_name,
                'value': value,
                'final_cooperation': final_coop,
                'avg_cooperation': avg_coop
            })
        
        # Plot for this parameter
        param_results = [r for r in results if r['parameter'] == param_name]
        x_vals = [r['value'] for r in param_results]
        y_final = [r['final_cooperation'] for r in param_results]
        y_avg = [r['avg_cooperation'] for r in param_results]
        
        axes[idx].plot(x_vals, y_final, 'bo-', label='Final Cooperation', linewidth=2, markersize=8)
        axes[idx].plot(x_vals, y_avg, 'ro-', label='Average Cooperation', linewidth=2, markersize=8)
        axes[idx].set_xlabel(param_name)
        axes[idx].set_ylabel('Cooperation Rate')
        axes[idx].set_title(f'Effect of {param_name}')
        axes[idx].legend()
        axes[idx].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Print insights
    print("\n📊 Parameter Sensitivity Insights")
    print("=" * 70)
    df = pd.DataFrame(results)
    
    for param in parameters.keys():
        param_df = df[df['parameter'] == param]
        print(f"\n{param}:")
        print(f"  Best value: {param_df.loc[param_df['avg_cooperation'].idxmax(), 'value']}")
        print(f"  Range of cooperation rates: {param_df['avg_cooperation'].min():.3f} to {param_df['avg_cooperation'].max():.3f}")

# Run sensitivity analysis
parameter_sensitivity_analysis()
```

---

# 🎓 Final Summary

```python
def final_summary():
    """Summarize all five projects"""
    
    print("=" * 70)
    print("🎯 GAME THEORY FINAL PROJECTS SUMMARY")
    print("=" * 70)
    
    projects = [
        {
            'name': 'Market Competition with Multiple Firms',
            'key_concepts': ['Cournot competition', 'Nash equilibrium', 'Market concentration', 'Efficiency'],
            'applications': ['Antitrust analysis', 'Industrial organization', 'Regulatory policy'],
            'python_features': ['NumPy vectorization', 'Interactive plotting', 'Sensitivity analysis']
        },
        {
            'name': 'Political Campaign Strategy',
            'key_concepts': ['Spatial competition', 'Median voter theorem', 'Campaign spending', 'Voter behavior'],
            'applications': ['Election strategy', 'Political consulting', 'Public opinion analysis'],
            'python_features': ['Monte Carlo simulation', 'Voter distribution modeling', 'Time series analysis']
        },
        {
            'name': 'Supply Chain Negotiation',
            'key_concepts': ['Bargaining power', 'Double marginalization', 'Vertical relationships', 'Network structure'],
            'applications': ['Supply chain management', 'Procurement strategy', 'Vertical integration'],
            'python_features': ['Network analysis', 'Game theory with bargaining', 'Visualization of complex systems']
        },
        {
            'name': 'International Diplomacy Game',
            'key_concepts': ['Alliance formation', 'Conflict resolution', 'Power dynamics', 'International cooperation'],
            'applications': ['International relations', 'Diplomacy simulation', 'Peace studies'],
            'python_features': ['Agent-based modeling', 'Multi-agent systems', 'Dynamic relationship modeling']
        },
        {
            'name': 'Evolutionary Cooperation Model',
            'key_concepts': ['Replicator dynamics', 'Cooperation emergence', 'Spatial structure', 'Strategy evolution'],
            'applications': ['Evolutionary biology', 'Social norms', 'Organizational behavior'],
            'python_features': ['Grid-based simulation', 'Evolutionary algorithms', 'Spatial visualization']
        }
    ]
    
    for i, proj in enumerate(projects, 1):
        print(f"\n📁 Project {i}: {proj['name']}")
        print("-" * 60)
        print(f"Key Concepts: {', '.join(proj['key_concepts'])}")
        print(f"Applications: {', '.join(proj['applications'])}")
        print(f"Python Features: {', '.join(proj['python_features'])}")
    
    print("\n" + "=" * 70)
    print("💡 KEY INSIGHTS ACROSS ALL PROJECTS")
    print("=" * 70)
    print("1. Strategic behavior depends on the structure of the game")
    print("2. Cooperation is fragile but can emerge under certain conditions")
    print("3. Power imbalances affect outcomes in predictable ways")
    print("4. Repeated interactions promote cooperation and stability")
    print("5. Monte Carlo simulation helps handle uncertainty in strategic games")
    print("6. Python provides powerful tools for game theory analysis")
    
    print("\n🚀 NEXT STEPS")
    print("-" * 70)
    print("1. Extend models with more realistic assumptions")
    print("2. Integrate machine learning for strategy optimization")
    print("3. Scale to larger populations using parallel computing")
    print("4. Add interactive visualizations with Plotly")
    print("5. Connect to real-world data for validation")

# Run final summary
final_summary()
```

---

## 📚 How to Use These Projects in Jupyter

1. **Create a new Jupyter notebook** for each project
2. **Copy the code** into code cells
3. **Run cells sequentially** to see results
4. **Experiment with parameters** using sliders or interactive widgets
5. **Modify the models** to test your own hypotheses
6. **Save visualizations** for reports or presentations

### Interactive Widget Example

```python
from ipywidgets import interact, widgets

@interact(
    num_firms=widgets.IntSlider(min=2, max=20, step=1, value=5),
    demand_slope=widgets.FloatSlider(min=0.1, max=2, step=0.1, value=0.5),
    learning_rate=widgets.FloatSlider(min=0.1, max=0.9, step=0.1, value=0.3)
)
def interactive_market(num_firms, demand_slope, learning_rate):
    market = MultiFirmMarket(
        num_firms=num_firms,
        demand_intercept=100,
        demand_slope=demand_slope,
        marginal_cost=10,
        fixed_cost=5
    )
    market.simulate(num_steps=50, learning_rate=learning_rate)
    market.plot_market_analysis()
```

---

## 📚 Recommended Extensions

1. **Add interactive widgets** using `ipywidgets`
2. **Create animated visualizations** using `matplotlib.animation`
3. **Export results** to CSV or Excel for further analysis
4. **Build a web dashboard** using Streamlit or Dash
5. **Implement reinforcement learning** for strategy adaptation
6. **Connect to real data** for empirical validation

---

## 🏆 Final Thoughts

These five projects demonstrate the power of combining **game theory** with **computational simulation**. Each project provides a complete framework for analyzing strategic situations, from market competition to international relations to evolutionary dynamics.

The Python implementations are designed to be:
- **Modular**: Easy to extend and modify
- **Visual**: Clear visualizations for understanding dynamics
- **Educational**: Well-commented code explaining key concepts
- **Practical**: Relevant to real-world applications

---

## 📖 References & Further Reading

1. **"Strategy: An Introduction to Game Theory"** - Joel Watson
2. **"Games of Strategy"** - Dixit, Skeath, Reiley
3. **"Theory of Games and Economic Behavior"** - von Neumann & Morgenstern
4. **"Evolutionary Game Theory"** - Jörgen Weibull
5. **"Industrial Organization: Theory and Applications"** - Oz Shy

---

**Happy simulating! 🎮**