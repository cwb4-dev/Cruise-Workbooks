---
title: "Monte Carlo Simulation: The Method That Turned Randomness Into Power"
source: "https://medium.com/@vplevris/monte-carlo-simulation-the-method-that-turned-randomness-into-power-64464eba6c29"
author:
  - "[[Vagelis Plevris]]"
published: 2026-03-01
created: 2026-03-17
description: "Monte Carlo Simulation explained: how random sampling estimates integrals, prices options, models risk, and powers modern science and AI."
tags:
  - "monte-carlo"
---

## How a solitaire question at Los Alamos reshaped science, finance, and artificial intelligence

In **1946**, a mathematician lay in bed recovering from a serious illness. He had suffered **encephalitis** and undergone brain surgery. For weeks, he was unsure how sharply his mind would return.

He was not thinking about atomic bombs or advanced physics. He was playing solitaire.

**Stanisław Ulam**, one of the sharpest minds working on the Manhattan Project, began wondering:

> **What are the chances of winning?**

Ulam was thinking specifically about the probability of winning a standard game of **Canfield solitaire**. It is a particularly difficult variant, where all foundations begin from a fixed lead card.

![Screenshot of a Canfield Solitaire game at the beginning of play. A stock pile and empty waste appear in the upper left, four foundation slots are shown at the top with 3 of clubs as the lead card, a vertical reserve stack of 13 face-up cards appears on the left, and four tableau cards (8 of diamonds, 6 of spades, 2 of hearts, 9 of spades) are displayed on a green background.](https://miro.medium.com/v2/resize:fit:640/format:webp/1*e07DR6kFN4xx53Q9NI0Z1Q.png)

Starting layout of a standard Canfield (Demon) Solitaire game. The foundations begin with a lead card (3♣), the reserve contains 13 face-up cards, and four tableau piles are dealt, with the stock and waste in the upper left.

He could have tried to calculate the probability analytically. But it would require tracking **an enormous number of possible card permutations**. The combinatorics explode almost instantly.

Instead, he realized something simpler: the probability of winning is just the fraction of wins over many independent games. Rather than solving the game on paper, **he could estimate the answer by repeated trials**.

He reframed a mathematical problem as an experiment.

That almost casual idea became one of the most powerful computational methods of the twentieth century.

It is now known as the **Monte Carlo method**.

## From Solitaire to the Manhattan Project

**Stanisław Ulam** (1909–1984) was a Polish mathematician and one of the leading thinkers of his generation. He was not an isolated mind idly speculating about card games. Before the war, he belonged to the brilliant **Polish Lwów school of mathematics**, and later became a key figure at Los Alamos. At the Manhattan Project, he worked on some of the most technically demanding problems in theoretical physics.

**The solitaire question was small. The habit of mind behind it was not.**

Ulam’s genius was not in grinding through equations. It was in asking the right question — and then changing the rules of how answers could be found.

![Black-and-white portrait of mathematician Stanisław Ulam wearing a coat, scarf, and hat, standing outdoors in the mid-1940s.](https://miro.medium.com/v2/resize:fit:640/format:webp/1*zoC63qOvRmusuzGjc9cxFQ.jpeg)

Stanisław Ulam, circa 1945. Los Alamos National Laboratory archive. Courtesy of Los Alamos National Laboratory (LANL), via Wikimedia Commons.

After he recovered and returned to Los Alamos, the implications of his bedside reflection became clearer. What had begun as a quiet thought experiment about solitaire now collided with urgent scientific challenges.

Ulam shared the idea with **John von Neumann** (1903–1957), the brilliant and famously eccentric mathematician helping shape early computational science. **Von Neumann immediately recognized its power**.

![Black-and-white portrait of mathematician John von Neumann wearing a suit and patterned tie, looking slightly to the side against a neutral background.](https://miro.medium.com/v2/resize:fit:640/format:webp/1*0sf3oBN1wCEDTu5Q00zvqw.jpeg)

John von Neumann, portrait from the Los Alamos National Laboratory archives. Courtesy of Los Alamos National Laboratory (LANL), via Wikimedia Commons.

Von Neumann saw more than a clever probabilistic trick. He saw a **computational revolution**. Monte Carlo methods were hungry for repetition. Thousands of simulated neutron paths could not be followed by hand, but electronic computers could perform them relentlessly.

**The emerging machines at Los Alamos suddenly had a purpose.**

The name “ **Monte Carlo** ” was a nod to the casino in Monaco, where outcomes depend on repeated random trials. But this was not about gambling. It was about neutrons.

Designing nuclear systems required understanding how particles move, scatter, and multiply inside complex materials. The governing equations were extraordinarily difficult, often resistant to exact analytical solutions.

Ulam’s insight offered a new path. Instead of solving the equations directly, simulate the physical process many times using randomness, then measure the statistical outcome.

**The idea was radical. It changed what it meant to ‘solve’ a problem.**

## The Core Idea

At its heart, Monte Carlo follows a remarkably simple structure.

**First**, define the space of all possible inputs. This could be the possible arrangements of cards, the potential paths of a neutron, the range of future stock prices, or the uncertain loads acting on a bridge.

**Second**, sample randomly from that space according to a specified probability distribution. Each sample represents one possible realization of the system.

**Third**, compute the outcome deterministically for that realization. There is no randomness in the evaluation itself — the randomness lies only in the input.

**Finally**, average the outcomes across many such realizations.

**What emerges from this repetition is not noise, but signal.**

The reason this works is mathematical. If *X* ₁, *X* ₂, …, *X* ₙ are independent samples from the same distribution, then

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*IkT-vbqH-4moV_Gqm_X_UA.png)

By the ***Law of Large Numbers***, the average of many independent random samples converges toward the expected value. The more samples we generate, the closer the empirical average approaches the true quantity we seek.

Each individual sample may look erratic. One simulated outcome may collapse, another may surge. A single realization can deviate wildly from the average. Yet when thousands or millions of such realizations are combined, fluctuations begin to cancel out. The noise diminishes, and a stable pattern gradually emerges.

Monte Carlo does not eliminate randomness. It harnesses it.

The power is not in a single draw, but in disciplined repetition.

## The Dartboard Principle: Estimating π

The cleanest illustration of Monte Carlo is estimating *π*.

Draw a square of side length 1. Inside it, inscribe a quarter circle of radius 1, as shown in the figure.

![Diagram of a square with side length 1 and a quarter circle of radius 1 drawn inside it from the lower-left corner. The quarter circle region is shaded in green and labeled Aqc = π/4. A dashed red line indicates the radius r = 1.](https://miro.medium.com/v2/resize:fit:640/format:webp/1*4jLrjLwFKltvmoQJICSQVw.png)

A unit square of side a = 1 with an inscribed quarter circle of radius r = 1.

The area of the square is 1. **The area of the quarter circle is π/4**.

The ratio of areas is:

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*KMdsmPSdyvJB-TTtXL7D3A.png)

**Now imagine you are blindfolded, throwing darts at this square**. Each dart lands at a random point.

Some fall inside the quarter circle. Some fall outside.

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*us2c9rjwCkWXyFSUgRBG3Q.png)

Blindfolded dart throwing as a metaphor for Monte Carlo sampling inside a unit square with an inscribed quarter circle (a = 1, r = 1).

If the points are **uniformly distributed**, the fraction that land inside the curved region must equal the ratio of the areas:

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*ajdkIWL65uoeeF7K6qtixg.png)

