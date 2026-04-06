# Bayesian Inference — WORKBOOK

> TypeScript • Google IDX • Firebase • iPad  
> *Background, Theory & 10 Interactive Examples*

---

## Part 0 — Your IDX Workflow

See the main `README.md` for the full startup sequence and toolchain.

### Gemini Prompt Template for This Project

```
I am building a Bayesian analysis tool in vanilla TypeScript in Google IDX.
Full Node.js environment. Use Firebase Web SDK v9 modular imports.
Give me complete index.html, main.ts, and style.css.
Include all imports at the top of each file.
```

---

## Part 1 — What is Bayesian Thinking?

### 1.1 The Origin — Thomas Bayes

Thomas Bayes was an 18th-century English minister who never published his most important idea in his lifetime.
After he died in 1761, his friend Richard Price found a paper describing a method for reasoning backward
from evidence to causes. The core question: *given that I have observed some evidence, what should I believe
about the underlying cause?*

### 1.2 Frequentist vs Bayesian

| | Frequentist | Bayesian |
|---|---|---|
| Probability means | Long-run frequency of repeated events | Degree of belief or certainty |
| Prior knowledge | Ignored — start fresh every time | Explicitly incorporated as a prior |
| Output | p-values, reject or fail to reject | Full probability distribution of beliefs |
| Says about hypothesis | Cannot assign probability | "73% confident this is true" |

### 1.3 Bayes' Theorem

```
P(H | E)  =  P(E | H)  ×  P(H)  /  P(E)
```

| Term | Name | Plain English |
|---|---|---|
| P(H \| E) | Posterior | Your belief AFTER seeing evidence. What you want. |
| P(E \| H) | Likelihood | How well does the hypothesis explain the evidence? |
| P(H) | Prior | Your belief BEFORE seeing any evidence. |
| P(E) | Marginal | Overall probability of seeing this evidence. Normalizing constant. |

**One sentence:** Your updated belief = how well the evidence fits the hypothesis × how plausible the hypothesis was to begin with.

### 1.4 Sequential Updating

One of the most powerful Bayesian properties: the posterior from one analysis becomes the prior for the next.

```
Prior → [Evidence 1] → Posterior 1 → [Evidence 2] → Posterior 2 → ...
```

### 1.5 TypeScript Bayesian Math Helpers

Include these in every Bayesian project:

```typescript
function betaMean(alpha: number, beta: number): number {
  return alpha / (alpha + beta);
}

function betaMode(alpha: number, beta: number): number {
  if (alpha <= 1 || beta <= 1) return alpha > beta ? 1 : 0;
  return (alpha - 1) / (alpha + beta - 2);
}

// Sample from Beta using Gamma method (Box-Muller approximation)
function sampleBeta(alpha: number, beta: number): number {
  const x = sampleGamma(alpha);
  const y = sampleGamma(beta);
  return x / (x + y);
}

function sampleGamma(shape: number): number {
  // Marsaglia and Tsang's method
  if (shape < 1) return sampleGamma(1 + shape) * Math.pow(Math.random(), 1 / shape);
  const d = shape - 1/3, c = 1 / Math.sqrt(9 * d);
  while (true) {
    let x: number, v: number;
    do { x = randomNormal(0, 1); v = 1 + c * x; } while (v <= 0);
    v = v * v * v;
    const u = Math.random();
    if (u < 1 - 0.0331 * (x * x) * (x * x)) return d * v;
    if (Math.log(u) < 0.5 * x * x + d * (1 - v + Math.log(v))) return d * v;
  }
}

function betaCredibleInterval(alpha: number, beta: number,
    level: number = 0.95, samples: number = 100000): [number, number] {
  const draws = Array.from({ length: samples }, () => sampleBeta(alpha, beta)).sort((a, b) => a - b);
  const tail = (1 - level) / 2;
  return [draws[Math.floor(tail * samples)], draws[Math.floor((1 - tail) * samples)]];
}
```

---

## Part 2 — IDX Project Setup

```bash
cd bayesian
npm init -y
npm install firebase
npm install -g typescript
```

---

## Part 3 — Example 1: Is This Coin Fair?

The perfect starting Bayesian example. You flip a coin 10 times and get 7 heads. How biased is it?

**Model:** Beta-Binomial conjugate. Update rule: `Beta(alpha + heads, beta + tails)`

