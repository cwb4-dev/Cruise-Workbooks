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

> **A note on visualization**: These exercises now use [Plotly](https://plotly.com/python/) (`pip install plotly`) instead of Matplotlib for the plots. Plotly charts are interactive in a notebook or browser — you can hover over points to see exact values, zoom in, and toggle series on/off by clicking the legend, which makes it much easier to build intuition about how posteriors shift. If you're running these as plain `.py` scripts rather than in Jupyter, `fig.show()` will open each chart in your default browser.

### Exercise 1: Medical Testing (Easy)
**Problem**: A disease affects 1% of the population. A test is 95% accurate (sensitivity = specificity = 95%). If someone tests positive, what's the probability they actually have the disease?

**Tasks**:
1. Calculate manually using Bayes' Theorem
2. Write a Python function that computes the posterior probability
3. Test with different prevalence rates

```python
# Your solution here
import plotly.graph_objects as go

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

# Task 3: Test with different prevalence rates
prevalence_values = [0.001, 0.01, 0.05, 0.10, 0.25]
posterior_values = []
for prevalence in prevalence_values:
    result = bayes_test(prevalence, 0.95, 0.95)
    posterior_values.append(result)
    print(f"Prevalence {prevalence:.1%} -> P(Disease | Positive): {result:.2%}")

# Interactive bar chart: hover to see exact posterior for each prevalence
fig = go.Figure(go.Bar(
    x=[f"{p:.1%}" for p in prevalence_values],
    y=posterior_values,
    text=[f"{v:.1%}" for v in posterior_values],
    textposition='outside',
    hovertemplate='Prevalence: %{x}<br>P(Disease | Positive): %{y:.2%}<extra></extra>'
))
fig.update_layout(
    title='Posterior Probability of Disease vs. Prevalence (95% sensitivity/specificity)',
    xaxis_title='Disease Prevalence',
    yaxis_title='P(Disease | Positive Test)',
    yaxis_tickformat='.0%'
)
fig.show()
```

**Expected Output**: ~16.1%

**Follow-up Questions**:
- What if the disease is more common (5%)? *(Try it: `bayes_test(0.05, 0.95, 0.95)` → ~50%)*
- What if the test is less specific (90%)? *(Try it: `bayes_test(0.01, 0.95, 0.90)` → ~8.8%)*

Notice how much the posterior swings with prevalence even though the test's accuracy never changes — this is the base-rate effect in action.

---

### Exercise 2: Spam Filter (Easy)
**Problem**: 30% of all emails are spam. The word "discount" appears in 80% of spam emails and 10% of legitimate emails. If an email contains "discount", what's the probability it's spam?

```python
# Your solution here
import plotly.graph_objects as go

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

word_labels = []
word_probs_list = []
for word, (p_spam_word, p_ham_word) in words.items():
    prob = spam_probability(spam_prior, p_spam_word, p_ham_word)
    word_labels.append(word)
    word_probs_list.append(prob)
    print(f"P(Spam | '{word}'): {prob:.2%}")

# Interactive bar chart, colored by whether the word raises or lowers
# spam probability relative to the 30% base rate
fig = go.Figure(go.Bar(
    x=word_labels,
    y=word_probs_list,
    text=[f"{p:.1%}" for p in word_probs_list],
    textposition='outside',
    marker_color=['crimson' if p > spam_prior else 'seagreen' for p in word_probs_list],
    hovertemplate='"%{x}"<br>P(Spam | word): %{y:.2%}<extra></extra>'
))
fig.add_hline(y=spam_prior, line_dash='dash', annotation_text='Base rate (30%)')
fig.update_layout(
    title='P(Spam | word present) vs. Base Rate',
    xaxis_title='Word in Email',
    yaxis_title='P(Spam | word present)',
    yaxis_tickformat='.0%'
)
fig.show()

# Follow-up: combine evidence from multiple words (Naive Bayes)
def naive_bayes_multi_word(p_spam, present_words, word_probs):
    """
    Combine multiple independent word-presence signals.
    present_words: list of words that appear in the email
    word_probs: dict of word -> (p_word_given_spam, p_word_given_ham)
    Assumes conditional independence between words given spam/ham (the
    "naive" assumption).
    """
    p_words_given_spam = 1.0
    p_words_given_ham = 1.0
    for word in present_words:
        p_spam_word, p_ham_word = word_probs[word]
        p_words_given_spam *= p_spam_word
        p_words_given_ham *= p_ham_word

    numerator = p_words_given_spam * p_spam
    denominator = numerator + p_words_given_ham * (1 - p_spam)
    return numerator / denominator

email_words = ['discount', 'urgent']
prob_combined = naive_bayes_multi_word(spam_prior, email_words, words)
print(f"P(Spam | contains {email_words}): {prob_combined:.2%}")
```

**Follow-up**: How would you combine evidence from multiple words? *(The `naive_bayes_multi_word` function above multiplies each word's likelihood ratio together, assuming words are conditionally independent given spam/ham — this is exactly the "naive" assumption behind a Naive Bayes spam classifier.)*

---

### Exercise 3: Weather Forecasting (Medium)
**Problem**: In your city, it rains 40% of the time. Your weather app is correct 85% of the time when forecasting rain, and correct 75% of the time when forecasting no rain. If the app forecasts rain tomorrow, what's the probability it will actually rain?

```python
# Your solution here
import numpy as np
import plotly.graph_objects as go

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
def seasonal_forecast(base_rain_prob, seasonal_sensitivity, seasonal_specificity):
    """
    Recompute the posterior using a season-specific base rain rate and
    season-specific app accuracy (e.g. the app may be more reliable
    forecasting rain in a rainy season than in a dry one).
    """
    return weather_bayes(base_rain_prob, seasonal_sensitivity, seasonal_specificity)

# Example: rainy season vs. dry season
print(f"Monsoon season: {seasonal_forecast(0.70, 0.90, 0.60):.2%}")
print(f"Dry season:     {seasonal_forecast(0.10, 0.80, 0.85):.2%}")

# Follow-up: plot posterior vs. prior, interactively, with a reference
# line showing where posterior == prior (i.e. the app added no info)
priors = np.linspace(0.01, 0.99, 100)
posteriors = [weather_bayes(p, sensitivity, specificity) for p in priors]

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=priors, y=posteriors, mode='lines', name='Posterior',
    hovertemplate='Prior: %{x:.2f}<br>Posterior: %{y:.2%}<extra></extra>'
))
fig.add_trace(go.Scatter(
    x=[0, 1], y=[0, 1], mode='lines', name='No update (y = x)',
    line=dict(dash='dash', color='gray')
))
fig.update_layout(
    title='How the Prior Shapes the Posterior',
    xaxis_title='Prior P(Rain)',
    yaxis_title='Posterior P(Rain | App says Rain)',
    yaxis_tickformat='.0%',
    xaxis_tickformat='.0%'
)
fig.show()
```

**Follow-up**: Plot how the posterior probability changes as the prior varies from 0 to 1. *(The code above does this - notice the posterior tracks the prior fairly closely here, since the app's accuracy isn't extreme in either direction. Compare this to Exercise 1, where a very low prior dominates even a 95%-accurate test.)*

---

### Exercise 4: Machine Learning Classifier (Medium)
**Problem**: You're building a classifier for a rare event (fraud detection). Fraud occurs in 0.5% of transactions. Your model has:
- True Positive Rate: 99% (catches fraud when it happens)
- False Positive Rate: 1% (flags legitimate transactions as fraud)

Calculate the precision (P(Fraud | Flagged)) and discuss the implications.

```python
import numpy as np
import plotly.graph_objects as go

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

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=prevalence_range, y=precision_values, mode='lines', name='Precision',
    hovertemplate='Prevalence: %{x:.2%}<br>Precision: %{y:.2%}<extra></extra>'
))
# Mark this exercise's specific scenario on the curve
fig.add_trace(go.Scatter(
    x=[fraud_rate], y=[precision], mode='markers', name='This scenario (0.5% fraud rate)',
    marker=dict(size=12, color='crimson')
))
fig.update_layout(
    title='Precision vs. Fraud Prevalence (TPR=99%, FPR=1%)',
    xaxis_title='Fraud Prevalence',
    yaxis_title='Precision',
    xaxis_tickformat='.1%',
    yaxis_tickformat='.0%'
)
fig.show()

# Follow-up: solve for the FPR needed to hit a target precision,
# holding prevalence and TPR fixed.
def required_fpr(prevalence, tpr, target_precision):
    """
    Rearranges precision = (tpr*prevalence) / (tpr*prevalence + fpr*(1-prevalence))
    to solve for the fpr that hits target_precision.
    """
    numerator = tpr * prevalence * (1 - target_precision)
    denominator = target_precision * (1 - prevalence)
    return numerator / denominator

target = 0.90
fpr_needed = required_fpr(fraud_rate, tpr, target)
print(f"FPR needed for {target:.0%} precision: {fpr_needed:.4%}")
```

**Follow-up**: How low must the false positive rate be to achieve 90% precision? *(With this fraud rate and TPR, the FPR would need to drop to roughly 0.055% — far below the 1% in the original setup, which illustrates how hard high precision is for very rare events.)*

---

### Exercise 5: A/B Testing (Medium-Difficult)
**Problem**: You're running an A/B test on a website. Version A has a 10% conversion rate (historical data). Version B converts 12% in a sample of 1000 visitors. Using Bayesian updating, determine the probability that B is better than A.

```python
from scipy import stats
import numpy as np
import plotly.graph_objects as go

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
        'mean_b': np.mean(samples_b),
        'samples_a': samples_a,
        'samples_b': samples_b
    }

# IMPORTANT: don't double-count your historical data. If Version A's
# 10% historical conversion rate is *encoded in the prior*, don't also
# feed those same visitors in as a fresh "observation" - that counts
# the same evidence twice and makes you falsely confident.
#
# Use a genuinely weak/uninformative prior for both arms, and let the
# historical data for A enter as its own observation (a real batch of
# past visitors), separate from the new A/B test traffic.

# Weak, uninformative prior - same starting point for both versions
prior_a = (2, 2)
prior_b = (2, 2)

obs_a = (100, 1000)  # Historical data for Version A: 100 conversions / 1000 visitors
obs_b = (120, 1000)  # New test data for Version B: 120 conversions / 1000 visitors

results = bayesian_ab_test(prior_a, prior_b, obs_a, obs_b)
print(f"Probability B is better than A: {results['prob_b_better']:.2%}")
print(f"Expected conversion A: {results['mean_a']:.2%}")
print(f"Expected conversion B: {results['mean_b']:.2%}")

# Interactive overlaid posterior distributions for A and B
fig = go.Figure()
fig.add_trace(go.Histogram(
    x=results['samples_a'], name='Version A', opacity=0.6,
    histnorm='probability density', nbinsx=80,
    hovertemplate='Conversion rate: %{x:.2%}<extra>Version A</extra>'
))
fig.add_trace(go.Histogram(
    x=results['samples_b'], name='Version B', opacity=0.6,
    histnorm='probability density', nbinsx=80,
    hovertemplate='Conversion rate: %{x:.2%}<extra>Version B</extra>'
))
fig.update_layout(
    barmode='overlay',
    title=f"Posterior Conversion Rate Distributions (P[B > A] = {results['prob_b_better']:.1%})",
    xaxis_title='Conversion Rate',
    yaxis_title='Density',
    xaxis_tickformat='.0%'
)
fig.show()
```

**Follow-up**: 
1. How does the result change with stronger prior beliefs? *(Try tightening the prior around 10%, e.g. `prior_a = prior_b = (50, 450)`, and see how much more evidence Version B needs before the "B is better" probability moves — a stronger prior makes the model more skeptical of the new data.)*
2. Calculate the expected loss if you choose wrong. *(Hint: `expected_loss_b = np.mean(np.maximum(results['samples_a'] - results['samples_b'], 0))` gives the average conversion-rate loss if you pick B but A was actually better — a common way to decide whether you have enough data to stop the test.)*

---

### Exercise 6: Markov Chain Monte Carlo (Difficult)
**Problem**: Implement a simple Metropolis-Hastings MCMC sampler to estimate the parameters of a Bayesian logistic regression model for a binary classification problem. Use synthetic data where the true parameters are known.

```python
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

# Visualize convergence: trace plots for each weight, side by side
burn_in = 10000
trace_fig = make_subplots(rows=1, cols=3, subplot_titles=[f'Weight {i+1}' for i in range(3)])
for i in range(3):
    trace_fig.add_trace(
        go.Scatter(y=samples[:, i], mode='lines', name=f'Weight {i+1} trace',
                   line=dict(width=1), showlegend=False),
        row=1, col=i + 1
    )
    trace_fig.add_hline(y=true_weights[i], line_dash='dash', line_color='red',
                         row=1, col=i + 1)
trace_fig.update_layout(title='MCMC Trace Plots (red dashed line = true value)', height=400)
trace_fig.show()

# Posterior distributions (after discarding burn-in), side by side
hist_fig = make_subplots(rows=1, cols=3, subplot_titles=[f'Weight {i+1} Posterior' for i in range(3)])
for i in range(3):
    hist_fig.add_trace(
        go.Histogram(x=samples[burn_in:, i], nbinsx=50, histnorm='probability density',
                     showlegend=False),
        row=1, col=i + 1
    )
    hist_fig.add_vline(x=true_weights[i], line_dash='dash', line_color='red',
                        row=1, col=i + 1)
hist_fig.update_layout(title='Posterior Distributions (burn-in discarded)', height=400)
hist_fig.show()
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