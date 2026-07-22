# Jupyter Notebook: Market Competition with Multiple Firms -- deepseek-ai

```markdown
# Market Competition with Multiple Firms
## A Game Theory Simulation in Python

---

## 📖 Overview

This notebook simulates market competition with multiple firms using game theory. Firms compete either by choosing **quantities** (Cournot competition) or **prices** (Bertrand competition). The simulation shows how market outcomes evolve over time as firms adjust their strategies.

### Key Concepts Covered:
- Cournot and Bertrand competition
- Nash equilibrium in oligopoly
- Market concentration (Herfindahl-Hirschman Index)
- Consumer surplus and deadweight loss
- Strategic adjustment dynamics

---

## 📚 Setup & Imports

```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

print("✅ All imports successful!")
print(f"NumPy version: {np.__version__}")
print(f"Pandas version: {pd.__version__}")
```

---

## 🏪 Class Definition: MultiFirmMarket

The `MultiFirmMarket` class simulates an oligopolistic market with multiple competing firms.

### Key Features:
- Supports both Cournot (quantity) and Bertrand (price) competition
- Tracks history of quantities, prices, and profits
- Calculates market concentration (HHI)
- Measures efficiency (consumer surplus, producer surplus, deadweight loss)
- Visualizes market dynamics

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
        -----------
        num_firms : int
            Number of firms in the market
        demand_intercept : float
            a in P = a - b*Q
        demand_slope : float
            b in P = a - b*Q
        marginal_cost : float
            Constant marginal cost
        fixed_cost : float
            Fixed cost per firm
        competition_type : str
            'cournot' or 'bertrand'
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
        """
        Best response quantity for Cournot competition.
        
        The best response for firm i is:
        q_i = (a - c - b * Q_{-i}) / (2 * b)
        """
        other_quantity = np.sum(self.quantities) - self.quantities[firm_index]
        br = (self.a - self.c - self.b * other_quantity) / (2 * self.b)
        return max(0, br)
    
    def _bertrand_best_response(self, firm_index):
        """
        Best response price for Bertrand competition.
        
        In Bertrand competition, firms undercut each other's prices
        until price equals marginal cost.
        """
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
        
        Parameters:
        -----------
        learning_rate : float
            Speed of adjustment (0 = no adjustment, 1 = full adjustment)
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
        """
        Run simulation for multiple steps.
        
        Parameters:
        -----------
        num_steps : int
            Number of simulation steps
        learning_rate : float
            Speed of adjustment
        """
        for _ in range(num_steps):
            self.step(learning_rate)
    
    def _calculate_concentration(self):
        """
        Calculate Herfindahl-Hirschman Index (HHI).
        
        HHI = sum of squared market shares * 10000
        - < 1500: Competitive
        - 1500-2500: Moderate concentration
        - > 2500: Highly concentrated
        """
        shares = self.quantities / np.sum(self.quantities)
        return np.sum(shares**2) * 10000
    
    def _calculate_efficiency(self):
        """
        Calculate market efficiency metrics.
        
        Returns:
        --------
        dict : Consumer surplus, producer surplus, deadweight loss, total surplus
        """
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
    
    def get_results(self):
        """Get final results of the simulation"""
        return {
            'quantities': self.quantities,
            'prices': self.prices,
            'profits': self.profits,
            'market_price': self.history['market_price'][-1],
            'total_quantity': self.history['total_quantity'][-1],
            'concentration': self._calculate_concentration(),
            'efficiency': self._calculate_efficiency()
        }
    
    def plot_evolution(self):
        """Plot the evolution of key variables over time"""
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
```

---

## 🚀 Run the Simulation

Now let's run the market simulation with default parameters:

```python
# Create and simulate market
market = MultiFirmMarket(
    num_firms=5,
    demand_intercept=100,
    demand_slope=0.5,
    marginal_cost=10,
    fixed_cost=5,
    competition_type='cournot'
)

print("🏪 Market Competition Simulation")
print("=" * 70)
print(f"Number of firms: {market.num_firms}")
print(f"Competition type: {market.competition_type.capitalize()}")
print(f"Demand: P = {market.a} - {market.b} * Q")
print(f"Marginal cost: {market.c}")
print(f"Fixed cost: {market.f}")
print("=" * 70)

# Simulate
market.simulate(num_steps=100, learning_rate=0.3)
```

