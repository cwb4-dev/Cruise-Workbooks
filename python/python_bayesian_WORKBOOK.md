# Bayesian Inference — Python Workbook

> Python • Google IDX • Firebase • iPad  
> *Background, Theory & 10 Examples*

---

## Part 0 — IDX Setup

### Session Startup

```bash
cd bayesian
pip3 install numpy matplotlib pandas scipy firebase-admin
```

### Standard Imports — Every Script

```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

np.random.seed(42)
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (10, 5)

if not firebase_admin._apps:
    cred = credentials.Certificate('../firebase/service-account.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()
print('Ready!')
```

### Gemini Prompt Template

```
I am writing Python in Google IDX terminal.
numpy, matplotlib, pandas, scipy, firebase-admin all installed.
Firebase db client already initialized. np.random.seed(42) already set.
Give me complete Python code I can save as a .py file and run with python3.
```

---

## Part 1 — What is Bayesian Thinking?

### The Origin — Thomas Bayes

Thomas Bayes was an 18th-century English minister who never published his most important idea
in his lifetime. After he died in 1761, his friend Richard Price found a paper describing
a method for reasoning backward from evidence to causes.

### Two Schools of Statistics

| | Frequentist | Bayesian |
|---|---|---|
| Probability means | Long-run frequency | Degree of belief |
| Prior knowledge | Ignored | Explicitly incorporated |
| Output | p-values, reject/fail | Full probability distribution |

### Bayes' Theorem

```
P(H | E)  =  P(E | H)  ×  P(H)  /  P(E)
```

| Term | Name | Plain English |
|---|---|---|
| P(H \| E) | Posterior | Belief AFTER seeing evidence |
| P(E \| H) | Likelihood | How well H explains the evidence |
| P(H) | Prior | Belief BEFORE seeing evidence |
| P(E) | Marginal | Normalizing constant |

### Conjugate Priors Quick Reference

| Likelihood | Conjugate Prior | Update Rule |
|---|---|---|
| Binomial (yes/no) | Beta(a, b) | Beta(a+heads, b+tails) |
| Poisson (counts) | Gamma(a, b) | Gamma(a+count, b+n) |
| Normal (known var) | Normal(mu, sigma) | Weighted average |

---

## Part 2 — Example 1: Is This Coin Fair?

### Ask Gemini

```
I am writing Python in Google IDX.
Write a Bayesian coin fairness analysis using the Beta-Binomial conjugate model.
Observed: 10 flips, 7 heads. Prior: Beta(2,2).
Update rule: Posterior = Beta(alpha+heads, beta+tails).
- Print: posterior mean, mode, 95% credible interval, P(coin biased toward heads)
- Plot 1: prior vs posterior on same chart (blue=prior, purple=posterior)
- Plot 2: sequential updating — show belief curve after each individual flip
- Use scipy.stats.beta for all distribution calculations
- Save to Firebase collection 'bayesian_analyses'
  Fields: analysis_type='coin_fairness', n_flips=10, n_heads=7,
  posterior_mean, ci_low, ci_high, prob_biased, timestamp
Give me complete Python code to save as coin_fairness.py.
```

### Run It

```bash
python3 coin_fairness.py
```

> **What to observe:** The posterior curve starts broad and narrows with more data. The peak moves toward 0.7 but gets pulled left by the prior. More flips = narrower, more confident curve.

---

## Part 3 — Example 2: Medical Diagnosis

### Ask Gemini

```
I am writing Python in Google IDX.
Write a Bayesian medical diagnosis calculator applying Bayes Theorem directly.
Test these scenarios:
  1. Rare disease: prevalence=1%, sensitivity=95%, specificity=95%
  2. Moderate disease: prevalence=5%, sensitivity=95%, specificity=95%
  3. Common disease: prevalence=20%, sensitivity=95%, specificity=95%
  4. Two positive tests in a row (posterior from test 1 = prior for test 2)
- Print a table: scenario, P(Disease|Positive), P(Disease|Negative)
- Plot: P(Disease|Positive) vs prevalence from 0% to 50%
  showing how the prior dramatically affects the result
- Save all to Firebase collection 'bayesian_analyses'
  Fields: analysis_type='medical_diagnosis', prevalence, sensitivity,
  specificity, prob_disease_given_positive, timestamp
Give me complete Python code to save as medical_diagnosis.py.
```

