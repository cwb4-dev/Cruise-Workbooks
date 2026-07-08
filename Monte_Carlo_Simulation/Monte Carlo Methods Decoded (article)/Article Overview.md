---
source: https://towardsdatascience.com/monte-carlo-methods-decoded-d63301bde7ce/
tags:
  - monte-carlo
  - from-dsai
---
Based on the article "Monte Carlo Methods Decoded" by Hennie de Harder, here are the main points:

### Core Concept & Basics
*   **Definition**: Monte Carlo methods are a broad class of computational algorithms that rely on **repeated random sampling** to obtain numerical results. They are used to model uncertainty in complex systems.
*   **Core Idea**: The name is metaphorical, referencing the randomness of a casino. The technique involves running many simulations (iterations) with random inputs to see a range of possible outcomes.
*   **Three Key Concepts**:
    1.  **Random Variable Sampling**: Generating values from probability distributions (e.g., normal, uniform) for uncertain input variables.
    2.  **Probability Distributions**: These represent the uncertainty and likelihood of different values for those variables.
    3.  **Iterations and Convergence**: Running the simulation thousands of times until the results stabilize, providing a robust statistical basis for prediction.

### Three Example Applications
1.  **Project Management (Launching New Software)**:
    *   **Scenario**: Estimating total time for a multi-task project with uncertain durations for each task.
    *   **Method**: Sample durations from distributions for each task, sum them (accounting for parallel tasks), and repeat thousands of times.
    *   **Output**: A distribution of total completion time, from which you can calculate probabilities (e.g., only a 21% chance of finishing within 180 days) and confidence intervals.
2.  **Approximating Area Under an Irregular Curve**:
    *   **Scenario**: When analytical integration is difficult or impossible.
    *   **Method**: Randomly sample points within a bounding rectangle that contains the curve. Count the percentage of points that fall *under* the curve. Multiply that percentage by the total area of the rectangle.
    *   **Output**: A close approximation of the area, which improves as more points (iterations) are used.
3.  **Monte Carlo Tree Search (MCTS) in Gaming**:
    *   **Scenario**: Finding the best move in a game (e.g., the simple game "Island Conquest").
    *   **Method**: This is a more dynamic application. It builds a tree of possible future game states through four steps:
        *   **Selection**: Traverse the tree, balancing exploration and exploitation using a formula (UCT).
        *   **Expansion**: Add a new child node (move) to the tree.
        *   **Simulation**: Play out the game randomly from that new node to a conclusion (win/loss/draw).
        *   **Backpropagation**: Update the statistics (wins, visits) of all nodes on the path based on the simulation result.
    *   **Output**: The action with the highest visit count is recommended, as it is the most promising.

### Cons & Limitations
*   **Computational Cost**: Can be very expensive and time-consuming, especially for complex problems with many variables.
*   **Sensitive to Assumptions**: Results are only as good as the input data and probability distributions. Biased or inaccurate data leads to unreliable results.
*   **Modeling & Interpretation Challenges**: Building an accurate model and correctly interpreting the probabilistic results can be difficult.
*   **Not a Precise Prediction**: Simulations provide approximations, not exact answers. Achieving high precision may require an impractically large number of iterations.