---

## 📊 Visualize Results

### Evolution Over Time

```python
# Plot the evolution of key variables
market.plot_evolution()
```

### Market Analysis

```python
# Plot comprehensive market analysis
market.plot_market_analysis()
```

---

## 🔬 Sensitivity Analysis

Now let's analyze how changing the number of firms affects market outcomes:

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
    
    print("\n📊 Sensitivity Analysis Results")
    print("=" * 60)
    print(df.round(2))
    
    return df

# Run sensitivity analysis
sensitivity_results = sensitivity_analysis()
```

---

## 🎯 Comparison: Cournot vs Bertrand Competition

Let's compare the outcomes under Cournot and Bertrand competition:

```python
def compare_competition_types():
    """Compare Cournot and Bertrand competition outcomes"""
    
    competition_types = ['cournot', 'bertrand']
    results = {}
    
    for comp_type in competition_types:
        market = MultiFirmMarket(
            num_firms=5,
            demand_intercept=100,
            demand_slope=0.5,
            marginal_cost=10,
            fixed_cost=5,
            competition_type=comp_type
        )
        market.simulate(num_steps=100, learning_rate=0.3)
        results[comp_type] = market.get_results()
    
    # Display comparison
    print("📊 Cournot vs Bertrand Competition")
    print("=" * 70)
    print(f"{'Metric':<25} | {'Cournot':<20} | {'Bertrand':<20}")
    print("-" * 70)
    
    metrics = [
        ('Market Price', 'market_price'),
        ('Total Quantity', 'total_quantity'),
        ('Total Profit', 'profits'),
        ('HHI', 'concentration')
    ]
    
    for label, key in metrics:
        if key == 'profits':
            cournot_val = np.sum(results['cournot'][key])
            bertrand_val = np.sum(results['bertrand'][key])
        else:
            cournot_val = results['cournot'][key]
            bertrand_val = results['bertrand'][key]
        
        print(f"{label:<25} | {cournot_val:<20.2f} | {bertrand_val:<20.2f}")
    
    print("\n💡 Key Insight:")
    print("  - Cournot competition yields higher prices and profits")
    print("  - Bertrand competition yields lower prices and higher quantities")
    print("  - Bertrand is more competitive and closer to perfect competition")

# Run comparison
compare_competition_types()
```

---

## 🚀 Extension: Heterogeneous Firms

Now let's extend the model to allow firms with different costs:

```python
class HeterogeneousMarket(MultiFirmMarket):
    """Market with firms that have different costs"""
    
    def __init__(self, costs, fixed_costs, *args, **kwargs):
        self.firm_costs = costs
        self.firm_fixed = fixed_costs
        super().__init__(num_firms=len(costs), *args, **kwargs)
        self.c = np.mean(costs)  # Average cost for equilibrium calculation
    
    def _cournot_best_response(self, firm_index):
        """Best response quantity with firm-specific costs"""
        other_quantity = np.sum(self.quantities) - self.quantities[firm_index]
        c_i = self.firm_costs[firm_index]
        br = (self.a - c_i - self.b * other_quantity) / (2 * self.b)
        return max(0, br)

# Run heterogeneous firm simulation
print("🏪 Heterogeneous Firms Competition")
print("=" * 70)

# Define firms with different costs
costs = [10, 12, 15, 8, 11]  # Different efficiencies
fixed_costs = [5, 7, 10, 3, 6]

hetero_market = HeterogeneousMarket(
    costs=costs,
    fixed_costs=fixed_costs,
    demand_intercept=100,
    demand_slope=0.5,
    competition_type='cournot'
)

hetero_market.simulate(num_steps=100, learning_rate=0.3)
hetero_market.plot_evolution()
hetero_market.plot_market_analysis()

print("\n📊 Heterogeneous Firms Analysis")
print("=" * 60)
print("Firm | Cost | Fixed Cost | Quantity | Profit | Market Share")
print("-" * 60)
total_q = np.sum(hetero_market.quantities)
for i in range(hetero_market.num_firms):
    share = hetero_market.quantities[i] / total_q * 100
    print(f"  {i+1}  | {hetero_market.firm_costs[i]:.1f}  | {hetero_market.firm_fixed[i]:.1f}    | "
          f"{hetero_market.quantities[i]:.2f}   | {hetero_market.profits[i]:.2f}  | {share:.1f}%")
