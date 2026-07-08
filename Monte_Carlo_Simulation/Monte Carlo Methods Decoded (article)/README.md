# Monte Carlo Methods Decoded (article)

## A Practical Introduction to Monte Carlo Methods Through Real-World Examples

---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Jupyter](https://img.shields.io/badge/Jupyter-F37626.svg?&logo=Jupyter&logoColor=white)](https://jupyter.org/)
[![Article](https://img.shields.io/badge/Read%20Article-Towards%20Data%20Science-blue)](https://towardsdatascience.com/monte-carlo-methods-decoded-d63301bde7ce/)

---

## 📚 Overview

This folder contains the complete Jupyter Notebook implementation for the article **"Monte Carlo Methods Decoded"** by Hennie de Harder. The notebook provides hands-on examples demonstrating the core concepts and practical applications of Monte Carlo methods across different domains.

Monte Carlo methods are computational algorithms that rely on **repeated random sampling** to obtain numerical results. Rather than solving problems analytically, they use random simulation to approximate solutions, making them invaluable for modeling uncertainty in complex systems.

### What's Inside

- **Complete Jupyter Notebook** with all code examples
- **Three Progressive Examples** from basic to advanced
- **Interactive Visualizations** to build intuition
- **Practical Applications**: Project management, numerical integration, game AI
- **MCTS Implementation**: A working Monte Carlo Tree Search for game playing
- **Summary & Best Practices**: When and how to use Monte Carlo methods

---

## 🎯 What This Notebook Covers

### The Core Concept

Monte Carlo methods are built on three key principles:

1. **Random Variable Sampling**: Generating values from probability distributions (normal, uniform, triangular, etc.) for uncertain input variables
2. **Probability Distributions**: Representing uncertainty and likelihood of different values
3. **Iterations and Convergence**: Running simulations thousands of times until results stabilize

### The Three Examples

#### 1. 🗺️ The Marble Jar (Foundation)
A simple introduction showing how random sampling reveals hidden distributions. This is the "Hello World" of Monte Carlo methods.

#### 2. 📊 Project Management (Software Launch)
Simulating a software project with uncertain task durations to answer critical questions:
- What's the probability of completing within 6 months?
- What's the 95% confidence interval for completion time?
- Which tasks have the biggest impact on total time?

#### 3. 📐 Area Under an Irregular Curve
Using Monte Carlo to approximate areas that would be difficult to calculate analytically. Demonstrates how error decreases with more samples.

#### 4. 🎮 Monte Carlo Tree Search (MCTS)
Implementing MCTS for the "Island Conquest" game, showing how Monte Carlo extends to sequential decision-making problems.

---

## 📖 Module Structure

### Part 1: The Basics - Marble Jar Analogy

**WHAT**: Simulating draws from a jar with unknown marble distribution to understand how random sampling reveals hidden patterns.

**WHY**: This demonstrates the fundamental principle: through repeated random sampling, we can approximate the true distribution of a system we can't observe directly.

**HOW**: The code draws random samples and compares observed distributions to the true (hidden) distribution, showing convergence with more samples.

**Key Insight**: As sample size increases, observed probabilities converge to true probabilities.

---

### Part 2: Example 1 - Project Management

**WHAT**: Simulating a software launch project with uncertain task durations.

**WHY**: Real projects have variable task completion times. Monte Carlo helps quantify risk and set realistic expectations.

**HOW**:
- Each task uses different probability distributions (normal, triangular, uniform)
- Tasks run in sequence or parallel
- Thousands of simulations generate a distribution of total completion time
- Statistics reveal probabilities, confidence intervals, and sensitivity analysis

**Key Insight**: Shows why "most likely" estimates are often misleading, and why probabilistic planning is superior.

---

### Part 3: Example 2 - Area Under a Curve

**WHAT**: Approximating the area under a complex function using random sampling.

**WHY**: Many integrals are difficult or impossible to solve analytically. Monte Carlo provides a practical alternative.

**HOW**:
1. Define a bounding rectangle that contains the curve
2. Randomly sample points within the rectangle
3. Count what percentage fall under the curve
4. Multiply by the rectangle area

**Key Insight**: Error decreases as ~1/√n, showing the trade-off between accuracy and computation time.

---

### Part 4: Example 3 - Monte Carlo Tree Search

**WHAT**: Implementing MCTS for the "Island Conquest" game.

**WHY**: MCTS is a powerful algorithm for sequential decision-making, used in AI for games like Go and chess.

**HOW**:
1. **Selection**: Traverse the tree balancing exploration and exploitation (UCT formula)
2. **Expansion**: Add a new child node (move) to the tree
3. **Simulation**: Play random games from the new node
4. **Backpropagation**: Update statistics (wins, visits) back up the tree

**Key Insight**: The algorithm learns optimal strategies through self-play without explicit game knowledge.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Jupyter Notebook or Jupyter Lab
- Basic understanding of Python and probability

### Installation

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/cwb4-dev/Cruise-Workbooks.git

# Navigate to this folder
cd Cruise-Workbooks/Monte_Carlo_Simulation/Monte\ Carlo\ Methods\ Decoded\ \(article\)

# Install required packages
pip install numpy matplotlib seaborn
```

### Running the Notebook

```bash
# Start Jupyter Notebook
jupyter notebook

# Or with Jupyter Lab
jupyter lab
```

Then open the notebook file (the one with `.ipynb` extension) and run cells in order.

---

## 💻 Code Preview

### The Marble Jar - Foundation

```python
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# True (hidden) composition of the jar
true_colors = {'red': 0.40, 'blue': 0.25, 'green': 0.20, 'yellow': 0.15}

# Draw samples
samples = np.random.choice(
    list(true_colors.keys()), 
    size=1000, 
    p=list(true_colors.values())
)

# Observe how sampling reveals the hidden distribution
```

### Project Management Simulation

```python
# Task durations with uncertainty
requirements = np.random.normal(30, 5, n_simulations)  # mean=30, std=5
design = np.random.triangular(20, 35, 50, n_simulations)  # min, mode, max
development = np.random.normal(60, 10, n_simulations)
testing = np.random.triangular(25, 40, 60, n_simulations)

# Parallel tasks (deployment and marketing)
deployment_training = np.random.uniform(20, 30, n_simulations)
marketing = np.random.uniform(15, 25, n_simulations)

# Total time = sequential tasks + max(parallel tasks)
total_time = (requirements + design + development + testing + 
              np.maximum(deployment_training, marketing))

# Calculate probability of completing within 180 days
prob_complete = np.mean(total_time <= 180)
```

### Monte Carlo Tree Search

```python
def mcts(root_state, iterations=1000):
    """Run MCTS and return the best move."""
    root_node = MCTSNode(root_state)
    
    for _ in range(iterations):
        node = root_node
        state = root_state.copy()
        
        # Selection: traverse tree using UCT
        while node.untried_moves == [] and node.children != []:
            node = node.select_child()
            state.claim_island(node.move)
        
        # Expansion: add new node
        if node.untried_moves:
            move = random.choice(node.untried_moves)
            state.claim_island(move)
            node = node.add_child(move, state)
        
        # Simulation: random playout
        while not state.is_game_over():
            possible_moves = state.get_legal_moves()
            if possible_moves:
                state.claim_island(random.choice(possible_moves))
        
        # Backpropagation: update statistics
        result = state.get_result(root_state.player_turn)
        while node is not None:
            node.update(result)
            node = node.parent
    
    return best_move(node)
```

---

## 📊 Visualization Gallery

The notebook includes rich visualizations:

1. **True vs. Observed Distributions** - Comparing hidden vs. sampled distributions
2. **Convergence Plots** - Showing how error decreases with more samples
3. **Project Completion Distributions** - Histograms with confidence intervals
4. **Area Approximation** - Visualizing points under/above the curve
5. **MCTS Statistics** - Win rates and visit counts for each move
6. **Distribution Comparisons** - Normal, uniform, triangular, log-normal

---

## 📋 Key Takeaways

After working through this notebook, you'll understand:

1. **The Core Principle**: Random sampling + repetition = understanding complex systems
2. **When to Use Monte Carlo**: Project risk, numerical integration, game AI, and more
3. **How to Implement**: Probability distributions, simulation loops, statistical analysis
4. **What to Expect**: Error decreases as ~1/√n, requiring many iterations
5. **The Limitations**: Computational cost, sensitivity to assumptions, approximations only

---

## 🎯 When to Use Monte Carlo Methods

| Application | Best For | Key Benefit |
|-------------|----------|-------------|
| **Project Management** | Uncertain task durations | Probability of completion, risk assessment |
| **Area Approximation** | Complex/irregular shapes | No analytical solution needed |
| **MCTS/Gaming** | Sequential decisions | No explicit game knowledge required |
| **Financial Modeling** | Portfolio risk, option pricing | Quantifies uncertainty |
| **Physics/Engineering** | Complex systems simulation | Handles nonlinear interactions |

---

## 🧪 Try It Yourself

### Exercise 1: Modify the Project
Change the task duration distributions or dependencies. How does completion probability change?

### Exercise 2: New Integration Function
Try integrating a different function. How does the shape affect convergence?

### Exercise 3: Modify MCTS
Adjust the exploration constant (UCT formula). How does it affect move selection?

### Exercise 4: New Game
Implement MCTS for a different game (like Tic-Tac-Toe).

---

## 📚 References

- **Original Article**: [Monte Carlo Methods Decoded](https://towardsdatascience.com/monte-carlo-methods-decoded-d63301bde7ce/) by Hennie de Harder
- **Monte Carlo Method** (Wikipedia): [https://en.wikipedia.org/wiki/Monte_Carlo_method](https://en.wikipedia.org/wiki/Monte_Carlo_method)
- **Monte Carlo Tree Search** (Wikipedia): [https://en.wikipedia.org/wiki/Monte_Carlo_tree_search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search)

---

## 📄 License

This project is licensed under the MIT License – see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Based on the article by **Hennie de Harder**
- Part of the **Cruise Workbooks** collection
- Built with ❤️ for the data science community

---

<div align="center">

**Start exploring Monte Carlo methods today!**

[![Star on GitHub](https://img.shields.io/github/stars/cwb4-dev/Cruise-Workbooks.svg?style=social)](https://github.com/cwb4-dev/Cruise-Workbooks)

</div>
