# 2B·P02 — The other composite of a Galois connection

**Type:** warm-up · **Technique:** dualizing a lecture proof · **Unlocked by:** `2b_units_counits` §6
**Source:** adapted from Leinster §2.2

## Statement

Let $P$ and $Q$ be posets and let $f \colon P \to Q$ and $g \colon Q \to P$ be
order-preserving maps with $f \dashv g$. Proposition 5 of the lecture studied the composite
$g \circ f$ on $P$. This exercise is about the composite $d = f \circ g \colon Q \to Q$.

1. Prove that $g \circ f \circ g = g$.
2. Prove that $d$ is order-preserving, that $d(b) \le b$ for every $b \in Q$, and that
   $d(d(b)) = d(b)$ for every $b \in Q$.
3. Prove that an element $b \in Q$ satisfies $d(b) = b$ if and only if $b = f(a)$ for some
   $a \in P$.

## What you may use

- The boxed criterion of 2B §6: $a \le g(f(a))$ for all $a \in P$, and $f(g(b)) \le b$ for all
  $b \in Q$.
- That $f$ and $g$ are order-preserving; reflexivity, transitivity and antisymmetry of $\le$.
- The equation $f \circ g \circ f = f$ from Proposition 5.
- Proposition 5 as a *model*. Its proof is about $P$; yours is about $Q$.

## What a complete proof must show

- [ ] Part 1 proves two inequalities and says where antisymmetry is used; for each inequality it says which hypothesis (unit or counit) is applied, and at which element.
- [ ] Part 2 addresses the three properties separately, for arbitrary elements of $Q$.
- [ ] Part 3 proves both directions of the "if and only if".
- [ ] No step quotes "by duality" without an argument.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Proposition 5 obtained an equation in $Q$ from two inequalities, one from applying a map to a
unit inequality and one from a counit inequality at a well-chosen element. Part 1 is the same
with the roles of unit and counit exchanged, and the equation now lives in $P$.

</details>

<details>
<summary>Hint 2 — part 1</summary>

You want $g(f(g(b))) \le g(b)$ and $g(b) \le g(f(g(b)))$. One of these is a unit or counit
inequality *as it stands*, at a particular element. The other is what you get by applying an
order-preserving map to a unit or counit inequality. Which is which?

</details>

<details>
<summary>Hint 3 — parts 2 and 3</summary>

Idempotence should cost one line once part 1 is available: what do you apply to both sides of
the equation in part 1? For part 3, one direction is immediate from the form of $d$; for the
other you need to simplify $f(g(f(a)))$, and you were told you may use an equation that does
so.

</details>

## Check yourself

- In part 1, did you use the unit at an element of $P$ of the form $g(b)$? Did you say so?
- Which of the three properties in part 2 differs from the corresponding property of a closure operator, and how?
- For the Galois connection $h_* \dashv h^*$ of a function $h \colon K \to L$: what is $d(T)$ for $T \subseteq L$, in words? Which subsets satisfy $d(T) = T$?
- For "closure $\dashv$ inclusion" on a topological space, what is $d$? (It is not the interior operator; why not?)

## Write it up

Write your proof in `proofs/2b/p02_interior_operator.md`, then ask Claude to review it.
