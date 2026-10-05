# 6C·P03 — Which complete lattices are cartesian closed?

**Type:** core · **Technique:** applying the poset adjoint functor theorem · **Unlocked by:** `6c_adjoints_and_limits` §4, §7
**Source:** adapted from Leinster §6.3

## Statement

Let $L$ be a complete poset: every subset has a meet. (You may use that every subset then also has
a join.) Regard $L$ as a category.

Prove that the following are equivalent:

1. $L$ is cartesian closed;
2. for every $b \in L$ and every subset $S \subseteq L$,
   $$b \wedge \bigvee S \;=\; \bigvee \{\, b \wedge s : s \in S \,\}.$$

## What you may use

- That products in a poset are meets and the terminal object is the greatest element (5A).
- The definition of a cartesian closed category.
- Theorem 2 of the lecture and its dual, stated in Section 6: an order-preserving map out of a
  poset with all joins has a right adjoint if and only if it preserves joins.

## What a complete proof must show

- [ ] That $L$ has finite products.
- [ ] For each $b$, which map must have a right adjoint, and a check that it is order-preserving.
- [ ] What "preserves joins" means for that map, including the case $S = \emptyset$, and how it compares with condition 2.
- [ ] Both directions of the equivalence.

## Hints — one at a time

<details>
<summary>Hint 1 — translate condition 1</summary>

The definition of cartesian closed asks for a right adjoint to a certain functor, one for each
object. In a poset, what is that functor as a function $L \to L$?

</details>

<details>
<summary>Hint 2 — which theorem</summary>

You want to know when an order-preserving map out of a complete poset has a *right* adjoint.
Theorem 2 as stated is about left adjoints and meets. Which version do you need, and what does it
ask the map to preserve?

</details>

<details>
<summary>Hint 3 — hypotheses and edge cases</summary>

Before applying the theorem, check that your map is order-preserving. Then write "preserves
joins" for it explicitly. What does it say when $S$ is empty, and is that case already true in
any poset with a least element?

</details>

## Check yourself

- Does the five-element lattice $M_3$ of the Compute It section satisfy condition 2? Find an explicit $b$ and $S$.
- What is the exponential $c^b$ in terms of joins, when it exists?
- Did you prove an "if and only if", or only one direction twice?

## Write it up

Write your proof in `proofs/6c/p03_distributive_complete_lattices.md`, then ask Claude to review it.
