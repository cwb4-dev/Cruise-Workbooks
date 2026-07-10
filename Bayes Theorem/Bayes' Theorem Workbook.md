# Bayes' Theorem Workbook

## Understanding Bayesian Thinking

### The Core Formula

Bayes' Theorem is a way to update our beliefs based on new evidence. At its heart:

```
P(A|B) = P(B|A) × P(A) / P(B)
```

Where:
- **P(A|B)** = Probability of A given B (posterior)
- **P(B|A)** = Probability of B given A (likelihood)
- **P(A)** = Probability of A (prior)
- **P(B)** = Probability of B (evidence)

### Why It Matters

Bayes' Theorem helps us:
- Update beliefs as new data arrives
- Handle uncertainty systematically
- Avoid common cognitive biases
- Make better decisions under uncertainty

### The Intuition

Think of Bayes as a "rebalancing" formula:
1. Start with your prior belief (how likely you think A is)
2. Consider how likely you'd see evidence B if A were true
3. Adjust based on how common evidence B is overall

**Example**: If you hear a car alarm at night, how likely is it a theft?
- Prior: Car thefts are rare (0.1%)
- Likelihood: Theft almost always triggers alarm (95%)
- Evidence: Car alarms go off for many reasons (2% of nights)
- Result: Surprisingly low probability of actual theft

---

## Python Exercises

### Exercise 1: Medical Testing (Easy)
**Problem**: A disease affects 1% of the population. A test is 95% accurate (sensitivity = specificity = 95%). If someone tests positive, what's the probability they actually have the disease?

**Tasks**:
1. Calculate manually using Bayes' Theorem
2. Write a Python function that computes the posterior probability
3. Test with different prevalence rates

```python
# Your solution here
def bayes_test(prevalence, sensitivity, specificity, test_positive=True):
    """
    Calculate posterior probability after a test result
    """
    # P(Disease)
    prior = prevalence
    
    # P(Test Positive | Disease)
    likelihood = sensitivity if test_positive else 1 - sensitivity
    
    # P(Test Positive) = P(TP|D)*P(D) + P(TP|~D)*P(~D)
    p_test_positive = (sensitivity * prevalence + 
                       (1 - specificity) * (1 - prevalence))
    
    # Apply Bayes
    posterior = (likelihood * prior) / p_test_positive
    return posterior

# Test it
print(f"Probability of disease given positive test: {bayes_test(0.01, 0.95, 0.95):.2%}")
```

**Expected Output**: ~16.1%

**Follow-up Questions**:
- What if the disease is more common (5%)?
- What if the test is less specific (90%)?

---

### Exercise 2: Spam Filter (Easy)
**Problem**: 30% of all emails are spam. The word "discount" appears in 80% of spam emails and 10% of legitimate emails. If an email contains "discount", what's the probability it's spam?

```python
# Your solution here
def spam_probability(p_spam, p_discount_given_spam, p_discount_given_ham):
    """
    Calculate probability email is spam given it contains "discount"
    """
    # Calculate P(Discount) overall
    p_discount = (p_discount_given_spam * p_spam + 
                  p_discount_given_ham * (1 - p_spam))
    
    # Apply Bayes
    p_spam_given_discount = (p_discount_given_spam * p_spam) / p_discount
    return p_spam_given_discount

# Test with multiple words
spam_prior = 0.30
words = {
    'discount': (0.80, 0.10),
    'free': (0.70, 0.05),
    'urgent': (0.40, 0.02),
    'meeting': (0.10, 0.30)
}

for word, (p_spam_word, p_ham_word) in words.items():
    prob = spam_probability(spam_prior, p_spam_word, p_ham_word)
    print(f"P(Spam | '{word}'): {prob:.2%}")
```

**Follow-up**: How would you combine evidence from multiple words?

---

### Exercise 3: Weather Forecasting (Medium)
**Problem**: In your city, it rains 40% of the time. Your weather app is correct 85% of the time when forecasting rain, and correct 75% of the time when forecasting no rain. If the app forecasts rain tomorrow, what's the probability it will actually rain?