Multiply by 4, and you obtain an estimate of π.

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*vGiUGNRWkq8f_TiSSAAOBQ.png)

To make this concrete, let us actually perform the experiment.

In the animation below, **2,000 random points** are generated uniformly inside the unit square. Each point is classified immediately: **green** if it falls inside the quarter circle, **red** if it falls outside. At the same time, the running estimate of *π* is updated after every new sample.

![Animated visualization of a Monte Carlo simulation for estimating pi. The top panel shows random green and red points inside a unit square with a quarter circle arc, distinguishing points inside and outside the circle. The bottom panel displays a graph of the estimated value of pi converging toward the true value as the number of samples increases, along with live statistics for samples, error, and accuracy.](https://miro.medium.com/v2/resize:fit:640/format:webp/1*PnSv_xhf45cC9fYKavlKqA.gif)

Animated Monte Carlo simulation estimating π. Random points are generated inside a unit square, classified as inside or outside the quarter circle, while the running estimate converges toward the true value of π.

Notice what happens in the early stages. The estimate fluctuates wildly. With only a few dozen points, randomness dominates. The curve overshoots, undershoots, and oscillates.

But as the number of samples grows, the noise begins to average out. The estimate stabilizes. The fluctuations shrink. Order slowly emerges from randomness.

By the end of this run, **after 2,000 samples**, the simulation produces ***π* ≈ 3.144**. The true value is ***π* ≈ 3.141593**. The absolute error is approximately 0.0024, corresponding to an accuracy of about **99.923%**.

There is no closed-form geometry being evaluated. No infinite series. No symbolic integration. **We simply counted.**

What is remarkable is not that the method works once. It is that it works consistently. If you repeat the experiment, you will not obtain exactly 3.144 again. You will obtain a slightly different value. But with enough samples, it will almost always hover close to 3.141593.

**This is Monte Carlo in its purest form: randomness revealing structure.**

## Why It Works

The dartboard example is not a trick. It is a manifestation of a deeper principle.

Suppose we want to compute a definite integral:

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*P1s0oOWhOIivkI39sm9kVA.png)

If this integral is difficult or impossible to evaluate analytically, we can reinterpret it probabilistically.

Let *X* be a random variable uniformly distributed on \[*a*, *b*\]. Then

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*5N8YbSLKvYpUEdbtnzma0Q.png)