```

---

## 🎮 Interactive Simulation

Create an interactive widget to explore how parameters affect outcomes:

```python
# Uncomment this cell if you have ipywidgets installed
# from ipywidgets import interact, widgets

# @interact(
#     num_firms=widgets.IntSlider(min=2, max=20, step=1, value=5),
#     demand_slope=widgets.FloatSlider(min=0.1, max=2, step=0.1, value=0.5),
#     marginal_cost=widgets.FloatSlider(min=5, max=20, step=1, value=10),
#     learning_rate=widgets.FloatSlider(min=0.1, max=0.9, step=0.1, value=0.3),
#     competition_type=widgets.Dropdown(options=['cournot', 'bertrand'], value='cournot')
# )
# def interactive_market(num_firms, demand_slope, marginal_cost, learning_rate, competition_type):
#     market = MultiFirmMarket(
#         num_firms=num_firms,
#         demand_intercept=100,
#         demand_slope=demand_slope,
#         marginal_cost=marginal_cost,
#         fixed_cost=5,
#         competition_type=competition_type
#     )
#     market.simulate(num_steps=50, learning_rate=learning_rate)
#     market.plot_market_analysis()
```

---

## 📚 Summary & Key Insights

```python
print("=" * 70)
print("🎯 KEY INSIGHTS FROM MARKET COMPETITION SIMULATION")
print("=" * 70)

print("\n1. Cournot vs Bertrand Competition:")
print("   • Cournot competition leads to higher prices and profits")
print("   • Bertrand competition leads to lower prices and higher quantities")
print("   • Bertrand is more competitive and closer to perfect competition")

print("\n2. Number of Firms Effect:")
print("   • More firms → lower prices, higher quantities")
print("   • More firms → lower profits per firm")
print("   • More firms → more competitive market")

print("\n3. Market Concentration:")
print("   • HHI measures market concentration")
print("   • HHI < 1500: Competitive market")
print("   • HHI 1500-2500: Moderate concentration")
print("   • HHI > 2500: Highly concentrated")

print("\n4. Efficiency:")
print("   • Total surplus = Consumer surplus + Producer surplus")
print("   • Deadweight loss occurs when price > marginal cost")
print("   • Competition reduces deadweight loss")

print("\n5. Heterogeneous Firms:")
print("   • More efficient firms (lower costs) gain market share")
print("   • Inefficient firms may be driven out of market")
print("   • Market structure reflects firm efficiency differences")

print("\n" + "=" * 70)
print("✅ Simulation Complete!")
```

---

## 🔧 Next Steps & Exercises

1. **Experiment with Parameters**: Try different demand slopes, costs, and numbers of firms
2. **Add Collusion**: Implement cartel behavior where firms coordinate
3. **Add Entry/Exit**: Allow firms to enter or exit the market
4. **Add Investment**: Allow firms to invest in cost reduction
5. **Add Uncertainty**: Add random shocks to demand or costs
6. **Connect to Real Data**: Use actual market data for parameters

---

## 📖 References

- Cournot, A. (1838). *Researches into the Mathematical Principles of the Theory of Wealth*
- Bertrand, J. (1883). *Review of Cournot's Theory*
- Tirole, J. (1988). *The Theory of Industrial Organization*
- Vives, X. (1999). *Oligopoly Pricing: Old Ideas and New Tools*

---

**Happy simulating! 🎮**
```

---

## Instructions to Use This Notebook

1. **Save the content** as a `.ipynb` file:
   - Copy all the content above
   - Save it with a `.ipynb` extension (e.g., `Market_Competition_Simulation.ipynb`)
   - OR copy each section into a new Jupyter notebook cell by cell

2. **Run the notebook**:
   - Open Jupyter Notebook: `jupyter notebook`
   - Navigate to the file and open it
   - Run cells sequentially (Shift + Enter)

3. **Required libraries**:
   ```bash
   pip install numpy matplotlib pandas seaborn scipy ipywidgets
   ```

4. **For interactive widgets** (optional):
   ```bash
   pip install ipywidgets
   jupyter nbextension enable --py widgetsnbextension
   ```