```python
# Your solution here
def weather_bayes(p_rain, app_correct_given_rain, app_correct_given_no_rain):
    """
    Calculate probability of rain given app forecast
    """
    # P(App says Rain)
    p_app_rain = (app_correct_given_rain * p_rain + 
                  (1 - app_correct_given_no_rain) * (1 - p_rain))
    
    # P(Rain | App says Rain)
    p_rain_given_app = (app_correct_given_rain * p_rain) / p_app_rain
    return p_rain_given_app

# Baseline
p_rain = 0.40
sensitivity = 0.85
specificity = 0.75

result = weather_bayes(p_rain, sensitivity, specificity)
print(f"P(Rain | App says Rain): {result:.2%}")

# Challenge: What if the app's performance changes with seasons?
def seasonal_forecast(season, base_rain_prob, app_accuracy_adjustment):
    """
    Adjust forecast based on seasonal patterns
    """
    p_rain = base_rain_prob * app_accuracy_adjustment
    return weather_bayes(p_rain, sensitivity, specificity)
```

**Follow-up**: Plot how the posterior probability changes as the prior varies from 0 to 1.

---

### Exercise 4: Machine Learning Classifier (Medium)
**Problem**: You're building a classifier for a rare event (fraud detection). Fraud occurs in 0.5% of transactions. Your model has:
- True Positive Rate: 99% (catches fraud when it happens)
- False Positive Rate: 1% (flags legitimate transactions as fraud)

Calculate the precision (P(Fraud | Flagged)) and discuss the implications.

```python
import numpy as np
import matplotlib.pyplot as plt

def calculate_precision(prevalence, tpr, fpr):
    """
    Calculate precision for a binary classifier
    """
    # P(Flagged) = P(Flagged|Fraud)*P(Fraud) + P(Flagged|No Fraud)*P(No Fraud)
    p_flagged = tpr * prevalence + fpr * (1 - prevalence)
    
    # P(Fraud | Flagged)
    precision = (tpr * prevalence) / p_flagged
    return precision

# Initial calculation
fraud_rate = 0.005
tpr = 0.99
fpr = 0.01

precision = calculate_precision(fraud_rate, tpr, fpr)
print(f"Precision: {precision:.2%}")

# Explore the tradeoff
prevalence_range = np.linspace(0.001, 0.10, 100)
precision_values = [calculate_precision(p, tpr, fpr) for p in prevalence_range]

plt.figure(figsize=(8, 6))
plt.plot(prevalence_range, precision_values)
plt.xlabel('Fraud Prevalence')
plt.ylabel('Precision')
plt.title('Precision vs. Fraud Prevalence')
plt.grid(True)
plt.show()
```

**Follow-up**: How low must the false positive rate be to achieve 90% precision?

---

### Exercise 5: A/B Testing (Medium-Difficult)
**Problem**: You're running an A/B test on a website. Version A has a 10% conversion rate (historical data). Version B converts 12% in a sample of 1000 visitors. Using Bayesian updating, determine the probability that B is better than A.

```python
from scipy import stats
import numpy as np

def bayesian_ab_test(prior_a, prior_b, observations_a, observations_b):
    """
    Perform Bayesian A/B test with Beta-Binomial model
    """
    # Prior: Beta distribution parameters
    # Let's use informative prior based on historical data
    alpha_a, beta_a = prior_a
    alpha_b, beta_b = prior_b
    
    # Update with observations
    conversions_a, visitors_a = observations_a
    conversions_b, visitors_b = observations_b
    
    # Posterior parameters
    posterior_a = (alpha_a + conversions_a, beta_a + visitors_a - conversions_a)
    posterior_b = (alpha_b + conversions_b, beta_b + visitors_b - conversions_b)
    
    # Sample from posteriors
    n_samples = 100000
    samples_a = np.random.beta(posterior_a[0], posterior_a[1], n_samples)
    samples_b = np.random.beta(posterior_b[0], posterior_b[1], n_samples)
    
    # Probability B is better than A
    prob_b_better = np.mean(samples_b > samples_a)
    
    return {
        'prob_b_better': prob_b_better,
        'posterior_a': posterior_a,
        'posterior_b': posterior_b,
        'mean_a': np.mean(samples_a),
        'mean_b': np.mean(samples_b)
    }

# Example: Historical conversion rate 10% with 1000 visitors
# Prior: Beta(100, 900)  # Weak prior
# Test: Version B with 120 conversions out of 1000 visitors

# Weak prior
prior_a = (100, 900)
prior_b = (100, 900)

obs_a = (100, 1000)  # Historical
obs_b = (120, 1000)  # Test

results = bayesian_ab_test(prior_a, prior_b, obs_a, obs_b)
print(f"Probability B is better than A: {results['prob_b_better']:.2%}")
print(f"Expected conversion A: {results['mean_a']:.2%}")
print(f"Expected conversion B: {results['mean_b']:.2%}")
```