> **The surprise:** With 1% prevalence and a 95% accurate test, a positive result means only 16% chance of having the disease — not 95%. The prior dominates.

---

## Part 4 — Examples 3, 4 & 5

### Example 3: Naive Bayes Spam Filter

```
I am writing Python in Google IDX.
Build a Naive Bayes spam classifier from scratch:
Training data: 7 spam emails and 7 ham emails as strings
- Train on word frequencies with Laplace smoothing (add 1 to counts)
- Predict spam probability for 4 new test emails using log probabilities
- Print verdict and spam probability for each test email
- Save to Firebase collection 'bayesian_analyses'
  Fields: analysis_type='spam_filter', email_preview, spam_prob, verdict, timestamp
Give me complete Python code to save as spam_filter.py.
```

### Example 4: Bayesian A/B Testing

```
I am writing Python in Google IDX.
Write a Bayesian A/B test analysis.
Data: Variant A: 1000 visitors, 52 conversions.
      Variant B: 1000 visitors, 63 conversions.
Prior: Beta(2, 20).
- Use Monte Carlo with 200,000 samples to compute P(B > A)
- Print: P(B better), expected lift, 95% credible interval for lift
- Print recommendation: 'Deploy B' if P(B>A) > 95%, else 'Continue testing'
- Plot both posterior distributions on same chart
- Save to Firebase collection 'bayesian_analyses'
  Fields: analysis_type='ab_test', prob_b_better, expected_lift,
  recommendation, timestamp
Give me complete Python code to save as ab_test.py.
```

> **The Bayesian advantage:** Instead of "p=0.043, reject null" you get: "84% probability B is better, expected 21% lift." That's the answer stakeholders actually need.

### Example 5: Bayesian Product Rating

```
I am writing Python in Google IDX.
Write a Bayesian product rating estimator.
Problem: a product has 6 five-star and 1 one-star review. Naive avg is misleading.
Use Bayesian shrinkage: pull toward prior mean of 3.5 stars (10 pseudo-observations).
- Compare naive average vs Bayesian estimate
- Show how estimate converges to naive average as reviews grow
  (simulate adding more reviews at same ratio, plot both estimates)
- Save to Firebase collection 'bayesian_analyses'
  Fields: analysis_type='product_rating', n_reviews, naive_avg,
  bayesian_estimate, timestamp
Give me complete Python code to save as product_rating.py.
```

---

## Part 5 — Examples 6, 7 & 8

### Example 6: Changepoint Detection

```
I am writing Python in Google IDX.
Write a Bayesian changepoint detection analysis.
Simulate 100 days of sales: first 50 days Poisson rate=20, next 50 rate=35.
For each possible changepoint day compute log posterior probability.
- Plot 1: actual sales time series with true changepoint marked
- Plot 2: posterior probability of changepoint at each day
- Print: detected changepoint vs true changepoint
- Save to Firebase collection 'bayesian_analyses'
  Fields: analysis_type='changepoint', true_changepoint,
  detected_changepoint, timestamp
Give me complete Python code to save as changepoint.py.
```

### Example 7: Bayesian Linear Regression

```
I am writing Python in Google IDX.
Write a Bayesian linear regression with uncertainty bands.
Generate synthetic data: y = 2x + 1 + noise (25 points, x from 0 to 10).
Use Gaussian prior N(0, 10^2) on intercept and slope.
Compute analytical posterior (closed form for Gaussian prior + likelihood).
- Print: posterior mean for intercept and slope (should be near 1 and 2)
- Plot: data points, posterior mean line, 95% credible band
- Use scipy or numpy matrix operations for the posterior calculation
- Save to Firebase collection 'bayesian_analyses'
  Fields: analysis_type='linear_regression', posterior_intercept,
  posterior_slope, timestamp
Give me complete Python code to save as linear_regression.py.
```

### Example 8: Drug Trial with Monte Carlo