### Ask Gemini

```
I am building a Bayesian coin fairness analyzer in vanilla TypeScript in Google IDX.
Use the Beta-Binomial conjugate model.
Prior: Beta(alpha, beta). Update: Beta(alpha+heads, beta+tails).

TypeScript interfaces:
  BetaParams { alpha: number, beta: number }
  CoinResult { nFlips: number, nHeads: number, prior: BetaParams,
               posterior: BetaParams, posteriorMean: number,
               ciLow: number, ciHigh: number, probBiased: number }

Requirements:
- Input fields: number of flips and heads
- Sliders for prior alpha and beta (default 2,2 — weakly believes coin is fair)
- Draw prior and posterior curves on Canvas in different colors
- Vertical line at 0.5 (fair coin)
- Animate sequential updating: show belief curve after each individual flip
- Print: posterior mean, 95% credible interval, P(coin biased toward heads)
- Save to Firebase collection 'bayesian_analyses'
  Fields: analysisType='coin_fairness', nFlips, nHeads, posteriorMean,
  ciLow, ciHigh, probBiased, timestamp
- Here is my Firebase config: [paste firebaseConfig]

Give me complete index.html, main.ts, style.css for IDX.
```

> **What to observe:** The posterior curve starts broad (uncertain) and narrows with more data. The peak moves toward 0.7 but gets pulled left by the prior. More flips = narrower, more confident curve.

---

## Part 4 — Example 2: Medical Diagnosis

The most important practical Bayes example. A disease affects 1% of people. Test is 95% accurate.
You test positive. What is the real probability you have the disease?

**The surprising answer: about 16%, not 95%.** The prior (how rare the disease is) dominates.

### Ask Gemini

```
I am building a Bayesian medical diagnosis calculator in vanilla TypeScript in Google IDX.

TypeScript interfaces:
  TestParams { prevalence: number, sensitivity: number, specificity: number }
  DiagnosisResult { params: TestParams, probDiseaseGivenPositive: number,
                    probDiseaseGivenNegative: number }

Requirements:
- Three sliders: prevalence (0-50%), sensitivity (50-100%), specificity (50-100%)
- Calculate P(Disease|Positive) and P(Disease|Negative) live as sliders move
- Draw chart: P(Disease|Positive) vs prevalence from 0% to 50%
  showing how the prior dramatically affects the result
- Show sequential testing: two positive tests in a row
  (posterior from test 1 becomes prior for test 2)
- Results table for 5 preset scenarios: rare disease, moderate, common
- Save all scenarios to Firebase collection 'bayesian_analyses'
  Fields: analysisType='medical_diagnosis', prevalence, sensitivity,
  specificity, probDiseaseGivenPositive, timestamp
- Here is my Firebase config: [paste firebaseConfig]

Give me complete index.html, main.ts, style.css for IDX.
```

---

## Part 5 — Examples 3, 4 & 5

### Example 3: Naive Bayes Spam Filter

```
Build a Naive Bayes spam classifier in vanilla TypeScript in Google IDX.

TypeScript interfaces:
  TrainingEmail { text: string, isSpam: boolean }
  WordCounts { [word: string]: number }
  ClassifierModel { spamCounts: WordCounts, hamCounts: WordCounts,
                    spamTotal: number, hamTotal: number,
                    spamPrior: number, vocab: Set<string> }

Requirements:
- Pre-load 7 spam and 7 ham training emails in the code
- Train using Laplace smoothing (add 1 to all word counts)
- Test input box: type any email and see spam probability live
- Show top 10 most spam-indicative words with their log-odds weights
- Save classifications to Firebase collection 'bayesian_analyses'
  Fields: analysisType='spam_filter', emailPreview, spamProb, verdict, timestamp
- Here is my Firebase config: [paste firebaseConfig]

Give me complete index.html, main.ts, style.css for IDX.
```

### Example 4: Bayesian A/B Testing