**Follow-up**: 
1. How does the result change with stronger prior beliefs?
2. Calculate the expected loss if you choose wrong.

---

### Exercise 6: Markov Chain Monte Carlo (Difficult)
**Problem**: Implement a simple Metropolis-Hastings MCMC sampler to estimate the parameters of a Bayesian logistic regression model for a binary classification problem. Use synthetic data where the true parameters are known.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import expit

def generate_data(n_samples=1000, true_weights=[0.5, -0.3, 0.1]):
    """
    Generate synthetic binary classification data
    """
    np.random.seed(42)
    X = np.random.randn(n_samples, len(true_weights))
    logits = X @ true_weights
    y = np.random.binomial(1, expit(logits))
    return X, y

def log_posterior(weights, X, y, prior_scale=1.0):
    """
    Calculate log of the unnormalized posterior
    """
    # Log likelihood (Bernoulli)
    logits = X @ weights
    log_likelihood = np.sum(y * logits - np.log(1 + np.exp(logits)))
    
    # Log prior (Gaussian)
    log_prior = -0.5 * np.sum(weights**2) / prior_scale**2
    
    return log_likelihood + log_prior

def metropolis_hastings(X, y, n_iterations=10000, proposal_scale=0.1):
    """
    Metropolis-Hastings sampler for Bayesian logistic regression
    """
    n_features = X.shape[1]
    
    # Initialize
    current_weights = np.zeros(n_features)
    current_log_posterior = log_posterior(current_weights, X, y)
    
    samples = np.zeros((n_iterations, n_features))
    acceptance_rate = 0
    
    for i in range(n_iterations):
        # Propose new weights
        proposal = current_weights + np.random.randn(n_features) * proposal_scale
        proposal_log_posterior = log_posterior(proposal, X, y)
        
        # Acceptance ratio
        log_acceptance_ratio = proposal_log_posterior - current_log_posterior
        
        # Accept or reject
        if np.log(np.random.random()) < log_acceptance_ratio:
            current_weights = proposal
            current_log_posterior = proposal_log_posterior
            acceptance_rate += 1
        
        samples[i] = current_weights
    
    acceptance_rate /= n_iterations
    return samples, acceptance_rate

# Generate data
X, y = generate_data()
true_weights = np.array([0.5, -0.3, 0.1])

# Run MCMC
samples, acceptance = metropolis_hastings(X, y, n_iterations=50000)

print(f"Acceptance rate: {acceptance:.2%}")
print(f"True weights: {true_weights}")
print(f"Estimated posterior means: {np.mean(samples[10000:], axis=0)}")

# Visualize convergence
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for i in range(3):
    axes[i].plot(samples[:, i])
    axes[i].axhline(y=true_weights[i], color='r', linestyle='--', label='True')
    axes[i].set_title(f'Weight {i+1}')
    axes[i].legend()
plt.tight_layout()
plt.show()

# Posterior distributions
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for i in range(3):
    axes[i].hist(samples[10000:, i], bins=50, density=True, alpha=0.7)
    axes[i].axvline(x=true_weights[i], color='r', linestyle='--', label='True')
    axes[i].set_title(f'Posterior Distribution - Weight {i+1}')
    axes[i].legend()
plt.tight_layout()
plt.show()
```

**Follow-up Questions**:
1. How does the acceptance rate change with different proposal scales?
2. How many burn-in samples are needed?
3. How do the posterior estimates change with different prior variances?

---

## Key Takeaways

1. **Bayes is about updating beliefs**: Always start with what you know (prior) and update with evidence (likelihood) to get your new belief (posterior).

2. **Prior matters**: Your initial assumptions significantly impact results, especially with limited data.

3. **Always consider the base rate**: Rare events require very strong evidence to become probable.

4. **Sequential updating**: Bayes naturally handles new information arriving over time.

5. **Computational methods**: For complex problems, MCMC and other sampling methods let us approximate posterior distributions when closed-form solutions aren't available.

6. **Visualization is crucial**: Always plot your priors, likelihoods, and posteriors to build intuition.

## Suggested Next Steps

1. Extend Exercise 6 to include automatic differentiation for more complex models
2. Implement a Gaussian Process for Bayesian optimization
3. Explore Variational Inference as an alternative to MCMC
4. Apply Bayesian methods to real-world datasets (Kaggle competitions)
5. Learn about Bayesian Neural Networks