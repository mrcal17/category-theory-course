# 5A·P06 — Finite limits from pullbacks and a terminal object

**Type:** stretch · **Technique:** building one universal property from another · **Unlocked by:** `5a_limits` §3, §7
**Source:** adapted from Leinster §5.1

## Statement

Let $\mathcal{A}$ be a category that has a terminal object $1$ and has pullbacks (every pair of
maps with a common codomain has a pullback).

1. Prove that $\mathcal{A}$ has binary products.
2. Prove that $\mathcal{A}$ has equalizers.
3. Conclude that $\mathcal{A}$ has all finite limits, quoting the results of 5A §7.

## What you may use

- The definitions of product, equalizer and pullback (5A §1–§3).
- Proof 3 of the lecture (a pullback over a terminal object is a product).
- From 5A §7: a category with finite products and equalizers has finite limits; a category with
  a terminal object and binary products has finite products.
- Once part 1 is done, you may use binary products freely in part 2, including the fact that a
  map into a product is determined by its two components.

## What a complete proof must show

- [ ] Part 1: which pullback is taken, and why its universal property is that of a product.
- [ ] Part 2: an explicit pullback square is written down (which two maps, with which common
      codomain), and a candidate equalizer map is extracted from it.
- [ ] Part 2: the candidate is a fork.
- [ ] Part 2: for an arbitrary fork, existence of the mediating map and, separately, its
      uniqueness, each deduced from the pullback's universal property.
- [ ] Part 3: one or two sentences assembling the cited results; no new argument.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Part 1 is short and has already been prepared in the lecture. Part 2 is the stretch: you must
*choose* a pullback whose universal property turns into that of an equalizer. Then the proof is
a universal-property proof in which every step is "translate the fork into test data for the
pullback, apply the pullback property, translate back".

</details>

<details>
<summary>Hint 2 — finding the square: think in Set</summary>

In $\mathbf{Set}$ the equalizer of $s, t \colon X \to Y$ is $\{x : s(x) = t(x)\}$. The
condition $s(x) = t(x)$ says that the pair $(s(x), t(x)) \in Y \times Y$ lies in a particular
subset of $Y \times Y$. Which subset? By 5A·P02, the set of $x$ whose image lies in a given
subset is a pullback. Of which two maps?

</details>

<details>
<summary>Hint 3 — making it element-free</summary>

Your answer to Hint 2 involves a map $X \to Y \times Y$ and a map $Y \to Y \times Y$. In a
general category each must be *defined* by the universal property of the product $Y \times Y$:
say what its two components are. Then compute, using those components, what the commuting
condition of the pullback square says about the two projections of the pullback.

</details>

<details>
<summary>Hint 4 — the fork and the test data</summary>

The pullback has two projections, one to $X$ and one to $Y$, but an equalizer is a single map
into $X$. What does the commuting condition tell you about the projection to $Y$ in terms of
the projection to $X$? Use the same observation in reverse to turn a fork $f \colon A \to X$
into a *pair* of maps forming test data for the pullback.

</details>

## Check yourself

- In part 2, did you prove the two maps into $Y \times Y$ equal by comparing components? Did
  you say why that suffices?
- In the uniqueness half, a competitor $g$ is only assumed to satisfy one equation (with the
  projection to $X$). How did you get the second equation needed for the pullback's uniqueness
  clause?
- Check your construction against $\mathbf{Set}$: does it return $\{x : s(x) = t(x)\}$ up to
  bijection?

## Write it up

Write your proof in `proofs/5a/p06_finite_limits_from_pullbacks.md`, then ask Claude to review it.