```
Build a Bayesian A/B test analyzer in vanilla TypeScript in Google IDX.

TypeScript interfaces:
  Variant { name: string, visitors: number, conversions: number }
  ABTestResult { probBBetter: number, expectedLift: number,
                 ciLow: number, ciHigh: number, recommendation: string }

Requirements:
- Input fields for Variant A and B: visitors and conversions
- Prior: Beta(2, 20) — weakly believes ~8-10% conversion rate
- Use 200,000 Monte Carlo samples to compute P(B > A)
- Draw both posterior distributions on Canvas
- Print: P(B better), expected lift, 95% credible interval for lift
- Recommendation: 'Deploy B' if P(B>A) > 95%, else 'Continue testing'
- Animate distributions updating as input values change
- Save to Firebase collection 'bayesian_analyses'
  Fields: analysisType='ab_test', probBBetter, expectedLift, recommendation, timestamp
- Here is my Firebase config: [paste firebaseConfig]

Give me complete index.html, main.ts, style.css for IDX.
```

> **The Bayesian advantage:** Instead of "p=0.043, reject null hypothesis" you get: "There is an 84% probability that B is better, with an expected 21% lift." That's the answer your stakeholders actually need.

### Example 5: Bayesian Product Rating

```
Build a Bayesian product rating estimator in vanilla TypeScript in Google IDX.
Problem: a product has 6 five-star and 1 one-star review. Naive avg is misleading.
Use Bayesian shrinkage: pull toward prior mean of 3.5 stars (10 pseudo-reviews).

Requirements:
- Input: number of 5-star and 1-star reviews (or full star breakdown)
- Show naive average vs Bayesian estimate side by side
- Animate how Bayesian estimate converges to naive average as reviews grow
- Product ranking table: 5 products with different review counts showing shrinkage
- Save to Firebase collection 'bayesian_analyses'
  Fields: analysisType='product_rating', nReviews, naiveAvg, bayesianEstimate, timestamp
- Here is my Firebase config: [paste firebaseConfig]

Give me complete index.html, main.ts, style.css for IDX.
```

---

## Part 6 — Examples 6, 7 & 8

### Example 6: Changepoint Detection

```
Build a Bayesian changepoint detector in vanilla TypeScript in Google IDX.
Simulate 100 days of sales: first 50 days Poisson rate=20, next 50 days rate=35.
For each possible changepoint day compute the log posterior probability.

Requirements:
- Draw sales time series on Canvas with true changepoint marked
- Draw posterior probability of changepoint at each day
- Show: detected changepoint vs true changepoint
- Button to generate new random data with different changepoint location
- Save to Firebase collection 'bayesian_analyses'
  Fields: analysisType='changepoint', trueChangepoint, detectedChangepoint, timestamp
- Here is my Firebase config: [paste firebaseConfig]

Give me complete index.html, main.ts, style.css for IDX.
```

### Example 7: Bayesian Linear Regression

```
Build a Bayesian linear regression visualizer in vanilla TypeScript in Google IDX.
Generate synthetic data: y = 2x + 1 + noise, 25 points, x from 0 to 10.
Use Gaussian prior N(0, 10^2) on intercept and slope.

Requirements:
- Draw scatter plot of data on Canvas
- Draw posterior mean regression line
- Draw 95% credible band as shaded region around the line
- Show: posterior mean intercept and slope (should be near 1 and 2)
- Button to generate new random data — watch line and band update
- Slider to add more data points — watch uncertainty band narrow
- Save to Firebase collection 'bayesian_analyses'
  Fields: analysisType='linear_regression', posteriorIntercept, posteriorSlope, timestamp
- Here is my Firebase config: [paste firebaseConfig]

Give me complete index.html, main.ts, style.css for IDX.
```

### Example 8: Drug Trial Analysis

```
Build a Bayesian clinical trial analyzer in vanilla TypeScript in Google IDX.
Data: 100 drug patients, 45 recoveries. 100 placebo patients, 30 recoveries.
Use Beta(2,2) priors for both recovery rates.

Requirements:
- Draw posterior distributions for drug rate, placebo rate, and treatment effect
- Use 200,000 Monte Carlo samples to compute all posteriors
- Print: P(drug better than placebo), expected improvement, 95% credible interval
- Sliders to adjust patient counts and recoveries — posteriors update live
- Decision panel: STRONG (>95%), MODERATE (80-95%), WEAK (<80%)
- Save to Firebase collection 'bayesian_analyses'
  Fields: analysisType='drug_trial', probDrugBetter, expectedImprovement,
  ciLow, ciHigh, decision, timestamp
- Here is my Firebase config: [paste firebaseConfig]

Give me complete index.html, main.ts, style.css for IDX.
```