Rearranging gives

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*Gid-UD9D0EAJHTw0F6tLGA.png)

Now draw samples *x* ₁, *x* ₂, …, *x* ₙ independently and uniformly from \[*a*, *b*\]. The Monte Carlo estimator becomes

![](https://miro.medium.com/v2/resize:fit:640/format:webp/1*mGd1qAffnWOrb8pG18S4Cg.png)

In plain language: you can estimate the integral by averaging *f* at random points, then multiplying by the interval length (*b* − *a*)

**No derivatives. No symbolic integration. Just averaging.**

And here is the remarkable part: **the convergence rate with respect to sample size does not deteriorate with dimension**. In very high-dimensional problems, where classical grid-based methods collapse under combinatorial explosion, Monte Carlo continues to work.

It changed what “solving” means. A solution is no longer a closed-form expression. It can be an estimate with quantifiable uncertainty.

## The Invisible Engine Powering Modern Life

Monte Carlo methods quietly power much of the modern world.

In **physics**, they simulate the random paths of billions of particles. Designing a nuclear reactor is not done by building one and hoping it behaves. Physicists simulate neutron collisions repeatedly, one random interaction at a time, and measure statistical outcomes.

In **finance**, Monte Carlo is used to price options and assess risk. When analysts price a complex derivative, they do not predict one future stock path. They simulate thousands of possible future paths, compute the payoff in each scenario, discount them, and average the results. The output is not a single prediction, but a distribution of possibilities.

In **engineering**, Monte Carlo methods quantify reliability. Uncertainty in loads, material properties, geometry, and boundary conditions is propagated through computational models. The result is a probability distribution of failure margins rather than a single deterministic number.

In **artificial intelligence**, the method appears in striking form. When systems like AlphaGo evaluate a move, they do not calculate every possible continuation. That would be impossible. Instead, they use Monte Carlo Tree Search: from a given position, they simulate thousands of random future games and choose the move that statistically wins more often. Random playouts guide strategic intelligence.

What began as a solitaire thought experiment now underlies supercomputers and machine learning systems.

## The Deeper Insight

Monte Carlo is not about chaos. It is about discipline applied to randomness.

It acknowledges something fundamental:

> **Many real-world systems are too complex for closed-form mathematics.**

Instead of forcing exact solutions, we simulate reality repeatedly and measure what emerges.

Accuracy improves with sample size.  
Uncertainty becomes measurable.  
Randomness becomes a computational tool.

But there is something deeper here.

For centuries, science pursued certainty. The ideal solution was exact, symbolic, and closed-form. **Monte Carlo accepts something humbler: not certainty, but confidence levels**. Not a single prediction, but a probability distribution.

It reflects a psychological shift as much as a mathematical one. We no longer demand perfect foresight. We ask instead: how likely is this outcome? What is the range of possibilities? What is the risk?

**In that sense, Monte Carlo mirrors modern decision-making itself**. We live under uncertainty, with incomplete information, and still must act. The method does not eliminate uncertainty. It quantifies it.

That is a profound change in what it means to ‘know’ something.

## The Trade-Off

Monte Carlo methods are not magic.

The typical statistical error decreases on the order of 1/√n. **Achieving ten times more accuracy requires roughly one hundred times more samples**. High precision can demand substantial computational power. And poor random number generation can introduce subtle biases that quietly corrupt results.

**Yet computational power has grown dramatically**. Parallel processors and high-performance computing systems now generate millions or billions of samples efficiently. Problems once considered intractable are simulated routinely.

The method scaled with the machines.

## From Casino to Supercomputers

There is an irony in all this.

An idea inspired by a card game now powers space mission reliability analysis, nuclear safety models, financial risk systems, climate simulations, and artificial intelligence.

**Monte Carlo stands among the most influential computational ideas of the twentieth century.**

It taught us something fundamental.

When exact mathematics fails, statistics can succeed. And sometimes, the fastest path to order runs straight through randomness.

A mathematician recovering in bed once asked how often he might win a card game.

In answering that question, he helped humanity learn how to think in probabilities.

[![Vagelis Plevris](https://miro.medium.com/v2/resize:fill:96:96/1*9Uh2XP9RGqY7CShmIxSouA.jpeg)](https://medium.com/@vplevris?source=post_page---post_author_info--64464eba6c29---------------------------------------)

Structural engineer, professor and science communicator making complex ideas simple. Passionate about research, teaching and improving lives through knowledge.

## Responses (14)

Charles Bartlett

```c
Loved every bit of this article. Keep creating amazing content!
```

10

```c
True, and kind of obvious at this stage of development, but presumably not in 1946! Stanislaw Ulam also wrote science fiction, well.Thank you, and really you could compile all your expositions into a book. It would be excellent value.
```

12

```c
I have now been reading at least 3 full articles from you, enjoying everyone of them and thinking they provide great value, just to realize I did not even follow you yet, that for sure deserves a follow, and many claps 👏😎
```

7
