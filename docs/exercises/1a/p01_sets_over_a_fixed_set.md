# 1A·P01 — Sets over a fixed set form a category

**Type:** warm-up · **Technique:** verifying axioms (closure) · **Unlocked by:** `1a_categories` §2
**Source:** adapted from Leinster §1.1 (the checklist) and Riehl §1.1; the example is a slice category, which returns in 2C

## Statement

Fix a set $S$. A **set over $S$** is a pair $(A, a)$ consisting of a set $A$ and a function
$a \colon A \to S$. A **map over $S$** from $(A, a)$ to $(B, b)$ is a function
$f \colon A \to B$ such that

$$b \circ f = a.$$

Prove that sets over $S$ and maps over $S$, with composition of functions as composition and
identity functions as identities, form a category.

(As in `1a_categories` §3, an arrow knows its domain and codomain: officially an arrow is a
triple $((A, a), (B, b), f)$, because the same function $f$ can be a map over $S$ between
several different pairs. You may leave this implicit.)

## What you may use

- The definition of a category and the four-item "verify" checklist from `1a_categories` §1.
- Proposition 2 of 0B: composition of functions is associative, and
  $f \circ 1_A = f = 1_B \circ f$ for every function $f \colon A \to B$.
- Proposition 2.1 of the lecture as a model for the layout. Its closure argument does not
  transfer: there the condition on an arrow was about elements, here it is an equation between
  functions.

## What a complete proof must show

- [ ] For all maps over $S$, $f \colon (A, a) \to (B, b)$ and $g \colon (B, b) \to (C, c)$, the function $g \circ f$ satisfies the condition to be a map over $S$ from $(A, a)$ to $(C, c)$. The condition is written out before it is proved.
- [ ] For every set over $S$, the identity function satisfies the condition to be a map from that object to itself.
- [ ] Associativity and both identity laws hold, with a reason given.
- [ ] Each equality names what justifies it: associativity of composition of functions, an identity law, "$f$ is a map over $S$" or "$g$ is a map over $S$".

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

This is a direct proof by unpacking a definition. Before writing anything, list what the
definition of a category asks you to verify, and decide which items have content here and
which are inherited from facts about functions.

</details>

<details>
<summary>Hint 2 — what closure says here</summary>

Write down, as a single equation between functions, what it means for $g \circ f$ to be a map
over $S$ from $(A, a)$ to $(C, c)$. Then write down the two equations you are given. Which
functions appear in the goal and in a hypothesis?

</details>

<details>
<summary>Hint 3 — no elements needed</summary>

The goal and both hypotheses are equations between composites, so this can be an equation
chase in the style of 0C §6. One law of Proposition 2 of 0B makes a hypothesis usable; say
which, and say in which order the two hypotheses get used.

</details>

## Check yourself

- Did you use each of the two hypotheses exactly once, and name the law that let you use it?
- For the identity function, which of the two identity laws did you need?
- Draw a map over $S$ as a triangle. What does your closure argument look like as a picture?
- What is this category when $S$ is a one-element set? What are its objects when $S = \emptyset$?

## Write it up

Write your proof in `proofs/1a/p01_sets_over_a_fixed_set.md`, then ask Claude to review it.