---

## Part 7 — Examples 9 & 10

### Example 9: Hierarchical Model — Campaign Comparison

```
Build a hierarchical Bayesian campaign analyzer in vanilla TypeScript in Google IDX.
Campaign data (visitors, conversions):
  A:(1000,52) B:(800,35) C:(50,8) D:(1200,67)
  E:(30,10)  F:(900,41) G:(600,33) H:(25,0)

Requirements:
- Show naive rate vs Bayesian shrinkage estimate for each campaign
- Shrinkage pulls small-sample campaigns (C,E,H) toward the group mean
- Use Beta-Binomial hierarchical model with group prior
- Draw grouped bar chart: naive vs Bayesian estimate per campaign
- Highlight small-sample campaigns — show how much they were shrunk
- Add campaigns via input fields — model updates automatically
- Save all results to Firebase collection 'bayesian_analyses'
  Fields: analysisType='hierarchical_campaigns', campaignName,
  naiveRate, bayesianRate, nVisitors, timestamp
- Here is my Firebase config: [paste firebaseConfig]

Give me complete index.html, main.ts, style.css for IDX.
```

> **Shrinkage:** Campaign H has 0/25 conversions — the hierarchical model gives it a non-zero estimate instead of exactly 0%. This is automatic correction for small-sample noise.

### Example 10: Bayesian Sales Forecast

```
Build a Bayesian sales forecaster in vanilla TypeScript in Google IDX.
Generate 24 months training data: sales = 100 + 3.5*month + normal noise(std=12).
Fit Bayesian linear regression and forecast the next 12 months.

Requirements:
- Draw training data scatter plot on Canvas
- Draw posterior mean forecast line for months 25-36
- Draw 90% prediction interval as shaded band
- Show: expected sales in months 30, 33, 36 with 90% intervals
- Slider to add/remove training data — watch forecast uncertainty change
- Save to Firebase collection 'bayesian_analyses'
  Fields: analysisType='sales_forecast', posteriorSlope,
  forecastMonth36Mean, forecastMonth36CiLow, forecastMonth36CiHigh, timestamp
- Here is my Firebase config: [paste firebaseConfig]

Give me complete index.html, main.ts, style.css for IDX.
```

---

## Part 8 — Query Your Analysis History

### Ask Gemini

```
Build a Bayesian analysis history dashboard in vanilla TypeScript in Google IDX.
Read all documents from Firebase Firestore collection 'bayesian_analyses' and show:
- Summary table: analysis type, key result, timestamp — newest first
- Filter buttons by analysis type
- For coin_fairness: chart of posteriorMean over time
- For ab_test: list of recommendations
- For drug_trial: probDrugBetter trend
- Count of analyses per type
Use Firebase Web SDK v9. Here is my firebaseConfig: [paste]
Give me complete index.html, main.ts, style.css for IDX.
```

---

## Quick Reference

### Key Terms

| Term | Plain English |
|---|---|
| Prior | Your belief before seeing data |
| Posterior | Your updated belief after seeing data |
| Credible interval | A range containing the true value with X% probability |
| Conjugate prior | A prior that keeps the posterior in the same family — gives a fast analytical answer |
| Shrinkage | Hierarchical models pull group estimates toward the overall mean |
| Likelihood | How well the hypothesis explains the observed data |

### Troubleshooting

| Problem | Gemini Prompt |
|---|---|
| TypeScript error | I have this error in IDX: [paste error]. Here is my code: [paste]. Fix the type issue. |
| Canvas not drawing | My distribution curve is not showing. Here is my drawing function: [paste]. What is wrong? |
| Firebase not saving | My addDoc is failing: [paste error]. Here is my Firebase setup: [paste]. Fix it. |
| Wrong posterior | My posterior looks too narrow or too wide. Here is my update code: [paste]. Fix the math. |
| Sliders not updating | Moving the slider does not update the chart. Here is my event handler: [paste]. Fix the reactivity. |

---

## Git and Wrap Up

```bash
git add .
git commit -m "Bayesian analyses complete with Firebase"
git push
```

---

> *Bayesian Inference • TypeScript • Google IDX • Firebase • iPad*  
> *MSC Meraviglia — Starlink Maritime*