```
I am writing Python in Google IDX.
Write a Bayesian drug trial analysis.
Data: 100 drug patients, 45 recoveries. 100 placebo patients, 30 recoveries.
Prior: Beta(2,2) for both recovery rates.
- Use Monte Carlo with 200,000 samples from each posterior
- Print: P(drug better), expected improvement, 95% credible interval
- Plot: posterior distributions for drug rate, placebo rate, and effect
- Decision: STRONG (>95%), MODERATE (80-95%), WEAK (<80%)
- Save to Firebase collection 'bayesian_analyses'
  Fields: analysis_type='drug_trial', prob_drug_better,
  expected_improvement, ci_low, ci_high, decision, timestamp
Give me complete Python code to save as drug_trial.py.
```

---

## Part 6 — Examples 9 & 10

### Example 9: Hierarchical Model — Campaign Comparison

```
I am writing Python in Google IDX.
Write a hierarchical Bayesian campaign analyzer.
Campaign data (visitors, conversions):
  A:(1000,52) B:(800,35) C:(50,8) D:(1200,67)
  E:(30,10)  F:(900,41) G:(600,33) H:(25,0)
- For each campaign: compute naive rate and Bayesian shrinkage estimate
- Shrinkage: pull toward group mean using Beta-Binomial hierarchical model
- Plot: grouped bar chart comparing naive vs Bayesian rates per campaign
- Highlight how small-sample campaigns (C, E, H) get shrunk toward the mean
- Save to Firebase collection 'bayesian_analyses'
  Fields: analysis_type='hierarchical_campaigns', campaign_name,
  naive_rate, bayesian_rate, n_visitors, timestamp
Give me complete Python code to save as hierarchical_campaigns.py.
```

> **Shrinkage:** Campaign H with 0/25 conversions gets a non-zero estimate instead of exactly 0%. This is automatic correction for small-sample noise.

### Example 10: Bayesian Sales Forecast

```
I am writing Python in Google IDX.
Write a Bayesian sales forecast with prediction intervals.
Generate 24 months training data: sales = 100 + 3.5*month + normal noise(std=12).
Fit Bayesian linear regression. Forecast next 12 months with full uncertainty.
- Draw 10,000 samples from the posterior to build prediction intervals
- Plot: training data, posterior mean forecast, 90% prediction interval
- Print: expected sales in months 30, 33, 36 with 90% intervals
- Save to Firebase collection 'bayesian_analyses'
  Fields: analysis_type='sales_forecast', posterior_slope,
  forecast_month_36_mean, forecast_month_36_ci_low,
  forecast_month_36_ci_high, timestamp
Give me complete Python code to save as sales_forecast.py.
```

---

## Part 7 — Query All Results

### Ask Gemini

```
Write Python that reads all results from Firebase Firestore
collection 'bayesian_analyses' and:
- Groups by analysis_type with count of runs per type
- For coin_fairness: shows how posterior_mean changed over runs
- For ab_test: lists recommendation and prob_b_better per run
- For drug_trial: shows prob_drug_better and decision per run
- Prints all results sorted by timestamp
db client already initialized. Give me complete Python code.
```

---

## Key Terms Reference

| Term | Plain English |
|---|---|
| Prior | Your belief before seeing data |
| Posterior | Your updated belief after seeing data |
| Credible interval | A range containing the true value with X% probability |
| Conjugate prior | A prior that keeps the posterior in the same distributional family |
| Shrinkage | Hierarchical models pull group estimates toward the overall mean |
| MCMC | Algorithm for sampling from complex posteriors — not needed for conjugate models |

---

## File Structure

```
bayesian/
├── WORKBOOK.md
├── coin_fairness.py
├── medical_diagnosis.py
├── spam_filter.py
├── ab_test.py
├── product_rating.py
├── changepoint.py
├── linear_regression.py
├── drug_trial.py
├── hierarchical_campaigns.py
└── sales_forecast.py
```

---

## Git and Wrap Up

```bash
git add .
git commit -m "Bayesian analyses complete"
git push
```

---

> *Bayesian Inference • Python • Google IDX • Firebase • iPad*  
> *MSC Meraviglia — Starlink Maritime*
