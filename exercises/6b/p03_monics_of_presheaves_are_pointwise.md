# 6B·P03 — Monics of presheaves are pointwise

**Type:** core · **Technique:** pointwise argument · **Unlocked by:** `6b_presheaf_limits` §2
**Source:** adapted from Leinster §6.2

## Statement

Let $\mathcal{A}$ be a small category and $\alpha \colon X \Rightarrow Y$ a map in the presheaf
category $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$.

Prove that $\alpha$ is monic in $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ if and only if, for every
object $A$ of $\mathcal{A}$, the function $\alpha_A \colon X(A) \to Y(A)$ is injective.

## What you may use

- The definition of monic (1B), and that the monics of $\mathbf{Set}$ are the injective functions.
- From 5A (its brief P04): a map $f \colon X \to Y$ is monic if and only if the square with
  $1_X, 1_X$ along two sides and $f, f$ along the other two is a pullback.
- Theorem 1 and Corollary 1 of the lecture.

## What a complete proof must show

- [ ] Both directions, kept separate.
- [ ] In the direction from "pointwise injective" to "monic": two natural transformations are shown equal by comparing components.
- [ ] In the direction from "monic" to "pointwise injective": exactly which result moves a statement about $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ to a statement about $\mathbf{Set}$ at each $A$, and why its hypotheses hold.

## Hints — one at a time

<details>
<summary>Hint 1 — the two directions are not equally hard</summary>

One direction follows from the definition of monic together with the fact that natural
transformations are equal when their components are. Do that one first. For the other, ask
yourself why you cannot simply "evaluate a monic at $A$": what would you need to know about the
functor $\mathrm{ev}_A$?

</details>

<details>
<summary>Hint 2 — turn monic into a limit</summary>

Functors do not preserve monics in general, but this module is full of results about functors
preserving *limits*. Which fact from 5A rephrases "monic" as a statement about a limit?

</details>

<details>
<summary>Hint 3 — choose the right result</summary>

You now have a limit cone in the functor category and want a limit cone at each $A$. Theorem 1(b)
goes from pointwise to global; you need the other direction. Which statement in the lecture gives
that, and what does it require of $\mathbf{Set}$?

</details>

## Check yourself

- Did you use that the target category is $\mathbf{Set}$? Which step would need rethinking for $[\mathcal{A}, \mathcal{S}]$ with $\mathcal{S}$ arbitrary?
- State the dual result about epics. Which facts would its proof need?
- For graphs, what does the result say a monic map of graphs is?

## Write it up

Write your proof in `proofs/6b/p03_monics_of_presheaves_are_pointwise.md`, then ask Claude to review it.
