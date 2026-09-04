# P vs NP – 9 notebook cells

Paste each block into its own cell in Colab or Jupyter.  
**Cell 1** is a Markdown / Text cell. **Cells 2–9** are Code cells.  
Then: Runtime → Run all.

---

## Cell 1 — Title (Markdown / Text)

```markdown
# P versus NP – Hands-On Demo
The $1,000,000 question in 8 simple live examples
```

---

## Cell 2 — Imports (Code)

```python
# ============================================================
# Cell 2: Import everything we need
# ============================================================
import time, numpy as np, matplotlib.pyplot as plt
from itertools import permutations, combinations
np.random.seed(42)          # makes results reproducible
```

---

## Cell 3 — Primality is in P (Code)

```python
# ============================================================
# Cell 3: Primality testing → this is in P
# We can SOLVE "is this number prime?" very quickly
# ============================================================
def is_prime(n):
    return all(n % i for i in range(2, int(n**0.5) + 1)) if n > 1 else False

print("Is this 13-digit number prime?", 10**12 + 39)
print("Prime?", is_prime(10**12 + 39))
```

---

## Cell 4 — Verification is in NP (Code)

```python
# ============================================================
# Cell 4: Verification is easy → this is why problems are in NP
# Given a candidate solution, we can check it instantly
# ============================================================
print("Does the subset [12, 7, 13] add up to 32?")
print("Answer →", sum([12, 7, 13]) == 32)
```

---

## Cell 5 — Finding a solution is hard (Code)

```python
# ============================================================
# Cell 5: Finding a solution is brutally slow (exponential time)
# ============================================================
def find_subset(nums, target):
    for r in range(len(nums) + 1):
        for combo in combinations(nums, r):
            if sum(combo) == target:
                return list(combo)
    return None

print("Looking for subset that sums to 123...")
print("Found →", find_subset([12, 7, 19, 3, 25, 44, 51, 8, 33, 15, 22, 6], 123))
```

---

## Cell 6 — 2ⁿ explosion (Code)

```python
# ============================================================
# Cell 6: Why NP problems explode → 2ⁿ growth
# ============================================================
n = np.arange(5, 35)
plt.figure(figsize=(11, 4))
plt.plot(n, 2**n, "r-", linewidth=5)
plt.yscale("log")
plt.title("Number of possible subsets = 2ⁿ", fontsize=16)
plt.xlabel("Number of items")
plt.ylabel("Possibilities (log scale)")
plt.grid(alpha=0.3)
plt.show()
```

---

## Cell 7 — If P = NP (Code)

```python
# ============================================================
# Cell 7: What would happen if P = NP were true?
# ============================================================
print("If someone proved P = NP tomorrow, we could instantly:")
print("• Break all current encryption (RSA, Bitcoin, HTTPS)")
print("• Solve perfect scheduling, logistics, protein folding")
print("• Win a million dollars")
print("\n99.9 % of experts believe P ≠ NP")
```

---

## Cell 8 — Traveling Salesman (Code)

```python
# ============================================================
# Cell 8: Traveling Salesman Problem – another famous NP problem
# 10 cities = doable, 15 cities = impossible in practice
# ============================================================
cities = np.random.rand(10, 2)
d = lambda a, b: np.hypot(a[0] - b[0], a[1] - b[1])

best = min(
    sum(d(cities[p[i]], cities[p[i + 1]]) for i in range(9))
    + d(cities[p[9]], cities[p[0]])
    for p in permutations(range(10))
)

print(f"Best route for 10 cities ≈ {best:.1f} units")
print("15 cities → 1.3 trillion routes → no computer can finish")
```

---

## Cell 9 — Summary (Code)

```python
# ============================================================
# Cell 9: The million-dollar summary
# ============================================================
print("P  = problems we can SOLVE fast")
print("NP = problems we can VERIFY fast")
print("\nThe $1,000,000 question:")
print("    Are P and NP the same?")
print("\nCurrent answer: probably NO")
print("Proving it either way wins the Clay Millennium Prize")
```
