# 5A·P01 — Meets are products

**Type:** warm-up · **Technique:** unpacking a universal property in a poset · **Unlocked by:** `5a_limits` §1
**Source:** adapted from Leinster §5.1

## Statement

Let $(P, \le)$ be a poset, regarded as a category in the usual way: its objects are the
elements of $P$, and there is exactly one arrow $a \to b$ when $a \le b$ and no arrow otherwise.
Let $x, y, m \in P$.

Prove that the following two statements are equivalent.

1. $m \le x$ and $m \le y$, and the object $m$ together with the arrows $m \to x$ and $m \to y$
   is a product of $x$ and $y$ in this category.
2. $m$ is a **greatest lower bound** (a *meet*) of $x$ and $y$: $m \le x$, $m \le y$, and for every
   $a \in P$ with $a \le x$ and $a \le y$ we have $a \le m$.

## What you may use

- The definition of a binary product (5A §1).
- The description of a poset as a category (1A): between any two objects there is at most one arrow.
- Nothing else: in particular, do not assume that meets exist in $P$.

## What a complete proof must show

- [ ] Both directions, (1) $\Rightarrow$ (2) and (2) $\Rightarrow$ (1), each labelled.
- [ ] In (2) $\Rightarrow$ (1): the existence of the mediating arrow **and** its uniqueness are
      argued separately, and each is justified.
- [ ] The two equations $p_1 \bar{f} = f_1$ and $p_2 \bar{f} = f_2$ are addressed, with a reason
      why they hold.
- [ ] It is said explicitly what "a map $A \to X$" means in this category.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

This is an "if and only if" between a universal property and an order-theoretic condition.
Each direction is a translation exercise: write the definition of product with every object
replaced by an element of $P$ and every arrow replaced by an inequality. What does the phrase
"a pair of maps $f_1 \colon a \to x$, $f_2 \colon a \to y$" become?

</details>

<details>
<summary>Hint 2 — existence</summary>

In a poset, what does it mean for an arrow $a \to m$ to *exist*? Which clause of statement (2)
talks about exactly that?

</details>

<details>
<summary>Hint 3 — uniqueness and the equations</summary>

The definition of product asks for two equations between arrows and for a uniqueness
statement. How many arrows are there from $a$ to $x$ in a poset? What does that tell you about
any equation between two arrows with the same domain and codomain, and about uniqueness?

</details>

## Check yourself

- Did you use anywhere that $\le$ is antisymmetric? Should you have needed to?
- If $m$ and $m'$ are both meets of $x$ and $y$, what does the uniqueness theorem of 5A §5 say,
  and what does it become in a poset?
- What is the product of $12$ and $18$ in the natural numbers ordered by divisibility?

## Write it up

Write your proof in `proofs/5a/p01_meets_are_products.md`, then ask Claude to review it.
